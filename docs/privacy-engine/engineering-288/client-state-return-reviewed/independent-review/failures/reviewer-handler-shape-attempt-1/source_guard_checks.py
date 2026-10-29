from pathlib import Path
import ast,copy,json,sys,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None
try:
 monitor=guard(root);m=module(root/'code/correspondence.py');monitor(m);d=m.inputs(root);cat=m.catalogue(d);c=d['coverage'];launcher,entry=m.sources(d);et=ast.parse(entry);dispatch=next(n for n in et.body if isinstance(n,ast.FunctionDef) and n.name=='_dispatch');tr=next(n for n in dispatch.body if isinstance(n,ast.Try));data=next(n for n in et.body if isinstance(n,ast.FunctionDef) and n.name=='_data')
 def site(n):return f'{n.lineno}:{n.col_offset}:{n.end_lineno}:{n.end_col_offset}:{type(n).__name__}'
 expected_guard=[{'kind':'try','region':'body','handlers':[ast.unparse(x.type) for x in tr.handlers]}]
 for stage,index in [('operation-check',1),('session-call',2),('state-shape',3),('conversion',4),('dispatch-return',4)]:
  s=cat['source']['stages'][stage]
  rec.check('AST-derived dispatch catch '+stage,lambda s=s:s['guards']==expected_guard)
  cont=s['continuation'];rec.check('AST-derived normal continuation '+stage,lambda cont=cont,index=index:[v['site'] for v in cont[0]['normal_prefix']]==[site(n) for n in dispatch.body[:2]] and [v['site'] for v in cont[1]['normal_prefix']]==[site(n) for n in tr.body[:index]])
 for stage in ['client-call','client-return','owner-lookup','owner-guard','manager-call','session-return','fixed-failure']:
  rec.check('source has no direct dispatch try guard '+stage,lambda stage=stage:not any(g.get('kind')=='try' and g.get('region')=='body' for g in cat['source']['stages'][stage]['guards']))
 rec.check('handler attribution remains outside own protected try',lambda:cat['source']['stages']['retain-error']['guards']==[{'kind':'handler','type':'BaseException'}])
 for label,mut in [('weaken-shape',lambda x:x['source'].update(state_shape_guard='True')),('omit-guard',lambda x:x['source']['stages']['conversion'].update(guards=[])),('reorder-prefix',lambda x:x['source']['stages']['conversion']['continuation'][1]['normal_prefix'].reverse()),('change-type',lambda x:x['source']['data_primitives'].append('float')),('deepcopy-semantics',lambda x:x['copy_semantics'].update(algorithm='deepcopy memo')),('omit-hop',lambda x:x['ordered_hops'].pop())]:
  x=copy.deepcopy(cat);mut(x);rec.reject('source validation rejects '+label,lambda x=x:c.validate_client_state(launcher,entry,m.manager_state(d),d['prior_module'].catalogue(d['prior_data']),m.inner(d)['ctx']['binding'],x),'CLIENT-STATE-SOURCE-CORRESPONDENCE')
 cases=json.loads((Path(sys.argv[3])/'constructed-cases.json').read_bytes())
 for case_rec in cases:
  case=case_rec['input'];p=case['projection'];state=case['anchor']['validated_state'];validated={'scope':p['scope'],'state':state};ctx=case['context']
  for label,mut in [('missing-root-field',lambda x:x.pop('seq')),('extra-root-field',lambda x:x.update(extra=None)),('state-list',None),('nested-list-for-dict',lambda x:x.update(counts=[])),('nested-None',lambda x:x.update(resources=None)),('wrong-integer-type',lambda x:x.update(seq=0.0))]:
   q=copy.deepcopy(p)
   if mut:mut(q['manager_case']['returned']['underlying']['value'])
   else:q['manager_case']['returned']['underlying']['value']=[]
   rec.reject('exact state shape '+label+' '+ctx,lambda q=q:c.client_state_projection(cat,q,validated))
  old=copy.deepcopy(case_rec['result']);old['outcome_classification'].update(modeled_kind='process-termination',terminal_python_exception_in_model=None);old['completion']='process-termination';old['outside_catch_failure']=False
  rec.reject('coordinated terminal claims cannot replace normal source path '+ctx,lambda old=old:c.validate_client_state_projection(cat,p,validated,old),'PROJECTION-CORRESPONDENCE')
 rec.save('guard-audit.json',{'source':identity(entry),'protected_state_stages':['operation-check','session-call','state-shape','conversion','dispatch-return'],'dynamic_protected_callee_stages':['manager-call','session-return'],'caller_or_prefix_or_helper_outside':['client-call','client-return','owner-lookup','owner-guard','fixed-failure'],'handler_outside_own_catch':'retain-error','all_source_guards_and_normal_prefix_order_independently_checked':True})
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error)
