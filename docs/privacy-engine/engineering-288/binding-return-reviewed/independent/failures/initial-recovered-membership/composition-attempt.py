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
actual={p.name:tree(p) for p in [root,workspace/'br-recovered']}
copies={}
for prefix,p,size,sha,total in [('retained/hf01',workspace/'upload/I164-HF01-correction(1).zip',39924668,'0e2cce5d4519ccaaab35e34af0f89ef01b8a773569fba66008ee7affb1a9529c',732),('retained/review',workspace/'Formal-Lab6-I164-HF01-independent-review.zip',40300846,'5f0abc1727cb346f21140e97f4c75508962cef515f452941935d082e33c76a2e',73)]:
 b=p.read_bytes();assert identity(b)=={'bytes':size,'sha256':sha}
 with zipfile.ZipFile(p) as z:
  assert len(z.infolist())==total and z.testzip() is None
  names=[n for n in z.namelist() if not (prefix=='retained/review' and n.startswith('input/'))];disk={p.relative_to(root/prefix).as_posix() for p in (root/prefix).rglob('*') if p.is_file()};assert disk==set(names)
  for n in names:assert (root/prefix/n).read_bytes()==z.read(n),(prefix,n)
 copies[prefix]={'archive':identity(b),'archive_entries':total,'byte_identical_members':len(names)}
before=(root/'retained/hf01/code/managed_coverage.py').read_bytes();after=(root/'code/managed_coverage.py').read_bytes()
def fn(b):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(b).body if isinstance(n,ast.FunctionDef)}
a,b=fn(before),fn(after);assert len(a)==31 and all(b[n]==v for n,v in a.items())
assert {ast.dump(n,include_attributes=False) for n in ast.parse(before).body if not isinstance(n,ast.FunctionDef)}=={ast.dump(n,include_attributes=False) for n in ast.parse(after).body if not isinstance(n,ast.FunctionDef)}
prior=json.loads((root/'retained/hf01/results/hf01-correspondence.json').read_bytes());now=json.loads((root/'results/binding-correspondence.json').read_bytes())
for oc,nc in zip(prior['contexts'],now['contexts']):assert set(nc)==set(oc)|{'binding_return_correspondence'} and all(canonical(nc[k])==canonical(v) for k,v in oc.items())
for k,v in prior.items():
 if k not in ('contexts','format','extension_components'):assert canonical(now[k])==canonical(v),k
supplied={}
for name,count in [('primary',95),('recovered',53),('input-gates',4)]:
 p=root/'results'/name/'RESULT.json';r=json.loads(p.read_bytes());assert r['result']=='PASS' and r['checks']==len(r['rows'])==count
 progress=p.parent/'progress.jsonl'
 if progress.exists():assert [json.loads(x) for x in progress.read_text().splitlines()]==r['rows']
 supplied[name]={'checks':count,'inspected_not_executed':True,'result_identity':identity(p.read_bytes()),'check_labels':[x['check'] for x in r['rows']]}
note=json.loads((root/'failures/slow-profile-attempt/NOTE.json').read_bytes());assert note['completed_assertions']==13 and note['status']=='INTERRUPTED'
assert len((root/'failures/slow-profile-attempt/partial-results/progress.jsonl').read_text().splitlines())==13
overall=json.loads((root/'RESULTS.json').read_bytes());process=json.loads((root/'results/fresh-process.json').read_bytes());assert process['exit']==0
for suffix in ('stdout','stderr'):assert identity((root/f'results/fresh-process.{suffix}').read_bytes())==process[suffix]
r={'result':'PASS','actual_trees':actual,'preserved_copies':copies,'prior_producer_functions_AST_identical':31,'new_producer_functions':sorted(set(b)-set(a)),'prior_context_fields_and_other_top_fields_unchanged':True,'supplied':supplied,'supplied_process':'Saved result inspected only','interrupted_attempt':note,'current_code':{n:identity((root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')},'current_receipt':identity((root/'results/binding-correspondence.json').read_bytes()),'prior_receipt':identity((root/'retained/hf01/results/hf01-correspondence.json').read_bytes()),'recovery_input_provenance':json.loads((root/'results/recovery-input.json').read_bytes()),'reported_recovery_outer_archive_freshly_verified':False,'historical_manifest_scopes_preserved':True}
out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'result':'PASS','original_members':732,'review_noninput_members':72,'supplied_counts':[95,53,4],'source_functions_preserved':31}))
