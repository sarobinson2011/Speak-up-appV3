"""Protected directory lifetime annotations consumed by the existing cardinality adapter.
Draft association only: no native schema change, instance expansion or invented bound.
"""
import ast,copy,json,sys,hashlib
from pathlib import Path
import cardinality as c
P=Path(__file__).resolve().parents[1]
SOURCE_PATHS=['support/code/ingest.py','integration/candidate_pipeline.py','support/code/static_declarations.py','support/reference/runtime/authority.py','support/reference/runtime/accounting.py','support/reference/runtime/ownership.py','compiler/live_connection.py','compiler/prospective_procedure.py','support/reference/I164-RETRY-ACCOUNTING-ADOPTION-1.md','support/reference/C5-ADOPTION-CLAUSES.md']

def source_sites(root,path):
 raw=(root/path).read_bytes();tree=ast.parse(raw);out=[]
 def walk(node,guards,owner):
  if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):owner=node.name
  if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='objects' for t in node.targets):
   out.append({'site':str(node.lineno)+':'+str(node.col_offset),'function':owner,'operation':'initialize','expression':ast.get_source_segment(raw.decode(),node),'enclosing':guards,'ast_sha256':c.sha(ast.dump(node,include_attributes=False).encode())})
  if isinstance(node,ast.Call):
   segment=ast.get_source_segment(raw.decode(),node)
   if isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name) and node.func.value.id=='objects':
    c.need(node.func.attr in ('append','extend'),'UNSUPPORTED-EMITTER')
    out.append({'site':str(node.lineno)+':'+str(node.col_offset),'function':owner,'operation':node.func.attr,'expression':segment,'enclosing':guards,'ast_sha256':c.sha(ast.dump(node,include_attributes=False).encode())})
  if isinstance(node,ast.If):
   walk(node.test,guards,owner)
   for n in node.body:walk(n,guards+[{'if':ast.unparse(node.test),'polarity':True}],owner)
   for n in node.orelse:walk(n,guards+[{'if':ast.unparse(node.test),'polarity':False}],owner)
   return
  if isinstance(node,(ast.For,ast.AsyncFor)):
   for n in node.body:walk(n,guards+[{'for':ast.unparse(node.target),'in':ast.unparse(node.iter)}],owner)
   for n in node.orelse:walk(n,guards+[{'loop_else':ast.unparse(node.iter)}],owner)
   return
  for child in ast.iter_child_nodes(node):walk(child,guards,owner)
 walk(tree,[],None)
 return {'identity':{'path':path,**c.identity(root/path)},'sites':out,'function_anchors':c.anchors(root,path),'scope':'syntactic enclosing branch/iteration mapping; successful fold required; not runtime reachability proof'}

def integer_constant(root,path,name):
 tree=ast.parse((root/path).read_bytes())
 nodes=[n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)]
 c.need(len(nodes)==1,'CONSTANT-SOURCE');v=ast.literal_eval(nodes[0].value);c.need(type(v) is int,'INTEGER-CONSTANT');return v

def source_constraints(root):
 # AST-extracted constants and guarded literal limits; not independent maxima summed.
 out=[]
 for path in ['support/reference/runtime/authority.py','support/reference/runtime/accounting.py','support/reference/runtime/ownership.py','support/code/ingest.py']:
  raw=(root/path).read_text();tree=ast.parse(raw)
  for node in ast.walk(tree):
   if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='need' and len(node.args)>1 and isinstance(node.args[1],ast.Constant):
    label=node.args[1].value
    if isinstance(label,str) and any(k in label for k in ('CAP','LIMIT','BOUND','HEADROOM','RESERVATION','REPLAY','AMBIGUOUS','ONE-LIFETIME')):
     out.append({'path':path,'line':node.lineno,'guard':ast.unparse(node.args[0]),'label':label,'source_sha256':c.sha(raw.encode()),'classification':'LOCAL_ENFORCEMENT; scope from owning function; no global lifetime inference'})
 return sorted(out,key=lambda x:(x['path'],x['line']))

