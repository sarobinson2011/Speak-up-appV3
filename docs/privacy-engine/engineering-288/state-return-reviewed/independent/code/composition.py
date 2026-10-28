from pathlib import Path,PurePosixPath
import ast,hashlib,json,os,stat,sys,zipfile
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]);out.parent.mkdir(parents=True,exist_ok=True);workspace=root.parent
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def canonical(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def tree(p):
 m=json.loads((p/'MANIFEST.json').read_bytes());files={};dirs=set();expected=set(m)|{'MANIFEST.json'};parentdirs={str(q) for n in expected for q in PurePosixPath(n).parents if str(q)!='.'}
 def walk(d):
  for e in os.scandir(d):
   q=Path(e.path);n=q.relative_to(p).as_posix();s=e.stat(follow_symlinks=False)
   if stat.S_ISDIR(s.st_mode):dirs.add(n);walk(q)
   else:assert stat.S_ISREG(s.st_mode),(str(p),n,'nonregular');files[n]=q
 walk(p);assert set(files)==expected and dirs==parentdirs,{'root':str(p),'extra':sorted(set(files)-expected),'missing':sorted(expected-set(files)),'extra_dirs':sorted(dirs-parentdirs)}
 for n,pin in m.items():assert identity(files[n].read_bytes())==pin,n
 return {'members':len(files),'directories':len(dirs),'regular_membership_and_hashes':'PASS'}
actual={p.name:tree(p) for p in [root,workspace/'st-recovered']}
review=workspace/'st-dependencies/Formal-Lab6-I164-config-return-correspondence-independent-review.zip';rb=review.read_bytes();assert identity(rb)=={'bytes':63598176,'sha256':'97ccc050f291230f667a8d1fde28d9f655d75a28d72ec6604654d728cb5dcf94'}
with zipfile.ZipFile(review) as rz:
 assert len(rz.infolist())==43 and rz.testzip() is None
 m=json.loads(rz.read('MANIFEST.json'))['members'];assert set(m)==set(rz.namelist())-{'MANIFEST.json'}
 for n,pin in m.items():assert identity(rz.read(n))==pin
 omitted=['input/I164-config-return-correspondence-1.zip','failures/initial-recovered-membership/unexpected-0.bin'];names=set(rz.namelist())-set(omitted)
 assert {p.relative_to(root/'retained/config-review').as_posix() for p in (root/'retained/config-review').rglob('*') if p.is_file()}==names
 for n in names:assert (root/'retained/config-review'/n).read_bytes()==rz.read(n)
 cb=rz.read(omitted[0]);assert identity(cb)=={'bytes':41158663,'sha256':'e97feef76c75230c8ebc348844192d825a28ee2efd5b38ae27f0edd86f16c52f'}
 import io
 with zipfile.ZipFile(io.BytesIO(cb)) as cz:
  assert len(cz.infolist())==918 and cz.testzip() is None
  assert {p.relative_to(root/'retained/config').as_posix() for p in (root/'retained/config').rglob('*') if p.is_file()}==set(cz.namelist())
  for n in cz.namelist():assert (root/'retained/config'/n).read_bytes()==cz.read(n)
def functions(b):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(b).body if isinstance(n,ast.FunctionDef)}
before=(root/'retained/config/code/managed_coverage.py').read_bytes();after=(root/'code/managed_coverage.py').read_bytes();a,b=functions(before),functions(after)
assert len(a)==42 and all(b[n]==v for n,v in a.items())
assert [ast.dump(n,include_attributes=False) for n in ast.parse(before).body if not isinstance(n,ast.FunctionDef)]==[ast.dump(n,include_attributes=False) for n in ast.parse(after).body if not isinstance(n,ast.FunctionDef)]
prior=json.loads((root/'retained/config/results/config-correspondence.json').read_bytes());now=json.loads((root/'results/state-correspondence.json').read_bytes())
assert len(prior['contexts'])==len(now['contexts'])==2
for oc,nc in zip(prior['contexts'],now['contexts']):assert set(nc)==set(oc)|{'state_return_correspondence'} and all(canonical(nc[k])==canonical(v) for k,v in oc.items())
for k,v in prior.items():
 if k not in ('contexts','format','extension_components'):assert canonical(now[k])==canonical(v),k
supplied={}
for name,count in [('primary',83),('recovered-final',77)]:
 p=root/'results'/name/'RESULT.json';r=json.loads(p.read_bytes());assert r['result']=='PASS' and r['checks']==len(r['rows'])==count
 assert [json.loads(x) for x in (p.parent/'progress.jsonl').read_text().splitlines()]==r['rows']
 supplied[name]={'checks':count,'result_identity':identity(p.read_bytes()),'inspected_not_executed':True,'labels':[x['check'] for x in r['rows']]}
process=json.loads((root/'results/fresh/RESULT.json').read_bytes());assert process['exit_code']==0
assert (root/'results/fresh/stderr').read_bytes()==b''
assert json.loads((root/'results/fresh/stdout').read_bytes())['receipt']==identity((root/'results/state-correspondence.json').read_bytes())
failures=[]
for name,results in [('recovered-initial','recovered'),('recovered-second','recovered-completed')]:
 base=root/'failures'/name;rec=json.loads((base/'PRESERVATION.json').read_bytes());fr=json.loads((base/'RESULT.json').read_bytes());assert fr['checks']==0 and fr['rows']==[] and fr['result']=='FAIL' and (base/'RESULT.json').read_bytes()==(root/'results'/results/'RESULT.json').read_bytes()
 if name=='recovered-initial':assert identity((base/rec['preserved_file']).read_bytes())==rec['identity']
 else:
  for x in rec['unexpected']:assert identity((base/x['preserved']).read_bytes())=={k:x[k] for k in ('bytes','sha256')}
 failures.append(rec)
r={'result':'PASS','trees':actual,'config_predecessor_unchanged_members':918,'independent_review_unchanged_included_records':41,'exact_external_review':identity(rb),'external_archival_omissions_preserved':omitted,'prior_functions_AST_identical':42,'other_top_level_AST_identical':True,'new_functions':sorted(set(b)-set(a)),'prior_context_fields_and_other_top_fields_unchanged':True,'supplied':supplied,'supplied_process':process,'two_zero_assertion_membership_failures_preserved':failures,'intermediate_recovery_provenance':json.loads((root/'results/recovery-input.json').read_bytes()),'intermediate_outer_archive_newly_verified':False,'current_code':{n:identity((root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')},'current_receipt':identity((root/'results/state-correspondence.json').read_bytes()),'prior_receipt':identity((root/'retained/config/results/config-correspondence.json').read_bytes())}
out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'result':'PASS','unchanged_predecessor_members':918,'unchanged_review_records':41,'prior_functions':42,'supplied_counts':[83,77],'failed_supplied_assertions':[0,0]}))
