"""Offline candidate metadata construction; no runtime signing, model expansion or registration."""
import ast,copy,gzip,json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'support/code'))
from common import enc,sha,need,same,Invalid
from static_declarations import build as source_templates, schemas
BLOCKERS=['QUALIFIED-DEPENDENCY-VISIBILITY-CUSTODY','ACTUAL-PHASE-PRODUCER-APPOINTMENTS','OPERATIONAL-CUSTODY-ROLLBACK-LIFETIME','FINITE-LIFETIME-ACQUISITION-AND-STORAGE','EXTERNAL-OUTCOME-SERIALIZATION-FINALITY','COMPLETE-MODEL-GRAPH-AND-LEDGER-BINDING','CANONICAL-REGISTRATION-NOT-PERFORMED']
SCOPE='I164-PROSPECTIVE-CANDIDATE-METADATA-1'
def read(p):return (ROOT/p).read_bytes()
def load(p):return json.loads(read(p))
def ident(p):
 b=read(p);return {'path':p,'bytes':len(b),'sha256':sha(b)}
def save(p,v):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(enc(v))
def pin_inputs():
 need(sha(read('provenance/input-pins.json'))=='7ec905a46ed6d532919a4aabf5b365d705888274c375f287388412ef35319df0','INPUT-PIN-SUBSTITUTION');pins=load('provenance/input-pins.json')
 for p,v in pins.items():need(ident(p)==v,'INPUT-IDENTITY:'+p)
 return pins

def namespace():
 rows=[json.loads(x) for x in gzip.decompress(read('native/candidate/ledger/node-duties.jsonl.gz')).splitlines()]
 ids=[r['field_class'] for r in rows];need(len(ids)==len(set(ids))==45043,'HISTORICAL-NAMESPACE')
 need(len(ids)==load('native/records/candidate-delta.json')['counts']['surfaces'][1],'HISTORICAL-COUNT')
 return ids

def mapping(path):
 rows=load('native/'+path)
 return [{'id':r['node_id'],'origin':{'path':'native/'+path,'pointer':'/'+str(i)},'native':r} for i,r in enumerate(rows)]
def roundtrip(rows,path):
 original=load('native/'+path)
 need(len(rows)==len(original),'NATIVE-MEMBER-COUNT')
 for i,(r,o) in enumerate(zip(rows,original)):
  same(r,{'id':o['node_id'],'origin':{'path':'native/'+path,'pointer':'/'+str(i)},'native':o},'NATIVE-ROUNDTRIP')
 # Original file, including whitespace/order, is retained; mapping does not reserialize it.
 return ident('native/'+path)

def declarations(bundle,inherited):
 rows=bundle['templates'];ids=[r['id'] for r in rows];need(len(ids)==len(set(ids)),'TEMPLATE-DUPLICATE');seen=set(ids)
 proposed={i:'I164:PROSPECTIVE-META1.F'+sha(i.encode()) for i in ids}
 need(not set(proposed.values())&set(inherited),'INHERITED-CLASS-CONFLICT')
 need(len(set(proposed.values()))==len(rows),'PROPOSED-CLASS-CONFLICT')
 out=[]
 for r in rows:
  need(r['parent'] is None or r['parent'] in seen,'MISSING-PARENT')
  p='support/'+r['source'];need(sha(read(p))==r['source_sha256'],'DECLARATION-SOURCE')
  out.append({'id':proposed[r['id']],'template_id':r['id'],'parent':None if r['parent'] is None else proposed[r['parent']],'native_template':r,'identity_status':'PROPOSED-CANDIDATE-ONLY'})
 return out

