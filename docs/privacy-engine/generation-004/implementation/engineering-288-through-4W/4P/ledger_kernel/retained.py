"""Exact retained ZIP/member acquisition only. Never invokes the expander."""
import hashlib,json,os,shutil,zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PINS={'4C':'ca4c968c22e738b5e98a4a90c0214bbcbd6d7b44fd9c15acafb8c71cb1dda9f7',
      '4B':'97fa92822ab7c0d42f0d120c6504097f6253fecbed6fbd4c272a05336dc219fd',
      '4A':'5a0880ba85ae97e1624a48886afdcdd85a77b524eb06e939955c2fbcb1dc900f',
      '3':'0dd4e3bd69735399ed47ac3953d12ec0d11aae5beec01ca66b29045bc39b98a3',
      '2':'3740c21246000bad0aeb2d34d081548914e073885b304df7f3eddad2b78501cd'}

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        while b:=f.read(1048576):h.update(b)
    return h.hexdigest()

def atomic(path, raw):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.part')
    with tmp.open('wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
    fd=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)

def archive(stage):
    order=list(PINS);p=ROOT/'retained/Engineering-288-checkpoint-4C.zip'
    for i,s in enumerate(order):
        if sha(p)!=PINS[s]:raise ValueError('retained archive changed: '+s)
        if s==stage:return p
        nxt=order[i+1];target=ROOT/'work/retained'/('Engineering-288-checkpoint-'+nxt+'.zip')
        if not target.exists():
            target.parent.mkdir(parents=True,exist_ok=True);tmp=target.with_suffix('.part')
            with zipfile.ZipFile(p) as z,z.open('Engineering-288-checkpoint-'+s+'/retained/'+target.name) as src,tmp.open('wb') as out:
                shutil.copyfileobj(src,out,1048576);out.flush();os.fsync(out.fileno())
            if sha(tmp)!=PINS[nxt]:raise ValueError('nested archive identity')
            tmp.replace(target)
        p=target
    raise ValueError(stage)

class CP2:
    def __init__(self):
        self.zip=zipfile.ZipFile(archive('2'));self.prefix='Engineering-288-checkpoint-2/'
        self.manifest=json.loads(self.zip.read(self.prefix+'PACKAGE-MANIFEST.json'))
        self.entries={e['path']:e for e in self.manifest['files']}
    def get(self,path):
        e=self.entries[path];target=ROOT/'work/cp2'/path
        if target.exists():
            if target.stat().st_size!=e['bytes'] or sha(target)!=e['sha256']:raise ValueError('changed cached CP2 input '+path)
            return target
        target.parent.mkdir(parents=True,exist_ok=True);tmp=target.with_suffix('.part')
        with self.zip.open(self.prefix+path) as src,tmp.open('wb') as out:
            shutil.copyfileobj(src,out,1048576);out.flush();os.fsync(out.fileno())
        if tmp.stat().st_size!=e['bytes'] or sha(tmp)!=e['sha256']:raise ValueError('CP2 exact member identity '+path)
        tmp.replace(target);return target
    def data(self,path):return json.loads(self.get(path).read_bytes())
