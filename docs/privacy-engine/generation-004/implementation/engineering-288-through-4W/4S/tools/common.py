import hashlib,json,os
from pathlib import Path
OLD='08d6e7fb1e0cf37cc7effa76b50eaff0459abc158d9c6f0da52c6c58372b14f1'
STREAM='de09187b26c18dbcfbefb0d2fc03f98a74e7ecc7ba29b2c1c851fd4b0c1e31ee'
CONTRACT='2bbd9d52e1591bc12adc9cc0983c1686ade2cfc4cbcbeb95b6025259d5bf07fc'
R=Path(__file__).resolve().parents[1]
def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def info(p):return {'bytes':Path(p).stat().st_size,'sha256':sha(p)}
def load(p):return json.loads(Path(p).read_bytes())
def save(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);raw=canonical(x);tmp=p.with_suffix(p.suffix+'.part')
 with tmp.open('wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 os.replace(tmp,p)
def pointers(x,value,path=''):
 if x==value:yield path
 if isinstance(x,dict):
  for k,v in x.items():yield from pointers(v,value,path+'/'+k.replace('~','~0').replace('/','~1'))
 elif isinstance(x,list):
  for i,v in enumerate(x):yield from pointers(v,value,path+'/'+str(i))
def exact_binding(actual,expected):
 if actual!=expected:raise ValueError('stale or substituted candidate binding')
 if expected.get('profile_sha256') is None:raise ValueError('final profile unavailable; execution receipt cannot be current')
