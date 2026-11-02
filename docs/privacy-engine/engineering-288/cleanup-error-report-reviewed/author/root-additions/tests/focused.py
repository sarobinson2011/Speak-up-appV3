"""New bounded line172 controls, one actual fresh recovered public positive."""
from pathlib import Path
import sys,signal,traceback,ast
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
import cases as F
root=Path(sys.argv[1]).resolve();r=Records(sys.argv[2]);failure=None
CORE='actual-authenticated-basis _construct_checked core (revalidates selected parent)'
OUT='producer output-comparison core with actual-authenticated predecessor-validated premises'
SEM='actual-authenticated-basis semantic catalogue/claims core'
INPUT='exact-type input gate before constructed predecessor validation'
def changed(value,path,new):
 v=D(value);q=v
 for k in path[:-1]:q=q[k]
 q[path[-1]]=new;return v
def outcomes(terminal):return F.outcomes(cat,terminal)
def submitted(fx,terminal):
 v=D(fx['projection']);v['outcomes']=outcomes(terminal);out=c.error_report_projection(cat,v,v);return v,out
def check_frontier(fx,control,origin,terminal):
 v,out=submitted(fx,terminal);assert c.validate_error_report_projection(cat,v,v,out);assert F.oracle(out,control,origin,terminal);return v,out
