"""Install pinned ComfyUI source into a new folder; reuse your AMD Python environment."""
from pathlib import Path
import argparse,hashlib,json,subprocess,urllib.request,zipfile
KIT=Path(__file__).resolve().parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--python',type=Path,required=True);args=parser.parse_args()
    root=args.output.resolve();python=args.python.resolve()
    if root.exists():raise RuntimeError('Choose a new installation folder; existing files are preserved')
    if not python.is_file():raise RuntimeError('Supply the existing ROCm-enabled Python executable')
    metadata_code="import importlib.metadata as m,json;print(json.dumps({n:m.version(n) for n in ['torch','gguf','comfyui-frontend-package','transformers','safetensors']}))"
    packages=json.loads(subprocess.check_output([str(python),'-c',metadata_code],text=True))
    if not packages['torch'].startswith('2.9.1+rocm7.2.1'):raise RuntimeError('This example records the existing torch2.9.1+ROCm7.2.1 environment; see the AMD setup guide')
    root.mkdir(parents=True);(root/'downloads').mkdir();records=[]
    for source in json.loads((KIT/'SOURCES.json').read_text('utf-8'))['sources']:
        archive=root/'downloads'/(source['name']+'.zip');urllib.request.urlretrieve(source['url'],archive)
        if archive.stat().st_size!=source['bytes'] or sha(archive)!=source['sha256']:raise RuntimeError('Source archive checksum differs')
        destination=root/'ComfyUI' if source['name']=='ComfyUI' else root/'ComfyUI/custom_nodes/ComfyUI-GGUF'
        destination.mkdir(parents=True)
        with zipfile.ZipFile(archive)as bundle:
            if bundle.testzip()is not None:raise RuntimeError('Source archive CRC failed')
            prefix=bundle.namelist()[0].split('/')[0]+'/';files=[]
            for member in bundle.infolist():
                if member.is_dir():continue
                if not member.filename.startswith(prefix):raise RuntimeError('Unexpected archive root')
                relative=member.filename[len(prefix):];target=(destination/relative).resolve()
                if not target.is_relative_to(destination.resolve()):raise RuntimeError('Unexpected archive path')
                data=bundle.read(member);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data);files.append(dict(path=relative,sha256=sha(target)))
        records.append(dict(**source,installed_directory=str(destination),files=files,crc_passed=True));print('SOURCE INSTALLED',source['name'],len(files),flush=True)
    proof=dict(status='completed',python=str(python),existing_python_environment=True,fresh_driver_install=False,fresh_torch_install=False,packages=packages,sources=records)
    (root/'INSTALLATION.json').write_text(json.dumps(proof,indent=2)+'\n','utf-8');print('Open the guide and run run_clip.py with this new ComfyUI directory.')
if __name__=='__main__':main()
