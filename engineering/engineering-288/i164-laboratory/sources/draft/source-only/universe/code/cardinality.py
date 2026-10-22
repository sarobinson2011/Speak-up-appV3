"""Source-pinned cardinality inputs for existing I164 count-only procedures.
No runtime mutation, model allocation, qualified classification or lifetime cap.
"""
import ast,copy,hashlib,json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
ROOT_MANIFEST_SHA='feef1fd4b423c067fa073b9aacb788a6553ec6fe99cde2dbfb0154ff25119209'
CONTEXTS=('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO')
SOURCES={
 'projection':'support/code/ingest.py', 'walk':'integration/candidate_pipeline.py',
 'schemas':'support/code/static_declarations.py','authority':'support/reference/runtime/authority.py',
 'accounting':'support/reference/runtime/accounting.py','ownership':'support/reference/runtime/ownership.py',
 'managed':'compiler/live_connection.py','review':'provenance/retry-review/REPORT.md',
 'adoption':'support/reference/I164-RETRY-ACCOUNTING-ADOPTION-1.md',
 'rules':'compiler/rule_basis.py','procedure':'compiler/prospective_procedure.py'}
def enc(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,msg):
 if not v:raise ValueError(msg)
def same(a,b,msg):need(enc(a)==enc(b),msg)
def load(p):return json.loads(Path(p).read_bytes())
def identity(p):
 b=Path(p).read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def verify_root(root):
 root=Path(root).resolve();p=BASE/'provenance/root-members.json'
 need(sha(p.read_bytes())==ROOT_MANIFEST_SHA,'BASELINE-MANIFEST-IDENTITY');m=load(p)
 actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
 need(actual==set(m),'EXACT-CURRENT-MEMBERSHIP')
 for n,v in m.items():
  p=root/n;need(not p.is_symlink(),'SYMLINK');same(identity(p),v,'CURRENT-SOURCE:'+n)
 return root,m

def anchors(root,path):
 raw=(root/path).read_text();tree=ast.parse(raw)
 return [{'name':n.name,'line':n.lineno,'end_line':n.end_lineno,'ast_sha256':sha(ast.dump(n,include_attributes=False).encode())} for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]

def inventory(root):
 """Independently enumerate every append/extend to the actual object stream.
 Exact pinned implementation, not submitted family table, defines this inventory.
 """
 path=SOURCES['projection'];raw=(root/path).read_text();tree=ast.parse(raw);out=[]
 for n in ast.walk(tree):
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='objects':
   need(n.func.attr in ('append','extend'),'UNSUPPORTED-PROJECTION-CONSTRUCT')
   out.append({'line':n.lineno,'end_line':n.end_lineno,'operation':n.func.attr,'source':ast.get_source_segment(raw,n),'ast_sha256':sha(ast.dump(n,include_attributes=False).encode())})
 # Initial stream creation is not an append.
 for n in ast.walk(tree):
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='objects' for t in n.targets):
   out.append({'line':n.lineno,'end_line':n.end_lineno,'operation':'initialize','source':ast.get_source_segment(raw,n),'ast_sha256':sha(ast.dump(n,include_attributes=False).encode())})
 return sorted(out,key=lambda x:(x['line'],x['operation']))