def deadline(s,f):raise TimeoutError('REPORT-SOFT-DEADLINE; finalization reserve')
class S(str):pass
class L(list):pass
class I(int):pass
try:
 r.save('environment.json',environment());r.save('input-verification.json',verify_root(root));monitor,captures=guard(root,r.path,r)
 m=module(root/'code/correspondence.py');monitor(m);data=m.inputs(root);cat=m.catalogue(data);c=data['coverage'];saved=(root/'receipts/prepared-error-report.json').read_bytes()
 p=root/'retained/cleanup';old=(p/'code/managed_coverage.py').read_bytes();new=(root/'code/managed_coverage.py').read_bytes()
 r.yes('reviewed producer prefix including EC01 unchanged',lambda:new.startswith(old),'exact source-prefix bytes')
 source=(root/'source-evidence/lab_bootstrap.py').read_bytes();order,origins=F.source_oracle(source)
 r.yes('independent defining-source evaluation order and anchors',lambda:cat['source']['order']==order and all({k:cat['source']['stages'][n][k] for k in ('site','expression')}==v for n,v in origins.items()),'defining-source AST; independent of generated catalogue')
 r.yes('mandatory relation and preserved predecessor receipt pins',lambda:m.RELATION in m.REQUIRED and m.PREDECESSOR_RECEIPT=={'bytes':13408039,'sha256':'4b84be0804b2a0a5dd0cef421403fa2e608a703899c97196f4063b11b04df952'},'adapter constants/source')
 r.save('independent-source-expectations.json',{'order':order,'origins':origins,'normal_terminal_exception':True,'termination_unobserved_terminal':None,'no_handler_exit':True})
 signal.signal(signal.SIGALRM,deadline);signal.setitimer(signal.ITIMER_REAL,max(1,3900-(time.monotonic()-r.start)))
 r.event('actual-current-public-validation-start',receipt=identity(saved),control_deadline_seconds=3900,hard_timeout_seconds=4500)
 public=m.validate(root,saved);r.save('actual-public-result.json',public)
 r.yes('fresh recovered public positive validates new prepared receipt',lambda:public['result']=='PASS' and public['contexts']==list(m.CONTEXTS) and public['receipt']==identity(saved),'full current public positive')
 assert len(captures)==1;basis=captures.pop();c=basis['fresh']['coverage'];cat=basis['catalogue'];data=basis['fresh'];r.save('predecessor-public-result.json',basis['public_predecessor'])
 r.yes('actual unchanged reviewed predecessor public positive',lambda:basis['public_predecessor']['result']=='PASS' and basis['public_predecessor']['receipt']==m.PREDECESSOR_RECEIPT,'actual unchanged predecessor public positive')
 r.yes('actual authenticated assembly equals new receipt',lambda:m.enc(m._assemble(data,m._rows(basis),basis))==saved,'authenticated-basis receipt assembly comparison')
 r.save('validated-receipt-identity.json',identity(saved));r.event('new-focused-cores-start',full_public_negative_derivations=0)
 fixtures=[];frontiers=[]
 for idx in (0,1):
  for control in (False,True):
   tag=f'{idx}:{control}';normal_by_origin={}
   for origin in ('close','append'):
    pc=F.parent_case(m,basis,idx,control,origin,'report-'+tag+'-'+origin)
    fx=F.from_parent(m,basis,pc);normal_by_origin[origin]=fx
    got=r.yes('legitimate selected '+tag+origin,lambda fx=fx:m._construct_checked(basis,fx),CORE)
    r.yes('source-grounded pending/error/list oracle '+tag+origin,lambda got=got: F.oracle(got['projection'],control,origin),'independent source-grounded outcome oracle over authenticated result')
    r.save('fixtures/'+tag.replace(':','-')+'-'+origin+'.json',fx);fixtures.append({'context':fx['context'],'control':control,'origin':origin,'invocation':fx['invocation'],'output':identity(m.enc(got['projection']))})
    for label,path,value in [
     ('old false terminal',['terminal_python_exception_in_model'],False),('unknown terminal on normal reporting',['terminal_python_exception_in_model'],None),
     ('discard original constructor',['earlier_constructor_exception'],None),('invent report bytes',['error_item_in_model',1,'formatted_bytes'],'invented'),
     ('confuse close failure',['close_itself_failed_established_in_model'],not (origin=='close')),('claim handler exit',['handler_exit_established'],True),
     ('claim final rethrow',['final_rethrow_established'],True),('forget partial effects',['cleanup_list_state','prior_partial_effects'],'ERASED'),
     ('wrong exact false type',['known_false_flags_preserved','new_authorization'],0)]:
     bad=changed(fx['output'],path,value)
     r.no('altered output '+tag+origin+label,lambda bad=bad,fx=fx:c.validate_error_report_projection(cat,fx['projection'],fx['projection'],bad),OUT,'REPORT-OUTPUT-CORRESPONDENCE')
    for label,path,value in [
     ('wrong token',['binding','references','token'],{'wrong':'token'}),('wrong owner',['binding','references','owner'],{'wrong':'owner'}),
     ('wrong selected error',['binding','selected_failure','reference'],'substitution'),('wrong protected origin',['binding','failure_occurrence','source','site'],'0:0:0:0:Call'),
     ('wrong list',['binding','cleanup_list','symbol'],'other-list'),('wrong name',['binding','selected_name'],'raw'),('wrong instance',['anchor','context'],'other-context'),
     ('wrong invocation',['invocation'],'other-invocation')]:
     bad=changed(fx,path,value);r.no('binding rejection '+tag+origin+label,lambda bad=bad:m._construct_checked(basis,bad),CORE)
    bad=D(fx);bad['projection']['binding']['selected_failure']['reference']='mixed';bad['output']['selected_cleanup_error']['reference']='mixed'
    r.no('coordinated returned selected-error substitution '+tag+origin,lambda bad=bad:m._construct_checked(basis,bad),CORE)
    got['projection']['binding']['references']['owner'].clear();got['projection']['cleanup_list_state'].clear();got['projection']['validated_parent'].clear()
    r.yes('nested returned mutations do not alter expectations '+tag+origin,lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'],CORE)
   fx=normal_by_origin['append']
   for stage in ('handler-type-evaluation','caught-error-binding-attempt','error-name-attribute','error-str-call-attempt','report-append-attempt','report-append-complete'):
    for kind in ('raise','process-termination','unobserved'):
     terminal=(stage,kind);v,out=r.yes('frontier '+tag+str(terminal),lambda terminal=terminal:check_frontier(fx,control,'append',terminal),OUT+' + independent source oracle')
     bad=changed(out,['terminal_python_exception_in_model'],False if kind=='raise' else True)
     r.no('wrong frontier classification '+tag+str(terminal),lambda v=v,bad=bad:c.validate_error_report_projection(cat,v,v,bad),OUT,'REPORT-OUTPUT-CORRESPONDENCE')
     frontiers.append({'context':fx['context'],'control':control,'stage':stage,'outcome':kind,'terminal':out['terminal_python_exception_in_model'],'prior_partial_effects':out['cleanup_list_state']['prior_partial_effects'],'append_completed':out['report_append_completed_in_model']})
   for label,mutator in [
    ('subclassed reason value',lambda v:v['binding'].__setitem__('caught_name',S(v['binding']['caught_name']))),
    ('subclassed literal key',lambda v:v['output'].__setitem__(S('handler_exit_established'),v['output'].pop('handler_exit_established'))),
    ('subclassed outcomes container',lambda v:v.__setitem__('outcomes',L(v['outcomes']))),
    ('nested exact int subclass',lambda v:v['output'].__setitem__('handler_exit_established',I(0)))]:
    bad=D(fx);mutator(bad);r.no('exact types '+tag+label,lambda bad=bad:m._construct_checked(basis,bad),INPUT,'REPORT-CONSTRUCTED-INPUT')
   bad=D(fx);bad['outcomes'][4:6]=reversed(bad['outcomes'][4:6]);bad['projection']['outcomes']=D(bad['outcomes']);r.no('reordered binding stages '+tag,lambda bad=bad:m._construct_checked(basis,bad),CORE,'REPORT-STEP-ORDER')
   bad=D(fx);bad['outcomes'].pop(5);bad['projection']['outcomes']=D(bad['outcomes']);r.no('missing binding completion '+tag,lambda bad=bad:m._construct_checked(basis,bad),CORE,'REPORT-STEP-ORDER')
   pc=F.parent_case(m,basis,idx,control,'outside','outside-'+tag)
   r.no('outside try failure cannot acquire handler '+tag,lambda pc=pc:F.from_parent(m,basis,pc),CORE,'REPORT-PROTECTED-FAILURE')
   pc=F.parent_case(m,basis,idx,control,'normal','normal-'+tag)
   r.no('normal predecessor cannot enter failure handler '+tag,lambda pc=pc:F.from_parent(m,basis,pc),CORE,'REPORT-PARENT-FAILURE')
   unknown=F.from_parent(m,basis,fx['parent_case'],continuity='UNESTABLISHED')
   r.yes('unknown continuity establishes no handler progress '+tag,lambda unknown=unknown:m._construct_checked(basis,unknown)['projection']['handler_entry_completed_in_model'] is False,CORE)
   # Mandatory relation gate invokes public entry but never begins derivation.
   receipt=json.loads(saved);receipt['contexts'][idx].pop(m.RELATION)
   r.no('missing mandatory relation public gate '+tag,lambda receipt=receipt:m.validate(root,m.enc(receipt)),'public required-relation gate before inputs/derivation','REPORT-MANDATORY-RELATIONS')
   badcat=D(cat);badcat['declarations'].pop(5);badcat['source']['order'].pop(5);badcat['source']['stages'].pop('caught-error-binding-complete')
   claims=m._rows(basis)
   for claim in claims:claim['declaration']=D(badcat)
   r.no('coordinated catalogue/claims omission '+tag,lambda badcat=badcat,claims=claims:m._check_candidate(basis,data,badcat,claims),SEM,'REPORT-CATALOGUE-SOURCE')
   claims=m._rows(basis);claims[idx]['scope']['context']='wrong'
   r.no('wrong semantic context scope '+tag,lambda claims=claims:m._check_rows(basis,claims),SEM,'REPORT-SEMANTIC-CORRESPONDENCE')
 # Every source stage has an exceptional frontier control, without replaying old suites.
 fx=normal_by_origin['append']
 for stage in order:
  r.yes('source stage raise '+stage,lambda stage=stage:check_frontier(fx,True,'append',(stage,'raise')),OUT+' + defining-source coverage')
 for label,mutator in [('wrong receipt field',lambda q:q['contexts'][0][m.RELATION].__setitem__('handler_exit_established',True)),('both context coordinated origins',lambda q:[r['declaration']['source'].__setitem__('catch_name','e') for r in [x[m.RELATION] for x in q['contexts']]])]:
  q=json.loads(saved);mutator(q);r.no(label,lambda q=q:m._receipt_checked(basis,m.enc(q)),'authenticated-basis receipt-comparison core; no public negative derivation','REPORT-STALE-OR-ALTERED-RECEIPT')
 rows=m._rows(basis);rows[0]['declaration']['source']['order'].clear();rows[1]['reference_basis'].clear()
 r.yes('returned context mutations leave both expected contexts intact',lambda:m._check_candidate(basis,data,cat)==m._rows(basis) and all(x['declaration']['source']['order']==order for x in m._rows(basis)),SEM)
 r.save('fixtures-index.json',fixtures);r.save('frontier-summary.json',frontiers)
 r.save('validation-layers.json',{'full_current_public_positive':1,'actual_unchanged_predecessor_public_positive':1,'public_required_relation_negative_calls':4,'full_public_negative_derivations':0,'core_negatives':'Rows individually identify exact-type gates, predecessor-revalidated constructed cores, actual-authenticated semantic/output cores or receipt comparisons. No core negative is a full public derivation.'})
 signal.setitimer(signal.ITIMER_REAL,0);r.event('finalization-start',reserved_seconds=4500-(time.monotonic()-r.start));r.save('final-verification.json',verify_root(root));r.event('finished')
except BaseException:
 failure=traceback.format_exc();r.save('failure.json',{'traceback':failure});raise
finally:
 signal.setitimer(signal.ITIMER_REAL,0);r.finish(failure,requests=0,acquisitions=0,database_connections=0,session_operations=0,Git_saves=0,completed_campaigns_replayed=False)
