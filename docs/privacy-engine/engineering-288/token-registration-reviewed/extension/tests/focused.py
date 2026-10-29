"""New supplied token controls only. No earlier suite or runtime entry is run."""
from pathlib import Path
import sys,copy,json,traceback,ast
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]).absolute();rec=Record(sys.argv[2]);error=None;write='--write' in sys.argv
class S(str):pass
class D(dict):pass
class L(list):pass
class I(int):pass
try:
 if not write:rec.save('input-verification.json',verify_root(root))
 mon=guard(root,rec.path);m=module(root/'code/correspondence.py');mon(m);data=m.inputs(root);cat=m.catalogue(data);rows,basis=m._checked(data,cat);c=data['coverage'];bundle=m._assemble(data,rows,basis)
 rec.check('mandatory predecessor invoked, both contexts retained',lambda:sum(x['function']=='derive_status' for x in CALLS)==1 and [r['context'] for r in rows]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
 rec.check('prior receipt exact and all prior fields preserved',lambda:all(bundle[k]==v for k,v in basis['prior'].items() if k not in ('format','contexts','extension_components')) and all(all(v==bundle['contexts'][i][k] for k,v in ctx.items()) for i,ctx in enumerate(basis['prior']['contexts'])))
 # Independent source audit: traversal of the actual _run body, not the producer's catalogue.
 launcher,entry=m.sources(data);tree=ast.parse(entry);run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run');w=run.body[2].body[0];owner,token,store,guarded=w.body;control,client,check=guarded.body;pop=guarded.finalbody[0]
 rec.check('source independently establishes owner token insertion order',lambda:[ast.unparse(n) for n in (owner,token,store)]==['owner = _Owner(wrapper)','token = object()','_OWNERS[token] = owner'])
 rec.check('source independently establishes callback branch and failure guard',lambda:ast.unparse(control.test)=='control is not None' and ast.unparse(client.body[0])=='client(Client(token))' and ast.unparse(check.test)=='owner.failure is not None')
 rec.check('source pop default and discarded result inside finally before context exit',lambda:ast.unparse(pop)=='_OWNERS.pop(token, None)' and type(pop) is ast.Expr and guarded in w.body and len(guarded.finalbody)==1)
 independent_order=['owner-create','token-create','registry-insert','control-guard','control-create','control-callback','client-create','client-callback','owner-failure-guard','finally-enter','removal-attempt','removal-complete']
 rec.check('source stage coverage is exact independent of declarations',lambda:cat['source']['order']==independent_order and [d['id'] for d in cat['declarations']]==independent_order)
 fixtures=[]
 for idx in (0,1):
  tag=rows[idx]['context'];fx=normal(m,basis,idx);fixtures.append(fx)
  def accepted(label,case):
   return rec.check(label+' '+tag,lambda:m._construct_checked(basis,case)['projection']==case['output'])
  def reject(label,case):return rec.reject(label+' '+tag,lambda:m._construct_checked(basis,case))
  accepted('normal controlled registration callback pop',fx);accepted('general callback without control',normal(m,basis,idx,control=False))
  no=normal(m,basis,idx,continuity=False);accepted('unknown continuity admitted without inferred selected-owner removal',no)
  rec.check('normal pop under unknown continuity proves no selected owner removal '+tag,lambda:no['output']['selected_owner_removed_in_model'] is None and no['output']['removal_completed_in_model'] and no['output']['revocation_persists'] is None)
  failed=normal(m,basis,idx,owner_none=False);accepted('normal callback with retained failure stops at exceptional frontier',failed)
  rec.check('retained failure gate does not claim finally or unwind '+tag,lambda:not failed['output']['finally_entered_in_model'] and failed['output']['outcome_classification']['terminal_python_exception_in_model'] is None)
  # Independent boundary cases include partial prefixes, finally entry and attempted pop.
  for stage in independent_order:
   for outcome in ('raise','process-termination','unobserved'):
    case=normal(m,basis,idx,terminal=(stage,outcome));accepted(stage+' '+outcome,case)
    out=case['output'];rec.check('no completion inference '+stage+' '+outcome+' '+tag,lambda out=out:not out['removal_completed_in_model'] and out['selected_owner_removed_in_model'] is None and out['database_cleanup_completion'] is None and out['retained_error'] is None and not out['authorization_renewed'] and (outcome=='raise' or out['outcome_classification']['terminal_python_exception_in_model'] is None))
  for role in ('token','owner','client','control','session','manager'):
   bad=copy.deepcopy(fx);bad['projection']['references'][role]['symbol']='wrong';reject('wrong '+role,bad)
  for edge in ('client.token','control.token','owners[token]','owner.wrapper','session.managed'):
   bad=copy.deepcopy(fx);bad['projection']['references'][edge]['symbol']='wrong';reject('wrong reference edge '+edge,bad)
  other=normal(m,basis,idx,invocation='constructed-run-B')
  bad=copy.deepcopy(fx);bad['projection']=copy.deepcopy(other['projection']);bad['output']=copy.deepcopy(other['output']);reject('coordinated foreign invocation projection and output',bad)
  rec.check('same content different invocation retains distinct occurrences '+tag,lambda:fx['output']['events'][0]['id']!=other['output']['events'][0]['id'] and fx['output']['reference_bindings']['token']!=other['output']['reference_bindings']['token'])
  for path in [('scope','instance'),('scope','acquisition'),('scope','frontier')]:
   bad=copy.deepcopy(fx);par=bad['projection'];
   for k in path[:-1]:par=par[k]
   par[path[-1]]={} if type(par[path[-1]]) is dict else 'stale';reject('stale scope '+str(path),bad)
  for stage in independent_order:
   bad=copy.deepcopy(fx);bad['projection']['outcomes']=[v for v in bad['projection']['outcomes'] if v['stage']!=stage];bad['outcomes']=copy.deepcopy(bad['projection']['outcomes']);reject('omitted step '+stage,bad)
  bad=copy.deepcopy(fx);bad['outcomes'][0],bad['outcomes'][2]=bad['outcomes'][2],bad['outcomes'][0];bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('reordered insertion before owner creation',bad)
  for field in ('finally_entered_in_model','removal_attempt_entered_in_model','removal_completed_in_model','selected_owner_removed_in_model'):
   bad=normal(m,basis,idx,terminal=('client-callback','process-termination'));bad['output'][field]=True;reject('premature '+field,bad)
  for field,value in [('retained_error',{}),('database_cleanup_completion',True),('authorization_renewed',True),('slot_after_pop_in_model','ABSENT-AT-POP-COMPLETION')]:
   bad=normal(m,basis,idx,terminal=('removal-complete','unobserved'));bad['output'][field]=value;reject('unsupported claim '+field,bad)
  bad=copy.deepcopy(no);bad['output']['selected_owner_removed_in_model']=True;reject('pop normal does not repair missing continuity',bad)
  bad=copy.deepcopy(fx);bad['output']['events'][0]['scope']['invocation']='foreign';reject('output event cross-invocation',bad)
  # Exact-type regressions at return-input, output and semantic-claim boundaries.
  for label,path,T in [('string',('projection','occurrence'),S),('dictionary',('projection','scope'),D),('list',('projection','outcomes'),L),('bool-as-int',('control_present',),int),('output-string',('output','completion'),S),('output-container',('output','events'),L)]:
   bad=copy.deepcopy(fx);p=bad
   for k in path[:-1]:p=p[k]
   p[path[-1]]=T(p[path[-1]]);reject('exact-type '+label,bad)
  bad=copy.deepcopy(fx);bad['output']={S(k):v for k,v in bad['output'].items()};reject('subclassed literal output keys',bad)
  bad=copy.deepcopy(fx);bad['projection']['references']['token']['scope']['instance']={S(k):v for k,v in bad['projection']['references']['token']['scope']['instance'].items()};reject('nested literal key subclass',bad)
  for path,change_value in [(('conditional_links',),[]),(('runtime_registration_revocation_links',),[]),(('classification',),'KNOWN'),(('scope','invocation'),'invented'),(('context',),rows[1-idx]['context'])]:
   claims=copy.deepcopy(rows);p=claims[idx]
   for k in path[:-1]:p=p[k]
   p[path[-1]]=change_value;rec.reject('semantic altered '+str(path)+' '+tag,lambda claims=claims:m._check_rows(basis,claims))
  claims=copy.deepcopy(rows);claims[idx]['declaration']['source']['entry']['bytes']=I(claims[idx]['declaration']['source']['entry']['bytes']);rec.reject('semantic nested same-valued int subclass '+tag,lambda:m._check_rows(basis,claims))
  out=m._construct_checked(basis,fx);out['projection']['reference_bindings']['token']['scope']['instance'].clear();out['projection']['events'].clear();out['anchor'].clear();accepted('mutated returned object cannot change expectations',fx)
  # Direct producer entry preflight, independent validated scope and detached outputs.
  p=fx['projection'];v=premise(fx);got=c.token_registration_projection(cat,p,v);rec.check('direct submitted output accepted '+tag,lambda:c.validate_token_registration_projection(cat,p,v,got))
  bad=copy.deepcopy(p);bad['references']['token']['symbol']=S(bad['references']['token']['symbol']);rec.reject('producer pre-normalization input gate '+tag,lambda:c.token_registration_projection(cat,bad,v))
  bad=copy.deepcopy(got);bad['events']=L(bad['events']);rec.reject('producer pre-normalization output gate '+tag,lambda:c.validate_token_registration_projection(cat,p,v,bad))
  got['reference_bindings']['owner']['scope'].clear();rec.check('producer output nested mutation isolation '+tag,lambda:c.validate_token_registration_projection(cat,p,v,c.token_registration_projection(cat,p,v)))
 # Source catalogue expectation independently regenerated; both omissions and coordinated edits reject.
 for label,edit in [('declaration omission',lambda x:x['declarations'].pop()),('guard omission',lambda x:x['guard_branches'].pop('stored_failure')),('order alteration',lambda x:x['source']['order'].reverse()),('remove wrong key',lambda x:x['source']['remove'].update(key='other')),('stale source',lambda x:x['source']['entry'].update(sha256='0'*64))]:
  bad=copy.deepcopy(cat);edit(bad);rec.reject('source validator '+label,lambda bad=bad:c.validate_token_registration(*m.sources(data),*m.dependencies(data),m.inner(data)['ctx']['binding'],bad))
 before=enc(m._assemble(data,rows,basis));bundle['contexts'][0]['token_registration_correspondence']['declaration'].clear();bundle['contexts'].clear();rec.check('bundle nested mutation isolates expectations',lambda:enc(m._assemble(data,rows,basis))==before)
 rec.check('observer stays unjoined and runtime unknown',lambda:all(r['observer_join'] is None and r['runtime_registration_revocation_links'] is None for r in rows))
 receipt=m.enc(m._assemble(data,rows,basis));rec.save('fixtures.json',{'cases':fixtures});rec.save('receipt-identity.json',identity(receipt))
 if write:rec.save('token-registration-correspondence.json',json.loads(receipt))
 else:rec.check('recovered exact receipt reproduction',lambda:(root/'results/primary/token-registration-correspondence.json').read_bytes()==receipt)
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='New Engineering supplied token registration controls only; prior independent/supplied results separate')
