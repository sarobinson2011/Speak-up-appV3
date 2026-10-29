"""Read-only preservation and IS-01 boundary audit; no candidate execution."""
from pathlib import Path
import ast,hashlib,json,sys,stat,os
r=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]);out.parent.mkdir(parents=True,exist_ok=True)
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def funcs(b):return {n.name:ast.get_source_segment(b.decode(),n) for n in ast.parse(b).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
old=(r/'original/code/managed_coverage.py').read_bytes();new=(r/'code/managed_coverage.py').read_bytes();of=funcs(old);nf=funcs(new);extension={'status_forward_source','compile_status_forward','validate_status_forward','status_snapshot_value','status_forward_projection','validate_status_forward_projection'}
unchanged=[n for n in of if of[n]==nf[n]];changed=[n for n in of if of[n]!=nf[n]];added=sorted(set(nf)-set(of));assert set(changed)<=extension and added==['status_exact_tree','status_typed_same'];assert old[:old.index(b'def status_forward_source(')]==new[:new.index(b'def status_exact_tree(')]
assert all(of[n]==nf[n] for n in of if n not in extension)
code=(r/'code/correspondence.py').read_bytes();af=funcs(code);assert nf['status_exact_tree'].replace('need(', 'require(')==af['status_exact_tree']
# Check original exact membership/types/hashes independently of candidate gate.
manifest=json.loads((r/'original/MANIFEST.json').read_bytes());expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};actual=set();seen=set()
for base,ds,fs in os.walk(r/'original',followlinks=False):
 for n in ds:
  p=Path(base)/n;assert stat.S_ISDIR(p.lstat().st_mode);seen.add(p.relative_to(r/'original').as_posix())
 for n in fs:
  p=Path(base)/n;assert stat.S_ISREG(p.lstat().st_mode);actual.add(p.relative_to(r/'original').as_posix())
assert actual==expected and seen==dirs
for n,pin in manifest.items():assert identity((r/'original'/n).read_bytes())==pin,n
# Review is exact except its explicitly omitted redundant target ZIP.
rm=json.loads((r/'review/MANIFEST.json').read_bytes());omitted='input/I164-internal-status-return-correspondence-1.zip';assert omitted in rm
reviewfiles={p.relative_to(r/'review').as_posix() for p in (r/'review').rglob('*') if p.is_file()};assert reviewfiles==(set(rm)|{'MANIFEST.json'})-{omitted}
for n,pin in rm.items():
 if n!=omitted:assert identity((r/'review'/n).read_bytes())==pin,n
runtime=[]
for p in (r/'original').rglob('*.py'):
 if p.name in ['live_connection.py','lab_bootstrap.py','prospective_entry.py']:
  runtime.append({'path':str(p.relative_to(r)),'identity':identity(p.read_bytes())})
# Pin intentional current changes and separately preserve pre-root-guard primary components.
changes={n:{'before':identity((r/'original/code'/n).read_bytes()),'after':identity((r/'code'/n).read_bytes())} for n in ['managed_coverage.py','correspondence.py']}
record={'result':'PASS','scope':'Static preservation and boundary audit, not runtime or independent review','inherited_functions_unchanged':unchanged,'current_extension_functions_changed':changed,'functions_added':added,'historical_prefix_byte_identical':True,'two_exact_tree_algorithms_identical':True,'original_members':len(actual),'original_directories':len(dirs),'review_non_input_records':len(reviewfiles),'runtime_sources_unchanged':runtime,'intentional_code_changes':changes,'primary_adapter_before_root_type_guard':identity((r/'provenance/primary-correspondence.py').read_bytes()),'unchanged_semantics':'Exact types only. No source values, caller routes, guards, copies, exception/termination classification, destinations, duties or authority changed.'}
out.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:v for k,v in record.items() if k not in ['runtime_sources_unchanged','inherited_functions_unchanged','intentional_code_changes']},indent=2))
