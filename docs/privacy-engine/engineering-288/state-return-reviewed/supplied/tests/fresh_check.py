import runpy,sys,json
from pathlib import Path
root=Path(sys.argv[1]).resolve()
ns=runpy.run_path(str(root/'tests/controls.py'),run_name='_install_guards_only')
m=ns['module'](root/'code/correspondence.py')
print(json.dumps(m.validate(root,(root/'results/state-correspondence.json').read_bytes()),sort_keys=True))
