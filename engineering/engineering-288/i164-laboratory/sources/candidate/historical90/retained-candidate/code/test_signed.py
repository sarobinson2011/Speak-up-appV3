import unittest,json,tempfile,copy
from pathlib import Path
import signed_eth,lab_evm,runtime,connected,stages
from carrier_fixture import Fixture
from anchor import enc,parse,MAX_INTENT,MAX_TRANSACTION,Uncertain
P=Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
 def setUp(self):
  self.pre=parse((P/'runs/2/records/prerequisites.json').read_bytes(),MAX_INTENT);self.i=parse((P/'runs/2/records/intent.json').read_bytes(),MAX_INTENT);self.raw=bytes.fromhex(self.i['signed_evm_hex']);d=signed_eth.decode(self.raw);self.expected={k:d[k] for k in signed_eth.FIELDS}
 def fixture(self,d):
  f=Fixture(d,self.pre);f.x.retire(f.u,self.i,'retire');meta=parse((P/'runs/2/records/meta.json').read_bytes(),MAX_INTENT);f.sch.open(f.u,(P/'runs/2/records/message.bin').read_bytes(),bytes.fromhex(meta['key']),bytes.fromhex(meta['signature']));return f
 def prepare(self,f,raw=None):
  full=json.loads((P/'runs/2/records/full.json').read_bytes());raw=raw or bytes.fromhex(full['cases'][0]['transactions'][14]['signed_transaction']);spec,near=f.near(raw,15);f.sch.prepare(f.u,spec,near,raw);return raw,near
 def test_exact_bytes_and_independent_signature_equation(self):
  from cryptography.hazmat.primitives.asymmetric import ec,utils
  from cryptography.hazmat.primitives import hashes
  a=signed_eth.decode_rlp(self.raw);v,r,s=[int.from_bytes(b,'big') for b in a[6:]];digest=lab_evm.keccak(lab_evm.rlp(a[:6]+[(v-35)//2,0,0]));pub=ec.derive_private_key(1,ec.SECP256K1()).public_key();pub.verify(utils.encode_dss_signature(r,s),digest,ec.ECDSA(utils.Prehashed(hashes.SHA256())))
  self.assertEqual(signed_eth.validate(self.raw,self.expected),signed_eth.decode(self.raw));self.assertEqual(bytes.fromhex(self.i['signed_evm_hex']),self.raw)
 def test_signed_wrong_fields(self):
  for field,value in [('nonce','99'),('gas_limit','20000000'),('gas_price','1'),('value','1'),('target','ab'*20),('calldata','abcd'),('signer','ab'*20),('chain','1')]:
   want=dict(self.expected);want[field]=value
   with self.assertRaises(ValueError):signed_eth.validate(self.raw,want)
  wrong=bytes.fromhex(lab_evm.tx(int(self.i['nonce']),self.i['registry'],bytes.fromhex(self.i['calldata_hex']),100000000,key=2))
  with self.assertRaises(ValueError):signed_eth.validate(wrong,self.expected)
 def test_validly_signed_wrong_intent(self):
  for nonce,target,data,gas in [(123,self.i['registry'],b'X',100000000),(int(self.i['nonce']),'ab'*20,bytes.fromhex(self.i['calldata_hex']),100000000),(int(self.i['nonce']),self.i['registry'],bytes.fromhex(self.i['calldata_hex']),10)]:
   raw=bytes.fromhex(lab_evm.tx(nonce,target,data,gas))
   with self.assertRaises(ValueError):signed_eth.validate(raw,self.expected)
 def test_malformed_and_unsupported(self):
  a=signed_eth.decode_rlp(self.raw)
  bad=[b'',b'\x02'+self.raw,self.raw+b'\0',self.raw[:-1],b'I164-LAB-STAGE-1\0',enc({'conditional_test_signature':'LAB-NOT-A-REAL-SIGNATURE'}),lab_evm.rlp(a[:8]),lab_evm.rlp(a+ [b'']),lab_evm.rlp([a]+a[1:]),lab_evm.rlp([b'\0']+a[1:])]
  for index,value in [(3,b''),(6,b'\x1b'),(6,(37).to_bytes(1,'big')),(7,b''),(8,lab_evm.N.to_bytes(32,'big')),(8,(lab_evm.N//2+1).to_bytes(32,'big'))]:
   x=copy.deepcopy(a);x[index]=value;bad.append(lab_evm.rlp(x))
  for raw in bad:
   with self.assertRaises(ValueError):signed_eth.validate(raw,self.expected)
 def test_mutation_retired(self):
  with tempfile.TemporaryDirectory() as d:
   f=self.fixture(d);before=f.s.fresh();self.i['signed_evm_hex']='00';f.x.recover();self.assertEqual(before,f.s.fresh())
   with self.assertRaises(ValueError):f.x.retire(f.u,self.i,'different')
   f.close()
 def test_normal_signed_stage_and_legacy_refusal(self):
  with tempfile.TemporaryDirectory() as d:
   f=self.fixture(d);full=json.loads((P/'runs/2/records/full.json').read_bytes());raw=bytes.fromhex(full['cases'][0]['transactions'][14]['signed_transaction']);spec,near=f.near(raw,15)
   with self.assertRaises(ValueError):f.sch.prepare(f.u,spec,near) # old carrier cannot silently change bytes
   self.prepare(f);f.sch.send(f.u,f.sink);self.assertEqual(f.sink.sent,[near]);f.close()
 def test_wrong_stage_signature(self):
  with tempfile.TemporaryDirectory() as d:
   f=self.fixture(d);raw=bytes.fromhex(lab_evm.tx(14,'11'*20,b'wrong',100000000))
   with self.assertRaises(ValueError):self.prepare(f,raw)
   self.assertEqual(f.s.fresh()['counts']['attempt'],0);f.close()
 def test_ack_loss_restart_no_second_release(self):
  with tempfile.TemporaryDirectory() as d:
   f=self.fixture(d);raw,near=self.prepare(f)
   def drop(q,r):
    if parse(q,600000)['request']['args'].get('kind')=='STAGE_ATTEMPT':raise OSError('lost acknowledgement')
    return r
   f.ch.filter=drop
   with self.assertRaises(Uncertain):f.sch.send(f.u,f.sink)
   self.assertFalse(f.sink.sent);counts=f.s.fresh()['counts'];f.close();f=Fixture(d,self.pre,False)
   f.sch.recover(f.u);f.sch.recover(f.u)
   with self.assertRaises(ValueError):f.sch.send(f.u,f.sink)
   self.assertEqual(counts,f.s.fresh()['counts']);self.assertFalse(f.sink.sent);f.close()
 def test_old_version_restart_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   f=self.fixture(d);f.close();pre=copy.deepcopy(self.pre);pre['ethereum_carrier']['version']='OLD'
   with self.assertRaises(ValueError):Fixture(d,pre,False)
 def test_exhaustion_and_retry_exact(self):
  with tempfile.TemporaryDirectory() as d:
   f=self.fixture(d);raw,near=self.prepare(f)
   with self.assertRaises(Uncertain):f.sch.send(f.u,f.sink,crash=True)
   f.sch.send(f.u,f.sink,retry=True);self.assertEqual(f.sink.sent,[near]);self.assertEqual(f.s.fresh()['counts']['attempt'],2)
   for _ in range(15):f.sch.send(f.u,f.sink,retry=True)
   before=f.s.fresh()['counts']
   with self.assertRaises(ValueError):f.sch.send(f.u,f.sink,retry=True)
   self.assertEqual(before,f.s.fresh()['counts']);self.assertTrue(all(x==near for x in f.sink.sent));f.close()
if __name__=='__main__':unittest.main(verbosity=2)
