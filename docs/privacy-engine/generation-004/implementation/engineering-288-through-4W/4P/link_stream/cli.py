"""Bounded supplied-file CLI. It never generates missing links."""
import math
import argparse,hashlib,json,pathlib,subprocess,sys,zipfile,shutil
ROOT=pathlib.Path(__file__).resolve().parents[1]
CP4A='5a0880ba85ae97e1624a48886afdcdd85a77b524eb06e939955c2fbcb1dc900f'
DESC='c79ea7fa8e27de3fb051c50f4f50d52cecb51c3d3e0025c9569b174d27882f5f'
def sha(path):
 h=hashlib.sha256()
 with pathlib.Path(path).open('rb') as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
def prepare():
 p=ROOT/'inputs/links.txt'
 if p.exists():
  if sha(p)!=DESC:raise ValueError('changed full retained descriptor')
  return p
 zpath=ROOT/'retained/Engineering-288-checkpoint-4A.zip'
 if sha(zpath)!=CP4A:raise ValueError('changed retained CP4A package')
 p.parent.mkdir(exist_ok=True);tmp=p.with_suffix('.part')
 with zipfile.ZipFile(zpath) as z,z.open('Engineering-288-checkpoint-4A/inputs/links.txt') as src,tmp.open('wb') as out:shutil.copyfileobj(src,out,1048576)
 if sha(tmp)!=DESC:raise ValueError('descriptor identity')
 tmp.replace(p);return p

def build():
 subprocess.run(['g++','-O3','-std=c++17','-Wno-deprecated-declarations',str(ROOT/'link_stream/native.cpp'),'-lcrypto','-o',str(ROOT/'link_stream/native')],check=True,timeout=60)
def native(path,descriptor=None,descriptor_sha256=None,expected_sha256=None,chunk_bytes=65536,max_bytes=67108864,seconds=50):
 if not seconds>0 or not math.isfinite(seconds):raise ValueError('finite positive explicit deadline required')
 if descriptor is None:descriptor=prepare();descriptor_sha256=DESC
 if not descriptor_sha256:raise ValueError('independent descriptor digest is required')
 command=[str(ROOT/'link_stream/native'),str(descriptor),descriptor_sha256,str(path),expected_sha256 or 'NONE',str(chunk_bytes),str(max_bytes),str(max(.001,seconds-.2))]
 try:
  cp=subprocess.run(command,capture_output=True,text=True,timeout=seconds)
 except subprocess.TimeoutExpired:
  return {'result':'INTERRUPTED','complete':False,'complete_stream_sha256':None,'consumed_sha256':None,'bytes_consumed':None,'failure':{'code':'RESOURCE-LIMIT','detail':'external deadline; native receipt unavailable, consumed prefix unknown'},'profile_admitted':False,'actual_qualification_established':False}
 if cp.stderr:print(cp.stderr,file=sys.stderr,end='')
 r=json.loads(cp.stdout);r['exit_code']=cp.returncode;return r

def main():
 p=argparse.ArgumentParser(description='Validate supplied static links; no generation and no admission')
 p.add_argument('operation',choices=('build','prepare','validate'));p.add_argument('input',nargs='?',type=pathlib.Path);p.add_argument('--descriptor',type=pathlib.Path);p.add_argument('--descriptor-sha256');p.add_argument('--expected-sha256');p.add_argument('--chunk-bytes',type=int,default=65536);p.add_argument('--max-bytes',type=int,default=67108864);p.add_argument('--seconds',type=float,default=50);p.add_argument('--output',type=pathlib.Path);a=p.parse_args()
 if a.operation=='build':build();return 0
 if a.operation=='prepare':print(prepare());return 0
 if a.input is None:p.error('input file required')
 r=native(a.input,a.descriptor,a.descriptor_sha256,a.expected_sha256,a.chunk_bytes,a.max_bytes,a.seconds);raw=json.dumps(r,indent=2)+'\n'
 if a.output:
  with a.output.open('x') as f:f.write(raw)
 print(raw,end='');return 0 if r['complete'] else 2
if __name__=='__main__':raise SystemExit(main())
