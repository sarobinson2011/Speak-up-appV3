"""Exact byte-continuity and supplied-evidence inspection, no code execution."""
from pathlib import Path
import hashlib,json,sys,zipfile
r=Path(sys.argv[1]);out=Path(sys.argv[2]);oldzip=Path(sys.argv[3]);reviewzip=Path(sys.argv[4])
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
deps=json.loads((r/'DEPENDENCIES.json').read_bytes())
for p,n in [(oldzip,'reviewed_reference_extension'),(reviewzip,'reference_independent_support')]:assert identity(p.read_bytes())=={k:deps[n][k] for k in ('bytes','sha256')}
for p,prefix,omit,count in [(oldzip,'retained/references',None,552),(reviewzip,'provenance/reference-review','input/I164-reference-transfer-correspondence-1.zip',34)]:
 with zipfile.ZipFile(p) as z:expected={n:z.read(n) for n in z.namelist() if n!=omit}
 actual={q.relative_to(r/prefix).as_posix():q.read_bytes() for q in (r/prefix).rglob('*') if q.is_file()};assert actual==expected and len(actual)==count
changes=json.loads((r/'CHANGED-IDENTITIES.json').read_bytes())
for p,v in changes['implementation_files'].items():assert identity((r/p).read_bytes())==v['after'] and identity((r/'retained/references'/p).read_bytes())==v['before']
old=(r/'retained/references/code/managed_coverage.py').read_bytes();new=(r/'code/managed_coverage.py').read_bytes()
assert new[:new.index(b'# Recovery return fields:')].rstrip()==old[:old.index(b'def main():')].rstrip() and new[new.index(b'def main():'):]==old[old.index(b'def main():'):]
old=(r/'retained/references/code/correspondence.py').read_bytes();new=(r/'code/correspondence.py').read_bytes()
assert new[:new.index(b'def validate_references(')].replace(b'def derive_references(',b'def derive(').rstrip()==old[:old.index(b'def validate(')].rstrip()
prior=json.loads((r/'retained/references/results/reference-correspondence.json').read_bytes());current=json.loads((r/'results/recovery-field-correspondence.json').read_bytes())
for k in prior:
 if k not in ('format','contexts','extension_components'):assert prior[k]==current[k],k
assert current['prior_reference_components']==prior['extension_components']
assert len(prior['contexts'])==len(current['contexts'])==2
for a,b in zip(prior['contexts'],current['contexts']):assert all(a[k]==b[k] for k in a)
supplied={}
for name,path,count in [('primary','results/primary/RESULT.json',117),('recovered','results/recovered.json',30),('input_gates','results/input-gates.json',5)]:
 d=json.loads((r/path).read_bytes());assert d['result']=='PASS' and d['passed']==len(d['checks'])==count
 if name=='primary':assert d['error'] is None and d['source']==d['source_after']=={Path(p).name:v['after'] for p,v in changes['implementation_files'].items()}
 supplied[name]={'reported_checks':count,'inspected_not_run':True}
f=json.loads((r/'results/fresh-process.stdout').read_bytes());assert f['result']=='PASS' and f['receipt']==identity((r/'results/recovery-field-correspondence.json').read_bytes()) and (r/'results/fresh-process.stderr').read_bytes()==b''
note=json.loads((r/'results/packaging-discrepancy.json').read_bytes());assert note['source_of_discrepancy']=='UNKNOWN' and note['recovered_controls_started'] is False and note['second_attempt']['controls_started'] is False
result={'result':'PASS','retained_reference_members_unchanged':552,'prior_independent_noninput_members_unchanged':34,'external_previous_archives_verified':{'reference_input':identity(oldzip.read_bytes()),'independent_review':identity(reviewzip.read_bytes())},'implementation_changes':changes['implementation_files'],'all_old_context_fields_and_obligations_preserved':True,'prior_receipt':identity((r/'retained/references/results/reference-correspondence.json').read_bytes()),'new_receipt':identity((r/'results/recovery-field-correspondence.json').read_bytes()),'supplied':supplied,'supplied_process_checks':1,'supplied_packaging_discrepancies_preserved':2,'discrepancy_cause':'UNKNOWN; damaged temporary archive bytes not present here','historical_manifests_keep_original_partial_copy_scopes':True}
out.write_text(json.dumps(result,indent=2)+'\n');print('PASS composition, prospective changed-file identities, prior output and supplied evidence')
