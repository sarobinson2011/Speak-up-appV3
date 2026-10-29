from pathlib import Path
import sys,ast,copy,json,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None
class S(str):pass
class I(int):pass
class D(dict):pass
class L(list):pass
class F(float):pass
class B(bytes):pass
def mod(x,path,fn):
 y=copy.deepcopy(x);p=y
 for k in path[:-1]:p=p[k]
 p[path[-1]]=fn(p[path[-1]]);return y
def key(x,k):return {S(a) if a==k else a:b for a,b in x.items()}
def reject_before_normalizing(label,fn):
 calls=[];jd=json.dumps;cp=copy.deepcopy
 def poison(*a,**k):calls.append(True);raise AssertionError('normalization-or-copy-before-type-check')
 try:
  json.dumps=poison;copy.deepcopy=poison
  try:fn()
  except ValueError as exc:msg=str(exc)
  else:raise AssertionError('accepted malformed input')
 finally:json.dumps=jd;copy.deepcopy=cp
 assert not calls;rec.row(label,'REJECTED',error=msg,normalization_calls=0)
try:
 mon=guard(root);m=module(root/'code/correspondence.py');mon(m);data=m.inputs(root);cat=m.catalogue(data);c=data['coverage'];rows,basis=m._checked(data,cat)
 rec.check('current basis invokes actual unchanged predecessor',lambda:sum(x['function']=='derive_client_state' for x in CALLS)==1)
 mt=ast.parse(m.inner(data)['manager']);cls=next(x for x in mt.body if isinstance(x,ast.ClassDef) and x.name=='ManagedAuthority');status=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=='status');ret=next(x.value for x in ast.walk(status) if isinstance(x,ast.Return));selectors={k.value:(v.attr if isinstance(v,ast.Attribute) else v.value) for k,v in zip(ret.keys,ret.values)}
 fields=['phase','reason','connection_epoch','actual_admission','external_nonexecution_established','authorization_renewed']
 rec.check('defining source literal keys selectors and False constants',lambda:list(selectors)==fields and all(type(k.value) is str for k in ret.keys) and list(selectors.values())==['_phase','_reason','_epoch',False,False,False] and all(v.value is False for v in ret.values[3:]))
 launcher,entry=m.sources(data)
 def method(raw,cls,fn):return next(f for x in ast.parse(raw).body if isinstance(x,ast.ClassDef) and x.name==cls for f in x.body if isinstance(f,ast.FunctionDef) and f.name==fn)
 ss=method(launcher,'ManagedSession','status');cs=method(entry,'_Control','status')
 rec.check('defining forwarders retain direct return and owner guard',lambda:ast.unparse(ss.body[0])=='return self.__managed.status()' and [ast.unparse(x) for x in cs.body]==['owner = _OWNERS.get(self.__token)','if owner is None:\n    _fail()','return owner.wrapper.status()'])
 rec.save('source-oracle.json',{'manager_status':ast.dump(status,include_attributes=False),'selectors':selectors,'session_status':ast.dump(ss,include_attributes=False),'control_status':ast.dump(cs,include_attributes=False),'source_identities':[identity(x) for x in [m.inner(data)['manager'],launcher,entry]]})
 fixtures=json.loads((root/'original/fixtures/normal-cases.json').read_bytes())['cases']
 for idx,fx in enumerate(fixtures):
  tag=fx['context'];p=copy.deepcopy(fx['projection']);v={k:copy.deepcopy(x) for k,x in p.items() if k!='returned'};out=c.status_forward_projection(cat,p,v)
  rec.check('legitimate submitted projection '+tag,lambda:c.validate_status_forward_projection(cat,p,v,out))
  rec.check('legitimate full constructed helper '+tag,lambda:m._construct_checked(basis,rows,fx)['projection']==out)
  for field in fields:
   bad=mod(p,('returned',1,'value'),lambda x:key(x,field));assert enc(bad)==enc(p)
   reject_before_normalizing('return literal-key exact type '+field+' '+tag,lambda:c.status_forward_projection(cat,bad,v))
   badout=mod(out,('hops',1,'value'),lambda x:key(x,field));assert enc(badout)==enc(out)
   reject_before_normalizing('submitted literal-key exact type '+field+' '+tag,lambda:c.validate_status_forward_projection(cat,p,v,badout))
   claims=mod(rows,(idx,'validated_manager_samples',0,'value'),lambda x:key(x,field));assert enc(claims)==enc(rows)
   reject_before_normalizing('claim literal-key exact type '+field+' '+tag,lambda:m._check_rows(basis,claims,rows))
  for label,path,T in [('reason',('value','reason'),S),('epoch',('value','connection_epoch'),I),('value dict',('value',),D),('scope dict',('scope',),D),('reference key',('reference',),lambda x:key(x,'symbol'))]:
   bad=mod(p,('returned',1)+path,T);badout=mod(out,('hops',1)+path,T)
   assert enc(bad)==enc(p) and enc(badout)==enc(out)
   reject_before_normalizing('return-input subclass '+label+' '+tag,lambda:c.status_forward_projection(cat,bad,v))
   reject_before_normalizing('submitted-output subclass '+label+' '+tag,lambda:c.validate_status_forward_projection(cat,p,v,badout))
  for label,path,T in [('reason',('validated_manager_samples',0,'value','reason'),S),('sample container',('validated_manager_samples',),L),('sample dict',('validated_manager_samples',0),D),('instance key',('instance_anchor',),lambda x:key(x,'instance')),('literal outer key',(),None)]:
   if path:claims=mod(rows,(idx,)+path,T)
   else:claims=copy.deepcopy(rows);claims[idx]=key(claims[idx],'context')
   assert enc(claims)==enc(rows)
   reject_before_normalizing('semantic preflight '+label+' '+tag,lambda:m.semantic(data,cat,claims))
   reject_before_normalizing('derivation preflight '+label+' '+tag,lambda:m.derive_status(data,cat,claims))
   rec.reject('coordinated bad claims and expected rows '+label+' '+tag,lambda:m._check_rows(None,claims,claims))
  for field,val in [('phase',0),('reason',None),('connection_epoch',True),('actual_admission',0),('external_nonexecution_established',0),('authorization_renewed',0)]:
   bad=mod(out,('hops',1,'value',field),lambda x:val)
   rec.reject('wrong builtin field '+field+' '+tag,lambda:c.validate_status_forward_projection(cat,p,v,bad))
  # Same wrong types placed throughout references, premises and outputs cannot corroborate each other.
  bad=copy.deepcopy(p);bad['scope']['context']=S(tag);vb={k:copy.deepcopy(x) for k,x in bad.items() if k!='returned'}
  reject_before_normalizing('coordinated scope types '+tag,lambda:c.status_forward_projection(cat,bad,vb))
  badcat=copy.deepcopy(cat);badcat['manager_fields']['declarations'][0]['name']=S('phase')
  reject_before_normalizing('coordinated catalogue and bad key '+tag,lambda:c.status_forward_projection(badcat,bad,vb))
  # Aliasing that satisfies the source contract is accepted; no deepcopy assumption on runtime.
  shared=copy.deepcopy(p['returned'][0]['value']);aliased=copy.deepcopy(p)
  for h in aliased['returned']:h['value']=shared
  rec.check('source-permitted equal and shared returned values '+tag,lambda:c.status_forward_projection(cat,aliased,v)['completion']=='normal-return')
  phases=['CLOSED','READY','QUARANTINED','CLEANUP_UNCERTAIN','OPEN_FAILED','VALIDATION_FAILED']
  for pos,phase in enumerate(phases):
   snap={'_phase':phase,'_reason':['','\x00λ\n','x'*10001][pos%3],'_epoch':0 if pos%2 else 10**120};allowed=copy.deepcopy(p);allowed['manager_snapshot']=snap;allowed['references']['owner_failed']=True
   expected={k:snap[x] if type(x) is str else x for k,x in selectors.items()}
   for h in allowed['returned']:h['value']=copy.deepcopy(expected)
   vp={k:copy.deepcopy(x) for k,x in allowed.items() if k!='returned'};got=c.status_forward_projection(cat,allowed,vp)
   rec.check('admitted diagnostic phase '+phase+' '+tag,lambda:got['completion']=='normal-return' and got['prior_owner_failure']['present'] and got['conditional_dictionary_value']==expected)
  # Source-required fixed missing-owner failure remains distinct from termination.
  fail=copy.deepcopy(p);fail['references']['owners[token]']=None;fail['manager_snapshot']=None;fail['returned']=[];fail['outcomes']={'control-call':'normal','owner-lookup':'normal','owner-guard':'normal','fixed-failure':'intended-raise'}
  for outcome,completion,exc in [('intended-raise','intentional-fixed-raise',True),('raise','unexpected-raise',True),('process-termination','process-termination',None)]:
   fail['outcomes']['fixed-failure']=outcome;fv={k:copy.deepcopy(x) for k,x in fail.items() if k!='returned'};got=c.status_forward_projection(cat,fail,fv)
   rec.check('owner guard '+outcome+' '+tag,lambda:got['completion']==completion and got['outcome_classification']['terminal_python_exception_in_model'] is exc and got['cleanup_completion'] is None and not got['authorization_renewed'])
  # Current output mutation must not change the next expectation.
  pristine=enc(out);out['hops'][1]['value'].clear();out['scope']['instance'].clear();out['events'].reverse()
  rec.reject('mutated output cannot set next expectation '+tag,lambda:c.validate_status_forward_projection(cat,p,v,out))
  again=c.status_forward_projection(cat,p,v);rec.check('pristine result repeat after mutations '+tag,lambda:enc(again)==pristine)
 # Helper type logic rejects metaclass tricks and hooks without invoking them.
 class Meta(type):
  def __eq__(self,other):raise AssertionError('metaclass equality')
 class Foreign(str,metaclass=Meta):pass
 class NoCopy(dict):
  def items(self):raise AssertionError('foreign items called')
  def __deepcopy__(self,memo):raise AssertionError('foreign deepcopy called')
 for helper in (c.status_exact_tree,m.status_exact_tree):
  for bad in [Foreign('x'),NoCopy(a=1),L([1]),F(0),B(b'x'),(1,),{False:'x'}]:
   rec.reject(helper.__module__+' foreign-tree '+type(bad).__name__,lambda:helper({'a':[bad]},'INDEPENDENT'))
  shared={'x':[None,False,True,0,0.5,'']};helper([shared,shared],'ALIASES');rec.row('finite shared tree accepted '+helper.__module__,'PASS')
  cycle={};cycle['self']=cycle;rec.reject('cycle rejected '+helper.__module__,lambda:helper(cycle,'INDEPENDENT'))
 # Current expected rows remain pristine after returned assembly changes.
 original=enc(m._assemble(data,rows,basis));assembled=m._assemble(data,rows,basis);assembled['contexts'].reverse();assembled['contexts'][0]['internal_status_return_correspondence']['validated_manager_samples'][0]['snapshot'].clear()
 rec.check('assembly detachment preserves pristine expectations',lambda:enc(m._assemble(data,rows,basis))==original)
 rec.check('corrected receipt corresponds exactly to derived bundle',lambda:original==(root/'results/fresh/corrected-receipt.json').read_bytes())
 rec.check('all eleven obligations and unavailable observations retained',lambda:json.loads(original)['unchanged_obligations']=={'bytes':56813,'sha256':'2c92141711e260a2ef0271635562cbac5a71aae82ac7e1a52b5dbc6f228d3a45'} and all(r['runtime_forwarding_links'] is None and r['observer_join'] is None and r['actual_status_forwarding_count'] is None for r in rows))
 rec.save('limits.json',json.loads(original)['new_internal_status_limits'])
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Independent IS-01 focused checks; constructed inputs, not runtime forwarding')
