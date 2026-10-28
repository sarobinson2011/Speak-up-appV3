import json,runpy,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve();g=runpy.run_path(str(root/'tests/controls.py'),run_name='_guards_only');m=g['module'](root/'code/correspondence.py')
print(json.dumps(m.validate(root,(root/'results/client-handle-correspondence.json').read_bytes()),sort_keys=True))
