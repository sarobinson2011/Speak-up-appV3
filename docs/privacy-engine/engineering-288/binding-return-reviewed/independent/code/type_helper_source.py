"""Read the retained anchor helper through the actual validated input loader."""
from pathlib import Path
import ast,hashlib,json,sys,types
root=Path(sys.argv[1]).resolve();p=root/'code/correspondence.py';m=types.ModuleType('type_sources');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__)
d=m.inputs(root)['prior_data'];items={k:v for k,v in d['ctx']['c'].items() if k.endswith('/anchor.py')};assert items
r={'matched_sources':{},'executed_source':False}
for n,b in items.items():
 f={x.name:x for x in ast.parse(b).body if isinstance(x,ast.FunctionDef)}
 assert ast.unparse(f['sha'].body[0])=='return hashlib.sha256(b).hexdigest()'
 assert ast.unparse(f['enc'].body[0])=="return (json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\\n').encode()"
 r['matched_sources'][n]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'sha_definition':ast.get_source_segment(b.decode(),f['sha']),'enc_definition':ast.get_source_segment(b.decode(),f['enc'])}
Path(sys.argv[2]).write_text(json.dumps(r,indent=2)+'\n')
