from pathlib import Path
import hashlib,json,os,stat,zipfile,datetime,io
ROOT=Path('/workspace/scratch/3da0de3fef10/status-boundary')
OUTPUT=ROOT.parent/'I164-status-boundary-correction-1.zip'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(n,x):
 p=ROOT/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
def inventory(base):
 rows=[]
 def walk(p):
  for e in sorted(os.scandir(p),key=lambda e:e.name):
   q=Path(e.path);mode=e.stat(follow_symlinks=False).st_mode;name=str(q.relative_to(base))
   if stat.S_ISDIR(mode):rows.append({'path':name,'type':'directory'});walk(q)
   elif stat.S_ISREG(mode):rows.append({'path':name,'type':'regular',**ident(q.read_bytes())})
   elif stat.S_ISLNK(mode):rows.append({'path':name,'type':'symlink','target':os.readlink(q)})
   elif stat.S_ISFIFO(mode):rows.append({'path':name,'type':'FIFO'})
   else:rows.append({'path':name,'type':'unsupported','mode':mode})
 walk(base);return rows
excluded=[]
for p in sorted((ROOT/'results').rglob('*')):
 if p.name in ('recovered-root','mutations') and p.is_dir():
  if any(str(p).startswith(str(x)+'/') for x in excluded):continue
  excluded.append(p)
  relative=str(p.relative_to(ROOT));write('provenance/fixture-inventories/'+relative.replace('/','--')+'.json',{'root':relative,'disposition':'Redundant recovered/mutated source tree; exact inventory preserved, no live special-file entries in ZIP','entries':inventory(p)})
