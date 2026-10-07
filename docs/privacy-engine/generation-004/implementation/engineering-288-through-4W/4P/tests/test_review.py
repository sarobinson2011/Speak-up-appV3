import copy,json,unittest
from fixtures.construct import dataset,wire,sha,tsv,EVIDENCE_HEADER
from admission_kernel.admission import collect
from admission_kernel.sources import FiniteLabProvider
from admission_kernel.observations import observe
from admission_kernel.failures import Failures
from v4_ingest.wire import read_table,object_digest,signature_preimage
from v4_ingest.records import ValidationError
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from tests.test_admission import evidence,set_evidence,profile


def provider(q,t):return FiniteLabProvider(t,{k:bytes.fromhex(v) for k,v in q['materials'].items()},{k:bytes.fromhex(v) for k,v in q['source_objects'].items()})
def node(n,c,v):return dict(id=n,context=c,exposure='PUBLIC',reuse='NONE',value_hex=v,role='NOT-APPLICABLE',source_domain='LAB',action_hex='')
class ReviewTests(unittest.TestCase):
 def test_signed_occurrence_cannot_replace_static_evidence(self):
  q,t=dataset()
  # Independent known fixture signing seed; valid signature, wrong phase.
  key=Ed25519PrivateKey.from_private_bytes(sha(b'PUBLIC CP3 UNIT FIXTURE KEY GAMMA').encode()[:32])
  for scope,b in q['bundles'].items():
   files={k:bytes.fromhex(v) for k,v in b['files'].items()}; r=read_table(files['evidence.tsv'],EVIDENCE_HEADER)[0]
   r['evidence_kind']=r['evidence_kind'].replace('ADMISSION-','');r['scope_id']=r['profile_id']+'#OCCURRENCE-SET-'+sha(files['tokens.tsv']);r['evidence_id']=r['profile_id']+'#'+r['evidence_kind']+'-'+('ALL' if scope=='NOT-APPLICABLE' else scope)
   files['evidence.tsv']=tsv(EVIDENCE_HEADER,[[r[k] for k in EVIDENCE_HEADER]])
   files['signature.txt']=(t['appointment']['authority_id']+' '+key.sign(signature_preimage(files)).hex()+'\n').encode()
   b.update(files={k:v.hex() for k,v in files.items()},object_sha256=object_digest(files))
  r=collect(q,t);self.assertIn('INVALID-ACTION-CONTEXT',r['failures']);self.assertNotIn('INVALID-EVIDENCE-AUTHENTICATION',r['failures'])
 def test_nested_construction_final_result_is_rejected(self):
  q,t=dataset();p=provider(q,t);raw=wire({'format':'CP3-LAB-MATERIAL-V1','payload':{'nested':[{'requires_admission_result':True}]},'dependencies':[]});p.materials[sha(raw)]=raw
  with self.assertRaises(ValidationError):p.construction([{'material_sha256':sha(raw)}])
 def test_transitive_missing_material_is_not_ignored_in_invocation(self):
  q,t=dataset();p=provider(q,t);sec=profile(q)['security_contract'];arg=evidence(q)['records']['ARGUMENT']['instances'][0]
  ref=sec['policy']['record']['policy_source'];obj=json.loads(p.raw(ref));obj['dependencies']=['f'*64];raw=wire(obj);ref['material_sha256']=sha(raw);p.materials[sha(raw)]=raw;t['anchors'][ref['source_anchor']]=sha(raw)
  from admission_kernel.sources import MissingMaterial
  with self.assertRaises(MissingMaterial):p.invocation(arg,sec,sha(wire(t['model'])))
 def test_unbound_exact_violation_is_not_known_counterexample(self):
  q,t=dataset();e=evidence(q);o=next(x for x in e['records']['OBLIGATION']['instances'] if x['kind']=='EXACT');ref=o['exact_evidence_refs'][0]
  raw=wire({'format':'CP3-LAB-MATERIAL-V1','payload':{'obligation_id':'WRONG','model_digest':'0'*64,'result':'EXACT-VIOLATION'},'dependencies':[]});q['materials'][sha(raw)]=raw.hex();ref['material_sha256']=sha(raw);t['anchors'][ref['source_anchor']]=sha(raw);set_evidence(q,e)
  r=collect(q,t);self.assertNotIn('ACTOR-RECONSTRUCTION-RISK',r['failures']);self.assertIn('INCOMPLETE-EVIDENCE-UNIVERSE',r['failures'])
 def test_visible_structural_path_is_correlation_without_equal_bytes(self):
  d={'nodes':[node('A','ONE','01'),node('B','TWO','02')],'edges':[['A','B','SOURCE']],'visibility':{'A':'VISIBLE','B':'VISIBLE'}}
  f=Failures();observe(d,f)
  # Missing edge visibility must not silently clear complete view.
  self.assertIn('INCOMPLETE-EVIDENCE-UNIVERSE',f.reasons)
 def test_public_cannot_be_hidden(self):
  f=Failures();observe({'nodes':[node('A','ONE','01')],'edges':[],'visibility':{'A':'HIDDEN'}},f);self.assertIn('INVALID-SURFACE-LABELS',f.reasons)
 def test_fake_nullifier_action_permission_rejected(self):
  from v4_ingest.typed import Codec
  ns=[dict(node(n,c,Codec().encode('PE-TSE-UINT',7).hex()),role='n',action_hex=Codec().encode('PE-TSE-UINT',9).hex()) for n,c in [('A','ONE'),('B','TWO')]]
  f=Failures();observe({'nodes':ns,'edges':[],'visibility':{'A':'VISIBLE','B':'VISIBLE'}},f)
  self.assertIn('INCOMPLETE-EVIDENCE-UNIVERSE',f.reasons);self.assertIn('UNIQUENESS-FAILURE',f.reasons)

class AdditionalReviewTests(unittest.TestCase):
 def test_explicit_visible_path_and_hidden_path(self):
  ns=[node('A','ONE','01'),node('B','TWO','02')]
  for state in ('VISIBLE','HIDDEN'):
   f=Failures();observe({'nodes':ns,'edges':[['A','B','SOURCE']],'visibility':{'A':'VISIBLE','B':'VISIBLE'},'edge_visibility':[state]},f)
   self.assertEqual('CORRELATION-FAILURE' in f.reasons,state=='VISIBLE')
 def test_unqualified_exact_assertion_not_disposition(self):
  q,t=dataset();del t['laboratory_assumptions']['model-ledger-classification'];r=collect(q,t)
  self.assertEqual(r['earliest_failure'],'INVALID-EVIDENCE-AUTHORITY');self.assertEqual(r['bindings']['computed_dispositions']['G-OB-EXACT'],'NOT-ESTABLISHED')

class ModelMetadataTests(unittest.TestCase):
 def test_exact_stream_descriptor_not_arbitrary_prose_or_digest(self):
  from admission_kernel.model import Model
  q,t=dataset()
  for key,value in [('format','OTHER'),('ordering','sampled'),('predicate','always false'),('row_encoding','text'),('sha256','not-a-digest')]:
   with self.subTest(field=key):
    m=copy.deepcopy(t['model']);m['equality_stream'][key]=value
    with self.assertRaises(ValidationError):Model(m)
