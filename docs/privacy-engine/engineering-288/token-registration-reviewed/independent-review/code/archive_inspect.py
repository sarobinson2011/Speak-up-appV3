from pathlib import Path,PurePosixPath
import hashlib,io,json,stat,zipfile
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def read(p):return json.loads(p.read_bytes())

def inspect(raw):
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  inf=z.infolist();names=[i.filename for i in inf];assert len(names)==len(set(names)) and z.testzip() is None
  for i in inf:
   n=i.filename;p=PurePosixPath(n);assert str(p)==n and not p.is_absolute() and all(x not in ('','.','..') for x in n.split('/')) and '\\' not in n and not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG)
  es={n:z.read(n) for n in names};rawm=json.loads(es['MANIFEST.json']);m=rawm.get('members',rawm);assert set(m)==set(es)-{'MANIFEST.json'}
  for n,p in m.items():assert ident(es[n])==p,n
  manifests=[]
  for n,b in es.items():
   if n.endswith('MANIFEST.json'):
    r=json.loads(b);r=r.get('members',r);prefix=n[:-len('MANIFEST.json')]
    if isinstance(r,dict) and all(isinstance(v,dict) and set(v)=={'bytes','sha256'} for v in r.values()):
     missing=[p for p in r if prefix+p not in es]
     for p,v in r.items():
      if prefix+p in es:assert ident(es[prefix+p])==v,(n,p)
     manifests.append({'manifest':n,'verified_present':len(r)-len(missing),'absent':missing})
  return es,{'identity':ident(raw),'entries':len(es),'CRC':'PASS','safe_exact_membership':'PASS','manifests':manifests}
