"""Minimal review witness for live Candidate output aliasing. No candidate edits.
Run each mode in a fresh Python process; consumes existing four-KiB head evidence.
"""
import sys,pathlib,json,hashlib,gzip,socket,time
root=pathlib.Path(sys.argv[1]).resolve();mode=sys.argv[2];out=pathlib.Path(sys.argv[3]);sys.dont_write_bytecode=True
sys.path.insert(0,str(root/'integration'))
def forbidden(*a,**k):raise AssertionError('No network permitted')
socket.socket=forbidden;socket.create_connection=forbidden
from candidate_pipeline import Candidate,parse,enc,Invalid
start=time.monotonic();c=Candidate();w=root/'support/preserved-review/SD-01-minimal.json';e=parse(w.read_bytes(),200000000)
x=c.ingest(e,'SYMBOLIC-U-ONE',c.binding)
original={'binding_keys':sorted(x['binding']),'blockers':list(x['blockers']),'candidate_reference':x['binding']['candidate'],'downstream_adapter':x['binding']['downstream_adapter']}
if mode=='binding':
 assert x['binding'] is c.binding
 del x['binding']['downstream_adapter']
else:
 import baseline
 assert x['blockers'] is baseline.BLOCKERS
 x['blockers'].clear()
accepted=c.validate_output(x,e)
assert accepted is True
r={'mode':mode,'result':'COUNTEREXAMPLE-REPRODUCED','saved_witness':{'path':str(w.relative_to(root)),'bytes':w.stat().st_size,'sha256':hashlib.sha256(w.read_bytes()).hexdigest()},'mutation':"del out['binding']['downstream_adapter']" if mode=='binding' else "out['blockers'].clear()",'prior':original,'validated_after_mutation':accepted,'binding_keys_after':sorted(x['binding']),'blockers_after':x['blockers'],'final_binding':x['final_binding'],'canonical_registration':x['canonical_registration'],'actual_admission':x['actual_admission'],'stream_identities':x['stream_identities'],'candidate_code_changed':False,'elapsed_seconds':time.monotonic()-start}
try:c.final_binding()
except Invalid as err:r['final_bind_still_rejects']=str(err)
else:raise AssertionError('final binding unexpectedly accepted')
if mode=='binding':
 fresh=Candidate()
 try:fresh.validate_output(parse(enc(x),500000000),e)
 except Invalid as err:r['new_instance_rejection']=str(err)
 else:r['new_instance_rejection']=None
out.write_text(json.dumps(r,indent=2)+'\n')
artifact=out.with_suffix('.mutant.json.gz');artifact.write_bytes(gzip.compress(enc(x),mtime=0));r['mutant_output_bytes']=len(enc(x));r['mutant_compressed_bytes']=artifact.stat().st_size;out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
