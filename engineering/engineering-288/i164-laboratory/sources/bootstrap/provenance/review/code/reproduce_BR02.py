"""Isolated helper witness only. Does not chmod, create DBs or run lifecycle."""
import sys,json
from pathlib import Path
root=Path(sys.argv[1]).resolve();witness=json.loads(Path(sys.argv[2]).read_bytes())
sys.path[:0]=[str(root/'prospective'),str(root/'retained-candidate/code')]
import provider
try:provider.authenticate('appointment',witness['packet'],witness['public_key'])
except Exception as e:
 assert str(e)=='BACKEND-UNAVAILABLE' and isinstance(e.__cause__,PermissionError)
 print('REPRODUCED BR-02: authenticated helper bytes, permission-denied execution')
else:raise AssertionError('original BR-02 no longer reproduced; do not count as current defect')
