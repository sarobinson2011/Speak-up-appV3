from pathlib import Path
import zipfile,io,json,hashlib,sys
r=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();candidate_parent=Path(sys.argv[3]).resolve()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def unpack(b):
 with zipfile.ZipFile(io.BytesIO(b)) as z:return {n:z.read(n) for n in z.namelist()}
deps=json.loads((r/'DEPENDENCIES.json').read_bytes());closure=(r/'inputs/closure-review.zip').read_bytes()
assert identity(closure)=={k:deps['independent_closure'][k] for k in ('bytes','sha256')}
review=unpack(closure);previous=unpack(review['input/I164-SOC02-R1-correction.zip'])
expected={n[len('corrected/'):]:b for n,b in previous.items() if n.startswith('corrected/')}
actual={p.relative_to(r/'retained/occurrence').as_posix():p.read_bytes() for p in (r/'retained/occurrence').rglob('*') if p.is_file()};assert actual==expected and len(actual)==467
for n in ('CHECKPOINT.json','REPORT.md'):assert (r/'review'/n).read_bytes()==review[n]
boundary=unpack(expected['inputs/correction.zip'])
assert (r/'original/code/correspondence.py').read_bytes()==boundary['code/correspondence.py']
assert (r/'original/code/managed_coverage.py').read_bytes()==boundary['retained/candidate/compiler/managed_coverage.py']
changed=json.loads((r/'CHANGED-IDENTITIES.json').read_bytes())
for row in changed['implementation_changes']:
 assert identity((r/row['path']).read_bytes())==row['after']
 assert identity((r/'original'/row['path']).read_bytes())==row['before']
old=(r/'original/code/managed_coverage.py').read_bytes();new=(r/'code/managed_coverage.py').read_bytes()
assert new[:new.index(b'# Bounded status-return extension.')]==old[:old.index(b'def main():')]
assert new[new.index(b'def main():'):]==old[old.index(b'def main():'):]
old=(r/'original/code/correspondence.py').read_bytes();new=(r/'code/correspondence.py').read_bytes()
assert new[:new.index(b'# New field-level connection.')].replace(b'def derive_boundary(',b'def derive(').rstrip()==old[:old.index(b'def validate(')].rstrip()
with zipfile.ZipFile(candidate_parent) as z:candidate=z.read('inputs/candidate.zip')
cpin=deps['candidate_archive_guard_provenance'] if 'candidate_archive_guard_provenance' in deps else next(v for v in deps.values() if isinstance(v,dict) and v.get('sha256')=='152207d3140b4d9b0d97890b5ce38f5f4ff4bab3bc009af951e489faaf534a42')
assert identity(candidate)=={k:cpin[k] for k in ('bytes','sha256')}
guards={}
with zipfile.ZipFile(io.BytesIO(candidate)) as z:
 for n,pin in deps['reused_guard_modules'].items():
  b=z.read('compiler/'+n);assert identity(b)=={k:pin[k] for k in ('bytes','sha256')};assert b==(r/'retained/compiler'/n).read_bytes();guards[n]=identity(b)
supplied=[]
for group in ('fresh','recovered'):
 d=json.loads((r/'results'/group/'RESULT.json').read_bytes());assert d['result']=='PASS' and d['error'] is None and d['passed']==len(d['checks'])==156
 assert d['source']==d['source_after']=={Path(row['path']).name:row['after'] for row in changed['implementation_changes']}
 supplied.append({'group':group,'reported_controls':156,'recorded_root':d['root'],'inspected_not_run':True})
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps({'result':'PASS','retained_occurrence_members':467,'retained_boundary_members':463,'prior_receipt':identity(expected['results/occurrence-connection.json']),'SOC_closed_adapter':identity(expected['code/smoke_occurrences.py']),'historical_compiler_body_and_CLI_byte_preserved':True,'boundary_body_byte_preserved_except_function_rename':True,'guard_provenance':{'candidate_archive':identity(candidate),'exact_selected_members':guards,'only_two_members_compared_no_pipeline_or_full_candidate_recheck':True},'intentional_changes':changed['implementation_changes'],'supplied_controls':supplied,'candidate_and_draft_map_counts':{n:len(json.loads(boundary['retained/launcher/provenance/'+n+'-members.json'])) for n in ('candidate','draft')}},indent=2)+'\n')
print('PASS composition, intentional changes, guard source provenance, supplied result identities')
