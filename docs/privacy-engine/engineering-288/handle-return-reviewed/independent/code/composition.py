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
actual={p.name:tree(p) for p in [root,workspace/'hr-recovered']}
review=workspace/'Formal-Lab6-I164-state-return-correspondence-independent-review.zip';rb=review.read_bytes()
assert identity(rb)=={'bytes':41478030,'sha256':'63c72c1b7ad2f42f05b8f005454748967bf3fac5fcbc26fb81058567a717a311'}
with zipfile.ZipFile(review) as rz:
 assert len(rz.infolist())==34 and rz.testzip() is None
 m=json.loads(rz.read('MANIFEST.json'))['members'];assert set(m)==set(rz.namelist())-{'MANIFEST.json'}
 for n,pin in m.items():assert identity(rz.read(n))==pin,n
 omitted=['input/I164-state-return-correspondence-1.zip'];names=set(rz.namelist())-set(omitted)
 assert {p.relative_to(root/'retained/state-review').as_posix() for p in (root/'retained/state-review').rglob('*') if p.is_file()}==names
 for n in names:assert (root/'retained/state-review'/n).read_bytes()==rz.read(n),n
 raw=rz.read(omitted[0]);assert identity(raw)=={'bytes':41935972,'sha256':'44942004491d883af8c422f10dd38fd1e25cbc4f56e2d53e6345e264d0893fdc'}
 import io
 with zipfile.ZipFile(io.BytesIO(raw)) as pz:
  assert len(pz.infolist())==1016 and pz.testzip() is None
  assert {p.relative_to(root/'retained/state').as_posix() for p in (root/'retained/state').rglob('*') if p.is_file()}==set(pz.namelist())
  for n in pz.namelist():assert (root/'retained/state'/n).read_bytes()==pz.read(n),n
def functions(raw):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef)}
before=(root/'retained/state/code/managed_coverage.py').read_bytes();after=(root/'code/managed_coverage.py').read_bytes();a,b=functions(before),functions(after)
assert len(a)==48 and all(b[n]==v for n,v in a.items())
assert [ast.dump(n,include_attributes=False) for n in ast.parse(before).body if not isinstance(n,ast.FunctionDef)]==[ast.dump(n,include_attributes=False) for n in ast.parse(after).body if not isinstance(n,ast.FunctionDef)]
prior=json.loads((root/'retained/state/results/state-correspondence.json').read_bytes());now=json.loads((root/'results/handle-correspondence.json').read_bytes())
assert len(prior['contexts'])==len(now['contexts'])==2
for oc,nc in zip(prior['contexts'],now['contexts']):assert set(nc)==set(oc)|{'handle_return_correspondence'} and all(canonical(nc[k])==canonical(v) for k,v in oc.items())
for k,v in prior.items():
 if k not in ('contexts','format','extension_components'):assert canonical(now[k])==canonical(v),k
assert now['prior_state_components']==prior['extension_components']
assert now['prior_state_receipt']==identity((root/'retained/state/results/state-correspondence.json').read_bytes())
supplied={}
for name,count in [('primary',101),('relations',21),('recovered',101)]:
 p=root/'results'/name/'RESULT.json';r=json.loads(p.read_bytes());assert r['result']=='PASS' and r['checks']==len(r['rows'])==count and r['error'] is None
 if (p.parent/'progress.jsonl').exists():assert [json.loads(x) for x in (p.parent/'progress.jsonl').read_text().splitlines()]==r['rows']
 supplied[name]={'checks':count,'result_identity':identity(p.read_bytes()),'inspected_not_executed':True,'labels':[x['check'] for x in r['rows']]}
for n in ('constructed-cases.json','escaping-paths.json'):assert (root/'results/primary'/n).read_bytes()==(root/'results/recovered'/n).read_bytes()
process=json.loads((root/'results/fresh/RESULT.json').read_bytes());assert process['exit_code']==0
assert (root/'results/fresh/stderr').read_bytes()==b''
assert json.loads((root/'results/fresh/stdout').read_bytes())==process['output']
assert process['output']['receipt']==identity((root/'results/handle-correspondence.json').read_bytes())
failures=[]
for name,results in [('recovered-initial','recovered'),('recovered-second','recovered-completed')]:
 base=root/'retained/state/failures'/name;rec=json.loads((base/'PRESERVATION.json').read_bytes());fr=json.loads((base/'RESULT.json').read_bytes());assert fr['checks']==0 and fr['rows']==[] and fr['result']=='FAIL' and (base/'RESULT.json').read_bytes()==(root/'retained/state/results'/results/'RESULT.json').read_bytes()
 if name=='recovered-initial':assert identity((base/rec['preserved_file']).read_bytes())==rec['identity']
 else:
  for x in rec['unexpected']:assert identity((base/x['preserved']).read_bytes())=={k:x[k] for k in ('bytes','sha256')}
 failures.append(rec)
changes=json.loads((root/'CHANGED-IDENTITIES.json').read_bytes())
for n,v in changes['intentional_changed_files'].items():assert identity((root/n).read_bytes())==v['after'] and identity((root/'retained/state'/n).read_bytes())==v['before']
assert sorted(set(b)-set(a))==changes['new_producer_functions']
r={'result':'PASS','trees':actual,'unchanged_predecessor_members':1016,'independent_review_unchanged_included_records':33,'exact_predecessor_review':identity(rb),'compact_review_omitted_redundant_archive':omitted,'prior_functions_AST_identical':48,'other_top_level_AST_identical':True,'new_functions':sorted(set(b)-set(a)),'prior_context_fields_and_other_top_fields_unchanged':True,'supplied':supplied,'supplied_process':process,'two_prior_zero_assertion_membership_failures_preserved':failures,'intermediate_recovery_provenance':json.loads((root/'results/recovery-input.json').read_bytes()),'intermediate_outer_archive_newly_verified':False,'current_code':{n:identity((root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')},'current_receipt':identity((root/'results/handle-correspondence.json').read_bytes()),'prior_receipt':identity((root/'retained/state/results/state-correspondence.json').read_bytes())}
out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'result':'PASS','unchanged_predecessor_members':1016,'unchanged_review_records':33,'prior_functions':48,'supplied_counts':[101,21,101],'prior_failed_supplied_assertions':[0,0]}))