# Retention is never authorized here. These are accounting carriers, not new classes.
def carriers(root):
 A='support/reference/runtime/authority.py';G='support/code/ingest.py';M='compiler/live_connection.py';O='support/reference/runtime/ownership.py';K='support/reference/runtime/accounting.py'
 def row(id,key,guard,scope,expr,mechanism,status,anchors,missing,retention):
  bound=[]
  for path,name in anchors:
   tree=ast.parse((root/path).read_bytes());nodes=[n for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name]
   c.need(nodes,'CARRIER-SOURCE-ANCHOR:'+name)
   bound.extend({'path':path,'name':name,'line':n.lineno,'end_line':n.end_lineno,'ast_sha256':c.sha(ast.dump(n,include_attributes=False).encode()),'source_sha256':c.identity(root/path)['sha256']} for n in nodes)
  return {'id':id,'occurrence_key':key,'creation_guard':guard,'lifetime_scope':scope,'count_expression':expr,'enforcing_mechanism':mechanism,'status':status,'source_anchors':bound,'missing_evidence':missing,'retention_obligation':retention,'finite_global_bound':None}
 return [
 row('session-head',['binding','database-incarnation','head-row-id=1'],'committed initialization; updates retain one row','database/session','SUM_{s in session_namespaces} 1','HEAD primary key; state/history exact correspondence','CONDITIONAL_EXPRESSION',[[A,'__init__'],[A,'state']], 'complete session/database namespace and writer scope','current authoritative head plus immutable after-states; overwriting HEAD does not delete event history'),
 row('event-history',['binding','seq','event_hash'],'save executes inside committed action transaction','session immutable history','SUM_s E_s; E_s <= MAX_EVENTS','save CAS, sequential event insertion, event/state byte ceilings','ESTABLISHED_FINITE_PER_SCOPE',[[A,'save'],[G,'validate_export']], 'number of namespaces and retained history copies','immutable events/after-states remain protected; exception is not proof of rollback'),
 row('journal',['binding','challenge'],'authenticated admissible envelope, fresh challenge, atomic journal reservation commits before processing','journal/database','SUM_j J_j; J_j <= MAX_ROWS','BEGIN IMMEDIATE, replay check, count guard, primary key','ESTABLISHED_FINITE_PER_SCOPE',[[A,'handle'],[A,'transaction']], 'journal/session lifetime multiplicity; external evidence byte bounds','retains accepted/stale/error/unanswered/interrupted requests; no deletion exemption'),
 row('saved-responses',['binding','challenge','packet_hash'],'response UPDATE and its transaction commit','journal/database','SUM_j R_j; 0 <= R_j <= J_j','single journal response cell; exact authenticated request/challenge binding','CONDITIONAL_EXPRESSION',[[A,'handle'],[G,'validate_export']], 'ambiguous response persistence requires current authenticated evidence','missing response does not prove non-execution; original exact envelope protected when available'),
 row('blob-store',['binding','blob_ref'],'new exact content not already stored; owning transaction commits','session blob namespace','SUM_s B_s','content-addressed equality/conflict check; export verifier ceiling 460 is local acquisition ceiling','CONDITIONAL_EXPRESSION',[[A,'blob'],[G,'validate_export']], 'lifetime namespaces/copies and original external byte-size evidence','physical same-namespace blobs may share exact content under source rule; each referencing occurrence remains distinct'),
 row('ownership-ledger',['ledger-incarnation','chain','executor','decimal_nonce'],'claim finds unowned coordinate in transaction; existing same owner is reused','shared ledger including historical signed-carrier writers','SUM_l O_l; O_l <= MAX_COORDINATES','permanent owner, atomic collision guard and local row ceiling','ESTABLISHED_FINITE_PER_SCOPE',[[O,'claim'],[O,'owner'],[O,'SignedCarrierGuard']], 'all writer/ledger namespaces; same chain/executor coverage','no free/renumber/reassignment; copying ledger creates no fresh ownership rights'),
 row('charged-attempts',['binding','U','attempt_blob','ordinal','parent_request'],'decide or explicit retry commits reserved resources and record','one opened lifetime stage per session','SUM_s A_s; A_s <= 102; slots_s + holds_s <=16','accounting reserve/record/settle; no double failure slot charge','ESTABLISHED_FINITE_PER_SCOPE',[[K,'reserve'],[K,'record'],[K,'settle']], 'session multiplicity; 101/61 structural bounds not demonstrated maxima','charges, consumed slots, ancestry and unresolved holds persist; recovery is not a new charged attempt'),
 row('pending-uncertainty',['binding','U','action','attempt','history_version'],'pending non-null, SIGNING ambiguity, unanswered or unresolved outcome','action and each retained history/acquisition','SUM_acquisitions SUM_histories 1[pending != null]','signing fence, authenticated fold, no new authorization from failure','CONDITIONAL_EXPRESSION',[[A,'sign'],[K,'ready'],[G,'validate_export']], 'number of acquisitions/histories; no duration-based expiry','unresolved signing/release/execution and recovery duties cannot be discharged by absence'),
 row('backup-identifiers',['binding','U','backup_id'],'fresh backup id and snapshot headroom, transaction commits','one stage/shared accounting namespace','SUM_s backup_ids_s; backup_ids_s <=85 within shared snapshot<=130','backup replay and shared/partition counters','ESTABLISHED_FINITE_PER_SCOPE',[[A,'apply'],[K,'validate']], 'external backup completion/copy/size evidence','RETAINED-UNCERTAIN is kernel bookkeeping only; not external storage completion'),
 row('export-acquisitions',['acquisition_receipt_id','source_binding','source_frontier'],'independently acquired or retained export; managed validation export may be transient','acquisition over lifetime','SUM_s retained_export_acquisitions_s','acquire/validate checks content and current expected head; no lifetime acquisition counter','MISSING_BOUND_EVIDENCE',[[G,'acquire'],[M,'_validate']], 'complete retained acquisition inventory and source-owned scope; source has no global acquisition identifier','equal exports are distinct acquisitions if separately required/retained; no automatic obligation to retain every transient read asserted'),
 row('read-recovery-invocations',['managed_instance_receipt_id','invocation_sequence','source_site'],'status or state guard succeeds; close/recover cycle succeeds; fresh authenticated head/sign recovery request admitted','managed instance / journal / lifetime','SUM_instances status_calls_i + state_calls_i + recover_calls_i; head/sign requests separately in J','lock/_require/quarantine fences; status has no allowance counter; journal-backed calls still consume journal rows','UNBOUNDED_ADMITTED_SEQUENCE',[[M,'status'],[M,'state'],[M,'recover'],[A,'sign']], 'which observations require retention, acquisition identity and complete invocation scope','static repeatability is not proof every invocation persists or of operational endurance'),
 row('managed-instances',['deployment_instance_receipt_id','process_start','database_binding'],'open_session constructs a managed owner and validates recovery','process/deployment lifetime','SUM_deployments managed_instances_d','exclusive-owner trusted-process boundary; no instance creation budget','MISSING_BOUND_EVIDENCE',[[M,'__init__'],[M,'open_session']], 'deployment identity and complete instance inventory; local epoch resets at construction','epoch alone is not a global unique instance id; new instance is not new allowance'),
 row('backup-restoration-copies',['retained_container_receipt_id','copy_id','original_binding','frontier'],'external backup/archive/restoration/copy retained; no source-owned operation count supplied','physical copies over lifetime','SUM_containers exact_bytes_c; number_of_containers UNKNOWN','no reviewed prospective full-backup implementation; validated reopening preserves original state/charges','MISSING_BOUND_EVIDENCE',[[M,'recover'],[G,'acquire']], 'complete storage/copy inventory, exact bytes, retention duties, external backup/restore evidence','copies do not reset counters or free U/nonce ownership; moving to archives is not capacity reduction'),
 row('diagnostic-interruption-evidence',['observation_receipt_id','instance','invocation','event_index'],'caught/propagated interruption or persistence uncertainty observation retained','trace/acquisition lifetime','SUM_retained_traces length(trace); exact retained bytes UNKNOWN','managed quarantine and incomplete-cleanup dispositions; no diagnostic lifetime cap','MISSING_BOUND_EVIDENCE',[[M,'_run'],[M,'_dispose'],[M,'recover']], 'required diagnostic retention/source-owned coverage and byte-size scope','partial/failed/unauthenticated/conflicting evidence not silently deleted or promoted to authenticated state')]