# Semantic associations are explicitly scoped code correspondence, not qualified edges.
RULES=[
 ('attempt-ancestry',['ATTEMPT:/parent','ATTEMPT:/action','ATTEMPT:/transaction','ATTEMPT:/ordinal','ATTEMPT:/retry_id'],'reference/runtime/accounting.py','record','first parent/transaction/retry_id null; retry parent is latest same-action attempt; immutable charged ordinal'),
 ('intent-retirement-owner',['U-ENTRY:/intent','U-ENTRY:/reservation','U-ENTRY:/retired','OWNERSHIP-ROW:/owner'],'reference/runtime/ownership.py','claim','permanent same chain/executor/nonce owner; different owner rejects; no transfer'),
 ('branch-template',['ACTION:/branch','ACTION:/kind','ACTION:/template','ACTION:/intent','ACTION:/u'],'reference/runtime/authority.py','apply','source branch eligibility; OPEN union reserved; abandonment excludes petition signing; PROCEED immediately unresolved'),
 ('charged-decision',['ACTION:/attempt_ordinal','COUNTS:/attempt','RESOURCES:/holds','RESOURCES:/query_holds'],'reference/runtime/accounting.py','reserve','atomic headroom before decision/signing/retry transmission; charges permanent'),
 ('once-only-disposition',['TRANSPORT-ENTRY:/slot','RESOURCES:/slots','RESOURCES:/holds'],'reference/runtime/accounting.py','settle','first failure HELD to CONSUMED once; retry stays CONSUMED; success releases only unused hold'),
 ('query-obligation',['QUERY:/attempt','QUERY:/ordinal','RESOURCES:/query_holds','COUNTS:/query'],'reference/runtime/accounting.py','query','first reserved query converts hold; extra polls separately charged; missing outcome unresolved'),
 ('signature-persistence',['PENDING:/phase','PENDING:/tx','ACTION:/template'],'reference/runtime/authority.py','sign','DECIDED -> SIGNING then exact signature persistence -> SIGNED; interrupted SIGNING cannot authorize conflicting action'),
 ('release-ancestry',['PENDING:/released','PENDING:/latest','ATTEMPT:/transaction','RELEASE-RESULT:/bytes','RETRY-RELEASE-RESULT:/bytes'],'reference/runtime/authority.py','apply','one-shot release committed before response; explicit retry requires fresh authorization and same exact signed bytes'),
 ('outcome-binding',['OBSERVATION:/action','OBSERVATION:/transaction','OBSERVATION:/query','OBSERVATION:/nonce_consumed'],'reference/runtime/authority.py','apply','qualified conditional disposition binds queried logical action; no broadcast attribution or nonexecution inferred'),
 ('immutable-history',['EVENT:/previous','EVENT:/after','HEAD:/head'],'reference/runtime/authority.py','state','canonical HEAD/latest-event agreement; retained counters/retirement/holds; no recovery allowance'),
 ('response-authentication',['RESPONSE:/signature','RESPONSE:/response','PACKET:/signature','JOURNAL:/response_hex'],'code/register.py','validate_response_projection','exact original signed envelope; packet digest distinct from request digest; challenge and occurrence association'),
 ('backup-obligation',['BACKUP-ENTRY:/key','BACKUP-ENTRY:/value','COUNTS:/snapshot'],'reference/runtime/authority.py','apply','RETAINED-UNCERTAIN obligation survives cleanup; no inferred completion callback')]
def associations(fields):
 by={r['template_id']:r['id'] for r in fields};out=[]
 for name,ends,path,fn,guard in RULES:
  need(all(e in by for e in ends),'ASSOCIATION-ENDPOINT:'+name)
  raw=read('support/'+path);tree=ast.parse(raw);nodes=[n for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==fn]
  need(nodes,'SOURCE-ANCHOR:'+name)
  out.append({'id':name,'endpoints':[{'template':e,'class':by[e]} for e in ends],'source':ident('support/'+path),'anchors':[{'function':fn,'first_line':n.lineno,'last_line':n.end_lineno} for n in nodes],'guard':guard,'status':'SOURCE-CODE-CORRESPONDENCE','qualified_dependency':'UNKNOWN','visibility':'UNKNOWN','custody':['UNKNOWN']*7,'occurrence_instantiation':'saved export fold / exact projection; complete symbolic expansion pending'})
 return out

