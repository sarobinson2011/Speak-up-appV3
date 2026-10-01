"""S89 V3 candidate declaration; exact construction, never privacy admission."""
from pathlib import Path
import runpy,hashlib,json
O=Path(__file__).resolve().parents[2]
P=runpy.run_path(str(Path(__file__).with_name('privacy_member.py')))
K=runpy.run_path(str(O/'privacy/relation-aware/proof_kernel.py'))
FILES=['sources/PE-G4-SOURCE-S89.md','privacy/relation-aware/rule.md','privacy/relation-aware/construct.py','privacy/relation-aware/proof_kernel.py','profile/integration/relation_member.py','profile/integration/relation_admission.py']
def declaration():
 # Refresh all graph declarations and full streamed equality binding locally.
 X=runpy.run_path(str(O/'privacy/expand_privacy.py'));X['expand']()
 base=P['declaration']()
 binding={p:hashlib.sha256((O/p).read_bytes()).hexdigest() for p in FILES+['sources/retained/S22.md','privacy/expanded/PRIVACY.candidate.json']}
 proof=K['certificate'](binding);checked=K['derive'](proof,binding)
 obligations=runpy.run_path(str(O/'privacy/relation-aware/construct.py'))['construct']()
 # Diagnostic implementation status is not an immutable governing fact.
 policy_obligations={k:obligations[k] for k in ('full_graph','pair','branches','all_other_pairs','established_cross_action_equality','unknown_visibility','actor_graph')}
 return {**base,'format':'PE-G4-PRIVACY-PROFILE-V3','format_source':'PE-G4-SOURCE-S89','format_source_sha256':binding['sources/PE-G4-SOURCE-S89.md'],'policy_sources':base['policy_sources']+['PE-G4-SOURCE-S89'],'procedures_sha256':{**base['procedures_sha256'],**binding},'relation_policy':{'bindings':binding,'conditional_proof':proof,'conclusion':checked['conclusion'],'premises':checked['assumptions'],'obligations':policy_obligations,'security_claim':'NONE-ESTABLISHED-BY-SERIALIZATION'}}
def member(appointment,trusted):
 P['appointment_shape'](appointment);P['appointment_shape'](trusted)
 if appointment!=trusted:raise ValueError('INVALID-EVIDENCE-AUTHORITY')
 return P['A']['canonical']({**declaration(),'appointment':appointment})
def construct_outer(appointment,trusted):
 privacy=member(appointment,trusted);body,program=P['A']['member_bytes']()
 return P['A']['encode_container']({'SOURCE-OWNED-BODY':body,'EXPRESSION-PROGRAM':program,'PRIVACY':privacy})
def validate_serialization(raw,appointment,trusted):
 decoded=P['A']['decode_container'](raw)
 if raw!=construct_outer(appointment,trusted):raise ValueError('PROFILE-DIGEST-MISMATCH')
 return {'serialization':'EXACT-V3','profile_admitted':False,'security_established':False}