def derive(root):
 root,m=c.verify_root(root);a=c.derive_inputs(root)
 sources={p:{'path':p,**m[p]} for p in SOURCE_PATHS}
 projection=source_sites(root,'support/code/ingest.py')
 native=c.load(root/'layout_outputs/directory.json');byid={d['id']:d for d in native['directories']}
 # Emission selection is independently extracted from actual append/extend/initializers.
 # Runtime-named BODY and ABI families are explicitly covered; unsupported emitter
 # syntax cannot be claimed complete through a submitted family list.
 emitted={}
 for site in projection['sites']:
  labels=set()
  tree=ast.parse(site['expression'])
  for node in ast.walk(tree):
   if isinstance(node,ast.Constant) and type(node.value) is str:
    if node.value in c.TOP:labels.add(node.value)
    if node.value=='RELEASE-RESULT':labels.add('RETRY-RELEASE-RESULT')
    if node.value=='BODY-':labels.update(f['family'] for f in a['families'] if f['family'].startswith('BODY-'));labels.add('UNVALIDATED-BODY')
    if node.value=='ABI-ARGUMENTS-':labels.update(['ABI-signPetition','ABI-signPetitionWithZKProof'])
  for f in labels:emitted.setdefault(f,[]).append(site['site'])
 families=[]
 for f in a['families']:
  dirs=[d for d in a['directories'] if d['family']==f['family']]
  roots=[d for d in dirs if d['parent'] is None]
  incoming={d['context']:d['expression']['incoming_ref_directories'] for d in roots}
  families.append({**copy.deepcopy(f),'lifetime_status':'CONDITIONAL_EXPRESSION','logical_state_count_is_not_occurrence_count':True,'protected_occurrence_key':['acquisition_receipt_id','context','record_index','pointer','template'],'receipt_identity_status':'required for lifetime composition; source-native export has no global acquisition id; not a new canonical identity','count_expression':{'op':'SUM_DISTINCT_RETAINED_ACQUISITIONS','domain':'retained_acquisition_receipts','body':{'op':'TOP_LEVEL_PLUS_EACH_REFERENCE','top':f['top_level_per_export'],'incoming_by_context':incoming}},'required_source_evidence':['acquisition scope/completeness','source-selected nested cardinalities','original exact bytes and retention obligations'],'guard_sources':['support/code/ingest.py:validate_export','integration/candidate_pipeline.py:Candidate.ingest','support/code/static_declarations.py:schemas'],'directory_ids':[d['directory'] for d in dirs],'direct_emission_site_ids':emitted.get(f['family'],[]),'nested_creation_rule':'one source-selected referenced occurrence per incoming ref; branch precedence/type/optional guards from directory_links; same bytes do not merge instances','normalization_source':{'path':'integration/candidate_pipeline.py',**m['integration/candidate_pipeline.py']}})
 directory_links=[]
 for d in a['directories']:
  native_d=byid[d['directory']]
  directory_links.append({'directory':d['directory'],'context':d['context'],'family':d['family'],'selector':native_d['selector'],'guard':d['guard'],'presence':native_d['presence'],'type':d['type'],'parent':d['parent'],'source':d['source'],'per_acquisition':d['expression'],'lifetime':{'op':'SUM_DISTINCT_RETAINED_ACQUISITIONS','term':d['directory'],'parameter':'retained_acquisition_receipts'},'required_procedure_range':[d['context'],native_d['class']],'cardinality':None,'classification':'UNKNOWN'})
 limits={'MAX_ROWS':integer_constant(root,'support/reference/runtime/authority.py','MAX_ROWS'),'MAX_EVENTS':integer_constant(root,'support/reference/runtime/authority.py','MAX_EVENTS'),'MAX_COORDINATES':integer_constant(root,'support/reference/runtime/ownership.py','MAX_COORDINATES')}
 return {'format':'I164-PROTECTED-PRODUCTION-UNIVERSE-1','adapter':c.identity(Path(__file__)),'cardinality_adapter':c.identity(P/'code/cardinality.py'),'root_manifest_sha256':c.ROOT_MANIFEST_SHA,'candidate_binding':a['candidate_binding'],'contexts':a['contexts'],'sources':sources,'source_emission_sites':projection,'enforcement_sites':source_constraints(root),'local_ceilings':limits,'families':families,'directory_links':directory_links,'managed_links':a['managed_directories'],'protected_carriers':carriers(root),'relation_lifetime':{'op':'SUM_PER_ACQUISITION_KEYED_JOINS','rules_input':'current layout_outputs/rules.json','cross_acquisition_pairs':'UNRESOLVED; do not invent Cartesian cross-export joins','physical_bytes':'sum over physical retained containers, not over symbolic contexts'},'protected_storage_formula':{'op':'SUM_DISTINCT_RETAINED_CONTAINERS','term':'exact retained bytes including indexes/SQLite overhead/journals/staging/exports/backups/restorations/traces','global_bound':None,'logical_content_deduplication':'not permitted for required distinct occurrences; native blob reuse remains source-specific'},'parameters':a['parameters'],'reviewed_structural_envelopes':a['conditional_envelopes'],'scope':'all 59 schema families / 18678 current directories / 13 managed requirement directories in pinned prospective export and managed sources; carrier duties cover named acquisition/copy classes without asserting exhaustive deployment inventory','outside_domain':['unregistered producer/deployment variants','external C4 RPC outcome/finality serialization','production backup implementation and storage engine overhead/endurance','complete immutable model/stream universes','required cross-acquisition qualified relationships'], 'blockers':a['blockers']+['COMPLETE-PROTECTED-CARRIER-AND-ACQUISITION-SCOPE','SOURCE-OWNED-COPY-AND-LIFETIME-MULTIPLICITIES'],'full_expansion_ready':False,'final_binding':'BLOCKED','actual_admission':False,'stream_identities':'UNCOMPUTED','backup':'KERNEL-ONLY','policy_changes':False}

