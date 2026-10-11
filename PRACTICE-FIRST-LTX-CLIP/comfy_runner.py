"""Start, monitor and stop one owned ComfyUI stage."""
from pathlib import Path
from datetime import datetime
import argparse,hashlib,json,os,socket,subprocess,sys,time,urllib.error,urllib.request
import psutil

KIT=Path(__file__).resolve().parent

def read(path):return json.loads(Path(path).read_text('utf-8-sig'))
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(2**20),b''):h.update(block)
    return h.hexdigest()
def identity(p):return dict(pid=p.pid,created=p.create_time(),command=p.cmdline())
def occupied(port):
    with socket.socket() as s:
        s.settimeout(.3);return s.connect_ex(('127.0.0.1',port))==0
def request(base,path,payload=None):
    req=urllib.request.Request(base+path,data=None if payload is None else json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=20) as response:return json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f'ComfyUI returned HTTP {exc.code}: '+exc.read().decode('utf-8','replace')) from exc

def stop_owned(process,expected):
    if process.poll() is not None:return
    parent=psutil.Process(process.pid)
    assert parent.create_time()==expected['created'] and parent.cmdline()==expected['command']
    owned=[(p,identity(p)) for p in parent.children(recursive=True)]+[(parent,expected)]
    for p,proof in owned:
        try:
            assert p.create_time()==proof['created'] and p.cmdline()==proof['command'];p.terminate()
        except psutil.NoSuchProcess:pass
    for p,proof in owned:
        try:p.wait(10)
        except psutil.TimeoutExpired:
            assert p.create_time()==proof['created'] and p.cmdline()==proof['command'];p.kill();p.wait(10)
        except psutil.NoSuchProcess:pass


def stage(args,root,name,graph,extra_options):
    if occupied(args.port):raise RuntimeError('Chosen port is in use; no existing server will be stopped')
    base=f'http://127.0.0.1:{args.port}'
    command=[str(args.python),'main.py','--listen','127.0.0.1','--port',str(args.port),'--disable-pinned-memory','--input-directory',str(root/'input'),'--output-directory',str(root/'output'),'--user-directory',str(root/'user'),'--extra-model-paths-config',str(root/'extra-model-paths.yaml')]+extra_options
    env=os.environ.copy();env.update(PYTHONUTF8='1',OMP_NUM_THREADS='2',MKL_NUM_THREADS='2')
    proof=dict(name=name,request=graph,command=command,status='starting',started_at=datetime.now().astimezone().isoformat())
    path=root/(name+'-REPORT.json')
    def save():path.write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    def healthy():
        if process.poll() is not None:raise RuntimeError('Owned ComfyUI exited; read '+str(root/(name+'.log')))
        free=psutil.virtual_memory().available/2**30
        with (root/(name+'-RAM.csv')).open('a',encoding='utf-8') as sample:
            sample.write(f'{time.time():.3f},{free:.6f}\n')
        proof['minimum_available_windows_ram_gib']=min(proof.get('minimum_available_windows_ram_gib',free),free)
        if free<.25:
            proof.setdefault('critical_since',time.monotonic())
            if time.monotonic()-proof['critical_since']>=5:raise RuntimeError('Windows RAM below 256 MiB for five seconds; stopping this owned process')
        else:proof.pop('critical_since',None)
    with (root/(name+'.log')).open('w',encoding='utf-8') as log:
        flags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0
        process=subprocess.Popen(command,cwd=args.comfyui,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=flags)
    proof['launcher']=identity(psutil.Process(process.pid));save()
    try:
        deadline=time.monotonic()+180
        while time.monotonic()<deadline:
            healthy()
            try:stats=request(base,'/system_stats');break
            except (urllib.error.URLError,TimeoutError):time.sleep(.5)
        else:raise RuntimeError('Startup exceeded three minutes')
        tree={process.pid}|{p.pid for p in psutil.Process(process.pid).children(recursive=True)}
        owners={c.pid for c in psutil.net_connections(kind='tcp') if c.status=='LISTEN' and c.laddr.port==args.port}
        if not owners or not owners.issubset(tree):raise RuntimeError('Port does not belong to the process we started')
        proof['system_stats']=stats
        queue=request(base,'/queue')
        assert not queue['queue_running'] and not queue['queue_pending']
        schema=request(base,'/object_info')
        for node in graph.values():
            if node['class_type'] not in schema:raise RuntimeError('Missing node: '+node['class_type'])
        started=time.monotonic();response=request(base,'/prompt',{'prompt':graph,'client_id':'dolmario-first-ltx'})
        prompt_id=response['prompt_id'];proof.update(prompt_id=prompt_id,status='running');save()
        deadline=time.monotonic()+args.timeout
        while time.monotonic()<deadline:
            healthy();history=request(base,'/history/'+prompt_id)
            if prompt_id in history:
                result=history[prompt_id];proof['history']=result
                if result.get('status',{}).get('status_str')!='success':raise RuntimeError('Prompt failed: '+str(result.get('status')))
                break
            time.sleep(1)
        else:raise RuntimeError('Prompt exceeded the chosen timeout')
        outputs=[]
        for value in result.get('outputs',{}).values():
            for kind in ('images','videos','gifs'):
                for item in value.get(kind,[]):
                    actual=(root/'output'/item.get('subfolder','')/item['filename']).resolve()
                    if not actual.is_relative_to((root/'output').resolve()) or not actual.is_file():raise RuntimeError('Unexpected result path')
                    outputs.append(dict(path=str(actual),kind=kind,sha256=sha(actual),bytes=actual.stat().st_size))
        if name=='00-text':
            for label in ('positive','negative'):
                actuals=list((root/'output/conditioning').glob('first-clip-'+label+'_*.safetensors'))
                if len(actuals)!=1:raise RuntimeError('Expected one new conditioning file for '+label)
                file=actuals[0];target=root/'embeddings'/('first-clip-'+label+'.safetensors');target.write_bytes(file.read_bytes())
                outputs.append(dict(path=str(target),kind='conditioning',sha256=sha(target),bytes=target.stat().st_size))
        if not outputs:raise RuntimeError('ComfyUI returned no result files')
        proof.update(status='completed',seconds=time.monotonic()-started,outputs=outputs);save();return outputs
    except BaseException as exc:
        proof.update(status='failed',error=str(exc));save();raise
    finally:
        stop_owned(process,proof['launcher']);proof['owned_process_stopped']=True;save()


