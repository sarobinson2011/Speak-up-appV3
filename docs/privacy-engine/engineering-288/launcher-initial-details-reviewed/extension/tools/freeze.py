"""Freeze new source and declared saved-input tree; no model execution."""
from pathlib import Path
import ast,difflib,hashlib,json,shutil
T=Path(__file__).resolve().parents[1];root=T/'input'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
prior=root/'retained/client-construction'
before=(prior/'code/managed_coverage.py').read_bytes();addition=(T/'tools/producer-addition.py').read_bytes();after=before+b'\n'+addition
(root/'code/managed_coverage.py').write_bytes(after)
p=root/'code/correspondence.py';raw=p.read_text();assert 'PRODUCER_PIN=None' in raw;p.write_text(raw.replace('PRODUCER_PIN=None', 'PRODUCER_PIN='+repr(ident(after)),1))
offline=(prior/'tests/offline.py').read_text().replace("'engineering-client-construction'","'engineering-launcher-details'").replace("('_checked','derive_status','derive_client_state','derive_client','derive_handle')","('validate','_basis','_checked','derive_status','derive_client_state','derive_client','derive_handle')").replace("('semantic','derive_client_construction','validate','_checked','_basis','constructed_projection')","('semantic','derive_launcher_details','validate','_checked','_basis','_public_predecessor','constructed_projection')")
(root/'tests/offline.py').write_text(offline)
for p in (root/'code').glob('*.py'):compile(p.read_bytes(),str(p),'exec')
for p in (root/'tests').glob('*.py'):compile(p.read_bytes(),str(p),'exec')
old=ast.parse(before);new=ast.parse(after);assert len(new.body)==len(old.body)+6 and all(ast.dump(a,include_attributes=True)==ast.dump(b,include_attributes=True) for a,b in zip(old.body,new.body))
changes={};diff=[]
for n in ('managed_coverage.py','correspondence.py'):
 a=(prior/'code'/n).read_bytes();b=(root/'code'/n).read_bytes();changes['code/'+n]={'before':ident(a),'after':ident(b)}
 diff.extend(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile='reviewed/'+n,tofile='proposed/'+n))
(root/'provenance/changed-files.json').write_bytes(enc({'intentional_changes':changes,'inherited_producer_definitions_unchanged':sum(isinstance(x,ast.FunctionDef) for x in old.body),'new_producer_definitions':6,'prior_reviewed_root_changes':0,'runtime_source_changes':0,'new_authentication_mechanism':'Actual unchanged predecessor public validation with passive CPython3.12 monitoring of one returned basis; no replacement. Busy slot stops.'}))
(root/'provenance/implementation.diff').write_text(''.join(diff))
(root/'provenance/prior-review-incorporation.json').write_bytes((root/'provenance/prior-review-incorporation.json').read_bytes())
manifest={p.relative_to(root).as_posix():ident(p.read_bytes()) for p in sorted(root.rglob('*')) if p.is_file()}
assert 'MANIFEST.json' not in manifest
(root/'MANIFEST.json').write_bytes(enc(manifest));print(json.dumps({'files':len(manifest)+1,'new_changed_files':changes}))
