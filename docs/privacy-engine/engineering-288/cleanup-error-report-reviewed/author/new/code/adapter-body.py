def catalogue(data):
 return data['coverage'].compile_error_report(*sources(data),data['prior']['contexts'][0]['exceptional_cleanup_append_correspondence']['declaration'])
def _basis(data):
 fresh=inputs(data['root']);pb,public=_public_predecessor(fresh);p=fresh['prior_module']
 require(sources(fresh)==p.sources(pb['fresh']),'REPORT-AUTHENTICATED-SOURCES')
 cat=fresh['coverage'].compile_error_report(*sources(fresh),pb['catalogue'])
 return {'fresh':fresh,'prior':copy.deepcopy(fresh['prior']),'prior_basis':pb,'prior_module':p,'public_predecessor':public,'catalogue':cat,'evidence':dict(pb['evidence'])}
def _rows(basis):
 require(tuple(x['context'] for x in basis['prior']['contexts'])==CONTEXTS,'REPORT-CONTEXT-DOMAIN');rows=[]
 for old in basis['prior']['contexts']:
  parent=old['exceptional_cleanup_append_correspondence'];cat=basis['catalogue']
  rows.append({'context':old['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(parent['instance_anchor']),'scope':copy.deepcopy(parent['scope']),'reference_basis':copy.deepcopy(parent['reference_basis']),
   'predecessor_receipt':PREDECESSOR_RECEIPT.copy(),'predecessor_public_validation':copy.deepcopy(basis['public_predecessor']),
   'conditional_links':[{'declaration':d['id'],'source_origin':copy.deepcopy(d['source_origin']),'invocation':None,'frame':None,'observed_value':None} for d in cat['declarations']],
   'required_parent':'Validated selected raise in protected close/normal-append try; exact occurrence and pending selected error',
   'selected_error_continuity':'Explicit conditional delivery and owner/local/name/details/list/method continuity; not observed reference identity',
   'partial_effects':'An earlier uncertain append remains uncertain even after error-item append completes',
   'runtime_error_report_chain':None,'physical_reference_observation':None,'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'actual_invocation_count':None,'observer_join':None,'separate_observer':copy.deepcopy(parent['separate_observer']),
   'handler_exit_established':False,'later_iterations_complete':False,'outer_cleanup_complete':False,'gap':'No runtime selected-error catch/evaluation/append chain; later cleanup and physical effects remain unestablished'})
 return rows
def _check_rows(basis,claims):exact(claims,'REPORT-SEMANTIC-CLAIMS');same(claims,_rows(basis),'REPORT-SEMANTIC-CORRESPONDENCE')
def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'REPORT-EVIDENCE-TYPES');require(candidate==basis['evidence'],'REPORT-VALIDATED-EVIDENCE')
def _check_candidate(basis,data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'REPORT-CATALOGUE');exact(claims,'REPORT-CLAIMS')
 same(submitted_catalogue,basis['catalogue'],'REPORT-CATALOGUE-SOURCE');require(sources(data)==sources(basis['fresh']) and all(type(x) is bytes for x in sources(data)),'REPORT-CANDIDATE-SOURCE');same(data['prior'],basis['prior'],'REPORT-CANDIDATE-PREDECESSOR')
 require(type(data['prior_saved']) is bytes and data['prior_saved']==basis['fresh']['prior_saved'],'REPORT-CANDIDATE-RECEIPT')
 if evidence is not None:_compare_evidence(basis,evidence)
 if claims is not None:_check_rows(basis,claims)
 return _rows(basis)
def _checked(data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'REPORT-CATALOGUE');exact(claims,'REPORT-CLAIMS');basis=_basis(data)
 return _check_candidate(basis,data,submitted_catalogue,claims,evidence),basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def _assemble(data,rows,basis):
 _check_rows(basis,rows);result=copy.deepcopy(basis['prior']);result['format']='I164-CLEANUP-ERROR-REPORT-CORRESPONDENCE-1';result['prior_cleanup_append_components']=result.pop('extension_components');result['prior_cleanup_append_receipt']=PREDECESSOR_RECEIPT.copy();result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(result['contexts'],rows):ctx[RELATION]=copy.deepcopy(row)
 result['new_error_report_limits']={'static_conditional_slice':True,'runtime_chain':'UNAVAILABLE','exact_generated_strings_bytes':None,'earlier_partial_effects_preserved':True,'handler_exit_established':False,'non_none_constructor_branch_complete':False,'outer_cleanup_complete':False,'later_iterations_complete':False,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False};return result
