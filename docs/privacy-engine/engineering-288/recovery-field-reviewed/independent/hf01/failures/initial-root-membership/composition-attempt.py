"""Independent byte continuity, source-change and supplied-result inspection."""
from pathlib import Path,PurePosixPath
import ast,difflib,hashlib,json,os,stat,sys,zipfile
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.parent.mkdir(parents=True,exist_ok=True)
workspace=root.parent
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def verify_tree(p):
 manifest=json.loads((p/'MANIFEST.json').read_bytes());expected=set(manifest)|{'MANIFEST.json'}
 dirs={str(q) for n in expected for q in PurePosixPath(n).parents if str(q)!='.'};files={};seen_dirs=set()
 def walk(d):
  for e in os.scandir(d):
   q=Path(e.path);n=q.relative_to(p).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):seen_dirs.add(n);walk(q)
   else:assert stat.S_ISREG(mode),(n,'nonregular');files[n]=q
 walk(p);assert set(files)==expected and seen_dirs==dirs
 for n,pin in manifest.items():assert ident(files[n].read_bytes())==pin,n
 return {'files':len(files),'parent_directories':len(dirs),'exact_regular_membership_and_hashes':'PASS'}
trees={str(p.name):verify_tree(p) for p in (root,workspace/'hfc-recovered')}
archives=[('original',workspace/'upload/I164-recovery-field-correspondence-1(1).zip',39038102,'c92840a853097a9fe5fd1cd80134649fdd25a7463422cce81361a46bec70f8cf',617),
 ('retained/review',workspace/'Formal-Lab6-I164-recovery-field-correspondence-independent-review.zip',39400482,'dc9e1fd7a71fb079853ad1c7ff380213cd2b80201a848670778bc5e2d027b291',64)]
copies={}
for prefix,path,size,sha,count in archives:
 b=path.read_bytes();assert ident(b)=={'bytes':size,'sha256':sha}
 with zipfile.ZipFile(path) as z:
  assert len(z.infolist())==count and z.testzip() is None
  names=[n for n in z.namelist() if not(prefix=='retained/review' and n.startswith('input/'))]
  actual={p.relative_to(root/prefix).as_posix() for p in (root/prefix).rglob('*') if p.is_file()}
  assert actual==set(names)
  for n in names:assert (root/prefix/n).read_bytes()==z.read(n),(prefix,n)
 copies[prefix]={'verified_archive':ident(b),'archive_entries':count,'exact_preserved_members':len(names)}
old=(root/'original/code/correspondence.py').read_bytes();new=(root/'code/correspondence.py').read_bytes()
assert (root/'code/managed_coverage.py').read_bytes()==(root/'original/code/managed_coverage.py').read_bytes()
def funcs(b):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(b).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
a=funcs(old);b=funcs(new);changed=[]
for n,v in a.items():
 if n=='recovery_inputs':
  node=next(n for n in ast.parse(new).body if isinstance(n,ast.FunctionDef) and n.name=='_reviewed_recovery_inputs');node.name='recovery_inputs';assert ast.dump(node,include_attributes=False)==v
 elif n in ('connected_recovery','derive_recovery'):changed.append(n)
 else:assert b[n]==v,n
oldreceipt=json.loads((root/'original/results/recovery-field-correspondence.json').read_bytes());receipt=json.loads((root/'results/hf01-correspondence.json').read_bytes())
assert [c['context'] for c in receipt['contexts']]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']
for oldc,newc in zip(oldreceipt['contexts'],receipt['contexts']):
 assert set(newc)==set(oldc)|{'hf01_evidence_binding'}
 assert all(enc(newc[k])==enc(v) for k,v in oldc.items())
for k,v in oldreceipt.items():
 if k not in ('format','extension_components','contexts'):assert enc(receipt[k])==enc(v),k
supplied={}
for label,name,count in [('primary','results/primary/RESULT.json',75),('recovered','results/recovered-clean/RESULT.json',23),('input_gates','results/input-gates.json',5)]:
 r=json.loads((root/name).read_bytes());assert r['passed']==count and len(r['checks'])==count and r['result']=='PASS'
 supplied[label]={'record':name,'inspected_not_executed':True,'count':count,'identity':ident((root/name).read_bytes())}
failure=json.loads((root/'failures/recovered-root-membership/RESULT.json').read_bytes());assert failure['passed']==0 and failure['result']=='FAIL'
overall=json.loads((root/'RESULTS.json').read_bytes());assert overall['new_controls']['fresh_process']['exit']==0
for n in ['results/fresh-process.stdout','results/fresh-process.stderr']:
 if (root/n).exists():assert ident((root/n).read_bytes())==overall['new_controls']['fresh_process'][n.rsplit('.',1)[1]]
core=json.loads((root/'provenance/core-preservation.json').read_bytes()) if (root/'provenance/core-preservation.json').exists() else None
result={'result':'PASS','exact_recovered_trees':trees,'preserved_copies':copies,
 'only_changed_implementation':'code/correspondence.py','before':ident(old),'after':ident(new),'unchanged_managed_coverage':ident((root/'code/managed_coverage.py').read_bytes()),
 'old_functions_preserved_except':changed+['recovery_inputs; old body retained as _reviewed_recovery_inputs'],
 'new_functions':sorted(set(b)-set(a)), 'all_prior_context_fields_and_noncomponent_top_fields_unchanged':True,
 'old_receipt':ident((root/'original/results/recovery-field-correspondence.json').read_bytes()),'new_receipt':ident((root/'results/hf01-correspondence.json').read_bytes()),
 'supplied':supplied,'supplied_fresh_process':'Inspected saved PASS only; not executed','failed_fixture':failure,
 'recovered_input_scope':overall['recovered_input'],'recovered_input_outer_ZIP_present':False,
 'historical_manifest_scopes':'Preserved. Partial review copy omits only its redundant input ZIP; original/ supplies all 617 decoded executable input members.',
 'no_completed_review_rerun':True}
out.write_text(json.dumps(result,indent=2)+'\n')
(out.parent/'correspondence.diff').write_text(''.join(difflib.unified_diff(old.decode().splitlines(True),new.decode().splitlines(True),fromfile='original',tofile='HF01-corrected')))
print(json.dumps({'result':'PASS','preserved_original':617,'preserved_review':63,'current_receipt':result['new_receipt'],'supplied_inspected':[75,23,5]}))
