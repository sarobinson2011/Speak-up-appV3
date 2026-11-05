"""One fresh recovered public positive; new focused authenticated cores, no old campaign."""
from pathlib import Path
import sys,signal,traceback,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
import cases as F
root=Path(sys.argv[1]).resolve();r=Records(sys.argv[2]);failure=None
CORE='actual-authenticated-basis constructed core; unchanged predecessor revalidates selected parent'
OUT='authenticated-parent producer output comparison core; no new public derivation'
SEM='actual-authenticated-basis semantic/source comparison core'
class S(str):pass
class L(list):pass
class I(int):pass
def deadline(s,f):raise TimeoutError('HELPER-OPEN-SOFT-DEADLINE')
def change(v,path,value):
 v=D(v);q=v
 for k in path[:-1]:q=q[k]
 q[path[-1]]=value;return v
try:
 r.save('environment.json',environment());r.save('input-root.json',verify_root(root));monitor,captures=guard(root,r.path,r)
 m=module(root/'code/correspondence.py');monitor(m);saved=(root/'receipts/prepared-helper-open-attempt.json').read_bytes()
 signal.signal(signal.SIGALRM,deadline);signal.setitimer(signal.ITIMER_REAL,max(1,4500-(time.monotonic()-r.start)))
 r.event('helper-open-recovered-public-start',receipt=identity(saved),full_public_negative_derivations=0)
 public=m.validate(root,saved);r.save('actual-public-result.json',public)
 r.yes('fresh recovered actual current public positive',lambda:public['result']=='PASS' and public['receipt']==identity(saved),'full public positive through unchanged actual predecessor')
 assert len(captures)==1;basis=captures[0];d=basis['fresh'];cat=basis['catalogue'];c=d['coverage'];r.save('predecessor-public-result.json',basis['public_predecessor'])
 r.yes('exact actual unchanged predecessor result',lambda:basis['public_predecessor']['result']=='PASS' and basis['public_predecessor']['receipt']==m.PREDECESSOR_RECEIPT,'actual predecessor public-return observation')
 r.yes('prepared receipt matches authenticated assembly',lambda:m.enc(m._assemble(d,m._rows(basis),basis))==saved,'authenticated-basis receipt comparison core')
 r.yes('independent AST order agrees with actual catalogue',lambda:[(s['operation'],s['source']['site']) for s in cat['source']['steps']]==F.plan(m.sources(d)[0]),'defining-source AST compared with authenticated catalogue')
 r.event('focused-authenticated-cores-start')
 for idx in (0,1):
  for control in (False,True):
   for origin in ('close','append'):
    tag=f'{idx}-{control}-{origin}';pc=json.loads((root/'fixtures/write-call'/(tag+'.json')).read_bytes());fx=F.make(c,cat,pc)
    got=r.yes('normal selected route '+tag,lambda fx=fx:m._construct_checked(basis,fx),CORE);v=m._premises(basis,fx)
    r.yes('parameter/pending/stop oracle '+tag,lambda got=got,pc=pc:F.oracle(got['projection'],pc['output']),'independent source oracle on authenticated-parent constructed result')
    for key,value in [('terminal_python_exception_in_model',False),('helper_return_established',True),('open_return_established',True),('file_creation_established',True),('context_manager_entry_established',True),('f_binding_established',True),('encoding_established',True),('exact_path_value','/invented'),('cleanup_list_state',{}),('last_pending_error_in_model',None)]:
     bad=change(fx['output'],[key],value);r.no('output '+key+' '+tag,lambda bad=bad,fx=fx,v=v:c.validate_helper_open_projection(cat,fx['projection'],v,bad),OUT,'OPEN-OUTPUT-CORRESPONDENCE')
    for path,value in [(['invocation'],'different'),(['context'],'SYMBOLIC-U-TWO' if idx==0 else 'SYMBOLIC-U-ONE'),(['binding','references','token','symbol'],'wrong'),(['binding','references','owner','symbol'],'wrong'),(['binding','parameters','p','argument','symbol'],'wrong-path'),(['binding','parameters','x','argument','reference'],'wrong-details'),(['binding','cleanup_list','reference'],'wrong-list'),(['binding','open_callable','name'],'other'),(['binding','helper_invocation','symbol'],'other-invocation')]:
     bad=change(fx,path,value);r.no('bound input '+str(path)+' '+tag,lambda bad=bad:m._construct_checked(basis,bad),CORE)
    # A coordinated new-layer substitution must still fail against actual predecessor output.
    bad=D(fx);bad['binding']['parameters']['p']['argument']['symbol']='coordinated';bad['projection']['binding']=D(bad['binding']);bad['output']['binding']=D(bad['binding']);bad['output']['bound_parameters']=D(bad['binding']['parameters'])
    r.no('coordinated path roles '+tag,lambda bad=bad:m._construct_checked(basis,bad),CORE,'OPEN-EXPECTED-BINDING')
    bad=D(fx);bad['parent_output']['call_attempt_established']=False;bad['projection']['parent_result']=D(bad['parent_output']);r.no('false parent completion '+tag,lambda bad=bad:m._construct_checked(basis,bad),CORE,'OPEN-VALIDATED-PARENT')
    bad=D(fx);bad['parent_case']['output']['last_pending_error_in_model']=None;bad['parent_output']=D(bad['parent_case']['output']);bad['projection']['parent_result']=D(bad['parent_output']);r.no('coordinated pending parent substitution '+tag,lambda bad=bad:m._construct_checked(basis,bad),CORE)
    bad=D(fx);bad['binding']['parameters']['p']['argument'],bad['binding']['parameters']['x']['argument']=bad['binding']['parameters']['x']['argument'],bad['binding']['parameters']['p']['argument'];bad['projection']['binding']=D(bad['binding']);r.no('swapped positional arguments '+tag,lambda bad=bad:m._construct_checked(basis,bad),CORE)
    # Validate exact-type boundaries before value equality/JSON normalization.
    bad=change(fx,['binding','continuity'],S('explicit conditional premise'));r.no('same-valued input subclass '+tag,lambda bad=bad:m._construct_checked(basis,bad),'exact-type constructed input gate','OPEN-CONSTRUCTED-INPUT')
    bad=change(fx['output'],['bound_parameters','p','position'],I(0));r.no('nested integer subclass '+tag,lambda bad=bad:c.validate_helper_open_projection(cat,fx['projection'],v,bad),'exact-type output gate','OPEN-OUTPUT-TYPE')
    bad=D(fx['output']);bad[S('completion')]=bad.pop('completion');r.no('literal-key subclass '+tag,lambda bad=bad:c.validate_helper_open_projection(cat,fx['projection'],v,bad),'exact-type output gate','OPEN-OUTPUT-TYPE')
    got['projection']['binding']['parameters']['x']['argument'].clear();got['projection']['cleanup_list_state'].clear()
    r.yes('returned nested mutation isolation '+tag,lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'],CORE)
    uf=F.make(c,cat,pc,continuity='UNESTABLISHED');r.yes('unestablished continuation remains frontier '+tag,lambda uf=uf:m._construct_checked(basis,uf)['projection']['helper_entry_established_in_model'] is False,CORE)
    nv=D(v);nv['binding']=D(uf['binding']);nv['outcomes']=F.outcomes(cat);r.no('unknown continuity cannot advance '+tag,lambda nv=nv:c.helper_open_projection(cat,nv,nv),OUT,'OPEN-UNKNOWN-CONTINUITY')
    # Each new semantic region, in every admitted context/prefix/origin combination.
    for terminal in ('raise','catchable-interruption','process-termination','unobserved'):
     stage=cat['source']['order'][-1];nv=D(v);nv['outcomes']=F.outcomes(cat,(stage,terminal));out=c.helper_open_projection(cat,nv,nv)
     r.yes('terminal frontier '+tag+' '+terminal,lambda out=out,pc=pc,stage=stage,terminal=terminal:F.oracle(out,pc['output'],stage,terminal),OUT)
     bad=D(out);bad['open_call_attempt_established_in_model']=True;r.no('false completed attempt '+tag+' '+terminal,lambda bad=bad,nv=nv:c.validate_helper_open_projection(cat,nv,nv,bad),OUT,'OPEN-OUTPUT-CORRESPONDENCE')
    for stage in cat['source']['order'][:-1]:
     nv=D(v);nv['outcomes']=F.outcomes(cat,(stage,'unobserved'));out=c.helper_open_projection(cat,nv,nv);r.yes('first unobserved frontier '+tag+' '+stage,lambda out=out,pc=pc,stage=stage:F.oracle(out,pc['output'],stage,'unobserved'),OUT)
    for label,oo in [('missing-entry',[v['outcomes'][0],*v['outcomes'][2:]]),('reordered',[v['outcomes'][1],v['outcomes'][0],*v['outcomes'][2:]]),('missing-attempt',v['outcomes'][:-1]),('extra-body',[*v['outcomes'],{'stage':'write','outcome':'normal'}])]:
     nv=D(v);nv['outcomes']=D(oo);r.no('ordering '+tag+' '+label,lambda nv=nv:c.helper_open_projection(cat,nv,nv),OUT)
    r.save('case-summary/'+tag+'.json',{'scope':fx['projection']['scope'],'case_identity':identity(m.enc(fx)),'output_identity':identity(m.enc(fx['output'])),'parent_fixture':tag+'.json','runtime_observation':False})
    if not control and origin=='close':
     for stage in cat['source']['order'][:-1]:
      for terminal in ('raise','catchable-interruption','process-termination'):
       nv=D(v);nv['outcomes']=F.outcomes(cat,(stage,terminal));out=c.helper_open_projection(cat,nv,nv);r.yes('earlier nonnormal frontier '+tag+' '+stage+' '+terminal,lambda out=out,pc=pc,stage=stage,terminal=terminal:F.oracle(out,pc['output'],stage,terminal),OUT)
  rec=json.loads(saved);rec['contexts'][idx].pop(m.RELATION);r.no('missing mandatory relation '+str(idx),lambda rec=rec:m.validate(root,m.enc(rec)),'public required-relation gate before predecessor','OPEN-MANDATORY-RELATIONS')
  rec=json.loads(saved);rec['contexts'][idx][m.RELATION]['open_return_established']=True;r.no('altered receipt '+str(idx),lambda rec=rec:m._receipt_checked(basis,m.enc(rec)),'authenticated-basis receipt comparison core; not full public negative derivation','OPEN-STALE-OR-ALTERED-RECEIPT')
  rows=m._rows(basis);rows[idx]['declaration']['guard_branches']['continuity']=[];r.no('semantic omitted guard '+str(idx),lambda rows=rows:m._check_rows(basis,rows),SEM,'OPEN-SEMANTIC-CORRESPONDENCE')
  rows=m._rows(basis);rows[idx]['declaration']['source']['parameters'][0]['name']=S('p');r.no('semantic same-valued subclass '+str(idx),lambda rows=rows:m._check_rows(basis,rows),'exact-type semantic claim gate','OPEN-SEMANTIC-CLAIMS')
 bad=D(cat);bad['source']['steps'].pop(2);bad['declarations'].pop(2);rows=m._rows(basis)
 for row in rows:row['declaration']=D(bad)
 r.no('coordinated catalogue/claims omission',lambda:m._check_candidate(basis,d,bad,rows),SEM,'OPEN-CATALOGUE-SOURCE')
 cb=[basis['prior_basis']['catalogue'],basis['prior_basis']['prior_basis']['catalogue'],basis['prior_basis']['prior_basis']['prior_basis']['catalogue'],basis['prior_basis']['prior_basis']['prior_basis']['prior_basis']['catalogue']]
 r.no('independent source rejects coordinated omission',lambda:c.validate_helper_open(*m.sources(d),*cb,bad),'source-recomputed catalogue comparison','OPEN-SOURCE-CORRESPONDENCE')
 rows=m._rows(basis);rows[0].clear();rows[1]['declaration']['source']['steps'].clear();r.yes('both-context expectation isolation',lambda:all(x['declaration']['source']['steps'] for x in m._rows(basis)),SEM)
 r.save('monitoring-state.json',{'slots':{str(i):sys.monitoring.get_tool(i) for i in range(6)},'qualification':'Normal public path only; free slots alone do not establish complete local-event/callback cleanup. Profile observer uses no cooperative monitoring slot.'})
 sys.setprofile(None);r.save('final-root.json',verify_root(root));r.save('layers.json',{'full_current_public_positive':1,'full_public_negative_derivations':0,'new_negative_layers':'Per-row exact labels; authenticated basis reused, no additional public derivation'})
except BaseException as e:failure={'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()}
finally:
 signal.setitimer(signal.ITIMER_REAL,0);sys.setprofile(None);r.finish(failure)
if failure:raise SystemExit(1)