def validate(root,submitted):
 expected=derive(root);c.same(submitted,expected,'PROTECTED-UNIVERSE-CORRESPONDENCE');return expected

def consume(root,submitted):
 expected=validate(root,submitted);base=c.derive_inputs(root);used=c.consume(root,base)
 procedure=used['existing_procedure_input'];ranges={(r['context'],r['class']) for r in procedure['directory_ranges']}
 c.need(ranges=={tuple(r['required_procedure_range']) for r in expected['directory_links']},'PROCEDURE-RANGE-COVERAGE')
 c.need(all(r['cardinality'] is None and r['classification']=='UNKNOWN' for r in procedure['directory_ranges']),'UNKNOWN-PROPAGATION')
 return {'format':'I164-PROTECTED-UNIVERSE-CONSUMPTION-1','input_sha256':c.sha(c.enc(expected)),'existing_cardinality_input_sha256':c.sha(c.enc(base)),'existing_consumption_sha256':c.sha(c.enc(used)),'existing_procedure_sha256':c.sha(c.enc(procedure)),'directory_count':len(ranges),'family_count':len(expected['families']),'relation_duties':len(procedure['relation_duties']),'managed_requirements':len(expected['managed_links']),'protected_carriers':len(expected['protected_carriers']),'lifetime_parameters':{'retained_acquisition_receipts':None,'retained_containers':None,'managed_instances':None,'required_external_values':None},'production_instance_total':None,'production_pair_total':None,'retained_storage_bytes':None,'blockers':expected['blockers'],'procedure_blockers':procedure['blockers'],'canonical_registration':False,'full_expansion_ready':False,'final_binding':'BLOCKED','actual_admission':False,'stream_identities':'UNCOMPUTED'}
