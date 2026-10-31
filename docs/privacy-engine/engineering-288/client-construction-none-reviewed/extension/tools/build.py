from pathlib import Path
import ast,hashlib,json,difflib
T=Path(__file__).resolve().parents[1];root=T/'input';prior=root/'retained/control-construction'
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
old=(prior/'code/managed_coverage.py').read_bytes();new=old+b'\n\n'+(T/'tools/producer-addition.py').read_bytes();before=ast.parse(old);after=ast.parse(new)
assert len(after.body)==len(before.body)+6 and all(ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False) for a,b in zip(before.body,after.body))
(root/'code/managed_coverage.py').write_bytes(new)
s=(prior/'code/correspondence.py').read_text()
s=s.replace('control-construction exception-to-finally/removal','client-construction exact-None handler-to-finally/removal')
s=s.replace('CONSTRUCTION-','CLIENT-CONSTRUCTION-').replace('I164-CONTROL-CLIENT-CONSTRUCTION-CORRESPONDENCE-1','I164-CLIENT-CONSTRUCTION-NONE-CORRESPONDENCE-1')
s=s.replace('compile_control_construction','compile_client_construction').replace('control_construction_projection','client_construction_projection').replace('control_construction_binding','client_construction_binding')
s=s.replace('derive_construction','derive_client_construction').replace("base=root/'retained/control'","base=root/'retained/control-construction'")
s=s.replace("'_control_predecessor'","'_control_construction_predecessor'").replace("'_construction_coverage'","'_client_construction_coverage'")
s=s.replace("'results/primary/control-exception.json'","'results/primary/control-construction.json'")
s=s.replace("'control_basis':bb,'control_module':p", "'construction_basis':bb,'construction_module':p")
functions={
'_rows':'''def _rows(basis):
 rows=[];cat=basis['catalogue'];require(tuple(r['context'] for r in basis['prior']['contexts'])==CONTEXTS,'CLIENT-CONSTRUCTION-CONTEXT-DOMAIN')
 for row in basis['prior']['contexts']:
  prior=row['control_construction_revocation_correspondence'];token=row['token_registration_correspondence'];same(prior['instance_anchor'],token['instance_anchor'],'CLIENT-CONSTRUCTION-VALIDATED-INSTANCE');same(prior['declaration']['source']['sources'],cat['source']['sources'],'CLIENT-CONSTRUCTION-VALIDATED-SOURCE')
  rows.append({'context':row['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(token['instance_anchor']),'predecessor_receipt':identity(basis['saved']),'scope':copy.deepcopy(token['scope']),'reference_basis':copy.deepcopy(token['reference_basis']),
   'conditional_links':[{'declaration':d['id'],'source_origin':copy.deepcopy(d['source_origin']),'invocation':None,'frame':None,'observed_value':None} for d in cat['declarations']],
   'reviewed_relations_preserved':copy.deepcopy(cat['preserved_relations']),'prefix_variants':['control-absent','control-construction-and-callback-completed-normally'],'guard_slot_continuity':'Explicit same-owner exact-None premise; not historical absence of storage','selected_owner_continuity':'Explicit conditional premise; not runtime exclusivity','client_handler_applicable':True,'construction_completed':False,'completed_client_object_reference':None,'client_callback_execution':False,'earlier_control_execution':'Conditional on selected validated prefix; no new runtime observation','constructor_substep_history':None,'runtime_client_construction_revocation_chain':None,'client_construction_producer_history':None,'exception_chain_observation':None,'prior_failure_storage_history':None,'physical_reference_observation':None,'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'actual_invocation_count':None,'observer_join':None,'separate_observer':copy.deepcopy(prior['separate_observer']),'outer_cleanup_complete':False,'gap':'No runtime Client construction/error/handler/bare-rethrow/pop chain or constructor progress. Non-None constructor handler branch and full outer cleanup remain unexpanded.'})
 return rows
''',
'_assemble':'''def _assemble(data,rows,basis):
 _check_rows(basis,rows);result=copy.deepcopy(basis['prior']);result['format']='I164-CLIENT-CONSTRUCTION-NONE-CORRESPONDENCE-1';result['prior_control_construction_components']=result.pop('extension_components');result['prior_control_construction_receipt']=identity(basis['saved']);result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(result['contexts'],rows):ctx['client_construction_none_correspondence']=copy.deepcopy(row)
 result['new_client_construction_limits']={'static_conditional_slice':True,'runtime_chain':'UNAVAILABLE','guard_slot_continuity':'Explicit same-owner exact-None premise','selected_owner_continuity':'Explicit premise','construction_completion_established':False,'client_callback_execution_established':False,'earlier_control_progress':'Preserve selected validated prefix separately','existing_cause_context_suppression':'UNKNOWN','physical_identity_or_inequality':None,'observer_join':None,'outer_cleanup_complete':False,'non_none_constructor_branch_complete':False,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False};return result
''',
'_premises':'''def _premises(basis,case):
 exact(case,'CLIENT-CONSTRUCTION-CONSTRUCTED-INPUT');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','token_case','construction_error','none_guard_binding','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-CLIENT-CONSTRUCTION-NONE','CLIENT-CONSTRUCTION-CONSTRUCTED-CASE')
 rows=[r for r in basis['prior']['contexts'] if r['context']==case['context']];require(len(rows)==1,'CLIENT-CONSTRUCTION-CONSTRUCTED-CONTEXT');anchor=rows[0]['token_registration_correspondence']['instance_anchor'];same(case['anchor'],anchor,'CLIENT-CONSTRUCTION-CONSTRUCTED-ANCHOR');tc=case['token_case'];require(type(tc) is dict,'CLIENT-CONSTRUCTION-TOKEN-CASE');same({k:tc.get(k) for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'CLIENT-CONSTRUCTION-TOKEN-INVOCATION')
 sb=basis['stored_basis'];token=sb['routes']['token_module']._construct_checked(sb['token_basis'],tc)['projection'];require(tc['owner_failure_none'] is True,'CLIENT-CONSTRUCTION-SELECTED-NONE-SLICE');require(token['registration_completed_in_model'] is True and token['completion']=='unexpected-raise' and token['client_callback_completed_in_model'] is False and token['events'][-1]['stage']=='client-create' and token['events'][-1]['outcome']=='raise','CLIENT-CONSTRUCTION-TOKEN-FRONTIER')
 refs=token['reference_bindings'];scope=token['scope'];cat=basis['catalogue'];error=basis['fresh']['coverage'].client_construction_binding(cat,scope,tc['control_present']);same(case['construction_error'],error,'CLIENT-CONSTRUCTION-EXPRESSION-ERROR')
 binding={'scope':copy.deepcopy(scope),'owner':copy.deepcopy(refs['owner']),'slot':'owner.failure','slot_value':None,'slot_exact_type':'NoneType','guard_expression':cat['source']['guard_expression'],'guard_result':False,'guard_source':copy.deepcopy(cat['source']['guard']),'source':copy.deepcopy(cat['source']['sources']['entry']),'premise':cat['source']['guard_slot_premise'],'runtime_reference_observation':None,'prior_storage_history':'UNKNOWN; no retained evidence is erased'}
 same(case['none_guard_binding'],binding,'CLIENT-CONSTRUCTION-SELECTED-GUARD-BINDING')
 return {'scope':copy.deepcopy(scope),'references':copy.deepcopy(refs),'token_inputs':copy.deepcopy(tc['projection']),'token_prefix':token,'construction_error':error,'none_guard_binding':binding,'outcomes':copy.deepcopy(case['outcomes'])}
''',
'_construct_checked':'''def _construct_checked(basis,case):
 v=_premises(basis,case);c=basis['fresh']['coverage'];cat=basis['catalogue'];out=c.client_construction_projection(cat,case['projection'],v);c.validate_client_construction_projection(cat,case['projection'],v,case['output']);return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(case['anchor']),'projection':out,'premises':'Selected Client(token) expression raises before client callback; control absent or its selected earlier path completed normally. Same-owner exact-None guard and selected-owner continuity are explicit conditional premises. No allocation, initializer history, physical identity or existing cause/context absence is inferred.','runtime_observation':False}
''',
'constructed_prior':'''def constructed_prior(data,submitted_catalogue,branch,case):
 exact(case,'CLIENT-CONSTRUCTION-PRIOR-CONSTRUCTED-INPUT');require(type(branch) is str and branch in ('control-construction','control','bare','stored-client','stored-normal','normal-token'),'CLIENT-CONSTRUCTION-PRIOR-BRANCH');_,basis=_checked(data,submitted_catalogue);return _construct_prior(basis,branch,case)
''',
'_construct_prior':'''def _construct_prior(basis,branch,case):
 exact(case,'CLIENT-CONSTRUCTION-PRIOR-CONSTRUCTED-INPUT');p=basis['construction_module'];b=basis['construction_basis']
 if branch=='control-construction':return p._construct_checked(b,case)
 return p._construct_prior(b,branch,case)
''',
'validate':'''def validate(root,saved):
 require(type(saved) is bytes,'CLIENT-CONSTRUCTION-RECEIPT-BYTES');v=json.loads(saved);required={'client_construction_none_correspondence','control_construction_revocation_correspondence','control_exception_revocation_correspondence','callback_bare_rethrow_correspondence','callback_stored_failure_correspondence','stored_failure_revocation_correspondence','token_registration_correspondence'}
 require(type(v) is dict and v.get('format')=='I164-CLIENT-CONSTRUCTION-NONE-CORRESPONDENCE-1' and type(v.get('contexts')) is list and len(v['contexts'])==2 and all(type(c) is dict and required<=set(c) for c in v['contexts']),'CLIENT-CONSTRUCTION-MANDATORY-RELATIONS');require(saved==enc(derive(root)),'CLIENT-CONSTRUCTION-STALE-OR-ALTERED-RECEIPT');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(saved),'runtime_client_construction_revocation_chain':'UNAVAILABLE','actual_admission':False}
'''}
pins={'PRODUCER_PIN':pin(new),'PREDECESSOR_MANIFEST':pin((prior/'MANIFEST.json').read_bytes()),'PREDECESSOR_RECEIPT':pin((prior/'results/primary/control-construction.json').read_bytes())}
t=ast.parse(s);lines=s.splitlines(True);edits=[]
for n in t.body:
 if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in pins:edits.append((n.lineno-1,n.end_lineno,n.targets[0].id+'='+repr(pins[n.targets[0].id])+'\n'))
 if isinstance(n,ast.FunctionDef) and n.name in functions:edits.append((n.lineno-1,n.end_lineno,functions[n.name]))
for a,b,text in reversed(edits):lines[a:b]=[text]
s=''.join(lines);compile(s,str(root/'code/correspondence.py'),'exec');(root/'code/correspondence.py').write_text(s)
(root/'provenance/changed-files.json').write_bytes(enc({'intentional_changes':{n:{'before':pin((prior/n).read_bytes()),'after':pin((root/n).read_bytes())} for n in ('code/managed_coverage.py','code/correspondence.py')},'inherited_producer_definitions_unchanged':sum(isinstance(n,ast.FunctionDef) for n in before.body),'new_producer_definitions':6,'runtime_source_changes':0,'prior_reviewed_root_changes':0}))
(root/'provenance/implementation.diff').write_text(''.join(''.join(difflib.unified_diff((prior/n).read_text().splitlines(True),(root/n).read_text().splitlines(True),fromfile='retained/control-construction/'+n,tofile=n)) for n in ('code/managed_coverage.py','code/correspondence.py')))
print('Additive producer and mandatory adapter prepared; inherited definitions unchanged; no model execution.')
