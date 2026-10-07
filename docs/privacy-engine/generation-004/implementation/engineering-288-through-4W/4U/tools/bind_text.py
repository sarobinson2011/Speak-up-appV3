"""4U mechanical derivation binding, not a protocol evidence/admission constructor."""
import copy,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODEL='dd946419e4fd4c657a0a0d663b145e958ddf3c4957bf006b94b5c3f7ec96e74d'
CONTRACT='2bbd9d52e1591bc12adc9cc0983c1686ade2cfc4cbcbeb95b6025259d5bf07fc'
BINARY='de09187b26c18dbcfbefb0d2fc03f98a74e7ecc7ba29b2c1c851fd4b0c1e31ee'
TEXT='dc5776088dfc860e25a42e260b245b607969f6c49346bd6912eecc0ef53d8a74'
SNAPSHOT='83138fdbb8e3a66ed638b32c85ddd1127775bdc2473a0e15c6344254a130fbf8'
KIT='98a1027a7968da0f940e501a6b0a65eeb4a066a301645c4110a2e637a757fa5f'
HEADER='link_order\tfrom_token_id\tto_token_id\trelation_order\trelation_class\n'
POTENTIAL=91157453467;STRUCTURAL=4368254;ROWS=91161821721;BYTES=19909380154846
S='historical/4S/';T='historical/4T/';Q='historical/4Q/'
def require(x,message):
 if not x:raise ValueError(message)