# Cardinalities of TOP-LEVEL records in ONE accepted saved export, before walk/ref
# expansion. Nested copies are separate occurrences and added by equations below.
TOP={
 'CONFIG':'1','OWNERSHIP-META':'1','BINDING':'1','EVENT':'E','HEAD':'E',
 'REQUEST':'J','PACKET':'J','RESPONSE':'R','OWNERSHIP-ROW':'O','OWNERSHIP-ROW-SQL':'O',
 'ATTEMPT':'A','ACTION':'D','TEMPLATE':'D','COUNTS':'E+1','PARTITIONS':'E+1','RESOURCES':'E+1',
 'U-ENTRY':'sum_h U_h','STAGE':'sum_h opened_h','TRANSPORT-ENTRY':'sum_h transport_h',
 'RETRY-ID-ENTRY':'sum_h retry_ids_h','BACKUP-ENTRY':'sum_h backups_h',
 'LAST':'sum_h last_present_h','PENDING':'sum_h pending_present_h','QUERY':'sum_h query_present_h',
 'UNSIGNED-INTENT':'U_plain','COMPACT-INTENT':'U_compact','ABI-signPetition':'U_ordinary',
 'ABI-signPetitionWithZKProof':'U_zk','CONDITIONAL-CAPSULE':'U','STAGE-META':'opened_final',
 'AUTHORIZED-MESSAGE':'opened_final','OBSERVATION':'Q_observed','SIGNED-TRANSACTION':'D_signed',
 'SIGNED-RESULT':'successful_sign_responses','RELEASE-RESULT':'successful_first_release_responses',
 'RETRY-RELEASE-RESULT':'successful_retry_release_responses','JOURNAL':'J','BLOB-STORE':'B',
 'UNVALIDATED-BODY':'sum_{q in journal requests} 1[(q.method,sha(enc(q.body))) in refused_keys]'}
PARAMETERS={
 'E':('session immutable history','committed source save transitions; no decrement','E <= U + opened + 4*D + retries + 2*Q + backups; loose retained envelope 794'),
 'A':('one opened stage','permanently charged first/retry transmissions','A<=102; reviewed structural A<=n+19 (101 ordinary / 61 ZK under local carrier ceilings)'),
 'D':('one opened stage','new decide actions, not recovered signing','D<=n+5; n+5 branch includes failed proceed; normal/finalized abandon <=n+4'),
 'Q':('one opened stage','charged reconciliation queries','Q<=A+16; shared headroom and verifier guards still apply'),
 'U':('session retirement namespace','new permanent retirement','U<=64; does not bound copies across histories/exports'),
 'J':('one journal','fresh authenticated unique challenge committed before method processing','J<=384000 implementation ceiling; not lifetime recovery capacity'),
 'R':('one journal','response persistence actually committed','0<=R<=J; missing response is not non-execution'),
 'O':('shared protected ownership ledger','new chain/executor/nonce coordinate','O<=4096 local ceiling only; other owners/session multiplicity not bounded by this slice'),
 'B':('session immutable blob store','first distinct content-addressed blob','B<=U+2*opened+2*D+A+Q_observed; retained loose ceiling 460'),
 'exports':('lifetime retained acquisitions','each independently retained validated acquisition','NO source-owned lifetime count supplied'),
 'managed_calls':('managed-instance/lifetime','state/status/handle/close/recover invocations','NO action charge for every managed call; no lifetime call bound'),
 'instances':('lifetime','open_session creates a managed authority','exclusive serving ownership does not bound lifetime instance creation'),
 'external_values':('per-value and lifetime','source-admitted JSON/conditional capsule/outcome data','Decision B; parser/carrier/storage ceilings are not authoritative outcome bounds')}

def family_scope(f):
 if f in ('ATTEMPT','TRANSPORT-ENTRY','RETRY-ID-ENTRY'):return 'attempt identity; repeated per historical state/export as selected'
 if f in ('UNSIGNED-INTENT','COMPACT-INTENT','U-ENTRY','STAGE-META','AUTHORIZED-MESSAGE') or f.startswith('ABI-'):return 'U; exact retained copies per export/history'
 if f in ('REQUEST','PACKET','RESPONSE','JOURNAL','SIGNED-RESULT','RELEASE-RESULT','RETRY-RELEASE-RESULT','UNVALIDATED-BODY') or f.startswith('BODY-'):return 'authenticated invocation/journal; may repeat without new action'
 if f in ('OWNERSHIP-ROW','OWNERSHIP-ROW-SQL','OWNERSHIP-META'):return 'shared ledger; chain/executor/nonce coordinate'
 return 'session record or nested value; per history/export occurrence, lifetime acquisitions unresolved'

