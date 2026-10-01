from pathlib import Path
import runpy,hashlib,json,copy,csv,contextlib,io
O=Path(__file__).resolve().parents[2]
K=runpy.run_path(str(Path(__file__).with_name('proof_kernel.py')))
M=runpy.run_path(str(O/'profile/integration/relation_member.py'))
with contextlib.redirect_stdout(io.StringIO()):d=M['declaration']()
b=d['relation_policy']['bindings'];proof=d['relation_policy']['conditional_proof']
r=K['derive'](proof,b);assert r['result']=='VALID-CONDITIONAL-DERIVATION' and r['security_established'] is False and r['profile_admitted'] is False
bad=[]
def case(name,edit):
 p=copy.deepcopy(proof);edit(p)
 try:K['derive'](p,b)
 except (ValueError,TypeError,KeyError):bad.append(name)
 else:raise AssertionError(name)
case('changed source binding',lambda p:p['binding'].__setitem__('sources/PE-G4-SOURCE-S89.md','00'*32))
case('extra completion flag',lambda p:p.__setitem__('complete',True))
case('unknown premise',lambda p:p['steps'][0].__setitem__('name','POSEIDON-SECURE'))
case('unsupported security rule',lambda p:p['steps'][5].__setitem__('rule','ASSUME-UNLINKABILITY'))
case('self reference',lambda p:p['steps'][4].__setitem__('refs',[4]))
case('forward reference',lambda p:p['steps'][4].__setitem__('refs',[5]))
case('negative reference',lambda p:p['steps'][4].__setitem__('refs',[-1]))
case('Boolean index',lambda p:p['steps'][4].__setitem__('refs',[False]))
case('missing relation',lambda p:p['steps'][5].__setitem__('refs',[4,0,2,3]))
case('wrong output premise',lambda p:p['steps'][5].__setitem__('refs',[4,1,2,0]))
case('swapped premise',lambda p:p['steps'][5].__setitem__('refs',[4,2,1,3]))
case('extra proof step',lambda p:p['steps'].append({'rule':'PREMISE','name':'output-equal'}))
case('short proof',lambda p:p['steps'].pop())
case('wrong final conclusion',lambda p:p['steps'].__setitem__(5,{'rule':'PREMISE','name':'output-equal'}))
assert d['format']=='PE-G4-PRIVACY-PROFILE-V3' and d['format_source']=='PE-G4-SOURCE-S89'
assert d['model']==M['P']['declaration']()['model']
assert d['relation_policy']['obligations']['full_graph']['removed_edges']==0
# No production authority exists. Synthetic shape-only authority never leaves memory.
key='00'*32
appointment={'authority_id':'SYNTHETIC-TEST-ONLY','algorithm':'ED25519-RFC8032','public_key':key,'key_fingerprint_sha256':hashlib.sha256(bytes.fromhex(key)).hexdigest(),'owner_source_id':'SYNTHETIC-TEST-ONLY','owner_anchor':'TEST'}
with contextlib.redirect_stdout(io.StringIO()):
 raw=M['construct_outer'](appointment,appointment)
 result=M['validate_serialization'](raw,appointment,appointment)
assert result['profile_admitted'] is False
members=M['P']['A']['decode_container'](raw)
assert json.loads(members['PRIVACY'])['format']=='PE-G4-PRIVACY-PROFILE-V3'
try:M['member'](None,None)
except ValueError:bad.append('missing appointment')
else:raise AssertionError('missing appointment')
# Mutating any bound policy or model byte cannot produce the canonical member.
q=json.loads(members['PRIVACY']);q['relation_policy']['security_claim']='SECURE'
mutated=M['P']['A']['encode_container']({**members,'PRIVACY':M['P']['A']['canonical'](q)})
with contextlib.redirect_stdout(io.StringIO()):
 try:M['validate_serialization'](mutated,appointment,appointment)
 except ValueError:bad.append('fabricated security claim')
 else:raise AssertionError('fabricated security claim')
source=(O/'sources/PE-G4-SOURCE-S89.md').read_text()
for f in ('privacy/relation-aware/proof_kernel.py','profile/integration/relation_member.py'):assert (O/f).read_text() in source
req=json.loads((O/'composition/requirement-inventory.json').read_text());assert [x['requirement_id'] for x in req[951:959]]==[f'PE-G4-CAP-{i:03}' for i in range(91,99)]
report={'source_integration':'PASS-S89-V3-CANDIDATE','conditional_proof':r,'rejected_cases':bad,'full_graph_unchanged':True,'synthetic_outer_written':False,'general_security_argument_validator':'NOT-IMPLEMENTED','acceptance_path':'NOT-COMPLETE','profile_admitted':False}
(O/'verification/relation-source-integration.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS — S89 source and V3 member integration; conditional proof checked; '+str(len(bad))+' malformed/mismatched cases rejected.')
print('BOUNDARY — conditional proof is not a security argument; production acceptance remains unfinished.')

A=runpy.run_path(str(O/'profile/integration/relation_admission.py'))
r=A['evaluate']({})
assert r['candidate_format']=='PE-G4-PRIVACY-PROFILE-V3' and r['profile_admitted'] is False
assert 'CRYPTOGRAPHIC-ARGUMENT-VALIDATOR' in r['unfinished_integration']
print('PASS — V3 rejection entrypoint regenerates the new source-bound model; no acceptance enabled.')
