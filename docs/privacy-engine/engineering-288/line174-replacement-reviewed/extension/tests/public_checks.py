"""One NEW replacement recovered public attempt plus new focused authenticated cores."""
from pathlib import Path
import sys,signal,traceback,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
import cases as F
root=Path(sys.argv[1]).resolve();r=Records(sys.argv[2]);failure=None
CORE='actual-authenticated-basis constructed core; unchanged predecessor revalidates parent'
OUT='actual-authenticated-basis output core; reuses validated selected parent'
SEM='actual-authenticated-basis semantic/source comparison core'
class S(str):pass
class L(list):pass
def deadline(s,f):raise TimeoutError('NEW-REPLACEMENT-SOFT-DEADLINE')
def change(v,path,value):
 v=D(v);q=v
 for k in path[:-1]:q=q[k]
 q[path[-1]]=value;return v
try:
 r.save('environment.json',environment());r.save('input-root.json',verify_root(root));monitor,captures=guard(root,r.path,r)
 m=module(root/'code/correspondence.py');monitor(m);saved=(root/'receipts/prepared-write-call-replacement.json').read_bytes()
 signal.signal(signal.SIGALRM,deadline);signal.setitimer(signal.ITIMER_REAL,max(1,4200-(time.monotonic()-r.start)))
 r.event('NEW-replacement-public-validation-start',receipt=identity(saved),full_public_negative_derivations=0)
 public=m.validate(root,saved);r.save('actual-public-result.json',public)
 r.yes('fresh recovered actual current public positive',lambda:public['result']=='PASS' and public['receipt']==identity(saved),'full public positive')
 assert len(captures)==1;basis=captures[0];d=basis['fresh'];cat=basis['catalogue'];c=d['coverage'];r.save('predecessor-public-result.json',basis['public_predecessor'])
 r.yes('exact actual unchanged predecessor result',lambda:basis['public_predecessor']['result']=='PASS' and basis['public_predecessor']['receipt']==m.PREDECESSOR_RECEIPT,'actual predecessor public result')
 r.yes('prepared receipt equals actual authenticated assembly',lambda:m.enc(m._assemble(d,m._rows(basis),basis))==saved,'authenticated receipt comparison')
 r.event('new-focused-authenticated-cores-start')
 for idx in (0,1):
  for control in (False,True):
   for origin in ('close','append'):
    tag=f'{idx}-{control}-{origin}';pc=json.loads((root/'fixtures/loop'/(tag+'.json')).read_bytes());fx=F.make(d,cat,pc,basis['session_bindings'][idx]);got=r.yes('normal selected route '+tag,lambda fx=fx:m._construct_checked(basis,fx),CORE)
    r.yes('pending error/list/stop oracle '+tag,lambda got=got,pc=pc:F.oracle(got['projection'],pc['output']),'source-grounded oracle on authenticated constructed output')
    v=m._premises(basis,fx)
    for key,value in [('terminal_python_exception_in_model',False),('write_new_body_entry_established',True),('pid_value',17),('directory_count_value',0),('filename_value','failure-1-0.json'),('cleanup_list_state',{}),('last_pending_error_in_model',None)]:
     bad=change(fx['output'],[key],value);r.no('output '+key+' '+tag,lambda bad=bad,fx=fx,v=v:c.validate_write_call_projection(cat,fx['projection'],v,bad),OUT,'WC-OUTPUT-CORRESPONDENCE')
    for path,value in [(['invocation'],'different'),(['binding','references','token','symbol'],'wrong'),(['binding','references','owner','symbol'],'wrong'),(['session_binding','recorded_destination'],'/different'),(['binding','details_role','reference'],'wrong'),(['binding','cleanup_list','reference'],'wrong'),(['parent_output','loop_completion_established'],False)]:
     bad=change(fx,path,value);r.no('bound input '+str(path)+' '+tag,lambda bad=bad:m._construct_checked(basis,bad),CORE)
    bad=D(fx);bad['session_binding']['recorded_destination']='/coordinated';bad['binding']['destination']['session_binding']=D(bad['session_binding']);bad['projection']['session_binding']=D(bad['session_binding']);bad['projection']['binding']=D(bad['binding']);r.no('coordinated destination '+tag,lambda bad=bad:m._construct_checked(basis,bad),CORE,'WC-VALIDATED-DESTINATION')
    got['projection']['binding'].clear();got['projection']['cleanup_list_state'].clear();r.yes('result mutation isolation '+tag,lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'],CORE)
    for terminal in ('raise','catchable-interruption','process-termination','unobserved'):
     nv=D(v);nv['outcomes']=F.outcomes(cat,(cat['source']['order'][-1],terminal));out=c.write_call_projection(cat,nv,nv)
     r.yes('terminal frontier '+tag+' '+terminal,lambda nv=nv,out=out,terminal=terminal,pc=pc:c.validate_write_call_projection(cat,nv,nv,out) and F.oracle(out,pc['output'],False,terminal),OUT)
     bad=D(out);bad['call_attempt_established']=True;r.no('false terminal attempt '+tag+' '+terminal,lambda bad=bad,nv=nv:c.validate_write_call_projection(cat,nv,nv,bad),OUT,'WC-OUTPUT-CORRESPONDENCE')
    r.save('case-summary/'+tag+'.json',{'scope':fx['projection']['scope'],'case_identity':identity(m.enc(fx)),'output_identity':identity(m.enc(fx['output'])),'parent_fixture':tag+'.json','runtime_observation':False})
    if not control and origin=='close':
     for stage in cat['source']['order']:
      nv=D(v);nv['outcomes']=F.outcomes(cat,(stage,'unobserved'));out=c.write_call_projection(cat,nv,nv);r.yes('stop at first unobserved '+tag+' '+stage,lambda out=out,pc=pc:F.oracle(out,pc['output'],False,'unobserved'),OUT)
     for terminal in ('raise','catchable-interruption','process-termination'):
      nv=D(v);nv['outcomes']=F.outcomes(cat,(cat['source']['order'][8],terminal));out=c.write_call_projection(cat,nv,nv);r.yes('early evaluation frontier '+tag+' '+terminal,lambda out=out,terminal=terminal,pc=pc:F.oracle(out,pc['output'],False,terminal),OUT)
     for label,oo in [('missing',v['outcomes'][:-1]),('reordered',[v['outcomes'][1],v['outcomes'][0],*v['outcomes'][2:]]),('extra',[*v['outcomes'],{'stage':'body','outcome':'normal'}])]:
      nv=D(v);nv['outcomes']=D(oo);r.no('order '+tag+' '+label,lambda nv=nv:c.write_call_projection(cat,nv,nv),OUT)
     for path,value in [(['binding','continuity'],S('explicit conditional premise')),(['outcomes'],L(v['outcomes']))]:
      bad=change(fx,path,value);r.no('exact input type '+tag+' '+str(path),lambda bad=bad:m._construct_checked(basis,bad),'exact-type constructed gate','WC-CONSTRUCTED-INPUT')
     bad=D(fx['output']);bad[S('completion')]=bad.pop('completion');r.no('subclass key '+tag,lambda bad=bad:c.validate_write_call_projection(cat,fx['projection'],v,bad),'exact-type output gate','WC-OUTPUT-TYPE')
     uf=F.make(d,cat,pc,basis['session_bindings'][idx],continuity='UNESTABLISHED');r.yes('unestablished continuation '+tag,lambda uf=uf:m._construct_checked(basis,uf)['projection']['terminal_python_exception_in_model'] is None,CORE)
  rec=json.loads(saved);rec['contexts'][idx].pop(m.RELATION);r.no('missing relation '+str(idx),lambda rec=rec:m.validate(root,m.enc(rec)),'public required-relation gate before predecessor','WC-MANDATORY-RELATIONS')
  rec=json.loads(saved);rec['contexts'][idx][m.RELATION]['write_new_body_established']=True;r.no('altered receipt '+str(idx),lambda rec=rec:m._receipt_checked(basis,m.enc(rec)),'authenticated-basis receipt comparison; not full public negative derivation','WC-STALE-OR-ALTERED-RECEIPT')
  rows=m._rows(basis);rows[idx]['declaration']['guard_branches']['continuity']=[];r.no('semantic omission '+str(idx),lambda rows=rows:m._check_rows(basis,rows),SEM,'WC-SEMANTIC-CORRESPONDENCE')
 bad=D(cat);bad['source']['steps'].pop();bad['declarations'].pop();rows=m._rows(basis)
 for row in rows:row['declaration']=D(bad)
 r.no('coordinated catalogue/claims omission',lambda:m._check_candidate(basis,d,bad,rows),SEM,'WC-CATALOGUE-SOURCE')
 r.no('independent source rejects coordinated catalogue',lambda:c.validate_write_call(*m.sources(d),basis['prior_basis']['catalogue'],basis['prior_basis']['prior_basis']['catalogue'],basis['prior_basis']['prior_basis']['prior_basis']['catalogue'],bad),'source-recomputed catalogue comparison','WC-SOURCE-CORRESPONDENCE')
 rows=m._rows(basis);rows[0].clear();rows[1]['declaration']['source']['steps'].clear();r.yes('both-context returned expectation isolation',lambda:all(x['declaration']['source']['steps'] for x in m._rows(basis)),SEM)
 r.save('monitoring-state.json',{'slots':{str(i):sys.monitoring.get_tool(i) for i in (1,2,3,4,5)},'qualification':'Normal public path only; free slots alone do not establish complete cleanup'})
 r.save('final-root.json',verify_root(root));r.save('layers.json',{'full_current_public_positive':1,'full_public_negative_derivations':0,'core_negatives':'individually labelled; authenticated basis reused, no extra public derivation'})
except BaseException as e:failure={'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()}
finally:
 signal.setitimer(signal.ITIMER_REAL,0);r.finish(failure)
if failure:raise SystemExit(1)
