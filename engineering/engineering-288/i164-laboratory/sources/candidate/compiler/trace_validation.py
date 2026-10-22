"""Pinned laboratory capture validation, not operational attestation or path completeness."""
import json,hashlib,ast
from pathlib import Path
import value_flow as vf
CATALOGUE_SHA256='ce77053799e2a0cc9d823d2e77fd4625e5c37e525bac66b63a40f5e17de795d8'
def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def literal():
 return ast.literal_eval(next(n.value for n in ast.parse(Path(__file__).read_bytes()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CATALOGUE_SHA256' for t in n.targets)))
def validate(record,root,context):
 root=Path(root);base=root/'reachability_outputs';raw=(base/'execution/INDEX.json').read_bytes()
 if sha(raw)!=literal():raise ValueError('CAPTURE-CATALOGUE-IDENTITY')
 items=json.loads(raw);item=next((i for i in items if i['name']==record.get('name')),None)
 b=enc(record)
 if not item or len(b)!=item['bytes'] or sha(b)!=item['sha256']:raise ValueError('CAPTURE-CURRENT-BYTES')
 # The hash catalogue is a pinned engineering capture, not a signature by an independent witness.
 for name,h in record['source_hashes'].items():
  if sha((root/name).read_bytes())!=h:raise ValueError('CAPTURE-SOURCE')
 source=(root/record['input_fixture']).read_bytes();identity=record['input_identity']
 if len(source)!=identity['bytes'] or sha(source)!=identity['sha256'] or json.loads(source)!=record['input']:raise ValueError('CAPTURE-INPUT')
 c=vf.s.setup(root)
 if context not in c.contexts:raise ValueError('CONTEXT')
 import ingest
 ingest.validate_export(record['input']);ingest.validate_export(record['export'])
 before=json.loads(bytes.fromhex(record['input']['head']));after=json.loads(bytes.fromhex(record['export']['head']))
 if enc(before)!=enc(record['before']) or enc(after)!=enc(record['after']):raise ValueError('CAPTURE-HEAD')
 q=json.loads(bytes.fromhex(record['request_hex']))['request']
 if q['expected']!=before['head']:raise ValueError('REQUEST-ANCESTRY')
 row=next((r for r in record['export']['journal'] if r[0]==q['challenge']),None)
 if row!=[q['challenge'],record['request_hex'],record['response_hex']]:raise ValueError('RESPONSE-ASSOCIATION')
 if any(after['counts'][k]<before['counts'][k] for k in before['counts']):raise ValueError('CHARGE-RESET')
 obligations=vf.obligations(record['export'])
 return {'format':'I164-BOUNDED-REACH-RECEIPT-1','capture_sha256':sha(b),'catalogue_sha256':literal(),'context':context,'candidate':c.binding,'before':before['head'],'after':after['head'],'request':sha(bytes.fromhex(record['request_hex'])),'obligations':obligations,'static_path_completeness':False,'execution_attestation':'PINNED-ENGINEERING-LAB-CAPTURE; TRUSTED-HARNESS-ASSUMPTION','final_binding':'BLOCKED','actual_admission':False,'stream_identities':'UNCOMPUTED','backup':'KERNEL-ONLY'}
def validate_receipt(receipt,record,root,context):
 if enc(receipt)!=enc(validate(record,root,context)):raise ValueError('REACH-RECEIPT-MISMATCH')
 return True
