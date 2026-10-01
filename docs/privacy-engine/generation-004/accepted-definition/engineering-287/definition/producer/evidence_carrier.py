"""Proposed V2 documentary evidence envelope. Lossless framing, not authentication.
Never parse source-specific witness bytes as though their interpretation were known.
"""
from pathlib import Path
import csv,struct
from functools import lru_cache
O=Path(__file__).resolve().parents[1]
MAGIC=b'PE-G4-PRODUCER-EVIDENCE-V2\x00'
PHASES=('ADMISSION','VERIFICATION','E','AUTHORIZED','PRE-EXECUTION','PRE-COMMITMENT','DELIVERY','RECOVERY','STATIC')
STATUS={'INAPPLICABLE':0,'UNAVAILABLE':1,'PRESENT':2};REVERSE={v:k for k,v in STATUS.items()}
@lru_cache(maxsize=1)
def directory():
 d={}
 for r in csv.DictReader((O/'privacy/producer-proposal/evidence-fields.tsv').open(),delimiter='\t'):d.setdefault(r['record'],[]).append(r['field'])
 return d
# These exact sets are part of this author-proposed carrier format, not inferred from record values.
RECORD_PHASES={
'candidate-domain':('ADMISSION','E'), 'admission-binding':('ADMISSION','E'), 'evaluation-binding':('E',),
'history-view':('E','PRE-EXECUTION','PRE-COMMITMENT'), 'state-view':('E','PRE-EXECUTION','PRE-COMMITMENT'),
'phase-view':('E','PRE-EXECUTION','PRE-COMMITMENT'),
'verifier-basis':('VERIFICATION','E'), 'verifier-execution':('VERIFICATION','E'), 'verifier-call':('VERIFICATION','E'),
'carrier-binding':('E','AUTHORIZED','PRE-EXECUTION','PRE-COMMITMENT'),
'evaluation-completion':('E',), 'component-view':('AUTHORIZED','PRE-EXECUTION','PRE-COMMITMENT'),
'comparison-view':('AUTHORIZED','PRE-EXECUTION','PRE-COMMITMENT'),
'commit-view':('PRE-COMMITMENT',), 'delivery-view':('DELIVERY',), 'recovery-view':('RECOVERY',), 'privacy-static':('STATIC',)}
# Historical E/C remain present in E's evaluation-binding. Gate phase-view binds the authorization instead.
E_ONLY={'E','C'}
GATE_ONLY={'authorization_binding','D','Q0','mapping_profile_binding','U','stage','attempt'}
def applicable(record,field,phase):
 if phase not in PHASES:raise ValueError('unknown phase')
 if phase not in RECORD_PHASES[record]:return False
 if record=='phase-view':
  if phase=='E' and field in GATE_ONLY:return False
  if phase!='E' and field in E_ONLY:return False
 return True
class FramingError(ValueError):pass
def u64(n):
 if not isinstance(n,int) or not 0<=n<2**64:raise FramingError('length overflow')
 return struct.pack('>Q',n)
def lp(b):
 if not isinstance(b,bytes):raise FramingError('bytes required')
 return u64(len(b))+b
def validate_shape(phase,records):
 d=directory()
 if phase not in PHASES or list(records)!=list(d):raise FramingError('phase or exact record directory mismatch')
 for rec,fields in d.items():
  v=records[rec]
  if set(v)!={'status','instances'} or v['status'] not in STATUS or not isinstance(v['instances'],list):raise FramingError('record shape')
  inphase=phase in RECORD_PHASES[rec]
  if (v['status']=='INAPPLICABLE')==inphase:raise FramingError('wrong record applicability')
  if v['status']!='PRESENT' and v['instances']:raise FramingError('absent record has instances')
  if v['status']=='PRESENT' and not v['instances']:raise FramingError('present record has no instance')
  for inst in v['instances']:
   if list(inst)!=fields:raise FramingError('exact ordered field directory mismatch')
   for field in fields:
    value=inst[field];needed=applicable(rec,field,phase)
    if needed and not isinstance(value,bytes):raise FramingError('applicable field requires bytes')
    if not needed and value is not None:raise FramingError('inapplicable field must have explicit absent tag')
 return True
def encode(phase,records):
 validate_shape(phase,records)
 out=MAGIC+lp(phase.encode('ascii'))+u64(len(records))
 for rec,v in records.items():
  out+=lp(rec.encode('ascii'))+bytes([STATUS[v['status']]])+u64(len(v['instances']))
  for inst in v['instances']:
   payload=u64(len(inst))
   for field,value in inst.items():payload+=lp(field.encode('ascii'))+(b'\x00' if value is None else b'\x01'+lp(value))
   out+=lp(payload)
 return out
class Reader:
 def __init__(self,b):self.b=b;self.p=0
 def take(self,n):
  if n>len(self.b)-self.p:raise FramingError('truncated value')
  v=self.b[self.p:self.p+n];self.p+=n;return v
 def uint(self):return int.from_bytes(self.take(8),'big')
 def blob(self):return self.take(self.uint())
 def ascii(self):
  try:return self.blob().decode('ascii')
  except UnicodeDecodeError:raise FramingError('non-ASCII identity')
 def end(self):
  if self.p!=len(self.b):raise FramingError('trailing bytes')
def decode(raw):
 if not isinstance(raw,bytes):raise FramingError('bytes required')
 r=Reader(raw)
 if r.take(len(MAGIC))!=MAGIC:raise FramingError('wrong format/version')
 phase=r.ascii();d=directory();out={}
 if phase not in PHASES or r.uint()!=len(d):raise FramingError('phase/directory mismatch')
 for expected,fields in d.items():
  if r.ascii()!=expected:raise FramingError('record omission/duplication/reordering')
  code=r.take(1)[0]
  if code not in REVERSE:raise FramingError('unknown status')
  count=r.uint()
  # Each instance requires at least an eight-byte prefix; bound before looping.
  if count>(len(raw)-r.p)//8:raise FramingError('impossible instance count')
  instances=[]
  for _ in range(count):
   q=Reader(r.blob())
   if q.uint()!=len(fields):raise FramingError('field count')
   inst={}
   for f in fields:
    if q.ascii()!=f:raise FramingError('field omission/duplication/reordering')
    tag=q.take(1)[0]
    if tag not in (0,1):raise FramingError('unknown field tag')
    inst[f]=None if tag==0 else q.blob()
   q.end();instances.append(inst)
  out[expected]={'status':REVERSE[code],'instances':instances}
 r.end();validate_shape(phase,out);return phase,out
def acquisition_status(phase,records):
 validate_shape(phase,records)
 missing=[k for k,v in records.items() if v['status']=='UNAVAILABLE']
 return {'unavailable_records':missing,'framing_complete':not missing,'semantic_validation':'REQUIRED','authenticated':False,'protocol_permission':False}
