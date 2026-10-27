import runpy,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve();ns=runpy.run_path(str(root/'tests/controls.py'),run_name='_audit_only');m=ns['module'](root/'code/correspondence.py')
print(m.enc(m.validate(root,(root/'results/hf01-correspondence.json').read_bytes())).decode(),end='')