# Verify preservation against the original delivery bytes, not just self-created reports.
adopt=Path('/workspace/scratch/3da0de3fef10/I164-status-contract-adoption-1.zip').read_bytes()
assert ident(adopt)=={'bytes':54869,'sha256':'e06103888909cb2100d97dd75ab721fed237a5180444d05bec781c6e2f5d9fdd'}
a=zipfile.ZipFile(io.BytesIO(adopt))
for n in ('CONTRACT-draft-1.txt','DECISION.json'):assert (ROOT/'contract'/n).read_bytes()==a.read(n)
lraw=Path('/workspace/scratch/3da0de3fef10/status-integration-source/I164-launcher-5002-review(1).zip').read_bytes();l=zipfile.ZipFile(io.BytesIO(lraw))
assert ident(lraw)=={'bytes':101857,'sha256':'bdef8320320e74c9f79e187da4e6adfe93ce1d4723871f69935c9f8816299e55'}
for n in l.namelist():assert (ROOT/'retained/launcher'/n).read_bytes()==l.read(n)
pins=json.loads((ROOT/'provenance/dependency-pins.json').read_bytes())
for n,v in pins.items():assert ident((ROOT/n).read_bytes())==v
bp=json.loads((ROOT/'provenance/basis-pins.json').read_bytes())
for n,v in bp['members'].items():assert ident((ROOT/'basis'/n).read_bytes())==v
preserved={**pins,**{'basis/'+n:v for n,v in bp['members'].items()}}
# Counts deliberately keep repetitions/continuation independent, not summed as coverage.
first=json.loads((ROOT/'results/controls-1/PARTIAL.json').read_bytes())
fresh=json.loads((ROOT/'results/controls-1/fresh-evidence/RESULT.json').read_bytes())
resume=json.loads((ROOT/'results/controls-resumed/RESULT.json').read_bytes())
recovered=json.loads((ROOT/'results/controls-resumed/recovered-evidence/RESULT.json').read_bytes())
adj=json.loads((ROOT/'results/adjacent-controls/RESULT.json').read_bytes())
bind=json.loads((ROOT/'results/correspondence-controls/RESULT.json').read_bytes())
assert len(first['passed'])==80 and fresh['count']==recovered['count']==79 and resume['count']==10 and adj['count']==24 and bind['count']==22
assert all(x['result']=='PASS' for x in (fresh,resume,recovered,adj,bind))
write('results/FINAL.json',{'result':'PASS for bounded implementation/control scope; independent review pending','primary_assertions':79,'first_partial_checks':80,'first_partial_explanation':'79 primary plus fresh-process pass; then recovered-copy harness failure','fresh_process_primary_assertions':79,'recovered_process_primary_assertions':79,'continuation_checks':10,'adjacent_assertions':24,'correspondence_assertions':22,'counts_are_not_summed_as_independent_coverage':True,'real_backend_qualification':False,'real_managed_lifecycle_executions':0,'completed_review_reruns':0,'host_session_access':False,'contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'historical_launcher_frames':'UNAVAILABLE','actual_admission':False})
write('provenance/preservation.json',{'verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Retained file-byte preservation only; not host observation','adoption_archive':ident(adopt),'launcher_archive':ident(lraw),'preserved_members':preserved,'original_runtime_methods_changed':False,'old_session_metadata_changed':False,'new_application_logger':False,'policy_or_limits_changed':False})
write('CHECKPOINT.json',{'checkpoint':'I164-status-boundary-correction-1','status':'IMPLEMENTED; BOUNDED ENGINEERING CHECKS PASS; INDEPENDENT REVIEW PENDING','contract':pins['contract/CONTRACT-draft-1.txt'],'decision':pins['contract/DECISION.json'],'entry':ident((ROOT/'code/prospective_entry.py').read_bytes()),'correspondence':ident((ROOT/'provenance/status-correspondence.json').read_bytes()),'test_disposition':'results/FINAL.json','failures_preserved':['failures/checks-before-recovery-copy-fix.py','results/controls-1/PARTIAL.json','results/controls-1/recovered.stderr'],'boundaries':{'source_only':True,'obligations':11,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'readiness':'BLOCKED','final_binding':'BLOCKED','admission':False,'backup':'KERNEL-ONLY','streams':'UNCOMPUTED','cumulative_envelope_adopted':False,'historical_launcher_frames':'UNAVAILABLE','unix_socket_execution_qualification':'UNTESTED; prior limitation preserved'}})
# Include this exact packager for reproducibility; it is not application code.
(ROOT/'provenance/package.py').write_bytes(Path(__file__).read_bytes())
def selected():
 return [p for p in sorted(ROOT.rglob('*')) if p.is_file() and not p.is_symlink() and not any(p==x or x in p.parents for x in excluded) and '__pycache__' not in p.parts and p.name not in ('MANIFEST.json','CHANGED-IDENTITIES.json')]
# Excluding by filename here would hide historical MANIFESTs: add them explicitly.
def members():
 return [p for p in sorted(ROOT.rglob('*')) if p.is_file() and not p.is_symlink() and not any(p==x or x in p.parents for x in excluded) and '__pycache__' not in p.parts and str(p.relative_to(ROOT)) not in ('MANIFEST.json','CHANGED-IDENTITIES.json')]
new={str(p.relative_to(ROOT)):{'change':'ADDED in separate prospective package',**ident(p.read_bytes())} for p in members() if str(p.relative_to(ROOT)) not in preserved}
write('CHANGED-IDENTITIES.json',{'existing_original_files_modified':[],'new_files':new,'unchanged_reference_files':preserved,'scope':'Separate checkpoint; no repository or host installation overwrite','not_a_self_digest':'CHANGED-IDENTITIES.json and MANIFEST.json bound by outer manifest/archive'})
files=members()+[ROOT/'CHANGED-IDENTITIES.json']
manifest={str(p.relative_to(ROOT)):ident(p.read_bytes()) for p in sorted(files)}
write('MANIFEST.json',{'format':'I164-status-boundary-checkpoint-1','members':manifest})
with zipfile.ZipFile(OUTPUT,'x',compression=zipfile.ZIP_DEFLATED) as z:
 for p in sorted(files+[ROOT/'MANIFEST.json']):z.write(p,str(p.relative_to(ROOT)))
with zipfile.ZipFile(OUTPUT) as z:
 names=z.namelist();assert len(names)==len(set(names));assert set(names)==set(manifest)|{'MANIFEST.json'};assert z.testzip() is None
 for n in names:
  assert not n.startswith('/') and '..' not in Path(n).parts
  assert stat.S_ISREG(z.getinfo(n).external_attr>>16)
  if n in manifest:assert ident(z.read(n))==manifest[n]
 receipt={'file':str(OUTPUT),'entries':len(names),**ident(OUTPUT.read_bytes()),'crc':'PASS','safe_unique_regular_members':'PASS','exact_manifest':'PASS'}
(ROOT.parent/'status-boundary-identity.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
