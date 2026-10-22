import sys,copy
from pathlib import Path
import universe as u
P=Path(__file__).resolve().parents[1];root=Path(sys.argv[1]);out=Path(sys.argv[2]);x=u.c.load(P/'outputs/universe.json');saved=u.c.load(P/'outputs/consumption.json')
r=u.consume(root,x);u.c.same(r,saved,'FRESH-RECOVERY-CORRESPONDENCE')
bad=copy.deepcopy(r);bad.update(full_expansion_ready=True,production_instance_total=0)
try:u.validate_result(root,x,bad)
except ValueError:pass
else:raise AssertionError('FALSE-RESULT')
try:u.require_ready(root,x)
except ValueError as e:assert str(e)=='UNKNOWN-LIFETIME-AND-QUALIFIED-OBLIGATIONS'
else:raise AssertionError('READINESS')
out.write_bytes(u.c.enc({'fresh_process':True,'recovered_root':True,'groups':3,'result':'PASS','checks':['exact-consumed-input-correspondence','false-zero/readiness-result-rejected','readiness-remains-blocked']}));print('PASS 3 fresh recovered controls')
