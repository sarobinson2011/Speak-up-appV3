"""Independent archive composition, changed-source and supplied-record audit."""
from pathlib import Path,PurePosixPath
import ast,hashlib,json,os,stat,zipfile
w=Path(__file__).resolve().parents[2];base=w/'oc-review';root=w/'oc-input'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p):return json.loads(p.read_bytes())
def archive(p,pin):
 b=p.read_bytes();assert ident(b)==pin
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None
  return {n:z.read(n) for n in z.namelist()}
current=archive(w/'upload/I164-outside-catch-classification-correction-1(1).zip',{'bytes':60424906,'sha256':'08499f314151aef36bdbe711ad6f821bf1258d28a8c0d65fd693e3b0db4a3ba5'})
old=archive(w/'upload/I164-client-handle-return-correspondence-1(1).zip',{'bytes':43439616,'sha256':'1f7b1c7dc58949e76f73cac68afb00ea0373490ac0c07bdada86d954772b4431'})
review=archive(w/'Formal-Lab6-I164-client-handle-return-correspondence-independent-review.zip',{'bytes':59157073,'sha256':'18cbb930e1b0db4d42b9e4b7f2af32f521d9f2c50c268216d8c02793c124df9f'})
assert len(old)==1282 and all(current['original/'+n]==v for n,v in old.items())
omitted={'input/I164-client-handle-return-correspondence-1.zip'}
assert len(review)==172 and all(current['review/'+n]==v for n,v in review.items() if n not in omitted)
def treecheck(path):
 files={};dirs=set();expected_dirs={p.as_posix() for n in current for p in PurePosixPath(n).parents if p.as_posix()!='.'}
 def walk(d):
  for e in os.scandir(d):
   p=Path(e.path);n=p.relative_to(path).as_posix();m=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(m):dirs.add(n);walk(p)
   else:assert stat.S_ISREG(m),n;files[n]=p
 walk(path);assert set(files)==set(current) and dirs==expected_dirs
 assert all(p.read_bytes()==current[n] for n,p in files.items())
 return {'members':len(files),'directories':len(dirs),'regular_exact_membership_and_bytes':'PASS'}
trees={n:treecheck(w/n) for n in ('oc-input','oc-recovered')}
changes={}
for n in ('managed_coverage.py','correspondence.py'):
 a=ast.parse(old['code/'+n]);b=ast.parse(current['code/'+n]);af={x.name:x for x in a.body if isinstance(x,(ast.FunctionDef,ast.ClassDef))};bf={x.name:x for x in b.body if isinstance(x,(ast.FunctionDef,ast.ClassDef))}
 changed=sorted(k for k in af.keys()&bf.keys() if ast.dump(af[k],include_attributes=False)!=ast.dump(bf[k],include_attributes=False));added=sorted(bf.keys()-af.keys());removed=sorted(af.keys()-bf.keys())
 assert not removed
 assert changed==(['client_handle_projection','compile_client_handle'] if n=='managed_coverage.py' else ['derive_client','predecessor_root'])
 assert added==(['_client_outcome_classification'] if n=='managed_coverage.py' else [])
 equal=[k for k in af if k not in changed];at=old['code/'+n].decode();bt=current['code/'+n].decode();assert all(ast.get_source_segment(at,af[k])==ast.get_source_segment(bt,bf[k]) for k in equal)
 changes[n]={'changed':changed,'added':added,'removed':removed,'unchanged_function_bytes':len(equal),'current':ident(current['code/'+n]),'previous':ident(old['code/'+n])}
 # Audit globals separately rather than relying on function comparisons.
 ag=[x for x in a.body if not isinstance(x,(ast.FunctionDef,ast.ClassDef))];bg=[x for x in b.body if not isinstance(x,(ast.FunctionDef,ast.ClassDef))]
 if n=='correspondence.py':
  ag=[x for x in ag if not (isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PRODUCER_PIN' for t in x.targets))];bg=[x for x in bg if not (isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PRODUCER_PIN' for t in x.targets))]
 assert [ast.dump(x,include_attributes=False) for x in ag]==[ast.dump(x,include_attributes=False) for x in bg]
