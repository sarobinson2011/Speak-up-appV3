from pathlib import Path
import json,ast,hashlib,difflib,re
BASE=Path('/workspace/scratch/ace5c9b2f18b');ROOT=Path('/workspace/review-evidence/FL6-control-20261030/primary');OUT=BASE/'cc-review/results'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(n):return (ROOT/n).read_bytes()
def obj(n):return json.loads(read(n))
changes=obj('provenance/changed-files.json');new=obj('provenance/new-files.json');m=obj('MANIFEST.json');cut=obj('provenance/recovery-cut-manifest.json');added=obj('provenance/final-added-files.json')
for n,pin in new.items():assert ident(read(n))==pin,n
diff=''
for n in ('code/managed_coverage.py','code/correspondence.py'):
 before=read('retained/bare/'+n);after=read(n);p=changes['intentional_implementation_changes'][n];assert ident(before)==p['before'] and ident(after)==p['after']
 diff+=''.join(difflib.unified_diff(before.decode().splitlines(True),after.decode().splitlines(True),fromfile='previous/'+n,tofile='new/'+n))
assert diff.encode()==read('provenance/implementation.diff')
before=ast.parse(read('retained/bare/code/managed_coverage.py'));after=ast.parse(read('code/managed_coverage.py'))
kind=(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)
old={n.name:ast.dump(n,include_attributes=False) for n in before.body if isinstance(n,kind)};cur={n.name:ast.dump(n,include_attributes=False) for n in after.body if isinstance(n,kind)}
assert len(old)==111 and all(cur[n]==v for n,v in old.items())
assert sorted(set(cur)-set(old))==changes['added_producer_functions']
assert [ast.dump(n) for n in before.body if not isinstance(n,kind)]==[ast.dump(n) for n in after.body if not isinstance(n,kind)]
sources={}
for n in ('prospective_entry.py','lab_bootstrap.py','live_connection.py'):
 b=read('source-evidence/'+n);assert b==read('retained/bare/source-evidence/'+n);sources[n]=ident(b)
prior=obj('retained/bare/results/primary/callback-bare-rethrow.json');receipt=obj('results/primary/control-exception.json')
assert all(all(receipt['contexts'][i][k]==v for k,v in row.items()) for i,row in enumerate(prior['contexts']))
for k,v in prior.items():
 if k not in ('format','extension_components','contexts'):assert receipt[k]==v,k
assert receipt['prior_callback_bare_components']==prior['extension_components']
supplied={}
for group,count in [('primary',276),('recovered',64),('public',7)]:
 stem='results/'+group+'/';result=obj(stem+'RESULT.json');progress=[json.loads(b) for b in read(stem+'progress.jsonl').splitlines()];lines=read(stem+'process.stdout').decode().splitlines();printed=[]
 for line in lines:
  z=re.fullmatch(r'(\d+) (.*) (PASS|REJECTED)',line)
  if z:printed.append((int(z[1]),z[2],z[3]))
 assert result['result']=='PASS' and result['checks']==count and result['rows']==progress and len(progress)==count
 assert printed==[(i,x['check'],x['result']) for i,x in enumerate(progress,1)]
 supplied[group]={'controls':count,'identity':ident(read(stem+'RESULT.json')),'progress_stdout_result_exact':True,'outcomes':{k:sum(x['result']==k for x in progress) for k in ('PASS','REJECTED')}}
failures=[]
for group in ('initial-membership','second-membership'):
 stem='failures/'+group+'/';record=obj(stem+'RECORD.json');result=obj(stem+'results/RESULT.json');assert record['checks']==result['checks']==0 and record['origin']=='UNESTABLISHED'
 fs=obj(stem+'failed-root-MANIFEST.json')
 if group=='initial-membership':
  assert ident(read(stem+'failed-root-MANIFEST.json'))==record['original_root_manifest'];parts=[]
  for i,v in enumerate(record['extra_entries'],1):
   p=stem+'partials/'+str(i);assert ident(read(p))=={k:v[k] for k in ('bytes','sha256')};assert v['path'] not in m and v['path'].removeprefix('retained/bare/') not in obj('retained/bare/MANIFEST.json')
   if v['path'] in fs:assert fs[v['path']]==ident(read(p))
   parts.append({'preserved_path':p,'identity':ident(read(p)),'original_extra_path':v['path'],'declared_in_failed_outer_manifest':v['path'] in fs,'undeclared_in_strict_predecessor':True})
 else:
  p=stem+'partial.bin';assert ident(read(p))=={k:record[k] for k in ('bytes','sha256')};assert record['path'] not in fs and record['path'] not in m and record['path'].removeprefix('retained/bare/') not in obj('retained/bare/MANIFEST.json');parts=[{'preserved_path':p,'identity':ident(read(p)),'original_extra_path':record['path'],'declared_in_failed_outer_manifest':False,'undeclared_in_strict_predecessor':True}]
 failures.append({'attempt':group,'controls':0,'origin':'UNESTABLISHED','result_identity':ident(read(stem+'results/RESULT.json')),'partials':parts,'outside_strict_predecessor':True})
for n,pin in cut.items():assert m[n]==pin,n
for n,pin in added.items():assert m[n]==pin,n
# Reuse the prior independently inspected qualification; compare exact retained
# records rather than re-executing any predecessor controls.
oldreview=obj('retained/review/CHECKPOINT.json');assert oldreview['independent_controls']==459
oldrecord=obj('retained/bare/RESULTS.json')['primary_log_reconciliation'];assert oldrecord['result_recorded_completed_controls']==308 and oldrecord['exact_progress_corroborated_controls']==307 and oldrecord['stdout_corroborated_prefix_controls']==303
assert oldrecord['progress_missing_result_ordinal']==304 and oldrecord['stdout_missing_result_ordinals']==[304,305,306,307,308]
out={'declared_diff_exact':True,'inherited_definitions':len(old),'added_definitions':sorted(set(cur)-set(old)),'nonfunction_AST_unchanged':True,'all_reviewed_context_relations_preserved':True,'all_prior_receipt_fields_preserved':True,'source_identities':sources,'new_receipt':ident(read('results/primary/control-exception.json')),'new_file_pins':len(new),'frozen_nonmanifest_members_preserved':len(cut),'intermediate_cut_outer_identity_freshly_verified':False,'supplied_results_inspected':supplied,'zero_control_failures':failures,'synchronizer_causation':'UNESTABLISHED','outside_synchronizer_scope_claim':'Explicitly qualified by preserved clarification; not independently established','prior_independent_controls_retained_not_rerun':459,'prior_Engineering_primary_qualification':[308,307,303],'prior_missing_progress_ordinal':304,'prior_missing_stdout_ordinals':[304,305,306,307,308],'prior_cause':'UNESTABLISHED','prior_separate_recovered_public':[78,5],'no_completed_suite_reruns':True}
(OUT/'composition-and-supplied.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps(out,sort_keys=True))
