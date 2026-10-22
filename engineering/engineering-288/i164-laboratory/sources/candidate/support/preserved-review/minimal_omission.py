import sys,json,copy,hashlib
from pathlib import Path
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(exist_ok=True,parents=True);sys.path.insert(0,str(root/'code'))
from common import *
from correspondence import Fold
from ingest import validate_export
from static_ingest import ingest
import static_declarations as sd
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
base=parse((root/'fixtures/minimal-response.json').read_bytes(),200000000)
head=Fold(base['config'],parse(hexbytes(base['ownership_meta'])),{},{}).s
r=copy.deepcopy(parse(hexbytes(base['journal'][0][1]))['request']);r.update(method='head',principal='executor',expected=ZERO,body={},challenge=sha(b'one-source-head-omission-witness'))
def sig(role,value):return Ed25519PrivateKey.from_private_bytes(hashlib.sha256(('PUBLIC-LAB-ONLY-'+role).encode()).digest()).sign(VERSION.encode()+b'\0'+enc(value)).hex()
p={'request':r,'signature':sig('executor',r)};res={'request':sha(enc(p)),'challenge':r['challenge'],'ok':True,'data':head};env={'response':res,'signature':sig('server',res)}
x=dict(base,head=enc(head).hex(),expected_head=ZERO,events=[],blobs=[],owners=[],journal=[[r['challenge'],enc(p).hex(),enc(env).hex()]])
raw=enc(x);(out/'SD-01-minimal.json').write_bytes(raw);validate_export(x);original=ingest(x,sd.build());assert len(original['response_selector_coverage'])==5
saved=sd.schemas
def omit():
 g,o,p=saved();del g['SUCCESS-RESPONSE']['data']['request_method_choice']['head'];return g,o,p
sd.schemas=omit
try:
 b=sd.build();sd.validate(b)
 try:ingest(x,b)
 except Invalid as e:assert str(e)=='REQUEST-METHOD-CONTEXT';failure=str(e)
 else:raise AssertionError('Expected omitted head branch rejection')
finally:sd.schemas=saved
result={'fixture_bytes':len(raw),'fixture_sha256':sha(raw),'events':0,'blobs':0,'owners':0,'journal_requests':1,'signed_responses':1,'unmodified_ingestion':'ACCEPTED','omitted_branch_build_and_validate':'ACCEPTED','omitted_branch_ingestion':failure,'candidate_source_modified':False}
(out/'SD-01-minimal-result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
