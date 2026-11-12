"""Bounded prospective managed-route coverage adapter; never a serving entry point.

Consumes pinned predecessor declarations and source. Emits no canonical class,
ordinal, token stream or runtime authority. Constructed scenarios are model checks,
not observations of the implementation. The inherited compilers remain unchanged.
"""
import ast, copy, hashlib, json, sys, zipfile
from pathlib import Path

PINS={'compiler/live_connection.py': {'path': 'compiler/live_connection.py', 'bytes': 5717, 'sha256': '7344170ca01a2dbbd3afbeb4a6a55c0b95db0edb1a8d74e4fa4638b6dcfc6da5'}, 'compiler/persistence_values.py': {'path': 'compiler/persistence_values.py', 'bytes': 13786, 'sha256': '410d0792ad0f6c805b33cc50efa29a3324fff5f3b97dd031bcaf8d0e64dad1ff'}, 'compiler/guard_relationships.py': {'path': 'compiler/guard_relationships.py', 'bytes': 6813, 'sha256': '97942b56af75398ad562da808d746787b7226d5400e1ca0a7dbe80fb98b9ac9b'}, 'compiler/guard_oracle.py': {'path': 'compiler/guard_oracle.py', 'bytes': 6171, 'sha256': 'b46c25dedf8d72151b5be405dbc3f12fdb05ac47293ee9e118171f8ece9ebb2e'}, 'compiler/prospective_procedure.py': {'path': 'compiler/prospective_procedure.py', 'bytes': 7210, 'sha256': '93bcd24f129465e4bef01c764f77d80e4c7cb98e121da6c459f83756b3bcfade'}, 'compiler/observation_contract.py': {'path': 'compiler/observation_contract.py', 'bytes': 10828, 'sha256': '04b32963c7e3e1d730c0f0dd815c6c46e98140f56979e11afa9e17105d556fa9'}, 'compiler/value_flow.py': {'path': 'compiler/value_flow.py', 'bytes': 13008, 'sha256': 'd0df4d091e3349c79fc4d0a2f66578891f7bfa59f4ad8003e26b44354ab52d18'}, 'compiler/program_coverage.py': {'path': 'compiler/program_coverage.py', 'bytes': 15875, 'sha256': 'bf466786fd868f0b482107cde803b3098d07ecbb661f6535f8c47a801c420d46'}, 'compiler/semantic.py': {'path': 'compiler/semantic.py', 'bytes': 17290, 'sha256': 'e2766583a1a4d43792f30ff827c07fd7dbecefc8fdfb0fb764b84637a3177ea8'}, 'compiler/compiler.py': {'path': 'compiler/compiler.py', 'bytes': 17964, 'sha256': 'b8f5b7e8bbc87c7290bdfdb34e4ee5a179d536501228c70b27e7a776b37639c4'}, 'support/code/ingest.py': {'path': 'support/code/ingest.py', 'bytes': 10971, 'sha256': 'a742246454965ad83f6e680dfe0d5f58b47287a38fad3ec88767d077d8fd8a6c'}, 'support/code/correspondence.py': {'path': 'support/code/correspondence.py', 'bytes': 18047, 'sha256': '5768ff4503be04bdf956b47c40a6bf8a1cd8ae0597f1d55212f562a5b054b8b2'}, 'support/code/static_declarations.py': {'path': 'support/code/static_declarations.py', 'bytes': 17393, 'sha256': 'b9186095473a06b7b0ee2f9c98c484935db14a233daa48bbe76e3293ec42d1af'}, 'support/code/response_obligations.py': {'path': 'support/code/response_obligations.py', 'bytes': 13306, 'sha256': 'bc6744af79b5269d67c2fad76d8f27bf6726043dd68b7c0e4bc99542fca7a1b7'}, 'support/reference/runtime/authority.py': {'path': 'support/reference/runtime/authority.py', 'bytes': 23223, 'sha256': '4565bb30cb637b3cef40a3f1da2b3722840b747ab110fa37eede0cbc2e3b313a'}, 'support/reference/runtime/accounting.py': {'path': 'support/reference/runtime/accounting.py', 'bytes': 4461, 'sha256': '7c344469895db20062380e60ad60e055e6fc5121a167720bc64162f2e8aa26cc'}, 'support/reference/runtime/ownership.py': {'path': 'support/reference/runtime/ownership.py', 'bytes': 5543, 'sha256': '484bb578e1fff08bd397fea25987c929400bb203ae72cf55b8091db5007b2b18'}, 'candidate/profile-binding.json': {'path': 'candidate/profile-binding.json', 'bytes': 4300, 'sha256': '0aaf70bc861021624388d81e05ef54e36f06848afce8f9d097bc801feeb1e9ac'}, 'candidate/fields.json': {'path': 'candidate/fields.json', 'bytes': 8750933, 'sha256': 'c52ea23610fc8f22f26a86c2a54120136f122cccab6d67f26cb9af4f1e2ee81a'}, 'candidate/directories.json': {'path': 'candidate/directories.json', 'bytes': 2961, 'sha256': '93b2e8c9b676e9315f960c5b1e69f8729fe2d9860b68121d3a634ac6c52bc76a'}, 'candidate/associations.json': {'path': 'candidate/associations.json', 'bytes': 14410, 'sha256': 'd61768526d4852958fd82e81e217b4f833e698ba01c454bd6cbec13d68d7086a'}, 'candidate/ledger-duties.json': {'path': 'candidate/ledger-duties.json', 'bytes': 4650, 'sha256': 'a52d1481a358fb5bb0738457a31923752a196523d965539e80443be3d2442098'}, 'candidate/identity.json': {'path': 'candidate/identity.json', 'bytes': 1672, 'sha256': '82dd8bd19fa850809a7403a1f51023831bd04c46fb5f68dc65bedcdbc41fcc3a'}, 'candidate/contexts.json': {'path': 'candidate/contexts.json', 'bytes': 2619, 'sha256': '4e545aa7e28a0e1dd500b795e2215d824c1831ae055812431ff2256f94c7ce7b'}, 'compiler_outputs/compiler-output.json': {'path': 'compiler_outputs/compiler-output.json', 'bytes': 35589854, 'sha256': 'b75724b3ab871040b3aa8d33c4cd1a5be7e682019a52793b835af72a9146514b'}, 'prospective_outputs/semantic/rules.json': {'path': 'prospective_outputs/semantic/rules.json', 'bytes': 372128, 'sha256': 'aa5485ceebf704637071d536ecddaa1169e4deb3783c551ec2663804802142b1'}, 'prospective_outputs/procedure.json': {'path': 'prospective_outputs/procedure.json', 'bytes': 11932093, 'sha256': '4ba2258a6008f3acef259fa8c560e612771dfb9ab756a6b8846b07d5a8847bb1'}, 'guard_emission_outputs/coverage.json': {'path': 'guard_emission_outputs/coverage.json', 'bytes': 6349813, 'sha256': '49922d4f01b534ba9b11df3b0f534bac943851effde09e8af988725f50204865'}, 'integration/candidate_pipeline.py': {'path': 'integration/candidate_pipeline.py', 'bytes': 12979, 'sha256': 'f9fba68bbc2a6c9341b676d22d3b6b233531af650e20fd11e2c38700d7c91d1d'}}
MANAGER = 'compiler/live_connection.py'
PERSISTENCE = 'compiler/persistence_values.py'
REVIEW = 'evidence/managed-integration/PF01-closure-review.zip'
REVIEW_ID = {'bytes':2345116,'sha256':'3473d8d2c5100f2842ec6f41ffcb9a7506a32b1658237d4d77d15cb91b177b39','entries':33}
FILES = {
 'profile':'candidate/managed-route/profile.json',
 'model':'candidate/managed-route/model.json',
 'producers':'candidate/managed-route/producers.json',
 'directories':'candidate/managed-route/directory-relations.json',
 'procedure':'prospective_outputs/managed-route/procedure-duty.json',
 'coverage':'compiler_outputs/managed-route-coverage.json'}
BOUNDARY = {'exclusive_connection_owner':True,'trusted_process':True,
 'mandatory_entry':'compiler/live_connection.py:open_session',
 'serving_arrangement':'reviewed single managed instance; serialized access',
 'raw_or_legacy_access':False,'competing_owners':False,
 'native_sqlite_cross_thread_qualification':False}
LIMITS = {'canonical_registration':False,'final_binding':'BLOCKED',
 'full_expansion_ready':False,'stream_identities':'UNCOMPUTED',
 'actual_admission':False,'real_storage_durability':'UNRESOLVED','backup':'KERNEL-ONLY'}
GAPS = ['source-owned lifetime/session/queue/recovery multiplicities',
 'operational exclusive ownership and mandatory ingress evidence',
 'native SQLite cross-thread / cross-process serving qualification',
 'real-storage durability, coherent rollback image and external anchoring',
 'complete feasible interruption, implicit exception and transitive runtime paths',
 'authenticated backup, external outcome/finality and qualified custody',
 'complete model/ledger, canonical designation and final binding',
 'runtime observation adapter for the new managed model records']
OBLIGATIONS = ['exact-committed-history','charges-and-allowances','reservations-and-retired-U',
 'immutable-intent','attempt-ancestry','signing-and-release-uncertainty',
 'saved-responses-and-authenticated-request-challenge','unresolved-recovery',
 'external-nonexecution-not-established','no-authorization-renewal',
 'no-conflicting-action','no-silent-resubmission']
FAMILIES = ['HEAD','HEAD-AFTER','EVENT','COUNTS','PARTITIONS','RESOURCES','U-ENTRY',
 'STAGE','PENDING','ATTEMPT','ACTION','QUERY','TRANSPORT-ENTRY','JOURNAL','REQUEST',
 'PACKET','RESPONSE','SUCCESS-RESPONSE','ERROR-RESPONSE','BLOB-STORE','SIGNED-RESULT',
 'RELEASE-RESULT','RETRY-RELEASE-RESULT','OWNERSHIP-META','OWNERSHIP-ROW','OWNERSHIP-ROW-SQL',
 'CONFIG','BINDING','UNSIGNED-INTENT','COMPACT-INTENT']
# Requirement interpretations are bounded to the exact bodies below. Every source
# statement/call/guard is separately inventoried and checked by the retained oracle.
REQUIREMENTS = [
 ('entry',['__init__','open_session'],'Exact Authority bytes; existing databases; recover before Scheduler(managed); exclusive owner is an external premise, not acquired by this code.'),
 ('normal',['_require','_run','state','handle','binding','config'],'Lock acquired, READY, live present, retired absent; no transaction before or after dispatch; config copied. A normal return is not external execution proof.'),
 ('quarantine',['_run','_quarantine','_require'],'BaseException revokes READY before reference transfer; failed rollback may leave dirty state but no subsequent managed dispatch is admitted.'),
 ('queued',['_run','_require'],'Per-instance RLock serializes entry; queued callers recheck current state after acquiring lock. No fairness, queue bound or native-thread suitability is established.'),
 ('interrupted-cleanup',['_quarantine','recover','_dispose'],'Interrupted reference transfer remains gated by phase; recover quarantines any remaining live reference before disposal. Process death requires new-process recovery, not a durable quarantine record.'),
 ('close-confirmed',['close','_dispose','recover'],'Retired close must return normally before reference removal and CLOSED; recovery disposes before opening.'),
 ('close-uncertain',['_dispose','recover'],'Close exception/acknowledgement loss retains retired handle and CLEANUP_UNCERTAIN; no reopen or dispatch until later confirmed close.'),
 ('reopening',['recover','_validate'],'READY recovery rejects; both existing files required; retain partially constructed Authority; no create, request, retry or allowance reset in recovery.'),
 ('open-failed',['recover','_dispose'],'Failed construction remains non-READY. A partial db is retained for cleanup; failed cleanup stays uncertain. Lack of db attribute does not prove storage non-execution.'),
 ('validation-failed',['_validate','recover','_dispose'],'Validate exact head, ordered events, blobs, journal, ownership and config through retained ingest; check inactive transaction before/after; failed validation cannot publish access.'),
 ('restored',['recover','status'],'Only after successful initialization and validation, publish live, clear retired, increment epoch, set READY. Recovery only; no new attempt authorization.'),
 ('response-correspondence',[],'Corrected persistence validator governs observed UPDATE argument types and authenticated envelope/request/challenge correspondence. It is an evidence checker, NOT a call made by ManagedAuthority._validate.'),
 ('obligation-preservation',['_validate','recover','status'],'Recovered history retains charges, reservations, immutable intent, ancestry and saved responses. Missing responses and cleanup never prove non-execution or discharge uncertain signing/release/recovery obligations.')]

def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def digest(b):return hashlib.sha256(b).hexdigest()
def identity(root,path):
 b=(Path(root)/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':digest(b)}
def need(value,code):
 if not value:raise ValueError(code)
def same(a,b,code):need(enc(a)==enc(b),code)
def load(root,path):return json.loads((Path(root)/path).read_bytes())
def check_pins(root):
 for path,expected in PINS.items():same(identity(root,path),expected,'STALE-SOURCE-OR-INPUT:'+path)
def review(root):
 p=Path(root)/REVIEW;b=p.read_bytes();need(len(b)==REVIEW_ID['bytes'] and digest(b)==REVIEW_ID['sha256'],'REVIEW-IDENTITY')
 with zipfile.ZipFile(p) as z:
  names=z.namelist();need(len(names)==33 and len(set(names))==33 and z.testzip() is None,'REVIEW-CRC-MEMBERSHIP')
  m=json.loads(z.read('MANIFEST.json'));same(sorted(names),sorted(list(m)+['MANIFEST.json']),'REVIEW-MEMBERSHIP')
  for n,v in m.items():
   raw=z.read(n);same({'bytes':len(raw),'sha256':digest(raw)},v,'REVIEW-MEMBER:'+n)
  summary=json.loads(z.read('SUMMARY.json'))
  need(summary['independent_negative_groups']==41 and summary['engineering_negative_groups_inspected_not_counted_as_independent']==28,'REVIEW-COUNTS')
  return {'archive':identity(root,REVIEW),'closure':summary,'prior_managed_review':{'fresh_independent_checks':62,'engineering_inspected_checks':123,'rerun':False},
   'attribution':'Retained Formal-Lab[5] closure; inspected here, not freshly executed',
   'delivery_failure':'Documentary failure preserved inside exact review; altered binary unavailable; no reconstruction'}

def source_inventory(root):
 # Verify bytes before importing either retained source traversal.
 check_pins(root)
 sys.path.insert(0,str(Path(root)/'compiler'))
 import guard_relationships as gr
 raw=(Path(root)/MANAGER).read_bytes();tree=ast.parse(raw);guards,unsupported=gr.derive(raw)
 need(not unsupported,'UNSUPPORTED-MANAGED-SYNTAX')
 rows=[];functions={}
 for n in ast.walk(tree):
  if isinstance(n,ast.FunctionDef):functions[n.name]={'site':gr.key(n),'expression':ast.get_source_segment(raw.decode(),n)}
  if hasattr(n,'lineno') and (isinstance(n,ast.stmt) or type(n).__name__ in ['Call','IfExp','BoolOp','ListComp','SetComp','DictComp','GeneratorExp','Lambda']):
   rows.append({'site':gr.key(n),'kind':type(n).__name__,'expression':ast.get_source_segment(raw.decode(),n),'guards':guards[gr.key(n)]})
 gr.validate_rows(raw,rows)
 need(set(functions)=={'__init__','status','_require','_quarantine','_run','state','handle','binding','config','_dispose','close','_validate','recover','open_session'},'MANAGED-FUNCTION-DOMAIN')
 # These checks make the key semantic order explicit as well as byte bound.
 require=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='_require')
 need(ast.unparse(require.body[0].test)=="self._phase != 'READY' or self._live is None or self._retired is not None",'READY-GUARD')
 q=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='_quarantine')
 need(ast.unparse(q.body[0])=="self._phase = 'QUARANTINED'",'REVOKE-BEFORE-TRANSFER')
 return {'source':identity(root,MANAGER),'functions':functions,'sites':rows,
  'scope':'complete selected statement/call/guard inventory of managed module; not proof of feasible path execution',
  'implicit_exceptions_and_arbitrary_interruptions':'GAP except prior scoped observations; no universal proof'}

def compile_bundle(root):
 root=Path(root);check_pins(root);rv=review(root);src=source_inventory(root)
 fields=load(root,'candidate/fields.json')['prospective'];dirs=load(root,'compiler_outputs/compiler-output.json');rules=load(root,'prospective_outputs/semantic/rules.json')
 assoc=load(root,'candidate/associations.json')['prospective'];duties=load(root,'candidate/ledger-duties.json')
 selected=[f for f in fields if f['native_template']['record'] in FAMILIES];ids={f['id'] for f in selected}
 need(set(FAMILIES)<={f['native_template']['record'] for f in selected},'MISSING-MODEL-FAMILY')
 directory=[d for d in dirs['directories'] if d['class'] in ids]
 structural=[r for r in dirs['relations'] if ids.intersection(r['endpoints'])]
 semantic=[r for r in rules['rules'] if r['from']['class'] in ids or r['to']['class'] in ids]
 reqs=[{'id':'managed:'+key,'functions':fn,'requirement':text,'status':'BOUNDED-SOURCE-CORRESPONDENCE; operational premises unestablished'} for key,fn,text in REQUIREMENTS]
 common={'format':'I164-MANAGED-INTEGRATION-1','limits':LIMITS,'gaps':GAPS,'ordinal_allocation':None}
 loader_raw=(root/'integration/candidate_pipeline.py').read_text();loader_tree=ast.parse(loader_raw)
 loader_anchor=next(n for n in loader_tree.body if isinstance(n,ast.FunctionDef) and n.name=='load_candidate')
 loader={'source':PINS['integration/candidate_pipeline.py'],'function':'load_candidate','first_line':loader_anchor.lineno,'last_line':loader_anchor.end_lineno,'exact_source':ast.get_source_segment(loader_raw,loader_anchor),'native_membership':'pinned candidate identity + source-derived baseline.validate_disk','managed_membership':FILES,'scope':'combined-tree loading only; historical producer inventories retain old identities, not current full-loader coverage'}
 profile=dict(common,layout_loader=loader,base_profile=PINS['candidate/profile-binding.json'],adopted_limits=PINS['candidate/directories.json'],acceptance_boundary=BOUNDARY,
  requirements=reqs,pf01_closure=rv,prior_findings='SV-01, SV-02, VF-01, EB-01 and prior scoped findings preserved; EB-01 applies to recorded CPython 3.12.14 optimize=0 observations, not arbitrary interpreters',
  excluded=['raw Authority and legacy entry points','private attributes / Python introspection','competing owners and other connections','unsupported thread/process/serving arrangements'])
 model=dict(common,base_fields=PINS['candidate/fields.json'],existing_declarations=selected,
  local_declarations=[{'id':'managed-local:'+name,'type':typ,'source':PINS[MANAGER],'scope':'per managed instance; prospective only','canonical_class':None,'ordinal':None,'runtime_evidence':'UNAVAILABLE for this declaration adapter'} for name,typ in [('phase','CLOSED|READY|QUARANTINED|CLEANUP_UNCERTAIN|OPEN_FAILED|VALIDATION_FAILED'),('live','optional opaque Authority reference'),('retired','optional opaque Authority reference'),('epoch','integer; per instance only'),('lock','RLock; no queue or fairness bound'),('recovery-result','status/head/recovery_only/new_attempt_authorized')]],
  preservation_obligations=OBLIGATIONS,full_model_binding=False)
 persistence_raw=(root/PERSISTENCE).read_bytes();persistence_tree=ast.parse(persistence_raw)
 persistence_anchors=[{'function':n.name,'first_line':n.lineno,'last_line':n.end_lineno,'expression':ast.get_source_segment(persistence_raw.decode(),n)} for n in persistence_tree.body if isinstance(n,ast.FunctionDef) and n.name in {'contract','inspect','validate'}]
 need(len(persistence_anchors)==3,'PERSISTENCE-ENTRY-DOMAIN')
 retained=load(root,'guard_emission_outputs/coverage.json')
 for family in FAMILIES:
  need(family in retained['families'],'MISSING-RETAINED-PRODUCER-FAMILY')
  need({x['class'] for x in retained['families'][family]['declarations']}=={x['id'] for x in selected if x['native_template']['record']==family},'RETAINED-PRODUCER-DECLARATION-JOIN')
 maps=[]
 for r in reqs:
  maps.append({'requirement':r['id'],'source':PINS[MANAGER] if r['functions'] else PINS[PERSISTENCE],
   'anchors':[dict(function=f,**src['functions'][f]) for f in r['functions']] if r['functions'] else persistence_anchors,
   'affected_model_families':FAMILIES if r['functions'] else ['JOURNAL','REQUEST','PACKET','RESPONSE','SUCCESS-RESPONSE','ERROR-RESPONSE'],
   'mapping_role':'entry / preservation / recovery guard, not a claim this function directly produces every affected field',
   'local_declarations':[x['id'] for x in model['local_declarations']],
   'dependency_role':'runtime recovery uses support/code/ingest.py' if r['functions'] else 'offline semantic and receipt evidence checker; not recovery runtime dependency',
   'obligations':OBLIGATIONS,'multiplicity':None,'occurrence_evidence':'No new runtime observation; source anchors alone do not establish an event occurred'})
 persistence_functions=[{'function':n.name,'first_line':n.lineno,'last_line':n.end_lineno} for n in persistence_tree.body if isinstance(n,ast.FunctionDef)]
 producers=dict(common,layout_loader=loader,source_inventory=src,bindings=list(PINS.values()),mappings=maps,
  persistence_validator={'source':PINS[PERSISTENCE],'functions':persistence_functions,'closure':rv['archive'],'retained_legitimate_cases':14,'fresh_Formal_negative_groups':41,'Engineering_inspected_negative_groups':28,'tests_rerun_here':False},
  runtime_ingest=PINS['support/code/ingest.py'],retained_producer_map=PINS['guard_emission_outputs/coverage.json'],
  delegations=[{'from':'ManagedAuthority.state -> _run','to':'Authority.state','source':PINS['support/reference/runtime/authority.py'],'guard':'_require and inactive transaction before/after; per-instance lock'},
   {'from':'ManagedAuthority.handle -> _run','to':'Authority.handle -> apply/sign and response persistence','source':PINS['support/reference/runtime/authority.py'],'guard':'_require and inactive transaction before/after; dispatch retains original request authentication and source branches'},
   {'from':'ManagedAuthority.recover','to':'Authority.__init__','source':PINS['support/reference/runtime/authority.py'],'guard':'old handle close confirmed, existing files; initializer/validation success required before READY'},
   {'from':'ManagedAuthority._validate','to':'ingest.validate_export','source':PINS['support/code/ingest.py'],'guard':'exact recovered export with inactive transaction before/after; saved-source correspondence only'}],
  retained_producer_sites=[x for x in retained['sources']['runtime']['sites'] if set(x['families']).intersection(FAMILIES)],
  retained_projection_sites=[x for x in retained['sources']['projection']['sites'] if set(x['families']).intersection(FAMILIES)],
  retained_mapping_status='Reused byte-pinned prior source mappings; no replay, no new observations, no expanded runtime completeness')
 guarded=dict(common,base_directory=PINS['compiler_outputs/compiler-output.json'],base_rules=PINS['prospective_outputs/semantic/rules.json'],
  existing_directories=directory,existing_structural_relations=structural,existing_semantic_relations=semantic,
  managed_directories=[{'id':'managed-directory:'+r['id'],'requirement':r['id'],'guard_source':PINS[MANAGER] if r['functions'] else PINS[PERSISTENCE],
   'guard_functions':r['functions'] if r['functions'] else ['contract','inspect','validate'],'existing_directory_ids':[d['id'] for d in directory if r['functions'] or d['record'] in ['JOURNAL','REQUEST','PACKET','RESPONSE','SUCCESS-RESPONSE','ERROR-RESPONSE']],
   'cardinality':{'exact':None,'status':'UNRESOLVED','basis':'per-instance invocation, queue, recovery and lifetime evidence unavailable'},
   'range':None,'runtime_occurrences':None} for r in reqs],
  relation_inputs=[{'id':'managed-relation:'+a['id'],'inherited_association':a['id'],'endpoints':a['endpoints'],'requirement':'managed:obligation-preservation',
   'guard':'managed entry admitted; exact authenticated retained history; source-specific inherited guards still apply',
   'ordinal':None,'count':None,'qualification':'UNAVAILABLE','disposition':'NOT-ESTABLISHED'} for a in assoc])
 procedure=dict(common,base_procedure=PINS['prospective_outputs/procedure.json'],base_adapter=PINS['compiler/prospective_procedure.py'],base_ledger=PINS['candidate/ledger-duties.json'],
  duties=[{'requirement':r['id'],'producer_mapping':r['id'],'directory':'managed-directory:'+r['id'],'obligations':OBLIGATIONS,
   'inherited_duties':[d['association'] for d in duties['prospective_duties']],
   'range':None,'count':None,'classification':'UNKNOWN','qualified_assessor':None,'disposition':'NOT-ESTABLISHED'} for r in reqs],
  inherited_classification_duties=duties['classification_duties'],production_token_count=None,production_pair_count=None,
  mode='Bounded source-connected prospective inputs; no invocation of full count, lower, lifecycle or expansion',
  constructed_consumer='compiler/managed_coverage.py:consume_constructed',runtime_observation_consumer='UNAVAILABLE')
 out={'profile':profile,'model':model,'producers':producers,'directories':guarded,'procedure':procedure}
 out['coverage']=dict(common,mandatory_inputs={FILES[k]:{'bytes':len(enc(v)),'sha256':digest(enc(v))} for k,v in out.items()},
  adapter=identity(root,'compiler/managed_coverage.py'),requirements=[r['id'] for r in reqs],
  integration_entry='compiler/managed_coverage.py:validate_bundle / consume_constructed',
  legacy_pipeline='Retained unchanged. Its output alone does not establish this managed-route profile coverage.',
  complete_runtime_coverage=False)
 return out

def validate_bundle(root,bundle):
 same(bundle,compile_bundle(root),'MANAGED-INTEGRATION-SUBSTITUTION');return True
def read_bundle(root):return {k:load(root,p) for k,p in FILES.items()}
def readiness(root,bundle):
 validate_bundle(root,bundle);raise ValueError('MANAGED-READINESS-BLOCKED')

# Finite abstract fixture transitions. Deliberately not a runtime observation
# decoder: a named close/validation event here is a constructed premise, not proof.
EDGES={
 'normal':({'READY'},'READY'), 'quarantine':({'READY'},'QUARANTINED'),
 'queued-blocked':({'QUARANTINED','CLEANUP_UNCERTAIN','OPEN_FAILED','VALIDATION_FAILED','CLOSED'},None),
 'queued-ready':({'READY'},'READY'),
 'interrupted-cleanup':({'QUARANTINED','CLEANUP_UNCERTAIN'},None),
 'close-begin':({'READY','QUARANTINED','CLEANUP_UNCERTAIN','OPEN_FAILED','VALIDATION_FAILED'},'CLEANUP_UNCERTAIN'),
 'close-uncertain':({'CLEANUP_UNCERTAIN'},'CLEANUP_UNCERTAIN'),
 'close-confirmed':({'CLEANUP_UNCERTAIN'},'CLOSED'),
 'reopening':({'CLOSED'},'OPEN_FAILED'),
 'open-failed':({'OPEN_FAILED'},'OPEN_FAILED'),
 'validation-begin':({'OPEN_FAILED'},'VALIDATION_FAILED'),
 'validation-failed':({'VALIDATION_FAILED'},'VALIDATION_FAILED'),
 'restored':({'VALIDATION_FAILED'},'READY')}
REQ_FOR={'queued-blocked':'queued','queued-ready':'queued','close-begin':'close-confirmed','validation-begin':'validation-failed'}
def consume_constructed(root,bundle,case):
 validate_bundle(root,bundle)
 same(case['boundary'],BOUNDARY,'UNSUPPORTED-ACCEPTANCE-BOUNDARY')
 need(case['evidence_class']=='CONSTRUCTED-INTEGRATION-FIXTURE','NOT-A-RUNTIME-OBSERVATION-ADAPTER')
 same(case['limits'],LIMITS,'UNSUPPORTED-READINESS-ESCALATION')
 need(case['initial_phase'] in {'CLOSED','READY'},'UNSUPPORTED-FIXTURE-INITIAL-STATE')
 phase=case['initial_phase'];seen=[];validated=False;opened=False
 for step in case['steps']:
  action=step['action'];need(action in EDGES,'UNMAPPED-DISPOSITION')
  allowed,to=EDGES[action];need(phase in allowed,'QUARANTINE-OR-TRANSITION-BYPASS')
  need(step['lock_held'] is True,'MISSING-ENTRY-LOCK')
  same(step['preserved_obligations'],OBLIGATIONS,'UNJUSTIFIED-OBLIGATION-DISCHARGE')
  need(step['authorization_renewed'] is False and step['external_nonexecution'] is False and step['resubmitted'] is False,'UNJUSTIFIED-AUTHORIZATION')
  if action in {'normal','queued-ready'}:need(step['live_present'] is True and step['retired_absent'] is True and step['transaction_before'] is False and step['transaction_after'] is False,'MISSING-MANAGED-ENTRY-GUARD')
  if action=='reopening':
   need(step['existing_files'] is True,'MISSING-EXISTING-DATABASE');opened=True;validated=False
  if action=='validation-begin':need(opened and step['construction_returned'] is True,'UNCONFIRMED-REOPEN')
  if action=='restored':
   need(opened and step['validation_returned'] is True and step['transaction_before'] is False and step['transaction_after'] is False,'UNVALIDATED-ACCESS')
   # A known committed anchor can be preserved in this finite fixture; no claim
   # that the implementation has an operational external rollback anchor.
   same(step['committed_identity'],case['committed_identity'],'COMMITTED-HISTORY-SUBSTITUTION');validated=True
  if action=='close-confirmed':need(step['close_returned'] is True,'UNCONFIRMED-CLOSE');opened=False;validated=False
  if action in {'open-failed','validation-failed'}:opened=False;validated=False
  phase=to or phase;seen.append('managed:'+REQ_FOR.get(action,action))
 duties={d['requirement']:d for d in bundle['procedure']['duties']}
 need(set(seen)<=set(duties),'MISSING-PROCEDURE-DUTY')
 return {'evidence_class':'CONSTRUCTED-INTEGRATION-FIXTURE','final_phase':phase,
  'consumed_duties':[duties[k] for k in sorted(set(seen))],'runtime_execution_established':False,
  'production_count':None,'limits':LIMITS,'obligations':OBLIGATIONS,
  'fixture_validation_returned':validated}

# Bounded status-return extension. Historical compile_bundle and consumers above
# remain unchanged. This entry consumes exact saved basis declarations, not a
# new runtime, finite lifetime directory, canonical allocation or serializer.
def status_source(raw, guard_generator, guard_oracle):
 """Reconstruct requirements from the defining AST, never from a catalogue.

 Guard clauses retain their existing syntactic meaning. Ordered block prefixes
 require normal continuation to the selected statement; neither is a feasibility
 proof. Exception operands are symbolic inputs, never executed exception code.
 """
 tree=ast.parse(raw);classes=[n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority']
 need(len(classes)==1,'STATUS-OWNER');cls=classes[0]
 methods={n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)}
 need(len(methods)==sum(isinstance(n,ast.FunctionDef) for n in cls.body),'DUPLICATE-METHOD')
 generated,unsupported=guard_generator.derive(raw);wanted,unsupported2=guard_oracle.expected(raw)
 need(not unsupported and not unsupported2,'STATUS-UNSUPPORTED-GUARDS');same(generated,wanted,'STATUS-GUARD-ORACLE')
 key=guard_generator.key;text=raw.decode();parents={};functions={}
 for p in ast.walk(tree):
  for f,v in ast.iter_fields(p):
   for i,c in enumerate(v if isinstance(v,list) else [v]):
    if isinstance(c,ast.AST):parents[c]=(p,f,i if isinstance(v,list) else None)
 for name,fn in methods.items():
  for n in ast.walk(fn):functions[n]=name
 def ref(n):return {'site':key(n),'expression':ast.get_source_segment(text,n)}
 def prefixes(n):
  out=[]
  while n in parents:
   p,f,i=parents[n]
   if isinstance(p,ast.FunctionDef):break
   v=getattr(p,f)
   if i is not None and isinstance(n,ast.stmt):
    out.append({'owner':key(p),'region':f,'normal_continuation_of':[ref(a) for a in v[:i] if isinstance(a,ast.stmt)]})
   n=p
  # Method-body predecessors matter too, e.g. _dispose's early return.
  if n in parents:
   p,f,i=parents[n]
   if isinstance(p,ast.FunctionDef) and i is not None:
    out.append({'owner':key(p),'region':f,'normal_continuation_of':[ref(a) for a in getattr(p,f)[:i] if isinstance(a,ast.stmt)]})
  return list(reversed(out))
 def located(n):return dict(ref(n),function=functions.get(n),guards=copy.deepcopy(wanted[key(n)]),continuation=prefixes(n))
 def attr(n):return n.attr if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id=='self' else None
 def expr(n):
  row=dict(ref(n),guards=copy.deepcopy(wanted[key(n)]))
  if isinstance(n,ast.Constant):
   need(type(n.value) in (str,int,bool),'STATUS-LITERAL-TYPE');row.update(op='literal',type=type(n.value).__name__,value=n.value)
  elif attr(n):row.update(op='state',name=attr(n))
  elif isinstance(n,ast.Name):row.update(op='local',name=n.id)
  elif isinstance(n,ast.BinOp) and isinstance(n.op,ast.Add):row.update(op='add',left=expr(n.left),right=expr(n.right))
  elif isinstance(n,ast.IfExp):row.update(op='choice',test=expr(n.test),yes=expr(n.body),no=expr(n.orelse))
  elif isinstance(n,ast.Compare) and len(n.ops)==1 and isinstance(n.ops[0],ast.In):row.update(op='in',left=expr(n.left),right=expr(n.comparators[0]))
  elif isinstance(n,ast.Tuple):row.update(op='tuple',values=[expr(a) for a in n.elts])
  elif isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='str' and len(n.args)==1 and isinstance(n.args[0],ast.Name) and not n.keywords:row.update(op='exception-text',name=n.args[0].id)
  elif isinstance(n,ast.Attribute) and n.attr=='__name__' and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='type' and len(n.value.args)==1 and isinstance(n.value.args[0],ast.Name) and not n.value.keywords:row.update(op='exception-type-name',name=n.value.args[0].id)
  else:raise ValueError('STATUS-UNSUPPORTED-EXPRESSION:'+ast.dump(n))
  return row
 node=methods['status'];returns=[n for n in ast.walk(node) if isinstance(n,ast.Return)]
 need(len(returns)==1 and isinstance(returns[0].value,ast.Dict),'STATUS-RETURN-SHAPE');ret=returns[0]
 need(len(node.body)==1 and isinstance(node.body[0],ast.With) and len(node.body[0].items)==1 and ast.unparse(node.body[0].items[0].context_expr)=='self._lock' and node.body[0].body==[ret],'STATUS-LOCKED-RETURN')
 fields=[]
 for k,v in zip(ret.value.keys,ret.value.values):
  need(isinstance(k,ast.Constant) and type(k.value) is str,'STATUS-FIELD-KEY')
  need(attr(v) is not None or isinstance(v,ast.Constant),'STATUS-FIELD-SELECTOR')
  fields.append({'name':k.value,'value':expr(v),'key':ref(k)})
 need(len({f['name'] for f in fields})==len(fields),'DUPLICATE-STATUS-FIELD')
 selected={f['value']['name'] for f in fields if f['value']['op']=='state'}
 writes=[];calls=[];local_reads=set()
 for fn in methods.values():
  for n in ast.walk(fn):
   targets=n.targets if isinstance(n,ast.Assign) else [n.target] if isinstance(n,(ast.AugAssign,ast.AnnAssign)) else n.targets if isinstance(n,ast.Delete) else []
   for t in targets:
    if attr(t) not in selected:continue
    need(isinstance(n,(ast.Assign,ast.AugAssign)),'STATUS-UNSUPPORTED-WRITE')
    if isinstance(n,ast.AugAssign):need(isinstance(n.op,ast.Add),'STATUS-UNSUPPORTED-UPDATE')
    value=expr(n.value)
    local_reads|={a.id for a in ast.walk(n.value) if isinstance(a,ast.Name) and a.id not in ('self','type','str')}
    writes.append(dict(located(n),id='status-write:'+key(n),target=attr(t),operation='add' if isinstance(n,ast.AugAssign) else 'set',value=value))
   if isinstance(n,ast.Call) and attr(n.func) in methods:
    calls.append(n)
 writes.sort(key=lambda v:tuple(map(int,v['site'].split(':')[:2])))
 types_={}
 for w in writes:
  if w['function']=='__init__':
   need(w['operation']=='set' and w['value']['op']=='literal','STATUS-INITIAL-TYPE');need(w['target'] not in types_,'STATUS-INITIAL-AMBIGUITY');types_[w['target']]=w['value']['type']
 need(set(types_)==selected,'STATUS-INITIAL-COVERAGE')
 for f in fields:f['type']=types_[f['value']['name']] if f['value']['op']=='state' else f['value']['type']
 # Resolve parameter writes from their exact internal call sites, not a string
 # bound or a copied expected list. Outside callers remain outside this slice.
 parameter_inputs=[];locals_=[]
 for name,fn in methods.items():
  used={w['value']['name'] for w in writes if w['function']==name and w['value']['op']=='local'}
  args=[a.arg for a in fn.args.args]
  for param in sorted(used & set(args)):
   index=args.index(param)-1;need(index>=0,'STATUS-SELF-AS-VALUE')
   hits=[n for n in calls if attr(n.func)==name]
   need(bool(hits),'STATUS-UNBOUND-PARAMETER')
   for n in hits:
    need(len(n.args)==len(args)-1 and not n.keywords,'STATUS-CALL-ARGUMENTS')
    parameter_inputs.append(dict(located(n),id='status-argument:'+key(n),callee=name,parameter=param,value=expr(n.args[index])))
  for n in ast.walk(fn):
   if isinstance(n,ast.Assign):
    for t in n.targets:
     if isinstance(t,ast.Name) and t.id in local_reads:
      locals_.append(dict(located(n),id='status-local:'+key(n),name=t.id,value=expr(n.value)))
 def infer(v,fn):
  op=v['op']
  if op=='literal':return v['type']
  if op=='state':need(v['name'] in types_,'STATUS-STATE-DEPENDENCY');return types_[v['name']]
  if op in ('exception-text','exception-type-name'):return 'str'
  if op=='local':
   choices=[p for p in parameter_inputs if p['callee']==fn and p['parameter']==v['name']]+[p for p in locals_ if p['function']==fn and p['name']==v['name']]
   need(bool(choices),'STATUS-LOCAL-DEPENDENCY');ts={infer(p['value'],p['function']) for p in choices};need(len(ts)==1,'STATUS-MIXED-TYPES');return ts.pop()
  if op=='add':
   a,b=infer(v['left'],fn),infer(v['right'],fn);need(a==b and a in ('str','int'),'STATUS-ADD-TYPE');return a
  if op=='tuple':
   ts={infer(a,fn) for a in v['values']};need(len(ts)==1,'STATUS-TUPLE-TYPE');return 'tuple'
  if op=='in':infer(v['left'],fn);need(infer(v['right'],fn)=='tuple','STATUS-IN-TYPE');return 'bool'
  if op=='choice':
   need(infer(v['test'],fn)=='bool','STATUS-CHOICE-TYPE');a,b=infer(v['yes'],fn),infer(v['no'],fn);need(a==b,'STATUS-CHOICE-ARMS');return a
  raise ValueError('STATUS-INFER')
 for w in writes:
  same(infer(w['value'],w['function']),types_[w['target']],'STATUS-WRITE-TYPE')
  if w['operation']=='add':need(types_[w['target']]=='int','STATUS-UPDATE-TYPE')
 for row in writes+parameter_inputs+locals_:
  names={v['name'] for v in _status_expr_nodes(row['value']) if v['op'] in ('exception-text','exception-type-name')}
  handlers=[]
  node_=next(n for n in ast.walk(tree) if hasattr(n,'lineno') and key(n)==row['site'])
  while node_ in parents:
   node_=parents[node_][0]
   if isinstance(node_,ast.ExceptHandler):handlers.append(node_)
  row['exception_bindings']=[dict(ref(h),name=h.name,exception_type=ast.unparse(h.type)) for h in handlers if h.name in names]
  need(names<={h['name'] for h in row['exception_bindings']},'STATUS-EXCEPTION-BINDING')
 affecting={w['function'] for w in writes}
 transitions=[dict(located(n),callee=attr(n.func),id='status-transition-call:'+key(n)) for n in calls if attr(n.func) in affecting]
 embeds=[]
 for n in ast.walk(methods['recover']):
  if isinstance(n,ast.Return) and isinstance(n.value,ast.Dict):
   for k,v in zip(n.value.keys,n.value.values):
    if isinstance(v,ast.Call) and attr(v.func)=='status':
     need(not v.args and not v.keywords,'STATUS-EMBED-ARGS');embeds.append(dict(located(n),key=ast.literal_eval(k),call=ref(v),fields=[f['name'] for f in fields],validator='managed_observations.fixed_status: existing child frame and exact whole-value equality'))
 need(len(embeds)==1,'STATUS-RECOVERY-EMBEDDING')
 return {'source':{'path':MANAGER,'bytes':len(raw),'sha256':digest(raw)},'return':located(ret),'fields':fields,'writes':writes,'parameter_inputs':parameter_inputs,'local_captures':locals_,'transition_calls':transitions,'recovery_embedding':embeds,
  'control_programs':[{'function':name,**ref(fn),'ast':ast.dump(fn,include_attributes=False)} for name,fn in methods.items() if name in affecting|{'status'}],
  'coverage':'All selected direct return selectors, writes, parameter call sites, local dependencies and syntactic guards of the exact source; no feasible-path, transitive callback or lifetime completeness claim'}

def _status_expr_nodes(value):
 yield value
 for k,v in value.items():
  if isinstance(v,dict) and 'op' in v:yield from _status_expr_nodes(v)
  elif isinstance(v,list):
   for a in v:
    if isinstance(a,dict) and 'op' in a:yield from _status_expr_nodes(a)

def compile_status_fields(raw,model,producer,guard_generator,guard_oracle):
 pin=PINS[MANAGER];same({'bytes':len(raw),'sha256':digest(raw)},{k:pin[k] for k in ('bytes','sha256')},'STATUS-DEFINING-SOURCE')
 source=status_source(raw,guard_generator,guard_oracle)
 # Reuse the already bound source inventory and local declarations. Require
 # existing statement/call guards to match freshly derived source requirements.
 inventory={r['site']:r for r in producer['source_inventory']['sites']}
 for row in source['writes']+source['parameter_inputs']+source['local_captures']+source['transition_calls']+[source['return']]:
  need(row['site'] in inventory,'STATUS-INHERITED-SITE');same(inventory[row['site']]['guards'],row['guards'],'STATUS-INHERITED-GUARDS')
 declarations=[];existing={d['id']:d for d in model['local_declarations']}
 for f in source['fields']:
  selector=f['value'].get('name');local='managed-local:'+selector.removeprefix('_') if selector else None
  declarations.append({'id':'managed-status-field:'+f['name'],'name':f['name'],'type':f['type'],'value':copy.deepcopy(f['value']),'owner':'managed-status-return','source_return':source['return']['site'],
   'inherited_local':copy.deepcopy(existing.get(local)),
   'origin_ids':[w['id'] for w in source['writes'] if w['target']==selector],
   'literal_value':f['value']['value'] if f['value']['op']=='literal' else None,
   'classification':'UNKNOWN','canonical_class':None,'ordinal':None})
 return {'format':'I164-MANAGED-STATUS-FIELDS-1','source':source,
  'owning_return':{'id':'managed-status-return','kind':'source-owned Python return dictionary; no intrinsic serialized bytes','site':source['return']['site'],'field_ids':[d['id'] for d in declarations],'multiplicity':None,'classification':'UNKNOWN','canonical_class':None,'ordinal':None},
  'declarations':declarations,'reason_domain':{'finite_bound':None,'exception_text':'Exact successful type(e).__name__/str(e) operands when supported evidence exists; symbolic otherwise','normal_evaluation_required':True,'foreign_mutation_or_unsupported_callers':'Not qualified'},
  'epoch_scope':'One ManagedAuthority instance; constructor reset and source increment do not reset security obligations or identify calls globally',
  'retained_evidence':'Existing exact capture bytes and acquisition/instance/frame lineage only; no per-call logging or new status serialization',
  'static_vs_actual':'Source sites do not establish execution, feasible histories, exception content or complete repetition scope',
  'full_model_binding':False,'complete_symbolic_coverage':False}

def validate_status_fields(raw,model,producer,guards,oracle,submitted):
 # Expected membership/origins are independently regenerated from defining
 # source on every call. No submitted expected list or returned mutable object
 # is consulted. Exact JSON equality distinguishes False from 0 and int from bool.
 same(submitted,compile_status_fields(raw,model,producer,guards,oracle),'STATUS-FIELD-CORRESPONDENCE')
 return True

def status_expression_value(expression,inputs):
 """Pure model expression evaluator for explicitly CONSTRUCTED controls only.
 Does not call __str__, type, application code, or claim recorded execution.
 """
 op=expression['op']
 if op=='literal':return expression['value']
 if op=='state':return inputs['state'][expression['name']]
 if op=='local':return inputs['locals'][expression['name']]
 if op in ('exception-type-name','exception-text'):
  v=inputs['exceptions'][expression['name']]['type_name' if op=='exception-type-name' else 'text'];need(type(v) is str,'STATUS-CONSTRUCTED-EXCEPTION-TYPE');return v
 if op=='add':
  a=status_expression_value(expression['left'],inputs);b=status_expression_value(expression['right'],inputs)
  need(type(a) is type(b) and type(a) in (str,int),'STATUS-CONSTRUCTED-ADD-TYPE');return a+b
 if op=='tuple':return tuple(status_expression_value(a,inputs) for a in expression['values'])
 if op=='in':return status_expression_value(expression['left'],inputs) in status_expression_value(expression['right'],inputs)
 if op=='choice':return status_expression_value(expression['yes'] if status_expression_value(expression['test'],inputs) else expression['no'],inputs)
 raise ValueError('STATUS-CONSTRUCTED-OP')


# Appended to the existing declaration producer. No application imports.
REFERENCE_SLOTS=('_live','_retired')

def _ref_attr(n):
 return n.attr if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id=='self' else None

def reference_source(raw,guards,oracle):
 """Source-owned conditional reference relations, not an object observation.

 The walk selecting assignments is independent of generated declarations.
 Control-owned guard requirements use the retained independent oracle. Ordered
 block prefixes explicitly require *normal* continuation, including early exits.
 """
 same({'bytes':len(raw),'sha256':digest(raw)},{k:PINS[MANAGER][k] for k in ('bytes','sha256')},'REFERENCE-DEFINING-SOURCE')
 tree=ast.parse(raw);text=raw.decode();key=guards.key
 cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority')
 methods={n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)}
 generated,bad=guards.derive(raw);wanted,bad2=oracle.expected(raw)
 need(not bad and not bad2,'REFERENCE-UNSUPPORTED-GUARDS');same(generated,wanted,'REFERENCE-GUARD-ORACLE')
 parents={};owners={}
 for p in ast.walk(tree):
  for f,v in ast.iter_fields(p):
   for i,c in enumerate(v if isinstance(v,list) else [v]):
    if isinstance(c,ast.AST):parents[c]=(p,f,i if isinstance(v,list) else None)
 for fn in methods.values():
  for n in ast.walk(fn):owners[n]=fn.name
 def ref(n):return {'site':key(n),'expression':ast.get_source_segment(text,n)}
 def located(n):
  prefix=[];child=n
  while child in parents and not isinstance(child,ast.FunctionDef):
   p,f,i=parents[child]
   if i is not None and isinstance(child,ast.stmt):
    prefix.append({'owner':key(p),'region':f,'normal_continuation_of':[ref(a) for a in getattr(p,f)[:i] if isinstance(a,ast.stmt)]})
   if isinstance(p,ast.FunctionDef):break
   child=p
  return dict(ref(n),function=owners.get(n),guards=copy.deepcopy(wanted[key(n)]),continuation=list(reversed(prefix)))
 def value(n):
  if isinstance(n,ast.Constant) and n.value is None:return {'kind':'none','expression':ref(n)}
  if _ref_attr(n) in REFERENCE_SLOTS:return {'kind':'slot-reference','slot':_ref_attr(n),'expression':ref(n)}
  if isinstance(n,ast.Name) and n.id=='a':return {'kind':'invocation-local-reference','local':n.id,'expression':ref(n)}
  raise ValueError('UNSUPPORTED-REFERENCE-RHS:'+ast.dump(n))
 writes=[]
 for fn in methods.values():
  for n in ast.walk(fn):
   targets=n.targets if isinstance(n,(ast.Assign,ast.Delete)) else [n.target] if isinstance(n,(ast.AugAssign,ast.AnnAssign)) else []
   for t in targets:
    if _ref_attr(t) not in REFERENCE_SLOTS:continue
    need(isinstance(n,ast.Assign) and len(n.targets)==1,'UNSUPPORTED-REFERENCE-WRITE')
    writes.append(dict(located(n),id='managed-reference-write:'+key(n),target=_ref_attr(t),value=value(n.value),
     effect='Evaluate RHS, then replace this one slot; aliases in other slots remain',
     completion='Conditional on this assignment completing; no physical close or obligation discharge follows from a clear'))
 writes.sort(key=lambda r:tuple(map(int,r['site'].split(':')[:2])))
 # A second control-owned statement traversal supplies assignment coverage.
 # It never reads writes or a generated declaration's origin list.
 independent=[]
 def visit(n,fn):
  if isinstance(n,ast.Assign):
   for t in n.targets:
    if _ref_attr(t) in REFERENCE_SLOTS:independent.append((key(n),fn,_ref_attr(t),ast.dump(n.value,include_attributes=False)))
  for c in ast.iter_child_nodes(n):visit(c,fn)
 for name,fn in methods.items():visit(fn,name)
 same(sorted((r['site'],r['function'],r['target'],ast.dump(ast.parse(r['value']['expression']['expression'],mode='eval').body,include_attributes=False)) for r in writes),sorted(independent),'REFERENCE-ASSIGNMENT-ORACLE')
 allocations=[];calls=[];reads=[]
 for fn in methods.values():
  for n in ast.walk(fn):
   if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='a' for t in n.targets):
    need(len(n.targets)==1 and isinstance(n.value,ast.Call) and ast.unparse(n.value.func)=='self._runtime.Authority.__new__','REFERENCE-LOCAL-PRODUCER')
    same([ast.unparse(a) for a in n.value.args],['self._runtime.Authority'],'REFERENCE-ALLOCATION-ARGS');need(not n.value.keywords,'REFERENCE-ALLOCATION-KW')
    allocations.append(dict(located(n),local='a',call=ref(n.value),
     identity='Result reference of this call within its context/acquisition/instance/invocation; neither equal bytes nor this static site identifies a runtime object'))
   if isinstance(n,ast.Attribute) and _ref_attr(n) in REFERENCE_SLOTS and isinstance(n.ctx,ast.Load):reads.append(dict(located(n),slot=_ref_attr(n)))
   if isinstance(n,ast.Call):
    target=ast.unparse(n.func)
    if _ref_attr(n.func) in ('_quarantine','_dispose','_require') or target in ('self._retired.close','self._runtime.Authority.__init__','self._validate'):
     bindings=[]
     if target=='self._retired.close':bindings.append({'role':'receiver','value':{'kind':'slot-reference','slot':'_retired','expression':ref(n.func.value)}})
     for i,a in enumerate(n.args):
      if isinstance(a,ast.Name) and a.id=='a':bindings.append({'role':'argument:'+str(i),'value':value(a)})
     calls.append(dict(located(n),callee=target,reference_bindings=bindings,
      argument_rule='Receiver and arguments must evaluate normally before callee entry; exception formatting is not assumed infallible'))
 need(len(allocations)==1,'REFERENCE-ALLOCATION-DOMAIN')
 # Preserve source control for every method carrying a write or related call;
 # this includes _run's failing argument evaluation and close's ordering.
 selected={r['function'] for r in writes+calls}|{'_require'}
 programs=[dict(located(fn),ast=ast.dump(fn,include_attributes=False)) for name,fn in methods.items() if name in selected]
 return {'source':copy.deepcopy(PINS[MANAGER]),'writes':writes,'local_producers':allocations,'reference_reads':sorted(reads,key=lambda r:tuple(map(int,r['site'].split(':')[:2]))),
  'calls':sorted(calls,key=lambda r:tuple(map(int,r['site'].split(':')[:2]))),'programs':programs,
  'guards_meaning':'Syntactic evaluation guards and ordered normal-continuation prerequisites; not path feasibility, complete history or callback safety'}

def compile_reference_transfers(raw,model,producer,guards,oracle,authority):
 source=reference_source(raw,guards,oracle)
 inventory={r['site']:r for r in producer['source_inventory']['sites']}
 for row in source['writes']+source['local_producers']+source['calls']:
  need(row['site'] in inventory,'REFERENCE-INHERITED-SITE');same(inventory[row['site']]['guards'],row['guards'],'REFERENCE-INHERITED-GUARDS')
 declarations=[]
 for slot in REFERENCE_SLOTS:
  hits=[d for d in model['local_declarations'] if d['id']=='managed-local:'+slot[1:]]
  need(len(hits)==1,'REFERENCE-DECLARATION-JOIN');d=hits[0]
  same(d['source'],PINS[MANAGER],'REFERENCE-DECLARATION-SOURCE');need(d['type']=='optional opaque Authority reference','REFERENCE-DECLARATION-TYPE')
  declarations.append({'declaration':copy.deepcopy(d),'slot':slot,'write_ids':[r['id'] for r in source['writes'] if r['target']==slot],
   'reference_type':'None or opaque source reference; uninitialized is not None','classification':'UNKNOWN','multiplicity':None})
 pin=PINS['support/reference/runtime/authority.py'];same({'bytes':len(authority),'sha256':digest(authority)},{k:pin[k] for k in ('bytes','sha256')},'REFERENCE-AUTHORITY-SOURCE')
 cls=next(n for n in ast.parse(authority).body if isinstance(n,ast.ClassDef) and n.name=='Authority')
 close=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='close')
 same(ast.unparse(close),'def close(self):\n    self.db.close()','REFERENCE-AUTHORITY-CLOSE-SHAPE')
 return {'format':'I164-MANAGED-REFERENCE-TRANSFERS-1','source':source,'declarations':declarations,
  'connection_relation':{'source':copy.deepcopy(pin),'site':guards.key(close),'expression':ast.get_source_segment(authority.decode(),close),
   'meaning':'For the pinned Authority method, the receiver owns a db attribute and close delegates to db.close. Reference-token equality is not database identity or durable closure evidence.',
   'actual_object_and_connection_identity':'UNESTABLISHED from sparse saved representations'},
  'identity':{'qualifiers':['symbolic context','acquisition/capture','managed instance','invocation','source site','occurrence within invocation'],
   'copy_rule':'Copy a reference conditional on source execution; two simultaneously populated slots may alias. Never infer identity from equal dictionaries, bindings, paths, phase or epoch.',
   'allocation_rule':'One source call-result variable per invocation; no global object, finite lifetime bound or proof of allocator freshness',
   'recorded_representations':'Distinct exact retained bytes/locations and occurrence lineage remain distinct from references and connections'},
  'cleanup':'Retired clear after normal close continuation; separate no-db partial-construction clear is not a close receipt. Abrupt or unobserved continuation retains uncertainty. Clearing never cancels governing duties.',
  'static_vs_actual':'Only conditional source relations; no unseen assignment, object identity, successful cleanup or absence of outstanding obligations inferred',
  'full_model_binding':False,'complete_symbolic_coverage':False,'actual_admission':False}

def validate_reference_transfers(raw,model,producer,guards,oracle,authority,submitted):
 same(submitted,compile_reference_transfers(raw,model,producer,guards,oracle,authority),'REFERENCE-CORRESPONDENCE')
 return True

def constructed_reference_path(raw,guards,oracle,case):
 """Finite SOURCE-ONLY path algebra, never producer or database execution.

 Opaque source operations have explicit constructed normal/abrupt premises.
 Only reference/phase predicates are computed. Others require case facts. A
 stop is a partial model prefix, not an exception, durable state or recovery log.
 No statement or expression from the producer is compiled/evaluated here.
 """
 source=reference_source(raw,guards,oracle);key=guards.key
 need(type(case) is dict and set(case)=={'kind','context','scope','method','initial','facts','outcomes','stop_after'},'REFERENCE-CASE-SHAPE')
 need(case['kind']=='CONSTRUCTED-REFERENCE-PATH' and case['context'] in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'),'REFERENCE-CASE-KIND')
 need(type(case['scope']) is dict and set(case['scope'])=={'acquisition','instance','invocation'} and all(type(v) is str and v for v in case['scope'].values()),'REFERENCE-CASE-SCOPE')
 initial=case['initial'];need(type(initial) is dict and set(initial)=={'_live','_retired','_phase'},'REFERENCE-INITIAL')
 scope={'context':case['context'],**case['scope']}
 def token(label):return {'kind':'constructed-reference','scope':copy.deepcopy(scope),'origin':label}
 def unbound():return {'kind':'uninitialized-slot'}
 state={}
 for slot in REFERENCE_SLOTS:
  v=initial[slot];need(v is None or type(v) is str and bool(v),'REFERENCE-INITIAL-TYPE');state[slot]=None if v is None else token('initial:'+v)
 need(initial['_phase'] in ('CLOSED','READY','QUARANTINED','CLEANUP_UNCERTAIN','OPEN_FAILED','VALIDATION_FAILED'),'REFERENCE-INITIAL-PHASE')
 state['_phase']=initial['_phase']
 if case['method']=='__init__':
  need(initial=={'_live':None,'_retired':None,'_phase':'CLOSED'},'REFERENCE-CONSTRUCTOR-INITIAL');state={s:unbound() for s in REFERENCE_SLOTS};state['_phase']=None
 cls=next(n for n in ast.parse(raw).body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority')
 methods={n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)}
 allowed={p['function'] for p in source['programs']};need(case['method'] in allowed,'REFERENCE-METHOD')
 for k in ('facts','outcomes'):need(type(case[k]) is dict,'REFERENCE-CASE-TABLE')
 need(case['stop_after'] is None or type(case['stop_after']) is str,'REFERENCE-STOP')
 events=[];used_facts=set();used_outcomes=set();frames=[];counter=0;stopped=False
 class Abrupt(Exception):pass
 class Stop(Exception):pass
 class Returned(Exception):pass
 def emit(event,n,**values):
  events.append({'event':event,'site':key(n),'frame':frames[-1]['id'],'function':frames[-1]['function'],**copy.deepcopy(values)})
 def gate(n,kind='opaque-operation',subject=None):
  address=str(frames[-1]['id'])+'/'+key(n)+'/'+kind
  outcome=case['outcomes'].get(address,'normal');need(outcome in ('normal','raise','stop'),'REFERENCE-OUTCOME')
  if address in case['outcomes']:used_outcomes.add(address)
  emit('premise',n,kind=kind,address=address,outcome=outcome,subject=subject)
  if outcome=='raise':raise Abrupt()
  if outcome=='stop':raise Stop()
 def read(n,local):
  if isinstance(n,ast.Constant) and n.value is None:return None
  if _ref_attr(n) in REFERENCE_SLOTS:return copy.deepcopy(state[_ref_attr(n)])
  if isinstance(n,ast.Name) and n.id=='a':need('a' in local,'REFERENCE-UNBOUND-LOCAL');return copy.deepcopy(local['a'])
  raise ValueError('REFERENCE-MODEL-RHS')
 def truth(n,local):
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.Not):return not truth(n.operand,local)
  if isinstance(n,ast.BoolOp):
   if isinstance(n.op,ast.Or):return any(truth(x,local) for x in n.values)
   if isinstance(n.op,ast.And):return all(truth(x,local) for x in n.values)
  if isinstance(n,ast.Compare) and len(n.ops)==1:
   a=_ref_attr(n.left);b=n.comparators[0]
   if a in REFERENCE_SLOTS and isinstance(b,ast.Constant) and b.value is None and isinstance(n.ops[0],(ast.Is,ast.IsNot)):
    need(state[a]!=unbound(),'REFERENCE-UNINITIALIZED-READ');answer=state[a] is None;return answer if isinstance(n.ops[0],ast.Is) else not answer
   if a=='_phase' and isinstance(b,ast.Constant) and type(b.value) is str and isinstance(n.ops[0],(ast.Eq,ast.NotEq)):
    answer=state[a]==b.value;return answer if isinstance(n.ops[0],ast.Eq) else not answer
   if isinstance(n.left,ast.Name) and n.left.id=='phase' and isinstance(n.ops[0],ast.In):return local['phase'] in ast.literal_eval(b)
  address=str(frames[-1]['id'])+'/'+key(n);need(address in case['facts'],'REFERENCE-MISSING-CONSTRUCTED-FACT:'+address)
  fact=case['facts'][address];need(type(fact) is dict and set(fact)=={'value','subject'} and type(fact['value']) is bool,'REFERENCE-FACT-SHAPE')
  subject=None
  if any(isinstance(x,ast.Name) and x.id=='a' for x in ast.walk(n)):subject=local.get('a')
  elif any(_ref_attr(x)=='_live' for x in ast.walk(n)):subject=state['_live']
  same(fact['subject'],subject,'REFERENCE-FACT-SUBJECT');used_facts.add(address)
  emit('condition-premise',n,address=address,result=fact['value'],subject=subject)
  return fact['value']
 def call(n,local):
  name=_ref_attr(n.func);target=ast.unparse(n.func)
  if name in ('_quarantine','_dispose','_require'):
   gate(n,'argument-evaluation');invoke(name);return
  subject=None
  if target=='self._retired.close':subject=copy.deepcopy(state['_retired']);need(subject is not None and subject!=unbound(),'REFERENCE-CLOSE-WITHOUT-REFERENCE')
  elif target in ('self._runtime.Authority.__init__','self._validate'):subject=read(n.args[0],local)
  gate(n,'call:'+target,subject)
 def stmt(n,local):
  # A pre-statement gate permits interruption/evaluation failure before any
  # modeled effect, including before an exception argument can be evaluated.
  gate(n,'statement-entry')
  if isinstance(n,ast.If):
   arm=truth(n.test,local);emit('branch',n,truth=arm);block(n.body if arm else n.orelse,local)
  elif isinstance(n,ast.With):
   for i in n.items:gate(i.context_expr,'context-enter')
   try:block(n.body,local)
   except Stop:stopped_flag[0]=True;raise
   finally:
    # A stopped prefix has no invented exit; an exception/return can still have
    # an exit failure. No arbitrary context-manager suppression is modeled.
    if not stopped_flag[0]:gate(n,'context-exit')
  elif isinstance(n,ast.Try):
   need(not n.finalbody and not n.orelse and all(ast.unparse(h.type)=='BaseException' for h in n.handlers),'REFERENCE-MODEL-TRY')
   try:block(n.body,local)
   except Abrupt:
    need(len(n.handlers)==1,'REFERENCE-MODEL-HANDLERS');emit('handler',n.handlers[0]);block(n.handlers[0].body,local)
  elif isinstance(n,ast.Assign):
   need(len(n.targets)==1,'REFERENCE-MODEL-ASSIGN');t=n.targets[0];slot=_ref_attr(t)
   if slot in REFERENCE_SLOTS:
    before=copy.deepcopy(state);rhs=read(n.value,local);state[slot]=copy.deepcopy(rhs)
    emit('reference-write',n,target=slot,rhs=rhs,before=before,after=state)
   elif isinstance(t,ast.Name) and t.id=='a':
    gate(n.value,'allocation-return');local['a']=token('call-result:'+str(frames[-1]['id'])+':'+key(n.value));emit('local-reference',n,value=local['a'])
   elif slot=='_phase':
    v=n.value
    if isinstance(v,ast.IfExp):v=v.body if truth(v.test,local) else v.orelse
    state[slot]=local[v.id] if isinstance(v,ast.Name) else ast.literal_eval(v);emit('phase',n,value=state[slot])
   elif isinstance(t,ast.Name) and t.id=='phase':local['phase']=state['_phase']
   elif isinstance(n.value,ast.Call) and _ref_attr(n.value.func)=='_validate':call(n.value,local)
   else:gate(n,'other-assignment')
  elif isinstance(n,ast.Expr) and isinstance(n.value,ast.Call):call(n.value,local)
  elif isinstance(n,ast.Raise):emit('raise',n);raise Abrupt()
  elif isinstance(n,ast.Return):gate(n,'return-expression');emit('return',n);raise Returned()
  else:gate(n,'other-statement')
  if case['stop_after']==str(frames[-1]['id'])+'/'+key(n):raise Stop()
 def block(body,local):
  for n in body:stmt(n,local)
 def invoke(name):
  nonlocal counter
  need(name in allowed and name not in [f['function'] for f in frames],'REFERENCE-MODEL-CYCLE');counter+=1
  frame={'id':counter,'function':name};frames.append(frame)
  try:
   emit('enter',methods[name],parent=None if len(frames)==1 else frames[-2]['id'])
   try:block(methods[name].body,{})
   except Returned:pass
   emit('normal-exit',methods[name])
  except Stop:stopped_flag[0]=True;raise
  finally:frames.pop()
 stopped_flag=[False]
 try:invoke(case['method']);completion='normal'
 except Abrupt:completion='abrupt'
 except Stop:completion='partial-prefix';stopped=True
 same(sorted(used_facts),sorted(case['facts']),'REFERENCE-UNUSED-FACT')
 same(sorted(used_outcomes),sorted(case['outcomes']),'REFERENCE-UNUSED-OUTCOME')
 need(case['stop_after'] is None or stopped,'REFERENCE-UNREACHED-STOP')
 return {'kind':'CONSTRUCTED-REFERENCE-PATH-RESULT','scope':scope,'case':copy.deepcopy(case),'completion':completion,'events':events,'final':copy.deepcopy(state),
  'actual_observation':False,'object_identity_evidence':False,'physical_close_established':False,'outstanding_obligations_discharged':False,
  'limits':'Source-structured conditional model with opaque normal/abrupt premises. Not feasible-path proof, callback semantics, arbitrary bytecode interruption, process restoration or a runtime trace.'}

def validate_constructed_reference_path(raw,guards,oracle,case,submitted):
 same(submitted,constructed_reference_path(raw,guards,oracle,case),'REFERENCE-PATH-SUBSTITUTION')
 return True



# Recovery return fields: additive source correspondence, never a runtime entry.
def _recovery_locations(raw,guards,oracle):
 tree=ast.parse(raw);text=raw.decode();key=guards.key;parents={};owners={}
 generated,bad=guards.derive(raw);wanted,bad2=oracle.expected(raw)
 need(not bad and not bad2,'RECOVERY-UNSUPPORTED-GUARDS');same(generated,wanted,'RECOVERY-GUARD-ORACLE')
 for p in ast.walk(tree):
  for field,value in ast.iter_fields(p):
   for i,n in enumerate(value if isinstance(value,list) else [value]):
    if isinstance(n,ast.AST):parents[n]=(p,field,i if isinstance(value,list) else None)
 for fn in (n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)):
  for n in ast.walk(fn):owners[n]=fn.name
 def basic(n):return {'site':key(n),'expression':ast.get_source_segment(text,n)}
 def locate(n):
  child=n;prefix=[]
  while child in parents and not isinstance(child,ast.FunctionDef):
   p,f,i=parents[child]
   if i is not None and isinstance(child,ast.stmt):prefix.append({'owner':key(p),'region':f,'normal_continuation_of':[basic(a) for a in getattr(p,f)[:i] if isinstance(a,ast.stmt)]})
   if isinstance(p,ast.FunctionDef):break
   child=p
  return dict(basic(n),function=owners.get(n),guards=copy.deepcopy(wanted[key(n)]),continuation=list(reversed(prefix)))
 return tree,locate

def recovery_source(raw,authority,guards,oracle):
 """Determine return membership and origins from defining sources, independent
 of submitted/generated field declarations. Fail closed on unsupported forms.
 """
 same({'bytes':len(raw),'sha256':digest(raw)},{k:PINS[MANAGER][k] for k in ('bytes','sha256')},'RECOVERY-MANAGER-SOURCE')
 authority_pin=PINS['support/reference/runtime/authority.py']
 same({'bytes':len(authority),'sha256':digest(authority)},{k:authority_pin[k] for k in ('bytes','sha256')},'RECOVERY-AUTHORITY-SOURCE')
 tree,loc=_recovery_locations(raw,guards,oracle);atree,aloc=_recovery_locations(authority,guards,oracle)
 cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority');methods={n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)}
 def one(nodes,label):
  nodes=list(nodes);need(len(nodes)==1,'RECOVERY-SOURCE-UNIQUE:'+label);return nodes[0]
 recover=methods['recover'];ret=one((n for n in ast.walk(recover) if isinstance(n,ast.Return)),'recover return');need(isinstance(ret.value,ast.Dict),'RECOVERY-RETURN-DICT')
 keys=[ast.literal_eval(k) for k in ret.value.keys];need(all(type(k) is str for k in keys) and len(set(keys))==len(keys),'RECOVERY-KEYS')
 embedded=[];fields=[];head_origin=None
 def assignment(fn,name):
  rows=[n for n in ast.walk(fn) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)]
  row=one(rows,name+' writer');need(len(row.targets)==1,'RECOVERY-MULTITARGET');return row
 for key_node,value in zip(ret.value.keys,ret.value.values):
  name=ast.literal_eval(key_node)
  if isinstance(value,ast.Call) and ast.unparse(value.func)=='self.status':
   need(not value.args and not value.keywords,'RECOVERY-STATUS-ARGS');embedded.append({'name':name,'call':loc(value),'reuse':'Existing exact status child/parent embedding'});continue
  row={'name':name,'key':loc(key_node),'origin':loc(value),'return_site':loc(ret)}
  if isinstance(value,ast.Constant):
   need(type(value.value) is bool,'RECOVERY-LITERAL-TYPE');row.update(kind='literal',type='bool',value=value.value)
  else:
   need(isinstance(value,ast.Name),'RECOVERY-UNSUPPORTED-RETURN-VALUE');head_origin=assignment(recover,value.id)
   call=head_origin.value;need(isinstance(call,ast.Call) and ast.unparse(call.func)=='self._validate' and len(call.args)==1 and not call.keywords,'RECOVERY-VALIDATOR-ORIGIN')
   row.update(kind='validated-state-head',type='str',local=value.id,assignment=loc(head_origin),call=loc(call))
  fields.append(row)
 need(len(embedded)==1 and head_origin is not None,'RECOVERY-RETURN-SLICE')
 validator=methods['_validate'];vret=one((n for n in ast.walk(validator) if isinstance(n,ast.Return)),'validator return')
 lookup=vret.value;need(isinstance(lookup,ast.Subscript) and isinstance(lookup.value,ast.Name) and isinstance(lookup.slice,ast.Constant) and type(lookup.slice.value) is str,'RECOVERY-HEAD-LOOKUP')
 state_name=lookup.value.id;selector=lookup.slice.value;state=assignment(validator,state_name)
 need(isinstance(state.value,ast.Call) and isinstance(state.value.func,ast.Attribute) and isinstance(state.value.func.value,ast.Name) and state.value.func.attr=='state' and not state.value.args and not state.value.keywords,'RECOVERY-STATE-ORIGIN')
 parameters=[a.arg for a in validator.args.args];need(parameters==['self',state.value.func.value.id],'RECOVERY-STATE-PARAMETER')
 exports=[n for n in ast.walk(validator) if isinstance(n,ast.Assign) and isinstance(n.value,ast.Dict) and any(isinstance(k,ast.Constant) and k.value=='expected_head' for k in n.value.keys)]
 export=one(exports,'export');need(len(export.targets)==1 and isinstance(export.targets[0],ast.Name),'RECOVERY-EXPORT-LOCAL')
 x=export.targets[0].id;expected=one((v for k,v in zip(export.value.keys,export.value.values) if ast.literal_eval(k)=='expected_head'),'expected_head')
 same(ast.dump(expected,include_attributes=False),ast.dump(lookup,include_attributes=False),'RECOVERY-EXPECTED-HEAD-ORIGIN')
 ingest=one((n for n in ast.walk(validator) if isinstance(n,ast.Call) and ast.unparse(n.func)=='self._ingest.validate_export'),'ingest')
 same([ast.unparse(n) for n in ingest.args],[x],'RECOVERY-INGEST-ARGUMENT');need(not ingest.keywords,'RECOVERY-INGEST-KEYWORDS')
 ac=next(n for n in atree.body if isinstance(n,ast.ClassDef) and n.name=='Authority');astate=next(n for n in ac.body if isinstance(n,ast.FunctionDef) and n.name=='state')
 aret=one((n for n in ast.walk(astate) if isinstance(n,ast.Return)),'authority state return');need(isinstance(aret.value,ast.Name),'RECOVERY-AUTHORITY-STATE-RETURN');aload=assignment(astate,aret.value.id)
 need(isinstance(aload.value,ast.Call) and ast.unparse(aload.value.func)=='parse','RECOVERY-HEAD-PARSER')
 raw_head=one((v for k,v in zip(export.value.keys,export.value.values) if ast.literal_eval(k)=='head'),'raw head')
 # Join the two source-selected HEAD queries without executing either query.
 def query(n):return one((c for c in ast.walk(n) if isinstance(c,ast.Call) and isinstance(c.func,ast.Attribute) and c.func.attr=='execute'),'HEAD query')
 aquery=query(aload);xquery=query(raw_head)
 same([ast.literal_eval(a) for a in aquery.args],[ast.literal_eval(a) for a in xquery.args],'RECOVERY-HEAD-QUERY')
 for row in fields:
  if row['kind']=='validated-state-head':row['head_selector']=selector
 # Retain the entire selected control text as well as typed links. Ordering and
 # implicit/explicit abrupt continuation are not turned into success evidence.
 return {'source':copy.deepcopy(PINS[MANAGER]),'authority_source':copy.deepcopy(authority_pin),'return':loc(ret),'keys':keys,'fields':fields,'status_embedding':embedded,
  'head_chain':{'validator_call':loc(head_origin.value),'parameter':parameters[1],'argument':loc(head_origin.value.args[0]),'state_assignment':loc(state),'state_call':loc(state.value),
   'validator_return':loc(vret),'lookup':loc(lookup),'selector':selector,'export_assignment':loc(export),'expected_head_expression':loc(expected),'ingest_call':loc(ingest),
   'raw_head_expression':loc(raw_head),'authority_state_return':aloc(aret),'authority_state_load':aloc(aload),'authority_head_query':aloc(aquery),'export_head_query':loc(xquery)},
  'programs':[{'owner':'ManagedAuthority.recover',**loc(recover),'ast':ast.dump(recover,include_attributes=False)}, {'owner':'ManagedAuthority._validate',**loc(validator),'ast':ast.dump(validator,include_attributes=False)}, {'owner':'Authority.state',**aloc(astate),'ast':ast.dump(astate,include_attributes=False)}],
  'coverage':'Selected return fields and exact source head-origin chain with syntactic guards/normal-continuation prerequisites, not all feasible histories or new transitive authentication proof'}

def compile_recovery_fields(raw,authority,model,producer,guards,oracle):
 source=recovery_source(raw,authority,guards,oracle)
 owners=[d for d in model['local_declarations'] if d['id']=='managed-local:recovery-result'];need(len(owners)==1,'RECOVERY-OWNER-DECLARATION')
 same(owners[0]['source'],PINS[MANAGER],'RECOVERY-OWNER-SOURCE')
 heads=[d for d in model['existing_declarations'] if d.get('template_id')=='HEAD:/'+source['head_chain']['selector']];need(len(heads)==1,'RECOVERY-HEAD-DECLARATION')
 head=heads[0]
 # This is an unchanged defining HEAD declaration from the retained source
 # model, not an expected list derived from this new generated catalogue.
 same({'bytes':len(enc(head)),'sha256':digest(enc(head))},{'bytes':802,'sha256':'5fdd96c185d4857e0236458730d0016e9814db273e7e5f026bc832c5e1e1c360'},'RECOVERY-HEAD-DEFINITION')
 need(head['native_template']['type']=='STRING','RECOVERY-HEAD-TYPE')
 inventory={r['site']:r for r in producer['source_inventory']['sites']}
 for row in [source['return'],source['head_chain']['state_assignment'],source['head_chain']['export_assignment'],source['head_chain']['ingest_call'],source['head_chain']['validator_return']]+[f['assignment'] for f in source['fields'] if f['kind']=='validated-state-head']:
  need(row['site'] in inventory,'RECOVERY-INHERITED-SITE');same(inventory[row['site']]['guards'],row['guards'],'RECOVERY-INHERITED-GUARDS')
 declarations=[]
 for field in source['fields']:
  declarations.append({'id':'managed-recovery-field:'+field['name'],'name':field['name'],'type':field['type'],'origin':copy.deepcopy(field),'owner':owners[0]['id'],
   'inherited_head':copy.deepcopy(head) if field['kind']=='validated-state-head' else None,'classification':'UNKNOWN','canonical_class':None,'ordinal':None,'multiplicity':None})
 return {'format':'I164-MANAGED-RECOVERY-FIELDS-1','source':source,'owner':copy.deepcopy(owners[0]),'declarations':declarations,
  'semantics':{'head':'Source-defined head value of the state used for this normal recovery validation; not a reference/object identity, fresh request or global latest-state assertion',
   'recovery_only':'Literal True marks this return as recovery only. It does not prove no prior external effect, successful physical closure or completed obligations.',
   'new_attempt_authorized':'Literal False supplies no authorization for a new attempt, allowance renewal, nonce reuse, refund or obligation release.'},
  'type_basis':'Boolean types/constants from defining return AST; head string type reuses the exact preexisting HEAD:/head source declaration. Authentication and byte-domain checks remain the retained validators, not a new transitive parser proof.',
  'limits':{'new_serialization':False,'complete_repetition_coverage':False,'full_model_binding':False,'actual_admission':False,'multiplicity':None,'runtime_history':'UNAVAILABLE beyond exact retained evidence'}}

def validate_recovery_fields(raw,authority,model,producer,guards,oracle,submitted):
 same(submitted,compile_recovery_fields(raw,authority,model,producer,guards,oracle),'RECOVERY-FIELD-CORRESPONDENCE')
 return True

def recovery_value_projection(catalogue,returned,validated_head,status_value):
 """Pure value projection, called only after source and evidence validation.
 Constructed values exercise this algebra but are never new runtime evidence.
 """
 need(type(returned) is dict and set(returned)==set(catalogue['source']['keys']),'RECOVERY-VALUE-FIELDS')
 status_name=catalogue['source']['status_embedding'][0]['name'];same(returned[status_name],status_value,'RECOVERY-STATUS-EMBEDDING')
 result=[]
 for field in catalogue['declarations']:
  value=returned[field['name']];need(type(value).__name__==field['type'],'RECOVERY-VALUE-TYPE:'+field['name'])
  expected=field['origin']['value'] if field['origin']['kind']=='literal' else validated_head
  same(value,expected,'RECOVERY-VALUE-ORIGIN:'+field['name']);result.append({'declaration':field['id'],'name':field['name'],'value':copy.deepcopy(value)})
 return result


def binding_source(raw,authority,guards,oracle):
 """Exact getter value origin, derived without using a submitted catalogue."""
 same({'bytes':len(raw),'sha256':digest(raw)},{k:PINS[MANAGER][k] for k in ('bytes','sha256')},'BINDING-MANAGER-SOURCE')
 ap=PINS['support/reference/runtime/authority.py']
 same({'bytes':len(authority),'sha256':digest(authority)},{k:ap[k] for k in ('bytes','sha256')},'BINDING-AUTHORITY-SOURCE')
 tree,loc=_recovery_locations(raw,guards,oracle);atree,aloc=_recovery_locations(authority,guards,oracle)
 def one(nodes,label):
  rows=list(nodes);need(len(rows)==1,'BINDING-SOURCE-UNIQUE:'+label);return rows[0]
 cls=one((n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority'),'manager')
 methods={n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)};fn=methods['binding']
 same([ast.unparse(d) for d in fn.decorator_list],['property'],'BINDING-PROPERTY')
 same(ast.unparse(fn.args),'self','BINDING-ARGUMENTS')
 need(len(fn.body)==1 and isinstance(fn.body[0],ast.With),'BINDING-WITH-SHAPE');lock=fn.body[0]
 need(len(lock.items)==1 and lock.items[0].optional_vars is None,'BINDING-LOCK-SHAPE');same(ast.unparse(lock.items[0].context_expr),'self._lock','BINDING-LOCK')
 need(len(lock.body)==2 and isinstance(lock.body[0],ast.Expr) and isinstance(lock.body[0].value,ast.Call) and isinstance(lock.body[1],ast.Return),'BINDING-ORDER')
 check=lock.body[0].value;ret=lock.body[1];value=ret.value
 same(ast.unparse(check),'self._require()','BINDING-READINESS-CALL')
 need(isinstance(value,ast.Attribute) and isinstance(value.value,ast.Attribute) and isinstance(value.value.value,ast.Name) and value.value.value.id=='self','BINDING-RETURN-SHAPE')
 slot=value.value.attr;field=value.attr;same(slot,'_live','BINDING-RECEIVER');same(field,fn.name,'BINDING-ATTRIBUTE')
 req=methods['_require'];need(len(req.body)==1 and isinstance(req.body[0],ast.If) and not req.body[0].orelse,'BINDING-REQUIRE-SHAPE')
 test=req.body[0].test;need(isinstance(test,ast.BoolOp) and isinstance(test.op,ast.Or) and len(test.values)==3,'BINDING-READY-OR')
 phase,live,retired=test.values
 need(isinstance(phase,ast.Compare) and ast.unparse(phase.left)=='self._phase' and len(phase.ops)==1 and isinstance(phase.ops[0],ast.NotEq) and isinstance(phase.comparators[0],ast.Constant) and type(phase.comparators[0].value) is str,'BINDING-PHASE-GUARD')
 same(ast.unparse(live),'self.'+slot+' is None','BINDING-LIVE-GUARD');same(ast.unparse(retired),'self._retired is not None','BINDING-RETIRED-GUARD')
 need(len(req.body[0].body)==1 and isinstance(req.body[0].body[0],ast.Raise),'BINDING-REQUIRE-RAISE')
 ac=one((n for n in atree.body if isinstance(n,ast.ClassDef) and n.name=='Authority'),'authority')
 writers=[]
 for n in ast.walk(ac):
  targets=n.targets if isinstance(n,(ast.Assign,ast.Delete)) else [n.target] if isinstance(n,(ast.AugAssign,ast.AnnAssign)) else []
  if any(ast.unparse(t)=='self.'+field for t in targets):writers.append(n)
 writer=one(writers,'underlying writer');need(isinstance(writer,ast.Assign) and len(writer.targets)==1,'BINDING-WRITER-SHAPE')
 need(isinstance(writer.value,ast.Call) and ast.unparse(writer.value.func)=='sha' and len(writer.value.args)==1 and not writer.value.keywords,'BINDING-SHA-ORIGIN')
 inner=writer.value.args[0];need(isinstance(inner,ast.Call) and ast.unparse(inner.func)=='enc' and len(inner.args)==1 and isinstance(inner.args[0],ast.Dict) and not inner.keywords,'BINDING-ENC-ORIGIN')
 need(aloc(writer)['function']=='__init__','BINDING-WRITER-OWNER')
 state=one((n for n in ac.body if isinstance(n,ast.FunctionDef) and n.name=='state'),'state')
 equality=one((n for n in ast.walk(state) if isinstance(n,ast.Compare) and any(ast.unparse(v)=='self.'+field for v in n.comparators)),'state equality')
 need(len(equality.ops)==1 and isinstance(equality.ops[0],ast.Eq) and isinstance(equality.left,ast.Subscript) and isinstance(equality.left.value,ast.Name),'BINDING-STATE-EQUALITY')
 same(ast.literal_eval(equality.left.slice),field,'BINDING-STATE-SELECTOR')
 enforcement=one((n for n in ast.walk(state) if isinstance(n,ast.Call) and ast.unparse(n.func)=='need' and n.args and n.args[0] is equality),'state check')
 return {'source':copy.deepcopy(PINS[MANAGER]),'authority_source':copy.deepcopy(ap),'getter':loc(fn),'lock':loc(lock),'return':loc(ret),'value':loc(value),'receiver':loc(value.value),
  'field':field,'slot':slot,'readiness_call':loc(check),'readiness_program':loc(req),'readiness_test':loc(test),'ready_phase':phase.comparators[0].value,
  'underlying_writer':aloc(writer),'underlying_value':aloc(writer.value),'state_equality':aloc(equality),'state_check':aloc(enforcement),'state_selector':field,
  'normal_return_requires':['lock context enter completes','_require returns normally','receiver and attribute evaluation complete','lock context exit completes without error'],
  'semantics':'On normal return forward this instance live reference\'s binding attribute. No fresh state/ingest/transaction check, copy, transformation or persistence occurs in the getter.',
  'type_scope':'Existing Authority implementation/initialized instance and retained typed state premise; arbitrary Python attribute mutation, introspection or monkey-patching is outside the trusted-process correspondence.'}

def compile_binding_return(raw,authority,model,producer,guards,oracle,references):
 source=binding_source(raw,authority,guards,oracle)
 validate_reference_transfers(raw,model,producer,guards,oracle,authority,references)
 rs=references['source']
 read=[r for r in rs['reference_reads'] if r['function']=='binding' and r['site']==source['receiver']['site']]
 call=[r for r in rs['calls'] if r['function']=='binding' and r['site']==source['readiness_call']['site']]
 req=[r for r in rs['programs'] if r['function']=='_require']
 need(len(read)==len(call)==len(req)==1,'BINDING-REFERENCE-JOINS')
 for old,new in [(read[0],source['receiver']),(call[0],source['readiness_call']),(req[0],source['readiness_program'])]:
  for k in ('site','expression','guards','continuation'):same(old[k],new[k],'BINDING-INHERITED-'+k)
 inventory={r['site']:r for r in producer['source_inventory']['sites']}
 for row in (source['return'],source['lock'],source['readiness_call']):
  need(row['site'] in inventory,'BINDING-INHERITED-SITE');same(inventory[row['site']]['guards'],row['guards'],'BINDING-INHERITED-GUARDS')
 heads=[d for d in model['existing_declarations'] if d.get('template_id')=='HEAD:/'+source['state_selector']];need(len(heads)==1,'BINDING-HEAD-DECLARATION');head=heads[0]
 same({'bytes':len(enc(head)),'sha256':digest(enc(head))},{'bytes':811,'sha256':'c0deee963a471854b87398351246c4ae31577d8e717abc98bf6b912a7e7f7900'},'BINDING-HEAD-DEFINITION')
 need(head['native_template']['type']=='STRING','BINDING-HEAD-TYPE')
 return {'format':'I164-MANAGED-BINDING-RETURN-1','source':source,
  'declaration':{'id':'managed-binding-return','owner':'ManagedAuthority.binding','type':'str','inherited_binding':copy.deepcopy(head),'origin':copy.deepcopy(source['value']),
   'classification':'UNKNOWN','canonical_class':None,'ordinal':None,'multiplicity':None},
  'reference_links':{'live_read':copy.deepcopy(read[0]),'ready_call':copy.deepcopy(call[0]),'ready_program':copy.deepcopy(req[0])},
  'identity':'Reference symbols, underlying connections and recorded binding strings remain different domains. Equal strings never prove same instance/object/connection.',
  'evidence_scope':'Existing validated recovery frontier only; not an observed getter invocation or a promise that the manager remains READY later.',
  'actual_getter_observations':None,'complete_repetition_coverage':False,'full_model_binding':False,'actual_admission':False}

def validate_binding_return(raw,authority,model,producer,guards,oracle,references,submitted):
 same(submitted,compile_binding_return(raw,authority,model,producer,guards,oracle,references),'BINDING-RETURN-CORRESPONDENCE');return True

def binding_value_projection(catalogue,premise,returned):
 """Pure conditional algebra. Caller validates source and evidence premises.
 Reference symbols here name constructed variables, never observed objects.
 """
 need(type(premise) is dict and set(premise)=={'phase','live_reference','retired_reference','underlying','lock_enter_completed','attribute_completed','lock_exit_completed'},'BINDING-PREMISE-FIELDS')
 for k in ('lock_enter_completed','attribute_completed','lock_exit_completed'):need(premise[k] is True,'BINDING-NORMAL-CONTINUATION:'+k)
 need(type(premise['phase']) is str and premise['phase']==catalogue['source']['ready_phase'] and premise['live_reference'] is not None and premise['retired_reference'] is None,'BINDING-READINESS')
 live=premise['live_reference'];under=premise['underlying']
 need(type(live) is dict and set(live)=={'scope','symbol'} and type(live['symbol']) is str and bool(live['symbol']),'BINDING-REFERENCE-SYMBOL')
 need(type(under) is dict and set(under)=={'reference','binding'},'BINDING-UNDERLYING-FIELDS')
 same(under['reference'],live,'BINDING-RECEIVER-REFERENCE')
 need(type(returned) is str and type(under['binding']) is str,'BINDING-VALUE-TYPE')
 same(returned,under['binding'],'BINDING-VALUE-ORIGIN')
 return {'declaration':catalogue['declaration']['id'],'value':returned,'reference_symbol':copy.deepcopy(live),'kind':'CONSTRUCTED-CONDITIONAL; not a getter execution'}

# Configuration storage/getter correspondence. No application code is executed.
def config_source(raw,authority,guards,oracle):
 ready=binding_source(raw,authority,guards,oracle)
 tree,loc=_recovery_locations(raw,guards,oracle);atree,aloc=_recovery_locations(authority,guards,oracle)
 def one(rows,label):
  rows=list(rows);need(len(rows)==1,'CONFIG-SOURCE-UNIQUE:'+label);return rows[0]
 cls=one((n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority'),'manager')
 methods={n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)};fn=methods['config']
 same([ast.unparse(d) for d in fn.decorator_list],['property'],'CONFIG-PROPERTY');same(ast.unparse(fn.args),'self','CONFIG-ARGUMENTS')
 need(len(fn.body)==1 and isinstance(fn.body[0],ast.With),'CONFIG-WITH');lock=fn.body[0]
 need(len(lock.items)==1 and lock.items[0].optional_vars is None,'CONFIG-LOCK-SHAPE');same(ast.unparse(lock.items[0].context_expr),'self._lock','CONFIG-LOCK')
 need(len(lock.body)==2 and isinstance(lock.body[0],ast.Expr) and isinstance(lock.body[1],ast.Return),'CONFIG-ORDER')
 check=lock.body[0].value;ret=lock.body[1];same(ast.unparse(check),'self._require()','CONFIG-READY-CALL')
 def deepcopy_arg(n,label):
  need(isinstance(n,ast.Call) and ast.unparse(n.func)=='copy.deepcopy' and len(n.args)==1 and not n.keywords,'CONFIG-DEEPCOPY:'+label);return n.args[0]
 origin=deepcopy_arg(ret.value,'getter');same(ast.unparse(origin),'self._config','CONFIG-GETTER-ORIGIN')
 writers=[]
 for n in ast.walk(cls):
  targets=n.targets if isinstance(n,(ast.Assign,ast.Delete)) else [n.target] if isinstance(n,(ast.AugAssign,ast.AnnAssign)) else []
  if any(ast.unparse(t)=='self._config' for t in targets):writers.append(n)
 store=one(writers,'storage writer');need(isinstance(store,ast.Assign) and len(store.targets)==1 and loc(store)['function']=='__init__','CONFIG-STORAGE-WRITER')
 argument=deepcopy_arg(store.value,'constructor');same(ast.unparse(argument),'config','CONFIG-CONSTRUCTOR-INPUT')
 ac=one((n for n in atree.body if isinstance(n,ast.ClassDef) and n.name=='Authority'),'authority');init=one((n for n in ac.body if isinstance(n,ast.FunctionDef) and n.name=='__init__'),'authority ctor')
 exact=one((n for n in ast.walk(init) if isinstance(n,ast.Call) and ast.unparse(n.func)=='exact' and ast.unparse(n.args[0])=='config'),'config membership')
 fields=ast.literal_eval(exact.args[1]);need(type(fields) is list and all(type(k) is str for k in fields) and len(fields)==len(set(fields)),'CONFIG-FIELD-DOMAIN')
 authority_store=one((n for n in ast.walk(init) if isinstance(n,ast.Assign) and any(ast.unparse(t)=='self.config' for t in n.targets)),'authority config')
 same(ast.unparse(authority_store.value),'parse(enc(config))','CONFIG-AUTHORITY-STORAGE')
 recover_copy=one((n for n in ast.walk(methods['recover']) if isinstance(n,ast.Call) and ast.unparse(n.func)=='copy.deepcopy' and ast.unparse(n.args[0])=='self._config'),'recovery copy')
 export_copy=one((n for n in ast.walk(methods['_validate']) if isinstance(n,ast.Call) and ast.unparse(n.func)=='copy.deepcopy' and ast.unparse(n.args[0])=='self._config'),'export copy')
 return {'source':copy.deepcopy(ready['source']),'authority_source':copy.deepcopy(ready['authority_source']),
  'constructor_storage':loc(store),'constructor_input':loc(argument),'constructor_copy':loc(store.value),'getter':loc(fn),'lock':loc(lock),'return':loc(ret),'copy_call':loc(ret.value),'origin':loc(origin),
  'readiness_call':loc(check),'readiness_program':copy.deepcopy(ready['readiness_program']),'readiness_test':copy.deepcopy(ready['readiness_test']),'ready_phase':ready['ready_phase'],
  'fields':fields,'authority_membership':aloc(exact),'authority_storage':aloc(authority_store),'recovery_copy':loc(recover_copy),'export_copy':loc(export_copy),
  'normal_return_requires':['lock context enter completes','_require returns normally','copy.deepcopy of stored _config completes','lock context exit completes without error'],
  'constructor_semantics':'One deepcopy(config) evaluated before _config assignment. An interrupted/failed copy does not establish storage or successful construction. Later caller-input mutations need not equal stored values.',
  'getter_semantics':'Return deepcopy of this manager stored _config, not Authority.config; no new state/ingest/transaction check or persistence. Copy evaluation or lock exit may fail.',
  'copy_scope':'Ordinary builtin dict/list data graphs and immutable scalar leaves below; shared internal references and cycles are preserved. Actual CONFIG is flat and scalar. Custom __deepcopy__, reducers, subclasses and arbitrary Python mutation are not covered by this conditional data projection.'}

def compile_config_return(raw,authority,model,producer,guards,oracle,references):
 source=config_source(raw,authority,guards,oracle)
 validate_reference_transfers(raw,model,producer,guards,oracle,authority,references)
 rs=references['source'];calls=[r for r in rs['calls'] if r['function']=='config' and r['site']==source['readiness_call']['site']];req=[r for r in rs['programs'] if r['function']=='_require']
 need(len(calls)==len(req)==1,'CONFIG-REFERENCE-JOINS')
 for old,new in [(calls[0],source['readiness_call']),(req[0],source['readiness_program'])]:
  for k in ('site','expression','guards','continuation'):same(old[k],new[k],'CONFIG-INHERITED-'+k)
 inventory={r['site']:r for r in producer['source_inventory']['sites']}
 for k in ('constructor_storage','constructor_copy','return','copy_call','lock','readiness_call','recovery_copy','export_copy'):
  row=source[k];need(row['site'] in inventory,'CONFIG-INHERITED-SITE');same(row['guards'],inventory[row['site']]['guards'],'CONFIG-INHERITED-GUARDS')
 declarations={d['template_id']:d for d in model['existing_declarations']};config=declarations['CONFIG:'];typ=config['native_template']['type']
 need(type(typ) is dict and set(typ)=={'object'},'CONFIG-DECLARATION-TYPE');same(sorted(typ['object']),sorted(source['fields']),'CONFIG-SOURCE-FIELD-COVERAGE')
 fields={k:copy.deepcopy(declarations['CONFIG:/'+k]) for k in source['fields']}
 for k,d in fields.items():same(d['native_template']['type'],typ['object'][k],'CONFIG-FIELD-TYPE');need(d['parent']==config['id'],'CONFIG-FIELD-PARENT')
 return {'format':'I164-MANAGED-CONFIG-RETURN-1','source':source,
  'declaration':{'id':'managed-config-return','owner':'ManagedAuthority.config','inherited_config':copy.deepcopy(config),'fields':fields,'origin':copy.deepcopy(source['copy_call']),'storage_origin':copy.deepcopy(source['constructor_copy']),
   'classification':'UNKNOWN','canonical_class':None,'ordinal':None,'multiplicity':None},
  'reference_links':{'ready_call':copy.deepcopy(calls[0]),'ready_program':copy.deepcopy(req[0])},
  'copy_relation':{'container_domain':['dict with str keys','list'],'immutable_leaves':['NoneType','bool','int','float-finite','str'],
   'mutable_nodes':'bijection preserving exact kinds, key/element order, scalar types/values, internal alias classes and cycles; source/copy mutable node sets disjoint',
   'immutable_identity':'No fresh identity or physical identity claimed for scalar leaves; sharing is allowed.',
   'phases':['constructor input at copy evaluation -> manager storage','manager storage at getter copy evaluation -> returned value'],
   'no_current_input_equality_requirement':True,'no_historical_alias_observation':True},
  'actual_getter_observations':None,'complete_repetition_coverage':False,'full_model_binding':False,'actual_admission':False}

def validate_config_return(raw,authority,model,producer,guards,oracle,references,submitted):
 same(submitted,compile_config_return(raw,authority,model,producer,guards,oracle,references),'CONFIG-RETURN-CORRESPONDENCE');return True

def config_value_type(catalogue,value):
 fields=catalogue['declaration']['inherited_config']['native_template']['type']['object']
 need(type(value) is dict and set(value)==set(fields),'CONFIG-VALUE-FIELDS')
 types={'STRING':str,'INTEGER':int}
 for k,t in fields.items():need(t in types and type(value[k]) is types[t],'CONFIG-VALUE-TYPE:'+k)
 return True

def copy_graph(*values):
 """Encode constructed builtin data references, never observed addresses.
 One memo for all roots records cross-boundary sharing without serializing ids.
 """
 import math
 nodes={};memo={}
 def edge(v):
  t=type(v)
  if t in (dict,list):
   if id(v) in memo:return {'ref':memo[id(v)]}
   symbol='n'+str(len(memo));memo[id(v)]=symbol;node={'kind':t.__name__,'items':[]};nodes[symbol]=node
   if t is dict:
    need(all(type(k) is str for k in v),'COPY-DICT-KEY-TYPE');node['items']=[[k,edge(x)] for k,x in v.items()]
   else:node['items']=[edge(x) for x in v]
   return {'ref':symbol}
  need(t in (type(None),bool,int,float,str),'COPY-UNSUPPORTED-TYPE')
  if t is float:need(math.isfinite(v),'COPY-NONFINITE');v=v.hex()
  return {'atom':t.__name__,'value':v}
 roots=[edge(v) for v in values];return {'roots':roots,'nodes':nodes}

def validate_copy_graph(graph):
 """Validate a two-root deepcopy relation for the declared builtin domain.
 Input is a finite symbolic graph; cycles do not imply infinite construction.
 """
 import math
 need(type(graph) is dict and set(graph)=={'roots','nodes'},'COPY-GRAPH-FIELDS');roots=graph['roots'];nodes=graph['nodes']
 need(type(roots) is list and len(roots)==2 and type(nodes) is dict and all(type(k) is str and k for k in nodes),'COPY-GRAPH-DOMAIN')
 def edge(e):
  need(type(e) is dict,'COPY-EDGE-TYPE')
  if set(e)=={'ref'}:need(type(e['ref']) is str and e['ref'] in nodes,'COPY-DANGLING-REFERENCE');return
  need(set(e)=={'atom','value'} and type(e['atom']) is str,'COPY-ATOM-FIELDS');t=e['atom'];v=e['value']
  types={'NoneType':type(None),'bool':bool,'int':int,'str':str,'float':str};need(t in types and type(v) is types[t],'COPY-ATOM-TYPE')
  if t=='float':
   try:f=float.fromhex(v)
   except ValueError:need(False,'COPY-FLOAT')
   need(math.isfinite(f) and f.hex()==v,'COPY-FLOAT')
 for node in nodes.values():
  need(type(node) is dict and set(node)=={'kind','items'} and node['kind'] in ('dict','list') and type(node['items']) is list,'COPY-NODE')
  if node['kind']=='dict':
   keys=[]
   for pair in node['items']:need(type(pair) is list and len(pair)==2 and type(pair[0]) is str,'COPY-DICT-ITEM');keys.append(pair[0]);edge(pair[1])
   need(len(keys)==len(set(keys)),'COPY-DUPLICATE-KEY')
  else:
   for x in node['items']:edge(x)
 for r in roots:edge(r)
 def reachable(root):
  found=set();pending=[root]
  while pending:
   e=pending.pop()
   if 'ref' not in e or e['ref'] in found:continue
   s=e['ref'];found.add(s);node=nodes[s];pending.extend([p[1] for p in node['items']] if node['kind']=='dict' else node['items'])
  return found
 left=reachable(roots[0]);right=reachable(roots[1]);need(left|right==set(nodes),'COPY-UNREACHABLE-NODE');need(not left&right,'COPY-MUTABLE-SHARING')
 forward={};backward={};pending=[tuple(roots)]
 while pending:
  a,b=pending.pop();need(set(a)==set(b),'COPY-EDGE-KIND')
  if 'atom' in a:same(a,b,'COPY-ATOM-VALUE');continue
  x,y=a['ref'],b['ref']
  if x in forward:need(forward[x]==y,'COPY-ALIAS-SPLIT');continue
  need(y not in backward,'COPY-ALIAS-MERGE');forward[x]=y;backward[y]=x
  an,bn=nodes[x],nodes[y];need(an['kind']==bn['kind'] and len(an['items'])==len(bn['items']),'COPY-CONTAINER-SHAPE')
  for av,bv in zip(an['items'],bn['items']):
   if an['kind']=='dict':need(av[0]==bv[0],'COPY-KEY-ORDER');pending.append((av[1],bv[1]))
   else:pending.append((av,bv))
 return {'result':'PASS','mutable_nodes':len(forward),'alias_and_cycle_correspondence':copy.deepcopy(forward),'runtime_observation':False,'immutable_identity_claim':False}

def config_value_projection(catalogue,premise,stored,returned):
 need(type(premise) is dict and set(premise)=={'phase','live_present','retired_absent','lock_enter_completed','copy_completed','lock_exit_completed'},'CONFIG-PREMISE-FIELDS')
 need(type(premise['phase']) is str and premise['phase']==catalogue['source']['ready_phase'],'CONFIG-READY-PHASE')
 for k in ('live_present','retired_absent','lock_enter_completed','copy_completed','lock_exit_completed'):need(premise[k] is True,'CONFIG-NORMAL-CONTINUATION:'+k)
 config_value_type(catalogue,stored);config_value_type(catalogue,returned)
 relation=validate_copy_graph(copy_graph(stored,returned))
 return {'declaration':catalogue['declaration']['id'],'value':copy.deepcopy(returned),'copy_relation':relation,'runtime_observation':False}


# State-return bridge: source-derived conditional values, never runtime calls.
def state_source(raw,authority,observations,guards,oracle):
 ready=binding_source(raw,authority,guards,oracle);recovery=recovery_source(raw,authority,guards,oracle)
 same({'bytes':len(observations),'sha256':digest(observations)},{'bytes':35124,'sha256':'2b4ccd7902d8e270ac8d4b22060d08d184dda1b0e6fcdccae781fd81eef902cc'},'STATE-WRAPPER-CHECK-SOURCE')
 tree,loc=_recovery_locations(raw,guards,oracle);atree,aloc=_recovery_locations(authority,guards,oracle)
 def one(rows,label):
  rows=list(rows);need(len(rows)==1,'STATE-SOURCE-UNIQUE:'+label);return rows[0]
 cls=one((n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority'),'manager');methods={n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)}
 wrapper=methods['state'];need(not wrapper.decorator_list and ast.unparse(wrapper.args)=='self' and len(wrapper.body)==1 and isinstance(wrapper.body[0],ast.Return),'STATE-WRAPPER-SHAPE')
 wr=wrapper.body[0];call=wr.value
 need(isinstance(call,ast.Call) and ast.unparse(call.func)=='self._run' and len(call.args)==1 and not call.keywords,'STATE-WRAPPER-DELEGATION');method=ast.literal_eval(call.args[0]);same(method,wrapper.name,'STATE-WRAPPER-METHOD')
 run=methods['_run'];same(ast.unparse(run.args),'self, method, *args','STATE-RUN-ARGS');need(len(run.body)==1 and isinstance(run.body[0],ast.With),'STATE-RUN-LOCK');lock=run.body[0]
 need(len(lock.items)==1 and lock.items[0].optional_vars is None,'STATE-LOCK-SHAPE');same(ast.unparse(lock.items[0].context_expr),'self._lock','STATE-LOCK')
 need(len(lock.body)==2 and isinstance(lock.body[0],ast.Expr) and isinstance(lock.body[1],ast.Try),'STATE-READINESS-TRY-ORDER')
 req=lock.body[0];same(ast.unparse(req.value),'self._require()','STATE-REQUIRE');tr=lock.body[1]
 need(not tr.orelse and not tr.finalbody and len(tr.handlers)==1 and len(tr.body)==4,'STATE-TRY-SHAPE');pre,assign,post,ret=tr.body
 for node,message in [(pre,'UNEXPECTED-ACTIVE-TRANSACTION'),(post,'UNCOMMITTED-STATE')]:
  need(isinstance(node,ast.If) and not node.orelse and len(node.body)==1 and isinstance(node.body[0],ast.Raise),'STATE-TRANSACTION-GUARD')
  same(ast.unparse(node.test),'self._live.db.in_transaction','STATE-TRANSACTION-ORIGIN');same(ast.unparse(node.body[0].exc),'RecoveryBlocked('+repr(message)+')','STATE-TRANSACTION-RAISE')
 need(isinstance(assign,ast.Assign) and len(assign.targets)==1 and isinstance(assign.targets[0],ast.Name),'STATE-RESULT-LOCAL');result=assign.targets[0].id
 same(ast.unparse(assign.value),'getattr(self._live, method)(*args)','STATE-DISPATCH');need(isinstance(ret,ast.Return) and isinstance(ret.value,ast.Name) and ret.value.id==result,'STATE-RETURN-LOCAL')
 writers=[n for n in ast.walk(run) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==result for t in n.targets)];need(writers==[assign],'STATE-RESULT-WRITER')
 handler=tr.handlers[0];same(ast.unparse(handler.type),'BaseException','STATE-HANDLER-TYPE');need(len(handler.body)==2 and isinstance(handler.body[0],ast.Expr) and isinstance(handler.body[1],ast.Raise) and handler.body[1].exc is None,'STATE-HANDLER-SHAPE')
 quarantine=handler.body[0].value;need(isinstance(quarantine,ast.Call) and ast.unparse(quarantine.func)=='self._quarantine' and len(quarantine.args)==1 and not quarantine.keywords,'STATE-QUARANTINE')
 reason=quarantine.args[0];same(ast.unparse(reason),"type("+handler.name+").__name__ + ':' + str("+handler.name+")",'STATE-REASON-ORIGIN')
 ac=one((n for n in atree.body if isinstance(n,ast.ClassDef) and n.name=='Authority'),'authority');backend=one((n for n in ac.body if isinstance(n,ast.FunctionDef) and n.name==method),'backend')
 need(ast.unparse(backend.args)=='self','STATE-BACKEND-ARGS');need(len(backend.body)==5,'STATE-BACKEND-SHAPE')
 load,binding,event,accounting,backendret=backend.body;need(isinstance(event,ast.If) and not event.orelse,'STATE-EVENT-GUARD')
 same(ast.unparse(event.test),"s['seq']",'STATE-EVENT-TEST');same(ast.unparse(accounting),'accounting.validate(s)','STATE-ACCOUNTING')
 same(aloc(load),recovery['head_chain']['authority_state_load'],'STATE-EXISTING-LOAD');same(aloc(backendret),recovery['head_chain']['authority_state_return'],'STATE-EXISTING-RETURN')
 same(ast.unparse(binding),"need(s['binding'] == self.binding, 'VERSION-BINDING')",'STATE-BACKEND-BINDING')
 checks=[n for n in ast.walk(event) if isinstance(n,ast.Call) and ast.unparse(n.func)=='need']
 need(len(checks)==2,'STATE-EVENT-CHECKS');same([ast.literal_eval(n.args[1]) for n in checks],['HEAD-EVENT','HEAD-EVENT-TYPED'],'STATE-EVENT-CHECK-NAMES')
 obs=ast.parse(observations);prop=one((n for n in ast.walk(obs) if isinstance(n,ast.Call) and ast.unparse(n.func)=='propagate' and [ast.unparse(x) for x in n.args]==['f','run']),'existing wrapper propagation')
 stages={'lock_enter':loc(lock.items[0].context_expr),'readiness':loc(req),'pre_transaction':loc(pre),'dispatch':loc(assign.value),'post_transaction':loc(post),'return_expression':loc(ret),'handler_reason':loc(reason),'quarantine':loc(quarantine),'reraise':loc(handler.body[1]),'lock_exit':loc(lock)}
 return {'source':copy.deepcopy(ready['source']),'authority_source':copy.deepcopy(ready['authority_source']),'wrapper':loc(wrapper),'wrapper_return':loc(wr),'wrapper_call':loc(call),'method':method,'args':[],
  'run':loc(run),'result_local':result,'result_assignment':loc(assign),'run_return':loc(ret),'dispatch':loc(assign.value),'dispatch_receiver':loc(assign.value.func.args[0]),
  'readiness_program':copy.deepcopy(ready['readiness_program']),'readiness_call':loc(req.value),'ready_phase':ready['ready_phase'],'try_region':loc(tr),'handler':loc(handler),'stages':stages,
  'normal_path':['lock_enter','readiness','pre_transaction','dispatch','post_transaction','return_expression','lock_exit'],
  'caught_stages':['pre_transaction','dispatch','post_transaction','return_expression'],'outside_handler':['lock_enter','readiness','lock_exit'],
  'backend':aloc(backend),'backend_load':aloc(load),'backend_return':aloc(backendret),'binding_check':aloc(binding),'event_guard':aloc(event),'event_checks':[aloc(n) for n in checks],'accounting_check':aloc(accounting),
  'existing_recovery_head_chain':copy.deepcopy(recovery['head_chain']),
  'existing_wrapper_check':{'source':{'path':'compiler/managed_observations.py','bytes':len(observations),'sha256':digest(observations)},'line':prop.lineno,'end_line':prop.end_lineno,'expression':ast.get_source_segment(observations.decode(),prop),'scope':'Reuse saved wrapper/run propagation where full trace exists; sparse capture does not supply missing backend frames.'},
  'semantics':'Normal state wrapper passes the same delegated result reference through the result local and returns. No deepcopy or conversion in either wrapper. Backend parses HEAD and performs its own binding/event/accounting checks; this is not recovery ingestion.',
  'exception_semantics':'Readiness precedes try; lock exit follows it. Failures inside try evaluate reason before calling quarantine, then re-raise if quarantine completes. Reason/quarantine may themselves fail or be interrupted. Lock exit may supersede a pending return/exception; no quarantine is invented for exit failure.'}

def compile_state_return(raw,authority,observations,model,producer,guards,oracle,references):
 source=state_source(raw,authority,observations,guards,oracle);validate_reference_transfers(raw,model,producer,guards,oracle,authority,references)
 heads=[d for d in model['existing_declarations'] if d.get('template_id')=='HEAD:'];need(len(heads)==1,'STATE-HEAD-DECLARATION');head=heads[0]
 need(type(head['native_template']['type']) is dict and set(head['native_template']['type'])=={'object'},'STATE-HEAD-OBJECT')
 delegation=[d for d in producer['delegations'] if d['from']=='ManagedAuthority.state -> _run'];need(len(delegation)==1 and delegation[0]['to']=='Authority.state','STATE-EXISTING-DELEGATION')
 inventory={r['site']:r for r in producer['source_inventory']['sites']}
 for row in [source['wrapper_return'],source['wrapper_call'],source['result_assignment'],source['run_return'],source['readiness_call']]:
  need(row['site'] in inventory,'STATE-INHERITED-SITE');same(row['guards'],inventory[row['site']]['guards'],'STATE-INHERITED-GUARD')
 rs=references['source'];calls=[r for r in rs['calls'] if r['site']==source['readiness_call']['site']];reads=[r for r in rs['reference_reads'] if r['site']==source['dispatch_receiver']['site']]
 need(len(calls)==len(reads)==1,'STATE-REFERENCE-JOINS')
 links=[{'id':'backend-to-run-result','from':copy.deepcopy(source['backend_return']),'to':copy.deepcopy(source['result_assignment']),'kind':'direct reference forwarding after normal dispatch'},
  {'id':'run-result-to-wrapper-return','from':copy.deepcopy(source['run_return']),'to':copy.deepcopy(source['wrapper_return']),'kind':'direct reference forwarding after normal run and lock exit'}]
 declarations=[{'id':name,'type':copy.deepcopy(head['native_template']['type']),'origin':copy.deepcopy(source[site]),'classification':'UNKNOWN','canonical_class':None,'ordinal':None,'multiplicity':None} for name,site in [('underlying-state','backend_return'),('run-result','result_assignment'),('wrapper-return','wrapper_return')]]
 return {'format':'I164-MANAGED-STATE-RETURN-1','source':source,'inherited_head':copy.deepcopy(head),'declarations':declarations,'links':links,'delegation':copy.deepcopy(delegation[0]),'reference_links':{'ready':copy.deepcopy(calls[0]),'live_read':copy.deepcopy(reads[0])},
  'type_scope':'Existing HEAD declaration and independently validated exact state; recursively preserve exact types/values of that state. This bridge is not a replacement full schema/ingestion validator.',
  'identity_scope':'Equal serialized values are not object identity. Constructed scoped reference symbols stipulate forwarding; actual result/connection identities remain unobserved.',
  'actual_runtime_links':None,'complete_repetition_coverage':False,'full_model_binding':False,'actual_admission':False}

def validate_state_return(raw,authority,observations,model,producer,guards,oracle,references,submitted):
 same(submitted,compile_state_return(raw,authority,observations,model,producer,guards,oracle,references),'STATE-RETURN-CORRESPONDENCE');return True

def state_value_compare(catalogue,value,validated):
 """Finite value/type relation to a separately validated state, not admission.
 Mutable alias topology is deliberately not inferred from equal contents.
 """
 fields=catalogue['inherited_head']['native_template']['type']['object']
 need(type(value) is dict and type(validated) is dict and set(value)==set(validated)==set(fields),'STATE-VALUE-FIELDS')
 pending=[(value,validated,'')]
 while pending:
  a,b,path=pending.pop();need(type(a) is type(b),'STATE-VALUE-TYPE:'+path)
  if type(b) is dict:
   need(set(a)==set(b) and all(type(k) is str for k in a),'STATE-VALUE-FIELDS:'+path);pending.extend((a[k],v,path+'/'+k) for k,v in b.items())
  elif type(b) is list:
   need(len(a)==len(b),'STATE-VALUE-LENGTH:'+path);pending.extend((x,y,path+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b)))
  else:need(type(b) in (str,int,bool,type(None)),'STATE-UNSUPPORTED-LEAF:'+path);same(a,b,'STATE-VALUE-ORIGIN:'+path)
 return True

def state_path_projection(catalogue,outcomes):
 """Constructed stage outcomes. Normal/abrupt premises are not observations.
 Actual RLock non-suppression and trusted source execution are premises.
 """
 need(type(outcomes) is dict,'STATE-PATH-OUTCOMES');src=catalogue['source'];used=set();events=[];failure=None;quarantine_called=False;quarantine_completed=None;dispatch_completed=False
 def take(stage):
  need(stage in outcomes,'STATE-PATH-MISSING:'+stage);v=outcomes[stage];allowed=(False,True,'raise') if stage in ('pre_transaction','post_transaction') else ('normal','raise')
  need(any(type(v) is type(x) and v==x for x in allowed),'STATE-PATH-OUTCOME:'+stage);used.add(stage);events.append({'stage':stage,'site':src['stages'][stage]['site'],'outcome':v});return v
 if take('lock_enter')=='raise':failure='lock_enter'
 else:
  if take('readiness')=='raise':failure='readiness'
  else:
   for stage in src['caught_stages']:
    value=take(stage)
    if value=='raise' or value is True:failure=stage;break
    if stage=='dispatch':dispatch_completed=True
   if failure:
    if take('handler_reason')=='raise':failure='handler_reason'
    else:
     quarantine_called=True;quarantine_completed=take('quarantine')=='normal'
     if not quarantine_completed:failure='quarantine'
     else:events.append({'stage':'reraise','site':src['stages']['reraise']['site'],'outcome':'original exception re-raised'})
  if take('lock_exit')=='raise':failure='lock_exit'
 need(used==set(outcomes),'STATE-PATH-UNREACHED-OUTCOMES')
 return {'kind':'CONSTRUCTED-STATE-PATH','completion':'normal' if failure is None else 'abrupt','return_links_admissible':failure is None,'failure_site':failure,'dispatch_completed':dispatch_completed,
  'quarantine_called':quarantine_called,'quarantine_completed':quarantine_completed,'failed_or_interrupted_quarantine_effects':'UNKNOWN unless independently constructed reference path supplies them','events':events,'runtime_observation':False}

def state_value_projection(catalogue,case,validated):
 """Caller validates catalogue, evidence anchor and every symbol scope first."""
 need(type(case) is dict and set(case)=={'method','args','phase','live_reference','retired_reference','outcomes','underlying','run_result','wrapper_return'},'STATE-PROJECTION-FIELDS')
 need(type(case['method']) is str and case['method']==catalogue['source']['method'],'STATE-METHOD');same(case['args'],catalogue['source']['args'],'STATE-ARGS')
 need(type(case['phase']) is str and case['phase']==catalogue['source']['ready_phase'] and case['live_reference'] is not None and case['retired_reference'] is None,'STATE-READINESS')
 path=state_path_projection(catalogue,case['outcomes']);need(path['return_links_admissible'],'STATE-NO-NORMAL-RETURN')
 live=case['live_reference'];need(type(live) is dict and set(live)=={'kind','scope','symbol'} and live['kind']=='authority-reference' and type(live['symbol']) is str and bool(live['symbol']),'STATE-LIVE-SYMBOL')
 under=case['underlying'];need(type(under) is dict and set(under)=={'receiver','value','reference'},'STATE-UNDERLYING-FIELDS');same(under['receiver'],live,'STATE-DISPATCH-RECEIVER')
 ref=under['reference'];need(type(ref) is dict and set(ref)=={'kind','scope','symbol'} and ref['kind']=='state-result-reference' and type(ref['symbol']) is str and bool(ref['symbol']),'STATE-RESULT-SYMBOL')
 same(ref['scope'],live['scope'],'STATE-RESULT-SCOPE')
 values=[]
 for name in ('underlying','run_result','wrapper_return'):
  row=case[name];need(type(row) is dict and set(row)==({'receiver','value','reference'} if name=='underlying' else {'value','reference'}),'STATE-LINK-FIELDS:'+name)
  state_value_compare(catalogue,row['value'],validated);same(row['reference'],ref,'STATE-REFERENCE-FORWARDING:'+name);values.append({'link':name,'value':copy.deepcopy(row['value']),'reference':copy.deepcopy(ref)})
 return {'kind':'CONSTRUCTED-STATE-RETURN','path':path,'links':values,'copy_in_wrapper':False,'actual_object_identity_established':False,'runtime_observation':False}


def handle_source(raw,authority,anchor,observations,guards,oracle):
 common=state_source(raw,authority,observations,guards,oracle)
 tree,loc=_recovery_locations(raw,guards,oracle);at,aloc=_recovery_locations(authority,guards,oracle)
 cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority');w=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='handle')
 need(ast.unparse(w.args)=='self, packet, inject=None' and len(w.body)==1 and isinstance(w.body[0],ast.Return),'HANDLE-WRAPPER-SHAPE')
 call=w.body[0].value;same(ast.unparse(call),"self._run('handle', packet, inject)",'HANDLE-DISPATCH')
 ac=next(n for n in at.body if isinstance(n,ast.ClassDef) and n.name=='Authority');h=next(n for n in ac.body if isinstance(n,ast.FunctionDef) and n.name=='handle')
 same(ast.unparse(h.args),ast.unparse(w.args),'HANDLE-ARGUMENT-CORRESPONDENCE')
 returns=[n for n in ast.walk(h) if isinstance(n,ast.Return)];need(len(returns)==1 and ast.unparse(returns[0].value)=='raw','HANDLE-BACKEND-RETURN')
 tr=[n for n in h.body if isinstance(n,ast.Try)];need(len(tr)==1,'HANDLE-TRY-DOMAIN');tr=tr[0]
 need(not tr.orelse and not tr.finalbody and len(tr.handlers)==1 and ast.unparse(tr.handlers[0].type)=='Exception','HANDLE-EXCEPTION-CLASS')
 success=tr.body[-1];handler=tr.handlers[0];need(len(handler.body)==1,'HANDLE-ERROR-BODY');error=handler.body[0]
 for n,expected in [(success,"{'request': sha(packet), 'challenge': r['challenge'], 'ok': True, 'data': data}"),(error,"{'request': sha(packet), 'challenge': r['challenge'], 'ok': False, 'error': type(e).__name__ + ':' + str(e)}")]:
  need(isinstance(n,ast.Assign) and [ast.unparse(t) for t in n.targets]==['response'],'HANDLE-RESPONSE-ASSIGNMENT');same(ast.unparse(n.value),expected,'HANDLE-RESPONSE-ORIGIN')
 raws=[n for n in ast.walk(h) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='raw' for t in n.targets)];need(len(raws)==1,'HANDLE-RAW-WRITER');encode=raws[0]
 same(ast.unparse(encode.value),"enc({'response': response, 'signature': sig('server', response)})",'HANDLE-RAW-ORIGIN')
 idx=h.body.index(tr);need(idx>0 and isinstance(h.body[idx-1],ast.With),'HANDLE-RESERVATION-ORDER');reserve=h.body[idx-1]
 after=h.body[idx+1:];need(len(after)==4 and after[0] is encode and isinstance(after[1],ast.Expr) and isinstance(after[2],ast.With) and after[3] is returns[0],'HANDLE-POST-ORDER')
 same(ast.unparse(after[1]),"need(len(raw) <= RESPONSE_LIMIT, 'RESPONSE-BOUND')",'HANDLE-RESPONSE-BOUND')
 same(ast.unparse(after[2]),"with self.transaction():\n    self.db.execute('UPDATE journal SET response=? WHERE challenge=?', (raw, r['challenge']))",'HANDLE-PERSISTENCE')
 for n in (reserve,after[2]):same(ast.unparse(n.items[0].context_expr),'self.transaction()','HANDLE-TRANSACTION')
 same(ast.unparse(reserve.body[-1]),"self.db.execute('INSERT INTO journal VALUES(?,?,NULL)', (r['challenge'], packet))",'HANDLE-RESERVATION-BYTES')
 # Independent defining-source structure includes every request and action guard.
 auth_prefix=h.body[:idx-1];need(bool(auth_prefix),'HANDLE-AUTH-PREFIX')
 allconst={}
 for n in at.body:
  if isinstance(n,ast.Assign):
   for t in n.targets:
    if isinstance(t,ast.Name) and t.id in ('VERSION','REQUEST_LIMIT','RESPONSE_LIMIT'):allconst[t.id]=ast.literal_eval(n.value)
 need(set(allconst)=={'VERSION','REQUEST_LIMIT','RESPONSE_LIMIT'},'HANDLE-SOURCE-CONSTANTS')
 encnode=next(n for n in ast.parse(anchor).body if isinstance(n,ast.FunctionDef) and n.name=='enc')
 same(ast.unparse(encnode),"def enc(x):\n    return (json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\\n').encode()",'HANDLE-ENC-BYTES')
 obs=ast.parse(observations);edge=next(n for n in obs.body if isinstance(n,ast.FunctionDef) and n.name=='source_edges')
 helpers=[n for n in edge.body if isinstance(n,ast.FunctionDef) and n.name in ('exact_bytes','decode','signature')];need(len(helpers)==3,'HANDLE-AUTH-HELPERS')
 authloop=[n for n in edge.body if isinstance(n,ast.For) and "'Authority.handle'" in ast.unparse(n) and "'RETURN-REQUEST'" in ast.unparse(n)];need(len(authloop)==1,'HANDLE-EXISTING-AUTH-CHECK')
 stages={'authenticate':[aloc(n) for n in auth_prefix],'reserve':aloc(reserve),'action':[aloc(n) for n in tr.body[:-1]],'success_response':aloc(success),'error_response':aloc(error),'encode_sign':aloc(encode),'response_bound':aloc(after[1]),'persist':aloc(after[2]),'return_raw':aloc(returns[0])}
 return {'source':common['source'],'authority_source':common['authority_source'],'anchor_source':{'bytes':len(anchor),'sha256':digest(anchor)},'observation_source':{'bytes':len(observations),'sha256':digest(observations)},
  'wrapper':loc(w),'wrapper_return':loc(w.body[0]),'wrapper_call':loc(call),'method':ast.literal_eval(call.args[0]),'parameter_names':[a.id for a in call.args[1:]],'default_inject':ast.literal_eval(w.args.defaults[0]),
  'run_source':{k:copy.deepcopy(common[k]) for k in ('source','run','readiness_program','readiness_call','ready_phase','try_region','handler','stages','normal_path','caught_stages','outside_handler','result_local','result_assignment','run_return','dispatch','dispatch_receiver')},'backend':aloc(h),'backend_return':aloc(returns[0]),'response_assignments':{'success':aloc(success),'error':aloc(error)},'raw_assignment':aloc(encode),'backend_stages':stages,'constants':allconst,
  'backend_program':ast.dump(h,include_attributes=False),'encoder':ast.get_source_segment(anchor.decode(),encnode),'auth_helper_programs':{n.name:ast.get_source_segment(observations.decode(),n) for n in helpers},'auth_check_program':ast.get_source_segment(observations.decode(),authloop[0]),
  'meaning':'Exact canonical signed response bytes, not decoded/re-encoded substitutes. Inner Exception may yield normal ok:false; uncaught BaseException and failures outside the inner try escape. A response is not proof of external nonexecution, renewed authorization or complete action semantics.'}

def compile_handle_return(raw,authority,anchor,observations,model,producer,guards,oracle,references):
 source=handle_source(raw,authority,anchor,observations,guards,oracle);validate_reference_transfers(raw,model,producer,guards,oracle,authority,references)
 names=['PACKET:','PACKET:#exact_bytes','REQUEST:','RESPONSE:','RESPONSE:#exact_bytes','SUCCESS-RESPONSE:','ERROR-RESPONSE:'];decl={n:[d for d in model['existing_declarations'] if d['template_id']==n] for n in names};need(all(len(v)==1 for v in decl.values()),'HANDLE-EXISTING-DECLARATIONS');decl={k:copy.deepcopy(v[0]) for k,v in decl.items()}
 ds=[d for d in producer['delegations'] if d['from']=='ManagedAuthority.handle -> _run'];need(len(ds)==1 and ds[0]['to']=='Authority.handle -> apply/sign and response persistence','HANDLE-DELEGATION')
 inv={r['site']:r for r in producer['source_inventory']['sites']}
 for r in (source['wrapper_return'],source['wrapper_call'],source['run_source']['result_assignment'],source['run_source']['run_return']):need(r['site'] in inv and r['guards']==inv[r['site']]['guards'],'HANDLE-GUARD-COVERAGE')
 origins=[source['backend_return'],source['run_source']['result_assignment'],source['wrapper_return']]
 return {'format':'I164-MANAGED-HANDLE-RETURN-1','source':source,'delegation':copy.deepcopy(ds[0]),'inherited_declarations':decl,'reference_links':copy.deepcopy(compile_state_return(raw,authority,observations,model,producer,guards,oracle,references)['reference_links']),
  'declarations':[{'id':n,'type':copy.deepcopy(decl['RESPONSE:#exact_bytes']['native_template']['type']),'logical_type':'exact Python bytes','representation':'retained bytes_hex lowercase exact hex; not decoded JSON','origin':copy.deepcopy(o),'classification':'UNKNOWN','ordinal':None,'multiplicity':None} for n,o in zip(['underlying-response','run-result','wrapper-return'],origins)],
  'links':[{'from':'underlying-response','to':'run-result','guard':'backend normal completion; same source result reference'},{'from':'run-result','to':'wrapper-return','guard':'_run normal completion including lock exit; same source result reference'}],
  'arguments':{'wrapper_to_run':['method literal handle','packet','inject including default None'],'run_to_backend':['packet','inject'],'missing_observations':'UNAVAILABLE; None is not an unknown inject value'},'runtime_links':None,'actual_admission':False,'complete_repetition_coverage':False}

def validate_handle_return(raw,authority,anchor,observations,model,producer,guards,oracle,references,submitted):
 same(submitted,compile_handle_return(raw,authority,anchor,observations,model,producer,guards,oracle,references),'HANDLE-SOURCE-CATALOGUE');return True

def handle_authentication(authority,anchor,observations):
 """Reuse exact retained offline verification primitives and pair-check loop.
 Only public-key derivation runs; no sig(), runtime application or session call.
 """
 a=ast.parse(authority);o=ast.parse(observations);an=ast.parse(anchor)
 public=next(n for n in a.body if isinstance(n,ast.FunctionDef) and n.name=='public')
 assignments=[n for n in a.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('VERSION','SEEDS','PUB') for t in n.targets)]
 encnode=next(n for n in an.body if isinstance(n,ast.FunctionDef) and n.name=='enc');edge=next(n for n in o.body if isinstance(n,ast.FunctionDef) and n.name=='source_edges')
 helpers=[n for n in edge.body if isinstance(n,ast.FunctionDef) and n.name in ('exact_bytes','decode','signature')]
 loop=next(n for n in edge.body if isinstance(n,ast.For) and "'Authority.handle'" in ast.unparse(n) and "'RETURN-REQUEST'" in ast.unparse(n))
 from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey,Ed25519PublicKey
 from cryptography.hazmat.primitives import serialization
 env={'hashlib':hashlib,'json':json,'need':need,'same':same,'Ed25519PrivateKey':Ed25519PrivateKey,'Ed25519PublicKey':Ed25519PublicKey,'serialization':serialization,'mc':type('DigestOnly',(),{'digest':staticmethod(digest)})}
 setup=ast.Module(body=[encnode,public,*assignments],type_ignores=[]);exec(compile(ast.fix_missing_locations(setup),'<retained-public-verification-primitives>','exec'),env)
 env['version']=env['VERSION'];env['pub']={k:v.hex() for k,v in env['PUB'].items()}
 init=ast.parse("frames={1:{'call':{'function':'Authority.handle','arguments':{'packet':packet}},'normal':True,'return':{'value':returned}}}").body
 fn=ast.FunctionDef(name='pair',args=ast.arguments(posonlyargs=[],args=[ast.arg(arg='packet'),ast.arg(arg='returned')],kwonlyargs=[],kw_defaults=[],defaults=[]),body=init+[loop,ast.Return(value=ast.Tuple(elts=[ast.Name(id='request',ctx=ast.Load()),ast.Name(id='r',ctx=ast.Load())],ctx=ast.Load()))],decorator_list=[])
 exec(compile(ast.fix_missing_locations(ast.Module(body=helpers+[fn],type_ignores=[])),'<retained-handle-pair-check>','exec'),env)
 return {'pair':env['pair'],'exact_bytes':env['exact_bytes'],'signature':env['signature'],'public_keys':copy.deepcopy(env['pub']),'version':env['VERSION']}

def handle_pair(catalogue,verification,packet,response,instance):
 """Exact bytes preserved. Context is independently validated by caller."""
 p=verification['exact_bytes'](packet);b=verification['exact_bytes'](response);const=catalogue['source']['constants'];need(len(p)<=const['REQUEST_LIMIT'] and len(b)<=const['RESPONSE_LIMIT'],'HANDLE-BYTE-BOUND')
 request,r=verification['pair'](packet,response)
 need(set(request)=={'version','binding','pilot','session','principal','challenge','expected','method','u','body'},'HANDLE-REQUEST-FIELDS')
 same(request['version'],const['VERSION'],'HANDLE-VERSION')
 for k in ('binding','pilot','session'):same(request[k],instance[k],'HANDLE-INSTANCE:'+k)
 need(request['principal'] in ('executor','observer') and ((request['method']=='observe')==(request['principal']=='observer')),'HANDLE-ROLE')
 need(all(type(request[k]) is str and len(request[k])==64 and all(c in '0123456789abcdef' for c in request[k]) for k in ('challenge','expected')),'HANDLE-DIGEST')
 need(type(request['u']) is str and 0<len(request['u'])<=128 and type(request['body']) is dict,'HANDLE-REQUEST-TYPE')
 need(type(r['ok']) is bool and (r['ok'] or type(r['error']) is str),'HANDLE-ERROR-TYPE')
 return {'packet':{'bytes_hex':p.hex()},'response':{'bytes_hex':b.hex()},'request':copy.deepcopy(request),'envelope_response':copy.deepcopy(r),'response_ok':r['ok'],'authentication':'retained laboratory verification only','action_semantics_proven':False,'external_nonexecution_established':False,'authorization_renewed':False}

def handle_backend_path(catalogue,outcomes):
 need(type(outcomes) is dict,'HANDLE-BACKEND-OUTCOMES');used=[];events=[];escaped=None;ok=None
 def take(name):
  need(name in outcomes and type(outcomes[name]) is str and outcomes[name] in ('normal','Exception','BaseException','process-termination'),'HANDLE-BACKEND-OUTCOME:'+name);used.append(name);v=outcomes[name];events.append({'stage':name,'source':copy.deepcopy(catalogue['source']['backend_stages'][name]),'outcome':v});return v
 for name in ('authenticate','reserve'):
  v=take(name)
  if v!='normal':escaped=v;break
 if escaped is None:
  for name in ('action','success_response'):
   v=take(name)
   if v!='normal':break
  if v=='Exception':
   v=take('error_response')
   if v=='normal':ok=False
   else:escaped=v
  elif v!='normal':escaped=v
  else:ok=True
 if escaped is None:
  for name in ('encode_sign','response_bound','persist','return_raw'):
   v=take(name)
   if v!='normal':escaped=v;break
 need(set(used)==set(outcomes),'HANDLE-BACKEND-UNREACHED')
 return {'kind':'CONSTRUCTED-BACKEND-PATH','completion':'normal' if escaped is None else 'process-termination' if escaped=='process-termination' else 'escaping-exception','escaped_class':escaped,'response_ok':ok if escaped is None else None,'events':events,'effects_on_failure':'UNKNOWN; charges, journal reservations, signing/release and recovery uncertainty remain','runtime_observation':False}

def handle_value_projection(catalogue,verification,case,validated):
 """Conditional component relation; validated must come from independent input.
 Production semantic/derive never obtain expectations from a submitted case.
 """
 fields={'occurrence','scope','arguments','run_arguments','backend_arguments','backend_outcomes','run_outcomes','underlying','run_result','wrapper_return'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==fields,'HANDLE-PROJECTION-FIELDS')
 for k in ('occurrence','scope','arguments','backend_outcomes','run_outcomes'):same(case[k],validated[k],'HANDLE-PREMISE:'+k)
 need(type(case['occurrence']) is str and bool(case['occurrence']),'HANDLE-OCCURRENCE')
 args=case['arguments'];need(type(args) is dict and set(args)=={'packet','inject'},'HANDLE-ARGUMENTS')
 same(case['run_arguments'],{'method':catalogue['source']['method'],'args':[args['packet'],args['inject']]},'HANDLE-RUN-ARGUMENTS');same(case['backend_arguments'],args,'HANDLE-BACKEND-ARGUMENTS')
 backend=handle_backend_path(catalogue,case['backend_outcomes']);run=state_path_projection({'source':catalogue['source']['run_source']},case['run_outcomes'])
 dispatched=any(e['stage']=='dispatch' for e in run['events']);need(dispatched,'HANDLE-CONSTRUCTED-DISPATCH-PREMISE')
 need(backend['completion']!='process-termination','HANDLE-NO-PYTHON-UNWIND-FOR-PROCESS-TERMINATION')
 need(case['run_outcomes']['dispatch']==('normal' if backend['completion']=='normal' else 'raise'),'HANDLE-DISPATCH-OUTCOME')
 links=[];pair=None
 for name in ('underlying','run_result','wrapper_return'):
  row=case[name];expected=validated[name]
  available=backend['completion']=='normal' if name in ('underlying','run_result') else run['completion']=='normal'
  if not available:need(row is None and expected is None,'HANDLE-NO-RETURN:'+name);continue
  need(type(row) is dict and type(expected) is dict and set(row)==set(expected)=={'value','reference'},'HANDLE-LINK-FIELDS:'+name)
  b=verification['exact_bytes'](row['value']);want=verification['exact_bytes'](expected['value']);need(b==want,'HANDLE-EXACT-RESPONSE:'+name);same(row['reference'],expected['reference'],'HANDLE-REFERENCE:'+name)
  if pair is None:
   pair=handle_pair(catalogue,verification,args['packet'],row['value'],case['scope']['instance']);need(pair['response_ok'] is backend['response_ok'],'HANDLE-SUCCESS-ERROR-GUARD')
  else:need(b==bytes.fromhex(pair['response']['bytes_hex']),'HANDLE-FORWARDING-BYTES');same(row['reference'],case['underlying']['reference'],'HANDLE-FORWARDING-REFERENCE')
  links.append({'id':case['occurrence']+'/'+name,'declaration':{'underlying':'underlying-response','run_result':'run-result','wrapper_return':'wrapper-return'}[name],'value':{'bytes_hex':b.hex()},'reference':copy.deepcopy(row['reference']),'occurrence':case['occurrence']})
 return {'kind':'CONSTRUCTED-HANDLE-RETURN','occurrence':case['occurrence'],'scope':copy.deepcopy(case['scope']),'arguments':copy.deepcopy(args),'backend':backend,'run':run,'links':links,'verified_pair':pair,'runtime_observation':False,'physical_object_identity_established':False,'external_nonexecution_established':False,'authorization_renewed':False,'admission':False}


def _client_locate(raw):
 tree=ast.parse(raw);parents={};text=raw.decode()
 for p in ast.walk(tree):
  for field,value in ast.iter_fields(p):
   for i,n in enumerate(value if isinstance(value,list) else [value]):
    if isinstance(n,ast.AST):parents[n]=(p,field,i if isinstance(value,list) else None)
 def basic(n):return {'site':f'{n.lineno}:{n.col_offset}:{n.end_lineno}:{n.end_col_offset}:{type(n).__name__}','expression':ast.get_source_segment(text,n)}
 def loc(n):
  row=basic(n);child=n;gs=[];prefix=[]
  while child in parents and not isinstance(child,ast.FunctionDef):
   p,f,i=parents[child]
   if isinstance(p,ast.If):gs.append({'kind':'if','test':basic(p.test),'arm':f})
   elif isinstance(p,ast.Try):gs.append({'kind':'try','region':f,'handlers':[ast.unparse(h.type) for h in p.handlers]})
   elif isinstance(p,ast.ExceptHandler):gs.append({'kind':'handler','type':ast.unparse(p.type),'binding':p.name})
   elif isinstance(p,ast.With):gs.append({'kind':'with','contexts':[ast.unparse(x.context_expr) for x in p.items]})
   elif isinstance(p,(ast.For,ast.While)):gs.append({'kind':type(p).__name__,'source':basic(p),'region':f})
   if i is not None and isinstance(child,ast.stmt):prefix.append({'owner':basic(p),'region':f,'normal_prefix':[basic(x) for x in getattr(p,f)[:i] if isinstance(x,ast.stmt)]})
   child=p
  row.update(guards=list(reversed(gs)),continuation=list(reversed(prefix)));return row
 return tree,loc

def client_handle_source(launcher,entry,manager):
 """Independent defining-source traversal, never a generated coverage oracle."""
 lt,ll=_client_locate(launcher);et,el=_client_locate(entry)
 def method(tree,cls,name):
  owner=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==cls) if cls else tree
  return next(n for n in owner.body if isinstance(n,ast.FunctionDef) and n.name==name)
 def shape(n,expected):
  def cleaned(fn):
   fn=copy.deepcopy(fn)
   if fn.body and isinstance(fn.body[0],ast.Expr) and isinstance(fn.body[0].value,ast.Constant) and type(fn.body[0].value.value) is str:fn.body.pop(0)
   return ast.dump(fn,include_attributes=False)
  same(cleaned(n),cleaned(ast.parse(expected).body[0]),'CLIENT-DEFINING-SHAPE:'+n.name)
 session_init=method(lt,'ManagedSession','__init__');session=method(lt,'ManagedSession','handle')
 client_init=method(et,'Client','__init__');client=method(et,'Client','handle');owner=method(et,'_Owner','__init__');dispatch=method(et,None,'_dispatch');fail=method(et,None,'_fail');run=method(et,None,'_run');general=method(et,None,'run');launch=method(lt,None,'_session')
 shape(session_init,'def __init__(self, managed): self.__managed=managed')
 shape(session,'def handle(self, authenticated_packet): return self.__managed.handle(authenticated_packet)')
 shape(client_init,'def __init__(self, token): self.__token=token')
 shape(client,"def handle(self, authenticated_packet): return _dispatch(self.__token, 'handle', authenticated_packet)")
 shape(owner,'def __init__(self, wrapper):\n self.wrapper=wrapper\n self.failure=None')
 shape(dispatch,"""def _dispatch(token, operation, packet):
 owner = _OWNERS.get(token)
 if owner is None or owner.failure is not None: _fail()
 try:
  if operation == 'handle':
   if type(packet) is not bytes: raise TypeError('PACKET-BYTES')
   result = owner.wrapper.handle(packet)
   if type(result) is not bytes: raise TypeError('RESPONSE-BYTES')
   return result
  if operation != 'state': raise RuntimeError('CLIENT-OPERATION')
  result = owner.wrapper.state()
  if type(result) is not dict or set(result) != _STATE_KEYS: raise RuntimeError('STATE-SHAPE')
  return _data(result)
 except BaseException as error: owner.failure = error
 _fail()
""")
 shape(fail,"def _fail(): raise ClientFailure('MANAGED-OPERATION-UNAVAILABLE; outcome uncertain; no renewed authorization') from None")
 shape(run,"""def _run(launcher, candidate, draft, runtime, destination, client, create, control):
 failed=False
 try:
  with launcher.session(candidate,draft,runtime,destination,create=create) as wrapper:
   owner=_Owner(wrapper)
   token=object()
   _OWNERS[token]=owner
   try:
    if control is not None: control(_Control(token))
    try: client(Client(token))
    except BaseException as client_error:
     if owner.failure is not None: raise owner.failure from client_error
     raise
    if owner.failure is not None: raise owner.failure
   finally: _OWNERS.pop(token,None)
 except BaseException: failed=True
 if failed: _fail()
""")
 shape(general,"""def run(candidate,draft,runtime,destination,client,*,create=False):
 failed=False
 try: launcher=_load_launcher()
 except BaseException: failed=True
 if failed: _fail()
 return _run(launcher,candidate,draft,runtime,destination,client,create,None)
""")
 # Exact existing exception-retention/cleanup body; no new sink is introduced.
 tr=launch.body[-1].body[-1];need(isinstance(tr,ast.Try) and len(tr.handlers)==1,'CLIENT-LAUNCHER-TRY')
 handler=tr.handlers[0];same(ast.unparse(handler.type),'BaseException','CLIENT-LAUNCHER-HANDLER')
 expected=ast.parse("""try: pass
except BaseException as e:
 details={'error':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'nonexecution_established':False,'new_authorization':False,'cleanup':[]}
 for name,obj in [('raw',raw),('managed',managed)]:
  if obj is not None:
   try: obj.close();details['cleanup'].append([name,'close returned'])
   except BaseException as close_error: details['cleanup'].append([name,type(close_error).__name__,str(close_error)])
 try: write_new(dest/'evidence'/('failure-'+str(os.getpid())+'-'+str(len(list((dest/'evidence').iterdir())))+'.json'),details)
 except BaseException: pass
 raise
""").body[0].handlers[0]
 same(ast.dump(handler,include_attributes=False),ast.dump(expected,include_attributes=False),'CLIENT-RETENTION-SOURCE')
 # Last normal statement removes ACTIVE only after normal managed close.
 same([ast.unparse(n) for n in tr.body[-4:]],["yield ManagedSession(managed)","managed.close()","managed = None","(dest / 'ACTIVE.json').unlink()"],'CLIENT-NORMAL-CLEANUP')
 clients=next(n for n in et.body if isinstance(n,ast.ClassDef) and n.name=='Client')
 public=[n.name for n in clients.body if isinstance(n,ast.FunctionDef) and not n.name.startswith('_')];same(public,['state','handle'],'CLIENT-PUBLIC-SURFACE')
 same(manager['source']['method'],'handle','CLIENT-MANAGER-SELECTOR');need(manager['source']['wrapper_return']['expression'].startswith('return '),'CLIENT-MANAGER-RETURN')
 handle_branch=dispatch.body[2].body[0];dh=dispatch.body[2].handlers[0]
 selected=[('session-init',launcher,ll,session_init),('session-handle',launcher,ll,session),('client-init',entry,el,client_init),('client-handle',entry,el,client),('owner-init',entry,el,owner),('dispatch',entry,el,dispatch),('fixed-failure',entry,el,fail),('owner-route',entry,el,run),('general-entry',entry,el,general),('launcher-error',launcher,ll,handler)]
 anchors={n:dict(loc(node),source={'bytes':len(raw),'sha256':digest(raw)},ast=ast.dump(node,include_attributes=False)) for n,raw,loc,node in selected}
 stages={'client-call':el(client.body[0]),'owner-lookup':el(dispatch.body[0]),'owner-guard':el(dispatch.body[1]),'packet-check':el(handle_branch.body[0]),'session-call':el(handle_branch.body[1]),'manager-call':ll(session.body[0]),'session-return':ll(session.body[0]),'response-check':el(handle_branch.body[2]),'dispatch-return':el(handle_branch.body[3]),'client-return':el(client.body[0]),'retain-error':el(dh.body[0]),'fixed-failure':el(fail.body[0]),'owner-route':el(run),'launcher-error':ll(handler)}
 return {'sources':{'launcher':{'bytes':len(launcher),'sha256':digest(launcher)},'entry':{'bytes':len(entry),'sha256':digest(entry)}},'anchors':anchors,'stages':stages,'client_method':client.name,'operation':client.body[0].value.args[1].value,'default_inject':copy.deepcopy(manager['source']['default_inject']),
  'packet_guard':ast.unparse(handle_branch.body[0].test),'response_guard':ast.unparse(handle_branch.body[2].test),'caught_class':ast.unparse(dh.type),'fixed_failure':{'type':fail.body[0].exc.func.id,'message':fail.body[0].exc.args[0].value,'explicit_cause':ast.literal_eval(fail.body[0].cause),'suppress_context':True},
  'packet_type_error':handle_branch.body[0].body[0].exc.args[0].value,'response_type_error':handle_branch.body[2].body[0].exc.args[0].value,'public_methods':public,
  'limits':['Trusted exact owners and unmodified builtins; no arbitrary Python introspection or hostile monkeypatch protection','No guarantee that _fail construction, outside-try lookup, interruption, error formatting, cleanup or evidence I/O succeeds','from None suppresses displayed context; no blanket absence of ambient caller exception/context or traceback object access','No runtime forwarding or callback trace supplied by a source anchor']}

def compile_client_handle(launcher,entry,manager,boundary):
 source=client_handle_source(launcher,entry,manager)
 wanted=['client-handle','dispatch-and-failure','owner-routing','general-entry','launcher-diagnostic-and-evidence']
 sites={s['id']:s for s in boundary['sites']}
 need(all(n in sites for n in wanted),'CLIENT-BOUNDARY-SITES')
 for n in wanted:
  pin=source['sources']['launcher' if n.startswith('launcher') else 'entry'];same({k:sites[n]['anchor'][k] for k in pin},pin,'CLIENT-BOUNDARY-SOURCE')
 ds={d['id']:d for d in manager['declarations']};need('wrapper-return' in ds,'CLIENT-MANAGER-DECLARATION')
 values=['session-return','dispatch-result','dispatch-return','client-return']
 return {'format':'I164-CLIENT-HANDLE-STATIC-2','source':source,'manager_relation':copy.deepcopy(manager),'boundary_contract':copy.deepcopy(boundary['contract']),'boundary_sites':[copy.deepcopy(sites[n]) for n in wanted],
  'declarations':[{'id':n,'type':copy.deepcopy(ds['wrapper-return']['type']),'logical_type':'exact Python bytes','representation':'lowercase bytes_hex; no decoded/re-encoded replacement','classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in values],
  'ordered_hops':['manager-return',*values],'arguments':[{'from':'Client.handle','to':'_dispatch','method':'handle','args':['client token','authenticated_packet']},{'from':'_dispatch','to':'ManagedSession.handle','args':['packet']},{'from':'ManagedSession.handle','to':'ManagedAuthority.handle','args':['authenticated_packet'],'inject':'source default None, not an observed value'}],
  'reference_edges':[['client.token','token'],['owners[token]','owner'],['owner.wrapper','session'],['session.managed','manager']],'required_destinations':{'response':'calling general client only; not automatic stdout/stderr/status publication','original_error':'owner.failure then existing trusted launcher error/cleanup route conditional on continuation','fixed_failure':'general client or outer run caller','failure_record':'existing launcher evidence/failure-*.json only; best effort, exact bytes unavailable without observation'},
  'outside_catch_failure_contract':{'version':'I164-CLIENT-TERMINAL-CLASSIFICATION-1','true_iff':'terminal unexpected modeled raise outside _dispatch protected region','false_is_not':'no exception, inside catch, no earlier effects, no pending error or permission to continue','intentional_fixed_raise_is_separate':True,'location_is_separate_from_outcome':True,'runtime_evidence_supplied':False},
  'runtime_links':None,'runtime_call_count':None,'complete_repetition_coverage':False,'actual_admission':False}

def validate_client_handle(launcher,entry,manager,boundary,submitted):
 same(submitted,compile_client_handle(launcher,entry,manager,boundary),'CLIENT-SOURCE-CORRESPONDENCE');return True

def _client_outcome_classification(catalogue,events,completion):
 """Classify the TERMINAL modeled stage relative to _dispatch's own catch.
 A source-intended fixed ClientFailure is not an unexpected stage failure.
 No classification here supplies runtime exception, unwind or retention evidence.
 """
 need(type(events) is list and bool(events),'CLIENT-CLASSIFICATION-EVENTS')
 terminal=events[-1];stage=terminal['stage'];source=catalogue['source']['stages'][stage]
 same(terminal['source'],source,'CLIENT-CLASSIFICATION-SOURCE')
 kinds={'normal':'normal-return','fixed-client-failure':'intentional-fixed-raise','unqualified-escape':'unexpected-raise','process-termination':'process-termination'}
 need(completion in kinds,'CLIENT-CLASSIFICATION-COMPLETION');kind=kinds[completion]
 expected='raise' if kind=='unexpected-raise' else 'process-termination' if kind=='process-termination' else 'normal'
 same(terminal['outcome'],expected,'CLIENT-CLASSIFICATION-OUTCOME')
 def protected(node):return any(g['kind']=='try' and g['region']=='body' and 'BaseException' in g['handlers'] for g in node['guards'])
 if stage in ('client-call','client-return'):location='caller-outside-dispatch';inside=False
 elif stage in ('owner-lookup','owner-guard'):location='dispatch-before-try';inside=False;need(not protected(source),'CLIENT-PREFIX-PROTECTION')
 elif stage=='retain-error':
  location='dispatch-handler-body';inside=False
  need(any(g['kind']=='handler' and g['type']=='BaseException' for g in source['guards']),'CLIENT-HANDLER-LOCATION')
 elif stage=='fixed-failure':location='fixed-helper-outside-protected-region';inside=False
 elif stage in ('manager-call','session-return'):
  location='callee-under-dispatch-protected-call';inside=True;need(protected(catalogue['source']['stages']['session-call']),'CLIENT-CALLEE-PROTECTION')
 else:location='dispatch-protected-try';inside=True;need(protected(source),'CLIENT-TRY-LOCATION')
 if kind=='normal-return':need(stage=='client-return','CLIENT-NORMAL-TERMINAL')
 if kind=='intentional-fixed-raise':need(stage=='fixed-failure','CLIENT-FIXED-TERMINAL')
 return {'contract':'I164-CLIENT-TERMINAL-CLASSIFICATION-1','stage':stage,'stage_outcome':terminal['outcome'],'modeled_kind':kind,'source':copy.deepcopy(source),
  'location_relative_to_dispatch_catch':location,'python_raise_protected_by_dispatch_catch':inside,
  'unexpected_raise_outside_dispatch_catch':kind=='unexpected-raise' and not inside,
  'terminal_python_exception_in_model':None if kind=='process-termination' else kind in ('unexpected-raise','intentional-fixed-raise'),
  'runtime_python_exception_evidence':'UNAVAILABLE','runtime_python_unwind_evidence':'UNAVAILABLE',
  'retention_cleanup_or_authority_established_by_classification':False}

def client_handle_projection(catalogue,verification,case,validated):
 """Conditional source interpreter; validated is an independent premise, not
 an admission certificate. Full validation rebuilds actual evidence separately.
 """
 keys={'occurrence','scope','references','packet','outcomes','manager_case','callback','cleanup'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'CLIENT-CASE-FIELDS')
 for k in keys-{'manager_case'}:same(case[k],validated[k],'CLIENT-PREMISE:'+k)
 need(type(case['occurrence']) is str and bool(case['occurrence']),'CLIENT-OCCURRENCE')
 scope=case['scope'];need(type(scope) is dict and set(scope)=={'context','acquisition','instance','recovery_frontier'},'CLIENT-SCOPE')
 need(scope['context'] in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'),'CLIENT-CONTEXT')
 refs=case['references'];required={'client','token','owner','session','manager','client.token','owners[token]','owner.wrapper','session.managed','owner_failed'}
 need(type(refs) is dict and set(refs)==required and type(refs['owner_failed']) is bool,'CLIENT-REFERENCES')
 for n in ('client','token','owner','session','manager'):
  r=refs[n];need(type(r) is dict and set(r)=={'scope','symbol'} and type(r['symbol']) is str and bool(r['symbol']),'CLIENT-REFERENCE-TYPE');same(r['scope'],scope,'CLIENT-REFERENCE-SCOPE')
 for a,b in catalogue['reference_edges']:
  if a=='owners[token]' and refs[a] is None:continue
  same(refs[a],refs[b],'CLIENT-REFERENCE-EDGE:'+a)
 packet=case['packet'];need(type(packet) is dict and set(packet)=={'type','value'},'CLIENT-PACKET-REPRESENTATION')
 need(packet['type'] in ('bytes','str','int','NoneType'),'CLIENT-PACKET-DOMAIN')
 if packet['type']=='bytes':verification['exact_bytes'](packet['value'])
 else:need(type(packet['value']) is {'str':str,'int':int,'NoneType':type(None)}[packet['type']],'CLIENT-PACKET-TYPE')
 outcomes=case['outcomes'];need(type(outcomes) is dict,'CLIENT-OUTCOMES');used=set();events=[];hops=[];arguments=[];dest=[];original=None;fixed=None;manager_result=None;completion='pending';retained=False
 def step(n):
  need(n in outcomes and outcomes[n] in ('normal','raise','process-termination'),'CLIENT-OUTCOME:'+n);used.add(n);v=outcomes[n];events.append({'stage':n,'source':copy.deepcopy(catalogue['source']['stages'][n]),'outcome':v});return v
 def link(n,row):hops.append({'id':case['occurrence']+'/'+n,'declaration':n,'value':copy.deepcopy(row['value']),'reference':copy.deepcopy(row['reference']),'scope':copy.deepcopy(scope)})
 def fail_fixed():
  nonlocal fixed,completion
  result=step('fixed-failure')
  if result=='normal':fixed=copy.deepcopy(catalogue['source']['fixed_failure']);completion='fixed-client-failure';dest.append({'kind':'fixed-failure','to':'general-client','value':copy.deepcopy(fixed)})
  else:completion='unqualified-escape' if result=='raise' else 'process-termination'
 def outer(n):
  nonlocal completion
  v=step(n)
  if v!='normal':completion='unqualified-escape' if v=='raise' else v;return False
  return True
 # Lookup and its guard precede the catch. They cannot be advertised as caught.
 entered=outer('client-call')
 if entered:arguments.append({'id':case['occurrence']+'/client-to-dispatch','to':'_dispatch','token':copy.deepcopy(refs['token']),'operation':catalogue['source']['operation'],'packet':copy.deepcopy(packet)})
 entered=entered and outer('owner-lookup') and outer('owner-guard')
 if entered and (refs['owners[token]'] is None or refs['owner_failed']):fail_fixed()
 elif entered:
  for stage in ('packet-check','session-call','manager-call','session-return','response-check','dispatch-return','client-return'):
   v=step(stage)
   # Client.handle's return is outside _dispatch's handler.
   if v!='normal':
    if v=='process-termination':completion=v;break
    if stage=='client-return':completion='unqualified-escape';break
    original={'kind':'conditional-exception','origin':stage,'catch_family':'BaseException','exact_type':None,'reference':case['occurrence']+'/error'};break
   if stage=='packet-check' and packet['type']!='bytes':original={'kind':'source-TypeError','origin':stage,'type':'TypeError','message':catalogue['source']['packet_type_error'],'reference':case['occurrence']+'/error'};break
   if stage=='session-call':arguments.append({'id':case['occurrence']+'/dispatch-to-session','to':'ManagedSession.handle','receiver':copy.deepcopy(refs['session']),'packet':copy.deepcopy(packet)})
   if stage=='manager-call':
    mc=case['manager_case'];mv=validated['manager_case'];need(mc is not None and mv is not None,'CLIENT-MANAGER-PREMISE')
    same(mc['scope'],scope,'CLIENT-MANAGER-SCOPE');same(mc['arguments'],{'packet':packet['value'],'inject':None},'CLIENT-MANAGER-ARGUMENTS')
    same(mc['occurrence'],case['occurrence']+'/managed-handle','CLIENT-MANAGER-OCCURRENCE')
    arguments.append({'id':case['occurrence']+'/session-to-manager','to':'ManagedAuthority.handle','receiver':copy.deepcopy(refs['manager']),'packet':copy.deepcopy(packet),'inject':None,'inject_basis':'source default; constructed, not observed'})
    manager_result=handle_value_projection(catalogue['manager_relation'],verification,mc,mv)
    if manager_result['run']['completion']!='normal':original={'kind':'manager-escaping-exception','origin':stage,'catch_family':'BaseException','exact_type':None,'reference':case['occurrence']+'/error'};break
    row=mc['wrapper_return'];verification['exact_bytes'](row['value']);link('manager-return',row)
   elif stage=='session-return':
    need(manager_result is not None and manager_result['run']['completion']=='normal','CLIENT-SESSION-RETURN-PREMISE');link('session-return',case['manager_case']['wrapper_return']);link('dispatch-result',case['manager_case']['wrapper_return'])
   elif stage=='response-check':
    # A conforming pinned manager returns exact bytes. A wrong type here is an
    # unsupported substitution, not a fabricated legitimate manager execution.
    need(hops and type(hops[-1]['value']) is dict,'CLIENT-RESPONSE-PREMISE');verification['exact_bytes'](hops[-1]['value'])
   elif stage=='dispatch-return':link('dispatch-return',case['manager_case']['wrapper_return'])
   elif stage=='client-return':link('client-return',case['manager_case']['wrapper_return']);completion='normal';dest.append({'kind':'exact-response-bytes','to':'general-client','value':copy.deepcopy(hops[-1]['value'])})
  if original is not None:
   v=step('retain-error')
   if v=='normal':retained=True;dest.append({'kind':'original-exception-reference','to':'owner.failure','reference':original['reference']});fail_fixed()
   else:completion='unqualified-escape' if v=='raise' else v;retained=None
 if manager_result is None:need(case['manager_case'] is None and validated['manager_case'] is None,'CLIENT-UNREACHED-MANAGER')
 need(used==set(outcomes),'CLIENT-UNREACHED-OUTCOME')
 callback=case['callback'];need(callback in ('returns','raises','unobserved'),'CLIENT-CALLBACK')
 cleanup=case['cleanup'];need(type(cleanup) is dict and set(cleanup)=={'revoke','format','cleanup','write','outer_fail'},'CLIENT-CLEANUP-FIELDS')
 need(all(v in ('normal','raise','unobserved') for v in cleanup.values()),'CLIENT-CLEANUP-OUTCOME')
 evidence={'original_reraised_to_launcher':None,'reference':None,'explicit_cause':'unobserved','retention':'UNESTABLISHED','bytes':None,'cleanup_obligations':'UNCHANGED','cleanup_premise':'normal means iteration/error-detail handling completed, not successful closure of every connection','active_marker_removal':'not established by this relation'}
 if retained and completion=='fixed-client-failure' and callback!='unobserved':
  if cleanup['revoke']=='normal':
   evidence.update(original_reraised_to_launcher=True,reference=original['reference'],explicit_cause='client_error' if callback=='raises' else None)
   dest.append({'kind':'original-exception-reference','to':'launcher-existing-error-cleanup','reference':original['reference']})
   if cleanup['format']=='normal' and cleanup['cleanup']=='normal':
    evidence['retention']='existing write returned normally; durability unestablished' if cleanup['write']=='normal' else 'write failed and suppressed; no record established' if cleanup['write']=='raise' else 'write unobserved'
    if cleanup['write']=='normal':dest.append({'kind':'source-defined-original-error-details','to':'existing-launcher-evidence/failure-*.json','reference':original['reference'],'exact_bytes':None,'observed':False})
   elif cleanup['format']=='raise' or cleanup['cleanup']=='raise':evidence['retention']='formatting/cleanup interrupted before write; no record established'
   if cleanup['format']!='normal':need(cleanup['cleanup']==cleanup['write']=='unobserved','CLIENT-UNREACHED-RETENTION')
   elif cleanup['cleanup']!='normal':need(cleanup['write']=='unobserved','CLIENT-UNREACHED-WRITE')
  else:
   evidence['retention']='revocation not confirmed; original propagation and record remain unresolved'
   need(all(cleanup[k]=='unobserved' for k in ('format','cleanup','write','outer_fail')),'CLIENT-UNREACHED-LAUNCHER')
  completed=cleanup['revoke']=='normal' and (cleanup['format']=='raise' or cleanup['format']=='normal' and (cleanup['cleanup']=='raise' or cleanup['cleanup']=='normal' and cleanup['write']!='unobserved'))
  if not completed:need(cleanup['outer_fail']=='unobserved','CLIENT-UNREACHED-OUTER-FAIL')
  elif cleanup['outer_fail']=='normal':dest.append({'kind':'fixed-failure','to':'general-entry-caller','value':copy.deepcopy(catalogue['source']['fixed_failure'])})
 else:
  need(all(v=='unobserved' for v in cleanup.values()),'CLIENT-UNSUPPORTED-CLEANUP-PREMISE')
 if completion=='process-termination':need(callback=='unobserved' and all(v=='unobserved' for v in cleanup.values()),'CLIENT-TERMINATION-CONTINUATION')
 classification=_client_outcome_classification(catalogue,events,completion)
 # No fabricated outer-run failure receipt: exact callback, exit and _fail
 # continuations beyond these conditional destinations remain unobserved.
 return {'kind':'CONSTRUCTED-CLIENT-HANDLE','occurrence':case['occurrence'],'scope':copy.deepcopy(scope),'reference_bindings':copy.deepcopy(refs),'packet':copy.deepcopy(packet),'argument_hops':arguments,'manager':copy.deepcopy(manager_result),'events':events,'hops':hops,'completion':completion,'original_exception':original,'retained_original':retained,'fixed_client_failure':fixed,'destinations':dest,'evidence_route':evidence,
  'outside_catch_failure':classification['unexpected_raise_outside_dispatch_catch'],'outcome_classification':classification,'prior_owner_failure':{'present':refs['owner_failed'],'exact_value':None,'resolution_established':False},'runtime_observation':False,'physical_identity_established':False,'raw_error_or_status_publication_authorized':False,'arbitrary_callback_forwarding_prevented':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_client_handle_projection(catalogue,verification,case,validated,submitted):
 expected=client_handle_projection(catalogue,verification,case,validated);same(submitted,expected,'CLIENT-PROJECTION-CORRESPONDENCE');return True


# Client state forwarding and source-specific detachment. No runtime calls.
def client_state_source(launcher,entry,state,handle,boundary):
 validate_client_handle(launcher,entry,handle['manager_relation'],boundary,handle)
 common=client_handle_source(launcher,entry,handle['manager_relation'])
 lt,ll=_client_locate(launcher);et,el=_client_locate(entry)
 def method(tree,cls,name):
  body=next(n.body for n in tree.body if isinstance(n,ast.ClassDef) and n.name==cls) if cls else tree.body
  return next(n for n in body if isinstance(n,ast.FunctionDef) and n.name==name)
 def shape(node,text):
  def norm(n):
   n=copy.deepcopy(n)
   if isinstance(n.body[0],ast.Expr) and isinstance(n.body[0].value,ast.Constant) and type(n.body[0].value.value) is str:n.body.pop(0)
   return ast.dump(n,include_attributes=False)
  same(norm(node),norm(ast.parse(text).body[0]),'CLIENT-STATE-DEFINING-SHAPE:'+node.name)
 session=method(lt,'ManagedSession','state');client=method(et,'Client','state');data=method(et,None,'_data');dispatch=method(et,None,'_dispatch')
 shape(session,'def state(self): return self.__managed.state()')
 shape(client,"def state(self): return _dispatch(self.__token, 'state', None)")
 shape(data,"""def _data(value):
 if type(value) in (str,int,bool,type(None)): return value
 if type(value) is list: return [_data(v) for v in value]
 if type(value) is dict and all(type(k) is str for k in value): return {k:_data(v) for k,v in value.items()}
 raise RuntimeError('UNSUPPORTED-CLIENT-VALUE')
""")
 key_nodes=[n for n in et.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_STATE_KEYS' for t in n.targets)]
 need(len(key_nodes)==1,'CLIENT-STATE-KEY-SOURCE');kn=key_nodes[0]
 need(isinstance(kn.value,ast.Call) and ast.unparse(kn.value.func)=='frozenset' and len(kn.value.args)==1 and not kn.value.keywords,'CLIENT-STATE-KEY-EXPRESSION')
 keys=ast.literal_eval(kn.value.args[0]);need(type(keys) is tuple and all(type(k) is str for k in keys) and len(keys)==len(set(keys)),'CLIENT-STATE-KEYS')
 same(sorted(keys),sorted(state['inherited_head']['native_template']['type']['object']),'CLIENT-STATE-HEAD-SHAPE')
 same(state['source']['method'],'state','CLIENT-STATE-MANAGER-METHOD');same(state['source']['args'],[],'CLIENT-STATE-MANAGER-ARGS')
 tr=dispatch.body[2];body=tr.body;db=[n for n in data.body if not (isinstance(n,ast.Expr) and isinstance(n.value,ast.Constant) and type(n.value.value) is str)]
 primitives=[ast.unparse(n) for n in db[0].test.comparators[0].elts]
 same(primitives,['str','int','bool','type(None)'],'CLIENT-STATE-DATA-PRIMITIVES')
 stages={'client-call':el(client.body[0]),'owner-lookup':el(dispatch.body[0]),'owner-guard':el(dispatch.body[1]),'operation-check':el(body[1]),'session-call':el(body[2]),'manager-call':ll(session.body[0]),'session-return':ll(session.body[0]),'state-shape':el(body[3]),'conversion':el(body[4].value),'dispatch-return':el(body[4]),'client-return':el(client.body[0]),'retain-error':el(tr.handlers[0].body[0]),'fixed-failure':copy.deepcopy(common['stages']['fixed-failure'])}
 anchors={n:{**loc(node),'source':{'bytes':len(raw),'sha256':digest(raw)},'ast':ast.dump(node,include_attributes=False)} for n,raw,loc,node in [('session-state',launcher,ll,session),('client-state',entry,el,client),('data',entry,el,data),('state-keys',entry,lambda n:{'site':f'{n.lineno}:{n.col_offset}:{n.end_lineno}:{n.end_col_offset}:{type(n).__name__}','expression':ast.get_source_segment(entry.decode(),n),'guards':[],'continuation':[]},kn)]}
 return {'sources':copy.deepcopy(common['sources']),'anchors':anchors,'stages':stages,'common_anchors':{n:copy.deepcopy(common['anchors'][n]) for n in ('session-init','client-init','owner-init','dispatch','fixed-failure','owner-route','general-entry','launcher-error')},
  'operation':client.body[0].value.args[1].value,'packet':ast.literal_eval(client.body[0].value.args[2]),'state_keys':list(keys),'state_shape_guard':ast.unparse(body[3].test),'operation_guard':ast.unparse(body[1].test),
  'state_shape_failure':{'type':body[3].body[0].exc.func.id,'message':body[3].body[0].exc.args[0].value},'operation_failure':{'type':body[1].body[0].exc.func.id,'message':body[1].body[0].exc.args[0].value},
  'data_primitives':['NoneType' if n=='type(None)' else n for n in primitives],
  'data_branches':{'primitive':el(db[0]),'list':el(db[1]),'dict':el(db[2]),'unsupported':el(db[3])},'data_failure':{'type':db[3].exc.func.id,'message':db[3].exc.args[0].value},
  'fixed_failure':copy.deepcopy(common['fixed_failure']),'caught_class':ast.unparse(tr.handlers[0].type),'limits':copy.deepcopy(common['limits'])}

def compile_client_state(launcher,entry,state,handle,boundary):
 source=client_state_source(launcher,entry,state,handle,boundary)
 wanted=['client-state','data-detachment','dispatch-and-failure','owner-routing','launcher-diagnostic-and-evidence'];sites={s['id']:s for s in boundary['sites']}
 for n in wanted:
  need(n in sites,'CLIENT-STATE-BOUNDARY-SITE');pin=source['sources']['launcher' if n.startswith('launcher') else 'entry'];same({k:sites[n]['anchor'][k] for k in pin},pin,'CLIENT-STATE-BOUNDARY-PIN')
 values=['manager-return','session-return','dispatch-result','converted-result','dispatch-return','client-return']
 origins=[state['source']['wrapper_return'],source['stages']['session-return'],source['stages']['session-call'],source['anchors']['data'],source['stages']['dispatch-return'],source['stages']['client-return']]
 return {'format':'I164-CLIENT-STATE-STATIC-1','source':source,'manager_relation':copy.deepcopy(state),'boundary_contract':copy.deepcopy(boundary['contract']),'boundary_sites':[copy.deepcopy(sites[n]) for n in wanted],
  'declarations':[{'id':n,'type':copy.deepcopy(state['inherited_head']['native_template']['type']),'source_origin':copy.deepcopy(o),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n,o in zip(values,origins)],'ordered_hops':values,
  'arguments':[{'from':'Client.state','to':'_dispatch','operation':'state','packet':None,'token':'client.token'},{'from':'_dispatch','to':'ManagedSession.state','args':[]},{'from':'ManagedSession.state','to':'ManagedAuthority.state','args':[]}],
  'reference_edges':copy.deepcopy(handle['reference_edges']),
  'copy_semantics':{'algorithm':'source-recursive exact-type detachment; no memo','containers':'fresh list/dict for EACH visited input path; repeated mutable aliases split, no output mutable alias sharing','keys':'exact str keys in insertion order','primitives':'same exact primitive values/types; no immutable physical-identity observation','cycles':'no finite normal unfolding; no inferred terminal exception class or resource bound','normal_guard':'supported acyclic finite input AND every source continuation returns normally','unsupported_guard':'unsupported exact type or non-str dict key when reached -> source RuntimeError; no user copy/repr hook'},
  'outside_catch_failure_contract':copy.deepcopy(handle['outside_catch_failure_contract']),
  'scope':'request-independent acquisition/context/instance/frontier plus distinct invocation; frontier is not an unobserved call time',
  'runtime_links':None,'physical_alias_observations':None,'complete_repetition_coverage':False,'actual_admission':False}

def validate_client_state(launcher,entry,state,handle,boundary,submitted):
 same(submitted,compile_client_state(launcher,entry,state,handle,boundary),'CLIENT-STATE-SOURCE-CORRESPONDENCE');return True

def data_source_domain(catalogue,value):
 """Source-domain analysis of constructed objects; never calls application _data.
 Domain feasibility is separate from resource/exception/termination outcomes.
 """
 src=catalogue['source'];allowed={'str':str,'int':int,'bool':bool,'NoneType':type(None)};types=tuple(allowed[n] for n in src['data_primitives']);pending=[(value,(),frozenset())];containers=0
 while pending:
  v,path,parents=pending.pop();t=type(v)
  if t in types:continue
  if t not in (list,dict) or t is dict and not all(type(k) is str for k in v):
   return {'normal_return_domain':False,'reason':'unsupported-type-or-dict-key','path':list(path),'source_defined_raise_if_reached':copy.deepcopy(src['data_failure']),'runtime_observation':False}
  if id(v) in parents:return {'normal_return_domain':False,'reason':'cycle-no-finite-normal-unfolding','path':list(path),'source_defined_raise_if_reached':None,'runtime_observation':False}
  containers+=1;anc=parents|{id(v)};children=list(v.items()) if t is dict else list(enumerate(v));pending.extend((x,path+(k,),anc) for k,x in reversed(children))
 return {'normal_return_domain':True,'container_path_occurrences':containers,'resource_completion_established':False,'runtime_observation':False}

def validate_data_detachment(graph):
 """Finite normal-return graph relation. Unlike deepcopy, no input-node memo.
 Symbols are constructed occurrence-local premises, never physical addresses.
 """
 need(type(graph) is dict and set(graph)=={'roots','nodes'},'DATA-GRAPH-FIELDS');roots=graph['roots'];nodes=graph['nodes']
 need(type(roots) is list and len(roots)==2 and type(nodes) is dict and all(type(k) is str and k for k in nodes),'DATA-GRAPH-DOMAIN')
 def edge(e):
  need(type(e) is dict,'DATA-EDGE')
  if set(e)=={'ref'}:need(type(e['ref']) is str and e['ref'] in nodes,'DATA-REFERENCE');return
  need(set(e)=={'atom','value'} and type(e['atom']) is str,'DATA-ATOM');types={'NoneType':type(None),'bool':bool,'int':int,'str':str}
  need(e['atom'] in types and type(e['value']) is types[e['atom']],'DATA-EXACT-PRIMITIVE')
 for n in nodes.values():
  need(type(n) is dict and set(n)=={'kind','items'} and n['kind'] in ('dict','list') and type(n['items']) is list,'DATA-NODE')
  if n['kind']=='dict':
   keys=[]
   for pair in n['items']:need(type(pair) is list and len(pair)==2 and type(pair[0]) is str,'DATA-DICT-ITEM');keys.append(pair[0]);edge(pair[1])
   need(len(keys)==len(set(keys)),'DATA-DUPLICATE-KEY')
  else:
   for e in n['items']:edge(e)
 for e in roots:edge(e)
 input_nodes=set();output_nodes=set();pairs=[];pending=[(roots[0],roots[1],(),frozenset())]
 while pending:
  a,b,path,anc=pending.pop();need(set(a)==set(b),'DATA-EDGE-KIND')
  if 'atom' in a:same(a,b,'DATA-EXACT-ATOM-VALUE');continue
  x,y=a['ref'],b['ref'];need(x not in anc,'DATA-CYCLE-NO-NORMAL-RETURN');need(y not in output_nodes,'DATA-OUTPUT-ALIAS-MEMO-OR-MERGE');input_nodes.add(x);output_nodes.add(y)
  an,bn=nodes[x],nodes[y];need(an['kind']==bn['kind'] and len(an['items'])==len(bn['items']),'DATA-CONTAINER-SHAPE');pairs.append({'path':list(path),'input':x,'output':y,'kind':an['kind']})
  children=[]
  for i,(av,bv) in enumerate(zip(an['items'],bn['items'])):
   if an['kind']=='dict':need(av[0]==bv[0],'DATA-KEY-ORDER');children.append((av[1],bv[1],path+(av[0],),anc|{x}))
   else:children.append((av,bv,path+(i,),anc|{x}))
  pending.extend(reversed(children))
 need(not input_nodes&output_nodes,'DATA-INPUT-OUTPUT-MUTABLE-SHARING');need(input_nodes|output_nodes==set(nodes),'DATA-UNREACHABLE-NODE')
 return {'result':'PASS','container_path_pairs':pairs,'input_distinct_containers':len(input_nodes),'output_container_occurrences':len(output_nodes),'internal_input_aliases_preserved':False,'immutable_identity_established':False,'runtime_observation':False}

def _data_graph_value(graph,root):
 """Decode only after the normal detachment relation has rejected cycles."""
 values={n:({} if v['kind']=='dict' else []) for n,v in graph['nodes'].items()}
 def val(e):return values[e['ref']] if 'ref' in e else e['value']
 for n,v in graph['nodes'].items():
  if v['kind']=='dict':values[n].update((k,val(e)) for k,e in v['items'])
  else:values[n].extend(val(e) for e in v['items'])
 return val(root)

def client_state_projection(catalogue,case,validated):
 """Conditional, source-grounded state path under independent validated premises.
 Neither this pure projector nor a caller-supplied graph admits actual evidence.
 """
 need(type(case) is dict and set(case)=={'occurrence','scope','references','outcomes','manager_case','detachment','callback','cleanup'},'CLIENT-STATE-CASE')
 need(type(validated) is dict and set(validated)=={'scope','state'},'CLIENT-STATE-VALIDATED');same(case['scope'],validated['scope'],'CLIENT-STATE-SCOPE')
 scope=case['scope'];need(type(scope) is dict and set(scope)=={'context','acquisition','instance','frontier','invocation'} and scope['context'] in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'),'CLIENT-STATE-INVOCATION-SCOPE')
 need(type(case['occurrence']) is str and bool(case['occurrence']) and case['occurrence']==scope['invocation'],'CLIENT-STATE-OCCURRENCE')
 refs=case['references'];base={'client','token','owner','session','manager','manager-result','data-result'};required=base|{'client.token','owners[token]','owner.wrapper','session.managed','owner_failed'}
 need(type(refs) is dict and set(refs)==required and type(refs['owner_failed']) is bool,'CLIENT-STATE-REFERENCES')
 for k in base:
  r=refs[k];need(type(r) is dict and set(r)=={'kind','scope','symbol'} and r['kind']==('state-result-reference' if k.endswith('result') else k+'-reference') and type(r['symbol']) is str and bool(r['symbol']),'CLIENT-STATE-REFERENCE-TYPE');same(r['scope'],scope,'CLIENT-STATE-REFERENCE-SCOPE')
 need(refs['manager-result']['symbol']!=refs['data-result']['symbol'],'CLIENT-STATE-DETACHED-REFERENCE')
 for a,b in catalogue['reference_edges']:
  if a=='owners[token]' and refs[a] is None:continue
  same(refs[a],refs[b],'CLIENT-STATE-REFERENCE-EDGE:'+a)
 outcomes=case['outcomes'];need(type(outcomes) is dict,'CLIENT-STATE-OUTCOMES');used=set();events=[];hops=[];args=[];dest=[];original=None;fixed=None;retained=False;completion='pending';manager=None;copy_relation=None;converted=None
 def step(n):
  need(n in outcomes and type(outcomes[n]) is str and outcomes[n] in ('normal','raise','process-termination'),'CLIENT-STATE-STAGE:'+n);used.add(n);v=outcomes[n];events.append({'stage':n,'source':copy.deepcopy(catalogue['source']['stages'][n]),'outcome':v});return v
 def link(n,value,reference):hops.append({'id':case['occurrence']+'/'+n,'declaration':n,'scope':copy.deepcopy(scope),'value':copy.deepcopy(value),'reference':copy.deepcopy(reference),'source':copy.deepcopy(next(d['source_origin'] for d in catalogue['declarations'] if d['id']==n))})
 def fail_fixed():
  nonlocal fixed,completion
  v=step('fixed-failure')
  if v=='normal':fixed=copy.deepcopy(catalogue['source']['fixed_failure']);completion='fixed-client-failure';dest.append({'kind':'fixed-failure','to':'general-client','value':copy.deepcopy(fixed)})
  else:completion='unqualified-escape' if v=='raise' else v
 def prefix(n):
  nonlocal completion
  v=step(n)
  if v!='normal':completion='unqualified-escape' if v=='raise' else v;return False
  return True
 entered=prefix('client-call')
 if entered:args.append({'id':case['occurrence']+'/client-to-dispatch','to':'_dispatch','token':copy.deepcopy(refs['token']),'operation':catalogue['source']['operation'],'packet':catalogue['source']['packet']})
 entered=entered and prefix('owner-lookup') and prefix('owner-guard')
 if entered and (refs['owners[token]'] is None or refs['owner_failed']):fail_fixed()
 elif entered:
  for stage in ('operation-check','session-call','manager-call','session-return','state-shape','conversion','dispatch-return','client-return'):
   v=step(stage)
   if v!='normal':
    if v=='process-termination':completion=v;break
    if stage=='client-return':completion='unqualified-escape';break
    original={'kind':'conditional-exception','origin':stage,'catch_family':catalogue['source']['caught_class'],'exact_type':None,'reference':case['occurrence']+'/error'};break
   if stage=='session-call':args.append({'id':case['occurrence']+'/dispatch-to-session','to':'ManagedSession.state','receiver':copy.deepcopy(refs['session']),'args':[]})
   elif stage=='manager-call':
    mc=case['manager_case'];need(type(mc) is dict and set(mc)=={'outcomes','returned'},'CLIENT-STATE-MANAGER-PREMISE')
    path=state_path_projection(catalogue['manager_relation'],mc['outcomes']);args.append({'id':case['occurrence']+'/session-to-manager','to':'ManagedAuthority.state','receiver':copy.deepcopy(refs['manager']),'args':[]})
    if path['completion']!='normal':
     need(mc['returned'] is None,'CLIENT-STATE-NO-ABRUPT-RETURN');manager={'path':path,'return':None};original={'kind':'manager-escaping-exception','origin':stage,'catch_family':'BaseException','exact_type':None,'reference':case['occurrence']+'/error'};break
    ret=mc['returned'];need(type(ret) is dict,'CLIENT-STATE-MANAGER-RETURN');same(ret['outcomes'],mc['outcomes'],'CLIENT-STATE-MANAGER-OUTCOMES')
    same(ret['live_reference']['scope'],scope,'CLIENT-STATE-LIVE-SCOPE');same(ret['wrapper_return']['reference'],refs['manager-result'],'CLIENT-STATE-MANAGER-REFERENCE')
    manager=state_value_projection(catalogue['manager_relation'],ret,validated['state']);link('manager-return',ret['wrapper_return']['value'],refs['manager-result'])
   elif stage=='session-return':
    need(manager is not None and manager.get('kind')=='CONSTRUCTED-STATE-RETURN','CLIENT-STATE-NORMAL-MANAGER');value=case['manager_case']['returned']['wrapper_return']['value'];link('session-return',value,refs['manager-result']);link('dispatch-result',value,refs['manager-result'])
   elif stage=='state-shape':
    value=case['manager_case']['returned']['wrapper_return']['value'];need(type(value) is dict and set(value)==set(catalogue['source']['state_keys']),'CLIENT-STATE-REQUIRED-SHAPE')
   elif stage=='conversion':
    d=case['detachment'];need(type(d) is dict and set(d)=={'input_reference','output_reference','graph'},'CLIENT-STATE-COPY-PREMISE')
    same(d['input_reference'],refs['manager-result'],'CLIENT-STATE-COPY-INPUT-REFERENCE');same(d['output_reference'],refs['data-result'],'CLIENT-STATE-COPY-OUTPUT-REFERENCE')
    copy_relation=validate_data_detachment(d['graph']);value=_data_graph_value(d['graph'],d['graph']['roots'][0]);converted=_data_graph_value(d['graph'],d['graph']['roots'][1]);state_value_compare(catalogue['manager_relation'],value,validated['state']);state_value_compare(catalogue['manager_relation'],converted,validated['state'])
    need(data_source_domain(catalogue,value)['normal_return_domain'],'CLIENT-STATE-COPY-DOMAIN');link('converted-result',converted,refs['data-result'])
   elif stage=='dispatch-return':need(copy_relation is not None,'CLIENT-STATE-CONVERSION-COMPLETION');link('dispatch-return',converted,refs['data-result'])
   elif stage=='client-return':link('client-return',converted,refs['data-result']);completion='normal';dest.append({'kind':'detached-state-data','to':'general-client','value':copy.deepcopy(converted)})
  if original is not None:
   v=step('retain-error')
   if v=='normal':retained=True;dest.append({'kind':'original-exception-reference','to':'owner.failure','reference':original['reference']});fail_fixed()
   else:retained=None;completion='unqualified-escape' if v=='raise' else v
 if manager is None:need(case['manager_case'] is None,'CLIENT-STATE-UNREACHED-MANAGER')
 if copy_relation is None:need(case['detachment'] is None,'CLIENT-STATE-UNREACHED-COPY')
 need(used==set(outcomes),'CLIENT-STATE-UNREACHED-STAGE')
 callback=case['callback'];cleanup=case['cleanup'];need(callback in ('returns','raises','unobserved'),'CLIENT-STATE-CALLBACK');need(type(cleanup) is dict and set(cleanup)=={'revoke','format','cleanup','write','outer_fail'} and all(v in ('normal','raise','unobserved') for v in cleanup.values()),'CLIENT-STATE-CLEANUP')
 evidence={'original_reraised_to_launcher':None,'reference':None,'explicit_cause':'unobserved','retention':'UNESTABLISHED','bytes':None,'cleanup_obligations':'UNCHANGED','cleanup_premise':'normal means iteration/error-detail handling completed, not every connection closed','active_marker_removal':'UNESTABLISHED'}
 if retained and completion=='fixed-client-failure' and callback!='unobserved':
  if cleanup['revoke']=='normal':
   evidence.update(original_reraised_to_launcher=True,reference=original['reference'],explicit_cause='client_error' if callback=='raises' else None);dest.append({'kind':'original-exception-reference','to':'launcher-existing-error-cleanup','reference':original['reference']})
   if cleanup['format']=='normal' and cleanup['cleanup']=='normal':
    evidence['retention']='existing write returned; durability unestablished' if cleanup['write']=='normal' else 'write failed and suppressed; no record established' if cleanup['write']=='raise' else 'write unobserved'
    if cleanup['write']=='normal':dest.append({'kind':'source-defined-original-error-details','to':'existing-launcher-evidence/failure-*.json','reference':original['reference'],'exact_bytes':None,'observed':False})
   elif cleanup['format']=='raise' or cleanup['cleanup']=='raise':evidence['retention']='formatting/cleanup interrupted; no record established'
   if cleanup['format']!='normal':need(cleanup['cleanup']==cleanup['write']=='unobserved','CLIENT-STATE-UNREACHED-RETENTION')
   elif cleanup['cleanup']!='normal':need(cleanup['write']=='unobserved','CLIENT-STATE-UNREACHED-WRITE')
  else:need(all(cleanup[k]=='unobserved' for k in ('format','cleanup','write','outer_fail')),'CLIENT-STATE-UNREACHED-LAUNCHER')
  completed=cleanup['revoke']=='normal' and (cleanup['format']=='raise' or cleanup['format']=='normal' and (cleanup['cleanup']=='raise' or cleanup['cleanup']=='normal' and cleanup['write']!='unobserved'))
  if not completed:need(cleanup['outer_fail']=='unobserved','CLIENT-STATE-UNREACHED-OUTER')
  elif cleanup['outer_fail']=='normal':dest.append({'kind':'fixed-failure','to':'general-entry-caller','value':copy.deepcopy(catalogue['source']['fixed_failure'])})
 else:need(all(v=='unobserved' for v in cleanup.values()),'CLIENT-STATE-UNSUPPORTED-CLEANUP')
 if completion=='process-termination':need(callback=='unobserved' and all(v=='unobserved' for v in cleanup.values()),'CLIENT-STATE-TERMINATION-CONTINUATION')
 classification=_client_outcome_classification(catalogue,events,completion)
 return {'kind':'CONSTRUCTED-CLIENT-STATE','occurrence':case['occurrence'],'scope':copy.deepcopy(scope),'references':copy.deepcopy(refs),'arguments':args,'manager':copy.deepcopy(manager),'events':events,'hops':hops,'copy_relation':copy_relation,'completion':completion,'original_exception':original,'retained_original':retained,'fixed_client_failure':fixed,'destinations':dest,'evidence_route':evidence,
  'outside_catch_failure':classification['unexpected_raise_outside_dispatch_catch'],'outcome_classification':classification,'prior_owner_failure':{'present':refs['owner_failed'],'resolution_established':False},'runtime_observation':False,'physical_identity_established':False,'request_or_journal_row_required':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False,'outer_continuation':'PARTIAL; abrupt/unrepresented continuation stays unresolved'}

def validate_client_state_projection(catalogue,case,validated,submitted):
 same(submitted,client_state_projection(catalogue,case,validated),'CLIENT-STATE-PROJECTION-CORRESPONDENCE');return True


def status_exact_tree(value,code):
 """Check exact representation types BEFORE equality, copying or JSON encoding.

 Repeated aliases are allowed; cycles are not finite JSON values. This is a
 representation contract, not a reason-string, epoch or lifetime bound.
 """
 stack=[(value,False)];active=set()
 while stack:
  node,leaving=stack.pop();kind=type(node)
  if leaving:active.remove(id(node));continue
  if kind is dict or kind is list:
   need(id(node) not in active,code+':CYCLE');active.add(id(node));stack.append((node,True))
   if kind is dict:
    for key,child in node.items():
     need(type(key) is str,code+':KEY-TYPE');stack.append((child,False))
   else:
    for child in node:stack.append((child,False))
  else:need(any(kind is allowed for allowed in (str,int,bool,float,type(None))),code+':VALUE-TYPE')

def status_typed_same(a,b,code):
 status_exact_tree(a,code);status_exact_tree(b,code);same(a,b,code)

def status_forward_source(launcher,entry,fields,boundary):
 """Source-derived internal diagnostic route. No operational code is invoked."""
 need(type(launcher) is bytes and type(entry) is bytes,'STATUS-FORWARD-SOURCE-TYPE');status_exact_tree(fields,'STATUS-FORWARD-FIELDS');status_exact_tree(boundary,'STATUS-FORWARD-BOUNDARY')
 lt,ll=_client_locate(launcher);et,el=_client_locate(entry)
 def method(tree,owner,name):
  body=tree.body if owner is None else next(n.body for n in tree.body if isinstance(n,ast.ClassDef) and n.name==owner)
  found=[n for n in body if isinstance(n,ast.FunctionDef) and n.name==name];need(len(found)==1,'STATUS-FORWARD-METHOD:'+name);return found[0]
 def shape(node,text):
  def norm(n):
   n=copy.deepcopy(n)
   if n.body and isinstance(n.body[0],ast.Expr) and isinstance(n.body[0].value,ast.Constant) and type(n.body[0].value.value) is str:n.body.pop(0)
   return ast.dump(n,include_attributes=False)
  status_typed_same(norm(node),norm(ast.parse(text).body[0]),'STATUS-FORWARD-SOURCE-SHAPE:'+node.name)
 session=method(lt,'ManagedSession','status');si=method(lt,'ManagedSession','__init__');control=method(et,'_Control','status');ci=method(et,'_Control','__init__');oi=method(et,'_Owner','__init__');fail=method(et,None,'_fail');route=method(et,None,'_run');controlled=method(et,None,'run_controlled')
 shape(si,'def __init__(self,managed): self.__managed=managed')
 shape(session,'def status(self): return self.__managed.status()')
 shape(ci,'def __init__(self,token): self.__token=token')
 shape(oi,'def __init__(self,wrapper):\n self.wrapper=wrapper\n self.failure=None')
 shape(control,'def status(self):\n owner=_OWNERS.get(self.__token)\n if owner is None: _fail()\n return owner.wrapper.status()')
 shape(fail,"def _fail(): raise ClientFailure('MANAGED-OPERATION-UNAVAILABLE; outcome uncertain; no renewed authorization') from None")
 shape(controlled,'''def run_controlled(candidate,draft,runtime,destination,client,*,control,create=False):
 failed=False
 try: launcher=_load_launcher()
 except BaseException: failed=True
 if failed: _fail()
 return _run(launcher,candidate,draft,runtime,destination,client,create,control)
''')
 # Independently locate the actual token store/control handoff/revocation. The
 # full _run body is already mandatorily checked by the reviewed predecessor.
 def unique(kind,expression):
  hits=[n for n in ast.walk(route) if isinstance(n,kind) and ast.unparse(n)==expression];need(len(hits)==1,'STATUS-FORWARD-ROUTE:'+expression);return hits[0]
 owner_store=unique(ast.Assign,'_OWNERS[token] = owner');token=unique(ast.Assign,'token = object()');new_owner=unique(ast.Assign,'owner = _Owner(wrapper)');control_call=unique(ast.Call,'control(_Control(token))');revoke=unique(ast.Call,'_OWNERS.pop(token, None)')
 need(any(g['kind']=='if' and g['test']['expression']=='control is not None' and g['arm']=='body' for g in el(control_call)['guards']),'STATUS-FORWARD-CONTROL-GUARD')
 phases=sorted({e['value'] for w in fields['source']['writes'] if w['target']=='_phase' for e in _status_expr_nodes(w['value']) if e['op']=='literal' and e['type']=='str'})
 need(bool(phases),'STATUS-FORWARD-PHASE-DOMAIN')
 epochs=[w for w in fields['source']['writes'] if w['target']=='_epoch'];initial=[w for w in epochs if w['function']=='__init__'];increments=[w for w in epochs if w['function']!='__init__']
 need(len(initial)==len(increments)==1 and initial[0]['operation']=='set' and initial[0]['value']['op']=='literal' and initial[0]['value']['type']=='int' and increments[0]['operation']=='add' and increments[0]['value']['op']=='literal' and increments[0]['value']['type']=='int' and increments[0]['value']['value']>0,'STATUS-FORWARD-EPOCH-SOURCE')
 types_={f['name']:f['type'] for f in fields['declarations']};need(set(types_)==set(fields['owning_return']['field_ids'][i].split(':')[-1] for i in range(len(types_))),'STATUS-FORWARD-FIELD-DOMAIN')
 manager_return=copy.deepcopy(fields['source']['return']);lock=next(g for g in manager_return['guards'] if g['kind']=='With')
 stages={'control-call':el(control),'owner-lookup':el(control.body[0]),'owner-guard':el(control.body[1]),'session-call':el(control.body[2].value),'manager-call':ll(session.body[0].value),'lock-enter':copy.deepcopy(lock),'manager-result':manager_return,'lock-exit':copy.deepcopy(lock),'manager-return':manager_return,'session-return':ll(session.body[0]),'control-return':el(control.body[2]),'fixed-failure':el(fail.body[0])}
 anchors={name:{**loc(node),'source':{'bytes':len(raw),'sha256':digest(raw)},'ast':ast.dump(node,include_attributes=False)} for name,raw,loc,node in [('session-status',launcher,ll,session),('session-init',launcher,ll,si),('control-status',entry,el,control),('control-init',entry,el,ci),('owner-init',entry,el,oi),('controlled-entry',entry,el,controlled),('control-call',entry,el,control_call),('owner-store',entry,el,owner_store),('token-create',entry,el,token),('owner-create',entry,el,new_owner),('revoke',entry,el,revoke),('fixed-failure',entry,el,fail)]}
 wanted=['manager-status','launcher-forwarder','internal-diagnostic','trusted-control-entry','owner-routing','general-entry'];sites={s['id']:s for s in boundary['sites']};need(all(n in sites for n in wanted),'STATUS-FORWARD-BOUNDARY-SITES')
 pins={'launcher':{'bytes':len(launcher),'sha256':digest(launcher)},'entry':{'bytes':len(entry),'sha256':digest(entry)},'manager':{k:fields['source']['source'][k] for k in ('bytes','sha256')}}
 for n in wanted:
  pin=pins['manager' if n=='manager-status' else 'launcher' if n=='launcher-forwarder' else 'entry'];status_typed_same({k:sites[n]['anchor'][k] for k in pin},pin,'STATUS-FORWARD-BOUNDARY-PIN')
 return {'sources':pins,'anchors':anchors,'stages':stages,'owner_guard':ast.unparse(control.body[1].test),'normal_owner_condition':'owner is not None; prior owner.failure does not guard this method','session_call':{'receiver':ast.unparse(control.body[2].value.func.value),'method':control.body[2].value.func.attr,'args':[]},'manager_call':{'receiver':ast.unparse(session.body[0].value.func.value),'method':session.body[0].value.func.attr,'args':[]},'fixed_failure':{'type':fail.body[0].exc.func.id,'message':ast.literal_eval(fail.body[0].exc.args[0]),'explicit_cause':ast.literal_eval(fail.body[0].cause),'context_display_suppressed':True,'ambient_exception_context_not_established':True},'source_phase_literals':phases,'epoch_initial':initial[0]['value']['value'],'epoch_increment':increments[0]['value']['value'],'epoch_write_origins':copy.deepcopy(epochs),'boundary_sites':[copy.deepcopy(sites[n]) for n in wanted],'no_local_except_in_forwarders':not any(isinstance(n,ast.Try) for fn in (session,control) for n in ast.walk(fn))}

def compile_status_forward(launcher,entry,fields,boundary):
 source=status_forward_source(launcher,entry,fields,boundary);need(source['no_local_except_in_forwarders'],'STATUS-FORWARD-LOCAL-CATCH')
 hops=['manager-return','session-return','control-return']
 return {'format':'I164-INTERNAL-STATUS-FORWARD-STATIC-1','source':source,'manager_fields':copy.deepcopy(fields),'boundary_contract':copy.deepcopy(boundary['contract']),'boundary_adoption':copy.deepcopy(boundary['adoption']),
  'declarations':[{'id':n,'type':{'exact':'dict','fields':{d['name']:d['type'] for d in fields['declarations']}},'source_origin':copy.deepcopy(source['stages'][n]),'fields':[{'name':d['name'],'manager_declaration':d['id'],'selector':copy.deepcopy(d['value']),'origin_ids':copy.deepcopy(d['origin_ids'])} for d in fields['declarations']],'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in hops],'ordered_hops':hops,
  'reference_edges':[['control.token','token'],['owners[token]','owner'],['owner.wrapper','session'],['session.managed','manager']],
  'normal_stage_order':['control-call','owner-lookup','owner-guard','session-call','manager-call','lock-enter','manager-result','lock-exit','manager-return','session-return','control-return'],
  'reference_semantics':{'manager_result':'new dictionary expression per successful status evaluation; no intrinsic serialized bytes','forwarders':'same returned reference; no conversion/copy/serialization','physical_object_identity_observed':False,'same_values_do_not_identify_calls_or_objects':True},
  'guard_semantics':{'READY_required':False,'owner_failure_blocks':False,'dispatch_path':False,'data_conversion':False,'missing_owner':'source _fail intentional raise if helper completes as defined','normal':'owner present AND all source evaluation/lock/return continuations normal','exception':'no local catch in either forwarder; outer control/orchestration continuation not established','termination':'no inferred Python exception, unwind, retained error, cleanup or authority'},
  'destinations':{'normal_status':'designated internal control caller','escaping_exception':'calling trusted control path; outer handling remains conditional/unobserved','general_client_status':False,'automatic_output':False,'new_capture_permission':False},
  'scope':'acquisition/context/validated manager instance plus distinct request-independent invocation; observed sample frontier is not a later call time','runtime_forwarding_links':None,'actual_call_count':None,'complete_repetition_coverage':False,'actual_admission':False}

def validate_status_forward(launcher,entry,fields,boundary,submitted):
 status_exact_tree(submitted,'STATUS-FORWARD-SUBMITTED-CATALOGUE')
 status_typed_same(submitted,compile_status_forward(launcher,entry,fields,boundary),'STATUS-FORWARD-SOURCE-CORRESPONDENCE');return True

def status_snapshot_value(catalogue,snapshot):
 status_exact_tree(catalogue,'STATUS-FORWARD-CATALOGUE');status_exact_tree(snapshot,'STATUS-FORWARD-SNAPSHOT')
 fields=catalogue['manager_fields']['declarations'];required={d['value']['name'] for d in fields if d['value']['op']=='state'}
 need(type(snapshot) is dict and set(snapshot)==required,'STATUS-FORWARD-SNAPSHOT-FIELDS');result={}
 for d in fields:
  expr=d['value'];v=snapshot[expr['name']] if expr['op']=='state' else expr['value'];need(d['type'] in ('str','int','bool') and type(v) is {'str':str,'int':int,'bool':bool}[d['type']],'STATUS-FORWARD-VALUE-TYPE:'+d['name']);result[d['name']]=v
 need(result['phase'] in catalogue['source']['source_phase_literals'],'STATUS-FORWARD-PHASE')
 delta=result['connection_epoch']-catalogue['source']['epoch_initial'];inc=catalogue['source']['epoch_increment'];need(delta>=0 and delta%inc==0,'STATUS-FORWARD-EPOCH')
 return copy.deepcopy(result)

def status_forward_projection(catalogue,case,validated):
 """Explicit conditional premises only. Not a status execution or history proof."""
 status_exact_tree(catalogue,'STATUS-FORWARD-CATALOGUE');status_exact_tree(case,'STATUS-FORWARD-RETURN-INPUT');status_exact_tree(validated,'STATUS-FORWARD-VALIDATED-INPUT')
 keys={'occurrence','scope','references','outcomes','manager_snapshot','returned'}
 need(type(case) is dict and set(case)==keys and type(validated) is dict and set(validated)==keys-{'returned'},'STATUS-FORWARD-CASE')
 for k in validated:status_typed_same(case[k],validated[k],'STATUS-FORWARD-PREMISE:'+k)
 scope=case['scope'];need(type(scope) is dict and set(scope)=={'context','acquisition','instance','frontier','invocation'},'STATUS-FORWARD-SCOPE');need(scope['context'] in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO') and type(case['occurrence']) is str and bool(case['occurrence']) and case['occurrence']==scope['invocation'],'STATUS-FORWARD-INVOCATION')
 refs=case['references'];roles=['control','token','owner','session','manager','result'];need(type(refs) is dict and set(refs)==set(roles)|{'control.token','owners[token]','owner.wrapper','session.managed','owner_failed'},'STATUS-FORWARD-REFERENCES');need(type(refs['owner_failed']) is bool,'STATUS-FORWARD-OWNER-FAILURE-TYPE')
 for role in roles:
  v=refs[role];need(type(v) is dict and set(v)=={'scope','symbol'} and type(v['symbol']) is str and bool(v['symbol']),'STATUS-FORWARD-REFERENCE-TYPE');status_typed_same(v['scope'],scope,'STATUS-FORWARD-REFERENCE-SCOPE')
 for a,b in catalogue['reference_edges']:
  if a=='owners[token]' and refs[a] is None:continue
  status_typed_same(refs[a],refs[b],'STATUS-FORWARD-REFERENCE-EDGE:'+a)
 outcomes=case['outcomes'];need(type(outcomes) is dict,'STATUS-FORWARD-OUTCOMES');used=set();events=[];hops=[];arguments=[];result=None;completion=None;fixed=None
 def step(stage):
  need(stage in outcomes,'STATUS-FORWARD-MISSING-STAGE:'+stage);v=outcomes[stage];allowed=('intended-raise','raise','process-termination') if stage=='fixed-failure' else ('normal','raise','process-termination');need(type(v) is str and v in allowed,'STATUS-FORWARD-STAGE-KIND');used.add(stage);events.append({'stage':stage,'source':copy.deepcopy(catalogue['source']['stages'][stage]),'outcome':v});return v
 stages=catalogue['normal_stage_order']
 for stage in stages:
  v=step(stage)
  if v!='normal':completion='unexpected-raise' if v=='raise' else 'process-termination';break
  if stage=='owner-guard' and refs['owners[token]'] is None:
   v=step('fixed-failure');completion='intentional-fixed-raise' if v=='intended-raise' else 'unexpected-raise' if v=='raise' else 'process-termination'
   if v=='intended-raise':fixed=copy.deepcopy(catalogue['source']['fixed_failure'])
   break
  if stage in ('session-call','manager-call'):
   arguments.append({'id':case['occurrence']+'/'+stage,'scope':copy.deepcopy(scope),'to':'ManagedSession.status' if stage=='session-call' else 'ManagedAuthority.status','receiver':copy.deepcopy(refs['session' if stage=='session-call' else 'manager']),'args':[],'kwargs':{}})
  if stage=='manager-result':result=status_snapshot_value(catalogue,case['manager_snapshot'])
  if stage in catalogue['ordered_hops']:
   need(result is not None,'STATUS-FORWARD-RETURN-WITHOUT-RESULT');hops.append({'id':case['occurrence']+'/'+stage,'declaration':stage,'manager_invocation':case['occurrence']+'/manager-status','scope':copy.deepcopy(scope),'value':copy.deepcopy(result),'reference':copy.deepcopy(refs['result'])})
  if stage=='control-return':completion='normal-return'
 need(used==set(outcomes),'STATUS-FORWARD-UNREACHED-STAGE')
 if result is None:need(case['manager_snapshot'] is None,'STATUS-FORWARD-UNREACHED-SNAPSHOT')
 need(type(case['returned']) is list,'STATUS-FORWARD-RETURNS-TYPE')
 for hop in case['returned']:
  need(type(hop) is dict and set(hop)=={'id','declaration','manager_invocation','scope','value','reference'},'STATUS-FORWARD-RETURN-SHAPE');value=hop['value'];defs=catalogue['manager_fields']['declarations'];need(type(value) is dict and set(value)=={d['name'] for d in defs},'STATUS-FORWARD-RETURN-VALUE-TYPE')
  for d in defs:need(type(value[d['name']]) is {'str':str,'int':int,'bool':bool}[d['type']],'STATUS-FORWARD-RETURN-FIELD-TYPE:'+d['name'])
 status_typed_same(case['returned'],hops,'STATUS-FORWARD-RETURN-LINKS')
 terminal=events[-1];exception=None if completion=='process-termination' else completion in ('intentional-fixed-raise','unexpected-raise')
 classification={'modeled_kind':completion,'terminal_stage':terminal['stage'],'stage_outcome':terminal['outcome'],'location':'internal-status path; not a _dispatch invocation','dispatch_catch_applicable':False,'status_forwarder_local_catch':False,'terminal_python_exception_in_model':exception,'unexpected_raise_outside_dispatch_catch':completion=='unexpected-raise','runtime_exception_evidence':'UNAVAILABLE','runtime_unwind_evidence':'UNAVAILABLE','retention_cleanup_or_authority_established':False}
 destinations=[]
 if completion=='normal-return':destinations.append({'kind':'status-reference','to':catalogue['destinations']['normal_status'],'reference':copy.deepcopy(refs['result'])})
 elif completion!='process-termination':destinations.append({'kind':completion,'to':'calling trusted control path conditional on ordinary exception propagation','exact_exception':fixed,'outer_handler_or_cleanup_reached':None})
 return {'kind':'CONSTRUCTED-INTERNAL-STATUS-FORWARD','occurrence':case['occurrence'],'scope':copy.deepcopy(scope),'reference_bindings':copy.deepcopy(refs),'arguments':arguments,'events':events,'hops':hops,'completion':completion,'outcome_classification':classification,'fixed_failure':fixed,'destinations':destinations,'conditional_dictionary_value':copy.deepcopy(result),'prior_owner_failure':{'present':refs['owner_failed'],'cleared':False,'exact_value':None},'runtime_observation':False,'physical_object_identity_observed':False,'reference_symbols_are_conditional':True,'source_phase_type_check_is_history_proof':False,'retained_error':None,'cleanup_completion':None,'new_output_permission':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_status_forward_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'STATUS-FORWARD-SUBMITTED-OUTPUT')
 status_typed_same(submitted,status_forward_projection(catalogue,case,validated),'STATUS-FORWARD-PROJECTION-CORRESPONDENCE');return True


def token_registration_source(launcher,entry,status,client,boundary):
 """Reuse reviewed source checks, then traverse the defining _run independently."""
 need(type(launcher) is bytes and type(entry) is bytes,'TOKEN-SOURCE-TYPE')
 for v in (status,client,boundary):status_exact_tree(v,'TOKEN-SOURCE-INPUT')
 validate_status_forward(launcher,entry,status['manager_fields'],boundary,status)
 validate_client_handle(launcher,entry,client['manager_relation'],boundary,client)
 tree,loc=_client_locate(entry);run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run')
 outer=run.body[2];with_=outer.body[0];owner,token,insert,protected=with_.body
 control,callback,stored=protected.body;remove=protected.finalbody[0]
 # The entire _run AST was checked above; these are source-derived nodes and
 # guards, independent of a submitted/generated stage catalogue.
 need(isinstance(protected,ast.Try) and not protected.handlers and len(protected.finalbody)==1,'TOKEN-FINALLY-STRUCTURE')
 need(isinstance(callback,ast.Try) and len(callback.body)==1,'TOKEN-CALLBACK-STRUCTURE')
 steps=[('owner-create',owner),('token-create',token),('registry-insert',insert),('control-guard',control.test),('control-create',control.body[0].value.args[0]),('control-callback',control.body[0]),('client-create',callback.body[0].value.args[0]),('client-callback',callback.body[0]),('owner-failure-guard',stored.test),('finally-enter',protected),('removal-attempt',remove.value),('removal-complete',remove)]
 anchors={name:{**loc(node),'source':{'bytes':len(entry),'sha256':digest(entry)}} for name,node in steps}
 need(any(g['kind']=='try' and g['region']=='finalbody' for g in loc(remove)['guards']),'TOKEN-REMOVAL-IN-FINALLY')
 return {'entry':{'bytes':len(entry),'sha256':digest(entry)},'run':loc(run),'stages':anchors,'order':[n for n,_ in steps],
  'control_guard':ast.unparse(control.test),'stored_failure_guard':ast.unparse(stored.test),'stored_failure_raise':loc(stored.body[0]),
  'insert':{'registry':ast.unparse(insert.targets[0].value),'key':ast.unparse(insert.targets[0].slice),'value':ast.unparse(insert.value)},
  'remove':{'receiver':ast.unparse(remove.value.func.value),'method':remove.value.func.attr,'key':ast.unparse(remove.value.args[0]),'default':ast.literal_eval(remove.value.args[1]),'return_consumed':False},
  'before_launcher_exit':True,'callback_returns_forwarded':False,'exceptional_continuation':'Existing outer/error/cleanup path, outside this slice'}

def compile_token_registration(launcher,entry,status,client,boundary):
 source=token_registration_source(launcher,entry,status,client,boundary)
 edges=[]
 for edge in client['reference_edges']+status['reference_edges']:
  if edge not in edges:edges.append(copy.deepcopy(edge))
 return {'format':'I164-TOKEN-REGISTRATION-STATIC-1','source':source,'reference_edges':edges,
  'declarations':[{'id':stage,'source_origin':copy.deepcopy(source['stages'][stage]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for stage in source['order']],
  'guard_branches':{'control':['None: skip control creation/callback','non-None: normal control callback required before client'],
   'stored_failure':['None: normal callback-to-finally path','non-None: exceptional continuation outside this slice'],
   'stage_outcome':['normal','raise: stop at exceptional frontier','process-termination: no inferred Python unwind','unobserved: stop without continuation']},
  'reference_semantics':{'token':'fresh object() symbol per selected _run invocation; not an observed address','owner':'fresh _Owner(wrapper) reference; wrapper is the selected validated instance representation','client_control':'distinct constructors, same selected token; control exists only on selected non-None branch','registry':'one invocation-qualified slot, not an inventory of global _OWNERS','equal_values_identify_objects':False},
  'removal_semantics':{'finally_entry_is_not_attempt':True,'attempt_is_not_completion':True,'pop_return_is_discarded':True,'normal_pop':'selected key absent at the operation completion under exact builtins; not permanent absence','selected_owner_removal':'requires explicit conditional continuity premise; not inferred from callback return or discarded pop result','concurrency_exclusivity_or_durability_proved':False},
  'boundary_contract':copy.deepcopy(status['boundary_contract']),'boundary_adoption':copy.deepcopy(status['boundary_adoption']),
  'termination_contract':copy.deepcopy(client['outside_catch_failure_contract']),
  'runtime_registration_revocation':None,'outer_lifecycle_complete':False,'actual_admission':False}

def validate_token_registration(launcher,entry,status,client,boundary,submitted):
 status_exact_tree(submitted,'TOKEN-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_token_registration(launcher,entry,status,client,boundary),'TOKEN-SOURCE-CORRESPONDENCE');return True

def token_reference_premises(scope,control_present):
 status_exact_tree(scope,'TOKEN-SCOPE');need(type(control_present) is bool,'TOKEN-CONTROL-TYPE')
 need(type(scope) is dict and set(scope)=={'context','acquisition','instance','frontier','invocation'} and scope['context'] in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO') and type(scope['invocation']) is str and bool(scope['invocation']),'TOKEN-SCOPE-SHAPE')
 # Canonical symbols are relational model names, not physical identity evidence.
 refs={n:{'scope':copy.deepcopy(scope),'symbol':scope['invocation']+'/'+n+'-symbol'} for n in ('token','owner','session','manager','client')}
 refs['control']={'scope':copy.deepcopy(scope),'symbol':scope['invocation']+'/control-symbol'} if control_present else None
 refs.update({'client.token':copy.deepcopy(refs['token']),'control.token':copy.deepcopy(refs['token']) if control_present else None,'owners[token]':copy.deepcopy(refs['owner']),'owner.wrapper':copy.deepcopy(refs['session']),'session.managed':copy.deepcopy(refs['manager'])})
 return refs

def token_registration_projection(catalogue,case,validated):
 """Finite conditional slice. validated comes from the mandatory evidence adapter.

 Outcomes and continuity are explicit constructed premises, never observations.
 Registry continuity is not proved by the callback, pop return or source anchor.
 """
 for x in (catalogue,case,validated):status_exact_tree(x,'TOKEN-EXACT-TYPE')
 keys={'occurrence','scope','references','control_present','owner_failure_none','registry_continuity','outcomes'}
 need(type(case) is dict and set(case)==keys and type(validated) is dict and set(validated)==keys-{'references'},'TOKEN-CASE-SHAPE')
 for k in validated:status_typed_same(case[k],validated[k],'TOKEN-PREMISE:'+k)
 for k in ('control_present','owner_failure_none','registry_continuity'):need(type(case[k]) is bool,'TOKEN-BOOL:'+k)
 scope=case['scope'];refs=token_reference_premises(scope,case['control_present']);need(type(case['occurrence']) is str and case['occurrence']==scope['invocation'],'TOKEN-OCCURRENCE')
 status_typed_same(case['references'],refs,'TOKEN-REFERENCES')
 # Source-derived catalogue is mandatory in the adapter. Do not accept a case's
 # supplied step order as the coverage oracle.
 order=[n for n in catalogue['source']['order'] if case['control_present'] or n not in ('control-create','control-callback')]
 outcomes=case['outcomes'];need(type(outcomes) is list and bool(outcomes),'TOKEN-OUTCOMES')
 events=[];completed=set();completion=None;terminal=None
 for i,stage in enumerate(order):
  need(i<len(outcomes),'TOKEN-MISSING-STEP:'+stage);row=outcomes[i]
  need(type(row) is dict and set(row)=={'stage','outcome'} and type(row['stage']) is str and row['stage']==stage,'TOKEN-STEP-ORDER')
  kind=row['outcome'];need(type(kind) is str and kind in ('normal','raise','process-termination','unobserved'),'TOKEN-OUTCOME-KIND')
  events.append({'id':case['occurrence']+'/'+stage,'scope':copy.deepcopy(scope),'stage':stage,'source':copy.deepcopy(catalogue['source']['stages'][stage]),'outcome':kind,'frame':None});terminal=kind
  if kind!='normal':completion={'raise':'unexpected-raise','process-termination':'process-termination','unobserved':'unobserved-continuation'}[kind];break
  completed.add(stage)
  if stage=='owner-failure-guard' and not case['owner_failure_none']:completion='stored-failure-exceptional-frontier';break
  if stage=='removal-complete':completion='normal-pop-completion'
 need(len(events)==len(outcomes),'TOKEN-UNREACHED-STEP')
 # Prefix creation/insertion acknowledgements establish only conditional model
 # state. Absence of completion never means absence of effects.
 popped='removal-complete' in completed;inserted='registry-insert' in completed
 before={'key':copy.deepcopy(refs['token']),'owner':copy.deepcopy(refs['owner']) if inserted and case['registry_continuity'] else None,'continuity':'explicit constructed premise' if case['registry_continuity'] else 'UNKNOWN'}
 exception=None if terminal in ('process-termination','unobserved') or completion=='stored-failure-exceptional-frontier' else terminal=='raise'
 return {'kind':'CONSTRUCTED-TOKEN-REGISTRATION','occurrence':case['occurrence'],'scope':copy.deepcopy(scope),'reference_bindings':copy.deepcopy(refs),'events':events,'completion':completion,
  'registration_completed_in_model':inserted,'control_callback_completed_in_model':('control-callback' in completed) if case['control_present'] else None,'client_callback_completed_in_model':'client-callback' in completed,
  'finally_entered_in_model':'finally-enter' in completed,'removal_attempt_entered_in_model':'removal-attempt' in completed,'removal_completed_in_model':popped,
  'selected_slot_before_removal':before,'selected_owner_removed_in_model':True if popped and inserted and case['registry_continuity'] else None,
  'slot_after_pop_in_model':'ABSENT-AT-POP-COMPLETION' if popped else 'UNKNOWN','revocation_persists':None,
  'callback_return_destination':None,'pop_return_value':None,'physical_object_identity_observed':False,'runtime_observation':False,
  'outcome_classification':{'modeled_kind':completion,'terminal_stage':events[-1]['stage'],'stage_outcome':terminal,'location':'_run orchestration, outside _dispatch catch; source outer BaseException and finally remain conditional','terminal_python_exception_in_model':exception,'runtime_python_exception_evidence':'UNAVAILABLE','runtime_unwind_evidence':'UNAVAILABLE','outer_handler_or_cleanup_reached':None},
  'retained_error':None,'database_cleanup_completion':None,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_token_registration_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'TOKEN-SUBMITTED-OUTPUT');status_typed_same(submitted,token_registration_projection(catalogue,case,validated),'TOKEN-PROJECTION-CORRESPONDENCE');return True


# Normal session-exit correspondence, additive to the reviewed token producer.
def session_exit_source(launcher,entry,manager,token):
 need(all(type(v) is bytes for v in (launcher,entry,manager)),'EXIT-SOURCE-TYPE');status_exact_tree(token,'EXIT-TOKEN-CATALOGUE')
 status_typed_same({'bytes':len(entry),'sha256':digest(entry)},token['source']['entry'],'EXIT-ENTRY-BINDING')
 lt,ll=_client_locate(launcher);et,el=_client_locate(entry);mt,ml=_client_locate(manager)
 def fn(tree,name):return next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
 run=fn(et,'_run');session=fn(lt,'session');launch=fn(lt,'_session');lock=fn(lt,'owner_lock')
 # Existing token validation has checked full _run/client/launcher error source.
 # Independently traverse the actual launcher tail and public generator bridge.
 with_=run.body[2].body[0];protected=with_.body[-1];pop=protected.finalbody[0]
 tr=launch.body[-1].body[-1];need(isinstance(tr,ast.Try),'EXIT-LAUNCHER-TRY');yield_,close,clear,unlink=tr.body[-4:]
 status_typed_same([ast.unparse(x) for x in (yield_,close,clear,unlink)],['yield ManagedSession(managed)','managed.close()','managed = None',"(dest / 'ACTIVE.json').unlink()"],'EXIT-LAUNCHER-SEQUENCE')
 bridge=session.body[-1];need(isinstance(bridge,ast.With),'EXIT-PUBLIC-BRIDGE');status_typed_same(ast.unparse(bridge),'with _session(*args, **kwargs) as managed:\n    yield managed','EXIT-PUBLIC-BRIDGE-SOURCE')
 status_typed_same(ast.unparse(with_.items[0].context_expr),'launcher.session(candidate, draft, runtime, destination, create=create)','EXIT-RUN-SESSION')
 status_typed_same(ast.unparse(pop),'_OWNERS.pop(token, None)','EXIT-POP-SOURCE')
 need(not unlink.value.args and not unlink.value.keywords,'EXIT-UNLINK-ARGUMENTS')
 need(isinstance(unlink.value.func.value,ast.BinOp) and isinstance(unlink.value.func.value.op,ast.Div),'EXIT-MARKER-EXPRESSION')
 need(ast.unparse(unlink.value.func.value.left)=='dest' and type(unlink.value.func.value.right.value) is str,'EXIT-MARKER-ROOT')
 cls=next(n for n in mt.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority');mc=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='close')
 status_typed_same(ast.unparse(mc),"def close(self):\n    with self._lock:\n        self._quarantine('explicit close')\n        self._dispose()\n        self._phase = 'CLOSED'\n        self._reason = 'close confirmed; no serving connection'",'EXIT-MANAGED-CLOSE-SOURCE')
 selected=[('session-resume',bridge.body[0]),('launcher-resume',yield_),('close-attempt',close.value),('close-complete',close),('managed-clear',clear),('unlink-attempt',unlink.value),('unlink-complete',unlink)]
 pin={'bytes':len(launcher),'sha256':digest(launcher)}
 return {'launcher':pin,'entry':{'bytes':len(entry),'sha256':digest(entry)},'manager':{'bytes':len(manager),'sha256':digest(manager)},'stages':{n:{**ll(node),'source':copy.deepcopy(pin)} for n,node in selected},'order':[n for n,_ in selected],
  'run_context':el(with_),'pop':el(pop),'session_bridge':ll(bridge),'owner_lock_destination':ll(lock),'manager_close':ml(mc),
  'marker_component':unlink.value.func.value.right.value,'marker_expression':ast.unparse(unlink.value.func.value),'unlink_args':[],'unlink_kwargs':{},'missing_ok_argument':'omitted; pathlib.Path.unlink default False','missing_file':'FileNotFoundError is not suppressed by this unlink call; launcher handler remains an exceptional frontier',
  'close_return':None,'local_clear':ast.literal_eval(clear.value),'normal_phase':mc.body[0].body[-2].value.value,'normal_reason':mc.body[0].body[-1].value.value,
  'exception_region':ll(tr.handlers[0]),'outer_lifecycle_complete':False}

def compile_session_exit(launcher,entry,manager,token,reference):
 status_exact_tree(reference,'EXIT-REFERENCE-CATALOGUE');source=session_exit_source(launcher,entry,manager,token)
 status_typed_same(source['manager'],{k:reference['source']['source'][k] for k in ('bytes','sha256')},'EXIT-REFERENCE-SOURCE')
 need(any(p['function']=='close' for p in reference['source']['programs']),'EXIT-CLOSE-REFERENCE-PROGRAM')
 return {'format':'I164-NORMAL-SESSION-EXIT-STATIC-1','source':source,
  'declarations':[{'id':n,'source_origin':copy.deepcopy(source['stages'][n]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in source['order']],
  'token_precondition':'Same selected invocation; validated normal-pop-completion. Selected-owner removal retains the separate continuity premise.',
  'reference_edges':[['run.wrapper','session'],['launcher.yielded_wrapper','session'],['launcher.managed','manager'],['session.managed','manager']],
  'reference_close_program':copy.deepcopy(next(p for p in reference['source']['programs'] if p['function']=='close')),
  'guards':['ordinary resumption after normal pop','close attempt only after launcher resumption','normal close completion independently checked by existing managed reference-path interpreter','local managed clear only after normal close return','unlink attempt only after local clear','normal unlink completion is not implied by marker absence'],
  'preserved_distinctions':['source references versus physical identity','local managed clear versus underlying close','marker unlink attempt versus completion','normal call versus durable closure','namespace absence versus successful earlier operations','earlier acknowledged facts versus later uncertainty'],
  'exceptional_and_outer_cleanup':'Existing source anchored, not expanded','runtime_exit_chain':None,'actual_admission':False}

def validate_session_exit(launcher,entry,manager,token,reference,submitted):
 status_exact_tree(submitted,'EXIT-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_session_exit(launcher,entry,manager,token,reference),'EXIT-SOURCE-CORRESPONDENCE');return True

def session_exit_projection(catalogue,case,validated):
 for v in (catalogue,case,validated):status_exact_tree(v,'EXIT-EXACT-TYPE')
 keys={'scope','references','session_binding','marker_path','token_result','close_result','outcomes','marker_at_unlink'}
 need(type(case) is dict and set(case)==keys and type(validated) is dict and set(validated)==keys,'EXIT-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'EXIT-VALIDATED:'+k)
 scope=case['scope'];token=case['token_result'];status_typed_same(token['scope'],scope,'EXIT-TOKEN-SCOPE')
 need(type(case['outcomes']) is list and type(case['marker_at_unlink']) is str and case['marker_at_unlink'] in ('present','absent','UNKNOWN'),'EXIT-INPUT-TYPES')
 normal=token['completion']=='normal-pop-completion' and token['removal_completed_in_model'] is True
 events=[];done=set();completion='predecessor-not-normal';terminal=None;cr=case['close_result'];close_reached=False
 if normal:
  for i,stage in enumerate(catalogue['source']['order']):
   need(i<len(case['outcomes']),'EXIT-MISSING-STEP:'+stage);r=case['outcomes'][i]
   need(type(r) is dict and set(r)=={'stage','outcome'} and type(r['stage']) is str and r['stage']==stage,'EXIT-STEP-ORDER')
   kind=r['outcome'];allowed=('normal','raise','process-termination','unobserved')+(('missing-file',) if stage=='unlink-complete' else ())
   need(type(kind) is str and kind in allowed,'EXIT-OUTCOME');terminal=kind
   if stage=='close-complete':
    close_reached=True
    if cr is None:need(kind in ('process-termination','unobserved'),'EXIT-MISSING-CLOSE-RELATION')
    elif cr['completion']=='normal':
     need(kind=='normal','EXIT-CONTRADICTED-CLOSE-COMPLETION');need(cr['final']=={'_live':None,'_retired':None,'_phase':catalogue['source']['normal_phase']},'EXIT-NORMAL-CLOSE-STATE')
    elif cr['completion']=='abrupt':need(kind=='raise','EXIT-CLOSE-RAISE-CORRESPONDENCE')
    else:need(cr['completion']=='partial-prefix' and kind in ('process-termination','unobserved'),'EXIT-CLOSE-PREFIX-CORRESPONDENCE')
   if stage=='unlink-complete':
    need(not (case['marker_at_unlink']=='absent' and kind=='normal'),'EXIT-ABSENT-UNLINK-NOT-SUPPRESSED')
    need(not (case['marker_at_unlink']=='present' and kind=='missing-file'),'EXIT-MARKER-FACT-CONTRADICTION')
   events.append({'id':scope['invocation']+'/'+stage,'scope':copy.deepcopy(scope),'stage':stage,'source':copy.deepcopy(catalogue['source']['stages'][stage]),'outcome':kind,'manager':copy.deepcopy(case['references']['manager']),'wrapper':copy.deepcopy(case['references']['session']),'session_binding':copy.deepcopy(case['session_binding']),'marker_path':copy.deepcopy(case['marker_path']),'runtime_frame':None})
   if kind!='normal':completion={'raise':'exceptional-frontier','missing-file':'unlink-FileNotFoundError-frontier','process-termination':'process-termination','unobserved':'unobserved-continuation'}[kind];break
   done.add(stage)
   if stage=='unlink-complete':completion='normal-marker-unlink-completion'
 need(len(events)==len(case['outcomes']),'EXIT-UNREACHED-STEPS')
 if not close_reached:need(cr is None,'EXIT-UNREACHED-CLOSE-RELATION')
 clear='managed-clear' in done;closed='close-complete' in done;unlinked='unlink-complete' in done
 exc=True if terminal in ('raise','missing-file') else False if terminal=='normal' else None
 return {'kind':'CONSTRUCTED-NORMAL-SESSION-EXIT','scope':copy.deepcopy(scope),'reference_bindings':copy.deepcopy(case['references']),'session_binding':copy.deepcopy(case['session_binding']),'marker_path':copy.deepcopy(case['marker_path']),
  'validated_token_prefix':copy.deepcopy(token),'selected_owner_removed_in_model':token['selected_owner_removed_in_model'],'continuity_premise':copy.deepcopy(token['selected_slot_before_removal']['continuity']),
  'events':events,'completion':completion,'close_attempt_entered_in_model':'close-attempt' in done,'close_normal_completion_in_model':closed,'managed_close_return':None,'managed_close_relation':copy.deepcopy(cr),
  'launcher_local_cleared_in_model':clear,'launcher_local_managed_after':None if clear else copy.deepcopy(case['references']['manager']),
  'wrapper_manager_reference_after':copy.deepcopy(case['references']['manager']),'unlink_attempt_entered_in_model':'unlink-attempt' in done,'marker_removal_completed_in_model':unlinked,
  'marker_namespace_fact':'ABSENT-AT-UNLINK-COMPLETION' if unlinked else 'ABSENT-REPORTED-BY-UNLINK' if terminal=='missing-file' else 'UNKNOWN',
  'exception_class':'FileNotFoundError' if terminal=='missing-file' else None,'terminal_python_exception_in_model':exc,'runtime_unwind_evidence':'UNAVAILABLE','runtime_exit_chain':None,
  'completion_flags_mean':'True = acknowledged in this conditional prefix; False = not established, not proof of no effects','physical_closure_established':False,'durability_established':False,'runtime_exclusivity_established':False,'marker_absence_persists':None,
  'outer_context_exit_or_lock_release_established':False,'outer_cleanup_completion':None,'retained_error':None,'runtime_observation':False,'observer_join':None,'obligations_discharged':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_session_exit_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'EXIT-SUBMITTED-OUTPUT');status_typed_same(submitted,session_exit_projection(catalogue,case,validated),'EXIT-OUTPUT-CORRESPONDENCE');return True


# Bounded owner-lock descriptor finalization; no OS operation is executed.
def owner_finalization_source(launcher,exit_catalogue):
 need(type(launcher) is bytes,'OWNER-SOURCE-TYPE');status_exact_tree(exit_catalogue,'OWNER-EXIT-CATALOGUE')
 pin={'bytes':len(launcher),'sha256':digest(launcher)};status_typed_same(pin,exit_catalogue['source']['launcher'],'OWNER-EXIT-SOURCE')
 tree,loc=_client_locate(launcher);funcs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)};lock=funcs['owner_lock'];launch=funcs['_session']
 expected=ast.parse("""@contextlib.contextmanager
def owner_lock(destination):
 dest=Path(destination).absolute();require(dest.name not in ('','.','..'),'DESTINATION')
 parent=dest.parent.resolve();require(parent.is_dir(),'MISSING-PARENT')
 dest=parent/dest.name
 fd=os.open(parent/('.'+dest.name+'.owner.lock'),os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
 try:
  try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:raise Blocked('OWNER-LOCK-CONTENDED')
  yield dest
 finally:os.close(fd)
""").body[0]
 status_typed_same(ast.dump(lock,include_attributes=False),ast.dump(expected,include_attributes=False),'OWNER-DEFINING-SHAPE')
 alloc=lock.body[-2];tr=lock.body[-1];yield_=tr.body[-1];close=tr.finalbody[0];outer=launch.body[-1]
 need(isinstance(outer,ast.With) and ast.unparse(outer.items[0].context_expr)=='owner_lock(destination)' and ast.unparse(outer.items[0].optional_vars)=='dest','OWNER-SESSION-CONTEXT')
 need(outer is launch.body[-1] and isinstance(outer.body[-1],ast.Try),'OWNER-NORMAL-TAIL')
 tail=outer.body[-1].body[-1];status_typed_same(loc(tail),{k:v for k,v in exit_catalogue['source']['stages']['unlink-complete'].items() if k!='source'},'OWNER-VALIDATED-UNLINK')
 status_typed_same(ast.unparse(tail),"(dest / 'ACTIVE.json').unlink()",'OWNER-NORMAL-PREDECESSOR')
 need(any(g['kind']=='try' and g['region']=='finalbody' for g in loc(close)['guards']),'OWNER-FINALBODY-GUARD')
 stage_nodes=[('owner-finalizer-enter',tr),('descriptor-close-attempt',close.value),('descriptor-close-complete',close)]
 return {'launcher':pin,'owner_lock':loc(lock),'owner_lock_call':loc(outer.items[0].context_expr),'descriptor_assignment':loc(alloc),'descriptor_call':loc(alloc.value),'descriptor_slot':alloc.targets[0].id,'close_argument':loc(close.value.args[0]),'close_callee':ast.unparse(close.value.func),'close_arguments':[ast.unparse(a) for a in close.value.args],'close_keywords':[],
  'open_arguments':[ast.unparse(a) for a in alloc.value.args],'open_keywords':[],'path_expression':ast.unparse(alloc.value.args[0]),'path_prefix':alloc.value.args[0].right.left.left.value,'path_suffix':alloc.value.args[0].right.right.value,'yield':loc(yield_),'normal_predecessor':loc(tail),'session_with':loc(outer),
  'order':[n for n,_ in stage_nodes],'stages':{n:{**loc(node),'source':copy.deepcopy(pin),'semantic_region':'finally-entry' if n=='owner-finalizer-enter' else 'finalbody'} for n,node in stage_nodes},
  'return_use':'os.close(fd) is an expression statement; its return value is discarded, not captured','source_binding_rule':'fd is the result of this owner_lock invocation\'s os.open; no intervening fd assignment in the defining source','normal_guard':'Validated normal unlink completion, normal completion of enclosing launcher try/body and ordinary resumption of this owner_lock generator','exceptional_finalizer':'The source finally also applies to exceptional exits; those routes are outside this normal-only construction, not ruled out'}

def compile_owner_finalization(launcher,exit_catalogue):
 source=owner_finalization_source(launcher,exit_catalogue)
 return {'format':'I164-OWNER-LOCK-FINALIZATION-STATIC-1','source':source,'descriptor_declaration':{'id':'owner-lock-descriptor-result','source_origin':copy.deepcopy(source['descriptor_assignment']),'call_origin':copy.deepcopy(source['descriptor_call']),'slot':source['descriptor_slot'],'type':'source-qualified os.open result passed as fd to os.close; numeric value unobserved','classification':'UNKNOWN','multiplicity':None,'ordinal':None},
  'declarations':[{'id':n,'source_origin':copy.deepcopy(source['stages'][n]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in source['order']],
  'guard_branches':{'normal_predecessor':'Only normal-marker-unlink-completion enters this normal-only relation','other_predecessor':'No stages in this slice; exceptional finalization remains unexpanded, not disproved','ordered_normal_prefix':'Every following stage requires the previous modeled stage to complete normally','failure_or_unknown':'Stop immediately; no later completion or automatic retry'},
  'identity_rule':'Context, acquisition, instance, selected invocation, owner_lock call and os.open origin qualify lineage. A descriptor number, path or equal value is not resource identity.',
  'limits':['SOURCE-ONLY static/constructed relation','No runtime descriptor, physical resource identity, physical lock-release, exclusive ownership or durability claim','No complete exceptional/outer lifecycle','No new logging, allowance, retention or authorization'],
  'runtime_finalizer_chain':None,'actual_admission':False}

def validate_owner_finalization(launcher,exit_catalogue,submitted):
 status_exact_tree(submitted,'OWNER-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_owner_finalization(launcher,exit_catalogue),'OWNER-SOURCE-CORRESPONDENCE');return True

def owner_descriptor_lineage(catalogue,scope,session_binding,marker_path):
 for v in (catalogue,scope,session_binding,marker_path):status_exact_tree(v,'OWNER-LINEAGE-TYPES')
 source=catalogue['source'];inv=scope['invocation'];need(inv is None or type(inv) is str and bool(inv),'OWNER-INVOCATION')
 dest=session_binding['recorded_destination'];need(type(dest) is str and '/' in dest,'OWNER-RECORDED-DESTINATION');parent,name=dest.rstrip('/').rsplit('/',1)
 return {'kind':'SOURCE-QUALIFIED-OWNER-DESCRIPTOR','scope':copy.deepcopy(scope),'owner_lock_occurrence':None if inv is None else inv+'/owner-lock','descriptor_result_occurrence':None if inv is None else inv+'/owner-lock/os.open-result','slot':source['descriptor_slot'],'producer':copy.deepcopy(source['descriptor_call']),'assignment':copy.deepcopy(source['descriptor_assignment']),'source':copy.deepcopy(source['launcher']),'owner_lock_call':copy.deepcopy(source['owner_lock_call']),
  'session_binding':copy.deepcopy(session_binding),'marker_path':copy.deepcopy(marker_path),'lock_path':{'root':'owner_lock resolved parent','expression':source['path_expression'],'nominal_recorded_path':parent+'/'+source['path_prefix']+name+source['path_suffix'],'physical_resolved_path':None},
  'close_argument_origin':copy.deepcopy(source['close_argument']),'source_lineage':'Same local fd result; no intervening reassignment in the pinned source','numeric_value':None,'runtime_descriptor_identity':None,'physical_resource_identity':None,'exclusive_owner_established':False}

def owner_finalization_projection(catalogue,case,validated):
 for v in (catalogue,case,validated):status_exact_tree(v,'OWNER-EXACT-TYPE')
 keys={'scope','session_binding','marker_path','references','exit_result','descriptor','outcomes'}
 need(type(case) is dict and set(case)==keys and type(validated) is dict and set(validated)==keys,'OWNER-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'OWNER-VALIDATED:'+k)
 scope=case['scope'];prior=case['exit_result'];status_typed_same(scope,prior['scope'],'OWNER-PREDECESSOR-SCOPE')
 status_typed_same(case['descriptor'],owner_descriptor_lineage(catalogue,scope,case['session_binding'],case['marker_path']),'OWNER-DESCRIPTOR-LINEAGE')
 normal=prior['completion']=='normal-marker-unlink-completion' and prior['marker_removal_completed_in_model'] is True
 need(type(case['outcomes']) is list,'OWNER-OUTCOMES');events=[];done=set();terminal=None;completion='outside-normal-finalization-slice'
 if normal:
  for i,stage in enumerate(catalogue['source']['order']):
   need(i<len(case['outcomes']),'OWNER-MISSING-STEP:'+stage);row=case['outcomes'][i]
   need(type(row) is dict and set(row)=={'stage','outcome'} and type(row['stage']) is str and row['stage']==stage,'OWNER-STEP-ORDER');outcome=row['outcome']
   need(type(outcome) is str and outcome in ('normal','raise','process-termination','unobserved'),'OWNER-OUTCOME');terminal=outcome
   events.append({'id':scope['invocation']+'/'+stage,'scope':copy.deepcopy(scope),'source':copy.deepcopy(catalogue['source']['stages'][stage]),'stage':stage,'outcome':outcome,'descriptor_result_occurrence':case['descriptor']['descriptor_result_occurrence'],'descriptor':copy.deepcopy(case['descriptor']),'manager':copy.deepcopy(case['references']['manager']),'session':copy.deepcopy(case['references']['session']),'runtime_frame':None})
   if outcome!='normal':completion={'raise':'exceptional-frontier','process-termination':'process-termination','unobserved':'unobserved-continuation'}[outcome];break
   done.add(stage)
   if stage=='descriptor-close-complete':completion='normal-descriptor-close-completion'
 need(len(events)==len(case['outcomes']),'OWNER-UNREACHED-STEPS')
 return {'kind':'CONSTRUCTED-OWNER-LOCK-FINALIZATION','scope':copy.deepcopy(scope),'descriptor_lineage':copy.deepcopy(case['descriptor']),'reference_bindings':copy.deepcopy(case['references']),'validated_normal_exit_prefix':copy.deepcopy(prior),'events':events,'completion':completion,'normal_route_applicable':normal,
  'finalizer_entry_completed_in_model':'owner-finalizer-enter' in done,'descriptor_close_attempt_entered_in_model':'descriptor-close-attempt' in done,'descriptor_close_normal_completion_in_model':'descriptor-close-complete' in done,
  'descriptor_close_return_use':catalogue['source']['return_use'],'descriptor_close_return_observation':None,'selected_owner_removed_in_model':prior['selected_owner_removed_in_model'],'continuity_premise':copy.deepcopy(prior['continuity_premise']),
  'terminal_python_exception_in_model':True if terminal=='raise' else False if terminal=='normal' else None,'completion_flags_mean':'True = acknowledged in this conditional prefix; False = not established, not proof of no effects. Outside this normal slice does not rule out exceptional finalization.',
  'physical_descriptor_closure_established':False,'physical_lock_release_established':False,'exclusive_ownership_established':False,'runtime_descriptor_finalization':None,'runtime_unwind_evidence':'UNAVAILABLE','durability_established':False,'complete_outer_context_exit_established':False,'exceptional_outer_cleanup_completion':None,'retained_error':None,'runtime_observation':False,'observer_join':None,'obligations_discharged':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_owner_finalization_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'OWNER-SUBMITTED-OUTPUT');status_typed_same(submitted,owner_finalization_projection(catalogue,case,validated),'OWNER-OUTPUT-CORRESPONDENCE');return True


def stored_failure_source(launcher,entry,token,handle,state):
 """Select the exceptional continuation independently from defining source."""
 for v in (token,handle,state):status_exact_tree(v,'STORED-SOURCE-INPUT')
 checked=client_handle_source(launcher,entry,handle['manager_relation'])
 pin={'bytes':len(entry),'sha256':digest(entry)}
 status_typed_same(token['source']['entry'],pin,'STORED-TOKEN-SOURCE')
 status_typed_same(state['source']['sources'],checked['sources'],'STORED-STATE-SOURCE')
 tree,loc=_client_locate(entry);funcs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)};run=funcs['_run'];dispatch=funcs['_dispatch']
 protected=run.body[2].body[0].body[-1];control,callback,guard=protected.body;raise_=guard.body[0];pop=protected.finalbody[0];storage=dispatch.body[2].handlers[0].body[0]
 need(isinstance(callback,ast.Try) and ast.unparse(callback.body[0])=='client(Client(token))','STORED-CALLBACK')
 need(ast.unparse(guard.test)=='owner.failure is not None' and ast.unparse(raise_)=='raise owner.failure' and raise_.cause is None,'STORED-RETHROW')
 need(not protected.handlers and len(protected.finalbody)==1 and ast.unparse(pop)=='_OWNERS.pop(token, None)','STORED-FINALLY')
 need(ast.unparse(storage)=='owner.failure = error','STORED-ERROR-STORAGE')
 status_typed_same(loc(raise_),token['source']['stored_failure_raise'],'STORED-PRIOR-RAISE-ANCHOR')
 status_typed_same(loc(guard.test),{k:v for k,v in token['source']['stages']['owner-failure-guard'].items() if k!='source'},'STORED-PRIOR-GUARD')
 stages=[('stored-error-rethrow',raise_),('finally-enter',protected),('removal-attempt',pop.value),('removal-complete',pop)]
 return {'sources':checked['sources'],'run':loc(run),'storage':loc(storage),'callback':loc(callback.body[0]),'guard':loc(guard.test),'raise':loc(raise_),'finally':loc(protected),'pop':loc(pop),
  'order':[n for n,_ in stages],'stages':{n:{**loc(node),'source':copy.deepcopy(pin),'semantic_region':'finally-entry' if n=='finally-enter' else 'source-statement'} for n,node in stages},
  'guard_expression':ast.unparse(guard.test),'raise_expression':ast.unparse(raise_),'explicit_cause':None,'explicit_cause_clause_present':False,'pop_key':ast.unparse(pop.value.args[0]),'pop_default':ast.literal_eval(pop.value.args[1]),'pop_return_consumed':False,
  'predecessor':'Validated token stored-failure-exceptional-frontier after normal client callback and non-None failure guard','storage_origin':'Existing validated Client.handle or Client.state failure projector, not a supplied error summary',
  'guard_slot_premise':'The selected local owner.failure at this guard is the same validated stored original error. Constructed source-state premise, not proof of arbitrary callback behavior or intervening history.',
  'cleanup_rule':'A raised original/evaluation exception enters the enclosing finally under ordinary Python continuation; later finally/removal raise replaces the pending outward exception for this prefix. Termination/unobserved continuation supplies no unwind.'}

def compile_stored_failure(launcher,entry,token,handle,state):
 source=stored_failure_source(launcher,entry,token,handle,state)
 return {'format':'I164-STORED-FAILURE-STATIC-1','source':source,'declarations':[{'id':n,'source_origin':copy.deepcopy(source['stages'][n]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in source['order']],
  'guard_branches':{'failure_provenance':['stored original with intentional fixed client failure','stored original with unexpected escaping helper raise','termination cannot establish callback normal return'],'callback':'normal return with validated earlier storage; not successful _run completion','guard':'owner.failure is the selected stored original, not None','rethrow':['raised-original: intentional source raise, not normal function return','raise: conditional evaluation/interruption exception, not guaranteed original','process-termination: no finally inference','unobserved: no finally inference'],'finally':['normal continuation to next point','raise ends this prefix with a replacement error','process-termination or unobserved stops without completion']},
  'reference_rule':'Parent invocation-qualified owner/token; child operation-qualified original error joined by explicit source forwarding/storage relations, not equal-message or observed physical identity.',
  'limits':['Static/constructed only','Selected-owner registry continuity remains an explicit premise','Guard-slot error continuity is an explicit constructed source-state premise','No complete outer handler, launcher cleanup, database close, retained evidence bytes, physical lock release, exclusivity or authorization'],
  'runtime_rethrow_revocation_chain':None,'actual_admission':False}

def validate_stored_failure(launcher,entry,token,handle,state,submitted):
 status_exact_tree(submitted,'STORED-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_stored_failure(launcher,entry,token,handle,state),'STORED-SOURCE-CORRESPONDENCE');return True

def stored_failure_projection(catalogue,case,validated):
 for v in (catalogue,case,validated):status_exact_tree(v,'STORED-EXACT-TYPE')
 keys={'scope','references','token_prefix','failure_provenance','stored_error_binding','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'STORED-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'STORED-VALIDATED:'+k)
 scope=case['scope'];prefix=case['token_prefix'];failure=case['failure_provenance'];binding=case['stored_error_binding'];original=binding['error']
 status_typed_same(scope,prefix['scope'],'STORED-PREFIX-SCOPE');status_typed_same(case['references'],prefix['reference_bindings'],'STORED-PREFIX-REFERENCES')
 need(prefix['completion']=='stored-failure-exceptional-frontier' and prefix['client_callback_completed_in_model'] is True,'STORED-PREFIX-FRONTIER')
 need(failure['retained_original'] is True and failure['completion'] in ('fixed-client-failure','unqualified-escape') and original is not None,'STORED-VALIDATED-STORAGE')
 status_typed_same(original,failure['original_exception'],'STORED-ERROR-PROVENANCE');status_typed_same(binding['owner'],case['references']['owner'],'STORED-ERROR-OWNER')
 need(binding['guard_slot_premise']==catalogue['source']['guard_slot_premise'],'STORED-GUARD-PREMISE')
 outcomes=case['outcomes'];need(type(outcomes) is list and bool(outcomes),'STORED-OUTCOMES');events=[];done=set();pending=None;cleanup_error=None;completion=None;terminal=None;rethrow=False
 for i,stage in enumerate(catalogue['source']['order']):
  need(i<len(outcomes),'STORED-MISSING-STEP:'+stage);row=outcomes[i];need(type(row) is dict and set(row)=={'stage','outcome'} and row['stage']==stage,'STORED-STEP-ORDER')
  outcome=row['outcome'];allowed=('raised-original','raise','process-termination','unobserved') if i==0 else ('normal','raise','process-termination','unobserved');need(type(outcome) is str and outcome in allowed,'STORED-STAGE-OUTCOME');terminal=outcome
  event={'id':scope['invocation']+'/'+stage,'scope':copy.deepcopy(scope),'stage':stage,'source':copy.deepcopy(catalogue['source']['stages'][stage]),'outcome':outcome,'owner':copy.deepcopy(case['references']['owner']),'token':copy.deepcopy(case['references']['token']),'pending_error_on_entry':copy.deepcopy(pending),'runtime_frame':None};events.append(event)
  if outcome in ('process-termination','unobserved'):
   completion=outcome;break
  if stage=='stored-error-rethrow':
   if outcome=='raised-original':rethrow=True;done.add(stage);pending=copy.deepcopy(original)
   else:pending={'kind':'conditional-rethrow-evaluation-exception','reference':scope['invocation']+'/rethrow-evaluation-error','exact_type':None,'source':copy.deepcopy(catalogue['source']['stages'][stage])}
   continue
  if outcome=='raise':
   cleanup_error={'kind':'conditional-finally-exception','reference':scope['invocation']+'/'+stage+'/error','exact_type':None,'source':copy.deepcopy(catalogue['source']['stages'][stage])};pending=copy.deepcopy(cleanup_error);completion='cleanup-exceptional-frontier';break
  done.add(stage)
  if stage=='removal-complete':completion='normal-removal-pending-original' if rethrow else 'normal-removal-pending-evaluation-error'
 need(len(events)==len(outcomes),'STORED-UNREACHED-STEPS');popped='removal-complete' in done
 continuity=copy.deepcopy(prefix['selected_slot_before_removal']);selected=True if popped and continuity['continuity']=='explicit constructed premise' else None
 return {'kind':'CONSTRUCTED-STORED-FAILURE-REVOCATION','scope':copy.deepcopy(scope),'reference_bindings':copy.deepcopy(case['references']),'validated_token_prefix':copy.deepcopy(prefix),'validated_failure_provenance':copy.deepcopy(failure),'stored_error_binding':copy.deepcopy(binding),'original_error':copy.deepcopy(original),'events':events,'completion':completion,
  'failure_storage_previously_completed_in_model':True,'callback_returned_normally_in_model':True,'run_success_established':False,'source_original_rethrow_completed_in_model':rethrow,'finally_entry_completed_in_model':'finally-enter' in done,'removal_attempt_entered_in_model':'removal-attempt' in done,'removal_completed_in_model':popped,
  'selected_slot_before_removal':continuity,'selected_owner_removed_in_model':selected,'slot_after_pop_in_model':'ABSENT-AT-POP-COMPLETION' if popped else 'UNKNOWN','pop_result_observation':None,'revocation_persists':None,
  'last_pending_error_in_model':copy.deepcopy(pending),'cleanup_error_in_model':cleanup_error,'outward_error_after_finally_in_model':copy.deepcopy(pending) if popped else None,'original_outward_after_finally_established_in_model':popped and rethrow,'original_reaches_launcher_established':False,'terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True,
  'exception_context_observation':None,'runtime_unwind_evidence':'UNAVAILABLE','runtime_observation':False,'physical_reference_identity':None,'runtime_rethrow_revocation_chain':None,'outer_cleanup_completion':None,'database_cleanup_completion':None,'retained_failure_record_bytes':None,'physical_lock_release_established':False,'exclusive_ownership_established':False,'durability_established':False,'observer_join':None,
  'completion_flags_mean':'Established only in this constructed prefix; false does not prove absence of unobserved effects. Prior storage is preserved across every later frontier. No original propagation guarantee after replacement cleanup error or termination.',
  'obligations_discharged':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_stored_failure_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'STORED-SUBMITTED-OUTPUT');status_typed_same(submitted,stored_failure_projection(catalogue,case,validated),'STORED-OUTPUT-CORRESPONDENCE');return True


def callback_failure_source(launcher,entry,stored,token,handle,state):
 """Derive the callback handler from the defining AST, not a claim catalogue."""
 validate_stored_failure(launcher,entry,token,handle,state,stored)
 tree,loc=_client_locate(entry);run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run');protected=run.body[2].body[0].body[-1];callback=protected.body[1];handler=callback.handlers[0];guard=handler.body[0];raise_=guard.body[0]
 need(len(callback.handlers)==1 and ast.unparse(handler.type)=='BaseException' and handler.name=='client_error','CALLBACK-HANDLER')
 need(len(handler.body)==2 and isinstance(handler.body[1],ast.Raise) and handler.body[1].exc is None,'CALLBACK-BARE-OTHER-BRANCH')
 need(ast.unparse(guard.test)=='owner.failure is not None' and len(guard.body)==1 and not guard.orelse,'CALLBACK-STORED-GUARD')
 need(ast.unparse(raise_.exc)=='owner.failure' and isinstance(raise_.cause,ast.Name) and raise_.cause.id==handler.name,'CALLBACK-EXPLICIT-CAUSE')
 pin={'bytes':len(entry),'sha256':digest(entry)}
 stages=[('callback-handler-enter',handler),('callback-failure-guard',guard.test),('callback-stored-rethrow',raise_)]
 anchors={n:{**loc(node),'source':copy.deepcopy(pin),'semantic_region':'handler-entry' if n=='callback-handler-enter' else 'source-statement'} for n,node in stages}
 for n in ('finally-enter','removal-attempt','removal-complete'):anchors[n]=copy.deepcopy(stored['source']['stages'][n])
 return {'sources':copy.deepcopy(stored['source']['sources']),'run':loc(run),'callback_call':loc(callback.body[0]),'handler':loc(handler),'guard':loc(guard.test),'raise':loc(raise_),'bare_raise_outside_slice':loc(handler.body[1]),'storage':copy.deepcopy(stored['source']['storage']),
  'order':[n for n,_ in stages]+['finally-enter','removal-attempt','removal-complete'],'stages':anchors,'catch_family':ast.unparse(handler.type),'exception_binding':handler.name,'guard_expression':ast.unparse(guard.test),'raise_expression':ast.unparse(raise_.exc),'cause_expression':ast.unparse(raise_.cause),'explicit_cause_clause_present':True,
  'reused_revocation':{k:copy.deepcopy(stored['source'][k]) for k in ('finally','pop','pop_key','pop_default','pop_return_consumed')},
  'guard_slot_premise':'At the selected callback-handler guard, local owner.failure is the same previously validated stored original. Conditional source-state premise, not intervening history or arbitrary callback safety.',
  'predecessor':'Validated token registration prefix ending with selected client-callback raise; no normal callback completion and no inferred handler/finally entry',
  'source_error_roles':'Stored original and caught client_error are separate semantic roles. Role-reference inequality does not assert physically distinct exception objects; self-cause is not excluded. Exact type/value/history of client_error is unavailable.',
  'continuation':'A modeled handler/guard/rethrow evaluation exception skips later handler stages and enters finally under ordinary Python continuation. A finally/removal exception ends this slice and may replace the pending error. Termination/unobserved continuation never establishes unwind.'}

def compile_callback_failure(launcher,entry,stored,token,handle,state):
 source=callback_failure_source(launcher,entry,stored,token,handle,state)
 return {'format':'I164-CALLBACK-FAILURE-STATIC-1','source':source,'declarations':[{'id':n,'source_origin':copy.deepcopy(source['stages'][n]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in source['order']],
  'guard_branches':{'callback':'selected client call raises BaseException; not normal callback return','stored_failure':'selected non-None original under explicit guard-slot premise; None/bare raise outside this slice','stored_provenance':copy.deepcopy(stored['guard_branches']['failure_provenance']),
   'handler':['normal: advance to non-None guard then source raise','raise: evaluation/interruption error replaces pending callback error and enters finally','process-termination/unobserved: stop without inferred unwind'],
   'rethrow':['raised-stored-from-client: stored original raised with caught callback error as explicit cause','raise: evaluation/interruption error, no established explicit-cause assignment','process-termination/unobserved: no inferred raise or finally'],
   'revocation':['normal: next source point','raise: replacement cleanup error, no guaranteed original propagation or completion','process-termination/unobserved: no later completion']},
  'normal_callback_relation':'Reviewed stored_failure_revocation_correspondence remains mandatory and byte-preserved through predecessor validation',
  'limits':['Static/constructed only','Guard-slot and selected-owner registry continuity are explicit premises','No physical reference equality or inequality from model role names','Callback exception exact producer, type, bytes and runtime frames unavailable','No full launcher cleanup, durability, physical lock release or exclusivity','No bare-raise/control callback expansion'],
  'runtime_callback_cause_revocation_chain':None,'actual_admission':False}

def validate_callback_failure(launcher,entry,stored,token,handle,state,submitted):
 status_exact_tree(submitted,'CALLBACK-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_callback_failure(launcher,entry,stored,token,handle,state),'CALLBACK-SOURCE-CORRESPONDENCE');return True

def callback_error_binding(catalogue,scope):
 status_exact_tree(scope,'CALLBACK-ERROR-SCOPE')
 return {'role':'caught-callback-exception','scope':copy.deepcopy(scope),'occurrence':scope['invocation']+'/callback-exception','reference':scope['invocation']+'/client_error','source':copy.deepcopy(catalogue['source']['handler']),
  'binding_name':catalogue['source']['exception_binding'],'catch_family':catalogue['source']['catch_family'],'exact_type':None,'exact_value_bytes':None,'producer_history':'UNAVAILABLE','physical_identity_relative_to_stored':'UNKNOWN','runtime_reference_observation':None}

def callback_failure_projection(catalogue,case,validated):
 for v in (catalogue,case,validated):status_exact_tree(v,'CALLBACK-EXACT-TYPE')
 keys={'scope','references','token_prefix','failure_provenance','stored_error_binding','callback_error','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'CALLBACK-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'CALLBACK-VALIDATED:'+k)
 scope=case['scope'];refs=case['references'];prefix=case['token_prefix'];failure=case['failure_provenance'];binding=case['stored_error_binding'];original=binding['error'];client=case['callback_error']
 status_typed_same(scope,prefix['scope'],'CALLBACK-PREFIX-SCOPE');status_typed_same(refs,prefix['reference_bindings'],'CALLBACK-PREFIX-REFERENCES')
 need(prefix['completion']=='unexpected-raise' and prefix['client_callback_completed_in_model'] is False and prefix['events'][-1]['stage']=='client-callback' and prefix['events'][-1]['outcome']=='raise','CALLBACK-PREFIX-FRONTIER')
 need(prefix['registration_completed_in_model'] is True,'CALLBACK-REGISTERED-PREFIX')
 need(failure['retained_original'] is True and failure['completion'] in ('fixed-client-failure','unqualified-escape') and type(original) is dict,'CALLBACK-VALIDATED-STORAGE')
 status_typed_same(original,failure['original_exception'],'CALLBACK-ORIGINAL-PROVENANCE');status_typed_same(binding['owner'],refs['owner'],'CALLBACK-STORED-OWNER');status_typed_same(binding['guard_slot_premise'],catalogue['source']['guard_slot_premise'],'CALLBACK-GUARD-PREMISE');status_typed_same(client,callback_error_binding(catalogue,scope),'CALLBACK-ERROR-BINDING')
 outcomes=case['outcomes'];need(type(outcomes) is list and bool(outcomes),'CALLBACK-OUTCOMES')
 order=catalogue['source']['order'];index=0;cursor=0;events=[];done=set();pending=copy.deepcopy(client);cause=None;evaluation=None;cleanup=None;completion=None;terminal=None
 while cursor<len(order):
  stage=order[cursor];need(index<len(outcomes),'CALLBACK-MISSING-STEP:'+stage);row=outcomes[index];index+=1
  need(type(row) is dict and set(row)=={'stage','outcome'} and row['stage']==stage,'CALLBACK-STEP-ORDER');kind=row['outcome']
  allowed=('raised-stored-from-client','raise','process-termination','unobserved') if stage=='callback-stored-rethrow' else ('normal','raise','process-termination','unobserved')
  need(type(kind) is str and kind in allowed,'CALLBACK-STAGE-OUTCOME');terminal=kind
  events.append({'id':scope['invocation']+'/'+stage,'scope':copy.deepcopy(scope),'stage':stage,'source':copy.deepcopy(catalogue['source']['stages'][stage]),'outcome':kind,'owner':copy.deepcopy(refs['owner']),'token':copy.deepcopy(refs['token']),'pending_error_on_entry':copy.deepcopy(pending),'runtime_frame':None})
  if kind in ('process-termination','unobserved'):completion=kind;break
  if cursor<3:
   if kind=='raise':
    evaluation={'role':'conditional-handler-evaluation-exception','reference':scope['invocation']+'/'+stage+'/error','scope':copy.deepcopy(scope),'source':copy.deepcopy(catalogue['source']['stages'][stage]),'exact_type':None,'physical_identity':None};pending=copy.deepcopy(evaluation);cursor=3;continue
   done.add(stage)
   if stage=='callback-stored-rethrow':
    pending=copy.deepcopy(original);cause={'raised_error':copy.deepcopy(original),'explicit_cause':copy.deepcopy(client),'source':copy.deepcopy(catalogue['source']['raise']),'expression':'raise owner.failure from client_error','suppress_context_in_model':True,'implicit_context_observation':None,'physical_identity_relative_to_stored':'UNKNOWN','runtime_observation':False}
  elif kind=='raise':
   cleanup={'role':'conditional-finally-exception','reference':scope['invocation']+'/'+stage+'/error','scope':copy.deepcopy(scope),'source':copy.deepcopy(catalogue['source']['stages'][stage]),'exact_type':None,'physical_identity':None};pending=copy.deepcopy(cleanup);completion='cleanup-exceptional-frontier';break
  else:done.add(stage)
  cursor+=1
  if stage=='removal-complete':completion='normal-removal-pending-stored' if cause is not None else 'normal-removal-pending-evaluation-error'
 need(index==len(outcomes),'CALLBACK-UNREACHED-STEPS');popped='removal-complete' in done;continuity=copy.deepcopy(prefix['selected_slot_before_removal']);removed=True if popped and continuity['continuity']=='explicit constructed premise' else None
 return {'kind':'CONSTRUCTED-CALLBACK-STORED-FAILURE','scope':copy.deepcopy(scope),'reference_bindings':copy.deepcopy(refs),'validated_token_prefix':copy.deepcopy(prefix),'validated_failure_provenance':copy.deepcopy(failure),'stored_error_binding':copy.deepcopy(binding),'original_error':copy.deepcopy(original),'callback_error':copy.deepcopy(client),'events':events,'completion':completion,
  'failure_storage_previously_completed_in_model':True,'callback_returned_normally_in_model':False,'callback_raised_in_model':True,'callback_handler_entry_completed_in_model':'callback-handler-enter' in done,'non_none_guard_completed_in_model':'callback-failure-guard' in done,'source_stored_rethrow_with_cause_completed_in_model':cause is not None,'established_explicit_cause':copy.deepcopy(cause),'handler_evaluation_error_in_model':evaluation,'cleanup_error_in_model':cleanup,
  'finally_entry_completed_in_model':'finally-enter' in done,'removal_attempt_entered_in_model':'removal-attempt' in done,'removal_completed_in_model':popped,'selected_slot_before_removal':continuity,'selected_owner_removed_in_model':removed,'slot_after_pop_in_model':'ABSENT-AT-POP-COMPLETION' if popped else 'UNKNOWN','pop_result_observation':None,'revocation_persists':None,
  'last_pending_error_in_model':copy.deepcopy(pending),'outward_error_after_finally_in_model':copy.deepcopy(pending) if popped else None,'original_outward_after_finally_established_in_model':popped and cause is not None,'original_reaches_launcher_established':False,'terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True,
  'role_relationship':'Separate semantic roles/occurrences; neither physical equality nor inequality established. Explicit cause is the selected client_error even if it aliases the stored object.','run_success_established':False,'runtime_observation':False,'runtime_callback_cause_revocation_chain':None,'runtime_unwind_evidence':'UNAVAILABLE','physical_reference_identity':None,'implicit_context_observation':None,'outer_cleanup_completion':None,'database_cleanup_completion':None,'retained_failure_record_bytes':None,'physical_lock_release_established':False,'exclusive_ownership_established':False,'durability_established':False,'observer_join':None,
  'completion_flags_mean':'Established only in this finite conditional prefix; false is not proof of absence of unobserved effects. Earlier storage and completed cause assignment survive later uncertainty; no original outward guarantee after cleanup failure or termination.',
  'obligations_discharged':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_callback_failure_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'CALLBACK-SUBMITTED-OUTPUT');status_typed_same(submitted,callback_failure_projection(catalogue,case,validated),'CALLBACK-OUTPUT-CORRESPONDENCE');return True

# Bounded callback exception with an exactly None selected owner.failure slot.
def callback_bare_source(launcher,entry,callback,stored,token,handle,state):
 validate_callback_failure(launcher,entry,stored,token,handle,state,callback)
 tree,loc=_client_locate(entry);run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run')
 handlers=[n for n in ast.walk(run) if isinstance(n,ast.ExceptHandler) and n.name=='client_error']
 need(len(handlers)==1,'BARE-UNIQUE-CALLBACK-HANDLER');handler=handlers[0]
 need(len(handler.body)==2 and isinstance(handler.body[0],ast.If) and isinstance(handler.body[1],ast.Raise),'BARE-HANDLER-SHAPE')
 guard=handler.body[0];bare=handler.body[1];test=guard.test
 need(isinstance(test,ast.Compare) and isinstance(test.left,ast.Attribute) and isinstance(test.left.value,ast.Name) and test.left.value.id=='owner' and test.left.attr=='failure' and len(test.ops)==len(test.comparators)==1 and isinstance(test.ops[0],ast.IsNot) and isinstance(test.comparators[0],ast.Constant) and test.comparators[0].value is None,'BARE-EXACT-NONE-GUARD')
 need(not guard.orelse and bare.exc is None and bare.cause is None,'BARE-NO-EXPRESSION-OR-CAUSE')
 source=callback['source'];pin=source['sources']['entry'];points=[('callback-handler-enter',handler),('callback-none-guard',test),('callback-bare-rethrow',bare)]
 stages={n:{**loc(node),'source':copy.deepcopy(pin),'semantic_region':'handler-entry' if n=='callback-handler-enter' else 'source-statement'} for n,node in points}
 for n in ('finally-enter','removal-attempt','removal-complete'):stages[n]=copy.deepcopy(source['stages'][n])
 return {'sources':copy.deepcopy(source['sources']),'run':loc(run),'callback_call':copy.deepcopy(source['callback_call']),'handler':loc(handler),'guard':loc(test),'raise':loc(bare),'order':[n for n,_ in points]+['finally-enter','removal-attempt','removal-complete'],'stages':stages,'catch_family':source['catch_family'],'exception_binding':source['exception_binding'],
  'guard_expression':ast.unparse(test),'selected_guard_result':False,'selected_slot_expression':ast.unparse(test.left),'selected_slot_value':None,'selected_slot_exact_type':'NoneType','raise_expression':None,'cause_expression':None,'raise_syntax':ast.unparse(bare),'bare_raise_has_explicit_cause_clause':False,'reused_revocation':copy.deepcopy(source['reused_revocation']),
  'guard_slot_premise':'At this selected callback-handler guard, the same local owner.failure slot is exactly None. Conditional source-state premise only; not a history of no prior storage, no mutation or arbitrary callback safety.',
  'error_continuity':'The active caught callback exception remains selected through normally completed handler/guard/bare raise. Evaluation/interruption errors may replace the pending error; role identities are not observed physical addresses.',
  'chain_semantics':'Bare raise reraises the selected active callback exception without a new explicit cause assignment. Existing __cause__, __context__ and __suppress_context__ remain UNKNOWN, not absent or cleared.',
  'continuation':source['continuation']}

def compile_callback_bare(launcher,entry,callback,stored,token,handle,state):
 source=callback_bare_source(launcher,entry,callback,stored,token,handle,state)
 return {'format':'I164-CALLBACK-BARE-STATIC-1','source':source,'declarations':[{'id':n,'source_origin':copy.deepcopy(source['stages'][n]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in source['order']],
  'guard_branches':{'callback':'Selected callback raises BaseException; normal callback return is not established','slot':'owner.failure is not None evaluates False because the selected slot is exactly None under explicit continuity premise','bare_raise':'Reraise the selected active callback exception; no new explicit cause assignment; existing cause/context/suppression UNKNOWN','handler_or_raise_interruption':'A modeled evaluation/interruption raise skips remaining handler stages and conditionally proceeds to finally with a replacement error','cleanup':'A later finally/removal raise may replace the pending error; no removal completion or callback propagation guarantee','termination_or_unobserved':'No inferred Python unwind or later completion'},
  'preserved_relations':['stored_failure_revocation_correspondence','callback_stored_failure_correspondence'],'limits':['Static conditional scope, not runtime execution','Exact None at this guard does not prove no earlier failure storage or clear retained evidence','No new exception chain evidence or physical reference identity','Guard-slot and selected-owner continuity are explicit premises','Full outer cleanup and control callback exceptions remain unexpanded'],'runtime_callback_bare_revocation_chain':None,'actual_admission':False}

def validate_callback_bare(launcher,entry,callback,stored,token,handle,state,submitted):
 status_exact_tree(submitted,'BARE-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_callback_bare(launcher,entry,callback,stored,token,handle,state),'BARE-SOURCE-CORRESPONDENCE');return True

def callback_bare_projection(catalogue,case,validated):
 for v in (catalogue,case,validated):status_exact_tree(v,'BARE-EXACT-TYPE')
 keys={'scope','references','token_prefix','none_guard_binding','callback_error','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'BARE-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'BARE-VALIDATED:'+k)
 scope=case['scope'];refs=case['references'];prefix=case['token_prefix'];binding=case['none_guard_binding'];client=case['callback_error']
 status_typed_same(scope,prefix['scope'],'BARE-PREFIX-SCOPE');status_typed_same(refs,prefix['reference_bindings'],'BARE-PREFIX-REFERENCES')
 need(prefix['registration_completed_in_model'] is True and prefix['completion']=='unexpected-raise' and prefix['client_callback_completed_in_model'] is False and prefix['events'][-1]['stage']=='client-callback' and prefix['events'][-1]['outcome']=='raise','BARE-PREFIX-FRONTIER')
 status_typed_same(binding['owner'],refs['owner'],'BARE-GUARD-OWNER');status_typed_same(binding['scope'],scope,'BARE-GUARD-SCOPE');need(binding['slot_value'] is None and binding['guard_result'] is False,'BARE-NONE-GUARD')
 status_typed_same(binding['premise'],catalogue['source']['guard_slot_premise'],'BARE-GUARD-PREMISE');status_typed_same(client,callback_error_binding(catalogue,scope),'BARE-CALLBACK-ERROR')
 outcomes=case['outcomes'];need(type(outcomes) is list and bool(outcomes),'BARE-OUTCOMES');order=catalogue['source']['order'];cursor=0;index=0;events=[];done=set();pending=copy.deepcopy(client);evaluation=None;cleanup=None;completion=None;terminal=None
 while cursor<len(order):
  stage=order[cursor];need(index<len(outcomes),'BARE-MISSING-STEP:'+stage);row=outcomes[index];index+=1
  need(type(row) is dict and set(row)=={'stage','outcome'} and row['stage']==stage,'BARE-STEP-ORDER');kind=row['outcome']
  allowed=('reraised-callback','raise','process-termination','unobserved') if stage=='callback-bare-rethrow' else ('normal','raise','process-termination','unobserved')
  need(type(kind) is str and kind in allowed,'BARE-STAGE-OUTCOME');terminal=kind
  events.append({'id':scope['invocation']+'/'+stage,'scope':copy.deepcopy(scope),'stage':stage,'source':copy.deepcopy(catalogue['source']['stages'][stage]),'outcome':kind,'owner':copy.deepcopy(refs['owner']),'token':copy.deepcopy(refs['token']),'pending_error_on_entry':copy.deepcopy(pending),'runtime_frame':None})
  if kind in ('process-termination','unobserved'):completion=kind;break
  if cursor<3:
   if kind=='raise':
    evaluation={'role':'conditional-handler-evaluation-exception','reference':scope['invocation']+'/'+stage+'/error','scope':copy.deepcopy(scope),'source':copy.deepcopy(catalogue['source']['stages'][stage]),'exact_type':None,'physical_identity':None};pending=copy.deepcopy(evaluation);cursor=3;continue
   done.add(stage)
   if stage=='callback-bare-rethrow':pending=copy.deepcopy(client)
  elif kind=='raise':
   cleanup={'role':'conditional-finally-exception','reference':scope['invocation']+'/'+stage+'/error','scope':copy.deepcopy(scope),'source':copy.deepcopy(catalogue['source']['stages'][stage]),'exact_type':None,'physical_identity':None};pending=copy.deepcopy(cleanup);completion='cleanup-exceptional-frontier';break
  else:done.add(stage)
  cursor+=1
  if stage=='removal-complete':completion='normal-removal-pending-callback' if 'callback-bare-rethrow' in done else 'normal-removal-pending-evaluation-error'
 need(index==len(outcomes),'BARE-UNREACHED-STEPS');popped='removal-complete' in done;reraised='callback-bare-rethrow' in done;continuity=copy.deepcopy(prefix['selected_slot_before_removal']);removed=True if popped and continuity['continuity']=='explicit constructed premise' else None
 return {'kind':'CONSTRUCTED-CALLBACK-BARE-RETHROW','scope':copy.deepcopy(scope),'reference_bindings':copy.deepcopy(refs),'validated_token_prefix':copy.deepcopy(prefix),'none_guard_binding':copy.deepcopy(binding),'callback_error':copy.deepcopy(client),'events':events,'completion':completion,
  'callback_raised_in_model':True,'callback_returned_normally_in_model':False,'callback_handler_entry_completed_in_model':'callback-handler-enter' in done,'none_guard_completed_in_model':'callback-none-guard' in done,'bare_rethrow_completed_in_model':reraised,'reraised_error_in_model':copy.deepcopy(client) if reraised else None,
  'bare_raise_semantics':{'adds_explicit_cause':False,'preserves_active_exception':True,'establishes_absent_existing_cause_or_context':False},'exception_chain_observation':{'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','physical_reference_observation':None},'new_explicit_cause_assignment_established_in_model':False,'handler_evaluation_error_in_model':evaluation,'cleanup_error_in_model':cleanup,
  'finally_entry_completed_in_model':'finally-enter' in done,'removal_attempt_entered_in_model':'removal-attempt' in done,'removal_completed_in_model':popped,'selected_slot_before_removal':continuity,'selected_owner_removed_in_model':removed,'slot_after_pop_in_model':'ABSENT-AT-POP-COMPLETION' if popped else 'UNKNOWN','pop_result_observation':None,'revocation_persists':None,
  'last_pending_error_in_model':copy.deepcopy(pending),'outward_error_after_finally_in_model':copy.deepcopy(pending) if popped else None,'callback_outward_after_finally_established_in_model':popped and reraised,'callback_reaches_launcher_established':False,'terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True,
  'prior_failure_storage_history':'UNKNOWN; the None guard does not erase any earlier established storage or evidence','run_success_established':False,'runtime_observation':False,'runtime_callback_bare_revocation_chain':None,'runtime_unwind_evidence':'UNAVAILABLE','physical_reference_identity':None,'outer_cleanup_completion':None,'database_cleanup_completion':None,'retained_failure_record_bytes':None,'physical_lock_release_established':False,'exclusive_ownership_established':False,'durability_established':False,'observer_join':None,
  'completion_flags_mean':'Established only in this finite conditional prefix; false is not proof of absence of unobserved effects. Earlier acknowledged facts survive interruption or termination; no later cleanup or callback propagation is guaranteed.',
  'obligations_discharged':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_callback_bare_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'BARE-SUBMITTED-OUTPUT');status_typed_same(submitted,callback_bare_projection(catalogue,case,validated),'BARE-OUTPUT-CORRESPONDENCE');return True

# Additive control-callback exceptional continuation. Historical functions unchanged.
def control_exception_source(launcher,entry,bare,callback,stored,token,handle,state):
 validate_callback_bare(launcher,entry,callback,stored,token,handle,state,bare)
 tree,loc=_client_locate(entry);run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run')
 protected=run.body[2].body[0].body[-1]
 need(isinstance(protected,ast.Try) and not protected.handlers and not protected.orelse and len(protected.body)==3 and len(protected.finalbody)==1,'CONTROL-PROTECTED-TRY')
 control,client,postclient=protected.body;pop=protected.finalbody[0]
 need(isinstance(control,ast.If) and not control.orelse and len(control.body)==1,'CONTROL-GUARD-SHAPE')
 guard=control.test;stmt=control.body[0];call=stmt.value
 need(isinstance(guard,ast.Compare) and isinstance(guard.left,ast.Name) and guard.left.id=='control' and len(guard.ops)==len(guard.comparators)==1 and isinstance(guard.ops[0],ast.IsNot) and isinstance(guard.comparators[0],ast.Constant) and guard.comparators[0].value is None,'CONTROL-EXACT-NONNONE-GUARD')
 need(isinstance(stmt,ast.Expr) and isinstance(call,ast.Call) and ast.unparse(call)=='control(_Control(token))','CONTROL-SELECTED-CALL')
 need(isinstance(client,ast.Try) and ast.unparse(client.body[0])=='client(Client(token))' and client.lineno>stmt.end_lineno,'CONTROL-CLIENT-HANDLER-NOT-CONTAINING-CONTROL')
 need(ast.unparse(pop)=='_OWNERS.pop(token, None)' and isinstance(pop,ast.Expr),'CONTROL-POP')
 pin={'bytes':len(entry),'sha256':digest(entry)}
 for name,node in [('control-guard',guard),('control-create',call.args[0]),('control-callback',stmt),('finally-enter',protected),('removal-attempt',pop.value),('removal-complete',pop)]:
  status_typed_same(token['source']['stages'][name],{**loc(node),'source':copy.deepcopy(pin)},'CONTROL-REUSED-STAGE:'+name)
 points=[('finally-enter',protected),('removal-attempt',pop.value),('removal-complete',pop)]
 return {'sources':copy.deepcopy(stored['source']['sources']),'run':loc(run),'control_guard':loc(guard),'guard_expression':ast.unparse(guard),'selected_guard_result':True,'control_constructor':loc(call.args[0]),'control_call':loc(stmt),'callee_expression':ast.unparse(call.func),'argument_expression':ast.unparse(call.args[0]),'client_handler':loc(client.handlers[0]),
  'order':[n for n,_ in points],'stages':{n:{**loc(node),'source':copy.deepcopy(pin),'semantic_region':'finally-entry' if n=='finally-enter' else 'source-statement'} for n,node in points},
  'prefix_order':token['source']['order'][:token['source']['order'].index('control-callback')+1],
  'client_handler_applies':False,'owner_failure_guard_applies':False,'new_explicit_cause_assignment':False,'local_exception_binding':None,
  'pop_key':ast.unparse(pop.value.args[0]),'pop_default':ast.literal_eval(pop.value.args[1]),'pop_return_consumed':False,
  'continuation':'Selected control constructor completed and actual control callback raises. Ordinary Python continuation enters this finally; the subsequent client try and post-client guard are not reached on this route. Cleanup may replace pending propagation; termination is not unwind.',
  'continuity':'Selected registry key/owner continuity is an explicit conditional premise, not exclusive ownership or arbitrary callback safety.'}

def compile_control_exception(launcher,entry,bare,callback,stored,token,handle,state):
 source=control_exception_source(launcher,entry,bare,callback,stored,token,handle,state)
 return {'format':'I164-CONTROL-EXCEPTION-STATIC-1','source':source,'token_relation':copy.deepcopy(token),
  'declarations':[{'id':n,'source_origin':copy.deepcopy(source['stages'][n]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in source['order']],
  'guard_branches':{'prefix':'control is not None; _Control(token) construction completed; selected control callback raises','continuation':'Ordinary continuation enters finally; each later stage requires preceding normal completion','cleanup_raise':'Stop with separate pending cleanup exception; original control exception remains an earlier established role','termination_or_unobserved':'Stop without inferred Python unwind, later removal or outward propagation','client':'No subsequent client creation/callback/handler or owner.failure guard on this route'},
  'preserved_relations':['token_registration_correspondence','stored_failure_revocation_correspondence','callback_stored_failure_correspondence','callback_bare_rethrow_correspondence'],
  'limits':['Static constructed scope; unavailable runtime control/finally/removal chain','Existing cause/context/suppression UNKNOWN, not cleared or absent','Constructor failure and full outer cleanup remain unexpanded','Symbolic role/reference correspondence is not observed physical identity','No owner.failure condition or history inferred'],
  'runtime_control_exception_revocation_chain':None,'actual_admission':False}

def validate_control_exception(launcher,entry,bare,callback,stored,token,handle,state,submitted):
 status_exact_tree(submitted,'CONTROL-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_control_exception(launcher,entry,bare,callback,stored,token,handle,state),'CONTROL-SOURCE-CORRESPONDENCE');return True

def control_exception_binding(catalogue,scope):
 status_exact_tree(scope,'CONTROL-ERROR-SCOPE')
 return {'role':'selected-control-callback-exception','scope':copy.deepcopy(scope),'occurrence':scope['invocation']+'/control-callback/exception','reference':scope['invocation']+'/control-callback/error','callback_occurrence':scope['invocation']+'/control-callback','callback_argument_reference':copy.deepcopy(token_reference_premises(scope,True)['control']),'source':copy.deepcopy(catalogue['source']['control_call']),
  'callee':'selected control argument of this _run invocation','local_handler_binding':None,'exact_type':None,'exact_value_bytes':None,'producer_history':'UNAVAILABLE','existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_reference_observation':None}

def control_exception_projection(catalogue,case,validated):
 for v in (catalogue,case,validated):status_exact_tree(v,'CONTROL-EXACT-TYPE')
 keys={'scope','references','token_inputs','token_prefix','control_error','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'CONTROL-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'CONTROL-VALIDATED:'+k)
 scope=case['scope'];refs=case['references'];prefix=case['token_prefix'];ti=case['token_inputs'];error=case['control_error'];source=catalogue['source']
 status_typed_same(refs,token_reference_premises(scope,True),'CONTROL-REFERENCE-ROLES');status_typed_same(scope,ti['scope'],'CONTROL-TOKEN-SCOPE')
 need(ti['control_present'] is True,'CONTROL-REQUIRES-CONTROL')
 expected_steps=[{'stage':n,'outcome':'raise' if n=='control-callback' else 'normal'} for n in source['prefix_order']]
 status_typed_same(ti['outcomes'],expected_steps,'CONTROL-SELECTED-PREFIX')
 tv={k:copy.deepcopy(v) for k,v in ti.items() if k!='references'}
 status_typed_same(prefix,token_registration_projection(catalogue['token_relation'],ti,tv),'CONTROL-VALIDATED-TOKEN-PREFIX')
 status_typed_same(refs,prefix['reference_bindings'],'CONTROL-PREFIX-REFERENCES')
 need(prefix['registration_completed_in_model'] is True and prefix['completion']=='unexpected-raise' and prefix['control_callback_completed_in_model'] is False and prefix['client_callback_completed_in_model'] is False,'CONTROL-REGISTERED-RAISE-FRONTIER')
 status_typed_same(error,control_exception_binding(catalogue,scope),'CONTROL-SELECTED-ERROR')
 outcomes=case['outcomes'];need(type(outcomes) is list and bool(outcomes),'CONTROL-OUTCOMES');events=[];done=set();pending=copy.deepcopy(error);cleanup=None;terminal=None;completion=None
 for i,stage in enumerate(source['order']):
  need(i<len(outcomes),'CONTROL-MISSING-STEP:'+stage);row=outcomes[i]
  need(type(row) is dict and set(row)=={'stage','outcome'} and row['stage']==stage,'CONTROL-STEP-ORDER');kind=row['outcome']
  need(type(kind) is str and kind in ('normal','raise','process-termination','unobserved'),'CONTROL-STAGE-OUTCOME');terminal=kind
  events.append({'id':scope['invocation']+'/'+stage,'scope':copy.deepcopy(scope),'stage':stage,'source':copy.deepcopy(source['stages'][stage]),'outcome':kind,'owner':copy.deepcopy(refs['owner']),'token':copy.deepcopy(refs['token']),'control':copy.deepcopy(refs['control']),'pending_error_on_entry':copy.deepcopy(pending),'runtime_frame':None})
  if kind in ('process-termination','unobserved'):completion=kind;break
  if kind=='raise':
   cleanup={'role':'conditional-finally-exception','reference':scope['invocation']+'/'+stage+'/error','scope':copy.deepcopy(scope),'source':copy.deepcopy(source['stages'][stage]),'exact_type':None,'physical_identity':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN'};pending=copy.deepcopy(cleanup);completion='cleanup-exceptional-frontier';break
  done.add(stage)
  if stage=='removal-complete':completion='normal-removal-pending-control-error'
 need(len(events)==len(outcomes),'CONTROL-UNREACHED-STEPS');popped='removal-complete' in done;continuity=copy.deepcopy(prefix['selected_slot_before_removal']);removed=True if popped and continuity['continuity']=='explicit constructed premise' else None
 return {'kind':'CONSTRUCTED-CONTROL-EXCEPTION','scope':copy.deepcopy(scope),'reference_bindings':copy.deepcopy(refs),'validated_token_prefix':copy.deepcopy(prefix),'control_error':copy.deepcopy(error),'events':events,'completion':completion,
  'control_callback_raised_in_model':True,'control_callback_returned_normally_in_model':False,'subsequent_client_execution_in_model':False,'client_handler_entered_in_model':False,'owner_failure_guard_evaluated_in_model':False,'new_explicit_cause_assignment_established_in_model':False,
  'exception_chain_observation':{'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','cleanup_context_link':'UNKNOWN','physical_reference_observation':None},'cleanup_error_in_model':cleanup,
  'finally_entry_completed_in_model':'finally-enter' in done,'removal_attempt_entered_in_model':'removal-attempt' in done,'removal_completed_in_model':popped,'selected_slot_before_removal':continuity,'selected_owner_removed_in_model':removed,'slot_after_pop_in_model':'ABSENT-AT-POP-COMPLETION' if popped else 'UNKNOWN','pop_result_observation':None,'revocation_persists':None,
  'last_pending_error_in_model':copy.deepcopy(pending),'outward_error_after_finally_in_model':copy.deepcopy(error) if popped else None,'control_outward_after_finally_established_in_model':popped,'control_reaches_launcher_established':False,'terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True,
  'prior_failure_storage_history':'UNKNOWN; no selected owner.failure guard here; previously established evidence is retained unchanged','role_relationship':'Separate semantic error roles and invocation-qualified occurrences; no physical equality or inequality inference','run_success_established':False,'runtime_observation':False,'runtime_control_exception_revocation_chain':None,'runtime_unwind_evidence':'UNAVAILABLE','physical_reference_identity':None,'outer_cleanup_completion':None,'database_cleanup_completion':None,'retained_failure_record_bytes':None,'physical_lock_release_established':False,'exclusive_ownership_established':False,'durability_established':False,'observer_join':None,
  'completion_flags_mean':'Only acknowledged conditional prefix facts; false does not disprove unobserved effects. Earlier registration and selected control raise survive later uncertainty. Pending propagation is not an observed outward exception.',
  'obligations_discharged':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_control_exception_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'CONTROL-SUBMITTED-OUTPUT');status_typed_same(submitted,control_exception_projection(catalogue,case,validated),'CONTROL-OUTPUT-CORRESPONDENCE');return True


def main():
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args()
 if a.write:
  for k,v in compile_bundle(a.root).items():
   target=a.root/FILES[k];need(not target.exists(),'REFUSE-OVERWRITE:'+str(target));target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(enc(v))
 if a.check:validate_bundle(a.root,read_bundle(a.root))
 print('PASS bounded managed integration; no runtime execution; readiness BLOCKED')
if __name__=='__main__':main()


# Additive construction-expression exceptional continuation; inherited functions unchanged.
def control_construction_source(launcher,entry,control,bare,callback,stored,token,handle,state):
 validate_control_exception(launcher,entry,bare,callback,stored,token,handle,state,control)
 tree,loc=_client_locate(entry);run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run')
 protected=run.body[2].body[0].body[-1];guard,client,post=protected.body;statement=guard.body[0];call=statement.value;construction=call.args[0];pop=protected.finalbody[0]
 need(isinstance(protected,ast.Try) and not protected.handlers and not protected.orelse and len(protected.finalbody)==1,'CONSTRUCTION-PROTECTED-TRY')
 need(ast.unparse(guard.test)=='control is not None' and ast.unparse(call)=='control(_Control(token))' and isinstance(construction,ast.Call) and ast.unparse(construction.func)=='_Control' and not construction.keywords,'CONSTRUCTION-EXPRESSION')
 need(isinstance(client,ast.Try) and client.lineno>statement.end_lineno and ast.unparse(client.body[0])=='client(Client(token))','CONSTRUCTION-OUTSIDE-CLIENT-HANDLER')
 cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='_Control');init=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='__init__')
 need([n.arg for n in init.args.args]==['self','token'] and len(init.body)==1 and ast.unparse(init.body[0])=='self.__token = token','CONSTRUCTION-INITIALIZER-SOURCE')
 pin={'bytes':len(entry),'sha256':digest(entry)}
 points=[('finally-enter',protected),('removal-attempt',pop.value),('removal-complete',pop)]
 prefix=token['source']['order'][:token['source']['order'].index('control-create')+1]
 need(prefix==['owner-create','token-create','registry-insert','control-guard','control-create'],'CONSTRUCTION-PREFIX-ORDER')
 status_typed_same(token['source']['stages']['control-create'],{**loc(construction),'source':copy.deepcopy(pin)},'CONSTRUCTION-REUSED-ATTEMPT')
 for name,node in points:
  status_typed_same(control['source']['stages'][name],{**loc(node),'source':copy.deepcopy(pin),'semantic_region':'finally-entry' if name=='finally-enter' else 'source-statement'},'CONSTRUCTION-REUSED-REVOCATION:'+name)
 return {'sources':copy.deepcopy(control['source']['sources']),'run':loc(run),'control_guard':loc(guard.test),'guard_expression':ast.unparse(guard.test),'selected_guard_result':True,
  'construction_expression':loc(construction),'constructor_expression':ast.unparse(construction.func),'argument_expression':ast.unparse(construction.args[0]),'initializer_source':loc(init),'initializer_assignment_source':loc(init.body[0]),
  'control_call_not_reached':loc(statement),'client_handler_not_reached':loc(client.handlers[0]),'prefix_order':prefix,
  'order':[n for n,_ in points],'stages':{n:copy.deepcopy(control['source']['stages'][n]) for n,_ in points},
  'evaluation_order':['evaluate control callable expression','evaluate _Control(token) argument expression','invoke control only after argument evaluation returns normally'],
  'selected_frontier':'Exception escapes the selected _Control(token) expression; no concrete failure mechanism or constructor substep is asserted',
  'allocation_progress_established':False,'initializer_entry_established':False,'initializer_assignment_established':False,'completed_control_object_established':False,
  'control_callback_execution_established':False,'client_callback_execution_established':False,'client_handler_applies':False,'owner_failure_guard_applies':False,'new_explicit_cause_assignment':False,
  'pop_key':ast.unparse(pop.value.args[0]),'pop_default':ast.literal_eval(pop.value.args[1]),'pop_return_consumed':False,
  'continuation':'Ordinary exceptional continuation from argument construction enters the enclosing finally. Later cleanup may replace pending propagation. Termination is not exception unwind.',
  'continuity':copy.deepcopy(control['source']['continuity'])}

def compile_control_construction(launcher,entry,control,bare,callback,stored,token,handle,state):
 source=control_construction_source(launcher,entry,control,bare,callback,stored,token,handle,state)
 return {'format':'I164-CONTROL-CONSTRUCTION-STATIC-1','source':source,'token_relation':copy.deepcopy(token),
  'declarations':[{'id':n,'source_origin':copy.deepcopy(source['stages'][n]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in source['order']],
  'guard_branches':{'prefix':'control is not None; selected _Control(token) argument expression raises before control invocation','continuation':'Ordinary continuation enters finally; later stages require preceding normal completion','cleanup_raise':'Separate cleanup exception may supersede pending construction error','termination_or_unobserved':'Stop without inferred unwind, completed removal or outward propagation','callbacks':'Neither selected control nor subsequent client callback executes on this route','constructor_progress':'No allocation, initializer entry, assignment or completed object inferred'},
  'preserved_relations':['control_exception_revocation_correspondence',*control['preserved_relations']],
  'reference_meaning':'Inherited control/client symbols are conditional role names, not completed or observed objects on this branch',
  'limits':['Static constructed scope; runtime construction/finally/removal observations unavailable','Existing cause/context/suppression UNKNOWN','Failure mechanism and constructor substep history unavailable','Full outer cleanup remains unexpanded','No owner.failure condition or history inferred'],
  'runtime_construction_exception_revocation_chain':None,'actual_admission':False}

def validate_control_construction(launcher,entry,control,bare,callback,stored,token,handle,state,submitted):
 status_exact_tree(submitted,'CONSTRUCTION-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_control_construction(launcher,entry,control,bare,callback,stored,token,handle,state),'CONSTRUCTION-SOURCE-CORRESPONDENCE');return True

def control_construction_binding(catalogue,scope):
 status_exact_tree(scope,'CONSTRUCTION-ERROR-SCOPE');refs=token_reference_premises(scope,True)
 return {'role':'selected-control-construction-expression-exception','scope':copy.deepcopy(scope),'occurrence':scope['invocation']+'/control-create/exception','reference':scope['invocation']+'/control-create/error',
  'construction_attempt':{'occurrence':scope['invocation']+'/control-create','source':copy.deepcopy(catalogue['source']['construction_expression']),'argument_token':copy.deepcopy(refs['token']),'registered_owner':copy.deepcopy(refs['owner'])},
  'local_handler_binding':None,'exact_type':None,'exact_value_bytes':None,'failure_mechanism':None,'allocation_progress':None,'initializer_progress':None,'completed_object_reference':None,
  'producer_history':'UNAVAILABLE','existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_reference_observation':None}

def control_construction_projection(catalogue,case,validated):
 for v in (catalogue,case,validated):status_exact_tree(v,'CONSTRUCTION-EXACT-TYPE')
 keys={'scope','references','token_inputs','token_prefix','construction_error','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'CONSTRUCTION-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'CONSTRUCTION-VALIDATED:'+k)
 scope=case['scope'];refs=case['references'];prefix=case['token_prefix'];ti=case['token_inputs'];error=case['construction_error'];source=catalogue['source']
 status_typed_same(refs,token_reference_premises(scope,True),'CONSTRUCTION-REFERENCE-ROLES');status_typed_same(scope,ti['scope'],'CONSTRUCTION-TOKEN-SCOPE');need(ti['control_present'] is True,'CONSTRUCTION-REQUIRES-CONTROL')
 expected=[{'stage':n,'outcome':'raise' if n=='control-create' else 'normal'} for n in source['prefix_order']]
 status_typed_same(ti['outcomes'],expected,'CONSTRUCTION-SELECTED-PREFIX')
 tv={k:copy.deepcopy(v) for k,v in ti.items() if k!='references'}
 status_typed_same(prefix,token_registration_projection(catalogue['token_relation'],ti,tv),'CONSTRUCTION-VALIDATED-TOKEN-PREFIX')
 status_typed_same(refs,prefix['reference_bindings'],'CONSTRUCTION-PREFIX-REFERENCES')
 need(prefix['registration_completed_in_model'] is True and prefix['completion']=='unexpected-raise' and prefix['events'][-1]['stage']=='control-create' and prefix['events'][-1]['outcome']=='raise' and prefix['control_callback_completed_in_model'] is False and prefix['client_callback_completed_in_model'] is False,'CONSTRUCTION-REGISTERED-RAISE-FRONTIER')
 status_typed_same(error,control_construction_binding(catalogue,scope),'CONSTRUCTION-SELECTED-ERROR')
 outcomes=case['outcomes'];need(type(outcomes) is list and bool(outcomes),'CONSTRUCTION-OUTCOMES');events=[];done=set();pending=copy.deepcopy(error);cleanup=None;terminal=None;completion=None
 for i,stage in enumerate(source['order']):
  need(i<len(outcomes),'CONSTRUCTION-MISSING-STEP:'+stage);row=outcomes[i]
  need(type(row) is dict and set(row)=={'stage','outcome'} and row['stage']==stage,'CONSTRUCTION-STEP-ORDER');kind=row['outcome'];need(type(kind) is str and kind in ('normal','raise','process-termination','unobserved'),'CONSTRUCTION-STAGE-OUTCOME');terminal=kind
  events.append({'id':scope['invocation']+'/'+stage,'scope':copy.deepcopy(scope),'stage':stage,'source':copy.deepcopy(source['stages'][stage]),'outcome':kind,'owner':copy.deepcopy(refs['owner']),'token':copy.deepcopy(refs['token']),'pending_error_on_entry':copy.deepcopy(pending),'runtime_frame':None})
  if kind in ('process-termination','unobserved'):completion=kind;break
  if kind=='raise':
   cleanup={'role':'conditional-finally-exception','reference':scope['invocation']+'/'+stage+'/error','scope':copy.deepcopy(scope),'source':copy.deepcopy(source['stages'][stage]),'exact_type':None,'physical_identity':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN'};pending=copy.deepcopy(cleanup);completion='cleanup-exceptional-frontier';break
  done.add(stage)
  if stage=='removal-complete':completion='normal-removal-pending-construction-error'
 need(len(events)==len(outcomes),'CONSTRUCTION-UNREACHED-STEPS');popped='removal-complete' in done;continuity=copy.deepcopy(prefix['selected_slot_before_removal']);removed=True if popped and continuity['continuity']=='explicit constructed premise' else None
 return {'kind':'CONSTRUCTED-CONTROL-CONSTRUCTION-EXCEPTION','scope':copy.deepcopy(scope),'reference_bindings':copy.deepcopy(refs),'reference_meaning':catalogue['reference_meaning'],'validated_token_prefix':copy.deepcopy(prefix),'construction_error':copy.deepcopy(error),'events':events,'completion':completion,
  'construction_expression_raised_in_model':True,'construction_completed_in_model':False,'completed_control_object_reference':None,'allocation_progress':None,'initializer_progress':None,'control_callback_executed_in_model':False,'subsequent_client_execution_in_model':False,'client_handler_entered_in_model':False,'owner_failure_guard_evaluated_in_model':False,'new_explicit_cause_assignment_established_in_model':False,
  'exception_chain_observation':{'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','cleanup_context_link':'UNKNOWN','physical_reference_observation':None},'cleanup_error_in_model':cleanup,
  'finally_entry_completed_in_model':'finally-enter' in done,'removal_attempt_entered_in_model':'removal-attempt' in done,'removal_completed_in_model':popped,'selected_slot_before_removal':continuity,'selected_owner_removed_in_model':removed,'slot_after_pop_in_model':'ABSENT-AT-POP-COMPLETION' if popped else 'UNKNOWN','pop_result_observation':None,'revocation_persists':None,
  'last_pending_error_in_model':copy.deepcopy(pending),'outward_error_after_finally_in_model':copy.deepcopy(error) if popped else None,'construction_outward_after_finally_established_in_model':popped,'construction_reaches_launcher_established':False,'terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True,
  'prior_failure_storage_history':'UNKNOWN; no selected owner.failure guard here; previously established evidence is retained unchanged','role_relationship':'Separate semantic error roles and invocation-qualified occurrences; no physical equality or inequality inference','run_success_established':False,'runtime_observation':False,'runtime_construction_exception_revocation_chain':None,'runtime_unwind_evidence':'UNAVAILABLE','physical_reference_identity':None,'outer_cleanup_completion':None,'database_cleanup_completion':None,'retained_failure_record_bytes':None,'physical_lock_release_established':False,'exclusive_ownership_established':False,'durability_established':False,'observer_join':None,
  'completion_flags_mean':'Only conditional acknowledged completions; no allocation or initializer substep inferred. Earlier registration and selected construction-expression raise survive later uncertainty. Pending propagation is not observed outward propagation.',
  'obligations_discharged':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_control_construction_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'CONSTRUCTION-SUBMITTED-OUTPUT');status_typed_same(submitted,control_construction_projection(catalogue,case,validated),'CONSTRUCTION-OUTPUT-CORRESPONDENCE');return True


# Additive Client construction / exact-None continuation. Inherited definitions unchanged.
def client_construction_source(launcher,entry,construction,control,bare,callback,stored,token,handle,state):
 validate_control_construction(launcher,entry,control,bare,callback,stored,token,handle,state,construction)
 tree,loc=_client_locate(entry);run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run')
 protected=run.body[2].body[0].body[-1];control_guard,client_try,post=protected.body;statement=client_try.body[0];call=statement.value;attempt=call.args[0];handler=client_try.handlers[0];guard=handler.body[0];raise_=handler.body[1];pop=protected.finalbody[0]
 need(isinstance(client_try,ast.Try) and len(client_try.body)==len(client_try.handlers)==1 and not client_try.orelse and not client_try.finalbody,'CLIENT-CONSTRUCTION-INNER-TRY')
 need(ast.unparse(call)=='client(Client(token))' and isinstance(attempt,ast.Call) and ast.unparse(attempt.func)=='Client' and len(attempt.args)==1 and not attempt.keywords,'CLIENT-CONSTRUCTION-EXPRESSION')
 need(ast.unparse(handler.type)=='BaseException' and handler.name=='client_error' and len(handler.body)==2,'CLIENT-CONSTRUCTION-HANDLER')
 need(ast.unparse(guard.test)=='owner.failure is not None' and not guard.orelse and isinstance(raise_,ast.Raise) and raise_.exc is None and raise_.cause is None,'CLIENT-CONSTRUCTION-NONE-BARE')
 cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Client');init=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='__init__')
 need([n.arg for n in init.args.args]==['self','token'] and len(init.body)==1 and ast.unparse(init.body[0])=='self.__token = token','CLIENT-CONSTRUCTION-INITIALIZER-SOURCE')
 pin={'bytes':len(entry),'sha256':digest(entry)}
 prefix=['owner-create','token-create','registry-insert','control-guard','control-create','control-callback','client-create']
 need(token['source']['order'][:len(prefix)]==prefix,'CLIENT-CONSTRUCTION-PREFIX-ORDER')
 status_typed_same(token['source']['stages']['client-create'],{**loc(attempt),'source':copy.deepcopy(pin)},'CLIENT-CONSTRUCTION-ATTEMPT-ORIGIN')
 points=[('callback-handler-enter',handler),('callback-none-guard',guard.test),('callback-bare-rethrow',raise_),('finally-enter',protected),('removal-attempt',pop.value),('removal-complete',pop)]
 for name,node in points:
  region='handler-entry' if name=='callback-handler-enter' else ('finally-entry' if name=='finally-enter' else 'source-statement')
  status_typed_same(bare['source']['stages'][name],{**loc(node),'source':copy.deepcopy(pin),'semantic_region':region},'CLIENT-CONSTRUCTION-REUSED-STAGE:'+name)
 return {'sources':copy.deepcopy(construction['source']['sources']),'run':loc(run),'construction_expression':loc(attempt),'constructor_expression':ast.unparse(attempt.func),'argument_expression':ast.unparse(attempt.args[0]),'initializer_source':loc(init),'initializer_assignment_source':loc(init.body[0]),
  'client_call_not_reached':loc(statement),'handler':loc(handler),'exception_binding':handler.name,'catch_family':ast.unparse(handler.type),'guard':loc(guard.test),'guard_expression':ast.unparse(guard.test),'selected_guard_result':False,'selected_slot_expression':'owner.failure','selected_slot_value':None,'selected_slot_exact_type':'NoneType','raise':loc(raise_),'raise_syntax':ast.unparse(raise_),'bare_raise_has_explicit_cause_clause':False,
  'prefix_order_control_present':prefix,'prefix_order_control_absent':[n for n in prefix if n not in ('control-create','control-callback')],'control_guard':loc(control_guard.test),'control_guard_expression':ast.unparse(control_guard.test),
  'order':[n for n,_ in points],'stages':{n:copy.deepcopy(bare['source']['stages'][n]) for n,_ in points},'guard_slot_premise':bare['source']['guard_slot_premise'],'reused_revocation':copy.deepcopy(bare['source']['reused_revocation']),
  'evaluation_order':['Earlier selected control path completes normally or is absent','Evaluate client callable expression','Evaluate Client(token) argument expression inside the client try','Invoke client only if argument construction returns normally'],
  'selected_frontier':'Exception escapes selected Client(token) expression; ordinary continuation binds it as client_error. No allocation/initializer substep or failure mechanism inferred.',
  'allocation_progress_established':False,'initializer_entry_established':False,'initializer_assignment_established':False,'completed_client_object_established':False,'client_callback_execution_established':False,'new_explicit_cause_assignment':False,
  'error_continuity':'The construction error is the selected caught error; bare raise reraises that active error under the exact-None guard. Handler evaluation or cleanup can replace pending propagation. Existing cause/context/suppression remain UNKNOWN.',
  'stage_names':'Reused callback-handler/guard/rethrow stage names identify the existing source handler; they do not assert client-callback invocation.',
  'continuity':copy.deepcopy(construction['source']['continuity'])}

def compile_client_construction(launcher,entry,construction,control,bare,callback,stored,token,handle,state):
 source=client_construction_source(launcher,entry,construction,control,bare,callback,stored,token,handle,state)
 return {'format':'I164-CLIENT-CONSTRUCTION-NONE-STATIC-1','source':source,'token_relation':copy.deepcopy(token),
  'declarations':[{'id':n,'source_origin':copy.deepcopy(source['stages'][n]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in source['order']],
  'guard_branches':{'prefix_control_absent':'control is None; selected client construction raises','prefix_control_present':'control is not None; its construction and callback completed normally before selected client construction raises','slot':'Selected same-owner failure slot is exactly None under explicit guard-slot continuity; no historical absence inferred','bare_raise':'Reraise the active construction exception, adding no explicit cause','handler_evaluation':'A raise in handler/guard/rethrow evaluation skips remaining handler stages and conditionally proceeds to finally with replacement error','cleanup':'Later finally/pop raise can replace propagation, without completed removal','termination_or_unobserved':'No inferred Python unwind, continuation, cleanup or outward propagation','client':'No completed Client or selected client-callback execution established'},
  'preserved_relations':['control_construction_revocation_correspondence',*construction['preserved_relations']],
  'reference_meaning':'Inherited client symbol denotes a conditional role, not a completed or observed Client; earlier control progress is preserved separately when established in the selected prefix',
  'limits':['Static constructed scope; runtime construction/handler/rethrow/removal chain unavailable','Exact None is a guard-slot premise, not proof of no earlier storage','Existing cause/context/suppression UNKNOWN','No concrete failure mechanism or allocation/initializer progress','Non-None constructor branch and full outer cleanup remain outside this slice'],
  'runtime_client_construction_revocation_chain':None,'actual_admission':False}

def validate_client_construction(launcher,entry,construction,control,bare,callback,stored,token,handle,state,submitted):
 status_exact_tree(submitted,'CLIENT-CONSTRUCTION-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_client_construction(launcher,entry,construction,control,bare,callback,stored,token,handle,state),'CLIENT-CONSTRUCTION-SOURCE-CORRESPONDENCE');return True

def client_construction_binding(catalogue,scope,control_present):
 status_exact_tree(scope,'CLIENT-CONSTRUCTION-ERROR-SCOPE');refs=token_reference_premises(scope,control_present)
 return {'role':'selected-client-construction-expression-exception','scope':copy.deepcopy(scope),'occurrence':scope['invocation']+'/client-create/exception','reference':scope['invocation']+'/client-create/error',
  'construction_attempt':{'occurrence':scope['invocation']+'/client-create','source':copy.deepcopy(catalogue['source']['construction_expression']),'argument_token':copy.deepcopy(refs['token']),'registered_owner':copy.deepcopy(refs['owner'])},
  'handler_binding_name_from_source':catalogue['source']['exception_binding'],'handler_binding_established_by_this_role':False,'exact_type':None,'exact_value_bytes':None,'failure_mechanism':None,'allocation_progress':None,'initializer_progress':None,'completed_object_reference':None,'producer_history':'UNAVAILABLE','existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_reference_observation':None}

def client_construction_projection(catalogue,case,validated):
 for v in (catalogue,case,validated):status_exact_tree(v,'CLIENT-CONSTRUCTION-EXACT-TYPE')
 keys={'scope','references','token_inputs','token_prefix','none_guard_binding','construction_error','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'CLIENT-CONSTRUCTION-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'CLIENT-CONSTRUCTION-VALIDATED:'+k)
 scope=case['scope'];refs=case['references'];prefix=case['token_prefix'];ti=case['token_inputs'];binding=case['none_guard_binding'];error=case['construction_error'];source=catalogue['source']
 need(type(ti['control_present']) is bool and ti['owner_failure_none'] is True,'CLIENT-CONSTRUCTION-SELECTED-PREMISES');control=ti['control_present']
 status_typed_same(refs,token_reference_premises(scope,control),'CLIENT-CONSTRUCTION-REFERENCE-ROLES');status_typed_same(scope,ti['scope'],'CLIENT-CONSTRUCTION-TOKEN-SCOPE')
 order=source['prefix_order_control_present' if control else 'prefix_order_control_absent'];expected=[{'stage':n,'outcome':'raise' if n=='client-create' else 'normal'} for n in order]
 status_typed_same(ti['outcomes'],expected,'CLIENT-CONSTRUCTION-SELECTED-PREFIX');tv={k:copy.deepcopy(v) for k,v in ti.items() if k!='references'}
 status_typed_same(prefix,token_registration_projection(catalogue['token_relation'],ti,tv),'CLIENT-CONSTRUCTION-VALIDATED-TOKEN-PREFIX');status_typed_same(refs,prefix['reference_bindings'],'CLIENT-CONSTRUCTION-PREFIX-REFERENCES')
 need(prefix['registration_completed_in_model'] is True and prefix['completion']=='unexpected-raise' and prefix['events'][-1]['stage']=='client-create' and prefix['events'][-1]['outcome']=='raise' and prefix['client_callback_completed_in_model'] is False,'CLIENT-CONSTRUCTION-REGISTERED-RAISE-FRONTIER')
 need(prefix['control_callback_completed_in_model'] is (True if control else None),'CLIENT-CONSTRUCTION-EARLIER-CONTROL')
 status_typed_same(error,client_construction_binding(catalogue,scope,control),'CLIENT-CONSTRUCTION-SELECTED-ERROR')
 expected_guard={'scope':copy.deepcopy(scope),'owner':copy.deepcopy(refs['owner']),'slot':'owner.failure','slot_value':None,'slot_exact_type':'NoneType','guard_expression':source['guard_expression'],'guard_result':False,'guard_source':copy.deepcopy(source['guard']),'source':copy.deepcopy(source['sources']['entry']),'premise':source['guard_slot_premise'],'runtime_reference_observation':None,'prior_storage_history':'UNKNOWN; no retained evidence is erased'}
 status_typed_same(binding,expected_guard,'CLIENT-CONSTRUCTION-NONE-GUARD')
 outcomes=case['outcomes'];need(type(outcomes) is list and bool(outcomes),'CLIENT-CONSTRUCTION-OUTCOMES');order=source['order'];cursor=0;index=0;events=[];done=set();pending=copy.deepcopy(error);evaluation=None;cleanup=None;completion=None;terminal=None
 while cursor<len(order):
  stage=order[cursor];need(index<len(outcomes),'CLIENT-CONSTRUCTION-MISSING-STEP:'+stage);row=outcomes[index];index+=1
  need(type(row) is dict and set(row)=={'stage','outcome'} and row['stage']==stage,'CLIENT-CONSTRUCTION-STEP-ORDER');kind=row['outcome']
  allowed=('reraised-construction','raise','process-termination','unobserved') if stage=='callback-bare-rethrow' else ('normal','raise','process-termination','unobserved')
  need(type(kind) is str and kind in allowed,'CLIENT-CONSTRUCTION-STAGE-OUTCOME');terminal=kind
  events.append({'id':scope['invocation']+'/'+stage,'scope':copy.deepcopy(scope),'stage':stage,'source':copy.deepcopy(source['stages'][stage]),'outcome':kind,'owner':copy.deepcopy(refs['owner']),'token':copy.deepcopy(refs['token']),'pending_error_on_entry':copy.deepcopy(pending),'runtime_frame':None})
  if kind in ('process-termination','unobserved'):completion=kind;break
  if cursor<3:
   if kind=='raise':
    evaluation={'role':'conditional-handler-evaluation-exception','reference':scope['invocation']+'/'+stage+'/error','scope':copy.deepcopy(scope),'source':copy.deepcopy(source['stages'][stage]),'exact_type':None,'physical_identity':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN'};pending=copy.deepcopy(evaluation);cursor=3;continue
   done.add(stage)
   if stage=='callback-bare-rethrow':pending=copy.deepcopy(error)
  elif kind=='raise':
   cleanup={'role':'conditional-finally-exception','reference':scope['invocation']+'/'+stage+'/error','scope':copy.deepcopy(scope),'source':copy.deepcopy(source['stages'][stage]),'exact_type':None,'physical_identity':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN'};pending=copy.deepcopy(cleanup);completion='cleanup-exceptional-frontier';break
  else:done.add(stage)
  cursor+=1
  if stage=='removal-complete':completion='normal-removal-pending-construction-error' if 'callback-bare-rethrow' in done else 'normal-removal-pending-evaluation-error'
 need(index==len(outcomes),'CLIENT-CONSTRUCTION-UNREACHED-STEPS');popped='removal-complete' in done;reraised='callback-bare-rethrow' in done;caught='callback-handler-enter' in done;continuity=copy.deepcopy(prefix['selected_slot_before_removal']);removed=True if popped and continuity['continuity']=='explicit constructed premise' else None
 return {'kind':'CONSTRUCTED-CLIENT-CONSTRUCTION-NONE','scope':copy.deepcopy(scope),'reference_bindings':copy.deepcopy(refs),'reference_meaning':catalogue['reference_meaning'],'validated_token_prefix':copy.deepcopy(prefix),'construction_error':copy.deepcopy(error),'none_guard_binding':copy.deepcopy(binding),'events':events,'completion':completion,
  'construction_expression_raised_in_model':True,'construction_completed_in_model':False,'completed_client_object_reference':None,'allocation_progress':None,'initializer_progress':None,'client_callback_executed_in_model':False,
  'earlier_control_present':control,'earlier_control_construction_completed_in_model':True if control else None,'earlier_control_callback_completed_in_model':prefix['control_callback_completed_in_model'],
  'handler_entry_completed_in_model':caught,'caught_error_in_model':copy.deepcopy(error) if caught else None,'caught_name_in_model':source['exception_binding'] if caught else None,'none_guard_completed_in_model':'callback-none-guard' in done,'bare_rethrow_effect_established_in_model':reraised,'reraised_error_in_model':copy.deepcopy(error) if reraised else None,
  'bare_raise_semantics':{'adds_explicit_cause':False,'preserves_active_exception':True,'establishes_absent_existing_cause_or_context':False},'exception_chain_observation':{'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','cleanup_context_link':'UNKNOWN','physical_reference_observation':None},'new_explicit_cause_assignment_established_in_model':False,'handler_evaluation_error_in_model':evaluation,'cleanup_error_in_model':cleanup,
  'finally_entry_completed_in_model':'finally-enter' in done,'removal_attempt_entered_in_model':'removal-attempt' in done,'removal_completed_in_model':popped,'selected_slot_before_removal':continuity,'selected_owner_removed_in_model':removed,'slot_after_pop_in_model':'ABSENT-AT-POP-COMPLETION' if popped else 'UNKNOWN','pop_result_observation':None,'revocation_persists':None,
  'last_pending_error_in_model':copy.deepcopy(pending),'outward_error_after_finally_in_model':copy.deepcopy(pending) if popped else None,'construction_outward_after_finally_established_in_model':popped and reraised,'construction_reaches_launcher_established':False,'terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True,
  'prior_failure_storage_history':'UNKNOWN; the exact None guard does not erase earlier established storage or evidence','role_relationship':'Construction and caught-error roles share the selected error; later evaluation/cleanup roles do not prove physical inequality','run_success_established':False,'runtime_observation':False,'runtime_client_construction_revocation_chain':None,'runtime_unwind_evidence':'UNAVAILABLE','physical_reference_identity':None,'outer_cleanup_completion':None,'database_cleanup_completion':None,'retained_failure_record_bytes':None,'physical_lock_release_established':False,'exclusive_ownership_established':False,'durability_established':False,'observer_join':None,
  'completion_flags_mean':'Conditional acknowledged model progress only. Earlier registration, construction-error and selected control completion survive later uncertainty. No allocation/initializer progress or guaranteed outward propagation.',
  'obligations_discharged':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_client_construction_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'CLIENT-CONSTRUCTION-SUBMITTED-OUTPUT');status_typed_same(submitted,client_construction_projection(catalogue,case,validated),'CLIENT-CONSTRUCTION-OUTPUT-CORRESPONDENCE');return True


# Bounded constructor-error delivery and initial launcher details; no runtime execution.
def launcher_details_source(launcher,entry,client_construction):
 for raw in (launcher,entry):need(type(raw) is bytes,'DETAILS-SOURCE-BYTES')
 status_exact_tree(client_construction,'DETAILS-PARENT-CATALOGUE')
 pins={'launcher':{'bytes':len(launcher),'sha256':digest(launcher)},'entry':{'bytes':len(entry),'sha256':digest(entry)}}
 status_typed_same(client_construction['source']['sources'],pins,'DETAILS-PARENT-SOURCES')
 lt,ll=_client_locate(launcher);et,el=_client_locate(entry)
 def function(tree,name):
  found=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name];need(len(found)==1,'DETAILS-FUNCTION:'+name);return found[0]
 run=function(et,'_run');session=function(lt,'session');private=function(lt,'_session')
 rw=[n for n in ast.walk(run) if isinstance(n,ast.With) and ast.unparse(n.items[0].context_expr).startswith('launcher.session(')]
 need(len(rw)==1 and len(rw[0].items)==1,'DETAILS-RUN-WITH');rw=rw[0]
 need(ast.unparse(rw.items[0].context_expr)=='launcher.session(candidate, draft, runtime, destination, create=create)' and ast.unparse(rw.items[0].optional_vars)=='wrapper','DETAILS-RUN-ROUTE')
 for fn in (session,private):need([ast.unparse(d) for d in fn.decorator_list]==['contextlib.contextmanager'],'DETAILS-GENERATOR-DECORATOR')
 sw=session.body[-1];need(isinstance(sw,ast.With) and len(sw.items)==1 and ast.unparse(sw.items[0].context_expr)=='_session(*args, **kwargs)' and ast.unparse(sw.items[0].optional_vars)=='managed','DETAILS-PUBLIC-PRIVATE-BRIDGE')
 need(len(sw.body)==1 and isinstance(sw.body[0],ast.Expr) and isinstance(sw.body[0].value,ast.Yield) and ast.unparse(sw.body[0].value.value)=='managed','DETAILS-PUBLIC-YIELD');sy=sw.body[0]
 protected=[n for n in ast.walk(private) if isinstance(n,ast.Try) and any(h.name=='e' and ast.unparse(h.type)=='BaseException' for h in n.handlers)]
 need(len(protected)==1,'DETAILS-PRIVATE-CATCH');tr=protected[0];need(len(tr.handlers)==1,'DETAILS-PRIVATE-HANDLERS');handler=tr.handlers[0]
 py=[n for n in tr.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Yield)]
 need(len(py)==1 and ast.unparse(py[0].value.value)=='ManagedSession(managed)','DETAILS-PRIVATE-YIELD');py=py[0]
 need([ast.unparse(n) for n in tr.body[tr.body.index(py)+1:]]==['managed.close()','managed = None',"(dest / 'ACTIVE.json').unlink()"],'DETAILS-NORMAL-ROUTE-IDENTITY')
 assignment=handler.body[0];need(isinstance(assignment,ast.Assign) and len(assignment.targets)==1 and ast.unparse(assignment.targets[0])=='details' and isinstance(assignment.value,ast.Dict),'DETAILS-ASSIGNMENT')
 d=assignment.value;need(all(isinstance(k,ast.Constant) and type(k.value) is str for k in d.keys),'DETAILS-LITERAL-KEYS')
 names=[k.value for k in d.keys];expressions=[ast.unparse(v) for v in d.values]
 need(names==['error','message','traceback','nonexecution_established','new_authorization','cleanup'],'DETAILS-FIELD-DOMAIN')
 need(expressions==['type(e).__name__','str(e)','traceback.format_exc()','False','False','[]'],'DETAILS-FIELD-ORIGINS')
 need(isinstance(handler.body[1],ast.For),'DETAILS-STOP-BEFORE-LOOP')
 status_typed_same(client_construction['source']['run'],el(run),'DETAILS-PARENT-RUN')
 points=[('run-with-exception-exit',el(rw),pins['entry'],'conditional-context-exit'),('session-yield-delivery',ll(sy),pins['launcher'],'conditional-generator-delivery'),('session-inner-with-exception-exit',ll(sw),pins['launcher'],'conditional-context-exit'),('private-yield-delivery',ll(py),pins['launcher'],'conditional-generator-delivery'),('launcher-handler-entry',ll(handler),pins['launcher'],'handler-entry'),('details-evaluation-attempt',ll(assignment),pins['launcher'],'statement-evaluation-entry')]
 fields=[]
 for key,value in zip(d.keys,d.values):
  name=key.value;points.extend([('details-key-'+name,ll(key),pins['launcher'],'key-evaluation'),('details-value-'+name,ll(value),pins['launcher'],'value-evaluation')])
  fields.append({'name':name,'key_source':{**ll(key),'source':copy.deepcopy(pins['launcher'])},'value_source':{**ll(value),'source':copy.deepcopy(pins['launcher'])},'expression':ast.unparse(value),'error_relation':'delivered e argument' if name in ('error','message') else 'selected active caught exception, conditional continuity' if name=='traceback' else 'source literal'})
 points.extend([('details-dict-completion',ll(d),pins['launcher'],'dictionary-construction-completion'),('details-assignment-attempt',ll(assignment.targets[0]),pins['launcher'],'local-binding-attempt'),('details-assignment-complete',ll(assignment),pins['launcher'],'local-binding-completion')])
 return {'sources':pins,'run':el(run),'public_session':ll(session),'private_session':ll(private),'catch_binding':handler.name,'catch_family':ast.unparse(handler.type),'fields':fields,'order':[n for n,_,_,_ in points],
  'stages':{n:{**loc,'source':copy.deepcopy(pin),'semantic_region':region} for n,loc,pin,region in points},'stop_before':{**ll(handler.body[1]),'source':copy.deepcopy(pins['launcher'])},
  'excluded_normal_stages':[ll(n) for n in tr.body[tr.body.index(py)+1:]],
  'propagation':'Explicit conditional ordinary context-manager exception delivery through both decorated generators; no runtime arrival follows from source anchors or completed pop',
  'evaluation_order':'Dictionary key then value pairs in defining-source order, then dictionary completion and local details binding; boundaries do not assert allocation or Python opcode history',
  'dynamic_values':'No concrete error name, message, traceback, formatted bytes or dynamic result type supplied by source correspondence',
  'scope':'Stop at initial details assignment; no cleanup-loop entry, write, outer propagation, lock release or authority change'}

def compile_launcher_details(launcher,entry,client_construction):
 source=launcher_details_source(launcher,entry,client_construction)
 return {'format':'I164-LAUNCHER-INITIAL-DETAILS-STATIC-1','source':source,
  'parent_catalogue':{'format':client_construction['format'],'identity':{'sha256':digest((json.dumps(client_construction,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode())}},
  'declarations':[{'id':n,'source_origin':copy.deepcopy(source['stages'][n]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in source['order']],
  'guard_branches':{'parent':'Reviewed exact-None bare rethrow, normal pop and original constructor error still pending; completed pop alone is insufficient','prefixes':['control absent','earlier control construction/callback completed normally'],'delivery':'Selected exception continuity is explicit conditional premise; unknown continuity establishes no handler arrival','evaluation':'Normal acknowledges only selected source-expression evaluation; exact generated values remain unknown','raise':'Replacement exception frontier; preserve earlier established constructor error and handler binding','termination':'No inferred Python exception or unwind','unobserved':'No further established progress','completion':'Known literal fields and initially empty cleanup list represented only after complete details assignment','excluded':'No normal managed close/clear/unlink, cleanup-loop, write, outward propagation or authority claim'},
  'preserved_relations':['client_construction_none_correspondence',*client_construction['preserved_relations']],
  'runtime_handler_details_observations':None,'non_none_construction_complete':False,'outer_cleanup_complete':False,'actual_admission':False}

def validate_launcher_details(launcher,entry,client_construction,submitted):
 status_exact_tree(submitted,'DETAILS-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_launcher_details(launcher,entry,client_construction),'DETAILS-SOURCE-CORRESPONDENCE');return True

def launcher_delivery_binding(catalogue,parent,anchor,continuity):
 for v in (catalogue,parent,anchor,continuity):status_exact_tree(v,'DETAILS-DELIVERY-TYPES')
 need(type(continuity) is str and continuity in ('explicit conditional premise','UNESTABLISHED'),'DETAILS-CONTINUITY-DOMAIN')
 source=catalogue['source'];scope=parent['scope'];refs=parent['reference_bindings']
 return {'scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(anchor),'selected_error':copy.deepcopy(parent['construction_error']),
  'references':{n:copy.deepcopy(refs[n]) for n in ('owner','token','session','manager')},
  'route':[{'stage':n,'source':copy.deepcopy(source['stages'][n])} for n in source['order'][:5]],
  'launcher_name':source['catch_binding'],'continuity':continuity,'active_exception_continuity':'Conditional same selected error across ordinary delivery and normal evaluation; no observation',
  'runtime_delivery':None,'physical_object_identity':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN'}

def launcher_details_projection(catalogue,case,validated):
 for v in (catalogue,case,validated):status_exact_tree(v,'DETAILS-EXACT-TYPE')
 keys={'scope','anchor','parent_result','delivery_binding','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'DETAILS-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'DETAILS-VALIDATED:'+k)
 parent=case['parent_result'];scope=case['scope'];anchor=case['anchor'];source=catalogue['source'];delivery=case['delivery_binding'];error=parent['construction_error']
 status_typed_same(scope,parent['scope'],'DETAILS-PARENT-SCOPE');status_typed_same(anchor['instance'],scope['instance'],'DETAILS-INSTANCE');need(anchor['context']==scope['context'],'DETAILS-CONTEXT')
 need(parent['kind']=='CONSTRUCTED-CLIENT-CONSTRUCTION-NONE' and parent['completion']=='normal-removal-pending-construction-error','DETAILS-PARENT-COMPLETION')
 need(parent['handler_entry_completed_in_model'] is True and parent['none_guard_completed_in_model'] is True and parent['bare_rethrow_effect_established_in_model'] is True and parent['removal_completed_in_model'] is True,'DETAILS-PARENT-REQUIRED-STEPS')
 need(parent['handler_evaluation_error_in_model'] is None and parent['cleanup_error_in_model'] is None and parent['construction_outward_after_finally_established_in_model'] is True,'DETAILS-PENDING-ORIGINAL-ERROR')
 for k in ('caught_error_in_model','reraised_error_in_model','last_pending_error_in_model','outward_error_after_finally_in_model'):status_typed_same(parent[k],error,'DETAILS-PARENT-ERROR:'+k)
 need(parent['construction_completed_in_model'] is False and parent['client_callback_executed_in_model'] is False,'DETAILS-PARENT-NO-CLIENT')
 status_typed_same(delivery,launcher_delivery_binding(catalogue,parent,anchor,delivery['continuity']),'DETAILS-DELIVERY-BINDING')
 outcomes=case['outcomes'];need(type(outcomes) is list and bool(outcomes),'DETAILS-OUTCOMES')
 if delivery['continuity']=='UNESTABLISHED':status_typed_same(outcomes,[{'stage':source['order'][0],'outcome':'unobserved'}],'DETAILS-UNESTABLISHED-DELIVERY')
 events=[];done=set();replacement=None;terminal=None;completion=None
 for i,stage in enumerate(source['order']):
  need(i<len(outcomes),'DETAILS-MISSING-STEP:'+stage);row=outcomes[i]
  need(type(row) is dict and set(row)=={'stage','outcome'} and type(row['stage']) is str and row['stage']==stage,'DETAILS-STEP-ORDER')
  kind=row['outcome'];need(type(kind) is str and kind in ('normal','raise','process-termination','unobserved'),'DETAILS-OUTCOME');terminal=kind
  events.append({'id':scope['invocation']+'/'+stage,'scope':copy.deepcopy(scope),'stage':stage,'source':copy.deepcopy(source['stages'][stage]),'outcome':kind,'selected_error':copy.deepcopy(error),'owner':copy.deepcopy(delivery['references']['owner']),'token':copy.deepcopy(delivery['references']['token']),'runtime_frame':None})
  if kind!='normal':
   if kind=='raise':replacement={'role':'conditional-launcher-delivery-or-evaluation-error','reference':scope['invocation']+'/'+stage+'/error','scope':copy.deepcopy(scope),'origin':copy.deepcopy(source['stages'][stage]),'exact_type':None,'exact_value_bytes':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','physical_identity':None}
   completion={'raise':'replacement-exception-frontier','process-termination':'process-termination','unobserved':'unobserved-continuation'}[kind];break
  done.add(stage)
  if stage==source['order'][-1]:completion='initial-details-assignment-complete'
 need(len(events)==len(outcomes),'DETAILS-UNREACHED-STEPS')
 assigned='details-assignment-complete' in done;entered='launcher-handler-entry' in done;details=None
 if assigned:
  details={'role':'conditional-initial-launcher-details','reference':scope['invocation']+'/launcher/details','scope':copy.deepcopy(scope),'assignment_source':copy.deepcopy(source['stages']['details-assignment-complete']),
   'dynamic_fields':[{'name':f['name'],'expression':f['expression'],'source':copy.deepcopy(f['value_source']),'selected_error':copy.deepcopy(error),'binding':f['error_relation'],'exact_value':None,'exact_type':None,'formatted_bytes':None,'observation':'UNAVAILABLE'} for f in source['fields'][:3]],
   'known_literal_fields':{'nonexecution_established':False,'new_authorization':False,'cleanup':[]},'cleanup_reference':{'scope':copy.deepcopy(scope),'symbol':scope['invocation']+'/launcher/details/initial-cleanup-list','meaning':'source-created empty list at this assignment; no observed physical identity'},
   'complete_runtime_dictionary_observed':False,'exact_serialized_bytes':None}
 return {'kind':'CONSTRUCTED-LAUNCHER-INITIAL-DETAILS','scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(anchor),'validated_parent':copy.deepcopy(parent),'delivery_binding':copy.deepcopy(delivery),'events':events,'completion':completion,
  'earlier_constructor_exception':copy.deepcopy(error),'earlier_control_completed_in_model':parent['earlier_control_callback_completed_in_model'],'selected_owner_continuity':copy.deepcopy(parent['selected_slot_before_removal']),
  'handler_entry_completed_in_model':entered,'launcher_e_in_model':copy.deepcopy(error) if entered else None,'active_caught_error_in_model':copy.deepcopy(error) if entered else None,
  'details_evaluation_attempt_in_model':'details-evaluation-attempt' in done,'details_dictionary_completed_in_model':'details-dict-completion' in done,'details_assignment_attempt_in_model':'details-assignment-attempt' in done,'details_assignment_completed_in_model':assigned,'details_in_model':details,
  'replacement_error_in_model':replacement,'last_pending_error_in_model':copy.deepcopy(replacement or error),'terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True,
  'existing_cause_context_suppression':'UNKNOWN; no new chain observation','new_explicit_cause_assignment_established':False,'runtime_handler_arrival':None,'runtime_handler_details_chain':None,'runtime_unwind_evidence':'UNAVAILABLE','physical_reference_identity':None,
  'cleanup_loop_entered':False,'normal_managed_close_spliced':False,'managed_clear_spliced':False,'ACTIVE_unlink_spliced':False,'retained_failure_record_bytes':None,'failure_file_established':False,'outward_propagation_established':False,'physical_closure_established':False,'physical_lock_release_established':False,'durability_established':False,'outer_cleanup_complete':False,
  'completion_flags_mean':'Acknowledged conditional modeled progress only; false means not established, not absence of partial effects','runtime_observation':False,'observer_join':None,'obligations_discharged':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_launcher_details_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'DETAILS-SUBMITTED-OUTPUT');status_typed_same(submitted,launcher_details_projection(catalogue,case,validated),'DETAILS-OUTPUT-CORRESPONDENCE');return True


# Bounded exceptional cleanup selection, close and normal append. No runtime calls.
def cleanup_append_source(launcher,entry,manager,details,reference):
 for raw in (launcher,entry,manager):need(type(raw) is bytes,'CLEANUP-SOURCE-BYTES')
 for v in (details,reference):status_exact_tree(v,'CLEANUP-PARENT-CATALOGUE')
 pins={n:{'bytes':len(raw),'sha256':digest(raw)} for n,raw in [('launcher',launcher),('entry',entry),('manager',manager)]}
 status_typed_same(details['source']['sources'],{n:pins[n] for n in ('launcher','entry')},'CLEANUP-DETAILS-SOURCES')
 status_typed_same(pins['manager'],{k:reference['source']['source'][k] for k in ('bytes','sha256')},'CLEANUP-MANAGER-SOURCE')
 tree,loc=_client_locate(launcher);mt,ml=_client_locate(manager)
 fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_session');outer=fn.body[-1];tr=outer.body[-1];handler=tr.handlers[0];loop=handler.body[1]
 need(isinstance(tr,ast.Try) and handler.name=='e' and ast.unparse(handler.type)=='BaseException','CLEANUP-OUTER-HANDLER')
 status_typed_same({**loc(loop),'source':pins['launcher']},details['source']['stop_before'],'CLEANUP-PARENT-FRONTIER')
 need(isinstance(loop,ast.For) and not loop.orelse and len(loop.body)==1 and ast.unparse(loop.target)=='(name, obj)','CLEANUP-LOOP-SHAPE')
 need(isinstance(loop.iter,ast.List) and len(loop.iter.elts)==2,'CLEANUP-INPUT-SHAPE')
 inputs=[]
 for pair in loop.iter.elts:
  need(isinstance(pair,ast.Tuple) and len(pair.elts)==2 and isinstance(pair.elts[0],ast.Constant) and type(pair.elts[0].value) is str and isinstance(pair.elts[1],ast.Name),'CLEANUP-INPUT-PAIR')
  inputs.append({'name':pair.elts[0].value,'slot':pair.elts[1].id,'name_origin':loc(pair.elts[0]),'object_origin':loc(pair.elts[1]),'pair_origin':loc(pair)})
 status_typed_same([[v['name'],v['slot']] for v in inputs],[['raw','raw'],['managed','managed']],'CLEANUP-ORDERED-INPUTS')
 guard=loop.body[0];need(isinstance(guard,ast.If) and not guard.orelse and len(guard.body)==1,'CLEANUP-GUARD-SHAPE')
 test=guard.test;need(isinstance(test,ast.Compare) and isinstance(test.left,ast.Name) and test.left.id=='obj' and len(test.ops)==len(test.comparators)==1 and isinstance(test.ops[0],ast.IsNot) and isinstance(test.comparators[0],ast.Constant) and test.comparators[0].value is None,'CLEANUP-EXACT-NONNONE')
 protected=guard.body[0];need(isinstance(protected,ast.Try) and len(protected.body)==2 and len(protected.handlers)==1 and not protected.orelse and not protected.finalbody,'CLEANUP-SHARED-TRY')
 close,append=protected.body;error_handler=protected.handlers[0]
 need(ast.unparse(close)=='obj.close()' and isinstance(close,ast.Expr) and isinstance(close.value,ast.Call) and not close.value.args and not close.value.keywords,'CLEANUP-CLOSE-EXPRESSION')
 need(ast.unparse(append)=="details['cleanup'].append([name, 'close returned'])" and isinstance(append,ast.Expr) and isinstance(append.value,ast.Call) and len(append.value.args)==1 and not append.value.keywords,'CLEANUP-APPEND-EXPRESSION')
 need(error_handler.name=='close_error' and ast.unparse(error_handler.type)=='BaseException','CLEANUP-INNER-HANDLER')
 # Local slot origins and the successful handoff frontier are read from source.
 raw_init=[n for n in outer.body if isinstance(n,ast.Assign) and ast.unparse(n)=='raw = None'];managed_init=[n for n in outer.body if isinstance(n,ast.Assign) and ast.unparse(n)=='managed = None']
 need(len(raw_init)==len(managed_init)==1,'CLEANUP-LOCAL-INITIALIZATION')
 create=tr.body[0];need(isinstance(create,ast.If) and ast.unparse(create.test)=='create' and not create.orelse,'CLEANUP-CREATE-PREFIX')
 status_typed_same([ast.unparse(n) for n in create.body[:4]],['raw = authority.Authority.__new__(authority.Authority)',"authority.Authority.__init__(raw, db, cfg['config'], True, ownership_path=owners)",'raw.close()','raw = None'],'CLEANUP-RAW-CLEAR-PREFIX')
 managed=tr.body[1];need(ast.unparse(managed)=="managed, _ = open_session(c, db, cfg['config'], ownership_path=owners)",'CLEANUP-MANAGED-BINDING')
 yielded=tr.body[-4];need(ast.unparse(yielded)=='yield ManagedSession(managed)','CLEANUP-HANDOFF')
 cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ManagedSession');init=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='__init__')
 need(ast.unparse(init)=='def __init__(self, managed):\n    self.__managed = managed','CLEANUP-SESSION-REFERENCE')
 # No local raw/managed rebind in the selected handler before loop selection.
 need(not any(isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store) and n.id in ('raw','managed') for n in ast.walk(handler.body[0])),'CLEANUP-DETAILS-LOCAL-REBIND')
 mcls=next(n for n in mt.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority');mc=next(n for n in mcls.body if isinstance(n,ast.FunctionDef) and n.name=='close')
 rp=[p for p in reference['source']['programs'] if p['function']=='close'];need(len(rp)==1,'CLEANUP-REFERENCE-CLOSE-PROGRAM')
 need(rp[0]['ast']==ast.dump(mc,include_attributes=False),'CLEANUP-REFERENCE-CLOSE-AST')
 points=[]
 def point(name,node,region='loop-selection'):points.append((name,node,region))
 point('loop-input-evaluation',loop.iter)
 for pair,record in zip(loop.iter.elts,inputs):
  label=record['name'];point('input-'+label+'-name',pair.elts[0]);point('input-'+label+'-object',pair.elts[1]);point('input-'+label+'-pair',pair)
 point('loop-inputs-complete',loop.iter);point('loop-iterator-attempt',loop)
 for record in inputs:
  label=record['name'];point(label+'-item-next',loop)
  for target in loop.target.elts:point(label+'-bind-'+target.id,target)
  point(label+'-guard-object',test.left);point(label+'-guard-none',test.comparators[0]);point(label+'-guard-result',test)
 # Expression traversal follows Python's callable-first, arguments-next order.
 point('selected-try-entry',protected,'try-entry')
 point('close-object-evaluation',close.value.func.value,'protected-close');point('close-method-evaluation',close.value.func,'protected-close');point('close-call-attempt',close.value,'protected-close');point('close-normal-return',close,'protected-close')
 call=append.value;sub=call.func.value;item=call.args[0]
 need(isinstance(sub,ast.Subscript) and isinstance(item,ast.List) and len(item.elts)==2,'CLEANUP-APPEND-PARTS')
 point('append-details-evaluation',sub.value,'protected-append');point('append-key-evaluation',sub.slice,'protected-append');point('append-list-resolution',sub,'protected-append');point('append-method-evaluation',call.func,'protected-append')
 for expression in item.elts:
  point('append-item-'+('name' if isinstance(expression,ast.Name) else 'message'),expression,'protected-append')
 point('append-item-complete',item,'protected-append');point('append-call-attempt',call,'protected-append');point('append-complete',append,'protected-append')
 return {'sources':pins,'ordered_inputs':inputs,'selected_name':inputs[1]['name'],'selected_slot':inputs[1]['slot'],'guard_expression':ast.unparse(test),'guard_semantics':'identity is not None; no truthiness substitution','guard_results':{'raw':False,'managed':True},
  'raw_origins':{'initial':loc(raw_init[0]),'create_close':loc(create.body[2]),'create_clear':loc(create.body[3])},'managed_initial':loc(managed_init[0]),'managed_assignment':loc(managed),'handoff':loc(yielded),'wrapper_reference':loc(init),
  'manager_close':{**ml(mc),'source':pins['manager']},'reference_close_program':copy.deepcopy(rp[0]),'close_method':close.value.func.attr,'close_arguments':[],'close_keywords':[],'close_return_use':'discarded expression result; no concrete return value asserted',
  'append_target_expression':ast.unparse(sub),'append_item_expressions':[ast.unparse(n) for n in item.elts],'append_message':item.elts[1].value,'inner_handler':{**loc(error_handler),'source':pins['launcher']},'inner_handler_name':error_handler.name,'same_try':loc(protected),
  'order':[n for n,_,_ in points],'stages':{n:{**loc(node),'source':copy.deepcopy(pins['launcher']),'semantic_region':region} for n,node,region in points},
  'continuity_premise':'Explicit conditional continuity of launcher locals, selected manager/method and details cleanup-list roles from validated handoff and completed details assignment. Not runtime identity, exclusivity, absence of mutation or qualification.',
  'raw_admissibility':'At the selected post-yield constructor-error route raw is None: initialized None on reopening, or cleared only after raw close returned on creation. A surviving partially constructed raw belongs to a different earlier route.',
  'stop':'Selected normal append only; no line172 error-report append, later iteration/loop completion, failure write, rethrow or owner-lock finalization'}

def compile_cleanup_append(launcher,entry,manager,details,reference):
 source=cleanup_append_source(launcher,entry,manager,details,reference)
 return {'format':'I164-EXCEPTIONAL-CLEANUP-APPEND-STATIC-1','source':source,'parent_catalogue_identity':{'sha256':digest((json.dumps(details,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode())},
  'declarations':[{'id':n,'source_origin':copy.deepcopy(source['stages'][n]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in source['order']],
  'guard_branches':{'parent':'Completed initial details assignment; original selected constructor error pending; no replacement','prefixes':['control absent','earlier control construction and callback completed normally'],'locals':'Same validated handoff under explicit continuity; raw None skipped, managed non-None selected','guard':'obj is not None by identity','normal':'Source-ordered progress; managed close return independently checked by reference-path interpreter before append','close_or_append_raise':'Distinct origins within same try; close_error handler is eligible but not entered/expanded by this slice','earlier_raise':'Loop input/iteration/binding/guard failures are outside the inner close_error try','termination':'No inferred Python exception or unwind','unobserved':'No further completion; absence of partial effects not established','continuity_unknown':'No loop-selection progress established'},
  'preserved_relations':['launcher_initial_details_correspondence',*details['preserved_relations']], 'runtime_cleanup_append_chain':None,'actual_admission':False}

def validate_cleanup_append(launcher,entry,manager,details,reference,submitted):
 status_exact_tree(submitted,'CLEANUP-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_cleanup_append(launcher,entry,manager,details,reference),'CLEANUP-SOURCE-CORRESPONDENCE');return True

def cleanup_append_binding(catalogue,parent,anchor,continuity):
 for v in (catalogue,parent,anchor,continuity):status_exact_tree(v,'CLEANUP-BINDING-TYPES')
 need(type(continuity) is str and continuity in ('explicit conditional premise','UNESTABLISHED'),'CLEANUP-CONTINUITY')
 scope=parent['scope'];refs=parent['delivery_binding']['references'];details=parent['details_in_model'];need(type(details) is dict,'CLEANUP-DETAILS-REQUIRED')
 return {'scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(anchor),'selected_error':copy.deepcopy(parent['earlier_constructor_exception']),'references':copy.deepcopy(refs),'ordered_values':[{'name':'raw','value':None,'exact_type':'NoneType'},{'name':'managed','value':copy.deepcopy(refs['manager']),'meaning':'source-qualified manager reference, not an observed Python object'}],
  'selected_index':1,'name':catalogue['source']['selected_name'],'object':copy.deepcopy(refs['manager']),'guard':{'expression':catalogue['source']['guard_expression'],'left':copy.deepcopy(refs['manager']),'right':None,'right_exact_type':'NoneType','result':True},
  'close_receiver':copy.deepcopy(refs['manager']),'method':catalogue['source']['close_method'],'method_origin':copy.deepcopy(catalogue['source']['manager_close']),'cleanup_list':copy.deepcopy(details['cleanup_reference']),'append_item':[catalogue['source']['selected_name'],catalogue['source']['append_message']],
  'continuity':continuity,'premise':catalogue['source']['continuity_premise'],'runtime_object_identity':None}

def cleanup_append_projection(catalogue,case,validated):
 for v in (catalogue,case,validated):status_exact_tree(v,'CLEANUP-EXACT-TYPE')
 keys={'scope','anchor','parent_result','binding','close_result','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'CLEANUP-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'CLEANUP-VALIDATED:'+k)
 parent=case['parent_result'];source=catalogue['source'];scope=case['scope'];anchor=case['anchor'];binding=case['binding'];error=parent['earlier_constructor_exception']
 need(parent['kind']=='CONSTRUCTED-LAUNCHER-INITIAL-DETAILS' and parent['details_assignment_completed_in_model'] is True and parent['replacement_error_in_model'] is None,'CLEANUP-COMPLETED-DETAILS')
 status_typed_same(parent['last_pending_error_in_model'],error,'CLEANUP-PENDING-ORIGINAL');status_typed_same(parent['active_caught_error_in_model'],error,'CLEANUP-ACTIVE-ORIGINAL');status_typed_same(scope,parent['scope'],'CLEANUP-PARENT-SCOPE');status_typed_same(anchor,parent['instance_anchor'],'CLEANUP-INSTANCE')
 status_typed_same(binding,cleanup_append_binding(catalogue,parent,anchor,binding['continuity']),'CLEANUP-SELECTED-BINDING')
 need(parent['cleanup_loop_entered'] is False,'CLEANUP-PARENT-FRONTIER');outcomes=case['outcomes'];need(type(outcomes) is list and bool(outcomes),'CLEANUP-OUTCOMES')
 if binding['continuity']=='UNESTABLISHED':status_typed_same(outcomes,[{'stage':source['order'][0],'outcome':'unobserved'}],'CLEANUP-UNKNOWN-CONTINUITY')
 events=[];done=set();replacement=None;terminal=None;close_reached=False;cr=case['close_result']
 for i,stage in enumerate(source['order']):
  need(i<len(outcomes),'CLEANUP-MISSING-STEP:'+stage);row=outcomes[i]
  need(type(row) is dict and set(row)=={'stage','outcome'} and type(row['stage']) is str and row['stage']==stage,'CLEANUP-STEP-ORDER');kind=row['outcome'];need(type(kind) is str and kind in ('normal','raise','process-termination','unobserved'),'CLEANUP-OUTCOME');terminal=kind
  if stage=='close-normal-return':
   close_reached=True
   if cr is None:need(kind in ('process-termination','unobserved'),'CLEANUP-MISSING-CLOSE-RELATION')
   elif cr['completion']=='normal':need(kind=='normal' and cr['final']=={'_live':None,'_retired':None,'_phase':'CLOSED'},'CLEANUP-CLOSE-NORMAL-CORRESPONDENCE')
   elif cr['completion']=='abrupt':need(kind=='raise','CLEANUP-CLOSE-RAISE-CORRESPONDENCE')
   else:need(cr['completion']=='partial-prefix' and kind in ('process-termination','unobserved'),'CLEANUP-CLOSE-PARTIAL-CORRESPONDENCE')
  origin=source['stages'][stage];events.append({'id':scope['invocation']+'/cleanup/'+stage,'scope':copy.deepcopy(scope),'stage':stage,'source':copy.deepcopy(origin),'outcome':kind,'selected_object':copy.deepcopy(binding['object']),'selected_error':copy.deepcopy(error),'runtime_frame':None})
  if kind!='normal':
   if kind=='raise':replacement={'role':'conditional-cleanup-error','reference':scope['invocation']+'/cleanup/'+stage+'/error','scope':copy.deepcopy(scope),'origin':copy.deepcopy(origin),'failure_region':origin['semantic_region'],'eligible_inner_handler':source['inner_handler_name'] if origin['semantic_region'] in ('protected-close','protected-append') else None,'handler_entry_established':False,'exact_type':None,'exact_value_bytes':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_observation':False}
   break
  done.add(stage)
 need(len(outcomes)==len(events),'CLEANUP-UNREACHED-STEPS')
 if not close_reached:need(cr is None,'CLEANUP-UNREACHED-CLOSE-RELATION')
 closed='close-normal-return' in done;appended='append-complete' in done;details=copy.deepcopy(parent['details_in_model'])
 if appended:details['known_literal_fields']['cleanup'].append(copy.deepcopy(binding['append_item']))
 return {'kind':'CONSTRUCTED-EXCEPTIONAL-CLEANUP-APPEND','scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(anchor),'validated_parent':copy.deepcopy(parent),'binding':copy.deepcopy(binding),'events':events,'completion':'selected-normal-append' if appended else {'raise':'exception-frontier','process-termination':'process-termination','unobserved':'unobserved-continuation'}[terminal],
  'earlier_constructor_exception':copy.deepcopy(error),'earlier_control_completed_in_model':parent['earlier_control_completed_in_model'],'selected_owner_continuity':copy.deepcopy(parent['selected_owner_continuity']),
  'raw_guard_false_completed_in_model':'raw-guard-result' in done,'selected_name_bound_in_model':'managed-bind-name' in done,'selected_object_bound_in_model':'managed-bind-obj' in done,'selected_non_none_guard_completed_in_model':'managed-guard-result' in done,
  'close_method_evaluation_completed_in_model':'close-method-evaluation' in done,'close_attempt_entered_in_model':any(e['stage']=='close-call-attempt' for e in events),'close_normal_return_completed_in_model':closed,'managed_close_relation':copy.deepcopy(cr),'close_return_value_observed':None,'close_return_use':source['close_return_use'],
  'append_evaluation_entered_in_model':any(e['stage']=='append-details-evaluation' for e in events),'append_attempt_entered_in_model':any(e['stage']=='append-call-attempt' for e in events),'append_completed_in_model':appended,'details_after_acknowledged_steps':details,'cleanup_list_after_frontier':'exact constructed appended item' if appended else 'UNKNOWN partial effects' if terminal!='normal' and any(e['stage']=='append-call-attempt' for e in events) else 'no append call reached in this modeled prefix',
  'replacement_error_in_model':replacement,'last_pending_error_in_model':copy.deepcopy(replacement or error),'close_itself_failed_established_in_model':close_reached and cr is not None and cr['completion']=='abrupt','terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True,
  'inner_handler_entry_established':False,'error_report_append_expanded':False,'later_iteration_established':False,'loop_completion_established':False,'failure_file_established':False,'final_rethrow_established':False,'owner_finalization_established':False,'managed_local_clear_established':False,'ACTIVE_unlink_established':False,
  'completion_flags_mean':'Acknowledged conditional modeled progress; false does not prove absence of partial effects','existing_cause_context_suppression':'UNKNOWN; selected original remains represented; no new exception chain evidence','runtime_cleanup_append_chain':None,'runtime_observation':False,'physical_reference_identity':None,'physical_closure_established':False,'durability_established':False,'released_ownership_established':False,'complete_cleanup_established':False,'observer_join':None,'obligations_discharged':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_cleanup_append_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'CLEANUP-SUBMITTED-OUTPUT');status_typed_same(submitted,cleanup_append_projection(catalogue,case,validated),'CLEANUP-OUTPUT-CORRESPONDENCE');return True

# Bounded line172 selected failure -> caught error -> error-item append.
def error_report_source(launcher,entry,manager,parent):
 for raw in (launcher,entry,manager):need(type(raw) is bytes,'REPORT-SOURCE-BYTES')
 status_exact_tree(parent,'REPORT-PARENT-CATALOGUE')
 pins={n:{'bytes':len(raw),'sha256':digest(raw)} for n,raw in [('launcher',launcher),('entry',entry),('manager',manager)]}
 status_typed_same(parent['source']['sources'],pins,'REPORT-PARENT-SOURCES')
 tree,loc=_client_locate(launcher)
 fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_session')
 outer=fn.body[-1].body[-1].handlers[0];loop=outer.body[1];protected=loop.body[0].body[0]
 need(outer.name=='e' and ast.unparse(outer.type)=='BaseException' and isinstance(protected,ast.Try) and len(protected.body)==2 and len(protected.handlers)==1 and not protected.orelse and not protected.finalbody,'REPORT-SHARED-TRY')
 h=protected.handlers[0];need(h.name=='close_error' and isinstance(h.type,ast.Name) and h.type.id=='BaseException' and len(h.body)==1,'REPORT-HANDLER')
 status_typed_same({**loc(h),'source':pins['launcher']},parent['source']['inner_handler'],'REPORT-HANDLER-ORIGIN')
 need([ast.unparse(n) for n in protected.body]==['obj.close()',"details['cleanup'].append([name, 'close returned'])"],'REPORT-PROTECTED-OPERATIONS')
 stmt=h.body[0];need(isinstance(stmt,ast.Expr) and isinstance(stmt.value,ast.Call),'REPORT-APPEND-STATEMENT')
 call=stmt.value
 need(ast.unparse(call)=="details['cleanup'].append([name, type(close_error).__name__, str(close_error)])" and not call.keywords and len(call.args)==1,'REPORT-ITEM-EXPRESSION')
 sub=call.func.value;item=call.args[0];name,ename,message=item.elts
 need(isinstance(call.func,ast.Attribute) and call.func.attr=='append' and isinstance(sub,ast.Subscript) and isinstance(item,ast.List) and isinstance(ename,ast.Attribute) and ename.attr=='__name__','REPORT-EXPRESSION-SHAPE')
 points=[]
 def point(label,node,region):points.append((label,node,region))
 # Semantic boundaries, not claims about Python allocation or opcode history.
 point('handler-type-evaluation',h.type,'handler-matching')
 point('handler-match',h.type,'handler-matching')
 point('handler-selection',h,'handler-selection')
 point('handler-entry',h,'handler-entry')
 point('caught-error-binding-attempt',h,'caught-binding')
 point('caught-error-binding-complete',h,'caught-binding')
 # Callable first; then list elements left-to-right, including inner callables.
 point('report-details-evaluation',sub.value,'report-target')
 point('report-key-evaluation',sub.slice,'report-target')
 point('report-list-resolution',sub,'report-target')
 point('report-method-evaluation',call.func,'report-target')
 point('report-item-name',name,'report-item')
 point('error-type-callable',ename.value.func,'report-item')
 point('error-type-argument',ename.value.args[0],'report-item')
 point('error-type-call-attempt',ename.value,'report-item')
 point('error-type-call-return',ename.value,'report-item')
 point('error-name-attribute',ename,'report-item')
 point('error-str-callable',message.func,'report-item')
 point('error-str-argument',message.args[0],'report-item')
 point('error-str-call-attempt',message,'report-item')
 point('error-str-call-return',message,'report-item')
 point('report-item-complete',item,'report-item')
 point('report-append-attempt',call,'report-append')
 point('report-append-complete',stmt,'report-append')
 protected_stages={n:copy.deepcopy(v) for n,v in parent['source']['stages'].items() if v['semantic_region'] in ('protected-close','protected-append')}
 need(bool(protected_stages),'REPORT-PROTECTED-DOMAIN')
 return {'sources':pins,'handler':{**loc(h),'source':pins['launcher']},'catch_family':h.type.id,'catch_name':h.name,'shared_try':loc(protected),
  'eligible_parent_stages':protected_stages,'name_expression':ast.unparse(name),'target_expression':ast.unparse(sub),'item_expressions':[ast.unparse(x) for x in item.elts],
  'dynamic_origins':{'error_name':{**loc(ename),'source':pins['launcher']},'message':{**loc(message),'source':pins['launcher']}},
  'order':[n for n,_,_ in points],'stages':{n:{**loc(node),'source':copy.deepcopy(pins['launcher']),'semantic_region':region} for n,node,region in points},
  'continuity':'Explicit conditional selected-error delivery and owner/local/name/details/list/method continuity; not runtime identity or exclusivity',
  'stop':'Selected error-item append completion or first nonnormal frontier; handler exit and all later cleanup remain unestablished'}

def compile_error_report(launcher,entry,manager,parent):
 source=error_report_source(launcher,entry,manager,parent)
 return {'format':'I164-CLEANUP-ERROR-REPORT-STATIC-1','source':source,'parent_catalogue_identity':{'sha256':digest((json.dumps(parent,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode())},
  'declarations':[{'id':n,'source_origin':copy.deepcopy(source['stages'][n]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in source['order']],
  'guard_branches':{'parent':'Selected actual modeled raise within the same protected close/normal-append try; not an outside failure, normal return, process termination or unobserved frontier',
   'continuity':'Explicit conditional premise or UNESTABLISHED; unknown establishes no handler progress','prefixes':['control absent','earlier control construction and callback completed normally'],
   'close_vs_append':'Preserve selected origin and any acknowledged normal close; caught name does not imply close failed',
   'normal':'Successful suboperations retain original constructor and active selected caught error; no normal overall return or handler exit',
   'raise':'Later matching/binding/reporting error distinct from selected cleanup error and constructor error',
   'termination':'None terminal-exception classification; no inferred unwind or completed reporting',
   'unobserved':'None terminal-exception classification; earlier acknowledged facts retained, continuation unknown',
   'partial_effects':'Earlier uncertain append effects survive successful error reporting; no exact complete list inferred'},
  'preserved_relations':['exceptional_cleanup_append_correspondence',*parent['preserved_relations']],
  'runtime_error_report_chain':None,'actual_admission':False}

def validate_error_report(launcher,entry,manager,parent,submitted):
 status_exact_tree(submitted,'REPORT-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_error_report(launcher,entry,manager,parent),'REPORT-SOURCE-CORRESPONDENCE');return True

def error_report_binding(catalogue,parent,anchor,continuity):
 for v in (catalogue,parent,anchor,continuity):status_exact_tree(v,'REPORT-BINDING-TYPES')
 need(type(continuity) is str and continuity in ('explicit conditional premise','UNESTABLISHED'),'REPORT-CONTINUITY-DOMAIN')
 need(parent['kind']=='CONSTRUCTED-EXCEPTIONAL-CLEANUP-APPEND' and parent['completion']=='exception-frontier' and parent['terminal_python_exception_in_model'] is True,'REPORT-PARENT-FAILURE')
 err=parent['replacement_error_in_model'];need(type(err) is dict and bool(parent['events']),'REPORT-SELECTED-ERROR')
 event=parent['events'][-1];source=catalogue['source'];stage=event['stage']
 need(event['outcome']=='raise' and stage in source['eligible_parent_stages'],'REPORT-PROTECTED-FAILURE')
 origin=source['eligible_parent_stages'][stage]
 status_typed_same(event['source'],origin,'REPORT-FAILURE-OCCURRENCE-SOURCE');status_typed_same(err['origin'],origin,'REPORT-ERROR-ORIGIN')
 need(err['eligible_inner_handler']==source['catch_name'] and err['handler_entry_established'] is False and parent['inner_handler_entry_established'] is False,'REPORT-HANDLER-FRONTIER')
 scope=parent['scope'];status_typed_same(err['scope'],scope,'REPORT-ERROR-SCOPE');status_typed_same(event['scope'],scope,'REPORT-EVENT-SCOPE');status_typed_same(parent['instance_anchor'],anchor,'REPORT-INSTANCE')
 status_typed_same(parent['last_pending_error_in_model'],err,'REPORT-PENDING-SELECTED')
 need(err['reference']==scope['invocation']+'/cleanup/'+stage+'/error' and event['id']==scope['invocation']+'/cleanup/'+stage,'REPORT-FAILURE-OCCURRENCE')
 details=parent['details_after_acknowledged_steps'];b=parent['binding']
 return {'scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(anchor),'selected_failure':copy.deepcopy(err),'failure_occurrence':copy.deepcopy(event),'constructor_error':copy.deepcopy(parent['earlier_constructor_exception']),
  'references':copy.deepcopy(b['references']),'selected_name':b['name'],'selected_object':copy.deepcopy(b['object']),
  'details_role':{'role':details['role'],'reference':details['reference'],'scope':copy.deepcopy(details['scope'])},'cleanup_list':copy.deepcopy(details['cleanup_reference']),
  'caught_name':source['catch_name'],'handler_origin':copy.deepcopy(source['handler']),'continuity':continuity,'premise':source['continuity'],
  'physical_identity_observed':None,'runtime_delivery_observed':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN'}

def error_report_projection(catalogue,case,validated):
 for v in (catalogue,case,validated):status_exact_tree(v,'REPORT-EXACT-TYPE')
 keys={'scope','anchor','parent_result','binding','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'REPORT-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'REPORT-VALIDATED:'+k)
 source=catalogue['source'];parent=case['parent_result'];scope=case['scope'];anchor=case['anchor'];binding=case['binding']
 status_typed_same(scope,parent['scope'],'REPORT-PARENT-SCOPE');status_typed_same(anchor,parent['instance_anchor'],'REPORT-PARENT-INSTANCE')
 status_typed_same(binding,error_report_binding(catalogue,parent,anchor,binding['continuity']),'REPORT-EXPECTED-BINDING')
 selected=binding['selected_failure'];original=binding['constructor_error'];outcomes=case['outcomes']
 need(type(outcomes) is list and bool(outcomes),'REPORT-OUTCOMES')
 if binding['continuity']=='UNESTABLISHED':status_typed_same(outcomes,[{'stage':source['order'][0],'outcome':'unobserved'}],'REPORT-UNKNOWN-CONTINUITY')
 events=[];done=set();replacement=None;terminal=None
 for i,stage in enumerate(source['order']):
  need(i<len(outcomes),'REPORT-MISSING-STEP:'+stage);row=outcomes[i]
  need(type(row) is dict and set(row)=={'stage','outcome'} and type(row['stage']) is str and row['stage']==stage,'REPORT-STEP-ORDER')
  terminal=row['outcome'];need(type(terminal) is str and terminal in ('normal','raise','process-termination','unobserved'),'REPORT-OUTCOME')
  origin=source['stages'][stage];events.append({'id':scope['invocation']+'/error-report/'+stage,'scope':copy.deepcopy(scope),'stage':stage,'source':copy.deepcopy(origin),'outcome':terminal,'selected_failure_occurrence':copy.deepcopy(binding['failure_occurrence']),'selected_error':copy.deepcopy(selected),'owner':copy.deepcopy(binding['references']['owner']),'token':copy.deepcopy(binding['references']['token']),'runtime_frame':None})
  if terminal!='normal':
   if terminal=='raise':replacement={'role':'conditional-error-report-replacement','reference':scope['invocation']+'/error-report/'+stage+'/error','scope':copy.deepcopy(scope),'origin':copy.deepcopy(origin),'exact_type':None,'exact_value_bytes':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_observation':False}
   break
  done.add(stage)
 need(len(outcomes)==len(events),'REPORT-UNREACHED-STEPS')
 entered='handler-entry' in done;bound='caught-error-binding-complete' in done;appended='report-append-complete' in done
 def symbolic(which):
  idx=1 if which=='error_name' else 2
  return {'role':'unobserved-error-report-'+which,'expression':source['item_expressions'][idx],'origin':copy.deepcopy(source['dynamic_origins'][which]),'argument':copy.deepcopy(selected),'caught_name':source['catch_name'],'exact_type':None,'exact_value':None,'formatted_bytes':None,'runtime_observation':False}
 item=[binding['selected_name'],symbolic('error_name'),symbolic('message')] if 'report-item-complete' in done else None
 attempt=any(e['stage']=='report-append-attempt' for e in events)
 prior_unknown=parent['cleanup_list_after_frontier']=='UNKNOWN partial effects'
 current_unknown=attempt and not appended
 details=copy.deepcopy(parent['details_after_acknowledged_steps'])
 return {'kind':'CONSTRUCTED-CLEANUP-ERROR-REPORT','scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(anchor),'validated_parent':copy.deepcopy(parent),'binding':copy.deepcopy(binding),'events':events,
  'completion':'selected-error-item-append' if appended else {'raise':'replacement-exception-frontier','process-termination':'process-termination','unobserved':'unobserved-continuation'}[terminal],
  'earlier_constructor_exception':copy.deepcopy(original),'selected_cleanup_error':copy.deepcopy(selected),'selected_failure_occurrence':copy.deepcopy(binding['failure_occurrence']),
  'failure_origin_region':selected['failure_region'],'earlier_control_completed_in_model':parent['earlier_control_completed_in_model'],'selected_owner_continuity':copy.deepcopy(parent['selected_owner_continuity']),
  'handler_eligible_in_model':True,'handler_match_completed_in_model':'handler-match' in done,'handler_selected_in_model':'handler-selection' in done,'handler_entry_completed_in_model':entered,
  'caught_binding_attempted_in_model':any(e['stage']=='caught-error-binding-attempt' for e in events),'caught_binding_completed_in_model':bound,'caught_name_in_model':source['catch_name'] if bound else None,'caught_error_in_model':copy.deepcopy(selected) if bound else None,
  'last_acknowledged_active_caught_error_in_model':copy.deepcopy(selected if entered else original),'active_at_terminal_observed':None,
  'original_error_pending_in_outer_handler':copy.deepcopy(original),'last_pending_error_in_model':copy.deepcopy(replacement or selected),'replacement_error_in_model':replacement,
  'pending_disposition':'Selected cleanup error remains represented inside its handler until handler exit, which is not modeled; no eventual propagation asserted',
  'terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True,'normal_overall_return_established':False,
  'close_normal_return_completed_in_model':parent['close_normal_return_completed_in_model'],'close_itself_failed_established_in_model':parent['close_itself_failed_established_in_model'],'managed_close_relation':copy.deepcopy(parent['managed_close_relation']),
  'error_item_completed_in_model':item is not None,'error_item_in_model':item,'report_append_attempted_in_model':attempt,'report_append_completed_in_model':appended,
  'details_after_predecessor_acknowledged_steps':details,
  'cleanup_list_state':{'target':copy.deepcopy(binding['cleanup_list']),'last_predecessor_acknowledged_literals':copy.deepcopy(details['known_literal_fields']['cleanup']),
   'prior_partial_effects':'UNKNOWN' if prior_unknown else 'No earlier append call reached in validated prefix','current_partial_effects':'UNKNOWN' if current_unknown else 'Acknowledged selected error-item append' if appended else 'No error-item append call reached',
   'any_unresolved_partial_effects':prior_unknown or current_unknown,'acknowledged_append':{'item':copy.deepcopy(item),'target':copy.deepcopy(binding['cleanup_list']),'occurrence':scope['invocation']+'/error-report/report-append-complete'} if appended else None,
   'complete_contents_established':False,'exact_runtime_contents':None},
  'known_false_flags_preserved':{k:details['known_literal_fields'][k] for k in ('nonexecution_established','new_authorization')},
  'dynamic_details_origins_preserved':copy.deepcopy(details['dynamic_fields']),
  'handler_exit_established':False,'later_iteration_established':False,'loop_completion_established':False,'failure_file_established':False,'final_rethrow_established':False,'owner_finalization_established':False,'complete_cleanup_established':False,
  'existing_cause_context_suppression':'UNKNOWN; no new explicit-cause or suppression assignment; original, selected and replacement errors remain distinct',
  'runtime_error_report_chain':None,'runtime_observation':False,'observer_join':None,'physical_reference_identity':None,'physical_closure_established':False,'durability_established':False,'released_ownership_established':False,
  'completion_flags_mean':'Acknowledged conditional progress, not observed objects/opcodes; false does not prove absence of partial effects','obligations_discharged':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_error_report_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'REPORT-SUBMITTED-OUTPUT');status_typed_same(submitted,error_report_projection(catalogue,case,validated),'REPORT-OUTPUT-CORRESPONDENCE');return True

# Bounded post-line172 continuation. The entire reviewed producer above is unchanged.
def cleanup_loop_source(launcher,entry,manager,report,cleanup):
 for raw in (launcher,entry,manager):need(type(raw) is bytes,'LOOP-SOURCE-BYTES')
 for value in (report,cleanup):status_exact_tree(value,'LOOP-PARENT-CATALOGUES')
 validate_error_report(launcher,entry,manager,cleanup,report)
 tree,loc=_client_locate(launcher);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_session')
 outer=fn.body[-1].body[-1].handlers[0];loop=outer.body[1];guard=loop.body[0];protected=guard.body[0];handler=protected.handlers[0]
 need(outer.name=='e' and isinstance(loop,ast.For) and not loop.orelse and len(loop.body)==1 and len(guard.body)==1 and not guard.orelse,'LOOP-EXACT-BODY')
 need(isinstance(loop.iter,ast.List) and len(loop.iter.elts)==2 and ast.unparse(loop.target)=='(name, obj)','LOOP-FINITE-INPUTS')
 pairs=[[p.elts[0].value,p.elts[1].id] for p in loop.iter.elts];status_typed_same(pairs,[['raw','raw'],['managed','managed']],'LOOP-ORDERED-INPUTS')
 need(ast.unparse(guard.test)=='obj is not None' and handler.name=='close_error' and len(handler.body)==1 and not protected.finalbody and not protected.orelse,'LOOP-HANDLER-TAIL')
 need(not any(isinstance(n,(ast.Break,ast.Continue,ast.Return,ast.Yield,ast.YieldFrom)) for n in ast.walk(handler)),'LOOP-NORMAL-DEPARTURE-SHAPE')
 pin=report['source']['sources']['launcher'];status_typed_same({**loc(handler),'source':pin},report['source']['handler'],'LOOP-EXACT-HANDLER')
 need(report['source']['order'][-1]=='report-append-complete','LOOP-PREDECESSOR-FRONTIER')
 status_typed_same([[x['name'],x['slot']] for x in cleanup['source']['ordered_inputs']],pairs,'LOOP-PREDECESSOR-INPUTS')
 following=outer.body[2];need(isinstance(following,ast.Try) and following.lineno==174,'LOOP-STOP-BEFORE-WRITE')
 # These are semantic acknowledgments, not a claimed sequence of hidden opcodes.
 # Name clearing and handled-error restoration form one normal departure boundary.
 points=[('inner-handler-departure-attempt',handler),('inner-handler-exit-complete',handler),('selected-loop-body-complete',guard),('final-iterator-advance-attempt',loop),('ordinary-iterator-exhaustion',loop.iter),('cleanup-loop-complete',loop)]
 return {'sources':copy.deepcopy(report['source']['sources']),'handler':copy.deepcopy(report['source']['handler']),'outer_caught_name':outer.name,'caught_name':handler.name,
  'loop':{**loc(loop),'source':copy.deepcopy(pin)},'ordered_inputs':copy.deepcopy(cleanup['source']['ordered_inputs']),'entry_count':len(pairs),'selected_index':len(pairs)-1,'next_index':len(pairs),
  'guard_expression':ast.unparse(guard.test),'required_guard_results':{'raw':False,'managed':True},'target_names':[n.id for n in loop.target.elts],
  'order':[n for n,_ in points],'stages':{n:{**loc(node),'source':copy.deepcopy(pin),'semantic_region':'post-error-report-loop-continuation'} for n,node in points},
  'normal_outcomes':{n:('exhausted' if n=='ordinary-iterator-exhaustion' else 'normal') for n,_ in points},
  'selection_prefix':[{ 'stage':n,'source':copy.deepcopy(s)} for n in cleanup['source']['order'] for s in [cleanup['source']['stages'][n]] if s['semantic_region']=='loop-selection'],
  'language_contract':{'reference':'https://docs.python.org/3.12/reference/compound_stmts.html','sections':['8.3 for','8.4.1 except'],
   'scope':'Retained CPython 3.12.14 conditional semantics; family language rules, not runtime qualification or exact opcode observation',
   'rules':['Normal handler departure clears its as-target and restores the previously handled exception; no assertion of physical destruction or internal substep order',
    'A for iterable expression is evaluated once; yielded entries bind targets in order; ordinary exhaustion ends the loop without a new propagating error',
    'For target names remain bound after loop completion; caught-name clearing is a different lifetime rule'],
   'premises':'Explicit continuity of the exact source-created two-entry list/iterator and selected locals, references, exception and details/list roles; no hostile replacement, extra entry or mutation inferred absent'},
  'continuity':'explicit conditional selected-owner, invocation, exception, local, handler, details/list and finite-loop iterator continuity; not observed identity or exclusivity',
  'stop_before':{**loc(following.body[0].value),'source':copy.deepcopy(pin)}}

def compile_cleanup_loop(launcher,entry,manager,report,cleanup):
 s=cleanup_loop_source(launcher,entry,manager,report,cleanup)
 return {'format':'I164-CLEANUP-LOOP-STATIC-1','source':s,'parent_catalogue_identity':{'sha256':digest((json.dumps(report,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode())},
  'declarations':[{'id':n,'source_origin':copy.deepcopy(s['stages'][n]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in s['order']],
  'guard_branches':{'parent':'Actual validated completed selected line172 append, bound error, original constructor pending; no replacement',
   'continuity':'Explicit conditional premise or UNESTABLISHED; append completion alone establishes no continuation',
   'prefixes':['control absent','earlier control construction and callback completed normally'],'origins':['protected-close','protected-append'],
   'normal':'Explicit stage outcomes through ordinary exhaustion of exact two-entry loop; original constructor remains pending in outer handler',
   'nonnormal':'First raise, catchable interruption, process termination or unobserved frontier stops; no inferred later completion',
   'name_lifetime':'Cleared local caught-name is separate from retained error evidence and last acknowledged caught error',
   'partial_effects':'Carry acknowledged reporting/close facts and UNKNOWN earlier append effects unchanged'},
  'preserved_relations':['cleanup_error_report_correspondence',*report['preserved_relations']],'runtime_loop_chain':None,'actual_admission':False}

def validate_cleanup_loop(launcher,entry,manager,report,cleanup,submitted):
 status_exact_tree(submitted,'LOOP-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_cleanup_loop(launcher,entry,manager,report,cleanup),'LOOP-SOURCE-CORRESPONDENCE');return True

def cleanup_loop_binding(catalogue,parent,anchor,continuity):
 for v in (catalogue,parent,anchor,continuity):status_exact_tree(v,'LOOP-BINDING-TYPES')
 need(type(continuity) is str and continuity in ('explicit conditional premise','UNESTABLISHED'),'LOOP-CONTINUITY-DOMAIN')
 s=catalogue['source'];need(parent['kind']=='CONSTRUCTED-CLEANUP-ERROR-REPORT' and parent['completion']=='selected-error-item-append' and parent['report_append_completed_in_model'] is True and parent['caught_binding_completed_in_model'] is True,'LOOP-COMPLETED-PREDECESSOR')
 need(parent['terminal_python_exception_in_model'] is True and parent['replacement_error_in_model'] is None and parent['handler_exit_established'] is False and parent['loop_completion_established'] is False,'LOOP-PARENT-FRONTIER')
 status_typed_same(parent['instance_anchor'],anchor,'LOOP-INSTANCE');b=parent['binding'];scope=parent['scope'];pre=parent['validated_parent'];pb=pre['binding']
 status_typed_same(parent['original_error_pending_in_outer_handler'],parent['earlier_constructor_exception'],'LOOP-ORIGINAL-PENDING')
 status_typed_same(parent['last_pending_error_in_model'],parent['selected_cleanup_error'],'LOOP-CAUGHT-PENDING-ROLE')
 status_typed_same(parent['caught_error_in_model'],parent['selected_cleanup_error'],'LOOP-CAUGHT-ERROR');status_typed_same(b['handler_origin'],s['handler'],'LOOP-HANDLER')
 need(parent['caught_name_in_model']==s['caught_name'] and b['selected_name']=='managed' and pb['ordered_values'][0]=={'name':'raw','value':None,'exact_type':'NoneType'},'LOOP-SELECTION')
 status_typed_same(pb['ordered_values'][1]['value'],b['selected_object'],'LOOP-SELECTED-OBJECT');need(pb['guard']['result'] is True and pb['guard']['right'] is None,'LOOP-SELECTED-GUARD')
 prefix=s['selection_prefix'];need(len(pre['events'])>len(prefix),'LOOP-SELECTION-EVENTS')
 for expected,event in zip(prefix,pre['events']):
  need(event['stage']==expected['stage'] and event['outcome']=='normal','LOOP-SELECTION-PREFIX');status_typed_same(event['source'],expected['source'],'LOOP-SELECTION-ORIGIN');status_typed_same(event['scope'],scope,'LOOP-SELECTION-SCOPE')
 event=parent['events'][-1];need(event['stage']=='report-append-complete' and event['outcome']=='normal' and event['id']==scope['invocation']+'/error-report/report-append-complete','LOOP-APPEND-OCCURRENCE')
 status_typed_same(event['scope'],scope,'LOOP-APPEND-SCOPE');status_typed_same(event['owner'],b['references']['owner'],'LOOP-APPEND-OWNER');status_typed_same(event['token'],b['references']['token'],'LOOP-APPEND-TOKEN')
 status_typed_same(parent['cleanup_list_state']['acknowledged_append']['target'],b['cleanup_list'],'LOOP-APPEND-LIST')
 return {'scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(anchor),'append_occurrence':copy.deepcopy(event),'handler_origin':copy.deepcopy(s['handler']),
  'original_constructor_error':copy.deepcopy(parent['earlier_constructor_exception']),'selected_cleanup_error':copy.deepcopy(parent['selected_cleanup_error']),'protected_failure_occurrence':copy.deepcopy(parent['selected_failure_occurrence']),
  'references':copy.deepcopy(b['references']),'selected_name':b['selected_name'],'selected_object':copy.deepcopy(b['selected_object']),'details_role':copy.deepcopy(b['details_role']),'cleanup_list':copy.deepcopy(b['cleanup_list']),
  'loop':{'ordered_values':copy.deepcopy(pb['ordered_values']),'entry_count':s['entry_count'],'selected_index':s['selected_index'],'next_index':s['next_index'],'raw_guard':False,'raw_body_skipped':True,'managed_guard':True,'selected_is_last':True,'iterator_role':scope['invocation']+'/launcher/cleanup-loop/iterator','source':copy.deepcopy(s['loop'])},
  'continuity':continuity,'premise':s['continuity'],'physical_identity_observed':None,'runtime_continuation_observed':None}

def cleanup_loop_projection(catalogue,case,validated):
 for v in (catalogue,case,validated):status_exact_tree(v,'LOOP-EXACT-TYPE')
 keys={'scope','anchor','parent_result','binding','outcomes'};need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'LOOP-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'LOOP-VALIDATED:'+k)
 s=catalogue['source'];p=case['parent_result'];scope=case['scope'];binding=case['binding'];outcomes=case['outcomes']
 status_typed_same(scope,p['scope'],'LOOP-PARENT-SCOPE');status_typed_same(binding,cleanup_loop_binding(catalogue,p,case['anchor'],binding['continuity']),'LOOP-EXPECTED-BINDING')
 need(type(outcomes) is list and bool(outcomes),'LOOP-EXPLICIT-CONTINUATION')
 if binding['continuity']=='UNESTABLISHED':status_typed_same(outcomes,[{'stage':s['order'][0],'outcome':'unobserved'}],'LOOP-UNKNOWN-CONTINUITY')
 events=[];done=set();replacement=None;terminal=None
 for i,stage in enumerate(s['order']):
  need(i<len(outcomes),'LOOP-MISSING-STEP:'+stage);row=outcomes[i]
  need(type(row) is dict and set(row)=={'stage','outcome'} and type(row['stage']) is str and row['stage']==stage,'LOOP-STEP-ORDER')
  terminal=row['outcome'];normal=s['normal_outcomes'][stage];need(type(terminal) is str and terminal in (normal,'raise','catchable-interruption','process-termination','unobserved'),'LOOP-OUTCOME')
  origin=s['stages'][stage];events.append({'id':scope['invocation']+'/cleanup-loop/'+stage,'scope':copy.deepcopy(scope),'stage':stage,'source':copy.deepcopy(origin),'outcome':terminal,'append_occurrence':binding['append_occurrence']['id'],'owner':copy.deepcopy(binding['references']['owner']),'token':copy.deepcopy(binding['references']['token']),'runtime_frame':None})
  if terminal!=normal:
   if terminal in ('raise','catchable-interruption'):replacement={'role':'conditional-loop-continuation-replacement','reference':scope['invocation']+'/cleanup-loop/'+stage+'/error','scope':copy.deepcopy(scope),'origin':copy.deepcopy(origin),'mode':terminal,'exact_type':None,'exact_value_bytes':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_observation':False}
   break
  done.add(stage)
 need(len(outcomes)==len(events),'LOOP-UNREACHED-STEPS')
 exited='inner-handler-exit-complete' in done;complete='cleanup-loop-complete' in done;original=binding['original_constructor_error'];selected=binding['selected_cleanup_error'];uncertain=terminal in ('process-termination','unobserved')
 return {'kind':'CONSTRUCTED-CLEANUP-LOOP','scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(case['anchor']),'validated_parent':copy.deepcopy(p),'binding':copy.deepcopy(binding),'events':events,
  'completion':'normal-cleanup-loop-exhaustion' if complete else {'raise':'replacement-exception-frontier','catchable-interruption':'interruption-frontier','process-termination':'process-termination','unobserved':'unobserved-continuation'}[terminal],
  'handler_exit_established':exited,'selected_body_complete':'selected-loop-body-complete' in done,'final_advance_attempted':any(e['stage']=='final-iterator-advance-attempt' for e in events),'ordinary_exhaustion_established':'ordinary-iterator-exhaustion' in done,'loop_completion_established':complete,
  'caught_name_lifetime':{'name':s['caught_name'],'last_acknowledged_binding':'CLEARED' if exited else 'BOUND selected cleanup error','normal_departure_clears_name':True,'state_at_nonnormal_frontier':'UNOBSERVED' if not complete else 'CONDITIONAL normal completion','physical_destruction_established':False},
  'retained_cleanup_error_evidence':copy.deepcopy(selected),'last_acknowledged_inner_caught_error':copy.deepcopy(selected),'last_acknowledged_active_caught_error_in_model':copy.deepcopy(original if exited else selected),'active_error_at_terminal_observed':None,
  'original_error_pending_in_outer_handler':copy.deepcopy(original),'last_pending_error_in_model':copy.deepcopy(replacement or (original if exited else selected)),'replacement_error_in_model':replacement,
  'terminal_python_exception_in_model':None if uncertain else True,'ordinary_exhaustion_is_new_propagating_error':False,'normal_overall_return_established':False,
  'loop_target_bindings_retained':{'name':binding['selected_name'],'obj':copy.deepcopy(binding['selected_object']),'conditional_continuity':binding['continuity']},'additional_body_execution_established':False,
  'earlier_control_completed_in_model':p['earlier_control_completed_in_model'],'selected_owner_continuity':copy.deepcopy(p['selected_owner_continuity']),'failure_origin_region':p['failure_origin_region'],
  'close_normal_return_completed_in_model':p['close_normal_return_completed_in_model'],'close_itself_failed_established_in_model':p['close_itself_failed_established_in_model'],'managed_close_relation':copy.deepcopy(p['managed_close_relation']),
  'report_append_completed_in_model':True,'cleanup_list_state':copy.deepcopy(p['cleanup_list_state']),'details_after_predecessor_acknowledged_steps':copy.deepcopy(p['details_after_predecessor_acknowledged_steps']),'known_false_flags_preserved':copy.deepcopy(p['known_false_flags_preserved']),'dynamic_details_origins_preserved':copy.deepcopy(p['dynamic_details_origins_preserved']),
  'existing_cause_context_suppression':'UNKNOWN; no new explicit cause/context/suppression evidence or assignment; all error roles retained',
  'line174_evaluation_established':False,'failure_file_established':False,'line175_suppression_established':False,'final_rethrow_established':False,'owner_finalization_established':False,'managed_local_clear_established':False,'active_removal_established':False,'complete_cleanup_established':False,
  'runtime_loop_chain':None,'runtime_observation':False,'observer_join':None,'physical_reference_identity':None,'physical_closure_established':False,'durability_established':False,'released_ownership_established':False,'obligations_discharged':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False,
  'completion_flags_mean':'Explicit conditional acknowledgments; false does not establish absence of partial effects; no physical object or interpreter execution observed'}

def validate_cleanup_loop_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'LOOP-SUBMITTED-OUTPUT');status_typed_same(submitted,cleanup_loop_projection(catalogue,case,validated),'LOOP-OUTPUT-CORRESPONDENCE');return True

# NEW replacement construction, 2026-11-03. No unavailable earlier bytes recovered.
def write_call_source(launcher,entry,manager,loop,report,cleanup):
 for b in (launcher,entry,manager):need(type(b) is bytes,'WC-SOURCE-TYPE')
 validate_cleanup_loop(launcher,entry,manager,report,cleanup,loop)
 tree,oldloc=_client_locate(launcher);functions={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
 fn=functions['_session'];owner=fn.body[-1];outer=owner.body[-1].handlers[0];region=outer.body[2]
 need(isinstance(region,ast.Try) and region.lineno==174 and len(region.body)==1 and not region.orelse and not region.finalbody,'WC-PROTECTED-SOURCE')
 call=region.body[0].value
 syntax="write_new(dest/'evidence'/('failure-'+str(os.getpid())+'-'+str(len(list((dest/'evidence').iterdir())))+'.json'),details)"
 need(ast.dump(call,include_attributes=False)==ast.dump(ast.parse(syntax,mode='eval').body,include_attributes=False),'WC-EXACT-EXPRESSION')
 pin=loop['source']['sources']['launcher'];status_typed_same(loop['source']['stop_before'],{**oldloc(call),'source':pin},'WC-PREDECESSOR-FRONTIER')
 lock=functions['owner_lock'];callee=functions['write_new']
 need(ast.unparse(owner.items[0].context_expr)=='owner_lock(destination)' and ast.unparse(owner.items[0].optional_vars)=='dest','WC-OWNER-BRIDGE')
 need(ast.unparse(lock.body[0])=='dest = Path(destination).absolute()' and ast.unparse(lock.body[2])=='parent = dest.parent.resolve()' and ast.unparse(lock.body[4])=='dest = parent / dest.name','WC-DESTINATION-ORIGIN')
 ys=[n for n in ast.walk(lock) if isinstance(n,ast.Yield)];need(len(ys)==1 and ast.unparse(ys[0].value)=='dest','WC-DESTINATION-YIELD')
 need([a.arg for a in callee.args.args]==['p','x'] and not callee.args.defaults and not callee.args.vararg and not callee.args.kwarg,'WC-CALLEE-ARGS')
 def loc(n):return {'source':copy.deepcopy(pin),'site':[n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__],'expression':ast.get_source_segment(launcher.decode(),n)}
 steps=[]
 def add(path,node,op,inputs,normal='normal',**kw):
  ident='write:'+path;need(ident not in {s['id'] for s in steps},'WC-UNIQUE-DECLARATION')
  steps.append({'id':ident,'source':loc(node),'operation':op,'inputs':inputs,'normal_outcome':normal,**kw});return ident
 add('continuation',region,'explicit continuation into selected protecting try',[])
 def visit(n,path):
  if isinstance(n,ast.Name):
   need(isinstance(n.ctx,ast.Load),'WC-NAME-LOAD');return add(path,n,'name lookup',[],name=n.id)
  if isinstance(n,ast.Constant):
   need(type(n.value) is str,'WC-LITERAL-TYPE');return add(path,n,'literal',[],literal=n.value)
  if isinstance(n,ast.Attribute):return add(path,n,'attribute lookup',[visit(n.value,path+'.base')],attribute=n.attr)
  if isinstance(n,ast.BinOp):
   need(type(n.op) in (ast.Add,ast.Div),'WC-OPERATOR');a=visit(n.left,path+'.left');b=visit(n.right,path+'.right');return add(path,n,'binary operation',[a,b],operator=type(n.op).__name__)
  if isinstance(n,ast.Call):
   need(not n.keywords and not any(isinstance(a,ast.Starred) for a in n.args),'WC-CALL-SHAPE')
   f=visit(n.func,path+'.callable');args=[visit(a,path+'.arg'+str(i)) for i,a in enumerate(n.args)]
   attempt=add(path+'.attempt',n,'nested call attempt',[f,*args],normal='attempted')
   return add(path+'.return',n,'nested normal return',[attempt])
  need(False,'WC-UNSUPPORTED-EXPRESSION')
 f=visit(call.func,'callable');args=[visit(a,'arg'+str(i)) for i,a in enumerate(call.args)]
 add('call-attempt',call,'write_new call attempt; body excluded',[f,*args],normal='attempted')
 return {'sources':copy.deepcopy(loop['source']['sources']),'call':loc(call),'outer_handler':loc(outer),'callee':loc(callee),'callee_parameters':['p','x'],'owner_lock':oldloc(lock),'destination_bridge':loc(owner.items[0].context_expr),'destination_yield':loc(ys[0]),'stop_before':loc(callee.body[0]),'steps':steps,'order':[s['id'] for s in steps],'normal_outcomes':{s['id']:s['normal_outcome'] for s in steps},'callable_step':f,'arguments':args,
  'language_contract':{'version':'Python3.12 under retained CPython3.12.14 cooperative contract','reference':'https://docs.python.org/3.12/reference/expressions.html','sections':['6.3.4 calls','6.16 evaluation order'],'rules':['Callable then positional arguments, left to right','Binary operands left to right; nested calls evaluate callable and arguments before attempted call and acknowledged normal return'],'limits':'Semantic regions; not observed opcode order, hidden library iteration, hostile-replacement resistance or alternate-interpreter qualification'},
  'continuity':'Explicit continuation and selected invocation/owner/token/error/destination/details/list and source-defined callable/builtin binding continuity; not runtime exclusivity',
  'excluded':['write_new body','open/write/flush/fsync','line175 suppression','line176 rethrow','owner finalization']}

def compile_write_call(launcher,entry,manager,loop,report,cleanup):
 s=write_call_source(launcher,entry,manager,loop,report,cleanup)
 return {'format':'I164-WRITE-CALL-REPLACEMENT-STATIC-1','source':s,'parent_catalogue_sha256':digest((json.dumps(loop,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()),'declarations':[{'id':x['id'],'source':copy.deepcopy(x['source']),'operation':x['operation'],'inputs':copy.deepcopy(x['inputs']),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for x in s['steps']],
  'guard_branches':{'parent':'Validated completed selected loop; original constructor pending; no replacement','continuity':['explicit conditional premise','UNESTABLISHED'],'prefixes':['control absent','control construction and callback completed normally'],'origins':['protected-close','protected-append'],'frontiers':['raise','catchable-interruption','process-termination','unobserved'],'values':'PID, directory count/contents and filename unobserved; no finite bound introduced'},'preserved_relations':['cleanup_loop_exhaustion_correspondence',*loop['preserved_relations']],'runtime_chain':None,'actual_admission':False}

def validate_write_call(launcher,entry,manager,loop,report,cleanup,submitted):
 status_exact_tree(submitted,'WC-CATALOGUE-TYPE');status_typed_same(submitted,compile_write_call(launcher,entry,manager,loop,report,cleanup),'WC-SOURCE-CORRESPONDENCE');return True

def write_call_binding(cat,parent,anchor,session,continuity):
 for v in (cat,parent,anchor,session,continuity):status_exact_tree(v,'WC-BINDING-TYPE')
 need(type(continuity) is str and continuity in ('explicit conditional premise','UNESTABLISHED'),'WC-CONTINUITY')
 need(parent['kind']=='CONSTRUCTED-CLEANUP-LOOP' and parent['completion']=='normal-cleanup-loop-exhaustion','WC-PARENT-COMPLETION')
 need(all(parent[k] is True for k in ('handler_exit_established','selected_body_complete','ordinary_exhaustion_established','loop_completion_established','terminal_python_exception_in_model')),'WC-PARENT-FLAGS')
 need(parent['replacement_error_in_model'] is None and parent['line174_evaluation_established'] is False,'WC-PARENT-ERROR-FRONTIER')
 error=parent['original_error_pending_in_outer_handler'];scope=parent['scope'];b=parent['binding'];event=parent['events'][-1]
 status_typed_same(parent['last_pending_error_in_model'],error,'WC-PENDING-ORIGINAL');status_typed_same(parent['last_acknowledged_active_caught_error_in_model'],error,'WC-ACTIVE-ORIGINAL');status_typed_same(parent['instance_anchor'],anchor,'WC-INSTANCE')
 status_typed_same(scope['instance'],anchor['instance'],'WC-SCOPE-INSTANCE');status_typed_same(session['instance'],anchor['instance'],'WC-DESTINATION-INSTANCE');need(session['acquisition']==scope['acquisition']==anchor['record']['acquisition'],'WC-ACQUISITION')
 status_typed_same(session['source_owner_lock'],cat['source']['owner_lock'],'WC-DESTINATION-SOURCE');need(type(session['recorded_destination']) is str and session['physical_resolved_destination'] is None,'WC-DESTINATION-ROLE')
 need(event['stage']=='cleanup-loop-complete' and event['outcome']=='normal' and event['id']==scope['invocation']+'/cleanup-loop/cleanup-loop-complete','WC-PARENT-OCCURRENCE')
 for k,v in (('scope',scope),('owner',b['references']['owner']),('token',b['references']['token'])):status_typed_same(event[k],v,'WC-PARENT-'+k)
 need(b['continuity']=='explicit conditional premise' and b['loop']['selected_is_last'] is True,'WC-PARENT-CONTINUITY')
 for k in ('details_role','cleanup_list'):status_typed_same(b[k]['scope'],scope,'WC-DETAILS-SCOPE')
 status_typed_same(parent['cleanup_list_state']['acknowledged_append']['target'],b['cleanup_list'],'WC-CLEANUP-TARGET')
 return {'scope':copy.deepcopy(scope),'anchor':copy.deepcopy(anchor),'loop_occurrence':copy.deepcopy(event),'references':copy.deepcopy(b['references']),'original_constructor_error':copy.deepcopy(error),'details_role':copy.deepcopy(b['details_role']),'cleanup_list':copy.deepcopy(b['cleanup_list']),
  'destination':{'role':'owner-lock-yielded-dest','symbol':scope['invocation']+'/launcher/dest','scope':copy.deepcopy(scope),'session_binding':copy.deepcopy(session),'bridge':copy.deepcopy(cat['source']['destination_bridge']),'yield':copy.deepcopy(cat['source']['destination_yield']),'physical_resolved_value':None},
  'callable':{'name':'write_new','scope':copy.deepcopy(scope),'source':copy.deepcopy(cat['source']['callee']),'runtime_identity':None},'call_source':copy.deepcopy(cat['source']['call']),'continuity':continuity,'premise':cat['source']['continuity'],'observed_identity':None}

def write_call_projection(cat,case,validated):
 for v in (cat,case,validated):status_exact_tree(v,'WC-EXACT-TYPE')
 keys={'scope','anchor','parent_result','session_binding','binding','outcomes'};need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'WC-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'WC-VALIDATED:'+k)
 p=case['parent_result'];scope=case['scope'];b=case['binding'];s=cat['source'];oo=case['outcomes']
 status_typed_same(scope,p['scope'],'WC-PARENT-SCOPE');status_typed_same(b,write_call_binding(cat,p,case['anchor'],case['session_binding'],b['continuity']),'WC-EXPECTED-BINDING')
 need(type(oo) is list and bool(oo),'WC-OUTCOMES')
 if b['continuity']=='UNESTABLISHED':status_typed_same(oo,[{'stage':s['order'][0],'outcome':'unobserved'}],'WC-UNKNOWN-CONTINUITY')
 events=[];values={};replacement=None;last=None;complete=False
 for i,step in enumerate(s['steps']):
  need(i<len(oo),'WC-MISSING-STEP');r=oo[i];need(type(r) is dict and set(r)=={'stage','outcome'} and type(r['stage']) is str and r['stage']==step['id'],'WC-ORDER')
  last=r['outcome'];need(type(last) is str and last in (step['normal_outcome'],'raise','catchable-interruption','process-termination','unobserved'),'WC-OUTCOME')
  ev={'id':scope['invocation']+'/line174/'+step['id'],'scope':copy.deepcopy(scope),'stage':step['id'],'source':copy.deepcopy(step['source']),'outcome':last,'owner':copy.deepcopy(b['references']['owner']),'token':copy.deepcopy(b['references']['token']),'runtime_frame':None};events.append(ev)
  if last!=step['normal_outcome']:
   if last in ('raise','catchable-interruption'):replacement={'role':'conditional-line174-replacement','reference':ev['id']+'/error','scope':copy.deepcopy(scope),'origin':copy.deepcopy(step['source']),'kind':last,'exact_type':None,'exact_value':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_observation':False}
   break
  if step['operation'] not in ('explicit continuation into selected protecting try','nested call attempt','write_new call attempt; body excluded'):
   role=copy.deepcopy(b['destination']) if step.get('name')=='dest' else copy.deepcopy(b['details_role']) if step.get('name')=='details' else copy.deepcopy(b['callable']) if step.get('name')=='write_new' else None
   values[step['id']]={'symbol':ev['id']+'/value','inputs':[{'occurrence':scope['invocation']+'/line174/'+x,'value':values[x]['symbol'] if x in values else None,'kind':'prior result' if x in values else 'prior call attempt'} for x in step['inputs']],'source':copy.deepcopy(step['source']),'literal':step.get('literal'),'value_kind':'source literal str' if 'literal' in step else 'symbolic unobserved result','bound_role':role,'concrete_value':step.get('literal') if 'literal' in step else None,'runtime_identity':None}
  if step['id']=='write:call-attempt':complete=True
 need(len(oo)==len(events),'WC-UNREACHED-STEPS')
 uncertain=last in ('process-termination','unobserved')
 out={'kind':'CONSTRUCTED-WRITE-CALL-REPLACEMENT','scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(case['anchor']),'binding':copy.deepcopy(b),'events':events,'values':values,'completion':'write_new-call-attempt' if complete else last+'-frontier','call_attempt_established':complete,
  'call_arguments':{'p':copy.deepcopy(values.get(s['arguments'][0])),'x':copy.deepcopy(b['details_role'])} if complete else None,
  'original_error_pending_in_outer_handler':copy.deepcopy(p['original_error_pending_in_outer_handler']),'last_pending_error_in_model':copy.deepcopy(replacement or p['last_pending_error_in_model']),'replacement_error_in_model':replacement,'terminal_python_exception_in_model':None if uncertain else True,
  'pid_value':None,'directory_count_value':None,'filename_value':None,'exact_path_value':None,'current_partial_effects':'UNKNOWN at nonnormal frontier; acknowledged semantic values only' if not complete else 'Evaluation acknowledged conditionally; no callee-body effects established',
  'existing_cause_context_suppression':'UNKNOWN; no new exception-chain facts','runtime_chain':None,'runtime_observation':False,'observer_join':None,'physical_reference_identity':None}
 for k in ('retained_cleanup_error_evidence','last_acknowledged_inner_caught_error','last_acknowledged_active_caught_error_in_model','earlier_control_completed_in_model','selected_owner_continuity','failure_origin_region','close_normal_return_completed_in_model','close_itself_failed_established_in_model','managed_close_relation','cleanup_list_state','details_after_predecessor_acknowledged_steps','known_false_flags_preserved','dynamic_details_origins_preserved'):out[k]=copy.deepcopy(p[k])
 for k in ('write_new_body_entry_established','write_new_return_established','file_open_established','file_write_established','file_flush_established','file_fsync_established','failure_file_established','line175_handler_entry_established','line175_suppression_established','final_rethrow_established','owner_finalization_established','managed_local_clear_established','active_removal_established','complete_cleanup_established','normal_overall_return_established','physical_closure_established','durability_established','released_ownership_established','obligations_discharged','external_nonexecution_established','authorization_renewed','actual_admission'):out[k]=False
 return out

def validate_write_call_projection(cat,case,validated,submitted):
 status_exact_tree(submitted,'WC-OUTPUT-TYPE');status_typed_same(submitted,write_call_projection(cat,case,validated),'WC-OUTPUT-CORRESPONDENCE');return True

# Bounded helper-entry/open-attempt extension. Historical functions unchanged.
def helper_open_source(launcher,entry,manager,write,loop,report,cleanup):
 validate_write_call(launcher,entry,manager,loop,report,cleanup,write)
 tree=ast.parse(launcher);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='write_new')
 need(fn.lineno==23 and len(fn.body)==1 and isinstance(fn.body[0],ast.With),'OPEN-HELPER-SOURCE')
 need(not fn.decorator_list and not fn.args.posonlyargs and not fn.args.kwonlyargs and not fn.args.defaults and not fn.args.kw_defaults and fn.args.vararg is None and fn.args.kwarg is None and [a.arg for a in fn.args.args]==['p','x'],'OPEN-PARAMETER-SHAPE')
 w=fn.body[0];need(w.lineno==24 and len(w.items)==1,'OPEN-WITH-SOURCE');item=w.items[0];call=item.context_expr
 need(ast.dump(call,include_attributes=False)==ast.dump(ast.parse("open(p,'xb')",mode='eval').body,include_attributes=False) and isinstance(item.optional_vars,ast.Name) and item.optional_vars.id=='f','OPEN-CALL-SOURCE')
 need(len(w.body)==3 and ast.unparse(w.body[0])=='f.write(enc(x))' and ast.unparse(w.body[1])=='f.flush()' and ast.unparse(w.body[2])=='os.fsync(f.fileno())','OPEN-STOP-SOURCE')
 pin=copy.deepcopy(write['source']['sources']['launcher'])
 def loc(n):return {'source':copy.deepcopy(pin),'site':[n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__],'expression':ast.get_source_segment(launcher.decode(),n)}
 status_typed_same(write['source']['callee'],loc(fn),'OPEN-PREDECESSOR-CALLEE');status_typed_same(write['source']['stop_before'],loc(w),'OPEN-PREDECESSOR-FRONTIER')
 need(write['source']['callee_parameters']==[a.arg for a in fn.args.args] and write['source']['order'][-1]=='write:call-attempt','OPEN-PREDECESSOR-ARGS')
 # Parameter correspondence is one structural mapping, not two invented Python assignments.
 steps=[{'id':'open:continuation','operation':'explicit continuation after validated call attempt','source':copy.deepcopy(write['source']['call']),'inputs':[],'normal_outcome':'normal'},
  {'id':'open:helper-entry','operation':'conditional selected-helper entry acknowledgment','source':loc(fn),'inputs':['open:continuation'],'normal_outcome':'normal'},
  {'id':'open:parameters','operation':'source positional parameter correspondence','source':loc(fn),'inputs':['open:helper-entry'],'normal_outcome':'normal','parameters':[{'name':a.arg,'position':i,'source':loc(a)} for i,a in enumerate(fn.args.args)]}]
 for suffix,node,op,extra in [('callable',call.func,'name lookup',{'name':call.func.id}),('path',call.args[0],'parameter lookup',{'name':call.args[0].id}),('mode',call.args[1],'literal',{'literal':call.args[1].value})]:
  steps.append({'id':'open:'+suffix,'operation':op,'source':loc(node),'inputs':['open:parameters'] if suffix=='path' else [],'normal_outcome':'normal',**extra})
 steps.append({'id':'open:attempt','operation':'open call attempt; return excluded','source':loc(call),'inputs':['open:callable','open:path','open:mode'],'normal_outcome':'attempted'})
 return {'sources':copy.deepcopy(write['source']['sources']),'parent_call':copy.deepcopy(write['source']['call']),'helper':loc(fn),'with_statement':loc(w),'open_call':loc(call),'f_target_excluded':loc(item.optional_vars),'body_excluded':loc(w.body[0]),'parameters':copy.deepcopy(steps[2]['parameters']),
  'steps':steps,'order':[s['id'] for s in steps],'normal_outcomes':{s['id']:s['normal_outcome'] for s in steps},
  'language_contract':copy.deepcopy(write['source']['language_contract']),
  'parameter_contract':'Two positional arguments map p then x by signature position. One structural correspondence after conditional entry acknowledgment, not an observed binding opcode sequence, separate assignments, copy, allocation or stronger physical identity claim. Parameters precede body expression evaluation.',
  'continuity':'Explicit continuation, selected invocation/owner/token/original-error and source-defined write_new/open callable plus argument/reference continuity. Conditional premise, not observed arrival or exclusivity.',
  'frontiers':'raise/catchable-interruption are conditional replacement frontiers, not demonstrated failure mechanisms. Termination/unobserved do not establish Python exception/unwind/completion. Stop at first nonnormal frontier.',
  'stop':'open call attempt; before open return, context protocol, as-f binding and helper body statements',
  'excluded':['open return','file creation','context-manager entry','f binding','encoding','writing','flushing','fsync','context exit','helper return','line175 suppression','final rethrow','owner finalization','physical cleanup']}

def compile_helper_open(launcher,entry,manager,write,loop,report,cleanup):
 s=helper_open_source(launcher,entry,manager,write,loop,report,cleanup)
 return {'format':'I164-HELPER-OPEN-ATTEMPT-STATIC-1','source':s,'parent_catalogue_sha256':digest((json.dumps(write,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()),
  'declarations':[{'id':x['id'],'source':copy.deepcopy(x['source']),'operation':x['operation'],'inputs':copy.deepcopy(x['inputs']),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for x in s['steps']],
  'guard_branches':{'parent':'Validated write_new call attempt, original constructor pending, no replacement','continuity':['explicit conditional premise','UNESTABLISHED'],'prefixes':['control absent','control construction and callback completed normally'],'origins':['protected-close','protected-append'],'frontiers':['raise','catchable-interruption','process-termination','unobserved'],'values':'Path, PID, directory count, filename and physical identities unobserved; no domain bound added'},
  'preserved_relations':['write_call_correspondence',*write['preserved_relations']],'runtime_chain':None,'actual_admission':False}

def validate_helper_open(launcher,entry,manager,write,loop,report,cleanup,submitted):
 status_exact_tree(submitted,'OPEN-CATALOGUE-TYPE');status_typed_same(submitted,compile_helper_open(launcher,entry,manager,write,loop,report,cleanup),'OPEN-SOURCE-CORRESPONDENCE');return True

def helper_open_binding(cat,parent,anchor,continuity):
 for v in (cat,parent,anchor,continuity):status_exact_tree(v,'OPEN-BINDING-TYPE')
 need(type(continuity) is str and continuity in ('explicit conditional premise','UNESTABLISHED'),'OPEN-CONTINUITY')
 need(parent['kind']=='CONSTRUCTED-WRITE-CALL-REPLACEMENT' and parent['completion']=='write_new-call-attempt' and parent['call_attempt_established'] is True,'OPEN-PARENT-COMPLETION')
 need(parent['replacement_error_in_model'] is None and parent['terminal_python_exception_in_model'] is True and parent['write_new_body_entry_established'] is False,'OPEN-PARENT-ERROR-FRONTIER')
 error=parent['original_error_pending_in_outer_handler'];status_typed_same(parent['last_pending_error_in_model'],error,'OPEN-PENDING-ORIGINAL')
 scope=parent['scope'];b=parent['binding'];event=parent['events'][-1];status_typed_same(parent['instance_anchor'],anchor,'OPEN-INSTANCE');status_typed_same(scope['instance'],anchor['instance'],'OPEN-SCOPE-INSTANCE')
 need(scope['acquisition']==anchor['record']['acquisition'],'OPEN-ACQUISITION');need(b['continuity']=='explicit conditional premise','OPEN-PARENT-CONTINUITY')
 need(event['stage']=='write:call-attempt' and event['outcome']=='attempted' and event['id']==scope['invocation']+'/line174/write:call-attempt','OPEN-PARENT-OCCURRENCE')
 for k,v in (('scope',scope),('owner',b['references']['owner']),('token',b['references']['token'])):status_typed_same(event[k],v,'OPEN-PARENT-'+k)
 status_typed_same(event['source'],cat['source']['parent_call'],'OPEN-PARENT-SOURCE');status_typed_same(b['callable']['source'],cat['source']['helper'],'OPEN-CALLEE-SOURCE')
 args=parent['call_arguments'];need(type(args) is dict and set(args)=={'p','x'} and type(args['p']) is dict,'OPEN-ARGUMENTS')
 status_typed_same(args['x'],b['details_role'],'OPEN-DETAILS-ARGUMENT');status_typed_same(b['cleanup_list']['scope'],scope,'OPEN-LIST-SCOPE')
 need(args['p']['concrete_value'] is None and args['p']['runtime_identity'] is None and parent['exact_path_value'] is None,'OPEN-SYMBOLIC-PATH')
 helper={'symbol':event['id']+'/callee/write_new','parent_occurrence':event['id'],'scope':copy.deepcopy(scope),'source':copy.deepcopy(cat['source']['helper']),'runtime_frame':None}
 parameters={x['name']:{'name':x['name'],'position':x['position'],'source':copy.deepcopy(x['source']),'helper_invocation':copy.deepcopy(helper),'argument':copy.deepcopy(args[x['name']]),'semantics':'source-established reference passing; not a copy or observed physical identity','runtime_object':None} for x in cat['source']['parameters']}
 return {'scope':copy.deepcopy(scope),'anchor':copy.deepcopy(anchor),'parent_occurrence':copy.deepcopy(event),'helper_invocation':helper,'references':copy.deepcopy(b['references']),'original_constructor_error':copy.deepcopy(error),'parameters':parameters,'details_role':copy.deepcopy(b['details_role']),'cleanup_list':copy.deepcopy(b['cleanup_list']),
  'open_callable':{'name':'open','scope':copy.deepcopy(scope),'source':copy.deepcopy(cat['source']['steps'][3]['source']),'runtime_identity':None,'resolution':'source-defined callable under explicit continuity; no observed replacement resistance'},
  'continuity':continuity,'premise':cat['source']['continuity'],'observed_identity':None}

def helper_open_projection(cat,case,validated):
 for v in (cat,case,validated):status_exact_tree(v,'OPEN-EXACT-TYPE')
 keys={'scope','anchor','parent_result','binding','outcomes'};need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'OPEN-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'OPEN-VALIDATED:'+k)
 p=case['parent_result'];scope=case['scope'];b=case['binding'];s=cat['source'];oo=case['outcomes']
 status_typed_same(scope,p['scope'],'OPEN-PARENT-SCOPE');status_typed_same(b,helper_open_binding(cat,p,case['anchor'],b['continuity']),'OPEN-EXPECTED-BINDING')
 need(type(oo) is list and bool(oo),'OPEN-OUTCOMES')
 if b['continuity']=='UNESTABLISHED':status_typed_same(oo,[{'stage':s['order'][0],'outcome':'unobserved'}],'OPEN-UNKNOWN-CONTINUITY')
 events=[];values={};replacement=None;last=None;complete=False;entry=False;bound=False;parameters=None
 for i,step in enumerate(s['steps']):
  need(i<len(oo),'OPEN-MISSING-STEP');r=oo[i];need(type(r) is dict and set(r)=={'stage','outcome'} and type(r['stage']) is str and r['stage']==step['id'],'OPEN-ORDER')
  last=r['outcome'];need(type(last) is str and last in (step['normal_outcome'],'raise','catchable-interruption','process-termination','unobserved'),'OPEN-OUTCOME')
  ev={'id':b['helper_invocation']['symbol']+'/'+step['id'],'scope':copy.deepcopy(scope),'helper_invocation':copy.deepcopy(b['helper_invocation']),'stage':step['id'],'source':copy.deepcopy(step['source']),'outcome':last,'owner':copy.deepcopy(b['references']['owner']),'token':copy.deepcopy(b['references']['token']),'runtime_frame':None};events.append(ev)
  if last!=step['normal_outcome']:
   if last in ('raise','catchable-interruption'):replacement={'role':'conditional-helper-open-replacement','reference':ev['id']+'/error','scope':copy.deepcopy(scope),'origin':copy.deepcopy(step['source']),'kind':last,'exact_type':None,'exact_value':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_observation':False}
   break
  if step['id']=='open:helper-entry':entry=True
  elif step['id']=='open:parameters':bound=True;parameters=copy.deepcopy(b['parameters'])
  elif step['id'] in ('open:callable','open:path','open:mode'):
   need(entry and bound,'OPEN-EVALUATION-GUARD')
   role=b['open_callable'] if step['id']=='open:callable' else parameters['p'] if step['id']=='open:path' else None
   values[step['id']]={'symbol':ev['id']+'/value','source':copy.deepcopy(step['source']),'bound_role':copy.deepcopy(role),'literal':step.get('literal'),'concrete_value':step.get('literal'),'runtime_identity':None}
  elif step['id']=='open:attempt':complete=True
 need(len(oo)==len(events),'OPEN-UNREACHED-STEPS')
 out={'kind':'CONSTRUCTED-HELPER-OPEN-ATTEMPT','scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(case['anchor']),'binding':copy.deepcopy(b),'events':events,'values':values,'completion':'open-call-attempt' if complete else last+'-frontier','helper_entry_established_in_model':entry,'parameter_binding_established_in_model':bound,'bound_parameters':parameters,'open_call_attempt_established_in_model':complete,
  'open_arguments':{'p':copy.deepcopy(values['open:path']),'mode':copy.deepcopy(values['open:mode'])} if complete else None,'source_reference_semantics':'Parameter passing forwards references; representation copying is not an observed runtime copy or physical identity',
  'original_error_pending_in_outer_handler':copy.deepcopy(p['original_error_pending_in_outer_handler']),'last_pending_error_in_model':copy.deepcopy(replacement or p['last_pending_error_in_model']),'replacement_error_in_model':replacement,'terminal_python_exception_in_model':None if last in ('process-termination','unobserved') else True,
  'pid_value':None,'directory_count_value':None,'filename_value':None,'exact_path_value':None,'physical_reference_identity':None,'runtime_chain':None,'runtime_observation':False,'observer_join':None,'existing_cause_context_suppression':'UNKNOWN; no new exception-chain facts','current_partial_effects':'UNKNOWN at nonnormal frontier; acknowledged semantic values only' if not complete else 'Conditional open call attempt acknowledged; no open return or effects established'}
 for k in ('retained_cleanup_error_evidence','last_acknowledged_inner_caught_error','last_acknowledged_active_caught_error_in_model','earlier_control_completed_in_model','selected_owner_continuity','failure_origin_region','close_normal_return_completed_in_model','close_itself_failed_established_in_model','managed_close_relation','cleanup_list_state','details_after_predecessor_acknowledged_steps','known_false_flags_preserved','dynamic_details_origins_preserved'):out[k]=copy.deepcopy(p[k])
 for k in ('open_return_established','file_creation_established','context_manager_entry_established','f_binding_established','encoding_established','file_write_established','file_flush_established','file_fsync_established','context_manager_exit_established','helper_return_established','failure_file_established','line175_handler_entry_established','line175_suppression_established','final_rethrow_established','owner_finalization_established','managed_local_clear_established','active_removal_established','complete_cleanup_established','normal_overall_return_established','physical_closure_established','durability_established','released_ownership_established','obligations_discharged','external_nonexecution_established','authorization_renewed','actual_admission'):out[k]=False
 return out

def validate_helper_open_projection(cat,case,validated,submitted):
 status_exact_tree(submitted,'OPEN-OUTPUT-TYPE');status_typed_same(submitted,helper_open_projection(cat,case,validated),'OPEN-OUTPUT-CORRESPONDENCE');return True

# NEW reconstruction R1. The reviewed 405785-byte producer prefix is unchanged.
# These are conditional model operations, not execution of write_new or open.
def compile_open_return(launcher, parent):
 status_exact_tree(parent,'OR-CATALOGUE-INPUT')
 need(type(launcher) is bytes,'OR-SOURCE-TYPE')
 pin={'bytes':11481,'sha256':'245d4f36d687834aeee064a60d4414b15f7b8babfdb5dec192aa995d93af2b78'}
 need({'bytes':len(launcher),'sha256':digest(launcher)}==pin,'OR-SOURCE-IDENTITY')
 tree=ast.parse(launcher);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='write_new')
 need(fn.lineno==23 and len(fn.body)==1 and isinstance(fn.body[0],ast.With),'OR-HELPER')
 w=fn.body[0];need(w.lineno==24 and len(w.items)==1,'OR-WITH');item=w.items[0];call=item.context_expr
 need(ast.dump(call,include_attributes=False)==ast.dump(ast.parse("open(p,'xb')",mode='eval').body,include_attributes=False),'OR-EXPRESSION')
 need(isinstance(item.optional_vars,ast.Name) and item.optional_vars.id=='f','OR-EXCLUDED-TARGET')
 def loc(n):return {'source':copy.deepcopy(pin),'site':[n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__],'expression':ast.get_source_segment(launcher.decode(),n)}
 need(parent['format']=='I164-HELPER-OPEN-ATTEMPT-STATIC-1','OR-PARENT-FORMAT')
 for key,node in [('open_call',call),('with_statement',w),('f_target_excluded',item.optional_vars)]:status_typed_same(parent['source'][key],loc(node),'OR-PARENT-SOURCE:'+key)
 need(parent['source']['order'][-1]=='open:attempt' and parent['source']['normal_outcomes']['open:attempt']=='attempted','OR-PARENT-FRONTIER')
 steps=[{'id':'open-return:continuation','operation':'explicit conditional continuation after the selected open attempt','source':loc(call),'normal_outcome':'normal'},
  {'id':'open-return:outcome','operation':'selected open outcome; only normal return supplies the with-item context operand','source':loc(call),'normal_outcome':'normal-return'}]
 source={'open_call':loc(call),'with_statement':loc(w),'operand_ast_field':'With.items[0].context_expr','excluded_target':loc(item.optional_vars),'steps':steps,'order':[s['id'] for s in steps],'language_contract':copy.deepcopy(parent['source']['language_contract'])}
 return {'format':'I164-OPEN-RETURN-RECONSTRUCTION-STATIC-1','source':source,'parent_catalogue_sha256':digest((json.dumps(parent,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()),
  'declarations':[{'id':s['id'],'source':copy.deepcopy(s['source']),'operation':s['operation'],'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for s in steps],
  'guard_branches':{'continuity':['explicit conditional premise','UNESTABLISHED'],'outcomes':['normal-return','raise','catchable-interruption','process-termination','unobserved'],'prefixes':copy.deepcopy(parent['guard_branches']['prefixes']),'origins':copy.deepcopy(parent['guard_branches']['origins'])},
  'preserved_relations':['helper_open_attempt_correspondence',*parent['preserved_relations']],
  'stop':'with-item context operand only; before context-manager protocol lookup, entry or f binding','runtime_chain':None,'actual_admission':False}

def validate_open_return(launcher,parent,submitted):
 status_exact_tree(submitted,'OR-CATALOGUE-TYPE');status_typed_same(submitted,compile_open_return(launcher,parent),'OR-CATALOGUE-SOURCE');return True

def open_return_binding(cat,parent,anchor,continuity):
 for v in (cat,parent,anchor,continuity):status_exact_tree(v,'OR-BINDING-TYPE')
 need(type(continuity) is str and continuity in ('explicit conditional premise','UNESTABLISHED'),'OR-CONTINUITY')
 need(parent['kind']=='CONSTRUCTED-HELPER-OPEN-ATTEMPT' and parent['completion']=='open-call-attempt' and parent['open_call_attempt_established_in_model'] is True,'OR-PARENT-COMPLETION')
 need(parent['helper_entry_established_in_model'] is True and parent['parameter_binding_established_in_model'] is True and parent['open_return_established'] is False,'OR-PARENT-FRONTIER')
 need(parent['replacement_error_in_model'] is None and parent['terminal_python_exception_in_model'] is True,'OR-PARENT-ERROR')
 original=parent['original_error_pending_in_outer_handler'];status_typed_same(parent['last_pending_error_in_model'],original,'OR-PENDING-ORIGINAL')
 scope=parent['scope'];b=parent['binding'];event=parent['events'][-1];helper=b['helper_invocation']
 status_typed_same(parent['instance_anchor'],anchor,'OR-ANCHOR');status_typed_same(scope['instance'],anchor['instance'],'OR-INSTANCE')
 need(scope['context']==anchor['context'] and scope['acquisition']==anchor['record']['acquisition'],'OR-CONTEXT-ACQUISITION')
 status_typed_same(helper['scope'],scope,'OR-HELPER-SCOPE');need(b['continuity']=='explicit conditional premise','OR-PARENT-CONTINUITY')
 need(event['id']==helper['symbol']+'/open:attempt' and event['stage']=='open:attempt' and event['outcome']=='attempted','OR-SELECTED-ATTEMPT')
 for key,value in [('scope',scope),('helper_invocation',helper),('owner',b['references']['owner']),('token',b['references']['token']),('source',cat['source']['open_call'])]:status_typed_same(event[key],value,'OR-ATTEMPT-'+key)
 args=parent['open_arguments'];need(type(args) is dict and set(args)=={'p','mode'},'OR-ARGUMENTS')
 need(type(args['mode']['concrete_value']) is str and args['mode']['concrete_value']=='xb','OR-MODE')
 status_typed_same(args['p']['bound_role'],parent['bound_parameters']['p'],'OR-PARAMETER')
 status_typed_same(parent['bound_parameters']['x']['argument'],b['details_role'],'OR-DETAILS')
 for k in ('details_role','cleanup_list'):status_typed_same(b[k]['scope'],scope,'OR-ROLE-SCOPE')
 need(parent['exact_path_value'] is None and parent['physical_reference_identity'] is None,'OR-UNOBSERVED-PATH-IDENTITY')
 return {'scope':copy.deepcopy(scope),'anchor':copy.deepcopy(anchor),'attempt':copy.deepcopy(event),'helper_invocation':copy.deepcopy(helper),'references':copy.deepcopy(b['references']),'arguments':copy.deepcopy(args),'details_role':copy.deepcopy(b['details_role']),'cleanup_list':copy.deepcopy(b['cleanup_list']),'original_constructor_error':copy.deepcopy(original),'continuity':continuity,'observed_identity':None}

def open_return_projection(cat,case,validated):
 for v in (cat,case,validated):status_exact_tree(v,'OR-EXACT-TYPE')
 keys={'scope','anchor','parent_result','binding','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'OR-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'OR-VALIDATED:'+k)
 p=case['parent_result'];scope=case['scope'];b=case['binding'];oo=case['outcomes']
 status_typed_same(scope,p['scope'],'OR-SCOPE');status_typed_same(b,open_return_binding(cat,p,case['anchor'],b['continuity']),'OR-EXPECTED-BINDING')
 need(type(oo) is list and bool(oo),'OR-OUTCOMES')
 if b['continuity']=='UNESTABLISHED':status_typed_same(oo,[{'stage':'open-return:continuation','outcome':'unobserved'}],'OR-UNKNOWN-CONTINUITY')
 events=[];replacement=None;last=None;normal=False
 for i,step in enumerate(cat['source']['steps']):
  need(i<len(oo),'OR-MISSING-STEP');r=oo[i]
  need(type(r) is dict and set(r)=={'stage','outcome'} and type(r['stage']) is str and r['stage']==step['id'],'OR-ORDER')
  last=r['outcome'];need(type(last) is str and last in (step['normal_outcome'],'raise','catchable-interruption','process-termination','unobserved'),'OR-OUTCOME')
  event={'id':b['attempt']['id']+'/'+step['id'],'scope':copy.deepcopy(scope),'helper_invocation':copy.deepcopy(b['helper_invocation']),'stage':step['id'],'source':copy.deepcopy(step['source']),'outcome':last,'owner':copy.deepcopy(b['references']['owner']),'token':copy.deepcopy(b['references']['token']),'runtime_frame':None};events.append(event)
  if last!=step['normal_outcome']:
   if last in ('raise','catchable-interruption'):replacement={'role':'conditional-open-outcome-replacement','reference':event['id']+'/error','scope':copy.deepcopy(scope),'origin':copy.deepcopy(step['source']),'frontier_stage':step['id'],'kind':last,'exact_type':None,'exact_value':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_observation':False}
   break
  if step['id']=='open-return:outcome':normal=True
 need(len(oo)==len(events),'OR-UNREACHED-STEPS')
 out=copy.deepcopy(p)
 out.update({'kind':'CONSTRUCTED-OPEN-RETURN-RECONSTRUCTION','binding':copy.deepcopy(b),'predecessor_events':copy.deepcopy(p['events']),'events':events,'completion':'with-context-operand' if normal else last+'-frontier','open_return_established':normal,'open_return_established_in_model':normal,'context_operand_established_in_model':normal,'context_protocol_lookup_established':False,'returned_object_role':None,'context_operand':None,
  'replacement_error_in_model':replacement,'last_pending_error_in_model':copy.deepcopy(replacement if replacement is not None else p['last_pending_error_in_model']),'terminal_python_exception_in_model':None if last in ('process-termination','unobserved') else True,
  'earlier_acknowledged_partial_effects':copy.deepcopy(p['current_partial_effects']),'current_partial_effects':'UNKNOWN; normal symbolic return establishes no physical file effects' if normal else 'UNKNOWN at first nonnormal frontier; no absence of partial effects established','stop':cat['stop']})
 if normal:
  role={'symbol':events[-1]['id']+'/returned-object','scope':copy.deepcopy(scope),'attempt':b['attempt']['id'],'source':copy.deepcopy(cat['source']['open_call']),'helper_invocation':copy.deepcopy(b['helper_invocation']),'runtime_identity':None,'concrete_value':None,'concrete_type':None}
  out['returned_object_role']=copy.deepcopy(role)
  out['context_operand']={'role':copy.deepcopy(role),'source':copy.deepcopy(cat['source']['with_statement']),'ast_field':'With.items[0].context_expr','reference_relation':'same symbolic expression result; no observed physical identity','physical_identity_established':False}
 return out

def validate_open_return_projection(cat,case,validated,submitted):
 status_exact_tree(submitted,'OR-OUTPUT-TYPE');status_typed_same(submitted,open_return_projection(cat,case,validated),'OR-OUTPUT-CORRESPONDENCE');return True

# Context special-method lookup slice. Exact reviewed R1 prefix remains unchanged.
def context_lookup_source(launcher,bytecodes,typeobject,parent):
 import re
 for raw in (launcher,bytecodes,typeobject):need(type(raw) is bytes,'LOOKUP-SOURCE-TYPE')
 status_exact_tree(parent,'LOOKUP-PARENT-CATALOGUE-TYPE')
 pins={'launcher':{'bytes':11481,'sha256':'245d4f36d687834aeee064a60d4414b15f7b8babfdb5dec192aa995d93af2b78'},'bytecodes':{'bytes':143622,'sha256':'f8c050621f1498d953d4898aaf29457e154620fec7f8bb987b4d3fde6f5a1d84'},'typeobject':{'bytes':328862,'sha256':'77e687a382ef5fbced0be9c99fb722e2531131f4cdd1216994a8a52696c21501'}}
 for name,raw in [('launcher',launcher),('bytecodes',bytecodes),('typeobject',typeobject)]:need({'bytes':len(raw),'sha256':digest(raw)}==pins[name],'LOOKUP-SOURCE-PIN:'+name)
 tree=ast.parse(launcher);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='write_new');w=fn.body[0];call=w.items[0].context_expr
 need(fn.lineno==23 and isinstance(w,ast.With) and w.lineno==24 and len(w.items)==1,'LOOKUP-WITH-SOURCE')
 need(ast.dump(call,include_attributes=False)==ast.dump(ast.parse("open(p,'xb')",mode='eval').body,include_attributes=False),'LOOKUP-OPERAND-EXPRESSION')
 def loc(n):return {'source':copy.deepcopy(pins['launcher']),'site':[n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__],'expression':ast.get_source_segment(launcher.decode(),n)}
 need(parent['format']=='I164-OPEN-RETURN-RECONSTRUCTION-STATIC-1','LOOKUP-PARENT-FORMAT')
 status_typed_same(parent['source']['open_call'],loc(call),'LOOKUP-PARENT-CALL');status_typed_same(parent['source']['with_statement'],loc(w),'LOOKUP-PARENT-WITH')
 need(parent['source']['order']==['open-return:continuation','open-return:outcome'] and parent['source']['operand_ast_field']=='With.items[0].context_expr','LOOKUP-PARENT-FRONTIER')
 bc=bytecodes.decode();start=bc.index('        inst(BEFORE_WITH,');end=bc.index('        inst(WITH_EXCEPT_START,',start);block=bc[start:end]
 matches=list(re.finditer(r'_PyObject_LookupSpecial\(mgr, &_Py_ID\((__\w+__)\)\)\s*;',block))
 need(len(matches)==2 and [x.group(1) for x in matches]==['__enter__','__exit__'],'LOOKUP-INTERPRETER-ORDER')
 invoke=block.index('_PyObject_CallNoArgs(enter)');need(matches[1].end()<invoke,'LOOKUP-STOP-BEFORE-CALL')
 tt=typeobject.decode();ts=tt.index('_PyObject_LookupSpecial(PyObject *self, PyObject *attr)');te=tt.index('\nPyObject *',ts);special=tt[ts:te]
 need('res = _PyType_Lookup(Py_TYPE(self), attr);' in special and 'Py_TYPE(res)->tp_descr_get' in special and 'res = f(res, self, (PyObject *)(Py_TYPE(self)));' in special,'LOOKUP-TYPE-DESCRIPTOR-SEMANTICS')
 def csite(name,text,offset,fragment):return {'source':copy.deepcopy(pins[name]),'file':'Python/bytecodes.c' if name=='bytecodes' else 'Objects/typeobject.c','line':text.count('\n',0,offset)+1,'expression':fragment,'tag':'v3.12.14'}
 steps=[{'id':'lookup:continuation','method':None,'source':loc(w),'normal_outcome':'normal','allowed':['normal','raise','catchable-interruption','process-termination','unobserved']}]
 for i,m in enumerate(matches):
  region=block[m.end():matches[i+1].start() if i+1<len(matches) else invoke]
  need('== NULL' in region and 'if (!_PyErr_Occurred(tstate))' in region and 'PyExc_TypeError' in region and 'goto error;' in region,'LOOKUP-ERROR-GUARD')
  name=m.group(1);steps.append({'id':'lookup:'+name,'method':name,'source':csite('bytecodes',bc,start+m.start(),m.group()),'normal_outcome':'found','allowed':['found','missing-method','raise','catchable-interruption','process-termination','unobserved'],'null_error_guard':'NULL plus existing error -> raised lookup; NULL without existing error -> source TypeError diagnostic path','diagnostic_requested_type':'TypeError'})
 return {'pins':pins,'open_call':loc(call),'with_statement':loc(w),'steps':steps,'order':[s['id'] for s in steps],'method_order':[m.group(1) for m in matches],'special_lookup':csite('typeobject',tt,ts,special),'next_call_excluded':csite('bytecodes',bc,start+invoke,'_PyObject_CallNoArgs(enter)'),
  'contract':'CPython 3.12.14 BEFORE_WITH and _PyObject_LookupSpecial; conditional source semantics, no new executable-image equivalence claim',
  'resolution':'lookup on Py_TYPE(receiver), not ordinary instance attribute access; descriptor binding may execute; concrete type, descriptor effects and callability unobserved',
  'missing':'missing-method denotes NULL without a pre-existing lookup error and the source-selected protocol diagnostic disposition. It is not Python None or a proved concrete formatted exception; diagnostic construction/formatting effects remain unestablished.',
  'stop':'after selected __exit__ lookup result, before either protocol method invocation, context entry or f binding'}

def compile_context_lookup(launcher,bytecodes,typeobject,parent):
 s=context_lookup_source(launcher,bytecodes,typeobject,parent)
 return {'format':'I164-CONTEXT-SPECIAL-LOOKUP-STATIC-1','source':s,'parent_catalogue_sha256':digest(enc(parent)),
  'declarations':[{'id':x['id'],'source':copy.deepcopy(x['source']),'method':x['method'],'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for x in s['steps']],
  'guard_branches':{'continuity':['explicit conditional premise','UNESTABLISHED'],'prefixes':copy.deepcopy(parent['guard_branches']['prefixes']),'origins':copy.deepcopy(parent['guard_branches']['origins']),'steps':{x['id']:copy.deepcopy(x['allowed']) for x in s['steps']}},
  'preserved_relations':['open_return_context_operand_correspondence',*parent['preserved_relations']],'runtime_chain':None,'actual_admission':False}

def validate_context_lookup(launcher,bytecodes,typeobject,parent,submitted):
 status_exact_tree(submitted,'LOOKUP-CATALOGUE-TYPE');status_typed_same(submitted,compile_context_lookup(launcher,bytecodes,typeobject,parent),'LOOKUP-CATALOGUE-SOURCE');return True

def context_lookup_binding(cat,parent,anchor,continuity):
 for v in (cat,parent,anchor,continuity):status_exact_tree(v,'LOOKUP-BINDING-TYPE')
 need(type(continuity) is str and continuity in ('explicit conditional premise','UNESTABLISHED'),'LOOKUP-CONTINUITY')
 need(parent['kind']=='CONSTRUCTED-OPEN-RETURN-RECONSTRUCTION' and parent['completion']=='with-context-operand','LOOKUP-PARENT-COMPLETION')
 for k in ('open_return_established','open_return_established_in_model','context_operand_established_in_model'):need(parent[k] is True,'LOOKUP-PARENT-NORMAL:'+k)
 need(parent['context_protocol_lookup_established'] is False and parent['context_manager_entry_established'] is False and parent['f_binding_established'] is False,'LOOKUP-PARENT-STOP')
 need(parent['replacement_error_in_model'] is None and parent['terminal_python_exception_in_model'] is True,'LOOKUP-PARENT-PENDING')
 status_typed_same(parent['last_pending_error_in_model'],parent['original_error_pending_in_outer_handler'],'LOOKUP-ORIGINAL-PENDING')
 scope=parent['scope'];b=parent['binding'];event=parent['events'][-1];role=parent['returned_object_role'];operand=parent['context_operand']
 status_typed_same(parent['instance_anchor'],anchor,'LOOKUP-ANCHOR');status_typed_same(scope['instance'],anchor['instance'],'LOOKUP-INSTANCE')
 need(scope['context']==anchor['context'] and scope['acquisition']==anchor['record']['acquisition'],'LOOKUP-CONTEXT-ACQUISITION')
 need(b['continuity']=='explicit conditional premise','LOOKUP-PARENT-CONTINUITY')
 need(event['id']==b['attempt']['id']+'/open-return:outcome' and event['stage']=='open-return:outcome' and event['outcome']=='normal-return','LOOKUP-PARENT-OUTCOME')
 for k,v in [('scope',scope),('helper_invocation',b['helper_invocation']),('owner',b['references']['owner']),('token',b['references']['token']),('source',cat['source']['open_call'])]:status_typed_same(event[k],v,'LOOKUP-EVENT:'+k)
 expected={'symbol':event['id']+'/returned-object','scope':copy.deepcopy(scope),'attempt':b['attempt']['id'],'source':copy.deepcopy(cat['source']['open_call']),'helper_invocation':copy.deepcopy(b['helper_invocation']),'runtime_identity':None,'concrete_value':None,'concrete_type':None}
 status_typed_same(role,expected,'LOOKUP-RETURNED-ROLE');status_typed_same(operand,{'role':copy.deepcopy(expected),'source':copy.deepcopy(cat['source']['with_statement']),'ast_field':'With.items[0].context_expr','reference_relation':'same symbolic expression result; no observed physical identity','physical_identity_established':False},'LOOKUP-CONTEXT-OPERAND')
 return {'scope':copy.deepcopy(scope),'anchor':copy.deepcopy(anchor),'operand_occurrence':copy.deepcopy(event),'operand_role':copy.deepcopy(role),'helper_invocation':copy.deepcopy(b['helper_invocation']),'references':copy.deepcopy(b['references']),'original_constructor_error':copy.deepcopy(parent['original_error_pending_in_outer_handler']),'details_role':copy.deepcopy(b['details_role']),'cleanup_list':copy.deepcopy(b['cleanup_list']),'continuity':continuity,'physical_identity':None}

def context_lookup_projection(cat,case,validated):
 for v in (cat,case,validated):status_exact_tree(v,'LOOKUP-EXACT-TYPE')
 keys={'scope','anchor','parent_result','binding','outcomes'};need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'LOOKUP-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'LOOKUP-VALIDATED:'+k)
 p=case['parent_result'];b=case['binding'];scope=case['scope'];oo=case['outcomes'];s=cat['source']
 status_typed_same(scope,p['scope'],'LOOKUP-SCOPE');status_typed_same(b,context_lookup_binding(cat,p,case['anchor'],b['continuity']),'LOOKUP-EXPECTED-BINDING')
 need(type(oo) is list and bool(oo),'LOOKUP-OUTCOMES')
 if b['continuity']=='UNESTABLISHED':status_typed_same(oo,[{'stage':'lookup:continuation','outcome':'unobserved'}],'LOOKUP-UNKNOWN-CONTINUITY')
 events=[];roles={name:None for name in s['method_order']};replacement=None;missing=None;last=None;complete=False
 for i,step in enumerate(s['steps']):
  need(i<len(oo),'LOOKUP-MISSING-STEP');r=oo[i];need(type(r) is dict and set(r)=={'stage','outcome'} and type(r['stage']) is str and r['stage']==step['id'],'LOOKUP-ORDER')
  last=r['outcome'];need(type(last) is str and last in step['allowed'],'LOOKUP-OUTCOME')
  event={'id':b['operand_occurrence']['id']+'/'+step['id'],'stage':step['id'],'scope':copy.deepcopy(scope),'helper_invocation':copy.deepcopy(b['helper_invocation']),'owner':copy.deepcopy(b['references']['owner']),'token':copy.deepcopy(b['references']['token']),'source':copy.deepcopy(step['source']),'receiver':copy.deepcopy(b['operand_role']),'method':step['method'],'outcome':last,'runtime_frame':None};events.append(event)
  if last!=step['normal_outcome']:
   if last in ('missing-method','raise','catchable-interruption'):
    if last=='missing-method':missing=step['method']
    replacement={'role':'conditional-context-lookup-error','reference':event['id']+'/error','scope':copy.deepcopy(scope),'origin':copy.deepcopy(step['source']),'frontier_stage':step['id'],'method':step['method'],'kind':last,'exact_type':None,'exact_value':None,'diagnostic_requested_type':step.get('diagnostic_requested_type') if last=='missing-method' else None,'diagnostic_completion_established':False,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_observation':False}
   break
  if step['method'] is not None:
   name=step['method'];roles[name]={'symbol':event['id']+'/lookup-result','scope':copy.deepcopy(scope),'method':name,'lookup_occurrence':event['id'],'receiver':copy.deepcopy(b['operand_role']),'source':copy.deepcopy(step['source']),'resolution':s['resolution'],'concrete_value':None,'concrete_type':None,'runtime_identity':None,'callability':'UNKNOWN','descriptor_effects':'UNKNOWN','live_reference_state':'UNKNOWN; acknowledged result role, not proof of retention after a later frontier'}
  if i==len(s['steps'])-1:complete=True
 need(len(oo)==len(events),'LOOKUP-UNREACHED-STEPS')
 out=copy.deepcopy(p);out.update({'kind':'CONSTRUCTED-CONTEXT-SPECIAL-LOOKUP','binding':copy.deepcopy(b),'predecessor_projection':copy.deepcopy(p),'events':events,'method_roles':roles,'completion':'protocol-lookups-complete' if complete else last+'-frontier','missing_method':missing,
  'context_protocol_lookup_established':complete,'lookup_completed_in_model':{k:v is not None for k,v in roles.items()},'enter_invocation_established':False,'exit_invocation_established':False,
  'replacement_error_in_model':replacement,'last_pending_error_in_model':copy.deepcopy(replacement if replacement is not None else p['last_pending_error_in_model']),'terminal_python_exception_in_model':None if last in ('process-termination','unobserved') else True,
  'prior_acknowledged_partial_effects':copy.deepcopy(p['current_partial_effects']),'current_partial_effects':'UNKNOWN; successful lookup or failure establishes no absence of descriptor, reference-release or physical file effects','descriptor_effects':'UNKNOWN','runtime_lookup_chain':None,'stop':s['stop']})
 return out

def validate_context_lookup_projection(cat,case,validated,submitted):
 status_exact_tree(submitted,'LOOKUP-OUTPUT-TYPE');status_typed_same(submitted,context_lookup_projection(cat,case,validated),'LOOKUP-OUTPUT-CORRESPONDENCE');return True

# I164-ENTER-CALL-ATTEMPT-1. All predecessor producer bytes above are retained.
def compile_enter_call(launcher,bytecodes,typeobject,r1,parent):
 for value in (r1,parent):status_exact_tree(value,'ENTER-CALL-CATALOGUE-TYPE')
 # Re-derive lookup expectations from defining bytes, independently of submitted declarations.
 validate_context_lookup(launcher,bytecodes,typeobject,r1,parent)
 text=bytecodes.decode();start=text.index('        inst(BEFORE_WITH,');end=text.index('        inst(WITH_EXCEPT_START,',start);block=text[start:end]
 sequence='            DECREF_INPUTS();\n            res = _PyObject_CallNoArgs(enter);'
 need(block.count(sequence)==1,'ENTER-CALL-SOURCE-ORDER')
 offset=start+block.index(sequence);decref=offset+len('            ');call=text.index('_PyObject_CallNoArgs(enter)',decref)
 need(block.index('exit = _PyObject_LookupSpecial')<block.index('if (exit == NULL)')<block.index(sequence),'ENTER-CALL-LOOKUP-GUARDS')
 def site(pos,expression):return {'source':copy.deepcopy(parent['source']['pins']['bytecodes']),'file':'Python/bytecodes.c','line':text.count('\n',0,pos)+1,'expression':expression,'tag':'v3.12.14'}
 target=site(call,'_PyObject_CallNoArgs(enter)');status_typed_same(target,parent['source']['next_call_excluded'],'ENTER-CALL-PARENT-SITE')
 steps=[{'id':'enter-call:continuation','source':site(decref,'DECREF_INPUTS();'),'normal_outcome':'normal','allowed':['normal','raise','catchable-interruption','process-termination','unobserved'],
         'meaning':'explicit conditional continuation from both successful lookups past the intervening source operation; no claim about its physical effects or internal failure mechanism'},
        {'id':'enter-call:attempt','source':target,'normal_outcome':'attempted','allowed':['attempted'],
         'meaning':'attempt at the selected C helper call site only; no helper or method-body entry, return, or res assignment'}]
 return {'format':'I164-ENTER-CALL-ATTEMPT-STATIC-1','source':{'launcher_operand':copy.deepcopy(parent['source']['open_call']),'with_statement':copy.deepcopy(parent['source']['with_statement']),
  'intervening_operation':site(decref,'DECREF_INPUTS();'),'call_site':target,'C_helper':'_PyObject_CallNoArgs','C_argument_expression':'enter','python_explicit_argument_count':0,
  'steps':steps,'order':[s['id'] for s in steps],'required_lookup_order':['__enter__','__exit__'],
  'contract':parent['source']['contract'],'stop':'at _PyObject_CallNoArgs(enter) attempt; before helper or method-body entry, outcome, res assignment, completed context entry or f binding'},
  'lookup_catalogue':copy.deepcopy(parent),'parent_catalogue_sha256':digest(enc(parent)),
  'declarations':[{'id':s['id'],'source':copy.deepcopy(s['source']),'meaning':s['meaning'],'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for s in steps],
  'guard_branches':{'continuity':['explicit conditional premise','UNESTABLISHED'],'prefixes':copy.deepcopy(parent['guard_branches']['prefixes']),'origins':copy.deepcopy(parent['guard_branches']['origins']),'steps':{s['id']:copy.deepcopy(s['allowed']) for s in steps}},
  'preserved_relations':['context_special_lookup_correspondence',*parent['preserved_relations']],'runtime_chain':None,'actual_admission':False}

def validate_enter_call(launcher,bytecodes,typeobject,r1,parent,submitted):
 status_exact_tree(submitted,'ENTER-CALL-CATALOGUE-TYPE');status_typed_same(submitted,compile_enter_call(launcher,bytecodes,typeobject,r1,parent),'ENTER-CALL-CATALOGUE-SOURCE');return True

def enter_call_binding(cat,parent,anchor,continuity):
 for value in (cat,parent,anchor,continuity):status_exact_tree(value,'ENTER-CALL-BINDING-TYPE')
 need(type(continuity) is str and continuity in ('explicit conditional premise','UNESTABLISHED'),'ENTER-CALL-CONTINUITY')
 need(parent['kind']=='CONSTRUCTED-CONTEXT-SPECIAL-LOOKUP' and parent['completion']=='protocol-lookups-complete','ENTER-CALL-PARENT-COMPLETION')
 need(parent['context_protocol_lookup_established'] is True and parent['lookup_completed_in_model']=={'__enter__':True,'__exit__':True},'ENTER-CALL-PARENT-LOOKUPS')
 for k in ('enter_invocation_established','exit_invocation_established','context_manager_entry_established','f_binding_established'):need(parent[k] is False,'ENTER-CALL-PARENT-BOUNDARY:'+k)
 need(parent['replacement_error_in_model'] is None and parent['terminal_python_exception_in_model'] is True,'ENTER-CALL-PARENT-ERROR')
 status_typed_same(parent['last_pending_error_in_model'],parent['original_error_pending_in_outer_handler'],'ENTER-CALL-ORIGINAL-PENDING')
 scope=parent['scope'];b=parent['binding']
 status_typed_same(parent['instance_anchor'],anchor,'ENTER-CALL-ANCHOR');status_typed_same(scope['instance'],anchor['instance'],'ENTER-CALL-INSTANCE')
 need(scope['context']==anchor['context'] and scope['acquisition']==anchor['record']['acquisition'],'ENTER-CALL-CONTEXT-ACQUISITION')
 need(b['continuity']=='explicit conditional premise','ENTER-CALL-PARENT-CONTINUITY')
 # Source/model parent consistency is supplemental; public authentication below
 # still requires the actual unchanged predecessor basis and checked construction.
 pc={'scope':copy.deepcopy(scope),'anchor':copy.deepcopy(anchor),'parent_result':copy.deepcopy(parent['predecessor_projection']),
     'binding':copy.deepcopy(b),'outcomes':[{'stage':e['stage'],'outcome':e['outcome']} for e in parent['events']]}
 validate_context_lookup_projection(cat['lookup_catalogue'],pc,pc,parent)
 status_typed_same(pc['outcomes'],[{'stage':'lookup:continuation','outcome':'normal'},{'stage':'lookup:__enter__','outcome':'found'},{'stage':'lookup:__exit__','outcome':'found'}],'ENTER-CALL-SELECTED-LOOKUPS')
 return {'scope':copy.deepcopy(scope),'anchor':copy.deepcopy(anchor),'helper_invocation':copy.deepcopy(b['helper_invocation']),
  'lookup_occurrences':copy.deepcopy(parent['events'][1:]),'method_results':copy.deepcopy(parent['method_roles']),'operand_role':copy.deepcopy(b['operand_role']),
  'references':copy.deepcopy(b['references']),'original_constructor_error':copy.deepcopy(parent['original_error_pending_in_outer_handler']),
  'details_role':copy.deepcopy(b['details_role']),'cleanup_list':copy.deepcopy(b['cleanup_list']),'continuity':continuity,
  'continuation_premise':'conditional same selected invocation, owner/token and symbolic references through DECREF_INPUTS; no observed exclusive ownership or physical retention',
  'intervening_operation':copy.deepcopy(cat['source']['intervening_operation']),'physical_identity':None}

def enter_call_projection(cat,case,validated):
 for v in (cat,case,validated):status_exact_tree(v,'ENTER-CALL-EXACT-TYPE')
 keys={'scope','anchor','parent_result','binding','outcomes'};need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'ENTER-CALL-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'ENTER-CALL-VALIDATED:'+k)
 p=case['parent_result'];b=case['binding'];scope=case['scope'];oo=case['outcomes'];s=cat['source']
 status_typed_same(scope,p['scope'],'ENTER-CALL-SCOPE');status_typed_same(b,enter_call_binding(cat,p,case['anchor'],b['continuity']),'ENTER-CALL-EXPECTED-BINDING')
 need(type(oo) is list and bool(oo),'ENTER-CALL-OUTCOMES')
 if b['continuity']=='UNESTABLISHED':status_typed_same(oo,[{'stage':'enter-call:continuation','outcome':'unobserved'}],'ENTER-CALL-UNKNOWN-CONTINUITY')
 events=[];replacement=None;attempt=False;last=None
 for i,step in enumerate(s['steps']):
  need(i<len(oo),'ENTER-CALL-MISSING-STEP');row=oo[i];need(type(row) is dict and set(row)=={'stage','outcome'} and type(row['stage']) is str and row['stage']==step['id'],'ENTER-CALL-ORDER')
  last=row['outcome'];need(type(last) is str and last in step['allowed'],'ENTER-CALL-OUTCOME')
  event={'id':b['lookup_occurrences'][-1]['id']+'/'+step['id'],'stage':step['id'],'scope':copy.deepcopy(scope),'helper_invocation':copy.deepcopy(b['helper_invocation']),
    'owner':copy.deepcopy(b['references']['owner']),'token':copy.deepcopy(b['references']['token']),'source':copy.deepcopy(step['source']),
    'lookup_occurrences':copy.deepcopy(b['lookup_occurrences']),'method_results':copy.deepcopy(b['method_results']),'outcome':last,'runtime_frame':None}
  events.append(event)
  if last!=step['normal_outcome']:
   if last in ('raise','catchable-interruption'):
    replacement={'role':'conditional-enter-call-continuation-error','reference':event['id']+'/error','scope':copy.deepcopy(scope),'frontier_stage':step['id'],
      'origin':'conditional interval before call attempt; not a proved DECREF_INPUTS internal failure mechanism','source_interval':copy.deepcopy(s['intervening_operation']),
      'kind':last,'exact_type':None,'exact_value':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_observation':False}
   break
  if i==len(s['steps'])-1:attempt=True
 need(len(oo)==len(events),'ENTER-CALL-UNREACHED-STEPS')
 out=copy.deepcopy(p);out.update({'kind':'CONSTRUCTED-ENTER-CALL-ATTEMPT','binding':copy.deepcopy(b),'predecessor_projection':copy.deepcopy(p),'events':events,
  'completion':'enter-call-attempt' if attempt else last+'-frontier','enter_call_attempt_established_in_model':attempt,
  'source_operation_acknowledged':copy.deepcopy(s['intervening_operation']),'continuation_past_source_operation_in_model':attempt,
  'source_operation_effects':'UNKNOWN; no physical reference release, descriptor, finalization, resource cleanup or exclusivity established',
  'call':{'source':copy.deepcopy(s['call_site']),'C_helper':s['C_helper'],'C_argument_expression':'enter','target_role':copy.deepcopy(b['method_results']['__enter__']),
    'retained_exit_role':copy.deepcopy(b['method_results']['__exit__']),'python_explicit_arguments':[],'receiver_rule':'no extra explicit receiver; the lookup result may already be descriptor-bound',
    'callability':'UNKNOWN','runtime_identity':None,'concrete_value':None,'attempted_in_model':True} if attempt else None,
  'call_outcome':None,'call_result_role':None,'helper_dispatch_entry_established':False,'method_body_entry_established':False,'res_assignment_established':False,
  'enter_invocation_established':False,'exit_invocation_established':False,'context_manager_entry_established':False,'f_binding_established':False,
  'replacement_error_in_model':replacement,'last_pending_error_in_model':copy.deepcopy(replacement if replacement is not None else p['last_pending_error_in_model']),
  'terminal_python_exception_in_model':None if last in ('process-termination','unobserved') else True,
  'prior_acknowledged_partial_effects':copy.deepcopy(p['current_partial_effects']),'current_partial_effects':'UNKNOWN; prior append/lookup/reference effects remain unresolved, including at a modeled call attempt',
  'runtime_call_attempt_chain':None,'stop':s['stop']})
 return out

def validate_enter_call_projection(cat,case,validated,submitted):
 status_exact_tree(submitted,'ENTER-CALL-OUTPUT-TYPE');status_typed_same(submitted,enter_call_projection(cat,case,validated),'ENTER-CALL-OUTPUT-CORRESPONDENCE');return True

# I164-ENTER-RETURN-RES-1. The entire reviewed producer prefix remains unchanged.
def compile_enter_return(launcher,bytecodes,typeobject,r1,lookup,parent):
 for value in (r1,lookup,parent):status_exact_tree(value,'ENTER-RETURN-CATALOGUE-TYPE')
 validate_enter_call(launcher,bytecodes,typeobject,r1,lookup,parent)
 text=bytecodes.decode();start=text.index('        inst(BEFORE_WITH,');end=text.index('        inst(WITH_EXCEPT_START,',start);block=text[start:end]
 statement='            res = _PyObject_CallNoArgs(enter);'
 need(block.count(statement)==1,'ENTER-RETURN-ASSIGNMENT-SOURCE')
 pos=start+block.index(statement);nextpos=pos+len(statement)+1
 need(text[nextpos:].startswith('            Py_DECREF(enter);\n            if (res == NULL)'), 'ENTER-RETURN-STOP-SOURCE')
 def site(offset,expression):return {'source':copy.deepcopy(parent['source']['call_site']['source']),'file':'Python/bytecodes.c','line':text.count('\n',0,offset)+1,'expression':expression,'tag':'v3.12.14'}
 call=site(pos,'_PyObject_CallNoArgs(enter)');status_typed_same(call,parent['source']['call_site'],'ENTER-RETURN-PARENT-SOURCE')
 assignment=site(pos,statement.strip());excluded=site(nextpos,'Py_DECREF(enter);')
 steps=[{'id':'enter-return:continuation','source':call,'allowed':['normal','raise','catchable-interruption','process-termination','unobserved'],'meaning':'explicit conditional continuation from selected authenticated call attempt; no inferred dispatch/body or runtime arrival'},
        {'id':'enter-return:c-return','source':call,'allowed':['non-NULL','NULL','raise','catchable-interruption','process-termination','unobserved'],'meaning':'completed C result distinguishes non-NULL PyObject pointer and C NULL; other frontiers do not establish a completed return'},
        {'id':'enter-return:res-assignment','source':assignment,'allowed':['assigned','process-termination','unobserved'],'meaning':'assign the already returned C value to res, or retain the completed return with assignment unestablished; no assignment-failure mechanism invented'}]
 return {'format':'I164-ENTER-RETURN-RES-STATIC-1','source':{'launcher_operand':copy.deepcopy(parent['source']['launcher_operand']),'with_statement':copy.deepcopy(parent['source']['with_statement']),
  'call_site':call,'assignment':assignment,'next_operation_excluded':excluded,'C_helper':'_PyObject_CallNoArgs','C_argument_expression':'enter','target':'res',
  'steps':steps,'order':[x['id'] for x in steps],'non_NULL_object_cases':['opaque','Python-None'],
  'contract':parent['source']['contract'],'error_indicator_contract':'UNKNOWN; no deeper helper contract or concrete error inferred from C NULL or a non-NULL result',
  'stop':'after selected C return and res assignment, or first nonnormal/unobserved frontier; before Py_DECREF(enter) at line2516'},
  'enter_call_catalogue':copy.deepcopy(parent),'parent_catalogue_sha256':digest(enc(parent)),
  'declarations':[{'id':x['id'],'source':copy.deepcopy(x['source']),'meaning':x['meaning'],'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for x in steps],
  'guard_branches':{'continuity':['explicit conditional premise','UNESTABLISHED'],'prefixes':copy.deepcopy(parent['guard_branches']['prefixes']),'origins':copy.deepcopy(parent['guard_branches']['origins']),'steps':{x['id']:copy.deepcopy(x['allowed']) for x in steps},'non_NULL_object_cases':['opaque','Python-None']},
  'preserved_relations':['enter_call_attempt_correspondence',*parent['preserved_relations']],'runtime_chain':None,'actual_admission':False}

def validate_enter_return(launcher,bytecodes,typeobject,r1,lookup,parent,submitted):
 status_exact_tree(submitted,'ENTER-RETURN-CATALOGUE-TYPE');status_typed_same(submitted,compile_enter_return(launcher,bytecodes,typeobject,r1,lookup,parent),'ENTER-RETURN-CATALOGUE-SOURCE');return True

def enter_return_binding(cat,parent,anchor,continuity):
 for value in (cat,parent,anchor,continuity):status_exact_tree(value,'ENTER-RETURN-BINDING-TYPE')
 need(type(continuity) is str and continuity in ('explicit conditional premise','UNESTABLISHED'),'ENTER-RETURN-CONTINUITY')
 need(parent['kind']=='CONSTRUCTED-ENTER-CALL-ATTEMPT' and parent['completion']=='enter-call-attempt' and parent['enter_call_attempt_established_in_model'] is True,'ENTER-RETURN-PARENT-ATTEMPT')
 need(parent['continuation_past_source_operation_in_model'] is True,'ENTER-RETURN-PARENT-CONTINUATION')
 need(parent['call_outcome'] is None and parent['call_result_role'] is None and parent['res_assignment_established'] is False,'ENTER-RETURN-PARENT-STOP')
 need(parent['replacement_error_in_model'] is None and parent['terminal_python_exception_in_model'] is True,'ENTER-RETURN-PARENT-ERROR')
 status_typed_same(parent['last_pending_error_in_model'],parent['original_error_pending_in_outer_handler'],'ENTER-RETURN-ORIGINAL-PENDING')
 scope=parent['scope'];status_typed_same(parent['instance_anchor'],anchor,'ENTER-RETURN-ANCHOR');status_typed_same(scope['instance'],anchor['instance'],'ENTER-RETURN-INSTANCE')
 need(scope['context']==anchor['context'] and scope['acquisition']==anchor['record']['acquisition'],'ENTER-RETURN-CONTEXT-ACQUISITION')
 pc={'scope':copy.deepcopy(scope),'anchor':copy.deepcopy(anchor),'parent_result':copy.deepcopy(parent['predecessor_projection']),'binding':copy.deepcopy(parent['binding']),'outcomes':[{'stage':e['stage'],'outcome':e['outcome']} for e in parent['events']]}
 validate_enter_call_projection(cat['enter_call_catalogue'],pc,pc,parent)
 status_typed_same(pc['outcomes'],[{'stage':'enter-call:continuation','outcome':'normal'},{'stage':'enter-call:attempt','outcome':'attempted'}],'ENTER-RETURN-EXACT-ATTEMPT')
 need(parent['binding']['continuity']=='explicit conditional premise','ENTER-RETURN-PARENT-CONTINUITY')
 return {'scope':copy.deepcopy(scope),'anchor':copy.deepcopy(anchor),'attempt':copy.deepcopy(parent['events'][-1]),'call':copy.deepcopy(parent['call']),
  'helper_invocation':copy.deepcopy(parent['binding']['helper_invocation']),'references':copy.deepcopy(parent['binding']['references']),
  'method_results':copy.deepcopy(parent['binding']['method_results']),'operand_role':copy.deepcopy(parent['binding']['operand_role']),
  'original_constructor_error':copy.deepcopy(parent['original_error_pending_in_outer_handler']),'details_role':copy.deepcopy(parent['binding']['details_role']),'cleanup_list':copy.deepcopy(parent['binding']['cleanup_list']),
  'continuity':continuity,'premise':'conditional selected invocation/owner/token/callable/reference continuity; no established runtime arrival, identity, exclusivity or helper-internal error contract','physical_identity':None}

def enter_return_projection(cat,case,validated):
 for v in (cat,case,validated):status_exact_tree(v,'ENTER-RETURN-EXACT-TYPE')
 keys={'scope','anchor','parent_result','binding','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'ENTER-RETURN-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'ENTER-RETURN-VALIDATED:'+k)
 p=case['parent_result'];b=case['binding'];scope=case['scope'];oo=case['outcomes'];s=cat['source']
 status_typed_same(scope,p['scope'],'ENTER-RETURN-SCOPE');status_typed_same(b,enter_return_binding(cat,p,case['anchor'],b['continuity']),'ENTER-RETURN-EXPECTED-BINDING')
 need(type(oo) is list and bool(oo),'ENTER-RETURN-OUTCOMES')
 if b['continuity']=='UNESTABLISHED':status_typed_same(oo,[{'stage':'enter-return:continuation','outcome':'unobserved'}],'ENTER-RETURN-UNKNOWN-CONTINUITY')
 events=[];replacement=None;completed=False;assigned=False;value=None;assignment=None;last=None;return_event=None
 for i,step in enumerate(s['steps']):
  need(i<len(oo),'ENTER-RETURN-MISSING-STEP');row=oo[i];need(type(row) is dict and type(row.get('stage')) is str and row['stage']==step['id'],'ENTER-RETURN-ORDER')
  last=row.get('outcome');need(type(last) is str and last in step['allowed'],'ENTER-RETURN-OUTCOME')
  required={'stage','outcome'}|({'object_case'} if i==1 and last=='non-NULL' else set());need(set(row)==required,'ENTER-RETURN-STAGE-FIELDS')
  if 'object_case' in row:need(type(row['object_case']) is str and row['object_case'] in s['non_NULL_object_cases'],'ENTER-RETURN-OBJECT-CASE')
  event={'id':b['attempt']['id']+'/'+step['id'],'stage':step['id'],'scope':copy.deepcopy(scope),'source':copy.deepcopy(step['source']),
   'selected_attempt':b['attempt']['id'],'helper_invocation':copy.deepcopy(b['helper_invocation']),'owner':copy.deepcopy(b['references']['owner']),'token':copy.deepcopy(b['references']['token']),
   'enter_role':copy.deepcopy(b['method_results']['__enter__']),'exit_role':copy.deepcopy(b['method_results']['__exit__']),'outcome':last,'runtime_frame':None}
  if 'object_case' in row:event['object_case']=row['object_case']
  events.append(event)
  if i==1 and last in ('non-NULL','NULL'):
   completed=True;return_event=event
   value={'kind':'SYMBOLIC-PYOBJECT' if last=='non-NULL' else 'C-NULL','symbol':event['id']+'/C-result','scope':copy.deepcopy(scope),'return_occurrence':event['id'],
    'C_NULL':last=='NULL','python_value_class':row['object_case'] if last=='non-NULL' else None,'python_object_role':event['id']+'/object' if last=='non-NULL' else None,
    'concrete_value':None,'runtime_identity':None,'runtime_observation':False,'meaning':'constructed value-class premise only; None concrete_value means unobserved, not Python None or C NULL'}
  elif i==2 and last=='assigned':
   need(completed and value is not None,'ENTER-RETURN-ASSIGNMENT-WITHOUT-RETURN');assigned=True
   assignment={'target':'res','source':copy.deepcopy(s['assignment']),'occurrence':event['id'],'from_return_occurrence':return_event['id'],'value':copy.deepcopy(value),
    'reference_semantics':'source-level C result forwarding; equal recorded values do not establish observed physical object identity'}
  elif not(i==0 and last=='normal'):
   if last in ('raise','catchable-interruption'):
    replacement={'role':'conditional-enter-return-frontier-error','reference':event['id']+'/error','scope':copy.deepcopy(scope),'frontier_stage':step['id'],'source':copy.deepcopy(step['source']),
     'kind':last,'origin':'conditional frontier before established C return; no concrete helper or assignment failure mechanism inferred','exact_type':None,'exact_value':None,
     'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_observation':False}
   break
 need(len(oo)==len(events),'ENTER-RETURN-UNREACHED-STEPS')
 out=copy.deepcopy(p);out.update({'kind':'CONSTRUCTED-ENTER-RETURN-RES','binding':copy.deepcopy(b),'predecessor_projection':copy.deepcopy(p),'events':events,
  'completion':'res-assigned-'+('NULL' if value['C_NULL'] else 'non-NULL') if assigned else last+'-frontier',
  'helper_c_return_completed_in_model':completed,'call_outcome':('C-return-NULL' if value['C_NULL'] else 'C-return-non-NULL') if completed else None,
  'call_result_role':copy.deepcopy(value),'res_assignment_established':assigned,'res_assignment':assignment,'res_value_role':copy.deepcopy(value) if assigned else None,
  'helper_error_indicator':'UNKNOWN','helper_error_contract_established':False,'C_NULL_implies_python_exception_established':False,
  'no_replacement_inferred_from_C_result':True,'last_acknowledged_pending_error_before_call':copy.deepcopy(p['last_pending_error_in_model']),
  'replacement_error_in_model':replacement,'last_pending_error_in_model':copy.deepcopy(replacement if replacement is not None else p['last_pending_error_in_model']),
  'pending_error_qualification':'original outer-handler error remains retained under conditional continuity; this field does not classify the helper C error indicator, prove absence of a replacement, or select later propagation',
  'terminal_python_exception_in_model':None if last in ('process-termination','unobserved') else True,
  'helper_dispatch_entry_established':False,'method_body_entry_established':False,'enter_invocation_established':False,'exit_invocation_established':False,
  'post_call_decref_established':False,'result_test_established':False,'result_error_routing_established':False,'context_manager_entry_established':False,'f_binding_established':False,
  'prior_acknowledged_partial_effects':copy.deepcopy(p['current_partial_effects']),'current_partial_effects':'UNKNOWN; prior append/lookup/reference and possible call effects remain unresolved even after modeled res assignment',
  'runtime_enter_return_chain':None,'stop':s['stop']})
 return out

def validate_enter_return_projection(cat,case,validated,submitted):
 status_exact_tree(submitted,'ENTER-RETURN-OUTPUT-TYPE');status_typed_same(submitted,enter_return_projection(cat,case,validated),'ENTER-RETURN-OUTPUT-CORRESPONDENCE');return True

# I164-ENTER-DECREF-ATTEMPT-1. Complete 452,888-byte reviewed prefix preserved.
def compile_enter_decref(launcher,bytecodes,typeobject,r1,lookup,enter,parent):
 for value in (r1,lookup,enter,parent):status_exact_tree(value,'ENTER-DECREF-CATALOGUE-TYPE')
 validate_enter_return(launcher,bytecodes,typeobject,r1,lookup,enter,parent)
 text=bytecodes.decode();start=text.index('        inst(BEFORE_WITH,');end=text.index('        inst(WITH_EXCEPT_START,',start);block=text[start:end]
 sequence='            res = _PyObject_CallNoArgs(enter);\n            Py_DECREF(enter);\n            if (res == NULL) {'
 need(block.count(sequence)==1,'ENTER-DECREF-SOURCE-ORDER')
 pos=start+block.index(sequence)+len('            res = _PyObject_CallNoArgs(enter);\n');testpos=pos+len('            Py_DECREF(enter);\n')
 def site(offset,expression):return {'source':copy.deepcopy(parent['source']['assignment']['source']),'file':'Python/bytecodes.c','line':text.count('\n',0,offset)+1,'expression':expression,'tag':'v3.12.14'}
 operation=site(pos,'Py_DECREF(enter);');status_typed_same(operation,parent['source']['next_operation_excluded'],'ENTER-DECREF-PARENT-BOUNDARY')
 steps=[{'id':'enter-decref:continuation','source':operation,'allowed':['normal','raise','catchable-interruption','process-termination','unobserved'],'meaning':'explicit conditional continuation from assigned res; interval error is not an invented Py_DECREF failure mechanism'},
        {'id':'enter-decref:attempt','source':operation,'allowed':['attempted','process-termination','unobserved'],'meaning':'selected source-operation attempt only; no macro expansion, completion, call frame or physical effect'}]
 return {'format':'I164-ENTER-DECREF-ATTEMPT-STATIC-1','source':{'launcher_operand':copy.deepcopy(parent['source']['launcher_operand']),'with_statement':copy.deepcopy(parent['source']['with_statement']),
  'assignment':copy.deepcopy(parent['source']['assignment']),'operation':operation,'operand_expression':'enter','operation_spelling':'Py_DECREF','next_operation_excluded':site(testpos,'if (res == NULL) {'),
  'steps':steps,'order':[x['id'] for x in steps],'res_classes':['C-NULL','non-NULL/opaque','non-NULL/Python-None'],'res_non_NULL_guard':False,
  'contract':parent['source']['contract'],'interpretation':'source operation, not an assumed separately observed C function or macro-body execution',
  'stop':'at selected Py_DECREF(enter) source-operation attempt at line2516 or first nonnormal/unobserved frontier; before operation completion/effects and result test at2517'},
  'enter_return_catalogue':copy.deepcopy(parent),'parent_catalogue_sha256':digest(enc(parent)),
  'declarations':[{'id':x['id'],'source':copy.deepcopy(x['source']),'meaning':x['meaning'],'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for x in steps],
  'guard_branches':{'continuity':['explicit conditional premise','UNESTABLISHED'],'prefixes':copy.deepcopy(parent['guard_branches']['prefixes']),'origins':copy.deepcopy(parent['guard_branches']['origins']),'steps':{x['id']:copy.deepcopy(x['allowed']) for x in steps},'res_non_NULL_guard':False},
  'preserved_relations':['enter_return_res_correspondence',*parent['preserved_relations']],'runtime_chain':None,'actual_admission':False}

def validate_enter_decref(launcher,bytecodes,typeobject,r1,lookup,enter,parent,submitted):
 status_exact_tree(submitted,'ENTER-DECREF-CATALOGUE-TYPE');status_typed_same(submitted,compile_enter_decref(launcher,bytecodes,typeobject,r1,lookup,enter,parent),'ENTER-DECREF-CATALOGUE-SOURCE');return True

def enter_decref_binding(cat,parent,anchor,continuity):
 for value in (cat,parent,anchor,continuity):status_exact_tree(value,'ENTER-DECREF-BINDING-TYPE')
 need(type(continuity) is str and continuity in ('explicit conditional premise','UNESTABLISHED'),'ENTER-DECREF-CONTINUITY')
 need(parent['kind']=='CONSTRUCTED-ENTER-RETURN-RES' and parent['helper_c_return_completed_in_model'] is True and parent['res_assignment_established'] is True,'ENTER-DECREF-COMPLETED-ASSIGNMENT')
 pc={'scope':copy.deepcopy(parent['scope']),'anchor':copy.deepcopy(parent['instance_anchor']),'parent_result':copy.deepcopy(parent['predecessor_projection']),'binding':copy.deepcopy(parent['binding']),
  'outcomes':[{k:copy.deepcopy(e[k]) for k in ('stage','outcome','object_case') if k in e} for e in parent['events']]}
 validate_enter_return_projection(cat['enter_return_catalogue'],pc,pc,parent)
 need(parent['events'][-1]['stage']=='enter-return:res-assignment' and parent['events'][-1]['outcome']=='assigned','ENTER-DECREF-ASSIGNMENT-FRONTIER')
 need(parent['binding']['continuity']=='explicit conditional premise','ENTER-DECREF-PARENT-CONTINUITY')
 need(parent['post_call_decref_established'] is False and parent['result_test_established'] is False,'ENTER-DECREF-PARENT-STOP')
 scope=parent['scope'];status_typed_same(parent['instance_anchor'],anchor,'ENTER-DECREF-ANCHOR');status_typed_same(scope['instance'],anchor['instance'],'ENTER-DECREF-INSTANCE')
 need(scope['context']==anchor['context'] and scope['acquisition']==anchor['record']['acquisition'],'ENTER-DECREF-CONTEXT-ACQUISITION')
 return {'scope':copy.deepcopy(scope),'anchor':copy.deepcopy(anchor),'assignment_occurrence':copy.deepcopy(parent['events'][-1]),'res_assignment':copy.deepcopy(parent['res_assignment']),
  'res_value_role':copy.deepcopy(parent['res_value_role']),'operand_role':copy.deepcopy(parent['binding']['method_results']['__enter__']),'exit_role':copy.deepcopy(parent['binding']['method_results']['__exit__']),
  'method_results':copy.deepcopy(parent['binding']['method_results']),'helper_invocation':copy.deepcopy(parent['binding']['helper_invocation']),'references':copy.deepcopy(parent['binding']['references']),
  'original_constructor_error':copy.deepcopy(parent['original_error_pending_in_outer_handler']),'pending_error_before_operation':copy.deepcopy(parent['last_pending_error_in_model']),
  'details_role':copy.deepcopy(parent['binding']['details_role']),'cleanup_list':copy.deepcopy(parent['binding']['cleanup_list']),
  'continuity':continuity,'premise':'conditional selected invocation/owner/token/enter-result continuity; assignment alone establishes no runtime arrival or decrement effects','physical_identity':None}

def enter_decref_projection(cat,case,validated):
 for value in (cat,case,validated):status_exact_tree(value,'ENTER-DECREF-EXACT-TYPE')
 keys={'scope','anchor','parent_result','binding','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'ENTER-DECREF-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'ENTER-DECREF-VALIDATED:'+k)
 p=case['parent_result'];b=case['binding'];scope=case['scope'];oo=case['outcomes'];s=cat['source']
 status_typed_same(scope,p['scope'],'ENTER-DECREF-SCOPE');status_typed_same(b,enter_decref_binding(cat,p,case['anchor'],b['continuity']),'ENTER-DECREF-EXPECTED-BINDING')
 need(type(oo) is list and bool(oo),'ENTER-DECREF-OUTCOMES')
 if b['continuity']=='UNESTABLISHED':status_typed_same(oo,[{'stage':'enter-decref:continuation','outcome':'unobserved'}],'ENTER-DECREF-UNKNOWN-CONTINUITY')
 events=[];replacement=None;attempted=False;operation=None;last=None
 for i,step in enumerate(s['steps']):
  need(i<len(oo),'ENTER-DECREF-MISSING-STEP');row=oo[i];need(type(row) is dict and set(row)=={'stage','outcome'},'ENTER-DECREF-STAGE-FIELDS')
  need(type(row['stage']) is str and row['stage']==step['id'],'ENTER-DECREF-ORDER');last=row['outcome'];need(type(last) is str and last in step['allowed'],'ENTER-DECREF-OUTCOME')
  event={'id':b['assignment_occurrence']['id']+'/'+step['id'],'stage':step['id'],'scope':copy.deepcopy(scope),'source':copy.deepcopy(step['source']),
   'selected_assignment':b['assignment_occurrence']['id'],'helper_invocation':copy.deepcopy(b['helper_invocation']),'owner':copy.deepcopy(b['references']['owner']),'token':copy.deepcopy(b['references']['token']),
   'operand_role':copy.deepcopy(b['operand_role']),'res_value_role':copy.deepcopy(b['res_value_role']),'exit_role':copy.deepcopy(b['exit_role']),'outcome':last,'runtime_frame':None}
  events.append(event)
  if i==1 and last=='attempted':
   attempted=True;operation={'occurrence':event['id'],'source':copy.deepcopy(s['operation']),'spelling':'Py_DECREF','operand_expression':'enter','operand_role':copy.deepcopy(b['operand_role']),
    'reference_semantics':'selected symbolic enter-result forwarding, not observed physical identity or a C call-frame claim','macro_expansion':None,'concrete_reference_count':None,'runtime_observation':False}
  elif not(i==0 and last=='normal'):
   if last in ('raise','catchable-interruption'):
    replacement={'role':'conditional-enter-decref-continuation-error','reference':event['id']+'/error','scope':copy.deepcopy(scope),'frontier_stage':step['id'],'source':copy.deepcopy(step['source']),
     'kind':last,'origin':'conditional continuation interval before established operation attempt; not a concrete Py_DECREF failure mechanism','exact_type':None,'exact_value':None,
     'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_observation':False}
   break
 need(len(oo)==len(events),'ENTER-DECREF-UNREACHED-STEPS')
 out=copy.deepcopy(p);out.update({'kind':'CONSTRUCTED-ENTER-DECREF-ATTEMPT','binding':copy.deepcopy(b),'predecessor_projection':copy.deepcopy(p),'events':events,
  'completion':'enter-decref-attempt' if attempted else last+'-frontier','post_call_decref_attempt_established_in_model':attempted,'decref_operation':operation,
  'post_call_decref_established':False,'decref_completion_established':False,'decref_effects_established':False,'macro_expansion_established':False,'reference_count_change_established':False,
  'finalization_established':False,'decref_callback_execution_established':False,'physical_release_established':False,'result_test_established':False,'result_error_routing_established':False,
  'context_manager_entry_established':False,'f_binding_established':False,'last_acknowledged_pending_error_before_decref':copy.deepcopy(p['last_pending_error_in_model']),
  'replacement_error_in_model':copy.deepcopy(replacement if replacement is not None else p['replacement_error_in_model']),
  'last_pending_error_in_model':copy.deepcopy(replacement if replacement is not None else p['last_pending_error_in_model']),
  'terminal_python_exception_in_model':None if last in ('process-termination','unobserved') else True,
  'pending_error_qualification':'original outer error and prior error evidence retained; conditional continuation error is distinct; helper C error indicator and eventual propagation remain unestablished',
  'prior_acknowledged_partial_effects':copy.deepcopy(p['current_partial_effects']),'current_partial_effects':'UNKNOWN; earlier append/lookup/reference/call effects remain unresolved; this attempt establishes no decrement effect',
  'runtime_enter_decref_chain':None,'stop':s['stop']})
 return out

def validate_enter_decref_projection(cat,case,validated,submitted):
 status_exact_tree(submitted,'ENTER-DECREF-OUTPUT-TYPE');status_typed_same(submitted,enter_decref_projection(cat,case,validated),'ENTER-DECREF-OUTPUT-CORRESPONDENCE');return True

# I164-DECREF-FAST-COMPLETION-1. Full 464,085-byte predecessor prefix unchanged.
def decref_fast_sources(files):
 """Exact source envelope, read as bytes; no C preprocessing or execution."""
 pins = {'Python/ceval.c': {'bytes': 88767, 'sha256': '29640a033f373391a5b000253f74a7a1bc3182265412c0b40a76c4615acd1fda'}, 'Python/bytecodes.c': {'bytes': 143622, 'sha256': 'f8c050621f1498d953d4898aaf29457e154620fec7f8bb987b4d3fde6f5a1d84'}, 'Include/Python.h': {'bytes': 2854, 'sha256': '729ef157f6026e6e1b3104593f87dddc597c3b83b60c7c2965878c62a56c6f7d'}, 'Include/internal/pycore_abstract.h': {'bytes': 611, 'sha256': '75ecd34cdcd06fc64fcfa550f66975d755619e7cf06fdae8ecbe2de6ec49ce39'}, 'Include/internal/pycore_call.h': {'bytes': 3920, 'sha256': '5e780aed2dc991455a0e528fc7baca8df61d2e4bec4e137d7e788668b5750ec5'}, 'Include/internal/pycore_ceval.h': {'bytes': 5265, 'sha256': '1af22b50c9ececfc4c3a5f37ecb70cc1c0eefad5a2656e6e22fc088cae54e226'}, 'Include/internal/pycore_code.h': {'bytes': 15835, 'sha256': '48e78dd1a12e6afa6e54e26f8e7c4f56e20689b84189d503507c7f6c36819092'}, 'Include/internal/pycore_function.h': {'bytes': 611, 'sha256': '8fad970bd3f31347aed72b92acd17270dbb6ec5333ab5ed6fe43dc9cf2527841'}, 'Include/internal/pycore_intrinsics.h': {'bytes': 1397, 'sha256': 'e6d6d1eae51b508196615094a4c17189e9822eacb5c0e94102e78aa7136dd9a8'}, 'Include/internal/pycore_long.h': {'bytes': 7805, 'sha256': '84c0c7bd7ba0c2fbbfb106561e32328e478d8350afe756af6a4862c95d921a06'}, 'Include/internal/pycore_instruments.h': {'bytes': 2998, 'sha256': 'dcdb0593cfa908c036d6661f1a776db48642c0fedd243da88161f45ff3c3e3fa'}, 'Include/internal/pycore_object.h': {'bytes': 14917, 'sha256': '56c99d065465adb1255cbb064a3b8bc52698393965982cfd9fd6adf54adc60f5'}, 'Include/internal/pycore_moduleobject.h': {'bytes': 1192, 'sha256': '55a8f42968545a349d8e0b43cd1822b22ae2cf9fa0fb098c6bb843e7af76e165'}, 'Include/internal/pycore_opcode.h': {'bytes': 20081, 'sha256': '432e30c6145dff72096325d17192d0eff9895b367d4590f782e2d8b9d5f78cd6'}, 'Include/internal/pycore_pyerrors.h': {'bytes': 3110, 'sha256': '87b6e1741b1d6c4fd7b370b41b06df113109a84f2308d01c4793315a538274b4'}, 'Include/internal/pycore_pymem.h': {'bytes': 3040, 'sha256': 'ad0b35bbf5e665e90223499f8954bfcf36448b1634d54501b0c84d08680323ca'}, 'Include/internal/pycore_pystate.h': {'bytes': 4982, 'sha256': 'c06823811bf5dd3d84f40d6a087452da5915e3ad277afef2202c9e86e833ce00'}, 'Include/internal/pycore_range.h': {'bytes': 346, 'sha256': '824c5023a85a9c1c2dd50fecf442d12c7b2966e0e71a2d291f6f17f7fd8c29bc'}, 'Include/internal/pycore_sliceobject.h': {'bytes': 414, 'sha256': 'e8b9ba794081a75bf73f0eb64089a766b5bd04b076d4368a14a83ff43ce909be'}, 'Include/internal/pycore_sysmodule.h': {'bytes': 999, 'sha256': '668e205cf1d4807953f1240d0e2420169c068607b94b05505179f8d6cce2d5e4'}, 'Include/internal/pycore_traceback.h': {'bytes': 3501, 'sha256': '3f9dfb009dc161f2d979f5af76d660611264b5d0b1b4adeeae10d30ee0999ede'}, 'Include/internal/pycore_tuple.h': {'bytes': 2197, 'sha256': 'de5677ac0809abf2744ebdd94768b6974e75ea62cc2cee44c4f433e2b818f953'}, 'Include/internal/pycore_typeobject.h': {'bytes': 4731, 'sha256': '7cbcc82334920ed3711f7cd761114d39168697bcf4d8ba85583cf4b25cc2c46a'}, 'Include/internal/pycore_emscripten_signal.h': {'bytes': 562, 'sha256': '1acd47a1c09e365be8c7fa51db31307021cc2e471471fc199e26f317df58c4b8'}, 'Include/internal/pycore_dict.h': {'bytes': 6384, 'sha256': '4d51e7184d50a5f8785a1cbdc9f6eb36b86201158ae6e3527884ce2b5dd504bf'}, 'Include/dictobject.h': {'bytes': 3860, 'sha256': '08f92e2a4421d3e81fa0fa1b60cbe97f2d69897226368481b0ffc41eeb202356'}, 'Include/internal/pycore_frame.h': {'bytes': 9255, 'sha256': '23d66ba6ef2936ecca96dc427be5e022712ae25c3f4b3df2abd2ca46b1ee5f39'}, 'Include/frameobject.h': {'bytes': 336, 'sha256': '969cd93065ce79b81bbc67a65d31b742e23f30bf79d6e44a306963d552ed0c35'}, 'Include/opcode.h': {'bytes': 12808, 'sha256': '4e8c6eee859813845b3a9dfe9e08ca4cc607a7f884048f5a6cebef6bdcc5d33d'}, 'Include/pydtrace.h': {'bytes': 2404, 'sha256': '7ac591e56e12936a32e3b0b85dae803f8f00bdc91abe01799ca2e4ce69548555'}, 'Include/setobject.h': {'bytes': 1557, 'sha256': '7ff1b984647598b19ff593b0fa40d44cf5d7bc37d386dd9fac059e560f4a31ca'}, 'Include/structmember.h': {'bytes': 1645, 'sha256': '9d4c39dee96e228f60cc8a6960b9e7049875ddbee15541a75629c07777916342'}, 'Python/ceval_macros.h': {'bytes': 12923, 'sha256': '3191f006924630d06aafd10deade8f6c4ff551a4efcde2902c4e9a5326cf51fd'}, 'Python/opcode_targets.h': {'bytes': 7466, 'sha256': '56e32cac65295cddfa90ecef1e2f63ebf79eda4318329fb50631e0ebd7379258'}, 'Python/generated_cases.c.h': {'bytes': 195111, 'sha256': '579706b9011997eed918fb546bd9382e8416d8cba3f9e87282aa5fa472c08b29'}, 'Include/patchlevel.h': {'bytes': 1301, 'sha256': '66ff726e200a2eba15cfedee752bf6a59e20d6741a7c45f7a2c424dea649f473'}, 'Include/pyconfig.h': {'bytes': 55933, 'sha256': '3a9546822f3c1b28caaedabf93cc862215f4cbff25a8d209edc08a21b908beba'}, 'Include/pymacconfig.h': {'bytes': 2810, 'sha256': '5dcd4fa505975be42c35a4707ab7cb5b6ddf2e896bb8fbb8c1fd9047e5183a3d'}, 'Include/pyport.h': {'bytes': 25593, 'sha256': '1cb92172d631c9176c32caec8a330c74a544e4a5a2f1e82c15b0f2411fb87bb7'}, 'Include/pymacro.h': {'bytes': 6656, 'sha256': 'c82a7ed12ffe85aa119e917a486a388cb0fc345719a7330bf1e2951d2d4f5282'}, 'Include/pymath.h': {'bytes': 1688, 'sha256': 'eeea8396e1acd271ba83a568ba572ead47493e492ce998756fe1256bf917b3f9'}, 'Include/pymem.h': {'bytes': 3914, 'sha256': '54a5315d7861e989c5099f168d946f5a421337efcd5d44896201016e92a81348'}, 'Include/pytypedefs.h': {'bytes': 851, 'sha256': '26d09a78c44998e8c0a74ed2d14e5346e4b922892eb79288049b7ac5b6a1e751'}, 'Include/pybuffer.h': {'bytes': 5282, 'sha256': 'c95edd830772e922f60f976ac0d98470b48a443ba198b0866a4096003c0740a4'}, 'Include/object.h': {'bytes': 37155, 'sha256': '68b97095c521fcb3fab7193e166870b0c040c8f19ac50efb42088364862503a7'}, 'Include/objimpl.h': {'bytes': 9238, 'sha256': '8828a8db3e9f14b5ca2d59b1d8c05f6bf54fae26736ae039b7420c886142dba2'}, 'Include/typeslots.h': {'bytes': 2342, 'sha256': '77fe4a71f5e5974c40fd3485d3c9aeb8b7ccf33969cd26feb58c64eda5f86f1d'}, 'Include/pyhash.h': {'bytes': 4252, 'sha256': 'a6bfc2bdb7d20abd9ee39d1a4ded6308632bf5d7534683d4032e4b7de2d8b355'}, 'Include/cpython/pydebug.h': {'bytes': 1413, 'sha256': '83d72e867b4fc9ac87efdfcb41c3d30ec20fa239fe6a74d1b85aa92e1f8d9506'}, 'Include/bytearrayobject.h': {'bytes': 1466, 'sha256': '0e93963caf43a057fb293ae5183d1b8bb45c9f57926ce8308f67a0f452843e85'}, 'Include/bytesobject.h': {'bytes': 2619, 'sha256': 'de8551db9323e7dc463717a624f2d35dacd17cdf0c7a7f6299128dd06348cf30'}, 'Include/unicodeobject.h': {'bytes': 35164, 'sha256': '5cc1350da2b00f5187065004a1f5d66764e86a0f20f8faba7d0eadf913297d93'}, 'Include/cpython/initconfig.h': {'bytes': 7820, 'sha256': '86e3b9d1de6f310415912e2cdfdc276e311c026ec7fdf6190893f6313cd860a3'}, 'Include/pystate.h': {'bytes': 4635, 'sha256': '065426aaa5fada90d61a17757fbc2e8ce3fb9cc203992990c4ca3cee7f9f80be'}, 'Include/pyerrors.h': {'bytes': 13017, 'sha256': '59bf06c7ba877ec76d09a41aac75e385a2723545388b105864f48f295e2524e0'}, 'Include/longobject.h': {'bytes': 3739, 'sha256': '0567b258763af5e6cb0ecba02135b41b012425a673d4da8c87db1333ac638901'}, 'Include/cpython/longintrepr.h': {'bytes': 4889, 'sha256': 'e2acf37f668089278081539473eeedc8537b848fcd2eb91f53172701c014b9c3'}, 'Include/boolobject.h': {'bytes': 1136, 'sha256': '84289d5b1a1b7ed6c547f4f081fba70e90a9d60dfa2d2b3155c33cdd2af41340'}, 'Include/floatobject.h': {'bytes': 1532, 'sha256': '50d23b4026d270e543d2dd52059bb409569218bf6c3c219dbe836077ee0ca868'}, 'Include/complexobject.h': {'bytes': 728, 'sha256': '9356805a24503256cd8914d7b7700357e01f471c211f9241c81981d89d6c3af8'}, 'Include/rangeobject.h': {'bytes': 630, 'sha256': '36547ab5862e82b09cbed7b786a4cfc86af1dec5a3778c50825bb266c9a6aec9'}, 'Include/memoryobject.h': {'bytes': 1081, 'sha256': 'efb734845a1366d77f6351cbb954c08681d4acfe6a53e41e82dd45fa881e0090'}, 'Include/tupleobject.h': {'bytes': 1615, 'sha256': 'd8de8d64e4b5c466c3bdd04f5664f0eba64a9198b30b5a29409d74a5b5f1def7'}, 'Include/listobject.h': {'bytes': 1782, 'sha256': 'f4cad9a1f48d27a9a7f56702ab0fe785013eb336ea919197600d86a6e54fa5bf'}, 'Include/cpython/odictobject.h': {'bytes': 1311, 'sha256': '97dc6296e890463fc6994247e885df65cd4024dc1b05facfdc984c37d646b919'}, 'Include/enumobject.h': {'bytes': 253, 'sha256': '2244fe250db9995068fe74dce0e23fd70c12b03fd94751d98b773be8f64896b6'}, 'Include/methodobject.h': {'bytes': 5076, 'sha256': '059e19bd8d418c8bf1481e301340f989317ba7b56de94729a19aae26fee3da62'}, 'Include/moduleobject.h': {'bytes': 3559, 'sha256': '5eb48f5d99322d7912a5c6f2b3a974e283c7a6045f79a503d7e09f3ac15b42ec'}, 'Include/cpython/funcobject.h': {'bytes': 7188, 'sha256': '11077e0acca3c026f706327c29d73ef629f5d6bfbd97b2178d672b80f8792497'}, 'Include/cpython/classobject.h': {'bytes': 2245, 'sha256': 'b38a0ecdebeae2a4d28dfe8a5f2833f676d38be9561ca4bdfdf5087bbe2f9332'}, 'Include/fileobject.h': {'bytes': 1650, 'sha256': '133e57cf705cbdaa79a0c115b27e748cc24dedb51ea17b441ff65d05df28a674'}, 'Include/pycapsule.h': {'bytes': 1727, 'sha256': '6929a47483ea5bb1a7b9b490a876b21beefed11061c94b2963b2608b7f542728'}, 'Include/cpython/code.h': {'bytes': 16188, 'sha256': 'd11649dd957102deb64de35f078f061735343f5c9a5c9c429a09722cd6a2931c'}, 'Include/pyframe.h': {'bytes': 551, 'sha256': '58513e7017805ee5c49a329a552f72a6be6d88ce2bcfa344f5130582fa75ecb6'}, 'Include/traceback.h': {'bytes': 585, 'sha256': 'ea59d511687f7f8643c7b8b0996e26f2c92bcc954639c6f98d08f6564b61d06d'}, 'Include/sliceobject.h': {'bytes': 2518, 'sha256': '527719b92e4fa9d5b371c30bc87bc0304ec20099b18c446ad1aa49fd61e5e387'}, 'Include/cpython/cellobject.h': {'bytes': 1076, 'sha256': '844f06178bbce2e9377a46ccc80e2aae85a73750932576a6cc4de934cc508cea'}, 'Include/iterobject.h': {'bytes': 597, 'sha256': '6b16711d2bb6cee55e4288f84142d592eebf07321e32998a5abe2c06deeb77b0'}, 'Include/cpython/genobject.h': {'bytes': 3316, 'sha256': '24f9bd2f19341dc73c7deebca17117ea3a94fd89865c0c6548e1bf5882f51d95'}, 'Include/descrobject.h': {'bytes': 3080, 'sha256': '2956a488f4c4c61341e361dac949cfa4a217e0fbd0097892513b02363c9570a7'}, 'Include/genericaliasobject.h': {'bytes': 334, 'sha256': '0e53a0b18c114be68eccea9ffd1dd577e204b1f0ada4d3aedc8e7ee0c80fc7f8'}, 'Include/warnings.h': {'bytes': 1129, 'sha256': '18fde34b12247460de805fc259ea7f14305fce4779d244c0a7bdc7c73b8f6b51'}, 'Include/weakrefobject.h': {'bytes': 1234, 'sha256': '031b4bc091cf442b4305f7c5ac9713f32101a5e40617f3cb56c632cb7b15fb5b'}, 'Include/structseq.h': {'bytes': 1398, 'sha256': '067f8663a922eb142a3fd12ff18eaa756553bef8a68eaa863f80419dbb8d1ffe'}, 'Include/cpython/picklebufobject.h': {'bytes': 848, 'sha256': '7040fb48462296c903f2f0d24d2b54e0de63cf7512dcf8d3048a0cadf7d94fd0'}, 'Include/cpython/pytime.h': {'bytes': 12402, 'sha256': 'a01714df4c0efdb9e20b26da6d1fc0e5a56619677c60c291f148db5e3cf2faa4'}, 'Include/codecs.h': {'bytes': 7071, 'sha256': '0ca3c6e55e7ff62872b47aeeb7379d784b03ebfc61bbd029b67485fe783baac5'}, 'Include/pythread.h': {'bytes': 4875, 'sha256': 'cd063073710988ea21b54588473542e5f3b2be06f637dc5a028aefd5a7949144'}, 'Include/cpython/context.h': {'bytes': 1965, 'sha256': '9e34d54a789cbf0d78d5ebb126e8384342c08dd81d944d10e3d8f0de0bbba10a'}, 'Include/modsupport.h': {'bytes': 6515, 'sha256': '064d1440d862d08f296c1cbe868e417af12b34f770be515461211f5beade04ff'}, 'Include/compile.h': {'bytes': 448, 'sha256': '1f10c818b29007e6a4446505a1140dd77ca6618ad81e87b502f4e22f4b274406'}, 'Include/pythonrun.h': {'bytes': 1313, 'sha256': '4749ef95e910632a1d04b912c4f1d615c9d10567cbaf52a2ab2c68c7c3a38d94'}, 'Include/pylifecycle.h': {'bytes': 2249, 'sha256': 'd313c5f3fe805606061ea78982ca5d5a9f09e687210c8b0fbcb50db596106691'}, 'Include/ceval.h': {'bytes': 6267, 'sha256': '9531cce1b80e804d46a9ef31bd22605f54d0ae0609dc3470946a4d8d4270af3a'}, 'Include/sysmodule.h': {'bytes': 1729, 'sha256': '09b6f415d4054fee4eb8375a94a724e102bc9a40633d16a437960671b1a9a1b4'}, 'Include/osmodule.h': {'bytes': 291, 'sha256': 'c013935b48f48ca8ce249a4d482c55e3fb6f1cfe786c5a32a57969bb74a779d9'}, 'Include/intrcheck.h': {'bytes': 772, 'sha256': '696fe17618c579a8cbaad9b86175f60d43ea0b9e8aaaa1d65ad256d53dc163c1'}, 'Include/import.h': {'bytes': 3033, 'sha256': '4113e1b6afa760c3decce2bb765835adda19861394974cfe301e1ccb482e2b94'}, 'Include/abstract.h': {'bytes': 32616, 'sha256': '8f0b27427f4e16b4295b2ab1a7bb499bf86748fafbd1959e220c506ed59f774f'}, 'Include/bltinmodule.h': {'bytes': 264, 'sha256': '1b5101b4b85409fd910032713906800bbb83580503036469c2a60ac8e80b8f72'}, 'Include/cpython/pyctype.h': {'bytes': 1387, 'sha256': '10b5ccbc210fd2832e9c34849a3952e8db75f0016add89188358b1da6a8f3dbb'}, 'Include/pystrtod.h': {'bytes': 1557, 'sha256': '8c8e9d1d279216f1c08f0aedac5de49a9b8852a3f838f21e298300e969474ef4'}, 'Include/pystrcmp.h': {'bytes': 436, 'sha256': 'f401d8338fb6ecf5f12768ee95cd09c262f880b2ee522ca344b890dbdcde4c88'}, 'Include/fileutils.h': {'bytes': 507, 'sha256': '51ae1c2ca70a8005206f653121d1ba3247f59421c96399739845d687980e9b01'}, 'Include/cpython/pyfpe.h': {'bytes': 444, 'sha256': 'ea7bfa7d891a0b5372d8b40a57d1b466b7824296e5c3f8d50b1a7cde084429b7'}, 'Include/tracemalloc.h': {'bytes': 2285, 'sha256': '1f40865be2187f8a532d01ac70bfd874848d63ab777ba38251ea1c445f7fced9'}, 'Include/internal/pycore_interp.h': {'bytes': 9086, 'sha256': '23f5d7884f9e0b212fe79879bbcdc5a2c23c22283db38cadbac6f108bf0f1b75'}, 'Include/internal/pycore_global_objects.h': {'bytes': 3035, 'sha256': 'ce857a319514b1682eb054bf4a017974b0bf211092819b25f23e877a228090df'}, 'Include/internal/pycore_runtime.h': {'bytes': 8429, 'sha256': 'd47fe4de4c245e2f90ce73792337565cae6ce95d8e2cd08bcda43ec92832b1ac'}, 'Include/internal/pycore_bitutils.h': {'bytes': 6062, 'sha256': '86628b9cbefe4ff000e1190cd36f37b70a2dad6a4e9231cc2466a84579cc2139'}, 'Include/internal/pycore_gc.h': {'bytes': 7658, 'sha256': 'd0349a94dafb16ec4c05ba5a94d3b9e6cec53fe7b5e0d74216ea31996546f9a3'}, 'Include/internal/pycore_dict_state.h': {'bytes': 1095, 'sha256': '5a15c2bb4020ce4a1d7a4c651e0f98b4becd910f89cd7c4089c80a0419ec4f1c'}, 'Include/cpython/dictobject.h': {'bytes': 4686, 'sha256': '5ac16d73f22038b12bd06904cf02a14bbdd723234d1d899354f1a041e8659505'}, 'Include/cpython/frameobject.h': {'bytes': 1108, 'sha256': 'e1421b58c6a25efb56f423a749c313e3f5392f58cc0c7f4f09b0412217a4a734'}, 'Include/cpython/setobject.h': {'bytes': 2146, 'sha256': 'c965bf093325e20c319af5183a8e5723d4d0b373cb6d1b8781df8c1e588963c0'}, 'Include/exports.h': {'bytes': 1267, 'sha256': 'd02e9937f747660b218062bcdab504b706cad264b4df993f749d9118f2f7b65c'}, 'Include/cpython/pymem.h': {'bytes': 3379, 'sha256': '8a3795a9350b10548e8ad6d37dad69be2abd3870a751e67faa32a19a090608db'}, 'Include/pystats.h': {'bytes': 2741, 'sha256': 'b93db83e29f09ff06b15bf39a21e53de82858ba92cbf48332d1ada1ac028d6f8'}, 'Include/cpython/object.h': {'bytes': 21212, 'sha256': 'f412fd84202ef228e6bf239c9a5a408b8d8623481a15452f8f3331dfc6342134'}, 'Include/cpython/objimpl.h': {'bytes': 3316, 'sha256': 'd99f0cff4297590a49f6616dbf1b04a06c745bed0a280ae35acc56fb3c47f2f3'}, 'Include/cpython/bytearrayobject.h': {'bytes': 1163, 'sha256': 'ae5e099856657f3b8606701df312866eaa88992f6cfd9f8567456e1588efceb1'}, 'Include/cpython/bytesobject.h': {'bytes': 4660, 'sha256': '5ba5010b9aa79f401196740da7c653590f5f4eec6b4f33e99de5412a969fcc8a'}, 'Include/cpython/unicodeobject.h': {'bytes': 35296, 'sha256': 'edfa102633ee0e3cc42652a36912b568ae0cea8bb72360cc97876f170504209c'}, 'Include/cpython/pystate.h': {'bytes': 17228, 'sha256': '11494795dd1d6945fbf8036af5ccf247463e94d405a760924a1c78f78ebfc4ec'}, 'Include/cpython/pyerrors.h': {'bytes': 4276, 'sha256': '1f5070d787263e3aa8845dc90b38aaeb0945be83ef2ba993a40b4af926daacad'}, 'Include/cpython/longobject.h': {'bytes': 4679, 'sha256': 'b443782d6b69a2cfd141ac13ac8b7a8d69e47bfdae9df984de4991b2d248b8b8'}, 'Include/cpython/floatobject.h': {'bytes': 900, 'sha256': 'f1c53f5b87f221db66004b836aa2fc9462aa46c2fbe46b417a8ddc803ce2f585'}, 'Include/cpython/complexobject.h': {'bytes': 1248, 'sha256': 'a4c110008e4d791a4577ce6ebee33bc512ec3e3db918bd2c296f00dd79379fcb'}, 'Include/cpython/memoryobject.h': {'bytes': 2272, 'sha256': '62f414f21611a31f453af7c8326b309aad8f79166087a951844921c50cc84dc7'}, 'Include/cpython/tupleobject.h': {'bytes': 1377, 'sha256': '301c0720038f50d8e9087b38cf1392524abf9e28262b677d841fc1a7e172c3f3'}, 'Include/cpython/listobject.h': {'bytes': 1633, 'sha256': '0ccca44b405add7a8c19d7a5e7701e06ab904cce5c430016b50f7968aef296fe'}, 'Include/cpython/methodobject.h': {'bytes': 2276, 'sha256': '5beb9f3b68ac72efe403a1b0a3fbbb14a5606a49a2840b9c7e9ff243d82d79b9'}, 'Include/cpython/fileobject.h': {'bytes': 818, 'sha256': '16ab872cbe2bb3351ce3090873440903b1460c1d68aed483c70c31edc4140ba2'}, 'Include/cpython/pyframe.h': {'bytes': 1479, 'sha256': '0c7ea17874b967892de6f6623aa426d5eaf267a56e6bbb84b3fefa40e59ec1b8'}, 'Include/cpython/traceback.h': {'bytes': 444, 'sha256': '7898a3c168973e1119fb3b57f144be627c1468082ab0b91d001dd876dd1dbcb6'}, 'Include/cpython/descrobject.h': {'bytes': 1642, 'sha256': 'a1ee0124142fe91204d0c5e85169b55341b2167111a1447e3a8ed50f9bd5a12f'}, 'Include/cpython/warnings.h': {'bytes': 564, 'sha256': 'b758a2e42b0c497ea811464f579603d14fc30b50bd6ebe064d8d2a7df7e2bd76'}, 'Include/cpython/weakrefobject.h': {'bytes': 2032, 'sha256': 'be0ab05169da7efcd13aba0ddc58604a80328d4e60349df6d4efdd1bf363e1a2'}, 'Include/cpython/pythread.h': {'bytes': 1418, 'sha256': '09edccc28c784f8bb85fb77583107ac1fb52fc748946596a03cc36a9296a70dd'}, 'Include/cpython/modsupport.h': {'bytes': 4336, 'sha256': 'a8d08132874d9d642ade82e62e87a510577b7bd4ab0685a90b044cc3b005232d'}, 'Include/cpython/compile.h': {'bytes': 2660, 'sha256': '32d7397c6fa5478feb2a4101641fca6dba3ac77abe4deed5c0f713a6cd6564f5'}, 'Include/cpython/pythonrun.h': {'bytes': 4903, 'sha256': '3290ea064e7450aaf43320a5fcac22d9b36acfab43d1d2c3381ade4b726ced8f'}, 'Include/cpython/pylifecycle.h': {'bytes': 3423, 'sha256': '02505815b8bc3e33fe31a11f4f7f960826aa1dce2c4cee6d62d2a0394470c9bf'}, 'Include/cpython/ceval.h': {'bytes': 1650, 'sha256': 'b08c549971f1006e681267dd8a88481353ce4bd89b9d859f81b72cf9bf867895'}, 'Include/cpython/sysmodule.h': {'bytes': 489, 'sha256': 'd4936db24692cccadb19c11accda260787f95e5658f88cfc752d9a49344ee051'}, 'Include/cpython/import.h': {'bytes': 1623, 'sha256': 'f3a6cb7ea774d2ffcb64c834dffaf008e8f9f3f10b23600d5522d82176cb241c'}, 'Include/cpython/abstract.h': {'bytes': 7870, 'sha256': '07d8b3b9c7db77e30adef4c4d9c7a4453b8eb1f48341ed5394bd5eebe239c9fd'}, 'Include/cpython/fileutils.h': {'bytes': 232, 'sha256': 'd7a2f703c6fba2efabd0b1cc916ad36074363a27a000987cfad17e21f04d44f1'}, 'Include/internal/pycore_ast_state.h': {'bytes': 6749, 'sha256': '1d76a7b5207c653a86dec97aab5ba1fcc5c75e94333662792a692cb68e5b26c6'}, 'Include/internal/pycore_atexit.h': {'bytes': 1149, 'sha256': '8c5c88b8452894cf8a5f243ceb9021060f0fe8f5689cbc3e705c19c5edc0798a'}, 'Include/internal/pycore_atomic.h': {'bytes': 16979, 'sha256': '95e7118e799ad3faafc8e58a29b2d1f1a4bb94e1aac3273e042f379f8e12d4e6'}, 'Include/internal/pycore_ceval_state.h': {'bytes': 2744, 'sha256': 'f29e3d6dcac96b0067a17845df8483013230805db10c6f3c5ecd02b9134640e7'}, 'Include/internal/pycore_context.h': {'bytes': 1301, 'sha256': '974d6bafbe0164d60dd1bc4f09b5eac9bcc9e2d9066924ba2a2ba6d502f115b5'}, 'Include/internal/pycore_dtoa.h': {'bytes': 1615, 'sha256': 'c83a4aa972a4845cdf36abdac4769ea30e877aae1997fc4999d020bc3e183c1e'}, 'Include/internal/pycore_exceptions.h': {'bytes': 842, 'sha256': '4590af737d53afcbd7d559434190d2d8ff4f5cd0e923837721aea5ebb000ef68'}, 'Include/internal/pycore_floatobject.h': {'bytes': 1578, 'sha256': '021fef24c4b7e7390c793af7ccf12ddd94b1871e27d26997b37eb3093d5380b5'}, 'Include/internal/pycore_genobject.h': {'bytes': 1186, 'sha256': 'a940f41da1e8d9d12c9c438ea0b4f24e72abc494447bcecd9423b76f54e3402a'}, 'Include/internal/pycore_import.h': {'bytes': 6358, 'sha256': 'e5b179692f05707e7fb182b908ed46f9a75f4a751b20501a74de2a440c387e1d'}, 'Include/internal/pycore_list.h': {'bytes': 1980, 'sha256': '470a62bb98b383b85ec738a6577424e6cdd51ae235f4e5ea06c5afdedb6e1652'}, 'Include/internal/pycore_object_state.h': {'bytes': 1016, 'sha256': '572c053ce17edd206c776e7138965fa1f7485127e05c68ce9ad0232e3a821692'}, 'Include/internal/pycore_obmalloc.h': {'bytes': 27284, 'sha256': 'd8738004c5dbb5520f401919ed55181a48a9e64a3b51930309fc99fb9d219576'}, 'Include/internal/pycore_unicodeobject.h': {'bytes': 2657, 'sha256': 'e171f3303be9a161db66cb8ab942ebe75976a5cc815a633ac6c38dba31d76d60'}, 'Include/internal/pycore_warnings.h': {'bytes': 740, 'sha256': '3229b207245cb9442f09991df7084c8e4cb87cb073a14a2d520bd92634371fcb'}, 'Include/internal/pycore_hashtable.h': {'bytes': 4286, 'sha256': '690488a7e50ad743e1bb685702fbcfac866ace89d2417a247c1171afdc222261'}, 'Include/internal/pycore_global_strings.h': {'bytes': 25438, 'sha256': 'da08d01f47b89ef7bc83893ba7b32a0b690fd3ac5a5922dffa7a649ceb900d91'}, 'Include/internal/pycore_hamt.h': {'bytes': 3742, 'sha256': '074b31c2f5701cac43d8dc3e4ede40b2befc6dddfcaa2862cfc8f76234c30ae8'}, 'Include/internal/pycore_faulthandler.h': {'bytes': 2220, 'sha256': '6444dce1924eae011d27385183ad1a5de6908501cedce2e1531abd834c68cae7'}, 'Include/internal/pycore_parser.h': {'bytes': 1358, 'sha256': '91189a016020eb7de0b1ab8ae38145dbec6b561ae5c75cea15980cb76255ba5b'}, 'Include/internal/pycore_pyhash.h': {'bytes': 709, 'sha256': '7c631d06afad90fa9c2ddc8dc04b7c2855ee5aa6e7ece0b22d0a966a702abf73'}, 'Include/internal/pycore_pythread.h': {'bytes': 2075, 'sha256': 'ba04eed4d18d6110982cc58800fda11f3899c61fed644ff9e52a4adedb7b750a'}, 'Include/internal/pycore_signal.h': {'bytes': 2611, 'sha256': '186835a8702a10bb1f3f63185d50874f24885716707717f620d3ffd0a2039679'}, 'Include/internal/pycore_time.h': {'bytes': 388, 'sha256': '6838118a537e71edaf76290da15cbf2da19499df1ee4e30b15f35bb4b9257b70'}, 'Include/internal/pycore_tracemalloc.h': {'bytes': 3075, 'sha256': '61ac9b846ae579c667d20034c9c4004a07ab3ff039848ddeeec8d9c39ff1331a'}, 'Include/cpython/pthread_stubs.h': {'bytes': 3505, 'sha256': '0f3108e0430ee937098c86352d2ced6e3ec7f5cb5bc7e06eebee58cf779fcd89'}, 'Include/dynamic_annotations.h': {'bytes': 22471, 'sha256': '3e4366f7d082835049730358d277a5ad7a60e16d1601f5622f0a045a37c152ac'}, 'Include/internal/pycore_gil.h': {'bytes': 1565, 'sha256': 'cf455aacd5651e5b43547ebe69bb324eab84238d92665df53c1df32434bd0d9b'}, 'Include/internal/pycore_pymath.h': {'bytes': 8600, 'sha256': '6dd3ea0f9a84bfa3a2eb0a2b7fa1af1dc8aadad3e74305e13f194a1586815376'}, 'Include/internal/pycore_fileutils.h': {'bytes': 7910, 'sha256': 'ea9cac693c87dc049f199cecd2844592ee08d0283dc0b059c4caab517932af73'}, 'Include/internal/pycore_ucnhash.h': {'bytes': 898, 'sha256': '6d9077e875703e5db7daf293a6c7ea3d43d1ee84dec137a950f17a26e9348eb5'}, 'Include/internal/pycore_ast.h': {'bytes': 31288, 'sha256': '064b6778fa758fb2580fb8770f77dd0d1eb19323df0e345373788c75754910cf'}, 'Include/internal/pycore_pyarena.h': {'bytes': 2733, 'sha256': 'd4f4e513bae78ff985f51ca48fb7d1a4d57055c59393a1eb661e55e6ec3ba61f'}, 'Include/internal/pycore_condvar.h': {'bytes': 2909, 'sha256': '97c4cb5f0a32cd967dd5d54d4ddaed9323c7c2439cd6ffbba9f7d48064b97b26'}, 'Include/internal/pycore_asdl.h': {'bytes': 3035, 'sha256': 'b29dace0f84849c4a24bc3745523a36911cd192bad7ec6fb48aba8facff51d3e'}}
 need(type(files) is dict and all(type(k) is str for k in files) and set(files)==set(pins),'DECREF-FAST-SOURCE-SET')
 need(all(type(b) is bytes for b in files.values()),'DECREF-FAST-SOURCE-BYTE-TYPE')
 lines={n:b.decode('utf-8').splitlines() for n,b in files.items()}
 def require_line(name,number,text):need(lines[name][number-1].strip()==text,'DECREF-FAST-DEFINING-SOURCE:'+name+':'+str(number))
 for n,text in [(49,'#if !defined(Py_DEBUG) && !defined(Py_TRACE_REFS)'),(56,'#undef Py_DECREF')]:require_line('Python/ceval.c',n,text)
 # Exact macro tokens are independently read from the defining body, not a catalogue.
 body='\n'.join(lines['Python/ceval.c'][56:68])
 expected='''#define Py_DECREF(arg) \\
    do { \\
        PyObject *op = _PyObject_CAST(arg); \\
        if (_Py_IsImmortal(op)) { \\
            break; \\
        } \\
        _Py_DECREF_STAT_INC(); \\
        if (--op->ob_refcnt == 0) { \\
            destructor dealloc = Py_TYPE(op)->tp_dealloc; \\
            (*dealloc)(op); \\
        } \\
    } while (0)'''
 need(body==expected,'DECREF-FAST-LOCAL-MACRO-BODY')
 for number,text in [(3,'#define _PY_INTERPRETER'),(45,'#if !defined(Py_BUILD_CORE)'),(603,'#include "ceval_macros.h"'),(663,'#include "opcode_targets.h"'),(849,'#include "generated_cases.c.h"')]:require_line('Python/ceval.c',number,text)
 for number,text in [(3496,'TARGET(BEFORE_WITH) {'),(3528,'#line 2515 "Python/bytecodes.c"'),(3529,'res = _PyObject_CallNoArgs(enter);'),(3530,'Py_DECREF(enter);'),(3531,'if (res == NULL) {')]:require_line('Python/generated_cases.c.h',number,text)
 for number,text in [(2515,'res = _PyObject_CallNoArgs(enter);'),(2516,'Py_DECREF(enter);'),(2517,'if (res == NULL) {')]:require_line('Python/bytecodes.c',number,text)
 for number,text in [(1615,'/* #undef Py_DEBUG */'),(1625,'/* #undef Py_STATS */'),(1631,'/* #undef Py_TRACE_REFS */'),(1688,'#define SIZEOF_VOID_P 8'),(1814,'/* #undef WITH_DTRACE */')]:require_line('Include/pyconfig.h',number,text)
 require_line('Include/object.h',241,'#if SIZEOF_VOID_P > 4')
 require_line('Include/object.h',242,'return _Py_CAST(PY_INT32_T, op->ob_refcnt) < 0;')
 require_line('Include/pystats.h',103,'#define _Py_DECREF_STAT_INC() ((void)0)')
 # Pins cover the entire conservatively recovered quoted-include closure, not only excerpts.
 for n,pin in pins.items():need({'bytes':len(files[n]),'sha256':digest(files[n])}==pin,'DECREF-FAST-SOURCE-IDENTITY:'+n)
 def site(n,line):return {'file':n,'line':line,'expression':lines[n][line-1].strip().rstrip('\\').rstrip(),'identity':copy.deepcopy(pins[n]),'revision':'2abcf904b8dac8c999d2b3aac76681abb333798a'}
 return {'revision':'2abcf904b8dac8c999d2b3aac76681abb333798a','source_identities':copy.deepcopy(pins),
  'override_guard':site('Python/ceval.c',49),'macro_definition':site('Python/ceval.c',57),'operand_binding':site('Python/ceval.c',59),'immortal_test':site('Python/ceval.c',60),
  'immortal_break':site('Python/ceval.c',61),'statistics':site('Python/ceval.c',63),'decrement_zero_test':site('Python/ceval.c',64),
  'destructor_select':site('Python/ceval.c',65),'destructor_call':site('Python/ceval.c',66),'macro_end':site('Python/ceval.c',68),
  'selected_operation':site('Python/bytecodes.c',2516),'generated_operation':site('Python/generated_cases.c.h',3530),'excluded_test':site('Python/bytecodes.c',2517),
  'immortal_predicate':site('Include/object.h',242),'stats_noop':site('Include/pystats.h',103),'interpretation':'local ceval do/while macro; not ordinary header inline function; source consistency is not binary-build provenance'}

def decref_fast_envelope():
 return {'configuration':{'Py_BUILD_CORE':True,'_PY_INTERPRETER':True,'Py_DEBUG':False,'Py_TRACE_REFS':False,'Py_STATS':False,'Py_LIMITED_API':False,'Py_REF_DEBUG':False,'WITH_DTRACE':False,'SIZEOF_VOID_P':8,'platform':'Linux-x86_64','__APPLE__':False},
  'configuration_status':'explicit SOURCE-ONLY envelope consistent with retained defaults, not observed historical effective defines',
  'external_macro_and_include_overrides_absent':'explicit conditional premise','standard_C_headers_do_not_redefine_relevant_CPython_names':'explicit conditional premise',
  'valid_selected_non_NULL_PyObject_pointer':'explicit conditional premise','defined_C_evaluation_and_integer_semantics':'explicit conditional premise',
  'enter_storage_and_branch_state_continuity':'explicit conditional premise; no intervening mutation during selected branch',
  'branch_state_evidence':'conditional state premise, never inferred from res, lookup success or observed runtime values',
  'qualified_binary_mapping':'UNESTABLISHED','runtime_object_state':'UNOBSERVED'}

def decref_fast_catalogue(parent,files):
 status_exact_tree(parent,'DECREF-FAST-PARENT-CATALOGUE-TYPE');s=decref_fast_sources(files)
 need(parent['format']=='I164-ENTER-DECREF-ATTEMPT-STATIC-1','DECREF-FAST-PARENT-CATALOGUE')
 op=parent['source']['operation'];need(op['file']=='Python/bytecodes.c' and op['line']==2516 and op['expression']=='Py_DECREF(enter);','DECREF-FAST-PARENT-BOUNDARY')
 # Statement source identity is also tied to the exact predecessor input, not a same-spelling occurrence.
 need(op['source']['sha256']==s['source_identities']['Python/bytecodes.c']['sha256'],'DECREF-FAST-PARENT-SOURCE')
 front=['interruption','process-termination','unobserved']
 specs=[('continuation','selected_operation','normal',['normal','raise','catchable-interruption','process-termination','unobserved']),
        ('operand','operand_binding','bound',['bound',*front]),('immortal-test','immortal_test',None,['true','false',*front]),
        ('break','immortal_break','taken',['taken',*front]),('statistics','statistics','no-op',['no-op',*front]),
        ('decrement-zero-test','decrement_zero_test','nonzero',['nonzero',*front]),('macro-end','macro_end','completed',['completed',*front])]
 steps=[{'id':'decref-fast:'+name,'source':copy.deepcopy(s[origin]),'normal':normal,'allowed':allowed} for name,origin,normal,allowed in specs]
 # Branch order follows the exact parsed body positions; break bypasses the tail of do/while.
 need(s['operand_binding']['line']<s['immortal_test']['line']<s['immortal_break']['line']<s['statistics']['line']<s['decrement_zero_test']['line']<s['destructor_call']['line']<s['macro_end']['line'],'DECREF-FAST-SOURCE-ORDER')
 orders={'immortal':['continuation','operand','immortal-test','break','macro-end'],
         'non-immortal-positive-gt-one':['continuation','operand','immortal-test','statistics','decrement-zero-test','macro-end']}
 return {'format':'I164-DECREF-FAST-COMPLETION-STATIC-1','source':s,'enter_decref_catalogue':copy.deepcopy(parent),'parent_catalogue_sha256':digest(enc(parent)),
  'configuration_and_C_premises':decref_fast_envelope(),'steps':steps,'branch_orders':{k:['decref-fast:'+x for x in v] for k,v in orders.items()},
  'branch_guards':{'immortal':{'immortal_predicate':True,'starting_count':'UNOBSERVED; not needed for immortal branch'},'non-immortal-positive-gt-one':{'immortal_predicate':False,'starting_count':'valid positive count > 1; symbolic n, no concrete value'}},
  'zero_count_route':{'completion':'UNRESOLVED','direct_selected_tp_dealloc':copy.deepcopy(s['destructor_call']),'not_via_header_Py_Dealloc':True,'accepted_as_fast_branch':False},
  'guard_branches':{'contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'prefixes':copy.deepcopy(parent['guard_branches']['prefixes']),'origins':copy.deepcopy(parent['guard_branches']['origins']),'continuity':['explicit conditional premise','UNESTABLISHED'],'branch_state':['immortal','non-immortal-positive-gt-one','UNESTABLISHED']},
  'declarations':[{'id':x['id'],'source':copy.deepcopy(x['source']),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for x in steps],
  'res_non_NULL_guard':False,'res_classes':copy.deepcopy(parent['source']['res_classes']),'preserved_relations':['enter_decref_attempt_correspondence',*parent['preserved_relations']],
  'stop':'conditional fast macro completion, or first nonnormal frontier; before bytecodes.c:2517 result test','runtime_chain':None,'actual_admission':False}

def compile_decref_fast(launcher,bytecodes,typeobject,r1,lookup,enter,returned,parent,files):
 validate_enter_decref(launcher,bytecodes,typeobject,r1,lookup,enter,returned,parent)
 need(type(bytecodes) is bytes and bytecodes==files['Python/bytecodes.c'],'DECREF-FAST-CALLSITE-BYTES')
 return decref_fast_catalogue(parent,files)

def validate_decref_fast(launcher,bytecodes,typeobject,r1,lookup,enter,returned,parent,files,submitted):
 status_exact_tree(submitted,'DECREF-FAST-CATALOGUE-TYPE');status_typed_same(submitted,compile_decref_fast(launcher,bytecodes,typeobject,r1,lookup,enter,returned,parent,files),'DECREF-FAST-CATALOGUE-SOURCE');return True

def decref_fast_binding(cat,parent,anchor,continuity,branch,envelope,files):
 for v in (cat,parent,anchor,continuity,branch,envelope):status_exact_tree(v,'DECREF-FAST-BINDING-TYPE')
 status_typed_same(cat,decref_fast_catalogue(cat['enter_decref_catalogue'],files),'DECREF-FAST-INDEPENDENT-CATALOGUE')
 status_typed_same(envelope,decref_fast_envelope(),'DECREF-FAST-ENVELOPE')
 need(type(continuity) is str and continuity in ('explicit conditional premise','UNESTABLISHED'),'DECREF-FAST-CONTINUITY')
 need(type(branch) is str and branch in ('immortal','non-immortal-positive-gt-one','UNESTABLISHED'),'DECREF-FAST-BRANCH-UNSUPPORTED')
 need(parent['kind']=='CONSTRUCTED-ENTER-DECREF-ATTEMPT' and parent['completion']=='enter-decref-attempt' and parent['post_call_decref_attempt_established_in_model'] is True,'DECREF-FAST-PARENT-ATTEMPT')
 pc={'scope':copy.deepcopy(parent['scope']),'anchor':copy.deepcopy(parent['instance_anchor']),'parent_result':copy.deepcopy(parent['predecessor_projection']),'binding':copy.deepcopy(parent['binding']),'outcomes':[{'stage':e['stage'],'outcome':e['outcome']} for e in parent['events']]}
 validate_enter_decref_projection(cat['enter_decref_catalogue'],pc,pc,parent)
 need(parent['binding']['continuity']=='explicit conditional premise' and parent['decref_completion_established'] is False and parent['result_test_established'] is False,'DECREF-FAST-PARENT-STOP')
 status_typed_same(pc['outcomes'],[{'stage':'enter-decref:continuation','outcome':'normal'},{'stage':'enter-decref:attempt','outcome':'attempted'}],'DECREF-FAST-EXACT-PARENT-ATTEMPT')
 scope=parent['scope'];status_typed_same(parent['instance_anchor'],anchor,'DECREF-FAST-ANCHOR');status_typed_same(scope['instance'],anchor['instance'],'DECREF-FAST-INSTANCE')
 need(scope['context'] in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO') and scope['context']==anchor['context'] and scope['acquisition']==anchor['record']['acquisition'],'DECREF-FAST-CONTEXT-ACQUISITION')
 op=parent['decref_operation'];status_typed_same(op['operand_role'],parent['binding']['method_results']['__enter__'],'DECREF-FAST-ENTER-ROLE')
 return {'scope':copy.deepcopy(scope),'anchor':copy.deepcopy(anchor),'selected_attempt':copy.deepcopy(parent['events'][-1]),'operation':copy.deepcopy(op),
  'enter_role':copy.deepcopy(op['operand_role']),'exit_role':copy.deepcopy(parent['binding']['exit_role']),'res_value_role':copy.deepcopy(parent['res_value_role']),
  'references':copy.deepcopy(parent['binding']['references']),'helper_invocation':copy.deepcopy(parent['binding']['helper_invocation']),
  'original_constructor_error':copy.deepcopy(parent['original_error_pending_in_outer_handler']),'pending_error_before_macro':copy.deepcopy(parent['last_pending_error_in_model']),
  'details_role':copy.deepcopy(parent['binding']['details_role']),'cleanup_list':copy.deepcopy(parent['binding']['cleanup_list']),
  'continuity':continuity,'envelope':copy.deepcopy(envelope),'branch':branch,
  'state_premise':{'scope':copy.deepcopy(scope),'enter_role':copy.deepcopy(op['operand_role']),'guard':copy.deepcopy(cat['branch_guards'].get(branch)),'concrete_count':None,'derived_from_res':False,'runtime_observation':False},
  'physical_identity':None,'qualified_binary_correspondence':False}

def decref_fast_projection(cat,case,validated,files):
 for v in (cat,case,validated):status_exact_tree(v,'DECREF-FAST-EXACT-TYPE')
 keys={'scope','anchor','parent_result','binding','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'DECREF-FAST-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'DECREF-FAST-VALIDATED:'+k)
 p=case['parent_result'];b=case['binding'];scope=case['scope'];oo=case['outcomes']
 status_typed_same(scope,p['scope'],'DECREF-FAST-SCOPE')
 status_typed_same(b,decref_fast_binding(cat,p,case['anchor'],b['continuity'],b['branch'],b['envelope'],files),'DECREF-FAST-EXPECTED-BINDING')
 need(type(oo) is list and bool(oo),'DECREF-FAST-OUTCOMES')
 unresolved=b['continuity']=='UNESTABLISHED' or b['branch']=='UNESTABLISHED'
 if unresolved:status_typed_same(oo,[{'stage':'decref-fast:continuation','outcome':'unobserved'}],'DECREF-FAST-UNESTABLISHED-PREMISE')
 order=['decref-fast:continuation'] if unresolved else cat['branch_orders'][b['branch']]
 steps={x['id']:x for x in cat['steps']};events=[];replacement=None;last=None;completed=False;decrement=False;predicate=None;break_taken=False
 for i,name in enumerate(order):
  need(i<len(oo),'DECREF-FAST-MISSING-STEP');row=oo[i];step=steps[name]
  need(type(row) is dict and set(row)=={'stage','outcome'} and type(row['stage']) is str and row['stage']==name,'DECREF-FAST-ORDER')
  last=row['outcome'];need(type(last) is str and last in step['allowed'],'DECREF-FAST-OUTCOME')
  normal=('true' if b['branch']=='immortal' else 'false') if name=='decref-fast:immortal-test' else step['normal']
  event={'id':b['selected_attempt']['id']+'/'+name,'stage':name,'source':copy.deepcopy(step['source']),'generated_operation':copy.deepcopy(cat['source']['generated_operation']),
   'selected_attempt':b['selected_attempt']['id'],'scope':copy.deepcopy(scope),'owner':copy.deepcopy(b['references']['owner']),'token':copy.deepcopy(b['references']['token']),
   'enter_role':copy.deepcopy(b['enter_role']),'exit_role':copy.deepcopy(b['exit_role']),'res_value_role':copy.deepcopy(b['res_value_role']),'outcome':last,'runtime_observation':False}
  events.append(event)
  if last!=normal:
   need(last not in ('true','false'),'DECREF-FAST-GUARD-CONTRADICTION')
   if last in ('raise','catchable-interruption'):
    need(name=='decref-fast:continuation','DECREF-FAST-NO-INVENTED-C-EXCEPTION')
    replacement={'role':'conditional-post-attempt-continuation-error','reference':event['id']+'/error','scope':copy.deepcopy(scope),'kind':last,
     'origin':'explicit interval frontier before macro-body entry; not a Python exception asserted inside a C primitive','exact_type':None,'exact_value':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_observation':False}
   break
  if name=='decref-fast:immortal-test':predicate=(last=='true')
  if name=='decref-fast:break':break_taken=True
  if name=='decref-fast:decrement-zero-test':decrement=True
  if name=='decref-fast:macro-end':completed=True
 need(len(oo)==len(events),'DECREF-FAST-UNREACHED-STEPS')
 uncertain=last in ('interruption','process-termination','unobserved')
 out=copy.deepcopy(p);out.update({'kind':'CONSTRUCTED-DECREF-FAST-COMPLETION','binding':copy.deepcopy(b),'predecessor_projection':copy.deepcopy(p),'events':events,
  'completion':('immortal-macro-complete' if b['branch']=='immortal' else 'nonzero-macro-complete') if completed else last+'-frontier',
  'conditional_fast_completion_in_model':completed,'conditional_macro_body_entered_in_model':any(e['stage']=='decref-fast:operand' and e['outcome']=='bound' for e in events),
  'new_model_claims':{'immortal_predicate_result':predicate,'break_from_do_while_in_model':break_taken,'interpreter_return_established':False,
   'decrement_and_nonzero_test_in_model':decrement,'count_relation':{'before':'n','premise':'valid positive n > 1 and non-immortal','after':'n - 1','nonzero':True,'same_selected_enter_role':copy.deepcopy(b['enter_role']),'selected_attempt':b['selected_attempt']['id'],'before_symbol':b['selected_attempt']['id']+'/conditional-count-before','after_symbol':b['selected_attempt']['id']+'/conditional-count-after','concrete_values':None} if decrement else None,
   'macro_completion_in_model':completed,'destructor_invocation_in_model':False,'destructor_skipped_by_completed_fast_branch':completed,'zero_count_completion':False},
  'legacy_attempt_flags_scope':'Unchanged predecessor-stage/unqualified flags are not new physical-effect claims; new conditional model facts are confined to new_model_claims and conditional_fast_completion_in_model',
  'runtime_macro_arrival':None,'runtime_decrement_completion':None,'physical_reference_count_effects':None,'qualified_binary_correspondence':False,
  'decref_effects_established':False,'reference_count_change_established':False,'physical_release_established':False,'finalization_established':False,'decref_callback_execution_established':False,
  'result_test_established':False,'result_error_routing_established':False,'context_manager_entry_established':False,'f_binding_established':False,
  'replacement_error_in_model':copy.deepcopy(replacement if replacement is not None else p['replacement_error_in_model']),
  'last_pending_error_in_model':copy.deepcopy(replacement if replacement is not None else p['last_pending_error_in_model']),
  'last_acknowledged_pending_error_before_macro':copy.deepcopy(p['last_pending_error_in_model']),
  'pending_error_at_frontier':'UNESTABLISHED' if uncertain else 'conditional retained lineage; helper error indicator remains UNKNOWN',
  'terminal_python_exception_in_model':None if uncertain else True,'C_primitive_python_exception_established':False,'Python_unwind_established':False,
  'current_partial_effects':'UNKNOWN; inherited effects and any incomplete macro stage remain unresolved; modeled fast completion does not establish physical effects',
  'prior_acknowledged_partial_effects':copy.deepcopy(p['current_partial_effects']),'stop':cat['stop']})
 return out

def validate_decref_fast_projection(cat,case,validated,submitted,files):
 status_exact_tree(submitted,'DECREF-FAST-OUTPUT-TYPE');status_typed_same(submitted,decref_fast_projection(cat,case,validated,files),'DECREF-FAST-OUTPUT-CORRESPONDENCE');return True

# I164-RES-NULL-TEST-1. Full 505,497-byte reviewed fast-completion prefix unchanged.
def res_null_sources(files):
 s=decref_fast_sources(files)
 specs=[('Python/bytecodes.c',2515,'res = _PyObject_CallNoArgs(enter);'),('Python/bytecodes.c',2516,'Py_DECREF(enter);'),('Python/bytecodes.c',2517,'if (res == NULL) {'),('Python/bytecodes.c',2518,'Py_DECREF(exit);'),('Python/bytecodes.c',2519,'ERROR_IF(true, error);'),('Python/generated_cases.c.h',3499,'PyObject *res;'),('Python/generated_cases.c.h',3528,'#line 2515 "Python/bytecodes.c"'),('Python/generated_cases.c.h',3529,'res = _PyObject_CallNoArgs(enter);'),('Python/generated_cases.c.h',3530,'Py_DECREF(enter);'),('Python/generated_cases.c.h',3531,'if (res == NULL) {'),('Python/generated_cases.c.h',3532,'Py_DECREF(exit);'),('Python/generated_cases.c.h',3533,'if (true) goto pop_1_error;'),('Python/generated_cases.c.h',3536,'STACK_GROW(1);'),('Python/generated_cases.c.h',3537,'stack_pointer[-1] = res;'),('Python/generated_cases.c.h',3539,'DISPATCH();')]
 sites={}
 for name,line,text in specs:
  need(files[name].decode().splitlines()[line-1].strip()==text,'RES-NULL-DEFINING-SOURCE:'+name+':'+str(line))
  sites[(name,line)]={'file':name,'line':line,'expression':text,'identity':copy.deepcopy(s['source_identities'][name]),'revision':s['revision']}
 return {'revision':s['revision'],'definition_identities':copy.deepcopy(s['source_identities']),
  'assignment':sites[('Python/bytecodes.c',2515)],'previous_operation':sites[('Python/bytecodes.c',2516)],'test':sites[('Python/bytecodes.c',2517)],
  'generated_test':sites[('Python/generated_cases.c.h',3531)],'storage_declaration':sites[('Python/generated_cases.c.h',3499)],
  'true_stop_before':sites[('Python/bytecodes.c',2518)],'generated_true_stop_before':sites[('Python/generated_cases.c.h',3532)],
  'false_stop_before':sites[('Python/generated_cases.c.h',3536)],
  'comparison':'C pointer equality against the null pointer constant; not Python truth testing, not a check of concrete_value placeholders',
  'C_semantics':'explicit defined-C pointer/null comparison premise within retained source envelope; no historical compiler or binary attestation'}

def res_null_catalogue(parent,files):
 status_exact_tree(parent,'RES-NULL-PARENT-CATALOGUE-TYPE')
 need(type(parent) is dict and parent.get('format')=='I164-DECREF-FAST-COMPLETION-STATIC-1','RES-NULL-PARENT-CATALOGUE')
 status_typed_same(parent,decref_fast_catalogue(parent['enter_decref_catalogue'],files),'RES-NULL-PARENT-INDEPENDENT-SOURCE')
 s=res_null_sources(files)
 steps=[{'id':'res-null:continuation','source':copy.deepcopy(s['test']),'normal':'normal','allowed':['normal','raise','catchable-interruption','process-termination','unobserved']},
        {'id':'res-null:comparison','source':copy.deepcopy(s['test']),'normal':'source-derived pointer comparison','allowed':['true','false','interruption','process-termination','unobserved']}]
 return {'format':'I164-RES-NULL-TEST-STATIC-1','source':s,'fast_catalogue':copy.deepcopy(parent),'parent_catalogue_sha256':digest(enc(parent)),
  'steps':steps,'order':[x['id'] for x in steps],
  'guard_branches':{'contexts':copy.deepcopy(parent['guard_branches']['contexts']),'prefixes':copy.deepcopy(parent['guard_branches']['prefixes']),'origins':copy.deepcopy(parent['guard_branches']['origins']),
   'fast_branches':['immortal','non-immortal-positive-gt-one'],'continuation':['explicit conditional premise','UNESTABLISHED'],'res_storage_continuity':['explicit conditional premise','UNESTABLISHED']},
  'required_predecessor_facts':['conditional_fast_completion_in_model','helper_c_return_completed_in_model','res_assignment_established'],
  'result_by_completed_C_class':{'C-NULL':True,'non-NULL/opaque':False,'non-NULL/Python-None':False},
  'missing_return_or_assignment':'No completed test claim; missing or contradictory predecessor evidence fails binding rather than becoming C NULL.',
  'declarations':[{'id':x['id'],'source':copy.deepcopy(x['source']),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for x in steps],
  'preserved_relations':['decref_fast_completion_correspondence',*parent['preserved_relations']],
  'stop':'selected C pointer comparison outcome or first nonnormal frontier; before Py_DECREF(exit), error routing, stack operations or dispatch',
  'runtime_chain':None,'actual_admission':False}

def compile_res_null(launcher,bytecodes,typeobject,r1,lookup,enter,returned,decref,fast,files):
 validate_decref_fast(launcher,bytecodes,typeobject,r1,lookup,enter,returned,decref,files,fast)
 return res_null_catalogue(fast,files)

def validate_res_null(launcher,bytecodes,typeobject,r1,lookup,enter,returned,decref,fast,files,submitted):
 status_exact_tree(submitted,'RES-NULL-CATALOGUE-TYPE')
 status_typed_same(submitted,compile_res_null(launcher,bytecodes,typeobject,r1,lookup,enter,returned,decref,fast,files),'RES-NULL-CATALOGUE-SOURCE');return True

def res_null_binding(cat,parent,anchor,continuation,storage_continuity,files):
 for v in (cat,parent,anchor,continuation,storage_continuity):status_exact_tree(v,'RES-NULL-BINDING-TYPE')
 status_typed_same(cat,res_null_catalogue(cat['fast_catalogue'],files),'RES-NULL-INDEPENDENT-CATALOGUE')
 need(type(parent) is dict and parent.get('kind')=='CONSTRUCTED-DECREF-FAST-COMPLETION','RES-NULL-PARENT-KIND')
 for k in ('conditional_fast_completion_in_model','helper_c_return_completed_in_model','res_assignment_established'):
  need(parent.get(k) is True,'RES-NULL-MISSING-PREDECESSOR:'+k)
 need(parent.get('res_assignment') is not None and parent.get('res_value_role') is not None,'RES-NULL-MISSING-ASSIGNMENT-VALUE')
 need(type(continuation) is str and continuation in ('explicit conditional premise','UNESTABLISHED'),'RES-NULL-CONTINUATION')
 need(type(storage_continuity) is str and storage_continuity in ('explicit conditional premise','UNESTABLISHED'),'RES-NULL-STORAGE-CONTINUITY')
 p=parent['predecessor_projection']
 pc={'scope':copy.deepcopy(parent['scope']),'anchor':copy.deepcopy(parent['instance_anchor']),'parent_result':copy.deepcopy(p),'binding':copy.deepcopy(parent['binding']),'outcomes':[{'stage':e['stage'],'outcome':e['outcome']} for e in parent['events']]}
 validate_decref_fast_projection(cat['fast_catalogue'],pc,pc,parent,files)
 need(parent['completion'] in ('immortal-macro-complete','nonzero-macro-complete') and parent['events'][-1]['stage']=='decref-fast:macro-end' and parent['events'][-1]['outcome']=='completed','RES-NULL-PARENT-COMPLETION')
 need(parent['result_test_established'] is False,'RES-NULL-PARENT-STOP')
 scope=parent['scope'];status_typed_same(parent['instance_anchor'],anchor,'RES-NULL-ANCHOR')
 status_typed_same(scope['instance'],anchor['instance'],'RES-NULL-INSTANCE')
 need(scope['context']==anchor['context'] and scope['context'] in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO') and scope['acquisition']==anchor['record']['acquisition'],'RES-NULL-CONTEXT-ACQUISITION')
 value=parent['res_value_role'];assignment=parent['res_assignment']
 need(type(value) is dict and type(value.get('C_NULL')) is bool,'RES-NULL-VALUE-CLASS')
 need(assignment['target']=='res' and assignment['source']['line']==2515,'RES-NULL-ASSIGNMENT-TARGET')
 status_typed_same(assignment['value'],value,'RES-NULL-ASSIGNED-VALUE')
 status_typed_same(value['scope'],scope,'RES-NULL-VALUE-SCOPE')
 need(assignment['from_return_occurrence']==value['return_occurrence'],'RES-NULL-RETURN-LINK')
 if value['C_NULL']:
  need(value['kind']=='C-NULL' and value['python_value_class'] is None and value['python_object_role'] is None,'RES-NULL-C-NULL')
 else:need(value['kind']=='SYMBOLIC-PYOBJECT' and value['python_value_class'] in ('opaque','Python-None') and type(value['python_object_role']) is str,'RES-NULL-NONNULL')
 return {'scope':copy.deepcopy(scope),'anchor':copy.deepcopy(anchor),'selected_fast_completion':copy.deepcopy(parent['events'][-1]),
  'selected_attempt':copy.deepcopy(parent['binding']['selected_attempt']),'fast_branch':parent['binding']['branch'],
  'assignment':copy.deepcopy(assignment),'res_value_role':copy.deepcopy(value),
  'res_storage_role':{'role':'C local res storage','symbol':scope['invocation']+'/BEFORE_WITH/res-storage','scope':copy.deepcopy(scope),'declaration':copy.deepcopy(cat['source']['storage_declaration']),'assignment_occurrence':assignment['occurrence'],'runtime_address':None},
  'enter_role':copy.deepcopy(parent['binding']['enter_role']),'exit_role':copy.deepcopy(parent['binding']['exit_role']),
  'references':copy.deepcopy(parent['binding']['references']),'helper_invocation':copy.deepcopy(parent['binding']['helper_invocation']),
  'original_constructor_error':copy.deepcopy(parent['original_error_pending_in_outer_handler']),'pending_error_before_test':copy.deepcopy(parent['last_pending_error_in_model']),
  'details_role':copy.deepcopy(parent['binding']['details_role']),'cleanup_list':copy.deepcopy(parent['binding']['cleanup_list']),
  'continuation':continuation,'res_storage_continuity':storage_continuity,
  'C_semantics':cat['source']['C_semantics'],'runtime_observation':False,'physical_identity':None}

def res_null_projection(cat,case,validated,files):
 for v in (cat,case,validated):status_exact_tree(v,'RES-NULL-EXACT-TYPE')
 keys={'scope','anchor','parent_result','binding','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'RES-NULL-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'RES-NULL-VALIDATED:'+k)
 p=case['parent_result'];b=case['binding'];scope=case['scope'];oo=case['outcomes']
 need(type(b) is dict and {'continuation','res_storage_continuity'}<=set(b),'RES-NULL-MISSING-PREMISE')
 status_typed_same(scope,p['scope'],'RES-NULL-SCOPE')
 status_typed_same(b,res_null_binding(cat,p,case['anchor'],b['continuation'],b['res_storage_continuity'],files),'RES-NULL-EXPECTED-BINDING')
 need(type(oo) is list and bool(oo),'RES-NULL-OUTCOMES')
 unresolved=b['continuation']=='UNESTABLISHED' or b['res_storage_continuity']=='UNESTABLISHED'
 if unresolved:status_typed_same(oo,[{'stage':'res-null:continuation','outcome':'unobserved'}],'RES-NULL-UNESTABLISHED-PREMISE')
 steps=cat['steps'][:1] if unresolved else cat['steps'];events=[];replacement=None;outcome=None;completed=False;last=None
 for i,step in enumerate(steps):
  need(i<len(oo),'RES-NULL-MISSING-STEP');row=oo[i]
  need(type(row) is dict and set(row)=={'stage','outcome'} and type(row['stage']) is str and row['stage']==step['id'],'RES-NULL-ORDER')
  last=row['outcome'];need(type(last) is str and last in step['allowed'],'RES-NULL-OUTCOME')
  expected='normal' if i==0 else ('true' if b['res_value_role']['C_NULL'] else 'false')
  event={'id':b['selected_fast_completion']['id']+'/'+step['id'],'stage':step['id'],'source':copy.deepcopy(step['source']),'generated_test':copy.deepcopy(cat['source']['generated_test']),
   'scope':copy.deepcopy(scope),'owner':copy.deepcopy(b['references']['owner']),'token':copy.deepcopy(b['references']['token']),
   'selected_fast_completion':b['selected_fast_completion']['id'],'assignment_occurrence':b['assignment']['occurrence'],
   'res_storage_role':copy.deepcopy(b['res_storage_role']),'res_value_role':copy.deepcopy(b['res_value_role']),
   'enter_role':copy.deepcopy(b['enter_role']),'exit_role':copy.deepcopy(b['exit_role']),'outcome':last,'runtime_observation':False}
  events.append(event)
  if last!=expected:
   need(last not in ('true','false'),'RES-NULL-POINTER-COMPARISON-CONTRADICTION')
   if last in ('raise','catchable-interruption'):
    need(i==0,'RES-NULL-NO-INVENTED-C-EXCEPTION')
    replacement={'role':'conditional-post-fast-completion-continuation-error','reference':event['id']+'/error','scope':copy.deepcopy(scope),'kind':last,
     'origin':'explicit interval frontier before pointer-test evaluation, not a Python exception inside C pointer comparison','exact_type':None,'exact_value':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_observation':False}
   break
  if i==1:completed=True;outcome=b['res_value_role']['C_NULL']
 need(len(oo)==len(events),'RES-NULL-UNREACHED-STEPS')
 uncertain=last in ('interruption','process-termination','unobserved')
 out=copy.deepcopy(p);out.update({'kind':'CONSTRUCTED-RES-NULL-TEST','binding':copy.deepcopy(b),'predecessor_projection':copy.deepcopy(p),'events':events,
  'completion':('res-null-true' if outcome else 'res-null-false') if completed else last+'-frontier',
  'res_null_test_completed_in_model':completed,'res_null_test_outcome':outcome,
  'new_model_claims':{'pointer_comparison_completed':completed,'res_equals_C_NULL':outcome,'Python_truthiness_used':False,'branch_body_entered':False},
  'legacy_flags_scope':'Inherited unqualified result_test_established remains false; new conditional facts are res_null_test_completed_in_model and res_null_test_outcome only.',
  'runtime_test_arrival':None,'runtime_test_outcome':None,'result_test_established':False,'result_error_routing_established':False,
  'exit_decref_attempt_established':False,'stack_operations_established':False,'dispatch_established':False,'context_manager_entry_established':False,'f_binding_established':False,
  'replacement_error_in_model':copy.deepcopy(replacement if replacement is not None else p['replacement_error_in_model']),
  'last_pending_error_in_model':copy.deepcopy(replacement if replacement is not None else p['last_pending_error_in_model']),
  'last_acknowledged_pending_error_before_test':copy.deepcopy(p['last_pending_error_in_model']),
  'pending_error_at_frontier':'UNESTABLISHED' if uncertain else 'conditional retained lineage; helper error indicator remains UNKNOWN',
  'terminal_python_exception_in_model':None if uncertain else True,'C_primitive_python_exception_established':False,'Python_unwind_established':False,
  'current_partial_effects':'UNKNOWN; inherited effects remain unresolved; conditional comparison establishes no physical effects',
  'prior_acknowledged_partial_effects':copy.deepcopy(p['current_partial_effects']),'stop':cat['stop']})
 return out

def validate_res_null_projection(cat,case,validated,submitted,files):
 status_exact_tree(submitted,'RES-NULL-OUTPUT-TYPE')
 status_typed_same(submitted,res_null_projection(cat,case,validated,files),'RES-NULL-OUTPUT-CORRESPONDENCE');return True

# I164-EXIT-DECREF-ATTEMPT-1. Complete 519785-byte predecessor prefix retained.
def exit_decref_sources(files):
 s=res_null_sources(files);sites={}
 specs=[('Python/bytecodes.c',2502,'exit = _PyObject_LookupSpecial(mgr, &_Py_ID(__exit__));'),('Python/bytecodes.c',2503,'if (exit == NULL) {'),('Python/bytecodes.c',2517,'if (res == NULL) {'),('Python/bytecodes.c',2518,'Py_DECREF(exit);'),('Python/bytecodes.c',2519,'ERROR_IF(true, error);'),('Python/generated_cases.c.h',3498,'PyObject *exit;'),('Python/generated_cases.c.h',3531,'if (res == NULL) {'),('Python/generated_cases.c.h',3532,'Py_DECREF(exit);'),('Python/generated_cases.c.h',3533,'if (true) goto pop_1_error;')]
 for name,line,text in specs:
  need(files[name].decode().splitlines()[line-1].strip()==text,'EXIT-DECREF-DEFINING-SOURCE:'+name+':'+str(line))
  sites[(name,line)]={'file':name,'line':line,'expression':text,'identity':copy.deepcopy(s['definition_identities'][name]),'revision':s['revision']}
 return {'revision':s['revision'],'definition_identities':copy.deepcopy(s['definition_identities']),
  'guard':sites[('Python/bytecodes.c',2517)],'generated_guard':sites[('Python/generated_cases.c.h',3531)],
  'operation':sites[('Python/bytecodes.c',2518)],'generated_operation':sites[('Python/generated_cases.c.h',3532)],
  'exit_lookup':sites[('Python/bytecodes.c',2502)],'exit_lookup_null_guard':sites[('Python/bytecodes.c',2503)],'exit_storage_declaration':sites[('Python/generated_cases.c.h',3498)],
  'excluded_error_routing':sites[('Python/bytecodes.c',2519)],'generated_excluded_error_routing':sites[('Python/generated_cases.c.h',3533)],
  'operand':'exit: exact selected successful __exit__ lookup-result role; not enter or res',
  'C_semantics':s['C_semantics'],'definition_context':'Inherited conditional local ceval override; attempt only, no macro expansion or completed effect',
  'stop':'selected Py_DECREF(exit) source-operation attempt or first nonnormal frontier; before decrement completion/effects, error routing and false-branch operations'}

def exit_decref_catalogue(parent,files):
 status_exact_tree(parent,'EXIT-DECREF-PARENT-CATALOGUE-TYPE')
 need(type(parent) is dict and parent.get('format')=='I164-RES-NULL-TEST-STATIC-1','EXIT-DECREF-PARENT-CATALOGUE')
 status_typed_same(parent,res_null_catalogue(parent['fast_catalogue'],files),'EXIT-DECREF-PARENT-INDEPENDENT-SOURCE');s=exit_decref_sources(files)
 steps=[{'id':'exit-decref:continuation','source':copy.deepcopy(s['operation']),'normal':'normal','allowed':['normal','raise','catchable-interruption','process-termination','unobserved']},
        {'id':'exit-decref:attempt','source':copy.deepcopy(s['operation']),'normal':'attempted','allowed':['attempted','interruption','process-termination','unobserved']}]
 return {'format':'I164-EXIT-DECREF-ATTEMPT-STATIC-1','source':s,'res_null_catalogue':copy.deepcopy(parent),'parent_catalogue_sha256':digest(enc(parent)),
  'steps':steps,'order':[x['id'] for x in steps],
  'guard_branches':{'contexts':copy.deepcopy(parent['guard_branches']['contexts']),'prefixes':copy.deepcopy(parent['guard_branches']['prefixes']),'origins':copy.deepcopy(parent['guard_branches']['origins']),'fast_branches':copy.deepcopy(parent['guard_branches']['fast_branches']),
   'comparison_required':True,'continuation':['explicit conditional premise','UNESTABLISHED'],'exit_role_continuity':['explicit conditional premise','UNESTABLISHED']},
  'required_predecessor_facts':['res_null_test_completed_in_model','res_null_test_outcome','conditional_fast_completion_in_model','helper_c_return_completed_in_model','res_assignment_established'],
  'no_false_branch':'Completed false comparison, including non-NULL Python None, cannot supply this relation.',
  'declarations':[{'id':x['id'],'source':copy.deepcopy(x['source']),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for x in steps],
  'preserved_relations':['res_null_test_correspondence',*parent['preserved_relations']],
  'stop':s['stop'],'runtime_chain':None,'actual_admission':False}

def compile_exit_decref(launcher,bytecodes,typeobject,r1,lookup,enter,returned,decref,fast,res_null,files):
 validate_res_null(launcher,bytecodes,typeobject,r1,lookup,enter,returned,decref,fast,files,res_null)
 return exit_decref_catalogue(res_null,files)

def validate_exit_decref(launcher,bytecodes,typeobject,r1,lookup,enter,returned,decref,fast,res_null,files,submitted):
 status_exact_tree(submitted,'EXIT-DECREF-CATALOGUE-TYPE')
 status_typed_same(submitted,compile_exit_decref(launcher,bytecodes,typeobject,r1,lookup,enter,returned,decref,fast,res_null,files),'EXIT-DECREF-CATALOGUE-SOURCE');return True

def exit_decref_binding(cat,parent,anchor,continuation,exit_continuity,files):
 for v in (cat,parent,anchor,continuation,exit_continuity):status_exact_tree(v,'EXIT-DECREF-BINDING-TYPE')
 status_typed_same(cat,exit_decref_catalogue(cat['res_null_catalogue'],files),'EXIT-DECREF-INDEPENDENT-CATALOGUE')
 need(type(parent) is dict and parent.get('kind')=='CONSTRUCTED-RES-NULL-TEST','EXIT-DECREF-PARENT-KIND')
 for k in cat['required_predecessor_facts']:need(parent.get(k) is True,'EXIT-DECREF-MISSING-TRUE-PREDECESSOR:'+k)
 for value,label in [(continuation,'CONTINUATION'),(exit_continuity,'EXIT-CONTINUITY')]:need(type(value) is str and value in ('explicit conditional premise','UNESTABLISHED'),'EXIT-DECREF-'+label)
 p=parent['predecessor_projection'];pc={'scope':copy.deepcopy(parent['scope']),'anchor':copy.deepcopy(parent['instance_anchor']),'parent_result':copy.deepcopy(p),'binding':copy.deepcopy(parent['binding']),'outcomes':[{'stage':e['stage'],'outcome':e['outcome']} for e in parent['events']]}
 validate_res_null_projection(cat['res_null_catalogue'],pc,pc,parent,files)
 need(parent['completion']=='res-null-true' and parent['events'][-1]['stage']=='res-null:comparison' and parent['events'][-1]['outcome']=='true','EXIT-DECREF-TRUE-COMPARISON')
 need(parent['exit_decref_attempt_established'] is False and parent['result_error_routing_established'] is False,'EXIT-DECREF-PARENT-FRONTIER')
 scope=parent['scope'];status_typed_same(parent['instance_anchor'],anchor,'EXIT-DECREF-ANCHOR');status_typed_same(scope['instance'],anchor['instance'],'EXIT-DECREF-INSTANCE')
 need(scope['context']==anchor['context'] and scope['context'] in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO') and scope['acquisition']==anchor['record']['acquisition'],'EXIT-DECREF-CONTEXT-ACQUISITION')
 b=parent['binding'];value=b['res_value_role'];need(value['C_NULL'] is True and value['kind']=='C-NULL' and value['python_value_class'] is None and value['python_object_role'] is None,'EXIT-DECREF-C-NULL-NOT-PYTHON-NONE')
 # Follow the retained embedding to the selected successful lookup; do not infer object identity.
 lookup=parent
 for kind in ('CONSTRUCTED-RES-NULL-TEST','CONSTRUCTED-DECREF-FAST-COMPLETION','CONSTRUCTED-ENTER-DECREF-ATTEMPT','CONSTRUCTED-ENTER-RETURN-RES','CONSTRUCTED-ENTER-CALL-ATTEMPT'):
  need(lookup['kind']==kind,'EXIT-DECREF-LOOKUP-EMBEDDING');status_typed_same(lookup['scope'],scope,'EXIT-DECREF-LOOKUP-SCOPE');lookup=lookup['predecessor_projection']
 need(lookup['kind']=='CONSTRUCTED-CONTEXT-SPECIAL-LOOKUP' and lookup['lookup_completed_in_model']['__exit__'] is True,'EXIT-DECREF-SUCCESSFUL-EXIT-LOOKUP')
 status_typed_same(lookup['scope'],scope,'EXIT-DECREF-LOOKUP-SCOPE')
 role=b['exit_role'];status_typed_same(role,lookup['method_roles']['__exit__'],'EXIT-DECREF-EXACT-LOOKUP-ROLE')
 e=lookup['events'][-1];need(e['stage']=='lookup:__exit__' and e['outcome']=='found' and role['method']=='__exit__' and role['lookup_occurrence']==e['id'],'EXIT-DECREF-LOOKUP-OCCURRENCE')
 need(role['source']['line']==2502 and role['source']['file']=='Python/bytecodes.c' and role['source']['source']==cat['source']['exit_lookup']['identity'],'EXIT-DECREF-LOOKUP-ORIGIN')
 status_typed_same(role['scope'],scope,'EXIT-DECREF-ROLE-SCOPE');status_typed_same(parent['events'][-1]['exit_role'],role,'EXIT-DECREF-COMPARISON-EXIT-ROLE')
 for k in ('owner','token'):
  status_typed_same(e[k],b['references'][k],'EXIT-DECREF-LOOKUP-'+k);status_typed_same(e[k]['scope'],scope,'EXIT-DECREF-REFERENCE-SCOPE')
 return {'scope':copy.deepcopy(scope),'anchor':copy.deepcopy(anchor),'comparison':copy.deepcopy(parent['events'][-1]),'comparison_result':True,
  'operand_role':copy.deepcopy(role),'selected_lookup':copy.deepcopy(e),'enter_role':copy.deepcopy(b['enter_role']),'res_value_role':copy.deepcopy(value),'res_storage_role':copy.deepcopy(b['res_storage_role']),
  'exit_storage_role':{'role':'C local exit storage','symbol':scope['invocation']+'/BEFORE_WITH/exit-storage','scope':copy.deepcopy(scope),'declaration':copy.deepcopy(cat['source']['exit_storage_declaration']),'lookup_occurrence':role['lookup_occurrence'],'runtime_address':None},
  'references':copy.deepcopy(b['references']),'helper_invocation':copy.deepcopy(b['helper_invocation']),'fast_branch':b['fast_branch'],
  'original_constructor_error':copy.deepcopy(parent['original_error_pending_in_outer_handler']),'pending_error_before_attempt':copy.deepcopy(parent['last_pending_error_in_model']),
  'details_role':copy.deepcopy(b['details_role']),'cleanup_list':copy.deepcopy(b['cleanup_list']),
  'continuation':continuation,'exit_role_continuity':exit_continuity,'C_semantics':cat['source']['C_semantics'],'runtime_observation':False,'physical_identity':None}

def exit_decref_projection(cat,case,validated,files):
 for v in (cat,case,validated):status_exact_tree(v,'EXIT-DECREF-EXACT-TYPE')
 keys={'scope','anchor','parent_result','binding','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'EXIT-DECREF-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'EXIT-DECREF-VALIDATED:'+k)
 p=case['parent_result'];b=case['binding'];scope=case['scope'];oo=case['outcomes']
 need(type(b) is dict and {'continuation','exit_role_continuity'}<=set(b),'EXIT-DECREF-MISSING-PREMISE')
 status_typed_same(scope,p['scope'],'EXIT-DECREF-SCOPE')
 status_typed_same(b,exit_decref_binding(cat,p,case['anchor'],b['continuation'],b['exit_role_continuity'],files),'EXIT-DECREF-EXPECTED-BINDING')
 need(type(oo) is list and bool(oo),'EXIT-DECREF-OUTCOMES')
 unresolved=b['continuation']=='UNESTABLISHED' or b['exit_role_continuity']=='UNESTABLISHED'
 if unresolved:status_typed_same(oo,[{'stage':'exit-decref:continuation','outcome':'unobserved'}],'EXIT-DECREF-UNESTABLISHED-PREMISE')
 steps=cat['steps'][:1] if unresolved else cat['steps'];events=[];replacement=None;attempt=None;last=None
 for i,step in enumerate(steps):
  need(i<len(oo),'EXIT-DECREF-MISSING-STEP');row=oo[i]
  need(type(row) is dict and set(row)=={'stage','outcome'} and type(row['stage']) is str and row['stage']==step['id'],'EXIT-DECREF-ORDER')
  last=row['outcome'];need(type(last) is str and last in step['allowed'],'EXIT-DECREF-OUTCOME')
  event={'id':b['comparison']['id']+'/'+step['id'],'stage':step['id'],'source':copy.deepcopy(step['source']),'generated_source':copy.deepcopy(cat['source']['generated_operation']),
   'scope':copy.deepcopy(scope),'owner':copy.deepcopy(b['references']['owner']),'token':copy.deepcopy(b['references']['token']),'comparison_occurrence':b['comparison']['id'],
   'operand_role':copy.deepcopy(b['operand_role']),'exit_storage_role':copy.deepcopy(b['exit_storage_role']),'res_value_role':copy.deepcopy(b['res_value_role']),'outcome':last,'runtime_observation':False}
  events.append(event)
  if last!=step['normal']:
   if last in ('raise','catchable-interruption'):
    need(i==0,'EXIT-DECREF-NO-INVENTED-C-EXCEPTION')
    replacement={'role':'conditional-post-comparison-continuation-error','reference':event['id']+'/error','scope':copy.deepcopy(scope),'kind':last,
     'origin':'explicit interval frontier before selected source-operation attempt, not an exception inside Py_DECREF','exact_type':None,'exact_value':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_observation':False}
   break
  if i==1:attempt=copy.deepcopy(event)
 need(len(oo)==len(events),'EXIT-DECREF-UNREACHED-STEPS')
 uncertain=last in ('interruption','process-termination','unobserved');out=copy.deepcopy(p)
 out.update({'kind':'CONSTRUCTED-EXIT-DECREF-ATTEMPT','binding':copy.deepcopy(b),'predecessor_projection':copy.deepcopy(p),'events':events,
  'completion':'exit-decref-attempt' if attempt is not None else last+'-frontier','exit_decref_attempt':attempt,'exit_decref_attempt_in_model':attempt is not None,
  'new_model_claims':{'selected_exit_decref_attempt':attempt is not None,'decrement_completion':False,'physical_effects':False},
  'legacy_flags_scope':'Inherited exit_decref_attempt_established remains False; new conditional fact is exit_decref_attempt_in_model only.',
  'exit_decref_attempt_established':False,'exit_decref_completion_established':False,'exit_refcount_effects_established':False,'exit_destructor_invocation_established':False,'exit_macro_expansion_established':False,
  'result_error_routing_established':False,'stack_operations_established':False,'dispatch_established':False,'context_manager_entry_established':False,'f_binding_established':False,'runtime_exit_decref_arrival':None,
  'replacement_error_in_model':copy.deepcopy(replacement if replacement is not None else p['replacement_error_in_model']),
  'last_pending_error_in_model':copy.deepcopy(replacement if replacement is not None else p['last_pending_error_in_model']),
  'last_acknowledged_pending_error_before_attempt':copy.deepcopy(p['last_pending_error_in_model']),
  'pending_error_at_frontier':'UNESTABLISHED' if uncertain else 'conditional retained lineage; helper error indicator remains UNKNOWN',
  'terminal_python_exception_in_model':None if uncertain else True,'C_primitive_python_exception_established':False,'Python_unwind_established':False,
  'current_partial_effects':'UNKNOWN; acknowledged earlier effects persist; an attempted source operation establishes no physical effects or their absence',
  'prior_acknowledged_partial_effects':copy.deepcopy(p['current_partial_effects']),'stop':cat['stop']})
 return out

def validate_exit_decref_projection(cat,case,validated,submitted,files):
 status_exact_tree(submitted,'EXIT-DECREF-OUTPUT-TYPE')
 status_typed_same(submitted,exit_decref_projection(cat,case,validated,files),'EXIT-DECREF-OUTPUT-CORRESPONDENCE');return True
