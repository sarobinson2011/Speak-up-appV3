"""Source-owned parser directory for exact retained executor formats.
No journal asserts source truth, qualification, finality or actual admission.
"""
from common import *
SOURCE='kernel/candidate/executor/session.py'
# Unions retain presence/status fields; a missing branch field is inapplicable only
# under the exact lifecycle variant below, never as an evidence default.
SCHEMAS={
 'META':('version','code','job'),
 'LOG':('seq','payload','digest'),
 'PAYLOAD':('previous','u','record'),
 'RECORD':('status','intent_ref','tx_ref','comparison_ref','reconciliation_ref'),
 'BLOB':('digest','payload'),
 'INTENT':tuple('chain registry executor nonce calldata_hex value gas_limit config decision source model contract profile scope key_epoch method arguments'.split()),
 'TRANSACTION':('conditional_test_signature','intent','u'),
 'RECONCILIATION':('conditional_fixture','tx_sha256','intent_sha256','outcome','finality','source'),
 'REJECTION':('u','intent_sha256','permit','comparison','static_failures','outer_component_join','outer_body_join','outer_program_join','conditional_test_requested','reason'),
 'STATUS':('head','states','actual_admission','conditional_only'),
 'STATE-ENTRY':('u','status','intent_sha256'),
 'BACKUP':('sha256','head','job','restore_requires_latest_external_head','antirollback_established'),
 'CAPSULE':('format','context','static_result_sha256','comparison_sha256','source_carrier_sha256','source_trust_sha256','permit_for_conditional_test','conditional_only','actual_admission'),
}
VARIANTS={'RETIRED':('status','intent_ref'),'SEALED':('status','intent_ref','tx_ref'),'UNCERTAIN':('status','intent_ref','tx_ref'),'REJECTED':('status','intent_ref','comparison_ref'),'SUCCESS':('status','intent_ref','tx_ref','reconciliation_ref'),'FAILED':('status','intent_ref','tx_ref','reconciliation_ref')}
ALLOWED={None:('RETIRED',),'RETIRED':('SEALED','REJECTED'),'SEALED':('UNCERTAIN',),'UNCERTAIN':('SUCCESS','FAILED')}
def validate_history(entries,blobs,job):
 need(type(job)is str and 0<len(job)<=128,'job binding')
 import sys
 sys.path.insert(0,str(ROOT/'retained/kernel/candidate/executor'))
 import session as executor
 prev='0'*64;states={};intents={};transactions={};nonces=set()
 for i,row in enumerate(entries,1):
  need(set(row)==set(SCHEMAS['LOG']) and row['seq']==i and i<=256,'log ordinal/limit')
  raw=bytes.fromhex(row['payload']);need(len(raw)<=8192 and digest(raw)==row['digest'],'log exact bytes')
  p=json.loads(raw);need(wire(p)==raw and set(p)==set(SCHEMAS['PAYLOAD']) and p['previous']==prev,'canonical history link')
  u,r=p['u'],p['record'];need(r.get('status') in VARIANTS and set(r)==set(VARIANTS[r['status']]),'record variant')
  old=states.get(u);need(r['status'] in ALLOWED.get(old['status'] if old else None,()),'retired-U lifecycle')
  if old:need(old['intent_ref']==r['intent_ref'] and ('tx_ref' not in old or old['tx_ref']==r['tx_ref']),'immutable intent/tx')
  for k in set(r)-{'status'}:
   need(r[k] in blobs and digest(blobs[r[k]])==r[k],'missing/corrupt owning blob')
  if u not in intents:
   intents[u],transactions[u]=executor.validate_intent(u,blobs[r['intent_ref']])
   i=intents[u];nonce=(i['chain'],i['executor'],i['nonce']);need(nonce not in nonces,'nonce already reserved');nonces.add(nonce)
  if 'tx_ref' in r:need(blobs[r['tx_ref']]==transactions[u],'exact submission bytes')
  if 'comparison_ref' in r:
   rejection=executor.parse(blobs[r['comparison_ref']]);need(rejection['u']==u and rejection['intent_sha256']==r['intent_ref'] and rejection['permit'] is False,'rejection correspondence')
  if 'reconciliation_ref' in r:
   e=executor.parse(blobs[r['reconciliation_ref']],executor.MAX_RECONCILIATION)
   need(set(e)==set(SCHEMAS['RECONCILIATION']) and e['conditional_fixture'] is True and e['tx_sha256']==r['tx_ref'] and e['intent_sha256']==r['intent_ref'] and e['finality']=='LAB-FINAL' and e['source']=='LAB-ORACLE' and e['outcome'] in ('SUCCESS','REVERTED') and {'SUCCESS':'SUCCESS','REVERTED':'FAILED'}[e['outcome']]==r['status'],'conditional reconciliation')
  states[u]=r;prev=row['digest']
 need(len(states)<=64,'U envelope');return {'head':prev,'states':states,'job':job,'source_qualified':False,'actual_admission':False}