def logical_key(f):
 if f in ('REQUEST','PACKET','RESPONSE','JOURNAL') or f.startswith('BODY-'):return 'binding/session + authenticated unique challenge + exact packet/request; projection record index distinguishes copies'
 if f in ('OWNERSHIP-ROW','OWNERSHIP-ROW-SQL'):return 'hash([chain,executor,decimal nonce]); permanent owner binding'
 if f in ('EVENT','HEAD','HEAD-AFTER'):return 'session binding + history sequence/hash + enclosing occurrence pointer'
 if f in ('ATTEMPT','ACTION','BLOB-STORE','SIGNED-TRANSACTION'):return 'immutable exact blob reference; attempt additionally binds ordinal/action/parent/request/U/intent'
 if f in ('U-ENTRY','UNSIGNED-INTENT','COMPACT-INTENT'):return 'session binding + U + immutable intent reference; history/export distinguishes copies'
 return 'enclosing source record identity + exact selector/key/index + context; no deduplication across retained copies'
def creation_condition(f):
 if f.startswith('BODY-'):return 'standalone BODY record with method '+f[5:]+' whose (method, sha(enc(body))) is absent from the export-wide refused_keys set; originating success alone is insufficient'
 if f=='UNVALIDATED-BODY':return 'each standalone BODY record whose (method, sha(enc(body))) is in refused_keys, including equal-key successful requests; count each record separately'
 if f in ('RESPONSE','SUCCESS-RESPONSE','ERROR-RESPONSE'):return 'saved authenticated response present; exact ok discriminator selects success/error, missing response emits neither'
 if f=='OBSERVATION':return 'committed observe event with bound proof; unavailable outcome retains unresolved obligation'
 if f=='SIGNED-TRANSACTION':return 'committed sign-persist event; not sign-claim or uncertain signing'
 if f=='SIGNED-RESULT':return 'successful sign response; recovered sign can repeat without a new attempt/signature event'
 if f in ('STAGE','STAGE-META','AUTHORIZED-MESSAGE'):return 'OPEN committed for permanently retired U; one active lifetime stage per current namespace'
 if f=='U-ENTRY':return 'retirement committed; entry retained in each applicable historical state'
 if f in ('ATTEMPT','TRANSPORT-ENTRY'):return 'atomic charged decision or explicit retry commit; permanent ancestry retained'
 if f=='RETRY-ID-ENTRY':return 'explicit authenticated retry_release committed with fresh retry ID and prior-attempt evidence'
 if f=='BACKUP-ENTRY':return 'backup ID accepted and charged under snapshot headroom; kernel-only RETAINED-UNCERTAIN'
 if f=='QUERY':return 'pending query non-null after charged query; not a new retry authorization'
 if f in ('PENDING','LAST'):return 'corresponding historical stage member is non-null; FAILED-FROZEN remains pending'
 return 'exact pinned ingest emission and nested walk/ref/discriminator guard; see source anchors and per-directory guards'
def enforcement(f):
 if f in ('U-ENTRY','UNSIGNED-INTENT','COMPACT-INTENT'):return 'authority.apply retire U-LIMIT 64; copies are not new retirements'
 if f in ('ATTEMPT','TRANSPORT-ENTRY','RETRY-ID-ENTRY'):return 'accounting.reserve/validate; stage102, slots+holds16; guards are not lifetime acquisition caps'
 if f=='BACKUP-ENTRY':return 'authority.apply backup: shared snapshot130 and partition85; no external backup assurance'
 if f in ('REQUEST','PACKET','RESPONSE','JOURNAL'):return 'authority.handle unique challenge; journal384000 fail-closed per-file ceiling, not source-owned outcome/lifetime bound'
 return 'existing source/type/guard validators; symbolic selected counts remain unresolved where no source bound exists'

def numerical_envelopes():
 # Retained conservative accounting, not demonstration of feasible maximal path.
 return {'attempt_cap':102,'shared_slots':16,'retired_u':64,'ordinary':{'n_local_ceiling':82,'structural_attempt_upper':82+19},'zk':{'n_local_ceiling':42,'structural_attempt_upper':42+19},'events_loose':64+1+4*102+2*(102+16)+85,'blobs_loose':64+2+87+87+102+118,'prospective_owned_coordinates':{'expression':'U+n+4 when one U opened; U when none opened','ordinary_upper':64+82+4,'zk_upper':64+42+4,'scope':'current prospective namespace only; not all shared-ledger writers'},'attained_maximum':False,'full_domain_bound':False,'source':SOURCES['review']}