def wire(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 def unique(pairs):
  d={}
  for k,v in pairs:
   require(k not in d,'duplicate JSON key');d[k]=v
  return d
 return json.loads(Path(p).read_bytes(),object_pairs_hook=unique)
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(wire(x))
def info(p):
 with Path(p).open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 return {'bytes':Path(p).stat().st_size,'sha256':h}
def ref(root,p):return {'path':p,**info(root/p)}
def unseal(v):
 require(set(v)=={'payload','sha256'} and sha(wire(v['payload']))==v['sha256'],'sealed receipt integrity');return v['payload']
def basis(root=ROOT):
 active=read(root/(S+'candidate/ACTIVE-IDENTITIES.json'));completion=unseal(read(root/(T+'snapshot/COMPLETION.json')));job=unseal(read(root/(T+'snapshot/supervisor/IDENTITY.json')))
 receipt=read(root/(T+'Engineering-288-4T-return-verification.json'));d=read(root/(T+'results/DESCRIPTOR-CORRESPONDENCE.json'))
 require(active==job['active']==receipt['active'],'active identity joins')
 require(active['model_sha256']==MODEL and active['selected_contract_sha256']==CONTRACT,'selected model/contract')
 require(completion==receipt['completion'] and completion['job_identity_sha256']==sha(wire(job))==receipt['job_identity_sha256'],'completion evidence substitution')
 require(receipt['snapshot_sha256']==SNAPSHOT and receipt['kit_sha256']==KIT,'snapshot/kit identity')
 require(completion['complete'] is True and completion['result']=='REPLAYED-CONDITIONAL-STATIC-TEXT-STREAM-IDENTITY','completion class')
 require(completion['generated_whole_stream_sha256']==completion['replayed_whole_stream_sha256']==completion['verified_whole_stream_sha256']==TEXT,'complete textual digest')
 require(d['candidate_model_sha256']==MODEL and d['selected_contract_sha256']==CONTRACT,'descriptor correspondence')
 require(d['descriptor_sha256']==job['retained_code']['descriptor_sha256'],'exact descriptor')
 require(d['potential_rows']==POTENTIAL and d['unique_structural_rows']==STRUCTURAL and d['total_rows']==ROWS and d['serialized_bytes_analytical']==BYTES,'row/byte correspondence')
 require(d['raw_structural_rows']==STRUCTURAL and d['structural_duplicates_removed']==0,'structural uniqueness')
 require(d['header_hex']==HEADER.encode().hex(),'header law')
 require(completion['rows']==ROWS and completion['serialized_bytes']==BYTES and completion['generation_segments']==completion['replayed_segments']==6672,'complete counts')
 for key in ['actual_admission','qualification_established','independent_generator','independent_supplied_row_validation']:require(completion[key] is False and receipt[key] is False,'qualification boundary '+key)
 require(receipt['verification_script_sha256']==info(root/(T+'verify-4T-return.py'))['sha256'],'retained verifier identity')
 require(info(root/(S+'candidate/reused/selected-contract.json'))['sha256']==CONTRACT,'contract bytes')
 return active,completion,job,receipt,d

def make_envelope(root=ROOT):
 active,c,job,receipt,d=basis(root)
 return {'format':'ENGINEERING-288-STATIC-TEXT-DERIVATION-V1','authority':'User-authorized checkpoint 4U mechanical metadata construction; no source appointment or qualification','binding':active,'phase':'STATIC-ADMISSION','universe':'ALL-RETAINED-STATIC-TOKENS-AND-STRUCTURAL-RELATIONS','scoped_bundle_correspondence_established':False,
 'identity':{'digest_type':'SHA256-EXACT-CANONICAL-LINKS-TSV','sha256':TEXT,'serialized_bytes':BYTES,'rows':ROWS,'potential_rows':POTENTIAL,'structural_rows':STRUCTURAL,'token_count':426984,'generation_segments':6672,'replay_segments':6672},
 'serialization':{'header_utf8':HEADER,'encoding':'UTF-8; retained identifiers use its ASCII subset; no BOM or CR','record_framing':'literal TAB between five cells; LF after header and every row','ordering':'strict lexicographic order of four STRING cells: from_token_id,to_token_id,relation_order,relation_class','merge':'set union of structural and potential four-cell tuples; identical tuples once; provenance-distinct relations retained','potential_orientation':'original token index i<j; never reorder endpoints by lexical identifier','potential_relation':['000000','EQUALS'],'structural_relation_order':'positive one-based retained template index as exact ORD6 within 000001..999999','link_order':'global one-based decimal; minimum width six, no upper six-digit cap','whole_hash':'SHA-256(header || every complete serialized row); not a descriptor digest or concatenated segment hashes'},
 'binary_identity':{'model_field':'/equality_stream/sha256','sha256':BINARY,'serialized_bytes':729259627770,'rows':POTENTIAL,'format':'PE-G4-POTENTIAL-EQUALITY-PAIRS-V1','row_encoding':'U32-BE left index; U32-BE right index','ordering':'lexicographic index pairs, i<j'},
 'exact_inputs':{'descriptor':{'archive':'retained/Engineering-288-checkpoint-4T.zip','member':'Engineering-288-checkpoint-4T/inputs/links.txt','bytes':236894099,'sha256':d['descriptor_sha256']},'prefix_table':d['prefix_table'],'retained_code':job['retained_code'],'generation_job_identity_sha256':c['job_identity_sha256'],'generation_package_manifest_sha256':c['package_manifest_sha256']},
 'evidence':{'snapshot':ref(root,'retained/Engineering-288-4T-textual-completion.zip'),'kit':ref(root,'retained/Engineering-288-checkpoint-4T.zip'),'completion':ref(root,T+'snapshot/COMPLETION.json'),'return_verification':ref(root,T+'Engineering-288-4T-return-verification.json'),'return_verifier':ref(root,T+'verify-4T-return.py'),'descriptor_correspondence':ref(root,T+'results/DESCRIPTOR-CORRESPONDENCE.json'),'binary_correspondence':ref(root,S+'candidate/BINARY-CORRESPONDENCE.json')},
 'source_clauses':[{'source':ref(root,T+'evidence/S90-FCR.md'),'lines':[385,390],'purpose':'closed model fields; binary layout retained'},{'source':ref(root,T+'evidence/S90-FCR.md'),'lines':[773,809],'purpose':'structural/potential tuple serialization, scope and exact links_sha256'},{'source':ref(root,T+'evidence/S70.md'),'lines':[745,749],'purpose':'LINK_HEADER and EVIDENCE_HEADER'},{'source':ref(root,T+'evidence/S70.md'),'lines':[967,987],'purpose':'link_bytes and exact V2 signed/object preimages'}],
 'applicable_schema_fields':{'rebuilt_model_change':None,'future_evidence_field':'evidence.tsv.links_sha256','future_evidence_field_populated':False,'condition':'Only for a future actual bundle whose source-owned scope yields these exact complete bytes; cannot transfer whole-model digest to an unverified component or occurrence scope.','outer_profile_digest':None,'signature':None,'four_file_object_digest':None},
 'method':'GENERATION-PLUS-REPLAY-USING-THE-SAME-RETAINED-GENERATOR','independent_generator':False,'independent_supplied_row_validation':False,'physical_supplied_file_acquired':False,'authentication_established':False,'full_model_integration_completed':False,'qualification_established':False,'actual_admission':False,'completion_trust':c['receipt_trust']}

def validate_envelope(e,root=ROOT):
 expected=make_envelope(root)
 require(set(e)==set(expected),'envelope fields')
 require(e['binding']==expected['binding'],'stale model/contract/profile binding')
 require(e['identity']['digest_type']=='SHA256-EXACT-CANONICAL-LINKS-TSV','wrong digest type')
 require(e['identity']['sha256']==TEXT and e['binary_identity']==expected['binary_identity'],'binary/text digest substitution')
 for key in ['serialized_bytes','rows','potential_rows','structural_rows','token_count','generation_segments','replay_segments']:
  require(type(e['identity'][key]) is int and e['identity'][key]==expected['identity'][key],'count '+key)
 require(e['identity']['potential_rows']+e['identity']['structural_rows']==e['identity']['rows'],'separate set totals')
 require(e['serialization']==expected['serialization'],'wrong textual serialization')
 require(e['exact_inputs']==expected['exact_inputs'],'descriptor/job/code mismatch')
 require(e['evidence']==expected['evidence'],'substituted completion evidence')
 require(e['source_clauses']==expected['source_clauses'] and e['applicable_schema_fields']==expected['applicable_schema_fields'],'source/schema binding')
 for key in ['independent_generator','independent_supplied_row_validation','physical_supplied_file_acquired','authentication_established','full_model_integration_completed','qualification_established','actual_admission','scoped_bundle_correspondence_established']:
  require(e[key] is False,'unestablished claim '+key)
 require(wire(e)==wire(expected),'unexpected derivation change')
 return True

def changes(a,b,p=''):
 if type(a)!=type(b):return [{'pointer':p,'old':a,'new':b}]
 if isinstance(a,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   q=p+'/'+k.replace('~','~0').replace('/','~1')
   if k not in a:out.append({'pointer':q,'operation':'add','new':b[k]})
   elif k not in b:out.append({'pointer':q,'operation':'remove','old':a[k]})
   else:out.extend(changes(a[k],b[k],q))
  return out
 if isinstance(a,list) and len(a)==len(b):return [c for i,(x,y) in enumerate(zip(a,b)) for c in changes(x,y,p+'/'+str(i))]
 return [] if a==b else [{'pointer':p,'old':a,'new':b}]

def graph_check(g):
 by={n['id']:n for n in g['nodes']};require(len(by)==len(g['nodes']),'duplicate graph node');done=set();visiting=set()
 def visit(k):
  require(k in by,'missing graph dependency');require(k not in visiting,'cycle')
  if k in done:return
  visiting.add(k)
  for d in by[k]['depends_on']:visit(d)
  visiting.remove(k);done.add(k)
 for k in by:visit(k)
 return len(done)

def construct(root=ROOT):
 active,c,job,receipt,d=basis(root);e=make_envelope(root);save(root/'derived/TEXTUAL-IDENTITY.json',e);eref=ref(root,'derived/TEXTUAL-IDENTITY.json')
 save(root/'derived/ACTIVE-IDENTITIES.json',active)
 oldw=read(root/(S+'candidate/WITNESS-ASSEMBLY.json'));w=copy.deepcopy(oldw)
 w.update(format='CP4U-CANDIDATE-WITNESS-ASSEMBLY-1',full_static_links_sha256=TEXT,state='STATIC-BINARY-AND-TEXT-IDENTITIES-BOUND-FULL-WITNESS-BLOCKED',static_text_identity=eref,static_text_identity_bytes=BYTES,static_text_identity_rows=ROWS,static_text_identity_method=e['method'])
 w['rebound_provenance']['path']=S+'candidate/ledger/BINDING.json'
 for slot in w['required_slots']:
  if slot['requirement_id']=='binary-stream':slot['artifact']['path']=S+'candidate/BINARY-CORRESPONDENCE.json'
  if slot['requirement_id']=='text-stream':slot.update(state='BLOCKED',mechanical_identity=eref,remaining=['physical exact-byte acquisition','independent supplied-row validation','scope-specific correspondence and authentication'])
 w['new_execution_receipts_created']=False;save(root/'derived/WITNESS-ASSEMBLY.json',w)
 oldrs=[json.loads(x) for x in (root/(S+'inventory/REQUIREMENTS.jsonl')).read_text().splitlines()];rs=copy.deepcopy(oldrs)
 for r in rs:
  if r['id']=='text-stream':
   r.update(category='mechanical-identity-complete-supplied-validation-outstanding',mechanical_identity=eref,missing_dependencies=['Physical complete supplied bytes or a separately reviewed recoverable exact-byte acquisition route.','Independent row validation of exact consumed bytes, legal membership, strict ordering/uniqueness, and separate structural/potential completeness.','Actual source-owned scopes and signed bundles; full-model static identity cannot automatically qualify component or occurrence views.'],acquisition_action='Reuse 4T identity. Prepare bounded review/prototype of recoverable exact-byte delivery to retained independent validator; do not rerun either completed identity pass. Obtain actual supplied files and authoritative scope/bundle inputs for integration.')
   r['available_artifacts'].append({**eref,'evidence_kind':'conditional same-generator generation/replay identity only'})
  elif r['id']=='execution-host':
   r['note_4U']='Ubuntu completed hash-only binary and textual jobs. Physical 19.91 TB storage/stream delivery, independent validation resources and genuine full-model scope costs remain unprovisioned.'
   r['acquisition_action']='Reuse completed host measurements. Preflight the distinct independent-validation/acquisition workload before authorizing it; completed 4T budget does not authorize another run.'
  elif r['id']=='final-profile':r['missing_dependencies']=['Actual independently governing policy/assumptions and other immutable members; exact source-owned correspondence and final outer bytes. Binary model and static textual identity exist; physical scoped supplied evidence and its authentication remain absent.']
 save(root/'derived/REQUIREMENTS.json',rs)
 (root/'derived/REQUIREMENTS.jsonl').write_bytes(b''.join(wire(r) for r in rs))
 oldgap=read(root/(S+'inventory/GAP-REPORT.json'));gap=copy.deepcopy(oldgap)
 gap.update(format='CP4U-GAP-UPDATE-1',text_stream_sha256=TEXT,text_stream_identity=eref,partial_mechanical=['text-stream','execution-host'],identity_subobligation_complete=True,independent_supplied_row_validation=False,physical_supplied_file_acquired=False,authentication_established=False,full_model_integration_completed=False,parent_inventory=info(root/(S+'inventory/REQUIREMENTS.jsonl')))
 gap['blocked']=[r['id'] for r in rs if r['status']=='BLOCKED'];gap['available_mechanical']=[r['id'] for r in rs if r['status']=='AVAILABLE-MECHANICAL'];save(root/'derived/GAP-REPORT.json',gap)
 oldg=read(root/(S+'dependencies/DEPENDENCY-GRAPH.json'));g=copy.deepcopy(oldg)
 g.update(format='CP4U-ACYCLIC-DEPENDENCY-UPDATE-1',retained_artifact_namespace='Exact paths on unchanged 4S archive unless node sets artifact_namespace=4U',no_current_receipts=True)
 for n in g['nodes']:
  if n['id']=='textual-identity':n.update(artifact='derived/TEXTUAL-IDENTITY.json',artifact_namespace='4U',depends_on=['candidate-model','selected-contract','model-arrays','textual-completion-evidence'],disposition='AVAILABLE-CONDITIONAL-MECHANICAL',reason='Exact hash and counts bound from completed retained-generator generation/replay; not supplied-row validation or qualification.')
  if n['id']=='candidate-model':n.update(disposition='UNCHANGED-FROM-4S',reason='No textual field in closed model schema. Binary equality_stream identity is unchanged; separate derivation envelope avoids a new model hash.')
  if n['id']=='ledger-binding':n.update(disposition='UNCHANGED-FROM-4S',reason='No model/source/contract change; 4S ledger binding remains exact. No duty disposition is discharged by textual generation/replay.')
  if n['id']=='signed-bundles':n['depends_on']+=['independent-supplied-row-validation'];n['reason']+=' Whole-model text identity applies only after exact scope correspondence; signed results and qualifications still absent.'
 g['nodes'] += [
 {'id':'textual-completion-evidence','depends_on':['model-arrays','selected-contract'],'artifact':'retained/Engineering-288-4T-textual-completion.zip','artifact_namespace':'4U','disposition':'PRESERVED-HISTORICAL-COMPLETED-JOB','reason':'Exact original 4T model/code-bound job; no journal rebinding or new execution receipt.'},
 {'id':'exact-text-byte-acquisition','depends_on':['textual-identity'],'artifact':None,'disposition':'MISSING','reason':'No physical full TSV exists. Existing stdin validation can consume bytes but native durable recovery expects seekable regular files. A no-full-materialization recoverable adapter needs separate review and bounded tests.'},
 {'id':'independent-supplied-row-validation','depends_on':['exact-text-byte-acquisition','candidate-model','selected-contract'],'artifact':None,'disposition':'NOT-EXECUTED','reason':'Retained independent validators implement legal membership/order/unique separate completeness and consumed-byte digest. Generator replay does not discharge this check.'}]
 graph_check(g);save(root/'derived/DEPENDENCY-GRAPH.json',g)
 cmp=read(root/(S+'results/MODEL-COMPARISON.json'));unchanged={'format':'CP4U-UNCHANGED-MODEL-COMPARISON-1','old':cmp['new'],'new':cmp['new'],'changes':[],'arrays':cmp['unchanged_arrays'],'array_evidence_basis':'Reused completed 4S comparison; exact same whole-model bytes verified again. No model parsing/expansion rerun.','binary_equality_stream_sha256':BINARY,'textual_digest_inserted_into_model':False,'model_rebinding_required':False,'source_contract_amendment_changed':False}
 save(root/'derived/MODEL-COMPARISON.json',unchanged)
 pairs=[('WITNESS-ASSEMBLY',oldw,w),('REQUIREMENTS',oldrs,rs),('GAP-REPORT',oldgap,gap),('DEPENDENCY-GRAPH',oldg,g)]
 save(root/'derived/CHANGED-FIELDS.json',{'format':'CP4U-EXACT-METADATA-DIFF-1','model_changes':[],'source_changes':[],'contract_changes':[],'changes':{n:changes(a,b) for n,a,b in pairs},'new_artifact':'derived/TEXTUAL-IDENTITY.json','historical_changes':[]})
 save(root/'derived/DEPENDENCY-IMPACT.json',{'format':'CP4U-BINDING-IMPACT-1','model':cmp['new'],'contract_sha256':CONTRACT,'unchanged':['accepted source/amendment bytes','candidate model including binary equality_stream','token/template/structural arrays','selected contract','source provenance and static directory selectors','4S mechanical ledger binding and NOT-ESTABLISHED dispositions','historical signatures, fixtures, journals and receipts'],'updated':['separate textual derivation envelope','witness static-links identity slot, without ready/admitted result','text-stream identity sub-obligation and host experience notes','dependency graph and exact metadata differences'],'future_dependencies':['actual evidence.tsv.links_sha256 only for proven exact scoped bytes','three source-owned scope closures and exact tokens.tsv','final outer-profile identity from genuine immutable members','three evidence result cells from qualified ledger/assessor outcomes','pure Ed25519 original V2 signed message','four-file length-prefixed object digest including signature.txt','new job catalogs and prerequisite receipts from exact actual inputs'],'final_profile_digest':None,'object_digest':None,'signature':None,'actual_admission':False})
 return {'result':'PASS-CONSTRUCTED-TEXTUAL-DERIVATION','model_changed':False,'requirements':len(rs),'blocked_groups':len(gap['blocked']),'identity_subobligation_complete':True,'full_stream_processed':False,'actual_admission':False}
if __name__=='__main__':print(json.dumps(construct()))
