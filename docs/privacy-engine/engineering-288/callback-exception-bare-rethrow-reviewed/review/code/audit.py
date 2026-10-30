import ast,difflib,hashlib,io,json,re,zipfile
from pathlib import Path
ROOT=Path('/workspace/review-evidence/FL6-bare-20261030/primary')
OUT=Path('/workspace/scratch/ace5c9b2f18b/br-review/results')
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(n):return (ROOT/n).read_bytes()
def obj(n):return json.loads(read(n))
oldzip=Path('/workspace/scratch/ace5c9b2f18b/br-prior/Formal-Lab6-I164-callback-exception-stored-failure-independent-review.zip')
assert ident(oldzip.read_bytes())=={'bytes':82756868,'sha256':'e14858c4bdb77f8aa158d9091bac40f76a6d4548f91d72412b1dbe8fd1be8ec3'}
with zipfile.ZipFile(oldzip) as z:
 checked_review=0
 for n in z.namelist():
  if n.startswith('input/'):continue
  assert read('retained/review/'+n)==z.read(n),n;checked_review+=1
 original=z.read('input/I164-callback-exception-stored-failure-correspondence-1.zip')
 assert ident(original)=={'bytes':84555031,'sha256':'0a39361622d3c05c7f46b258bfd7570d632ab57ee87317103cacce1f52822255'}
 with zipfile.ZipFile(io.BytesIO(original)) as p:
  for n in p.namelist():assert read('retained/callback/'+n)==p.read(n),n
  checked_predecessor=len(p.namelist())
prev=ast.parse(read('retained/callback/code/managed_coverage.py'));now=ast.parse(read('code/managed_coverage.py'))
defs=lambda t:{n.name:ast.dump(n,include_attributes=False) for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
olddefs=defs(prev);newdefs=defs(now);assert all(newdefs[n]==v for n,v in olddefs.items())
others=lambda t:[ast.dump(n,include_attributes=False) for n in t.body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))]
assert others(prev)==others(now)
changes=obj('provenance/changed-files.json');assert set(newdefs)-set(olddefs)==set(changes['added_producer_functions']);assert len(olddefs)==106
diff=''
for n in ('code/managed_coverage.py','code/correspondence.py'):
 a=read('retained/callback/'+n);b=read(n);assert changes['intentional_implementation_changes'][n]=={'current':ident(b),'previous':ident(a)}
 diff+=''.join(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile='reviewed-callback/'+n,tofile='callback-bare/'+n))
# The declaration may order the two diffs differently; compare each complete block.
declared=read('provenance/intentional.diff').decode()
def blocks(s):return sorted('--- '+x for x in s.split('--- ')[1:])
assert blocks(diff)==blocks(declared)
sources={}
for n in ('prospective_entry.py','lab_bootstrap.py','live_connection.py'):
 b=read('source-evidence/'+n);assert b==read('retained/callback/source-evidence/'+n);sources[n]=ident(b)
cut=obj('provenance/recovery-cut-manifest.json');manifest=obj('MANIFEST.json')
assert len(cut)==2907 and all(manifest[n]==v for n,v in cut.items())
records={}
for mode in ('primary','recovered','public'):
 result=obj('results/'+mode+'/RESULT.json');rows=result['rows'];progress=[json.loads(x) for x in read('results/'+mode+'/progress.jsonl').splitlines() if x];stdout=read('results/'+mode+'/stdout.log').decode();lines=[]
 for line in stdout.splitlines():
  m=re.fullmatch(r'(\d+) (.*) (PASS|REJECTED)',line)
  if m:lines.append((int(m[1]),m[2],m[3]))
 pos=0;missing=[]
 for i,x in enumerate(rows,1):
  if pos<len(progress) and progress[pos]==x:pos+=1
  else:missing.append({'ordinal':i,'record':x})
 assert pos==len(progress)
 for i,label,status in lines:assert rows[i-1]['check']==label and rows[i-1]['result']==status
 records[mode]={'result_count':result['checks'],'actual_result_rows':len(rows),'progress_rows':len(progress),'stdout_rows':len(lines),'missing_progress':missing,'missing_stdout_ordinals':sorted(set(range(1,len(rows)+1))-{i for i,_,_ in lines}),'row_correspondence':'PASS','result_identity':ident(read('results/'+mode+'/RESULT.json'))}
assert records['primary']['actual_result_rows']==308 and records['primary']['progress_rows']==307 and records['primary']['stdout_rows']==303
assert records['primary']['missing_progress']==[{'ordinal':304,'record':{'check':'adjacent normal-callback stored failure preserved 1','result':'PASS'}}]
for mode,count in [('recovered',78),('public',5)]:assert records[mode]['result_count']==records[mode]['progress_rows']==records[mode]['stdout_rows']==count
failure={}
for mode in ('public','recovered'):
 r=obj('failures/process-membership/'+mode+'/RESULT.json');assert r['checks']==0;failure[mode]={'checks':0,'error':r.get('error'),'identity':ident(read('failures/process-membership/'+mode+'/RESULT.json'))}
partial=ident(read('failures/process-membership/undeclared-partial.bin'));assert partial=={'bytes':25690112,'sha256':'ed75ee885f67eca2938340b1aa5c423a9e60c04bceedfd3f90933cba0c44345e'}
for a,b in [('RESULT.json','RESULT.json'),('progress.jsonl','progress.jsonl'),('primary.log','stdout.log')]:assert read('failures/packaging-reconciliation/'+a)==read('results/primary/'+b)
stored=obj('results/primary/callback-bare-rethrow.json');prior=obj('retained/callback/results/primary/callback-stored-failure.json')
for i,ctx in enumerate(stored['contexts']):
 for k,v in prior['contexts'][i].items():assert ctx[k]==v,k
for k,v in prior.items():
 if k not in ('format','contexts','extension_components'):assert stored[k]==v,k
assert stored['prior_callback_stored_components']==prior['extension_components']
report={'preserved_predecessor_members':checked_predecessor,'preserved_prior_review_members':checked_review,'inherited_definitions':len(olddefs),'new_definitions':sorted(set(newdefs)-set(olddefs)),'nonfunction_AST_unchanged':True,'declared_diff_exact':True,'source_identities':sources,'intermediate_cut_nonmanifest_members_unchanged':len(cut),'intermediate_outer_archive_freshly_verified':False,'supplied_records':records,'primary_qualification':'308 result-recorded; 307 exact progress rows; 303 exact stdout rows. Missing row/lines not repaired; origin UNESTABLISHED. No unsupported aggregate accepted.','zero_assertion_failures':failure,'undeclared_partial':partial,'partial_location':'failures/process-membership; outside strict predecessor root','partial_origin':'UNESTABLISHED','packaging_failure_original_records_exact':True,'all_prior_receipt_fields_preserved':True,'prior_results_rerun':False}
(OUT/'composition-and-supplied.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');print(json.dumps(report,sort_keys=True,indent=2))
