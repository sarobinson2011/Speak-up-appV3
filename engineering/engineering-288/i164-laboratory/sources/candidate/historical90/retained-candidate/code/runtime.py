"""Reuses the reviewed loaded-code/ABI guard; does not instantiate its local anchor."""
import sys,importlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'retained-C2/code'))
import bridge as retained
import session_identity as si
from anchor import enc,sha,need
executor=retained.e
class Guard:
 def __init__(self):
  self.base=si.Identity(retained.ROOT,retained,retained.t,executor,retained.a)
  importlib.import_module('wire')
  importlib.import_module('outcome')
  importlib.import_module('provider')
  importlib.import_module('strict_types')
  importlib.import_module('evidence_record')
  importlib.import_module('stages')
  importlib.import_module('stage_carrier')
  importlib.import_module('signed_eth')
  importlib.import_module('lab_evm')
  self.modules={n:sys.modules[n] for n in ['evidence_record','runtime','anchor','backend','sole_service','connected','wire','outcome','provider','strict_types','stages','stage_carrier','signed_eth','lab_evm']}
  self.raw={n:si.read(Path(m.__file__)) for n,m in self.modules.items()}
  self.refs={n:dict(si.functions(m)) for n,m in self.modules.items()}
  self.codes={n:si.compiled_functions(b) for n,b in self.raw.items()}
  self.literals=[v for n,m in self.modules.items() for v in si.literal_bindings(self.raw[n],m)]
  self.binding={'retained':self.base.binding,'sole_anchor_files':{n:sha(b) for n,b in self.raw.items()}}
  self.signed_decoder=sys.modules['signed_eth']._decode
  self.signed_decoder_code=self.signed_decoder.__wrapped__.__code__
  self.digest=sha(enc(self.binding));self.check()
 def check(self):
  self.base.check()
  need(sys.modules['signed_eth']._decode is self.signed_decoder and self.signed_decoder.__wrapped__.__code__ is self.signed_decoder_code,'SIGNED-DECODER-REPLACED')
  for obj,k,v in self.literals:need(getattr(obj,k)==v,'LOADED-CONSTANT')
  for n,m in self.modules.items():
   need(si.read(Path(m.__file__))==self.raw[n],'CODE-REPLACED:'+n)
   current=dict(si.functions(m));need(current.keys()==self.refs[n].keys(),'CODE-MEMBERS')
   for name,f in current.items():
    need(f is self.refs[n][name] and si.code_value(f.__code__)==self.codes[n][f.__qualname__],'LOADED-CODE:'+n+':'+name)
