from pathlib import Path
import sys,json,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from cases import *
root=Path(sys.argv[1]).resolve();r=Records(sys.argv[2]);error=None
class S(str):pass
class L(list):pass
class M(dict):pass
try:
 r.save('input-verification.json',verify_root(root));monitor,captures=guard(root,r.path,r);m=module(root/'code/correspondence.py');monitor(m)
 saved=(root/'results/primary/launcher-details.json').read_bytes();r.event('full-current-public-validation-start',actual_unchanged_predecessor_public_required=True)
 public=m.validate(root,saved);r.save('public-result.json',public)
 r.yes('fresh recovered full current public accepts both contexts',lambda:public['result']=='PASS' and public['contexts']==list(m.CONTEXTS) and public['actual_admission'] is False)
 assert len(captures)==1;b=captures.pop();data=b['fresh'];cat=b['catalogue'];c=data['coverage'];rows=m._rows(b);before=m.enc(rows)
 r.yes('candidate monitoring slot released after actual predecessor validation',lambda:sys.monitoring.get_tool(2) is None and sys.monitoring.get_events(2)==0 and sys.monitoring.get_local_events(2,b['prior_module']._basis.__code__)==0)
 r.yes('authenticated basis reproduces saved current receipt',lambda:m.enc(m._assemble(data,rows,b))==saved)
 r.save('source-catalogue.json',cat);r.save('predecessor-public-result.json',b['public_predecessor']);r.save('semantic-rows.json',rows);fixtures=[]
 r.event('checked-core-controls-start',basis='Actual public validation return; no function replacement')
 assert cat['source']['order']==ORDER
 for idx in (0,1):
  for control in (False,True):
   label=str((idx,control));q=make(m,b,idx,control=control);fixtures.append(q)
   r.yes('independent construction and oracle '+label,lambda q=q:oracle(q,m._construct_checked(b,q)))
   for opt in ({'owner_continuity':False},{'continuity':'UNESTABLISHED'},{'invocation':'fl6-distinct-launcher-details'}):
    x=make(m,b,idx,control=control,**opt);r.yes('conditional or distinct occurrence '+label+str(opt),lambda x=x:oracle(x,m._construct_checked(b,x)))
   selected=ORDER if not control else ['launcher-handler-entry','details-value-message','details-dict-completion','details-assignment-attempt','details-assignment-complete']
   for stage in selected:
    for kind in ('raise','process-termination','unobserved'):
     x=make(m,b,idx,control=control,terminal=(stage,kind));tag=str((idx,control,stage,kind))
     r.yes('independent frontier oracle '+tag,lambda x=x:oracle(x,m._construct_checked(b,x)))
     bad=change(x,('output','details_assignment_completed_in_model'),True);r.no('false completion '+tag,lambda bad=bad:m._construct_checked(b,bad),'DETAILS-OUTPUT-CORRESPONDENCE')
   for stage in ('callback-handler-enter','callback-none-guard','callback-bare-rethrow'):
    x=make(m,b,idx,control=control,parent_overrides={stage:'raise'},invalid_parent=True)
    assert x['parent_output']['removal_completed_in_model'] is True and x['parent_output']['handler_evaluation_error_in_model'] is not None
    r.no('completed removal with replacement cannot select constructor '+label+stage,lambda x=x:m._construct_checked(b,x),'DETAILS-PARENT-COMPLETION')
   x=make(m,b,idx,control=control,parent_overrides={'removal-complete':'raise'},invalid_parent=True);r.no('cleanup replacement cannot enter selected route '+label,lambda x=x:m._construct_checked(b,x),'DETAILS-PARENT-COMPLETION')
  q=fixtures[-1]
  for path,value in [(('invocation',),'foreign'),(('anchor','recovery_occurrence'),'stale'),(('context',),'SYMBOLIC-U-TWO' if idx==0 else 'SYMBOLIC-U-ONE'),(('delivery_binding','selected_error','reference'),'wrong-error'),(('delivery_binding','references','owner','symbol'),'wrong-owner'),(('delivery_binding','references','token','symbol'),'wrong-token'),(('delivery_binding','references','manager','symbol'),'wrong-instance'),(('delivery_binding','scope','acquisition'),'mixed-acquisition'),(('delivery_binding','launcher_name'),'other'),(('delivery_binding','runtime_delivery'),True),(('delivery_binding','existing_cause'),None),(('delivery_binding','continuity'),True),(('outcomes',),L(q['outcomes'])),(('delivery_binding',),M(q['delivery_binding'])),(('delivery_binding','launcher_name'),S('e'))]:
   x=change(q,path,value);r.no('lineage type or unsupported claim '+str((idx,path)),lambda x=x:m._construct_checked(b,x))
  for role in ('owner','token','manager'):
   x=substitute(q,q['delivery_binding']['references'][role]['symbol'],'coordinated-'+role);r.no('coordinated reference substitution '+str((idx,role)),lambda x=x:m._construct_checked(b,x))
  x=substitute(q,q['delivery_binding']['selected_error']['reference'],'coordinated-error');r.no('coordinated selected-error substitution '+str(idx),lambda x=x:m._construct_checked(b,x))
  x=D(q);x['delivery_binding']={S(k):v for k,v in x['delivery_binding'].items()};r.no('literal-key subclasses '+str(idx),lambda x=x:m._construct_checked(b,x),'KEY-TYPE')
  for n in range(len(ORDER)):
   x=D(q);del x['outcomes'][n];x['projection']['outcomes']=D(x['outcomes']);r.no('source stage omission '+str((idx,ORDER[n])),lambda x=x:m._construct_checked(b,x))
  for seq in (list(reversed(q['outcomes'])),[q['outcomes'][0],*q['outcomes']],q['outcomes']+[{'stage':'normal-managed-close','outcome':'normal'}]):
   x=D(q);x['outcomes']=D(seq);x['projection']['outcomes']=D(seq);r.no('reordering duplication or normal-path splice '+str(idx),lambda x=x:m._construct_checked(b,x))
  x=make(m,b,idx,continuity='UNESTABLISHED');x['outcomes']=D(q['outcomes']);x['projection']['outcomes']=D(q['outcomes']);r.no('unknown delivery cannot advance to handler '+str(idx),lambda x=x:m._construct_checked(b,x),'DETAILS-UNESTABLISHED-DELIVERY')
  x=make(m,b,idx,terminal=('details-value-message','raise'));x['outcomes'].append({'stage':'details-key-traceback','outcome':'normal'});x['projection']['outcomes']=D(x['outcomes']);r.no('replacement skips subsequent evaluation '+str(idx),lambda x=x:m._construct_checked(b,x),'DETAILS-UNREACHED-STEPS')
  for flag in ('cleanup_loop_entered','normal_managed_close_spliced','managed_clear_spliced','ACTIVE_unlink_spliced','failure_file_established','outward_propagation_established','runtime_observation','obligations_discharged','authorization_renewed','actual_admission'):
   x=change(q,('output',flag),True);r.no('unsupported output '+str((idx,flag)),lambda x=x:m._construct_checked(b,x),'DETAILS-OUTPUT-CORRESPONDENCE')
  for path,value in [(('known_literal_fields','nonexecution_established'),0),(('known_literal_fields','new_authorization'),0),(('known_literal_fields','cleanup'),[None]),(('dynamic_fields',0,'exact_value'),'RuntimeError'),(('dynamic_fields',1,'exact_type'),'str'),(('dynamic_fields',2,'formatted_bytes'),'invented'),(('dynamic_fields',2,'selected_error','reference'),'other'),(('complete_runtime_dictionary_observed',),True)]:
   x=change(q,('output','details_in_model',*path),value);r.no('exact literals or unavailable dynamic values '+str((idx,path)),lambda x=x:m._construct_checked(b,x))
  got=m._construct_checked(b,q);got['projection']['details_in_model']['known_literal_fields']['cleanup'].append('mutated');got['projection']['delivery_binding']['selected_error'].clear();got['projection']['events'].clear()
  r.yes('nested result mutation cannot alter expectations '+str(idx),lambda q=q:oracle(q,m._construct_checked(b,q)))
  for field,value in [('runtime_handler_details_chain',True),('exact_generated_message','fabricated'),('classification','PASS'),('multiplicity',0),('cleanup_loop_coverage',True),('existing_cause_context_suppression','ABSENT')]:
   x=D(rows);x[idx][field]=value;x[idx]['declaration']['runtime_handler_details_observations']=True;r.no('coordinated semantic claims '+str((idx,field)),lambda x=x:m._check_rows(b,x),'DETAILS-SEMANTIC-CORRESPONDENCE')
 r.save('independent-fixtures.json',fixtures)
 for value,label in [(rows[::-1],'reordered'),(rows[:1],'missing'),([rows[0],rows[0]],'duplicated')]:r.no('semantic contexts '+label,lambda value=value:m._check_rows(b,value))
 got=m._rows(b);got[0]['declaration']['source'].clear();r.yes('fresh semantic expectations isolated',lambda:m.enc(m._rows(b))==before)
 got=m._assemble(data,rows,b);got['contexts'].reverse();got['contexts'][0][m.RELATION]['declaration'].clear();public['contexts'].reverse();public['receipt'].clear();r.yes('public and derived nested returns isolated',lambda:m.enc(m._assemble(data,rows,b))==saved and m.CONTEXTS==('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'))
 for key in ('prior','prior_saved','sources'):
  altered=dict(data);altered[key]=D(data[key])
  if key=='prior':altered[key]['contexts'].reverse()
  elif key=='prior_saved':altered[key]+=b'\n'
  else:altered[key]=(data[key][1],data[key][0])
  r.no('candidate input substitution '+key,lambda altered=altered:m._check_candidate(b,altered,cat))
 e=D(b['evidence']);k=next(k for k,v in e.items() if v);e[k]+=b'\n';r.no('altered saved evidence',lambda:m._compare_evidence(b,e),'DETAILS-VALIDATED-EVIDENCE');del e[k];r.no('omitted saved evidence',lambda:m._compare_evidence(b,e),'DETAILS-VALIDATED-EVIDENCE')
 for i in (0,1):
  for relation in sorted(m.REQUIRED):
   x=json.loads(saved);del x['contexts'][i][relation];r.no('public mandatory pre-derivation '+str((i,relation)),lambda x=x:m.validate(root,m.enc(x)),'DETAILS-MANDATORY-RELATIONS')
  for field,value in [('runtime_handler_details_chain',True),('classification','PASS')]:
   x=json.loads(saved);x['contexts'][i][m.RELATION][field]=value;x['contexts'][i][m.RELATION]['declaration']['runtime_handler_details_observations']=True;r.no('receipt-comparison core coordinated claims '+str((i,field)),lambda x=x:m._receipt_checked(b,m.enc(x)),'DETAILS-STALE-OR-ALTERED-RECEIPT')
 for label,change in [('reversed',lambda x:x['contexts'].reverse()),('duplicate',lambda x:x['contexts'].__setitem__(1,D(x['contexts'][0]))),('source-binding',lambda x:x['extension_components']['managed_coverage.py'].__setitem__('sha256','0'*64))]:
  x=json.loads(saved);change(x);r.no('receipt-comparison core '+label,lambda x=x:m._receipt_checked(b,m.enc(x)),'DETAILS-STALE-OR-ALTERED-RECEIPT')
 r.yes('comparison core still accepts pristine bytes',lambda:m._receipt_checked(b,saved)['result']=='PASS')
 r.save('final-verification.json',verify_root(root));r.event('finished')
except BaseException:
 error=traceback.format_exc();(r.path/'failure.txt').write_text(error)
 if 'x' in globals():r.save('last-case.json',x)
 raise
finally:r.finish(error,scope='One actual current full public positive and actual unchanged predecessor public validation; authenticated-basis checked cores, pre-derivation gates and receipt-comparison cores separately identified',full_public_negative_derivations=0,CLI_execution_claimed=False)
