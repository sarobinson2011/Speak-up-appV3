"""Ephemeral cryptographic transport fixtures only; no authority or profile admitted."""
from pathlib import Path
import runpy,copy,hashlib,json
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat
O=Path(__file__).resolve().parents[2];M=runpy.run_path(str(Path(__file__).with_name('evidence_auth.py')))
# Ephemeral in-memory key: never written, appointed, or used for real candidate evidence.
key=Ed25519PrivateKey.generate();pub=key.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw)
a={'authority_id':'SYNTHETIC-TRANSPORT-TEST','algorithm':'ED25519-RFC8032','public_key':pub.hex(),'key_fingerprint_sha256':hashlib.sha256(pub).hexdigest(),'owner_source_id':'SYNTHETIC-TEST','owner_anchor':'NOT-AUTHORITY'}
def fixture(scope):
 expected={'evidence.tsv':('SYNTHETIC-EVIDENCE\n'+scope+'\n').encode(),'tokens.tsv':b'SYNTHETIC-TOKENS\n','links.tsv':b'SYNTHETIC-LINKS\n'}
 signed=b'PE-TSE-PRIVACY-EVIDENCE-V2\n'+b''.join(expected[k] for k in M['NAMES'][:-1]);files=dict(expected,**{'signature.txt':(a['authority_id']+' '+key.sign(signed).hex()+'\n').encode()})
 return expected,files,M['object_digest'](files)
expected,files,digest=fixture('ONE');assert M['authenticate'](a,a,files,digest,expected)['result']=='EXACT-EVIDENCE-BYTES-AUTHENTICATED'
assert M['authenticate'](a,a,files,digest,expected)['profile_admitted'] is False
cases=0
for args,want in [((a,None,files,digest,expected),'INVALID-EVIDENCE-AUTHORITY'),((a,{**a,'authority_id':'OTHER'},files,digest,expected),'INVALID-EVIDENCE-AUTHORITY'),((a,a,{},digest,expected),'MISSING-EVIDENCE'),((a,a,files,'00'*32,expected),'INVALID-EVIDENCE-DIGEST'),((a,a,files,digest,{}),'INCOMPLETE-EVIDENCE-UNIVERSE')]:
 assert M['authenticate'](*args)['failure']==want;cases+=1
for field in M['NAMES']:
 bad=copy.deepcopy(files);bad[field]+=b'X';assert M['authenticate'](a,a,bad,M['object_digest'](bad),expected)['failure']=='INVALID-EVIDENCE-AUTHENTICATION';cases+=1
for field in M['NAMES'][:-1]:
 bad=dict(expected);bad[field]+=b'OTHER';assert M['authenticate'](a,a,files,digest,bad)['failure']=='INCOMPLETE-EVIDENCE-UNIVERSE';cases+=1
objs={};expect={}
for scope in ('ROOT-ELIGIBLE','SCOPED-USED','NOT-APPLICABLE'):
 e,f,d=fixture(scope);objs[scope]={'files':f,'object_sha256':d};expect[scope]=e
assert M['authenticate_bundle'](a,a,objs,expect)['result']=='BUNDLE-AUTHENTICATED'
for scope in objs:
 bad=dict(objs);del bad[scope];assert M['authenticate_bundle'](a,a,bad,expect)['result']=='FAIL';cases+=1
bad=dict(objs);bad['ROOT-ELIGIBLE']=objs['SCOPED-USED'];assert M['authenticate_bundle'](a,a,bad,expect)['result']=='FAIL';cases+=1
report={'author_checks':'PASS','negative_cases':cases,'signature_preimage':'PE-TSE-PRIVACY-EVIDENCE-V2','object_preimage':'PE-TSE-PRIVACY-EVIDENCE-OBJECT-V2','synthetic_transport_only':True,'test_keys_or_signed_fixtures_saved':False,'real_appointment_created':False,'profile_admitted':False}
(O/'verification/evidence-authentication.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS — V2 evidence signatures, object digests and three-scope bundle binding; '+str(cases)+' negative cases rejected.')
