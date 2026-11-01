"""Freeze the bounded new-producer correction after preserving its zero-control failure."""
from pathlib import Path
import ast,difflib,hashlib,json
T=Path(__file__).resolve().parents[1];root=T/'input';prior=root/'retained/client-construction'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
before=(prior/'code/managed_coverage.py').read_bytes();after=before+b'\n'+(T/'tools/producer-addition.py').read_bytes();(root/'code/managed_coverage.py').write_bytes(after)
p=root/'code/correspondence.py';s=p.read_text();lines=s.splitlines(True)
n=next(n for n in ast.parse(s).body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='PRODUCER_PIN');lines[n.lineno-1:n.end_lineno]=['PRODUCER_PIN='+repr(ident(after))+'\n'];p.write_text(''.join(lines))
for p in [*(root/'code').glob('*.py'),*(root/'tests').glob('*.py')]:compile(p.read_bytes(),str(p),'exec')
old=ast.parse(before);new=ast.parse(after);assert len(new.body)==len(old.body)+6 and all(ast.dump(a,include_attributes=True)==ast.dump(b,include_attributes=True) for a,b in zip(old.body,new.body))
record=json.loads((root/'provenance/changed-files.json').read_bytes());diff=[]
for n in ('managed_coverage.py','correspondence.py'):
 a=(prior/'code'/n).read_bytes();b=(root/'code'/n).read_bytes();record['intentional_changes']['code/'+n]={'before':ident(a),'after':ident(b)};diff.extend(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile='reviewed/'+n,tofile='proposed/'+n))
record['new_source_preparation_failure']='Preserved separately: failures/source-initial; zero controls; no completed campaign replay'
(root/'provenance/changed-files.json').write_bytes(enc(record));(root/'provenance/implementation.diff').write_text(''.join(diff))
m={p.relative_to(root).as_posix():ident(p.read_bytes()) for p in sorted(root.rglob('*')) if p.is_file() and p!=root/'MANIFEST.json'};(root/'MANIFEST.json').write_bytes(enc(m));print(json.dumps({'files':len(m)+1,'changes':record['intentional_changes']}))