def derive_inputs(root,validated=None):
 root,m=verify_root(root)
 sys.path.insert(0,str(root/'compiler'));import layout_consumers as lc
 v={k:load(root/path) for k,path in lc.PATHS.items()} if validated is None else validated
 # Passing a previously computed bundle is internal only; public consume rederives.
 ds=v['directory']['directories'];rules=v['rules']['rules'];families=sorted({r['record'] for r in ds})
 rows=[]
 for f in families:
  expr=TOP.get(f,'sum_{q in journal requests} 1[q.method == '+repr(f[5:])+' and (q.method,sha(enc(q.body))) not in refused_keys]' if f.startswith('BODY-') else '0')
  rows.append({'family':f,'top_level_per_export':expr,'top_level_zero_scope':'no standalone emission in this pinned export projection; NOT zero nested occurrences' if expr=='0' else None,'scope':family_scope(f),'status':'CONDITIONAL_EXPRESSION','identity':'sha256(canonical[candidate,context,record_index,pointer,template]); retained copies are distinct','creation_guard':'accepted authenticated export then source-admitted Candidate.ingest/walk branch; root refs also emit','sources':[SOURCES['projection'],SOURCES['walk'],SOURCES['schemas']],'lifetime':'sum over retained exports and contexts; export multiplicity unresolved','logical_key':logical_key(f),'creation_condition':creation_condition(f),'enforcement':enforcement(f)})
 refs={f:[] for f in families}
 for r in ds:
  if isinstance(r['type'],dict) and 'ref' in r['type']:refs[r['type']['ref']].append(r['id'])
 equations=[]
 for r in ds:
  sel=r['selector'];parent=r['parent'];t=r['type'];ctx=r['context']
  if parent is None:
   expression={'op':'ADD_TOP_AND_REFERENCE_COPIES','top_family':r['record'],'incoming_ref_directories':[i for i in refs[r['record']] if i.startswith(ctx+'|')]}
  elif '#' in sel and sel.rsplit('#',1)[1] in ('presence','availability','encoding_length','member_count','exact_bytes','type_tag','key_encoding','separator_encoding','opening_delimiter','closing_delimiter'):
   expression={'op':'ONE_PER_PRESENT_PARENT','parent':parent}
  elif (r['guard']=='present' and r['presence']=='required' and '*' not in sel.rsplit('/',1)[-1]) or r['guard'].startswith('fixed index '):
   expression={'op':'ONE_PER_PRESENT_PARENT','parent':parent}
  else:
   # Exact source selector walk, not a guessed multiplication by a fixture count.
   expression={'op':'SUM_SOURCE_SELECTED_CHILDREN','parent':parent,'selector':sel,'guard':r['guard'],'presence':r['presence'],'semantics':'Candidate.ingest.walk: required child=one; optional inverse=absent; union first matching branch; discriminator exact; directory/array per member; keys/indices distinct; recursive refs retained','unresolved_parameter':'selected_child_counts:'+r['id']}
  equations.append({'directory':r['id'],'context':ctx,'family':r['record'],'type':t,'guard':r['guard'],'parent':parent,'source':r['source'],'expression':expression,'exact':None,'status':'CONDITIONAL_EXPRESSION','classification':'UNKNOWN'})
 relations=[]
 for r in v['directory']['relations']:
  relations.append({'ordinal':r['ordinal'],'kind':r['kind'],'rule':copy.deepcopy(r),'expression':({'op':'COMPLETE_AUTHENTICATED_FOLDS','pair_count':False,'per_complete_fold':1} if r['kind']=='SOURCE-FOLD-OBLIGATION' else {'op':'COUNT_GUARDED_SOURCE_WITH_UNIQUE_TARGET','operator':r['join']['operator'],'contexts':list(CONTEXTS),'keys':r['join']['keys'],'guard':r['guard']}),'exact':None,'classification':'UNKNOWN'})
 for r in rules:
  relations.append({'ordinal':r['ordinal'],'kind':r['kind'],'rule':copy.deepcopy(r),'expression':{'op':'SUM_SOURCE_ADMITTED_KEYED_MATCHES','operator':r['join']['operator'],'contexts':list(CONTEXTS),'keys':r['join']['keys'],'guard':r['guard'],'multiplicity':r['join']['multiplicity']},'exact':None,'classification':'UNKNOWN'})
 managed=load(root/'candidate/managed-route/directory-relations.json')
 mr=[{'id':r['id'],'requirement':r['requirement'],'source':r['guard_source'],'guards':r['guard_functions'],'scope':'managed invocation / instance / lifetime','expression':'sum invocations satisfying source requirement guard; no adopted lifetime invocation bound','status':'MISSING_BOUND_EVIDENCE','exact':None} for r in managed['managed_directories']]
 return {'format':'I164-PRODUCTION-CARDINALITY-INPUT-1','adapter':identity(Path(__file__)),'root_manifest_sha256':ROOT_MANIFEST_SHA,'contexts':list(CONTEXTS),'candidate_binding':v['directory']['candidate_binding'],'sources':{k:{'path':p,**m[p],'anchors':anchors(root,p) if p.endswith('.py') else []} for k,p in SOURCES.items()},'body_selection':{'scope':'standalone BODY records only; nested REQUEST/PACKET union selection unchanged','refused_keys':'{(request.method, sha(enc(request.body))) for each journal row with absent response or response.ok is False}','selection':'after ABI/release-result normalization, a BODY-method record becomes UNVALIDATED-BODY iff (method, sha(enc(original body))) is in refused_keys','multiplicity':'sum over distinct emitted record occurrences; never count distinct body values or distinct refused keys','source':SOURCES['walk']},'emission_inventory':inventory(root),'families':rows,'directories':equations,'relations':relations,'managed_directories':mr,'parameters':{k:{'scope':v[0],'guard':v[1],'constraint_or_gap':v[2],'status':('ESTABLISHED_FINITE_PER_SCOPE' if k in ('A','Q','U') else 'CONDITIONAL_EXPRESSION' if k in ('E','D','R','B') else 'MISSING_BOUND_EVIDENCE'),'finite_global_lifetime_bound':None} for k,v in PARAMETERS.items()},'repeatability':{'source':SOURCES['managed'],'paths':['ManagedAuthority.status','ManagedAuthority.state','close -> recover -> close'],'status':'UNBOUNDED_ADMITTED_INVOCATION_SEQUENCE_IN_PINNED_IMPLEMENTATION','proof':'status reads under lock without charging or advancing a limiting counter; finite arbitrary repetition stays admitted. Sequential successful close/recover increments epoch without a cap. This is a static recurrence, not a runtime/storage endurance experiment.','persistent_accumulation':'only conditional on retaining observations/acquisitions; implementation does not itself persist every status invocation','lifetime_evidence_bound':None},'conditional_envelopes':numerical_envelopes(),'blockers':['lifetime export/session/instance/read/recovery multiplicities','recursive/source-owned external value bounds under Decision B','qualified ownership/visibility/custody and ledger duties','canonical authority and complete immutable model binding'],'full_expansion_ready':False,'final_binding':'BLOCKED','backup':'KERNEL-ONLY','stream_identities':'UNCOMPUTED','actual_admission':False}

