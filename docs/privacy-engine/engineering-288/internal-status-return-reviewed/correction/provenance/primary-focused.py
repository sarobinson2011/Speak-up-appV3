"""New IS-01 exact-type controls, saved evidence only; no historic suite rerun."""
from pathlib import Path
import sys,copy,json,traceback,ast
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None;write='--write' in sys.argv
class S(str):pass
class I(int):pass
class D(dict):pass
class L(list):pass
class F(float):pass
class B(bytes):pass
# Match the review's builtin-named subclasses as well as arbitrary names.
NS=type('str',(str,),{});NI=type('int',(int,),{});ND=type('dict',(dict,),{})
def replace_at(value,path,fn):
 parent=value
 for k in path[:-1]:parent=parent[k]
 parent[path[-1]]=fn(parent[path[-1]])
def key_sub(value,key):
 return {S(k) if k==key else k:v for k,v in value.items()}
def modified(value,path,fn):
 value=copy.deepcopy(value);replace_at(value,path,fn);return value
try:
 mon=guard(root);m=module(root/'code/correspondence.py');mon(m);d=m.inputs(root);cat=m.catalogue(d);c=d['coverage'];fixtures=json.loads((root/'original/fixtures/normal-cases.json').read_bytes())['cases']
 rows,basis=m._checked(d,cat);bundle=m._assemble(d,rows,basis)
 rec.check('both contexts independently validated through actual predecessor',lambda:[r['context'] for r in rows]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and sum(x['function']=='derive_client_state' for x in CALLS)==1)
 # Exact original output preserved except the two intentional current code pins.
 old=json.loads((root/'original/results/status-forward-correspondence.json').read_bytes())
 rec.check('only current code identities change pristine receipt',lambda:all(enc(v)==enc(bundle[k]) for k,v in old.items() if k!='extension_components') and set(old)==set(bundle))
 launcher,entry=m.sources(d);fields=m.manager_fields(d);boundary=m.inner(d)['ctx']['binding']
 rec.check('pristine source declaration accepted',lambda:c.validate_status_forward(launcher,entry,fields,boundary,cat))
 # Independent defining-source audit; expected types do not come from the candidate catalogue.
 mt=ast.parse(m.inner(d)['manager']);status=next(f for cls in mt.body if isinstance(cls,ast.ClassDef) and cls.name=='ManagedAuthority' for f in cls.body if isinstance(f,ast.FunctionDef) and f.name=='status');ret=next(n.value for n in ast.walk(status) if isinstance(n,ast.Return));selectors={k.value:v.attr if isinstance(v,ast.Attribute) else v.value for k,v in zip(ret.keys,ret.values)}
 rec.check('source literal keys and three exact False expressions',lambda:all(type(k.value) is str for k in ret.keys) and list(selectors)==['phase','reason','connection_epoch','actual_admission','external_nonexecution_established','authorization_renewed'] and all(selectors[k] is False for k in list(selectors)[3:]))
 def sourcevalue(snap):return {k:snap[v] if type(v) is str else v for k,v in selectors.items()}
 for idx,fx in enumerate(fixtures):
  tag=fx['context'];p=copy.deepcopy(fx['projection']);val={k:copy.deepcopy(v) for k,v in p.items() if k!='returned'};out=c.status_forward_projection(cat,p,val)
  rec.check('pristine return-input and submitted-output '+tag,lambda:c.validate_status_forward_projection(cat,p,val,out))
  rec.check('pristine constructed adapter '+tag,lambda:m._construct_checked(basis,rows,fx)['projection']==out)
  def rejected(label,fn):rec.reject(label+' '+tag,fn)
  # Review reason witness and adjacent exact types at every return/output level.
  mutations=[('reason',('hops',1,'value','reason'),S),('named reason',('hops',1,'value','reason'),NS),('epoch',('hops',1,'value','connection_epoch'),I),('named epoch',('hops',1,'value','connection_epoch'),NI),('dict',('hops',1,'value'),D),('named dict',('hops',1,'value'),ND),('hop dict',('hops',1),D),('hops list',('hops',),L),('hops tuple',('hops',),tuple),('nested scope',('hops',1,'scope','instance'),D),('scope string',('hops',1,'scope','context'),S),('literal key',('hops',1,'value'),lambda v:key_sub(v,'phase')),('outer key',('hops',1),lambda v:key_sub(v,'value')),('reference key',('hops',1,'reference'),lambda v:key_sub(v,'symbol'))]
  for label,path,change in mutations:
   bad=modified(out,path,change);assert enc(bad)==enc(out)
   rejected('submitted-output rejects '+label,lambda bad=bad:c.validate_status_forward_projection(cat,p,val,bad))
   ipath=('returned',)+path[1:];bad=modified(p,ipath,change);assert enc(bad)==enc(p)
   rejected('return-input rejects '+label,lambda bad=bad:c.status_forward_projection(cat,bad,val))
   fc=copy.deepcopy(fx);fc['projection']=bad
   rejected('constructed entry rejects '+label,lambda fc=fc:m.constructed_projection(d,cat,fc))
  # Exact fields: builtin distinctions, not merely subclass filtering.
  for field,v in [('phase',1),('reason',[]),('connection_epoch',True),('connection_epoch',1.0),('actual_admission',0),('external_nonexecution_established',0),('authorization_renewed',0)]:
   bad=copy.deepcopy(out);bad['hops'][1]['value'][field]=v
   rejected('submitted-output rejects wrong builtin '+field+' '+type(v).__name__,lambda bad=bad:c.validate_status_forward_projection(cat,p,val,bad))
  for field,T in [('_phase',S),('_reason',NS),('_epoch',I)]:
   bad=modified(p,('manager_snapshot',field),T);vbad={k:copy.deepcopy(v) for k,v in bad.items() if k!='returned'}
   rejected('coordinated snapshot and premise subclasses '+field,lambda bad=bad,vbad=vbad:c.status_forward_projection(cat,bad,vbad))
   rejected('snapshot entry subclass '+field,lambda bad=bad:c.status_snapshot_value(cat,bad['manager_snapshot']))
  bad=copy.deepcopy(p);bad['manager_snapshot']=key_sub(bad['manager_snapshot'],'_reason');vbad={k:copy.deepcopy(v) for k,v in bad.items() if k!='returned'}
  rejected('snapshot literal key in coordinated premises',lambda:c.status_forward_projection(cat,bad,vbad))
  # Semantic claim nested values, keys, lists, dictionaries, and arbitrary/builtin-name types.
  claimmut=[('sample reason',('validated_manager_samples',0,'value','reason'),S),('named reason',('validated_manager_samples',0,'value','reason'),NS),('sample epoch',('validated_manager_samples',0,'value','connection_epoch'),I),('sample dictionary',('validated_manager_samples',0,'value'),D),('sample key',('validated_manager_samples',0,'value'),lambda v:key_sub(v,'phase')),('sample list',('validated_manager_samples',),L),('conditional links',('conditional_links',),tuple),('nested declaration key',('declaration',),lambda v:key_sub(v,'format')),('context',('context',),S),('anchor dictionary',('instance_anchor',),D),('reference scope',('scope',),D)]
  for label,path,change in claimmut:
   claims=modified(rows,(idx,)+path,change);assert enc(claims)==enc(rows)
   rejected('semantic row check '+label,lambda claims=claims:m._check_rows(basis,claims,rows))
   rejected('semantic public entry '+label,lambda claims=claims:m.semantic(d,cat,claims))
   rejected('derive public entry '+label,lambda claims=claims:m.derive_status(d,cat,claims))
   # Coordinated contamination of caller-supplied comparison rows must not bypass types.
   rejected('coordinated row claim/expectation '+label,lambda claims=claims:m._check_rows(None,claims,copy.deepcopy(claims)))
  # All source-admitted phases remain available, no artificial string/epoch limits.
  for phase in cat['source']['source_phase_literals']:
   snap={'_phase':phase,'_reason':'\x00λ\nexception-derived content / '+('x'*8193),'_epoch':10**40}
   case=copy.deepcopy(p);case['manager_snapshot']=snap;case['references']['owner_failed']=True
   for hop in case['returned']:hop['value']=sourcevalue(snap)
   premise={k:copy.deepcopy(v) for k,v in case.items() if k!='returned'}
   got=c.status_forward_projection(cat,case,premise)
   rec.check('legitimate non-READY diagnostic '+phase+' '+tag,lambda:got['completion']=='normal-return' and got['prior_owner_failure']['present'] and c.validate_status_forward_projection(cat,case,premise,got))
  # Source owner/token guard and termination distinction remain present.
  case=copy.deepcopy(p);case['references']['owners[token]']=None;case['manager_snapshot']=None;case['returned']=[];case['outcomes']={s:'normal' for s in ['control-call','owner-lookup','owner-guard']};case['outcomes']['fixed-failure']='intended-raise';premise={k:copy.deepcopy(v) for k,v in case.items() if k!='returned'};got=c.status_forward_projection(cat,case,premise)
  rec.check('owner absence fixed raise preserved '+tag,lambda:got['completion']=='intentional-fixed-raise' and got['outcome_classification']['terminal_python_exception_in_model'] is True)
  case['outcomes']['fixed-failure']='process-termination';premise={k:copy.deepcopy(v) for k,v in case.items() if k!='returned'};got=c.status_forward_projection(cat,case,premise)
  rec.check('termination proves no exception or cleanup '+tag,lambda:got['completion']=='process-termination' and got['outcome_classification']['terminal_python_exception_in_model'] is None and got['retained_error'] is None and got['cleanup_completion'] is None and not got['authorization_renewed'])
  # Exact normalization guard alone is insufficient: builtin substituted values still reject.
  claims=copy.deepcopy(rows);claims[idx]['validated_manager_samples'][0]['value']['reason']='wrong builtin reason'
  rejected('semantic same-type changed value',lambda:m._check_rows(basis,claims,rows))
  bad=copy.deepcopy(out);bad['hops'][1]['reference']['symbol']='wrong builtin reference';rejected('output same-type wrong reference',lambda:c.validate_status_forward_projection(cat,p,val,bad))
  forged=copy.deepcopy(rows);forged[idx]['context']=rows[1-idx]['context'];rejected('required context independently enforced',lambda:m._check_rows(basis,forged,rows))
  # Returned representations cannot become mutable validation expectations.
  out['hops'][1]['value']['reason']='mutation';out['events'].clear();out['scope']['instance'].clear()
  pristine=c.status_forward_projection(cat,p,val);rec.check('nested output mutations isolated '+tag,lambda:c.validate_status_forward_projection(cat,p,val,pristine))
  rejected('changed old result does not change expectation',lambda:c.validate_status_forward_projection(cat,p,val,out))
 # Declared source schema and helper boundaries also preflight before normalization.
 for path,T in [(('declarations',),L),(('source','epoch_initial'),I),(('format',),S),(('declarations',0,'type','fields'),lambda v:key_sub(v,'phase'))]:
  bad=modified(cat,path,T)
  rec.reject('source validator rejects subclass '+str(path),lambda bad=bad:c.validate_status_forward(launcher,entry,fields,boundary,bad))
  rec.reject('full semantic catalogue rejects subclass '+str(path),lambda bad=bad:m.semantic(d,bad))
  rec.reject('producer projection rejects subclass catalogue '+str(path),lambda bad=bad:c.status_forward_projection(bad,p,val))
 # Hooks cannot run in place of exact-type checks. Poison normalizers with tripwire.
 class Meta(type):
  def __eq__(self,other):raise AssertionError('type equality hook invoked')
 class Sneaky(str,metaclass=Meta):pass
 class Poison(str):
  def __str__(self):raise AssertionError('string coercion hook invoked')
  def __eq__(self,other):raise AssertionError('equality hook invoked')
 for helper in [m.status_exact_tree,c.status_exact_tree]:
  for item in [Sneaky('x'),Poison('x'),F(1.0),B(b'x'),(1,),{1:'x'}]:
   rec.reject('exact tree rejects foreign type without hooks '+type(item).__name__,lambda helper=helper,item=item:helper({'nested':[item]},'FOCUSED'))
  shared={'reason':'same'};helper([shared,shared],'SHARED');rec.row('repeated representational aliases permitted','PASS')
  cycle=[];cycle.append(cycle);rec.reject('cyclic representations rejected without serialization',lambda helper=helper:helper(cycle,'FOCUSED'))
 # Both supplied output and claim checks must precede encoder, equality and copy.
 normalizer=json.dumps
 def poison(*a,**k):raise AssertionError('normalization before type check')
 bad=copy.deepcopy(pristine);bad['hops'][1]['value']['reason']=S(bad['hops'][1]['value']['reason']);claims=copy.deepcopy(rows);claims[0]['validated_manager_samples'][0]['value']['reason']=S(claims[0]['validated_manager_samples'][0]['value']['reason'])
 for label,fn in [('output',lambda:c.validate_status_forward_projection(cat,p,val,bad)),('claims',lambda:m._check_rows(basis,claims,rows)),('full claims',lambda:m.derive_status(d,cat,claims))]:
  try:
   json.dumps=poison
   try:fn()
   except ValueError:pass
   else:raise AssertionError('type accepted')
  finally:json.dumps=normalizer
  rec.row('type gate precedes serialization '+label,'PASS')
 # Independently assembled outputs are detached from basis and from each other.
 before=enc(m._assemble(d,rows,basis));bundle['contexts'][0]['internal_status_return_correspondence']['validated_manager_samples'][0]['value']['reason']='changed';bundle['contexts'].clear();rec.check('nested bundle mutation cannot alter expectation',lambda:enc(m._assemble(d,rows,basis))==before)
 receipt=m.enc(m._assemble(d,rows,basis));json_bundle=json.loads(receipt);m._check_rows(basis,[r['internal_status_return_correspondence'] for r in json_bundle['contexts']],rows);rec.row('pristine public JSON representation accepted internally','PASS')
 if write:rec.save('corrected-receipt.json',json_bundle)
 else:rec.check('recovered receipt exact reproduction',lambda:(root/'results/primary/corrected-receipt.json').read_bytes()==receipt)
 rec.check('runtime forwarding remains unavailable; observer stays unjoined',lambda:all(r['runtime_forwarding_links'] is None and r['observer_join'] is None for r in rows))
 rec.save('boundaries.json',json_bundle['new_internal_status_limits'])
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Engineering focused IS-01 controls only; independent review totals separate')
