"""Download the four pinned LTX-2.5 model files; preserve unverified existing files."""
from pathlib import Path
import argparse,hashlib,json,urllib.request
KIT=Path(__file__).resolve().parent
def sha(path):
    digest=hashlib.sha256()
    with path.open('rb')as stream:
        while block:=stream.read(16*1024*1024):digest.update(block)
    return digest.hexdigest()
def main(folder):
    root=Path(folder).resolve();root.mkdir(parents=True,exist_ok=True)
    for row in json.loads((KIT/'MODELS.json').read_text('utf-8'))['models']:
        target=(root/row['path']).resolve()
        if not target.is_relative_to(root):raise RuntimeError('Unexpected model path')
        target.parent.mkdir(parents=True,exist_ok=True);partial=target.with_suffix(target.suffix+'.part')
        if target.exists():
            if target.stat().st_size==row['bytes']and sha(target)==row['sha256']:print('Already verified:',row['path'],flush=True);continue
            raise RuntimeError('Existing unverified file preserved: '+str(target))
        offset=partial.stat().st_size if partial.exists()else 0
        if offset>row['bytes']:raise RuntimeError('Oversized partial download preserved')
        if offset<row['bytes']:
            request=urllib.request.Request(row['url'],headers={'Range':f'bytes={offset}-'}if offset else{})
            with urllib.request.urlopen(request,timeout=120)as response:
                if offset and(response.status!=206 or not response.headers.get('Content-Range','').startswith(f'bytes {offset}-')):raise RuntimeError('Unexpected resume response; partial file preserved')
                with partial.open('ab'if offset else'wb')as output:
                    while block:=response.read(4*1024*1024):output.write(block)
        if partial.stat().st_size!=row['bytes']or sha(partial)!=row['sha256']:raise RuntimeError('Model checksum differs; partial file preserved')
        partial.rename(target);print('Verified:',row['path'],flush=True)
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True);main(parser.parse_args().output)
