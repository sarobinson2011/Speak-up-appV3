def inner(data):return data['prior_module'].inner(data['prior_data'])
def sources(data):return data['prior_module'].sources(data['prior_data'])
def manager_state(data):
 h=data['prior_data']['prior_data'];return h['prior_module'].catalogue(h['prior_data'])
def catalogue(data):
 return data['coverage'].compile_client_state(*sources(data),manager_state(data),data['prior_module'].catalogue(data['prior_data']),inner(data)['ctx']['binding'])
def _basis(data):
 fresh=inputs(data['root']);p=fresh['prior_module'];pd=fresh['prior_data'];prior=p.derive_client(pd,p.catalogue(pd))
 saved=(fresh['prior_root']/'results/client-handle-correspondence.json').read_bytes();require(identity(saved)==CLIENT_RECEIPT and enc(prior)==saved,'CLIENT-STATE-PREDECESSOR-RECEIPT')
 return {'fresh':fresh,'prior':prior,'saved':saved,'catalogue':catalogue(fresh),'evidence':dict(inner(fresh)['ctx']['e'])}
def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'CLIENT-STATE-EVIDENCE-TYPES')
 path='evidence/recovery-export-0.json';require(path in candidate,'CLIENT-STATE-MISSING-EXPORT');want=json.loads(basis['evidence'][path]);got=json.loads(candidate[path]);require(type(got) is dict and type(got.get('head')) is str,'CLIENT-STATE-MISSING-HEAD')
 actual=json.loads(bytes.fromhex(got['head']));expected=json.loads(bytes.fromhex(want['head']))
 basis['fresh']['coverage'].state_value_compare(basis['catalogue']['manager_relation'],actual,expected)
 # The same independently validated predecessor supplies HEAD, bindings and all
 # exact evidence. Consistent candidate reports never replace this authority.
 fresh=basis['fresh'];fresh['prior_module']._compare_evidence({'fresh':fresh['prior_data'],'evidence':basis['evidence']},candidate)
def _rows(basis):
 rows=[];cat=basis['catalogue'];fresh=basis['fresh'];c=fresh['coverage'];e=basis['evidence'];path='evidence/recovery-export-0.json';export=json.loads(e[path]);state=json.loads(bytes.fromhex(export['head']))
 for context in basis['prior']['contexts']:
  prior=context['state_return_correspondence'];anchor=prior['validated_state_anchor'];same(cat['manager_relation'],prior['declaration'],'CLIENT-STATE-MANAGER-DECLARATION')
  c.state_value_compare(cat['manager_relation'],anchor['validated_state'],state);same(anchor['instance']['binding'],state['binding'],'CLIENT-STATE-INSTANCE-BINDING')
  require(anchor['record']['artifact']==path and anchor['record']['pointer']=='/head' and {k:anchor['record'][k] for k in ('bytes','sha256')}==identity(e[path]),'CLIENT-STATE-VALIDATED-RECORD')
  links=[{'declaration':d['id'],'source_origin':copy.deepcopy(d['source_origin']),'conditional_value_at_validated_frontier':copy.deepcopy(state),'value_type':copy.deepcopy(d['type']),'observed_value':None,'frame':None,'reference_observation':None} for d in cat['declarations']]
  rows.append({'context':context['context'],'declaration':copy.deepcopy(cat),'validated_state_anchor':copy.deepcopy(anchor),'manager_state_relation':copy.deepcopy(prior),'predecessor_receipt':identity(basis['saved']),
   'conditional_links':links,'reference_copy_relationships':{'same_result_reference':['manager-return','session-return','dispatch-result'],'detached_result_reference':['converted-result','dispatch-return','client-return'],'no_mutable_sharing_between_groups':True,'copy_algorithm':'_data path-wise list/dict recreation, not deepcopy memo','physical_alias_observations':None},
   'invocation_scope':{'context':context['context'],'acquisition':anchor['record']['acquisition'],'instance':copy.deepcopy(anchor['instance']),'frontier':anchor['recovery_occurrence'],'invocation':None,'request_identifier':None,'meaning':'Source-defined state invocation has no packet/request/journal requirement. New constructed invocations remain distinct; acquisition is an evidence frontier, not an actual call time.'},
   'separate_observer':copy.deepcopy(prior['separate_observer']),'observer_to_forwarding_links':None,'runtime_forwarding_links':None,'actual_client_state_call_count':None,'classification':'UNKNOWN','multiplicity':None,'ordinal':None,
   'gap':'No complete Client/dispatcher/session/manager state-return or conversion trace. The separate frameless observer is retained without invented frame, parent, alias or chain joins.'})
 return rows
