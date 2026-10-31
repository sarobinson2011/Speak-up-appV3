"""Finish only the original unfinished altered-source control; no 285-row replay."""
from pathlib import Path
import sys,traceback,json
root=Path(sys.argv[1]).absolute();sys.path.insert(0,str(root/'tests'))
from offline import *
rec=Record(sys.argv[2]);error=None
try:
 rec.save('input-verification.json',verify_root(root));monitor=guard(root,rec.path);m=module(root/'code/correspondence.py');monitor(m);data=m.inputs(root);entry=m.sources(data)[1];c=data['coverage']
 print('Only unfinished source-argument rejection; previous 285 rows are preserved, not replayed',flush=True)
 rec.reject('altered defining construction token',lambda:c.compile_control_construction(m.sources(data)[0],entry.replace(b'control(_Control(token))',b'control(_Control(owner))'),*m.dependencies(data)))
 rec.save('final-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='One unfinished source control only; original primary campaign remains interrupted with 285 corroborated rows')
