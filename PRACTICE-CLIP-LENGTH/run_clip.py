"""Run the supplied LTX graph in an owned ComfyUI process using existing verified models."""
from pathlib import Path
import argparse,json,os,subprocess,sys
import psutil
import comfy_runner as runner
KIT=Path(__file__).resolve().parent
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--comfyui',type=Path,required=True);parser.add_argument('--python',type=Path,default=Path(sys.executable));parser.add_argument('--models',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--port',type=int,default=18201);parser.add_argument('--timeout',type=int,default=3600);parser.add_argument('--check',action='store_true');parser.add_argument('--frames',type=int,choices=[121,241],default=241);args=parser.parse_args()
    args.comfyui=args.comfyui.resolve();args.python=args.python.resolve();args.models=args.models.resolve();root=args.output.resolve()
    if not(args.comfyui/'main.py').is_file()or not args.python.is_file():raise RuntimeError('Supply the installed ComfyUI source and existing AMD Python executable')
    graph=runner.read(KIT/'01-CLIP.api.json');graph['11']['inputs']['length']=args.frames;graph['13']['inputs']['frames_number']=args.frames
    for n in graph.values():
        for value in n['inputs'].values():
            if isinstance(value,list)and len(value)==2 and isinstance(value[0],str)and value[0]not in graph:raise RuntimeError('Broken graph connection')
    models=[]
    for model in runner.read(KIT/'MODELS.json')['models']:
        file=args.models/model['path']
        if not file.is_file()or file.stat().st_size!=model['bytes']or runner.sha(file)!=model['sha256']:raise RuntimeError('Model file differs: '+str(file))
        models.append(model);print('FULL MODEL SHA OK',model['path'],flush=True)
    for asset in runner.read(KIT/'BASELINE-ASSETS.json')['assets']:
        file=KIT/asset['path']
        if not file.is_file() or file.stat().st_size!=asset['bytes'] or runner.sha(file)!=asset['sha256']:raise RuntimeError('Supplied baseline asset differs: '+str(file))
    if args.check:print('Four model files and graph connections checked; no inference.');return
    if root.exists():raise RuntimeError('Choose a new output folder')
    if runner.occupied(args.port):raise RuntimeError('Chosen port is already occupied; no existing server is stopped')
    if psutil.virtual_memory().available/2**30<12:raise RuntimeError('Close your own model work first; start with 12 GiB available Windows RAM')
    for process in psutil.process_iter(['pid','cmdline'],ad_value=[]):
        if process.pid==os.getpid():continue
        command=process.info['cmdline']or[]
        if any(Path(value).name.lower()in('llama-server.exe','llama-cli.exe','main.py','moss_probe.py','acestep_ui.py')for value in command):raise RuntimeError('Another model process is present; close your own work before starting')
    gpu=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine | Select-Object Name,UtilizationPercentage | ConvertTo-Json -Compress'],capture_output=True,text=True,timeout=30)
    if gpu.returncode!=0 or not gpu.stdout.strip():raise RuntimeError('GPU activity could not be read')
    engines=json.loads(gpu.stdout);engines=engines if isinstance(engines,list)else[engines]
    if any(float(row['UtilizationPercentage'])>10 for row in engines):raise RuntimeError('GPU is active; wait for your other work to finish')
    root.mkdir(parents=True)
    for name in ['input','output','user','results','embeddings']:(root/name).mkdir()
    (root/'extra-model-paths.yaml').write_text('existing_ltx:\n  base_path: '+args.models.as_posix()+'\n  diffusion_models: diffusion_models\n  text_encoders: text_encoders\n  vae: vae\n  latent_upscale_models: latent_upscale_models\nown_text:\n  base_path: '+root.as_posix()+'\n  embeddings: embeddings\n','utf-8')
    (root/'input/PORTRAIT.png').write_bytes((KIT/'example/PORTRAIT.png').read_bytes())
    (root/'MODELS-VERIFIED.json').write_text(json.dumps(models,indent=2)+'\n','utf-8')
    for name in ['first-clip-positive.safetensors','first-clip-negative.safetensors']:
        file=KIT/'example/conditioning'/name;target=root/'embeddings'/name;target.write_bytes(file.read_bytes())
    (root/'CONDITIONING-REUSE.json').write_text(json.dumps(dict(new_text_encoding=False,reused_from='Executed first LTX portrait text run; see supplied conditioning and manifest'),indent=2)+'\n','utf-8')
    outputs=runner.stage(args,root,'01-clip',graph,['--reserve-vram','16']);source=next(Path(r['path'])for r in outputs if Path(r['path']).suffix.lower()=='.mp4');target=root/'results/CLIP.mp4';target.write_bytes(source.read_bytes())
    details=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(target)],text=True))
    video=next(r for r in details['streams']if r['codec_type']=='video')
    assert (video['width'],video['height'],video['nb_frames'],video['r_frame_rate'])==(1024,1024,str(args.frames),'24/1')
    assert not any(r['codec_type']=='audio'for r in details['streams'])
    subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(target),'-f','null','-'],check=True)
    result=dict(status='completed',clip=str(target),sha256=runner.sha(target),all_four_models_full_sha_verified=True,new_prompt_conditioning=False,reused_conditioning=True,frames=args.frames,owned_server_stopped=True,ffprobe=details)
    (root/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n','utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
