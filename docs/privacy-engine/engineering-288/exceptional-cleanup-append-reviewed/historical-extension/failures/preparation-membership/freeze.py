"""Prepare static submitted receipt and a recovered input root; no validation is claimed here."""
from pathlib import Path
import json,hashlib,types,zipfile,stat,datetime
T=Path(__file__).resolve().parents[1];r=T/'input'
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(n,v):p=r/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(enc(v))
def declared_files(root):
 # Source-controlled work files and exact retained manifests; no inferred copies.
 names=[]
 for q in root.rglob('*'):
  if q.is_file():names.append(q.relative_to(root).as_posix())
 return sorted(names)
p=r/'retained/details';pm=json.loads((p/'MANIFEST.json').read_bytes())
actual={n for n in declared_files(p)};assert actual==set(pm)|{'MANIFEST.json'},(actual-(set(pm)|{'MANIFEST.json'}))
for n,pin in pm.items():assert ident((p/n).read_bytes())==pin,n
save('provenance/intake.json',{'prior_save_reused':'c43954ff5ee384c6fb6e7a85d83eb36bfea342d1','prior_archive':{'bytes':139583348,'sha256':'e4accc10b74390d08266853a0da649c8e4c235ce839bbf2b9bb9548926f7c97c','entries':3771},'independent_closure':{'bytes':136204484,'sha256':'52accc6e32c4af44be4392d1d2db811bd2cb8ef208c0140a64bbea0a82ccdd24','entries':134},'closure_scope':'LD-01 CLOSED within retained CPython3.12.14 cooperative monitoring contract; prior source support unchanged','retained_predecessor_files_verified':len(pm)+1,'prior_campaigns_replayed':False,'runtime_sources_unchanged':True})
mod=types.ModuleType('cleanup_preparation');mod.__file__=str(r/'code/correspondence.py');exec(compile((r/'code/correspondence.py').read_bytes(),mod.__file__,'exec'),mod.__dict__)
data=mod.inputs(r);cat=mod.catalogue(data)
# Reuse an exact previously recorded public predecessor result only as submitted
# fixture metadata. Actual validators reauthenticate the predecessor independently.
public=json.loads((p/'ld01/results/primary/actual-public-result.json').read_bytes())
fixture={'fresh':data,'prior':data['prior'],'catalogue':cat,'public_predecessor':public}
prepared=mod.enc(mod._assemble(data,mod._rows(fixture),fixture));q=r/'receipts/prepared-cleanup-append.json';q.parent.mkdir();q.write_bytes(prepared)
save('provenance/receipt-preparation.json',{'kind':'STATIC-SUBMITTED-INPUT-PREPARATION-NOT-VALIDATION','prepared':ident(prepared),'prior_saved_result':ident((p/'ld01/results/primary/actual-public-result.json').read_bytes()),'new_execution_claims':0,'authenticating_predecessor_calls_in_preparation':0,'acceptance_requires':'Actual current mandatory public validation through unchanged predecessor and same authenticated basis; no fixture metadata bypass'})
for name in ['producer-addition.py','build.py','freeze.py','supervise.py']:
 q=r/'tools'/name;q.parent.mkdir(exist_ok=True);q.write_bytes((T/'tools'/name).read_bytes())
names=declared_files(r);assert 'MANIFEST.json' not in names
m={n:ident((r/n).read_bytes()) for n in names};(r/'MANIFEST.json').write_bytes(enc(m))
zpath=T/'recovery-input.zip'
with zipfile.ZipFile(zpath,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n in ['MANIFEST.json',*names]:
  zi=zipfile.ZipInfo(n);zi.create_system=3;zi.external_attr=(stat.S_IFREG|0o644)<<16;zi.compress_type=zipfile.ZIP_DEFLATED;z.writestr(zi,(r/n).read_bytes())
recovered=T/'recovered';recovered.mkdir()
with zipfile.ZipFile(zpath) as z:z.extractall(recovered)
(T/'RECOVERY-INPUT-IDENTITY.json').write_bytes(enc({'archive':ident(zpath.read_bytes()),'entries':len(names)+1,'manifest':ident((r/'MANIFEST.json').read_bytes()),'prepared_receipt':ident(prepared),'verified_before_execution':True}))
print('FROZEN',len(names)+1,'files; prepared receipt',ident(prepared),flush=True)