def construct():
 pins=pin_inputs();ns=namespace();bundle=source_templates();same(bundle,load('support/declarations/static.json'),'REVIEWED-TEMPLATES')
 fields=declarations(bundle,ns);groups,owners,optional=schemas();guards={r["id"]:r["guard"] for r in bundle["templates"]}
 a=mapping('retained/registers/fields.json');b=mapping('records/added-fields.json')
 roundtrip(a,'retained/registers/fields.json');roundtrip(b,'records/added-fields.json')
 need(set(x['id'] for x in a+b)<=set(ns),'NATIVE-NAMESPACE')
 rel=load('support/reference/relationships-43.json');need(len(rel)==43,'RELATIONSHIPS')
 same(rel,load('native/retained/mapping/records/relationships-43.json'),'INHERITED-RELATIONSHIPS')
 catalog=ast.parse(read('native/prior-code/model_kernel/catalog.py'));ctx=next(ast.literal_eval(n.value) for n in catalog.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CONTEXTS' for t in n.targets))
 same(list(ctx),load('native/sources/selected-contract.json')['contexts'],'CONTEXT-DEFINITION')
 out={}
 out['inheritance.json']=load('provenance/inheritance.json')
 out['namespace.json']={'historical_classes':ns,'complete_for_pinned_historical_candidate':True,'source':ident('native/candidate/ledger/node-duties.jsonl.gz'),'prospective_classes':[r['id'] for r in fields]}
 out['native-mapping.json']={'format':'LOSSLESS-CANDIDATE-NATIVE-VIEW-1','canonical_schema':False,'fields':a+b,'exact_native_containers':[ident('native/'+p) for p in ['retained/registers/fields.json','records/added-fields.json','retained/registers/schemas.json','retained/registers/source-forms.json','retained/registers/dependencies.json','retained/registers/custody.tsv','records/surface-delta.json']],'source_resolution':load('provenance/native-sources.json'),'historical_overlay_order':['retained/registers/fields.json','records/added-fields.json','records/surface-delta.json'],'note':'surface-delta applies model owner anchors only; preserve original rows and exact overlay; no old field rewriting'}
 out['fields.json']={'inherited_mapping':'native-mapping.json','inherited_namespace':'namespace.json','prospective':fields,'canonical_registration':False}
 out['schemas.json']={'inherited':ident('native/retained/registers/schemas.json'),'prospective':groups,'guards':guards,'optional':optional,'field_membership':{g:[r['id'] for r in fields if r['native_template']['record']==g] for g in groups},'canonical_registration':False}
 out['source-forms.json']={'inherited':ident('native/retained/registers/source-forms.json'),'prospective':[{'record':g,'shape':groups[g],'owner':owners[g],'field_classes':[r['id'] for r in fields if r['native_template']['record']==g]} for g in sorted(groups)],'canonical_registration':False}
 out['associations.json']={'inherited_dependencies':ident('native/retained/registers/dependencies.json'),'inherited_relation_rules':ident('native/records/relation-rules.json'),'prospective':associations(fields),'qualification':'UNAVAILABLE'}
 out['contexts.json']={'scope':SCOPE,'historical_definitions':[ident('native/prior-code/model_kernel/catalog.py')]+[ident(str(p.relative_to(ROOT))) for p in sorted((ROOT/'native/sources').rglob('*')) if p.is_file()],'associations':[{'context':c,'scope':SCOPE,'class_directory':'fields.json#/prospective','status':'NEW-CANDIDATE-ASSOCIATION','canonical':False} for c in ctx],'full_expansion':False,'no_equivalence_between_contexts_inferred':True}
 out['directories.json']={'source':ident('support/code/model_adapter.py'),'local':{'U':{'max':64,'guard':'retired lifetime entries, no reset'},'stage':{'max':1,'guard':'one lifetime staged U; terminal retained'},'aggregate_attempt_guard':{'max':2070,'guard':'historical aggregate guard; not attainable prospective count'},'attempt':{'max':102,'guard':'charged before action; shared failure/hold constraints'},'slots_plus_holds':{'max':16,'guard':'atomic reserve; unknown keeps hold'},'stage_queries':{'max':2086,'guard':'inside shared 3110; charged plus reserved obligations'},'shared_queries':{'max':3110,'guard':'shared lifetime; includes preserved Pilot001 debit'},'extra_queries':{'max':16,'guard':'additional poll debit'},'stage_backups':{'max':85,'guard':'inside shared 130; unresolved retained'},'shared_snapshots':{'max':130,'guard':'includes preserved Pilot001 backup'},'verifier':{'max':64,'guard':'shared budget, stage partition18'},'stage_verifier':{'max':18,'guard':'finalize and ZK proceed incl retries'},'events':{'max':12000,'guard':'local fail-closed history cap'},'journal':{'max':384000,'guard':'per journal only, atomic count/check/insert'},'shared_owners':{'max':4096,'guard':'local ownership ledger cap; no lifetime replenishment'}},'structural_attempt_upper_bounds':{'ordinary':101,'ZK':61,'attainability':'NOT-DEMONSTRATED'},'lifetime_acquisition_recovery_diagnostics':{'bound':None,'status':'UNRESOLVED','blocks':['finite-full-model-directory','full-domain-capacity','final-binding']},'physical_storage':{'bound':None,'status':'UNRESOLVED'},'external_evidence':{'bound':None,'policy':'Decision B; fail closed unresolved, not outcome exclusion'}}
 out['directories.json']['defining_sources']=[ident('support/reference/runtime/'+p+'.py') for p in ['authority','accounting','ownership']]
 out['directories.json']['branch_directories']={'parameter':'n=ceil(exact original message bytes/512); b=start_nonce; p=b+n+2','begin':'b; one if OPEN committed','append':'b+1..b+n; next authenticated index only','finalize':'b+n+1; after all n appends','proceed':'p; finalized, no pending, branch not ABANDON','abandon':'eligible reconciled Open next q; or finalized p; or confirmed petition revert p+1','cleanup':'early abandon q+1; finalized abandon/proceed p+1; post-revert abandon p+2; semantic FAILED per source manager state','ownership':'RETIRE petition coordinate; OPEN full union [b,p+2], shared chain/executor/nonce permanent owner','retry':'same exact tx/nonce; new attempt ancestry and charge; no new signature','bounds_status':'guarded alternatives; not additive independently attainable maxima'}
 out['ledger-duties.json']={'inherited_binding':ident('native/candidate/ledger/binding.json'),'prospective_duties':[{'association':r['id'],'duty':'SOURCE/SELECTOR/REFERENCE/EXACT-BYTE-CORRESPONDENCE','mechanical_basis':r['source'],'qualified_assessor':None,'status':'METADATA-DECLARED; saved-example checks separate'} for r in out['associations.json']['prospective']],'classification_duties':BLOCKERS,'risk_allocation':'UNAVAILABLE','full_ledger_bound':False}
 decisions=['reference/prospective-APPROVAL.md','reference/I164-RETRY-ACCOUNTING-ADOPTION-1.md','reference/RETRY-SPEC.md','reference/C5-ADOPTION-CLAUSES.md','reference/C5-TRANSITIONS.md']
 out['profile-binding.json']={'format':SCOPE,'association':'FIRST-PROSPECTIVE-CANDIDATE','historical_profile':ident('native/candidate/profile-binding.json'),'adopted_basis':[ident('support/'+p) for p in decisions],'precedence':'later explicit adoption and RETRY-3 implementation resolve historical proposal text; no allowance amendment','runtime':[ident('support/reference/runtime/'+p+'.py') for p in ['authority','accounting','ownership']],'adapters':[ident('support/code/'+p+'.py') for p in ['correspondence','ingest','register','pipeline','model_adapter','static_ingest','static_declarations','response_obligations','framing_templates']],'metadata':{p:{'bytes':len(enc(v)),'sha256':sha(enc(v))} for p,v in out.items()},'canonical_registration':False,'project_designation':'construction authorized only','complete_model_binding':False,'qualification':False,'blockers':BLOCKERS,'actual_admission':False}
 out['status.json']={'scope':SCOPE,'metadata':'CONSTRUCTED; focused validation receipt separate','project_designation':'AUTHORIZED-CANDIDATE-CONSTRUCTION','canonical_registration':'NOT-OCCURRED','canonical_head':None,'registered_delta_chain':'NOT-APPLICABLE-NO-PROSPECTIVE-BASELINE','complete_immutable_model_binding':False,'qualification':False,'stream_identities':'UNCOMPUTED','actual_admission':False,'blockers':BLOCKERS,'review_support':'IA-01 and SD-01 remain scoped; no independent review of this new candidate yet'}
 out['identity.json']={'scope':SCOPE,'input_pin_sha256':sha(read('provenance/input-pins.json')),'construction_code':ident('tools/baseline.py'),'artifacts':{p:{'bytes':len(enc(v)),'sha256':sha(enc(v))} for p,v in out.items()},'canonical_registration':False,'actual_admission':False}
 return out

def validate_values(actual,expected):
 need(set(actual)==set(expected),'ARTIFACT-MEMBERSHIP')
 for p in expected:same(actual[p],expected[p],'ARTIFACT-SUBSTITUTION:'+p)
 return {'metadata_correspondence':'PASS','canonical_registration':False,'final_binding':'BLOCKED','actual_admission':False}
def validate_disk():
 expected=construct();actual={p.name:json.loads(p.read_bytes()) for p in (ROOT/'candidate').iterdir() if p.is_file()};r=validate_values(actual,expected)
 for p,v in expected.items():need(read('candidate/'+p)==enc(v),'EXACT-CANDIDATE-BYTES:'+p)
 return r

def final_binding(actual,claims=None):
 # Project designation is not qualification. A claim object cannot discharge evidence.
 raise Invalid('FINAL-BINDING-BLOCKED:'+','.join(BLOCKERS))
if __name__=='__main__':
 if sys.argv[1:] == ['build']:
  need(not (ROOT/'candidate').exists(),'OUTPUT-EXISTS')
  out=construct()
  for p,v in out.items():save('candidate/'+p,v)
  print('Constructed',len(out),'candidate artifacts; no canonical registration')
 elif sys.argv[1:] == ['validate']:print(json.dumps(validate_disk()))
 else:raise SystemExit('usage: baseline.py build|validate')
