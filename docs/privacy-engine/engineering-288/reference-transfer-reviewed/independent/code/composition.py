"""Read-only archive composition/preservation audit; no candidate imports."""
from pathlib import Path
import difflib,hashlib,json,sys,zipfile
root=Path(sys.argv[1]);out=Path(sys.argv[2]);old_input=Path(sys.argv[3]);old_review=Path(sys.argv[4])
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
deps=json.loads((root/'DEPENDENCIES.json').read_bytes())
for path,name in [(old_input,'reviewed_field_extension'),(old_review,'field_independent_support')]:
 pin=deps[name];assert ident(path.read_bytes())=={k:pin[k] for k in ('bytes','sha256')}
 with zipfile.ZipFile(path) as z:assert len(z.infolist())==pin['entries']
with zipfile.ZipFile(old_input) as z:
 expected={n:z.read(n) for n in z.namelist()}
 actual={p.relative_to(root/'retained/fields').as_posix():p.read_bytes() for p in (root/'retained/fields').rglob('*') if p.is_file()}
 assert actual==expected and len(actual)==489
with zipfile.ZipFile(old_review) as z:
 expected={n:z.read(n) for n in z.namelist() if n!='input/I164-status-field-correspondence-1.zip'}
 actual={p.relative_to(root/'retained/field-independent-review').as_posix():p.read_bytes() for p in (root/'retained/field-independent-review').rglob('*') if p.is_file()}
 assert actual==expected and len(actual)==27
changes=json.loads((root/'CHANGED-IDENTITIES.json').read_bytes())
for row in changes['intentional_implementation_changes']:
 assert ident((root/row['path']).read_bytes())==row['after']
 assert ident((root/'retained/fields'/row['path']).read_bytes())==row['before']
for rel,pin in deps['source_and_guard_pins'].items():assert ident((root/'retained/fields'/rel).read_bytes())==pin
old=(root/'retained/fields/code/managed_coverage.py').read_bytes();new=(root/'code/managed_coverage.py').read_bytes()
assert new[:new.index(b'# Appended to the existing declaration producer.')].rstrip()==old[:old.index(b'def main():')].rstrip()
assert new[new.index(b'def main():'):]==old[old.index(b'def main():'):]
old=(root/'retained/fields/code/correspondence.py').read_bytes();new=(root/'code/correspondence.py').read_bytes()
assert new[:new.index(b'def validate_fields(')].replace(b'def derive_fields(',b'def derive(').rstrip()==old[:old.index(b'def validate(')].rstrip()
supplied=[]
for name in ('attempt-2','recovered'):
 d=json.loads((root/'results'/name/'RESULT.json').read_bytes());assert d['result']=='PASS' and d['error'] is None and d['passed']==len(d['checks'])==182
 assert d['source']==d['source_after']=={Path(r['path']).name:r['after'] for r in changes['intentional_implementation_changes']}
 paths=json.loads((root/'results'/name/'constructed-paths.json').read_bytes());assert len(paths)==21 and all(p['actual_observation'] is False for p in paths.values())
 supplied.append({'name':name,'controls':182,'constructed_cases':21,'recorded_root':d['root'],'inspected_not_executed':True})
failed=json.loads((root/'results/attempt-1/RESULT.json').read_bytes());assert failed['result']=='FAIL' and failed['passed']==0
assert failed['source']=={n:ident((root/'failures/attempt-1'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
fresh=json.loads((root/'results/fresh-process.stdout').read_bytes());assert fresh['receipt']==changes['new_output'] and fresh['result']=='PASS' and (root/'results/fresh-process.stderr').read_bytes()==b''
before=json.loads((root/'retained/fields/results/status-field-correspondence.json').read_bytes());after=json.loads((root/'results/reference-correspondence.json').read_bytes())
assert ident((root/'retained/fields/results/status-field-correspondence.json').read_bytes())==changes['prior_output_unchanged']
assert ident((root/'results/reference-correspondence.json').read_bytes())==changes['new_output']
for key in before:
 if key not in ('format','contexts','extension_components'):assert before[key]==after[key],key
assert before['extension_components']==after['prior_field_components']
for one,two in zip(before['contexts'],after['contexts']):
 for key in one:assert one[key]==two[key],(one['context'],key)
assert len(before['contexts'])==len(after['contexts'])==2
result={'result':'PASS','reviewed_field_root_unchanged_members':489,'independent_review_unchanged_noninput_members':27,
 'externally_retained_predecessor_archives_verified':{name:ident(p.read_bytes()) for name,p in [('field_input',old_input),('independent_review',old_review)]},
 'all_previous_context_fields_and_obligations_preserved':True,'historical_compiler_body_and_CLI_byte_preserved':True,'historical_field_body_byte_preserved_except_name':True,
 'intentional_changes':changes['intentional_implementation_changes'],'new_output':changes['new_output'],'prior_output':changes['prior_output_unchanged'],
 'supplied_controls':supplied,'supplied_process_checks':1,'supplied_failure':{'passed':0,'error':failed['error'],'original_code_and_output_preserved':True},
 'historical_partial_review_manifest_scope_preserved':True,'current_offline_recovery_complete_without_external_original_zip':True}
out.write_text(json.dumps(result,indent=2)+'\n');print('PASS archive composition, source pins, preserved outputs and supplied records')