def validate_inputs(root,submitted):
 expected=derive_inputs(root);same(submitted,expected,'CARDINALITY-SOURCE-CORRESPONDENCE');return expected

def sum_scopes(counts):
 need(type(counts) is list,'SCOPE-TYPE')
 for n in counts:need(n is None or type(n) is int and n>=0,'COUNT-TYPE')
 return None if any(n is None for n in counts) else sum(counts)

def consume(root,submitted):
 root,_=verify_root(root);sys.path.insert(0,str(root/'compiler'));import layout_consumers as lc
 expected=validate_inputs(root,submitted)
 values=lc.derive(root) # invokes existing compiler, semantic rules and p.count_only
 same(derive_inputs(root,values),expected,'CURRENT-DERIVATION-CORRESPONDENCE')
 # Use the actual validated count-only procedure result; retain all its duties,
 # unknown classifications and null production totals. Sidecar annotations do not
 # pretend to be a new valid native procedure-input schema.
 procedure=values['procedure']
 need(len(procedure['directory_ranges'])==len(expected['directories']),'DIRECTORY-COVERAGE')
 same([r['ordinal'] for r in procedure['relation_duties']],[r['ordinal'] for r in expected['relations']],'DUTY-COVERAGE')
 return {'format':'I164-PRODUCTION-CARDINALITY-CONSUMPTION-1','input_sha256':sha(enc(expected)),'existing_procedure_input':procedure,'family_annotations':expected['families'],'body_selection':expected['body_selection'],'directory_annotations':expected['directories'],'relation_annotations':expected['relations'],'managed_annotations':expected['managed_directories'],'conditional_envelopes':expected['conditional_envelopes'],'unresolved_parameters':expected['parameters'],'blockers':expected['blockers'],'production_instance_total':None,'production_pair_total':None,'full_expansion_ready':False,'final_binding':'BLOCKED','actual_admission':False,'stream_identities':'UNCOMPUTED'}
