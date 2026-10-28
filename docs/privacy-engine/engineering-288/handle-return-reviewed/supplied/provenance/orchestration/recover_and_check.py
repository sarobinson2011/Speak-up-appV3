"""Package a stable input, extract once and run only the new recovered controls."""
import json,runpy,sys
from pathlib import Path
B=Path(__file__).resolve().parents[1];R=B/'handle-return';ns=runpy.run_path(str(R/'tools/checkpoint.py'),run_name='_packaging_only')
files={n:b for n,b in ns['inventory'](R).items() if not n.startswith('results/primary/')}
target=B/'handle-tools/recovery-input.zip';out=ns['pack'](files,target);recovered=B/'handle-tools/recovered-root';ns['verify'](target,recovered)
actual=ns['inventory'](recovered);m=json.loads(actual['MANIFEST.json']);assert set(actual)==set(m)|{'MANIFEST.json'}
for n,pin in m.items():assert ns['identity'](actual[n])==pin,n
report={'identity':out,'physical_gate_files':len(m),'extraction_and_controls_same_process':True,'intermediate_not_final_checkpoint':True,'excluded':'Only primary in-progress results; later final metadata remains separate.'}
(R/'results/recovery-input.json').write_bytes(ns['enc'](report));print(json.dumps(report),flush=True)
del actual,files
sys.argv=[str(recovered/'tests/controls.py'),'--root',str(recovered),'--output',str(R/'results/recovered'),'--recovered'];runpy.run_path(sys.argv[0],run_name='__main__')
