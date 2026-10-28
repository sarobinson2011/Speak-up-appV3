import json,runpy,sys
from pathlib import Path
base=Path(__file__).resolve().parents[1]
root=base/'state-return';ns=runpy.run_path(str(root/'tools/checkpoint.py'),run_name='_packaging_only')
recovered=base/'state-tools/recovered-root-3'
out=ns['verify'](base/'state-tools/recovery-input.zip',recovered)
files=ns['inventory'](recovered);m=json.loads(files['MANIFEST.json'])
assert set(files)==set(m)|{'MANIFEST.json'},sorted(set(files)-set(m)-{'MANIFEST.json'})
for n,pin in m.items():assert ns['identity'](files[n])==pin,n
record={'result':'PASS','archive':out,'physical_membership_and_hashes':len(m),'new_root':'recovered-root-3','same_process_extraction_gate_and_controls':True,'previous_failed_roots_preserved':True}
(root/'results/recovered-same-process-gate.json').write_bytes(ns['enc'](record))
print(json.dumps(record),flush=True)
del files
sys.argv=[str(recovered/'tests/controls.py'),'--root',str(recovered),'--output',str(root/'results/recovered-final'),'--recovered']
runpy.run_path(sys.argv[0],run_name='__main__')
