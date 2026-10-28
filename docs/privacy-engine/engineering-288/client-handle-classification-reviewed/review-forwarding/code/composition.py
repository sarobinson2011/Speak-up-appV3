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
actual={p.name:tree(p) for p in [root,workspace/'ch-recovered-2']}
review=workspace/'Formal-Lab6-I164-handle-return-correspondence-independent-review.zip';rb=review.read_bytes();assert identity(rb)=={'bytes':42069714,'sha256':'d69cd5939e0fc051adee4f270dd0148d4aecf5cfef2ecae65b3ec33cedf4f31c'}
with zipfile.ZipFile(review) as z:
 assert len(z.infolist())==142 and z.testzip() is None;m=json.loads(z.read('MANIFEST.json'))['members'];assert set(m)==set(z.namelist())-{'MANIFEST.json'}
 for n,pin in m.items():assert identity(z.read(n))==pin
 omitted='input/I164-handle-return-correspondence-1.zip';names=set(z.namelist())-{omitted}
 assert {p.relative_to(root/'retained/handle-review').as_posix() for p in (root/'retained/handle-review').rglob('*') if p.is_file()}==names
 for n in names:assert (root/'retained/handle-review'/n).read_bytes()==z.read(n)
 raw=z.read(omitted);assert identity(raw)=={'bytes':42330497,'sha256':'6b486b1ca0c49da010face18132507020a07f3db84602d62a7c75af0305caa8e'}
 import io
 with zipfile.ZipFile(io.BytesIO(raw)) as pz:
  assert len(pz.infolist())==1088 and pz.testzip() is None
  assert {p.relative_to(root/'retained/handle').as_posix() for p in (root/'retained/handle').rglob('*') if p.is_file()}==set(pz.namelist())
  for n in pz.namelist():assert (root/'retained/handle'/n).read_bytes()==pz.read(n),n
def functions(b):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(b).body if isinstance(n,ast.FunctionDef)}
before=(root/'retained/handle/code/managed_coverage.py').read_bytes();after=(root/'code/managed_coverage.py').read_bytes();a,b=functions(before),functions(after)
assert len(a)==55 and all(b[n]==v for n,v in a.items())
assert [ast.dump(n,include_attributes=False) for n in ast.parse(before).body if not isinstance(n,ast.FunctionDef)]==[ast.dump(n,include_attributes=False) for n in ast.parse(after).body if not isinstance(n,ast.FunctionDef)]
prior=json.loads((root/'retained/handle/results/handle-correspondence.json').read_bytes());now=json.loads((root/'results/client-handle-correspondence.json').read_bytes())
assert len(prior['contexts'])==len(now['contexts'])==2
for oc,nc in zip(prior['contexts'],now['contexts']):assert set(nc)==set(oc)|{'client_handle_return_correspondence'} and all(canonical(nc[k])==canonical(v) for k,v in oc.items())
for k,v in prior.items():
 if k not in ('contexts','format','extension_components'):assert canonical(now[k])==canonical(v),k
assert now['prior_handle_components']==prior['extension_components']
supplied={}
for name,count,path in [('corrected-focused',17,'results/focused-correction'),('corrected-recovered',168,'results/recovered'),('pre-correction',170,'failures/pre-correction/primary')]:
 p=root/path/'RESULT.json';r=json.loads(p.read_bytes());assert r['result']=='PASS' and r['checks']==len(r['rows'])==count and r['error'] is None
 assert [json.loads(x) for x in (p.parent/'progress.jsonl').read_text().splitlines()]==r['rows']
 supplied[name]={'checks':count,'result_identity':identity(p.read_bytes()),'source':r['source'],'inspected_not_executed':True,'labels':[x['check'] for x in r['rows']]}
 old=name=='pre-correction';code=root/('failures/pre-correction/code' if old else 'code')
 for n,pin in r['source'].items():assert identity((code/n).read_bytes())==pin
w=json.loads((root/'failures/pre-correction/edge-witness.json').read_bytes());assert w['classification_inconsistent'] is True and w['output']['completion']=='unqualified-escape' and w['output']['outside_catch_failure'] is False
assert w['source']==identity((root/'failures/pre-correction/code/managed_coverage.py').read_bytes())
process=json.loads((root/'results/fresh/RESULT.json').read_bytes());assert process['exit_code']==0 and (root/'results/fresh/stderr').read_bytes()==b''
answer=json.loads((root/'results/fresh/stdout').read_bytes());assert answer['receipt']==identity((root/'results/client-handle-correspondence.json').read_bytes())
changes=json.loads((root/'CHANGED-IDENTITIES.json').read_bytes())
for n,v in changes['intentional_code_changes'].items():assert identity((root/'code'/n).read_bytes())==v['after'] and identity((root/'retained/handle/code'/n).read_bytes())==v['before']
r={'result':'PASS','trees':actual,'unchanged_predecessor_members':1088,'unchanged_prior_review_records':141,'exact_prior_review':identity(rb),'omitted_redundant_input':omitted,'unchanged_prior_functions':55,'other_top_level_AST_unchanged':True,'new_functions':sorted(set(b)-set(a)),'prior_context_fields_and_other_top_fields_unchanged':True,'supplied':supplied,'supplied_process':process,'preserved_witness':identity((root/'failures/pre-correction/edge-witness.json').read_bytes()),'pre_correction_campaign_not_interrupted':json.loads((root/'failures/pre-correction/PRESERVATION.json').read_bytes()),'intermediate_recovery_provenance':json.loads((root/'results/recovery-input.json').read_bytes()),'intermediate_outer_archive_newly_verified':False,'current_code':{n:identity((root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')},'current_receipt':identity((root/'results/client-handle-correspondence.json').read_bytes()),'prior_receipt':identity((root/'retained/handle/results/handle-correspondence.json').read_bytes())}
out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'result':'PASS','unchanged_predecessor_members':1088,'unchanged_review_records':141,'unchanged_functions':55,'supplied_corrected':[17,168],'supplied_pre_correction':170}))