def validate_result(root,submitted,result):same(consume(root,submitted),result,'RESULT-CORRESPONDENCE')
def require_ready(root,submitted):
 consume(root,submitted);raise ValueError('UNRESOLVED-PRODUCTION-CARDINALITIES-AND-DUTIES')

def _body_counts(objects,journal,context,encode,parse,digest):
 # Private arithmetic on a validated object stream; no authentication claim here.
 refused=set()
 for _,packet,response in journal:
  request=parse(bytes.fromhex(packet))['request']
  if response is None or parse(bytes.fromhex(response))['response']['ok'] is False:
   refused.add((request['method'],digest(encode(request['body']))))
 counts={};occurrences=[]
 for index,(kind,body) in enumerate(objects):
  if not kind.startswith('BODY-'):continue
  key=(kind[5:],digest(encode(body)))
  family='UNVALIDATED-BODY' if key in refused else kind
  counts[family]=counts.get(family,0)+1
  occurrences.append({'context':context,'record_index':index,'original_family':kind,'selected_family':family,'selection_key':list(key)})
 return {'counts':counts,'occurrences':occurrences}

def body_counts(root,export,context):
 root,_=verify_root(root);need(context in CONTEXTS,'BODY-CONTEXT')
 sys.path.insert(0,str(root/'compiler'));import compiler as existing
 existing.setup(root)
 from ingest import validate_export
 from common import enc as source_enc,parse,sha as source_sha
 checked=validate_export(export) # existing exact request/signature/history validation
 result=_body_counts(checked['objects'],export['journal'],context,source_enc,parse,source_sha)
 return {'format':'I164-PC01-BODY-COUNT-1','source':{'path':SOURCES['walk'],**identity(root/SOURCES['walk'])},'export_sha256':source_sha(source_enc(export)),'context':context,**result,'scope':'standalone BODY normalization only; no readiness or lifetime claim','actual_admission':False}

def validate_body_counts(root,export,context,result):
 same(body_counts(root,export,context),result,'BODY-OCCURRENCE-CORRESPONDENCE')

def main():
 import argparse
 p=argparse.ArgumentParser();p.add_argument('root');p.add_argument('output');p.add_argument('--input');a=p.parse_args()
 x=load(a.input) if a.input else derive_inputs(a.root);r=consume(a.root,x)
 dest=Path(a.output);need(not dest.exists(),'OUTPUT-EXISTS');dest.mkdir(parents=True)
 (dest/'cardinality-inputs.json').write_bytes(enc(x));(dest/'count-only-result.json').write_bytes(enc(r))
 print(json.dumps({'families':len(x['families']),'directories':len(x['directories']),'relations':len(x['relations']),'managed_requirements':len(x['managed_directories']),'contexts':x['contexts'],'full_expansion_ready':False,'final_binding':'BLOCKED','actual_admission':False}))
if __name__=='__main__':main()
