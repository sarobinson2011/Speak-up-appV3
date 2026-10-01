"""Fresh exact V2 four-file evidence authentication. Not source appointment/admission.
Expected bytes must come from independent governing model regeneration, never issuer caches.
"""
from pathlib import Path
import runpy,hashlib,re
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
P=runpy.run_path(str(Path(__file__).with_name('privacy_member.py')))
NAMES=('evidence.tsv','tokens.tsv','links.tsv','signature.txt')
def h(b):return hashlib.sha256(b).hexdigest()
def object_digest(files):return h(b'PE-TSE-PRIVACY-EVIDENCE-OBJECT-V2\n'+b''.join(len(files[n]).to_bytes(8,'big')+files[n] for n in NAMES))
def authenticate(appointment,trusted,files,digest,expected):
 """expected exact evidence/tokens/links bytes include scope, profile and computed results."""
 def fail(code):return {'result':'FAIL','failure':code,'source_authority_established':False,'profile_admitted':False}
 try:
  P['appointment_shape'](appointment);P['appointment_shape'](trusted)
  if appointment!=trusted:raise ValueError('appointment mismatch')
 except (ValueError,TypeError):return fail('INVALID-EVIDENCE-AUTHORITY')
 if not isinstance(files,dict) or set(files)!=set(NAMES) or not all(isinstance(x,bytes) for x in files.values()):return fail('MISSING-EVIDENCE')
 try:
  sig=files['signature.txt'].decode('ascii')
  prefix=trusted['authority_id']+' '
  if not sig.startswith(prefix) or not re.fullmatch('[0-9a-f]{128}\n',sig[len(prefix):]):raise ValueError('signature grammar')
  payload=b'PE-TSE-PRIVACY-EVIDENCE-V2\n'+files['evidence.tsv']+files['tokens.tsv']+files['links.tsv']
  Ed25519PublicKey.from_public_bytes(bytes.fromhex(trusted['public_key'])).verify(bytes.fromhex(sig[len(prefix):-1]),payload)
 except Exception:return fail('INVALID-EVIDENCE-AUTHENTICATION')
 if object_digest(files)!=digest:return fail('INVALID-EVIDENCE-DIGEST')
 if not isinstance(expected,dict) or set(expected)!=set(NAMES[:-1]) or any(not isinstance(v,bytes) for v in expected.values()):return fail('INCOMPLETE-EVIDENCE-UNIVERSE')
 if any(files[k]!=expected[k] for k in NAMES[:-1]):return fail('INCOMPLETE-EVIDENCE-UNIVERSE')
 return {'result':'EXACT-EVIDENCE-BYTES-AUTHENTICATED','failure':'NONE','source_authority_established':False,'profile_admitted':False}
def authenticate_bundle(appointment,trusted,objects,expected_by_scope):
 scopes={'ROOT-ELIGIBLE','SCOPED-USED','NOT-APPLICABLE'}
 if not isinstance(objects,dict) or set(objects)!=scopes or not isinstance(expected_by_scope,dict) or set(expected_by_scope)!=scopes:return {'result':'FAIL','failure':'MISSING-EVIDENCE','profile_admitted':False}
 result={}
 for scope in sorted(scopes):
  item=objects[scope]
  if not isinstance(item,dict) or set(item)!={'files','object_sha256'}:return {'result':'FAIL','failure':'MISSING-EVIDENCE','profile_admitted':False}
  result[scope]=authenticate(appointment,trusted,item['files'],item['object_sha256'],expected_by_scope[scope])
 return {'result':'BUNDLE-AUTHENTICATED' if all(r['failure']=='NONE' for r in result.values()) else 'FAIL','scopes':result,'profile_admitted':False}
