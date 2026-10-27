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


def main():
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args()
 if a.write:
  for k,v in compile_bundle(a.root).items():
   target=a.root/FILES[k];need(not target.exists(),'REFUSE-OVERWRITE:'+str(target));target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(enc(v))
 if a.check:validate_bundle(a.root,read_bundle(a.root))
 print('PASS bounded managed integration; no runtime execution; readiness BLOCKED')
if __name__=='__main__':main()