def validate_result(root,x,r):c.same(consume(root,x),r,'UNIVERSE-RESULT-CORRESPONDENCE')
def require_ready(root,x):consume(root,x);raise ValueError('UNKNOWN-LIFETIME-AND-QUALIFIED-OBLIGATIONS')

def count_acquisition_bag(root,submitted,records):
 # Count-only carrier composition, not an alternative projection/model validator.
 x=validate(root,submitted);seen=set();totals={};unknown=set();frontiers={}
 valid={d['directory'] for d in x['directory_links']}
 for r in records:
  c.need(type(r) is dict and set(r)=={'acquisition_id','context','export_sha256','counts'},'ACQUISITION-FIELDS')
  c.need(type(r['acquisition_id']) is str and r['acquisition_id'],'ACQUISITION-ID');c.need(r['context'] in x['contexts'],'ACQUISITION-CONTEXT')
  if r['acquisition_id'] in frontiers:c.need(frontiers[r['acquisition_id']]==r['export_sha256'],'MIXED-ACQUISITION-FRONTIER')
  frontiers[r['acquisition_id']]=r['export_sha256']
  k=(r['acquisition_id'],r['context']);c.need(k not in seen,'DUPLICATE-ACQUISITION-CONTEXT');seen.add(k)
  c.need(type(r['export_sha256']) is str and len(r['export_sha256'])==64 and all(v in '0123456789abcdef' for v in r['export_sha256']),'EXPORT-IDENTITY')
  c.need(type(r['counts']) is dict,'COUNTS')
  for d,n in r['counts'].items():
   c.need(d in valid and d.startswith(r['context']+'|'),'DIRECTORY-CONTEXT');c.need(n is None or type(n) is int and n>=0,'EXACT-COUNT-TYPE')
   if n is None:unknown.add(d)
   else:totals[d]=totals.get(d,0)+n
 for d in unknown:totals[d]=None
 return {'scope':'SUPPLIED-ACQUISITION-COUNTS-ONLY; counts require original projection evidence; no lifetime completeness claim','supplied_acquisition_contexts':len(seen),'counts':totals,'omitted_directories':'UNSUPPLIED not zero','physical_byte_bound':None,'production_complete':False,'full_expansion_ready':False}

def scoped_upper(root,submitted,kind,scope_counts):
 x=validate(root,submitted);c.need(kind in x['local_ceilings'],'BOUND-KIND');cap=x['local_ceilings'][kind]
 c.need(type(scope_counts) is list,'SCOPE-LIST')
 for n in scope_counts:c.need(n is None or type(n) is int and 0<=n<=cap,'PER-SCOPE-BOUND')
 return {'scope':'SUPPLIED-SCOPES-ONLY','observed_sum':c.sum_scopes(scope_counts),'local_upper_for_listed_scopes':len(scope_counts)*cap,'global_upper':None,'lifetime_complete':False}

def main():
 root=Path(sys.argv[1]);out=Path(sys.argv[2]);c.need(not out.exists(),'OUTPUT-EXISTS');out.mkdir(parents=True)
 x=derive(root);r=consume(root,x)
 (out/'universe.json').write_bytes(c.enc(x));(out/'consumption.json').write_bytes(c.enc(r));print(json.dumps({k:r[k] for k in ('family_count','directory_count','relation_duties','managed_requirements','protected_carriers','full_expansion_ready')}))
if __name__=='__main__':main()
