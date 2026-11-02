"""Only new loop controls. One fresh recovered full public positive; no historical suite replay."""
from pathlib import Path
import sys,signal,traceback,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
import cases as F
root=Path(sys.argv[1]).resolve();r=Records(sys.argv[2]);failure=None
CORE='authenticated-basis constructed core; selected parent revalidated by unchanged predecessor'
OUT='authenticated-basis producer output-comparison core with validated parent'
SEM='authenticated-basis semantic catalogue/claims core'
def changed(v,path,new):
 v=D(v);q=v
 for k in path[:-1]:q=q[k]
 q[path[-1]]=new;return v
def frontier(fx,control,origin,terminal):
 v=D(fx['projection']);v['outcomes']=F.outcomes(cat,terminal);out=c.cleanup_loop_projection(cat,v,v);assert c.validate_cleanup_loop_projection(cat,v,v,out);assert F.oracle(out,control,origin,terminal);return v,out
def deadline(s,f):raise TimeoutError('LOOP-SOFT-DEADLINE; finalization reserve')
class S(str):pass
class L(list):pass
class I(int):pass
try:
 r.save('environment.json',environment());r.save('input-verification.json',verify_root(root));monitor,captures=guard(root,r.path,r)
 m=module(root/'code/correspondence.py');monitor(m);data=m.inputs(root);cat=m.catalogue(data);c=data['coverage'];saved=(root/'receipts/prepared-cleanup-loop.json').read_bytes()
 old=(root/'retained/report/code/managed_coverage.py').read_bytes();new=(root/'code/managed_coverage.py').read_bytes()
 r.yes('reviewed entire producer prefix unchanged including LD01/EC01 support',lambda:new.startswith(old),'exact retained prefix bytes')
 order,origins=F.source_oracle((root/'source-evidence/lab_bootstrap.py').read_bytes())
 r.yes('independent source traversal confirms exact two-entry final loop and stop',lambda:cat['source']['order']==order and all({k:cat['source']['stages'][n][k] for k in ('site','expression')}==v for n,v in origins.items()),'independent defining-source AST oracle')
 r.yes('source count order index and guard oracle',lambda:cat['source']['entry_count']==2 and cat['source']['selected_index']==1 and cat['source']['next_index']==2 and [[v['name'],v['slot']] for v in cat['source']['ordered_inputs']]==[['raw','raw'],['managed','managed']] and cat['source']['required_guard_results']=={'raw':False,'managed':True},'independent defining-source AST oracle')
 r.yes('mandatory extension and exact predecessor receipt',lambda:m.RELATION in m.REQUIRED and m.PREDECESSOR_RECEIPT=={'bytes':15694813,'sha256':'726e80b38028c6e3958b4e346696a7296307ca0109b65e17318eb7f580d6072f'},'adapter source/constants')
 r.save('independent-source-expectations.json',{'order':order,'origins':origins,'entry_order':['raw','managed'],'selected_index':1,'entry_count':2,'normal_terminal_python_exception':True,'termination_unobserved':None,'stop_before_line':174})
 signal.signal(signal.SIGALRM,deadline);signal.setitimer(signal.ITIMER_REAL,max(1,3900-(time.monotonic()-r.start)))
 r.event('actual-current-public-validation-start',receipt=identity(saved),control_deadline_seconds=3900,hard_timeout_seconds=4500)
 public=m.validate(root,saved);r.save('actual-public-result.json',public)
 r.yes('fresh recovered full public positive for new prepared receipt',lambda:public['result']=='PASS' and public['receipt']==identity(saved),'full current public positive')
 assert len(captures)==1;basis=captures.pop();c=basis['fresh']['coverage'];cat=basis['catalogue'];data=basis['fresh'];r.save('predecessor-public-result.json',basis['public_predecessor'])
 r.yes('actual unchanged line172 predecessor public positive',lambda:basis['public_predecessor']['result']=='PASS' and basis['public_predecessor']['receipt']==m.PREDECESSOR_RECEIPT,'actual unchanged predecessor public validation')
 r.yes('new prepared receipt equals authenticated assembly',lambda:m.enc(m._assemble(data,m._rows(basis),basis))==saved,'authenticated-basis receipt comparison')
 r.save('validated-receipt-identity.json',identity(saved));r.event('focused-cores-start',full_public_negative_derivations=0)
 fixture_index=[];frontiers=[]
 for idx in (0,1):
  for control in (False,True):
   tag=f'{idx}-{control}'
   for origin in ('close','append'):
    label=tag+'-'+origin;fx=F.normal(m,basis,idx,control,origin,'loop-'+label)
    got=r.yes('normal explicit continuation '+label,lambda fx=fx:m._construct_checked(basis,fx),CORE)
    r.yes('independent pending/name/list and exhaustion oracle '+label,lambda got=got:F.oracle(got['projection'],control,origin),'independent source/language oracle')
    r.save('fixtures/'+label+'.json',fx);fixture_index.append({'context':fx['context'],'control':control,'origin':origin,'invocation':fx['invocation'],'output':identity(m.enc(got['projection']))})
    for name,path,value in [
     ('normal loses pending constructor',['terminal_python_exception_in_model'],False),('wrong pending error',['last_pending_error_in_model'],fx['output']['retained_cleanup_error_evidence']),('erase retained cleanup error',['retained_cleanup_error_evidence'],None),
     ('caught name stays bound',['caught_name_lifetime','last_acknowledged_binding'],'BOUND selected cleanup error'),('physical destruction',['caught_name_lifetime','physical_destruction_established'],True),
     ('discard partial effects',['cleanup_list_state','prior_partial_effects'],'NONE'),('complete contents',['cleanup_list_state','complete_contents_established'],True),('lose close fact',['close_normal_return_completed_in_model'],not(origin=='append')),
     ('line174 attempt',['line174_evaluation_established'],True),('invent extra body',['additional_body_execution_established'],True),('exhaustion becomes propagating error',['ordinary_exhaustion_is_new_propagating_error'],True),('false flag exact type',['known_false_flags_preserved','new_authorization'],0)]:
     bad=changed(fx['output'],path,value);r.no('output '+label+' '+name,lambda bad=bad,fx=fx:c.validate_cleanup_loop_projection(cat,fx['projection'],fx['projection'],bad),OUT,'LOOP-OUTPUT-CORRESPONDENCE')
    for name,path,value in [('wrong token',['binding','references','token'],{'wrong':'token'}),('wrong owner',['binding','references','owner'],{'wrong':'owner'}),('wrong error',['binding','selected_cleanup_error','reference'],'other'),('wrong invocation',['invocation'],'other'),('wrong instance',['anchor','context'],'other'),('wrong handler',['binding','handler_origin','site'],'0:0:0:0:ExceptHandler'),('wrong list',['binding','cleanup_list','symbol'],'other'),('wrong count',['binding','loop','entry_count'],3),('wrong index',['binding','loop','selected_index'],0),('wrong next index',['binding','loop','next_index'],1),('raw not skipped',['binding','loop','raw_body_skipped'],False)]:
     bad=changed(fx,path,value);r.no('bound premise '+label+' '+name,lambda bad=bad:m._construct_checked(basis,bad),CORE)
    bad=D(fx);bad['binding']['loop']['ordered_values'].reverse();bad['projection']['binding']=D(bad['binding']);bad['output']['binding']=D(bad['binding'])
    r.no('coordinated substituted input order '+label,lambda bad=bad:m._construct_checked(basis,bad),CORE,'LOOP-EXPECTED-BINDING')
    bad=D(fx);bad['parent_output']['report_append_completed_in_model']=False;bad['projection']['parent_result']=D(bad['parent_output'])
    r.no('false predecessor completion '+label,lambda bad=bad:m._construct_checked(basis,bad),CORE,'LOOP-VALIDATED-PARENT-OUTPUT')
    for name,oo in [('missing exit',[x for x in fx['outcomes'] if x['stage']!='inner-handler-exit-complete']),('reordered advance',list(reversed(fx['outcomes']))),('premature exhaustion',fx['outcomes'][4:]),('missing explicit continuation',[]),('extra body',fx['outcomes']+[{'stage':'managed-body-again','outcome':'normal'}]),('ordinary advance called exhaustion',[{'stage':x['stage'],'outcome':('exhausted' if x['stage']=='final-iterator-advance-attempt' else x['outcome'])} for x in fx['outcomes']])]:
     bad=D(fx);bad['outcomes']=D(oo);bad['projection']['outcomes']=D(oo);r.no('ordering '+label+' '+name,lambda bad=bad:m._construct_checked(basis,bad),CORE)
    for stage in order:
     for kind in ('raise','catchable-interruption','process-termination','unobserved'):
      terminal=(stage,kind);v,out=r.yes('frontier '+label+' '+stage+' '+kind,lambda terminal=terminal:frontier(fx,control,origin,terminal),OUT+' + independent oracle')
      bad=changed(out,['loop_completion_established'],True);r.no('false completion '+label+' '+stage+' '+kind,lambda v=v,bad=bad:c.validate_cleanup_loop_projection(cat,v,v,bad),OUT,'LOOP-OUTPUT-CORRESPONDENCE')
      frontiers.append({'context':fx['context'],'control':control,'origin':origin,'stage':stage,'outcome':kind,'terminal':out['terminal_python_exception_in_model'],'exit':out['handler_exit_established'],'prior_partial_effects':out['cleanup_list_state']['prior_partial_effects']})
    for name,mutator in [('nested str subclass',lambda q:q['binding'].__setitem__('selected_name',S('managed'))),('subclassed literal key',lambda q:q['output'].__setitem__(S('loop_completion_established'),q['output'].pop('loop_completion_established'))),('list subclass',lambda q:q.__setitem__('outcomes',L(q['outcomes']))),('int subclass',lambda q:q['binding']['loop'].__setitem__('entry_count',I(2)))]:
     bad=D(fx);mutator(bad);r.no('exact type '+label+' '+name,lambda bad=bad:m._construct_checked(basis,bad),'exact-type constructed input gate','LOOP-CONSTRUCTED-INPUT')
    got['projection']['binding']['references']['owner'].clear();got['projection']['cleanup_list_state'].clear();got['projection']['validated_parent'].clear()
    r.yes('nested returned mutations cannot change expectation '+label,lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'],CORE)
    unknown=F.from_parent(m,basis,fx['parent_case'],continuity='UNESTABLISHED')
    r.yes('unknown continuity no handler exit or exhaustion '+label,lambda unknown=unknown:m._construct_checked(basis,unknown)['projection']['handler_exit_established'] is False and unknown['output']['terminal_python_exception_in_model'] is None,CORE)
   receipt=json.loads(saved);receipt['contexts'][idx].pop(m.RELATION)
   r.no('missing mandatory relation '+tag,lambda receipt=receipt:m.validate(root,m.enc(receipt)),'public required-relation gate before inputs/derivation','LOOP-MANDATORY-RELATIONS')
 # Source expectations come from independently parsed source, never submitted catalogue.
 for name,edit in [('omit exit',lambda q:(q['source']['order'].remove('inner-handler-exit-complete'),q['declarations'].pop(1))),('wrong count',lambda q:q['source'].__setitem__('entry_count',3)),('wrong guard',lambda q:q['source']['required_guard_results'].__setitem__('raw',True)),('reverse inputs',lambda q:q['source']['ordered_inputs'].reverse()),('wrong origin',lambda q:q['source']['stages']['ordinary-iterator-exhaustion'].__setitem__('site','174:0:174:1:Call'))]:
  bad=D(cat);edit(bad);claims=m._rows(basis)
  for row in claims:row['declaration']=D(bad)
  r.no('coordinated catalogue claims '+name,lambda bad=bad,claims=claims:m._check_candidate(basis,data,bad,claims),SEM,'LOOP-CATALOGUE-SOURCE')
  r.no('source-derived catalogue oracle '+name,lambda bad=bad:c.validate_cleanup_loop(*m.sources(data),basis['prior_basis']['catalogue'],basis['prior_basis']['prior_basis']['catalogue'],bad),'source-recomputed declaration comparison','LOOP-SOURCE-CORRESPONDENCE')
 for idx in (0,1):
  claims=m._rows(basis);claims[idx]['scope']['context']='other';r.no('wrong semantic context '+str(idx),lambda claims=claims:m._check_rows(basis,claims),SEM,'LOOP-SEMANTIC-CORRESPONDENCE')
  q=json.loads(saved);q['contexts'][idx][m.RELATION]['line174_evaluation_established']=True
  r.no('receipt claims line174 '+str(idx),lambda q=q:m._receipt_checked(basis,m.enc(q)),'authenticated-basis receipt comparison; not full public negative derivation','LOOP-STALE-OR-ALTERED-RECEIPT')
 rows=m._rows(basis);rows[0]['declaration']['source']['order'].clear();rows[1]['reference_basis'].clear()
 r.yes('both context expectations survive returned nested mutation',lambda:m._check_candidate(basis,data,cat)==m._rows(basis) and all(x['declaration']['source']['order']==order for x in m._rows(basis)),SEM)
 r.save('fixtures-index.json',fixture_index);r.save('frontier-summary.json',frontiers)
 r.save('validation-layers.json',{'full_current_public_positive':1,'actual_unchanged_predecessor_public_positive':1,'public_required_relation_negatives':4,'full_public_negative_derivations':0,'core_negatives':'Individually labelled; reused actual authenticated basis is not another public derivation'})
 signal.setitimer(signal.ITIMER_REAL,0);r.event('finalization-start');r.save('final-verification.json',verify_root(root));r.event('finished')
except BaseException:
 failure=traceback.format_exc();r.save('failure.json',{'traceback':failure});raise
finally:
 signal.setitimer(signal.ITIMER_REAL,0);r.finish(failure,requests=0,acquisitions=0,database_connections=0,session_operations=0,Git_saves=0,completed_campaigns_replayed=False)
