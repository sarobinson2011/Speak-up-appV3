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
actual={p.name:tree(p) for p in [root,workspace/'cfg-recovered-2']}
copies={}
for prefix,p,size,sha,total,omitted in [('retained/binding',workspace/'upload/I164-binding-return-correspondence-1(1).zip',40870457,'269e5e439de97fe77fcacba484c544b276457db7643cc5863875ef227331dc4f',844,[]),('retained/binding-review',workspace/'Formal-Lab6-I164-binding-return-correspondence-independent-review.zip',57847754,'e6a180b5828f411746cbf4094282cd653d1826efc37ad690176f59f0be2cdf75',43,['input/I164-binding-return-correspondence-1.zip','failures/initial-recovered-membership/unexpected-0.bin'])]:
 b=p.read_bytes();assert identity(b)=={'bytes':size,'sha256':sha}
 with zipfile.ZipFile(p) as z:
  assert len(z.infolist())==total and z.testzip() is None
  names=[n for n in z.namelist() if n not in omitted];disk={p.relative_to(root/prefix).as_posix() for p in (root/prefix).rglob('*') if p.is_file()};assert disk==set(names)
  for n in names:assert (root/prefix/n).read_bytes()==z.read(n),(prefix,n)
 copies[prefix]={'archive':identity(b),'archive_entries':total,'byte_identical_members':len(names),'omitted_from_current_tree_but_exact_external_archive_available':omitted}
before=(root/'retained/binding/code/managed_coverage.py').read_bytes();after=(root/'code/managed_coverage.py').read_bytes()
def fn(b):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(b).body if isinstance(n,ast.FunctionDef)}
a,b=fn(before),fn(after);assert len(a)==35 and all(b[n]==v for n,v in a.items())
assert [ast.dump(n,include_attributes=False) for n in ast.parse(before).body if not isinstance(n,ast.FunctionDef)]==[ast.dump(n,include_attributes=False) for n in ast.parse(after).body if not isinstance(n,ast.FunctionDef)]
prior=json.loads((root/'retained/binding/results/binding-correspondence.json').read_bytes());now=json.loads((root/'results/config-correspondence.json').read_bytes())
assert len(prior['contexts'])==len(now['contexts'])==2
for oc,nc in zip(prior['contexts'],now['contexts']):assert set(nc)==set(oc)|{'config_return_correspondence'} and all(canonical(nc[k])==canonical(v) for k,v in oc.items())
for k,v in prior.items():
 if k not in ('contexts','format','extension_components'):assert canonical(now[k])==canonical(v),k
supplied={};overall=json.loads((root/'RESULTS.json').read_bytes())
for name,count in [('primary',127),('recovered',105)]:
 p=root/'results'/name/'RESULT.json';r=json.loads(p.read_bytes());assert r['result']=='PASS' and r['checks']==len(r['rows'])==count
 assert [json.loads(x) for x in (p.parent/'progress.jsonl').read_text().splitlines()]==r['rows']
 pin=overall['new_supplied_results'][name];assert identity(p.read_bytes())=={k:pin[k] for k in ('bytes','sha256')}
 supplied[name]={'checks':count,'inspected_not_executed':True,'result_identity':identity(p.read_bytes()),'labels':[x['check'] for x in r['rows']]}
process=json.loads((root/'results/fresh/RESULT.json').read_bytes());assert process['exit_code']==0 and process['validator_result']['receipt']==identity((root/'results/config-correspondence.json').read_bytes())
failed=root/'failures/control-syntax-preflight/controls.py'
try:ast.parse(failed.read_bytes());raise AssertionError('expected recorded syntax failure')
except SyntaxError as e:assert e.lineno==92 and e.msg=="unmatched ')'"
assert json.loads((failed.parent/'RESULT.json').read_bytes())['assertions']==0
interrupted=root/'retained/binding/failures/slow-profile-attempt';note=json.loads((interrupted/'NOTE.json').read_bytes());assert note['completed_assertions']==13 and note['status']=='INTERRUPTED';assert len((interrupted/'partial-results/progress.jsonl').read_text().splitlines())==13
r={'result':'PASS','actual_trees':actual,'preserved_copies':copies,'prior_producer_functions_AST_identical':35,'new_producer_functions':sorted(set(b)-set(a)),'prior_context_fields_and_other_top_fields_unchanged':True,'supplied':supplied,'supplied_process':process,'preflight_failure_reproduced_by_parse_only':True,'interrupted_attempt_preserved':note,'current_code':{n:identity((root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')},'current_receipt':identity((root/'results/config-correspondence.json').read_bytes()),'prior_receipt':identity((root/'retained/binding/results/binding-correspondence.json').read_bytes()),'recovery_input_provenance':json.loads((root/'results/recovery-input.json').read_bytes()),'reported_intermediate_recovery_archive_freshly_verified':False}
out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'result':'PASS','preserved_predecessor':844,'preserved_review_records':41,'supplied_counts':[127,105],'source_functions_preserved':35}))