def declarations():
 out=[]
 for schema,fs in SCHEMAS.items():
  for f in (*fs,'$record','presence','availability','encoding_length'):
   out.append({'node_id':'I164:EXECUTOR-'+schema+'.'+f,'record':'EXECUTOR-'+schema,'selector':f,'source_file':SOURCE,'source_anchor':'Session/validate_intent; exact variant '+schema,'slots':256 if schema in ['LOG','PAYLOAD','RECORD','BLOB'] else 64,'declared_exposure':'UNKNOWN','reuse':'NONE','representation':'EXACT-CANONICAL-JSON-OR-BLOB','phase':['E','PRE-EXECUTION','PRE-COMMITMENT'],'lifecycle_context':'RECOVERY is a lifecycle context, not a new accepted phase','custody':['UNKNOWN']*7,'owner_source_id':'I164-EXACT-CUT-PROFILE-4','genuine_value':'UNAVAILABLE','qualification':'UNAVAILABLE'})
 return out

# The ABI remains the owner of nested operation/decision argument shapes.
_base_declarations=declarations
def declarations():
 out=_base_declarations();abi_path=ROOT/'retained/kernel/candidate/contract/ABI.json'
 abi=load(abi_path)
 for method in ('signPetition','signPetitionWithZKProof'):
  fn=next(f for f in abi if f.get('type')=='function' and f.get('name')==method)
  def visit(items,parent=''):
   for f in items:
    pointer=parent+'/'+f['name'];row=dict(out[0]);row.update(node_id='I164:EXECUTOR-ARGS-'+method+'.F'+digest(pointer.encode())[:24],record='EXECUTOR-ARGS-'+method,selector=pointer,source_file='kernel/candidate/contract/ABI.json',source_anchor=method+pointer,source_sha256=sha(abi_path),slots=64,representation=f['type']);out.append(row)
    if f['type']=='tuple':visit(f['components'],pointer)
  visit(fn['inputs'])
 for row in out:
  row['multiplicity_status']='DRAFT-DIRECTORY-BOUND; complete operational BACKUP/STATUS repetition is not established' if row['record'] in ('EXECUTOR-BACKUP','EXECUTOR-STATUS') else 'RETAINED-64-U-ENVELOPE-UPPER-BOUND'
  row.setdefault('source_sha256',sha(ROOT/'retained'/row['source_file']))
 return out

def validate_export(envelope,expected_binding,expected_head):
 need(set(envelope)=={'meta','entries','blobs'},'export keys')
 need(envelope['meta']==expected_binding and set(expected_binding)=={'version','code','job'},'cross-job/code binding')
 need(type(envelope['entries'])is list and len(envelope['entries'])<=256,'entry bound')
 need(type(envelope['blobs'])is dict and len(envelope['blobs'])<=256,'blob count bound')
 blobs={}
 for h,v in envelope['blobs'].items():
  need(type(v)is str and len(v)<=2*(262144+2048),'blob encoding size')
  b=bytes.fromhex(v);need(v==b.hex() and digest(b)==h,'exact blob identity');blobs[h]=b
 result=validate_history(envelope['entries'],blobs,expected_binding['job'])
 need(result['head']==expected_head,'stale/incomplete history head')
 return result