def derive_error_report(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);return _assemble(data,rows,basis)
def _premises(basis,case):
 exact(case,'REPORT-CONSTRUCTED-INPUT');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','parent_case','parent_output','binding','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-CLEANUP-ERROR-REPORT','REPORT-CONSTRUCTED-CASE')
 rows=[r for r in basis['prior']['contexts'] if r['context']==case['context']];require(len(rows)==1,'REPORT-CONSTRUCTED-CONTEXT');anchor=rows[0]['exceptional_cleanup_append_correspondence']['instance_anchor'];same(case['anchor'],anchor,'REPORT-CONSTRUCTED-ANCHOR')
 pc=case['parent_case'];require(type(pc) is dict,'REPORT-PARENT-CASE');same({k:pc.get(k) for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'REPORT-PARENT-INVOCATION')
 parent=basis['prior_module']._construct_checked(basis['prior_basis'],pc)['projection'];same(case['parent_output'],parent,'REPORT-VALIDATED-PARENT-OUTPUT')
 binding=case['binding'];require(type(binding) is dict and 'continuity' in binding,'REPORT-BINDING-INPUT')
 expected=basis['fresh']['coverage'].error_report_binding(basis['catalogue'],parent,anchor,binding['continuity']);same(binding,expected,'REPORT-EXPECTED-BINDING')
 return {'scope':copy.deepcopy(parent['scope']),'anchor':copy.deepcopy(anchor),'parent_result':parent,'binding':expected,'outcomes':copy.deepcopy(case['outcomes'])}
def _construct_checked(basis,case):
 v=_premises(basis,case);c=basis['fresh']['coverage'];cat=basis['catalogue'];out=c.error_report_projection(cat,case['projection'],v);c.validate_error_report_projection(cat,case['projection'],v,case['output']);return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(case['anchor']),'projection':out,'runtime_observation':False}
def constructed_projection(data,submitted_catalogue,case):
 exact(case,'REPORT-CONSTRUCTED-INPUT');_,basis=_checked(data,submitted_catalogue);return _construct_checked(basis,case)
def _construct_prior(basis,branch,case):
 exact(case,'REPORT-PRIOR-INPUT');require(type(branch) is str,'REPORT-PRIOR-BRANCH')
 if branch=='cleanup':return basis['prior_module']._construct_checked(basis['prior_basis'],case)
 return basis['prior_module']._construct_prior(basis['prior_basis'],branch,case)
def constructed_prior(data,submitted_catalogue,branch,case):
 _,basis=_checked(data,submitted_catalogue);return _construct_prior(basis,branch,case)
def derive(root=ROOT):
 data=inputs(root);return derive_error_report(data,catalogue(data))
def _receipt_shape(saved):
 require(type(saved) is bytes,'REPORT-RECEIPT-BYTES');v=json.loads(saved)
 require(type(v) is dict and v.get('format')=='I164-CLEANUP-ERROR-REPORT-CORRESPONDENCE-1' and type(v.get('contexts')) is list and len(v['contexts'])==2 and all(type(c) is dict and REQUIRED<=set(c) for c in v['contexts']),'REPORT-MANDATORY-RELATIONS');return v
def _receipt_checked(basis,saved):
 _receipt_shape(saved);require(saved==enc(_assemble(basis['fresh'],_rows(basis),basis)),'REPORT-STALE-OR-ALTERED-RECEIPT');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(saved),'runtime_error_report_chain':'UNAVAILABLE','actual_admission':False}
def validate(root,saved):
 _receipt_shape(saved);data=inputs(root);_,basis=_checked(data,catalogue(data));return _receipt_checked(basis,saved)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
