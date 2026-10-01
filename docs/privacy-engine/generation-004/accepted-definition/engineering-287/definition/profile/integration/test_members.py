from pathlib import Path
import runpy,json,hashlib,copy
O=Path(__file__).resolve().parents[2]
A=runpy.run_path(str(Path(__file__).with_name('assemble_members.py')));P=runpy.run_path(str(Path(__file__).with_name('privacy_member.py')))
report=A['write_or_verify']();body,program=A['member_bytes']();j=json.loads(program)
assert A['parse']('and(arg(0001),not(arg(0002)))')==['and',['arg','0001'],['not',['arg','0002']]]
assert set(j)=={'types','definitions','components','fields','root_definition','root_fields','groups'}
assert len(j['types'])==22 and len(j['definitions'])==60 and len(j['components'])==2 and len(j['fields'])==118 and len(j['root_fields'])==94
assert body.endswith((O/'profile/fragments/recovery.tsv').read_bytes())
assert [d['id'] for d in j['definitions']]==[d['definition_id'] for d in A['rows']('definitions.tsv')]
assert all(d['expression']==A['parse'](r['expression']) for d,r in zip(j['definitions'],A['rows']('definitions.tsv')))
# Synthetic authority shape only, no private key/signing/appointment created.
fixture={'authority_id':'SYNTHETIC-TEST-ONLY','algorithm':'ED25519-RFC8032','public_key':'01'*32,'key_fingerprint_sha256':hashlib.sha256(bytes.fromhex('01'*32)).hexdigest(),'owner_source_id':'SYNTHETIC-TEST-SOURCE','owner_anchor':'TEST-ONLY'}
raw=P['construct_outer'](fixture,fixture)
assert P['validate_serialization'](raw,fixture,fixture)['profile_admitted'] is False
assert list(A['decode_container'](raw))==['SOURCE-OWNED-BODY','EXPRESSION-PROGRAM','PRIVACY']
failures=0
for app,trusted in [(None,None),(fixture,None),({},{}),(fixture,{**fixture,'authority_id':'OTHER'}),(dict(fixture,public_key='00'),fixture),(dict(fixture,key_fingerprint_sha256='00'*32),fixture)]:
 try:P['construct_outer'](app,trusted)
 except ValueError:failures+=1
 else:raise AssertionError('invalid appointment accepted')
for bad in [b'',raw[:-1],raw+b'\n',b'INVALID'+raw,raw.replace(b'SOURCE-OWNED-BODY',b'SOURCE-OWNED-BODZ',1)]:
 try:A['decode_container'](bad)
 except ValueError:failures+=1
 else:raise AssertionError('malformed container accepted')
# Preserve shape but alter bytes in each of the three members.
for name in A['decode_container'](raw):
 members=A['decode_container'](raw);members[name]+=b'X';bad=A['encode_container'](members)
 try:P['validate_serialization'](bad,fixture,fixture)
 except ValueError:failures+=1
 else:raise AssertionError('member mutation accepted')
# The older integration candidate cannot be passed off as the new governing member.
wrong=A['encode_container']({'SOURCE-OWNED-BODY':body,'EXPRESSION-PROGRAM':program,'PRIVACY':(O/'privacy/expanded/PRIVACY.candidate.json').read_bytes()})
try:P['validate_serialization'](wrong,fixture,fixture)
except ValueError:failures+=1
else:raise AssertionError('old integration candidate accepted as governing member')
# Synthetic full-profile bytes/digest are intentionally not written or used in mapping.
report.update(negative_vectors=failures,synthetic_container_roundtrip=True,governing_privacy_serializer_constructed=True,production_appointment_available=False,production_outer_profile_created=False,profile_admitted=False)
(O/'verification/profile-integration.json').write_bytes(A['canonical'](report))
print('PASS — exact source-body/program members and S88 PRIVACY/container serialization constructed.')
print('PASS — '+str(failures)+' malformed/mismatched integration cases rejected; no synthetic profile materialized.')
print('BOUNDARY — real appointed authority, complete source/observer evidence and integrated admission validation remain open.')
