"""Read-only finite saved-export pipeline entry point; no signing/execution."""
import argparse,json
from pathlib import Path
import semantic as s
p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--rules',required=True);p.add_argument('--export',required=True);p.add_argument('--context',required=True);p.add_argument('--output',required=True);a=p.parse_args()
c=s.setup(a.root);root=Path(a.root);out=Path(a.output);s.m.need(not out.exists(),'OUTPUT-EXISTS')
r=json.loads(Path(a.rules).read_bytes());e=json.loads(Path(a.export).read_bytes());d=json.loads((root/'compiler_outputs/compiler-output.json').read_bytes());o=c.ingest(e,a.context,c.binding);result=s.lower(d,r,o,e);out.write_bytes(s.m.enc(result));print(result['exact_finite_pairs'],'finite pairs; final binding BLOCKED')
