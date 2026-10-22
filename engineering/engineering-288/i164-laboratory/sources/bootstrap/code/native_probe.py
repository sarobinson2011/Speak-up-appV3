"""Use retained exact packet, no signing/key generation. Primitive scope only."""
import sys,json
from pathlib import Path
runtime=Path(sys.argv[1]).resolve();witness=json.loads(Path(sys.argv[2]).read_bytes());mode=sys.argv[3] if len(sys.argv)>3 else 'valid'
sys.path[:0]=[str(runtime/'prospective'),str(runtime/'retained-candidate/code')]
import provider
if mode=='invalid':witness['packet']['signature']='00'*64
try:
 r=provider.authenticate('appointment',witness['packet'],witness['public_key'])
except Exception as e:
 if mode!='invalid':raise
 assert str(e)=='RFC8032-AUTHENTICATION';print('PASS invalid signature rejected by retained helper')
else:
 assert mode=='valid' and r==witness['packet']['claim'];print('PASS exact retained signed packet; primitive authentication only')
