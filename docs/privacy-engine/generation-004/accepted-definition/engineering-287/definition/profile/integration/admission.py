"""Fresh integrated static admission rejection/preflight over current G4 declarations.
No acceptance path is enabled while symbolic-policy evidence integration is incomplete.
This is explicit: negative gate integration is not a complete admission validator.
"""
from pathlib import Path
import runpy,json,hashlib,contextlib,io
O=Path(__file__).resolve().parents[2]
P=runpy.run_path(str(Path(__file__).with_name('privacy_member.py')))
E=runpy.run_path(str(Path(__file__).with_name('evidence_auth.py')))
G=runpy.run_path(str(O/'privacy/cross_role_uniqueness.py'))
ORDER=G['C']['BASE']['ORDER']
SCOPE={'ROOT-ELIGIBLE','SCOPED-USED','NOT-APPLICABLE'}
def canonical(v):return P['A']['canonical'](v)
def regenerate():
 # Every program/type/source declaration is rechecked, then all static tokens,
 # owning component relations and equality pairs are independently regenerated.
 with contextlib.redirect_stdout(io.StringIO()):
  runpy.run_path(str(O/'verify-candidate.py'))
  X=runpy.run_path(str(O/'privacy/expand_privacy.py'));X['expand']()
 return P['declaration']()
def collect(request,model):
 """Pure ordered rejection collector. model is internal regeneration output, never a request field."""
 failures=set();checks={};open_work=['SYMBOLIC-POLICY-EVIDENCE-INTEGRATION']
 if not isinstance(request,dict):return decision({'INVALID-PROFILE-SCHEMA'},checks,open_work)
 allowed={'outer_bytes','outer_sha256','appointment','trusted_appointment','evidence_objects'}
 if set(request)-allowed:failures.add('INVALID-PROFILE-SCHEMA')
 appointment=request.get('appointment');trusted=request.get('trusted_appointment')
 try:
  P['appointment_shape'](appointment);P['appointment_shape'](trusted)
  if appointment!=trusted:raise ValueError('authority mismatch')
  checks['appointment_shape_and_external_equality']='PASS-NOT-SOURCE-AUTHORITY-PROOF'
 except (ValueError,TypeError):failures.add('INVALID-EVIDENCE-AUTHORITY')
 outer=request.get('outer_bytes');digest=request.get('outer_sha256')
 if not isinstance(outer,bytes) or hashlib.sha256(outer).hexdigest()!=digest:failures.add('PROFILE-DIGEST-MISMATCH')
 if isinstance(outer,bytes):
  try:
   members=P['A']['decode_container'](outer);body,program=P['A']['member_bytes']()
   if members['SOURCE-OWNED-BODY']!=body or members['EXPRESSION-PROGRAM']!=program:failures.add('PROFILE-DIGEST-MISMATCH')
   submitted=json.loads(members['PRIVACY'])
   if canonical(submitted)!=members['PRIVACY']:failures.add('INVALID-PROFILE-SCHEMA')
   # All decision-bearing model fields are regenerated, not read back as trusted cache.
   expected={**model,'appointment':appointment}
   if submitted!=expected:failures.add('INVALID-PROFILE-SCHEMA')
  except (ValueError,TypeError,KeyError,UnicodeDecodeError):failures.add('INVALID-PROFILE-SCHEMA')
 surfaces=model.get('model',{}).get('surfaces',[])
 if not surfaces or any(s.get('declared_exposure') not in ('PUBLIC','CONFIDENTIAL','PRIVATE-ACTOR') for s in surfaces):failures.add('INVALID-SURFACE-LABELS')
 components=model.get('components',[])
 if len(components)!=2 or {c.get('id') for c in components}!={'ROOT-ELIGIBLE','SCOPED-USED'}:failures.add('COMPONENT-COUNT-MISMATCH')
 if any(c.get('necessity') not in ('PREDICATE-INPUT','AUTHORIZATION-BINDING','ORDERING-COORDINATE','DEPENDENCY-COORDINATE') for c in components):failures.add('UNNECESSARY-COMPONENT')
 if any(c.get('privacy')=='PRIVATE-ACTOR' for c in components):failures.add('PUBLIC-PRIVATE-VALUE')
 objects=request.get('evidence_objects')
 if not isinstance(objects,dict) or set(objects)!=SCOPE:failures.add('MISSING-EVIDENCE')
 # Authentication runs even when labels/contexts are incomplete. This prevents
 # later missing model facts from masking earlier bad authentication.
 if isinstance(objects,dict):
  for scope in sorted(SCOPE):
   item=objects.get(scope)
   if not isinstance(item,dict) or set(item)!={'files','object_sha256'}:
    failures.add('MISSING-EVIDENCE');continue
   # No self-selected expected bytes. None deliberately forces the remaining
   # independently regenerated universe gate to fail after authentication.
   r=E['authenticate'](appointment,trusted,item['files'],item['object_sha256'],None)
   failures.add(r['failure']);checks['evidence:'+scope]=r['failure']
 failures.discard('NONE')
 # Current declarations carry no authenticated complete observer/coalition
 # model and symbolic-to-policy binding universe. No caller booleans are accepted.
 failures.add('INCOMPLETE-EVIDENCE-UNIVERSE')
 return decision(failures,checks,open_work)
def decision(failures,checks,open_work):
 ordered=[c for c in ORDER if c in failures]
 return {'result':'REJECTED-INCOMPLETE','earliest_failure':ordered[0] if ordered else 'NONE','failures':ordered,'checked_gates':checks,'unfinished_integration':open_work,'profile_admitted':False,'production_profile_written':False}
def evaluate(request):
 try:model=regenerate()
 except Exception as error:
  return {**decision({'INVALID-PROFILE-SCHEMA'},{},['SYMBOLIC-POLICY-EVIDENCE-INTEGRATION']),'regeneration_error_type':type(error).__name__}
 return collect(request,model)
if __name__=='__main__':
 result=evaluate({})
 (O/'verification/admission-readiness.json').write_bytes(canonical(result))
 print('PASS — integrated regeneration and ordered rejection gates executed.')
 print('BOUNDARY — '+result['earliest_failure']+'; acceptance remains disabled pending symbolic-policy evidence integration.')
