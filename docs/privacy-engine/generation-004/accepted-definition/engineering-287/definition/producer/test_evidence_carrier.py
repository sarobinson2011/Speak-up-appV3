from pathlib import Path
import runpy,copy,json
O=Path(__file__).resolve().parents[1];m=runpy.run_path(str(O/'producer/evidence_carrier.py'))
def fixture(phase):
 return {r:{'status':'PRESENT' if phase in m['RECORD_PHASES'][r] else 'INAPPLICABLE','instances':[{f:(b'SYNTHETIC:'+r.encode()+b':'+f.encode()) if m['applicable'](r,f,phase) else None for f in fs}] if phase in m['RECORD_PHASES'][r] else []} for r,fs in m['directory']().items()}
roundtrips=0;negatives=0
for phase in m['PHASES']:
 v=fixture(phase);raw=m['encode'](phase,v);assert m['decode'](raw)==(phase,v);roundtrips+=1
 assert m['acquisition_status'](phase,v)['protocol_permission'] is False
 # Every truncation must fail; framing cannot accept a plausible prefix as a package.
 for i in range(len(raw)):
  try:m['decode'](raw[:i])
  except m['FramingError']:negatives+=1
  else:raise AssertionError(('truncation accepted',phase,i))
 for altered in (raw+b'\x00',b'WRONG'+raw):
  try:m['decode'](altered)
  except m['FramingError']:negatives+=1
  else:raise AssertionError('bad envelope accepted')
 for r,record in v.items():
  bad=copy.deepcopy(v)
  if record['status']=='PRESENT':
   bad[r]={'status':'UNAVAILABLE','instances':[]};assert m['decode'](m['encode'](phase,bad))==(phase,bad)
   assert r in m['acquisition_status'](phase,bad)['unavailable_records'];roundtrips+=1
   bad=copy.deepcopy(v);bad[r]['instances'][0]['UNDECLARED']=b'x'
  else:bad[r]={'status':'PRESENT','instances':[]}
  try:m['encode'](phase,bad)
  except m['FramingError']:negatives+=1
  else:raise AssertionError('bad directory/applicability accepted')
# Absence is distinct from present empty bytes; empty remains subject to owning semantics.
v=fixture('E');assert v['phase-view']['instances'][0]['U'] is None
v['phase-view']['instances'][0]['E']=b''
assert m['decode'](m['encode']('E',v))[1]['phase-view']['instances'][0]['E']==b''
for phase,field in [('E','U'),('PRE-EXECUTION','E'),('PRE-COMMITMENT','C')]:
 bad=fixture(phase);bad['phase-view']['instances'][0][field]=b'fake'
 try:m['encode'](phase,bad)
 except m['FramingError']:negatives+=1
 else:raise AssertionError('inapplicable field accepted')
# Large declared counts cannot force unbounded loops.
raw=m['encode']('STATIC',fixture('STATIC'));n=len(m['MAGIC'])+8+len('STATIC')
bad=raw[:n]+b'\xff'*8+raw[n+8:]
try:m['decode'](bad)
except m['FramingError']:negatives+=1
else:raise AssertionError('bad count accepted')
report={'status':'PASS-FRAMING-ONLY','roundtrip_cases':roundtrips,'malformed_cases':negatives,'phases':list(m['PHASES']),'source_witness_parser_implemented':False,'owning_semantics_validated':False,'source_appointed':False,'protocol_permission':False}
(O/'verification/evidence-carrier.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS — phase-specific V2 evidence framing; explicit unavailable/inapplicable states and malformed input rejection.')