def _check_rows(basis,claims,rows):
 require(type(claims) is list and len(claims)==len(rows)==2,'CLIENT-STATE-CONTEXT-DOMAIN')
 for got,want in zip(claims,rows):
  require(type(got) is dict and set(got)==set(want) and got['context']==want['context'],'CLIENT-STATE-CONTEXT-FIELDS')
  basis['fresh']['coverage'].state_value_compare(basis['catalogue']['manager_relation'],got['validated_state_anchor']['validated_state'],want['validated_state_anchor']['validated_state'])
  links=got['conditional_links'];require(type(links) is list and len(links)==len(want['conditional_links']),'CLIENT-STATE-LINK-COVERAGE')
  for row,expected in zip(links,want['conditional_links']):
   require(type(row) is dict and set(row)==set(expected) and row['declaration']==expected['declaration'],'CLIENT-STATE-LINK-FIELDS')
   basis['fresh']['coverage'].state_value_compare(basis['catalogue']['manager_relation'],row['conditional_value_at_validated_frontier'],want['validated_state_anchor']['validated_state']);same(row,expected,'CLIENT-STATE-LINK-CORRESPONDENCE')
  same(got,want,'CLIENT-STATE-CONTEXT-CORRESPONDENCE')
def _checked(data,submitted_catalogue,claims=None,evidence=None):
 basis=_basis(data);same(submitted_catalogue,basis['catalogue'],'CLIENT-STATE-SOURCE-CATALOGUE');d=inner(data);fd=inner(basis['fresh'])
 require(sources(data)==sources(basis['fresh']) and d['ctx']['c']==fd['ctx']['c'],'CLIENT-STATE-CANDIDATE-SOURCES');same(d['ctx']['binding'],fd['ctx']['binding'],'CLIENT-STATE-CANDIDATE-BINDING')
 _compare_evidence(basis,d['ctx']['e'] if evidence is None else evidence);rows=_rows(basis)
 if claims is not None:_check_rows(basis,claims,rows)
 return rows,basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def _assemble(data,rows,basis):
 result=copy.deepcopy(basis['prior']);result['format']='I164-CLIENT-STATE-RETURN-CORRESPONDENCE-1';result['prior_client_handle_components']=result.pop('extension_components');result['prior_client_handle_receipt']=identity(basis['saved'])
 result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for context,row in zip(result['contexts'],rows):require(context['context']==row['context'],'CLIENT-STATE-DERIVATION-CONTEXT');context['client_state_return_correspondence']=copy.deepcopy(row)
 result['new_client_state_limits']={'static_conditional_correspondence':True,'runtime_chain':'UNAVAILABLE','observer_to_chain_join':None,'actual_call_count':None,'copy_alias_observations':None,'request_independent':True,'constructed_cases_not_runtime':True,'_data_is_not_deepcopy':True,'no_new_HEAD_authentication_rule':True,'complete_repetition_coverage':False,'outer_callback_cleanup_projection':'PARTIAL; unchanged scope','all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}
 return result
def derive_client_state(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);return _assemble(data,rows,basis)
def invocation_scope(anchor,invocation):
 require(type(invocation) is str and bool(invocation),'CLIENT-STATE-INVOCATION')
 return {'context':anchor['context'],'acquisition':anchor['record']['acquisition'],'instance':copy.deepcopy(anchor['instance']),'frontier':anchor['recovery_occurrence'],'invocation':invocation}
def _construct_checked(basis,rows,case):
 require(type(case) is dict and set(case)=={'kind','context','anchor','projection'} and case['kind']=='CONSTRUCTED-CONDITIONAL-CLIENT-STATE','CLIENT-STATE-CONSTRUCTED-CASE')
 found=[r for r in rows if r['context']==case['context']];require(len(found)==1,'CLIENT-STATE-CONSTRUCTED-CONTEXT');anchor=found[0]['validated_state_anchor'];same(case['anchor'],anchor,'CLIENT-STATE-CONSTRUCTED-ANCHOR')
 p=case['projection'];require(type(p) is dict and type(p.get('occurrence')) is str,'CLIENT-STATE-CONSTRUCTED-PROJECTION');scope=invocation_scope(anchor,p['occurrence'])
 value=basis['fresh']['coverage'].client_state_projection(basis['catalogue'],p,{'scope':scope,'state':anchor['validated_state']})
 return {'kind':'CONSTRUCTED-CONDITIONAL-CLIENT-STATE','context':case['context'],'anchor':copy.deepcopy(anchor),'projection':value,'runtime_observation':False}
def constructed_projection(data,submitted_catalogue,case):
 rows,basis=_checked(data,submitted_catalogue);return _construct_checked(basis,rows,case)
def derive(root=ROOT):
 data=inputs(root);return derive_client_state(data,catalogue(data))
def validate(root,saved):
 require(type(saved) is bytes,'CLIENT-STATE-RECEIPT-BYTES')
 candidate=json.loads(saved);require(type(candidate) is dict and candidate.get('format')=='I164-CLIENT-STATE-RETURN-CORRESPONDENCE-1' and type(candidate.get('contexts')) is list and len(candidate['contexts'])==2 and all(type(c) is dict and 'client_state_return_correspondence' in c for c in candidate['contexts']),'CLIENT-STATE-MANDATORY-RELATION')
 require(saved==enc(derive(root)),'STALE-OR-ALTERED-CLIENT-STATE-CORRESPONDENCE')
 return {'result':'PASS','contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'receipt':identity(saved),'runtime_client_state_chain':'UNAVAILABLE','actual_admission':False}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
