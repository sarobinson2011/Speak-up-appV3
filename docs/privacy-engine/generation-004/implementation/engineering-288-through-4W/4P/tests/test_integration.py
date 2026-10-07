import unittest,io
from unittest.mock import patch
from fixtures.construct import dataset,sha,tsv,EVIDENCE_HEADER
from admission_kernel.admission import collect
from admission_kernel.model import Model
from v4_ingest.wire import LINK_HEADER,read_table,object_digest,signature_preimage
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

class IntegrationTests(unittest.TestCase):
 def test_admission_uses_byte_stream_without_link_list_parser(self):
  import v4_ingest.wire as wire
  original=wire.read_table
  def guarded(raw,header):
   self.assertNotEqual(header,LINK_HEADER);return original(raw,header)
  q,t=dataset()
  with patch.object(wire,'read_table',guarded),patch.object(Model,'validate_links',side_effect=AssertionError('legacy list path called')):
   r=collect(q,t)
  self.assertEqual(r['earliest_failure'],'NONE',r);self.assertFalse(r['profile_admitted'])
 def resign(self,q,t,mutate):
  key=Ed25519PrivateKey.from_private_bytes(sha(b'PUBLIC CP3 UNIT FIXTURE KEY GAMMA').encode()[:32])
  scope='ROOT-ELIGIBLE';b=q['bundles'][scope];files={k:bytes.fromhex(v) for k,v in b['files'].items()};files['links.tsv']=mutate(files['links.tsv']);e=read_table(files['evidence.tsv'],EVIDENCE_HEADER)[0];e['links_sha256']=sha(files['links.tsv']);files['evidence.tsv']=tsv(EVIDENCE_HEADER,[[e[k] for k in EVIDENCE_HEADER]]);files['signature.txt']=(t['appointment']['authority_id']+' '+key.sign(signature_preimage(files)).hex()+'\n').encode();b.update(files={k:v.hex() for k,v in files.items()},object_sha256=object_digest(files))
 def test_authenticated_malformed_frame_maps_to_schema(self):
  q,t=dataset();self.resign(q,t,lambda b:b[:-1]);r=collect(q,t);self.assertEqual(r['earliest_failure'],'INVALID-PROFILE-SCHEMA',r);self.assertNotIn('INVALID-EVIDENCE-AUTHENTICATION',r['failures'])
 def test_authenticated_missing_row_is_incomplete(self):
  q,t=dataset();self.resign(q,t,lambda b:b[:b.rfind(b'\n',0,-1)+1]);r=collect(q,t);self.assertIn('INCOMPLETE-EVIDENCE-UNIVERSE',r['failures']);self.assertNotIn('INVALID-EVIDENCE-AUTHENTICATION',r['failures'])
 def test_bad_signature_retained_with_later_stream_failure(self):
  from tests.test_admission import bad_signature
  q,t=dataset();self.resign(q,t,lambda b:b[:-1]);bad_signature(q);r=collect(q,t);self.assertIn('INVALID-EVIDENCE-AUTHENTICATION',r['failures']);self.assertEqual(r['earliest_failure'],'INVALID-PROFILE-SCHEMA')