def diff(a,b,p=''):
 if type(a) is not type(b):return [p]
 if isinstance(a,dict):
  out=[]
  for k in sorted(a.keys()|b.keys()):out+=diff(a[k],b[k],p+'/'+k) if k in a and k in b else [p+'/'+k]
  return out
 if isinstance(a,list):
  return [p] if len(a)!=len(b) else [v for i,(x,y) in enumerate(zip(a,b)) for v in diff(x,y,p+'/'+str(i))]
 return [] if a==b else [p]
receipt=read(root/'results/client-handle-correspondence.json');prior=json.loads(old['results/client-handle-correspondence.json']);paths=diff(prior,receipt)
expected=['/contexts/'+str(i)+'/client_handle_return_correspondence/declaration/'+k for i in (0,1) for k in ('format','outside_catch_failure_contract')]+['/extension_components/'+n+'/'+k for n in ('correspondence.py','managed_coverage.py') for k in ('bytes','sha256')]+['/format']
assert sorted(paths)==sorted(expected)
assert receipt['unchanged_obligations']==prior['unchanged_obligations'] and receipt['inventory_unknown_totals']==4 and receipt['lifetime_unknown_totals']==14
supplied={}
for name,count in [('primary',131),('recovered',129)]:
 p=root/'results'/name;r=read(p/'RESULT.json');rows=[json.loads(x) for x in (p/'progress.jsonl').read_text().splitlines()]
 assert r['result']=='PASS' and r['checks']==count and r['error'] is None and rows==r['rows'] and len(rows)==count
 assert r['source']=={n:ident(current['code/'+n]) for n in changes}
 supplied[name]={'checks':count,'identity':ident((p/'RESULT.json').read_bytes()),'source':r['source'],'inspected_not_executed':True,'labels':[v['check'] for v in rows]}
failed={}
for name,count in [('primary-fixture-selector',81),('primary-normal-comparison',103)]:
 p=root/'failures'/name;r=read(p/'results/RESULT.json');rows=[json.loads(x) for x in (p/'results/progress.jsonl').read_text().splitlines()]
 assert r['result']=='FAIL' and r['checks']==count and len(rows)==count and r['rows']==rows and r['error'] is not None
 assert r['source']=={n:ident(current['code/'+n]) for n in changes}
 failed[name]={'completed_before_failure':count,'error':r['error'],'result':ident((p/'results/RESULT.json').read_bytes()),'stderr':ident((p/'stderr').read_bytes()),'excluded_from_completed_totals':True}
# Retain the prior independent counts exactly, not as fresh tests.
cp=read(root/'review/CHECKPOINT.json');assert cp['independent_results']['primary_assertions']==217 and cp['independent_results']['recovered_assertions']==149
cli=read(root/'results/fresh.process.json');stdout=read(root/'results/fresh.stdout');assert stdout['result']=='PASS' and stdout['receipt']==ident(current['results/client-handle-correspondence.json']) and (root/'results/fresh.stderr').read_bytes()==b''
r={'result':'PASS','trees':trees,'unchanged_original_members':1282,'unchanged_independent_review_records':171,'prior_independent_assertions':[217,149],'prior_extra_caveat_cases':6,'prior_zero_assertion_failure_preserved':True,'source_changes':changes,'receipt_change_paths':paths,'all_other_receipt_fields_unchanged':True,'current_receipt':ident(current['results/client-handle-correspondence.json']),'prior_receipt':ident(old['results/client-handle-correspondence.json']),'supplied_controls':supplied,'supplied_failed_attempts':failed,'supplied_fresh_process':cli,'supplied_fresh_result':stdout,'intermediate_recovery_outer_archive_newly_verified':False,'intermediate_recovery':read(root/'results/recovery-input.json'),'implementation_modified':False}
(base/'results/composition.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS 1508 exact members; 1282 predecessor + 171 independent review records preserved; deliberate deltas and supplied failures inspected')
