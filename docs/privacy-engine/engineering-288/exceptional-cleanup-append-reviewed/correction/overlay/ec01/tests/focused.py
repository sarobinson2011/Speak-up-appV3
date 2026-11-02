"""EC-01 only; one actual fresh recovered public validation, then new focused cores."""
from pathlib import Path
import sys,ast,signal,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
root=Path(sys.argv[1]).resolve();r=Records(sys.argv[2]);failure=None
CORE='actual-authenticated-basis _construct_checked/output-comparison core'
OUTPUT='producer output-comparison core with predecessor-validated premises from actual authenticated basis'
INPUT='exact-type gate before constructed parent validation'
def flag(v,x):
 v=D(v);v['terminal_python_exception_in_model']=x;return v
class I(int):pass
class S(str):pass
def source_audit():
 old=(root/'ec01/original/code/managed_coverage.py').read_bytes();new=(root/'code/managed_coverage.py').read_bytes()
 a=b"'terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True if terminal=='raise' else False,"
 b=b"'terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True,"
 r.yes('only EC01 projector expression changes in producer',lambda:old.count(a)==1 and old.replace(a,b)==new,'source-byte diff')
 olda=(root/'ec01/original/code/correspondence.py').read_text();newa=(root/'code/correspondence.py').read_text()
 line=next(x for x in olda.splitlines() if x.startswith('PRODUCER_PIN='))
 r.yes('adapter changes only producer pin; public predecessor and monitoring unchanged',lambda:olda.replace(line,'PRODUCER_PIN='+repr(identity(new)))==newa,'source-byte diff')
 before=(root/'ec01/original/tests/cases.py').read_text();after=(root/'tests/cases.py').read_text()
 insert=" # EC-01: lab_bootstrap.py:167-171 remains in the constructor-error handler.\n # A normal cleanup append does not establish normal overall return.\n if terminal is None:assert out['terminal_python_exception_in_model'] is True\n"
 r.yes('only missing normal terminal oracle is added',lambda:before.replace(' if terminal:\n',insert+' if terminal:\n')==after,'test-oracle source diff')
 tree=ast.parse((root/'source-evidence/lab_bootstrap.py').read_bytes());fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='_session')
 h=next(x for x in ast.walk(fn) if isinstance(x,ast.ExceptHandler) and x.name=='e');loop=h.body[1];protected=loop.body[0].body[0]
 r.yes('normal close/append remains inside selected BaseException handler',lambda:ast.unparse(h.type)=='BaseException' and h.lineno==167 and loop.lineno==169 and [ast.unparse(x) for x in protected.body]==['obj.close()', "details['cleanup'].append([name, 'close returned'])"] and not any(isinstance(x,(ast.Return,ast.Raise,ast.Yield)) for stmt in protected.body for x in ast.walk(stmt)),'defining-source AST')
 projection=next(x for x in ast.parse(new).body if isinstance(x,ast.FunctionDef) and x.name=='cleanup_append_projection')
 expr=next(v for x in ast.walk(projection) if isinstance(x,ast.Dict) for k,v in zip(x.keys,x.values) if isinstance(k,ast.Constant) and k.value=='terminal_python_exception_in_model')
 r.yes('True covers pending original/replacement; None qualification unchanged',lambda:isinstance(expr.body,ast.Constant) and expr.body.value is None and isinstance(expr.orelse,ast.Constant) and expr.orelse.value is True,'corrected-expression AST')
 r.save('source-oracle.json',{'handler':{'line':h.lineno,'type':ast.unparse(h.type),'error':'e'},'normal_subpath':[ast.unparse(x) for x in protected.body],'normal_terminal_expected':True,'reason':'Validated original remains pending inside handler; normal suboperations do not establish normal overall return.','termination_unobserved_expected':None,'final_rethrow_or_later_cleanup_established':False})
def check_pending(out,expected,original=True):
 assert type(out['terminal_python_exception_in_model']) is (bool if expected is not None else type(None))
 assert out['terminal_python_exception_in_model'] is expected
 assert out['validated_parent']['terminal_python_exception_in_model'] is True
 assert out['validated_parent']['active_caught_error_in_model']==out['earlier_constructor_exception']
 if original:assert out['last_pending_error_in_model']==out['earlier_constructor_exception'] and out['replacement_error_in_model'] is None
 else:assert out['replacement_error_in_model'] is not None and out['last_pending_error_in_model']==out['replacement_error_in_model'] and out['last_pending_error_in_model']!=out['earlier_constructor_exception']
 assert all(out[k] is False for k in ('inner_handler_entry_established','error_report_append_expanded','later_iteration_established','loop_completion_established','failure_file_established','final_rethrow_established','owner_finalization_established','physical_closure_established','durability_established','released_ownership_established','authorization_renewed','actual_admission'))
 assert out['runtime_cleanup_append_chain'] is None and out['observer_join'] is None
 return True
def deadline(signum,frame):raise TimeoutError('EC01-SOFT-DEADLINE; finalization reserved')
try:
 r.save('environment.json',environment());r.save('input-verification.json',verify_root(root));monitor,captures=guard(root,r.path,r)
 source_audit()
 m=module(root/'code/correspondence.py');monitor(m);saved=(root/'ec01/receipts/prepared-cleanup-append.json').read_bytes();historical=(root/'results/recovered/cleanup-append.json').read_bytes()
 r.event('actual-corrected-public-validation-start',new_receipt=identity(saved),historical_receipt=identity(historical),control_deadline_seconds=3150,hard_timeout_seconds=3600)
 signal.signal(signal.SIGALRM,deadline);signal.setitimer(signal.ITIMER_REAL,max(1,3150-(time.monotonic()-r.start)))
 public=m.validate(root,saved);r.save('actual-public-result.json',public)
 r.yes('new prepared receipt validated through actual current public entry',lambda:public['result']=='PASS' and public['contexts']==list(m.CONTEXTS) and public['receipt']==identity(saved),'full current public positive')
 assert len(captures)==1;basis=captures.pop();c=basis['fresh']['coverage'];cat=basis['catalogue'];r.save('predecessor-public-result.json',basis['public_predecessor'])
 r.yes('unchanged actual predecessor public validator passed',lambda:basis['public_predecessor']['result']=='PASS' and basis['public_predecessor']['receipt']==m.PREDECESSOR_RECEIPT,'actual unchanged predecessor public positive')
 r.yes('authenticated derivation matches newly prepared receipt exactly',lambda:m.enc(m._assemble(basis['fresh'],m._rows(basis),basis))==saved,'authenticated-basis assembly comparison')
 r.save('validated-receipt-identity.json',identity(saved))
 r.yes('historical receipt untouched; only new component pins prepared',lambda:identity(historical)=={'bytes':13408039,'sha256':'f37342856f6b0f3ef9d79714a0d412e0273f09b85eb5a1adb5670a1f4accdefb'} and json.loads(saved)['contexts']==json.loads(historical)['contexts'],'saved-byte/receipt comparison')
 r.event('focused-EC01-checks-start',full_public_negative_derivations=0)
 # Reuse exact independent witness, changing only its submitted terminal flag.
 witness=json.loads((root/'ec01/witnesses/EC01-smallest-case.json').read_bytes());counter=json.loads((root/'ec01/witnesses/EC01-source-consistent-one-field-output.json').read_bytes())
 assert flag(witness['output'],True)==counter
 corrected=D(witness);corrected['output']=counter
 accepted=r.yes('retained independent source-consistent counterpart now accepted',lambda:m._construct_checked(basis,corrected),CORE)
 r.yes('retained witness original still pending; only flag differs',lambda:check_pending(accepted['projection'],True) and accepted['projection']==counter,CORE)
 r.no('retained independent old False witness now rejected',lambda:m._construct_checked(basis,witness),CORE,'CLEANUP-OUTPUT-CORRESPONDENCE')
 r.save('corrected-independent-witness-result.json',accepted)
 factory=module(root/'tests/cases.py');fixtures=json.loads((root/'results/recovered/fixtures.json').read_bytes());assert len(fixtures)==4
 normal_summaries=[];frontiers=[]
 for index,old in enumerate(fixtures):
  idx=index//2;control=bool(index%2);tag=str((idx,control));fx=D(old);fx['output']=flag(old['output'],True)
  got=r.yes('corrected normal result '+tag,lambda fx=fx:m._construct_checked(basis,fx),CORE)
  r.yes('source-grounded normal terminal oracle '+tag,lambda got=got,control=control:factory.oracle(got['projection'],cat['source'],control) and check_pending(got['projection'],True),'source-grounded test oracle over authenticated result')
  r.no('old False normal flag '+tag,lambda old=old:m._construct_checked(basis,old),CORE,'CLEANUP-OUTPUT-CORRESPONDENCE')
  r.no('oracle catches previously omitted False flag '+tag,lambda old=old,control=control:factory.oracle(old['output'],cat['source'],control),'test oracle only',exception=AssertionError)
  v=m._premises(basis,fx)
  for wrong in (None,1,'True'):
   bad=flag(fx['output'],wrong);r.no('wrong exact terminal value '+tag+repr(wrong),lambda bad=bad,v=v,fx=fx:c.validate_cleanup_append_projection(cat,fx['projection'],v,bad),OUTPUT,'CLEANUP-OUTPUT-CORRESPONDENCE')
  for label,modify in [('subclassed integer',lambda o:o.__setitem__('terminal_python_exception_in_model',I(1))),('subclassed literal key',lambda o:o.__setitem__(S('terminal_python_exception_in_model'),o.pop('terminal_python_exception_in_model'))),('nested subclassed error reference',lambda o:o['earlier_constructor_exception'].__setitem__('reference',S(o['earlier_constructor_exception']['reference'])))]:
   bad=D(fx);modify(bad['output']);r.no('exact typing '+tag+label,lambda bad=bad:m._construct_checked(basis,bad),INPUT,'CLEANUP-CONSTRUCTED-INPUT')
  # Returned nested objects are never validation expectations.
  got['projection']['last_pending_error_in_model'].clear();got['projection']['binding']['references']['owner'].clear();got['projection']['validated_parent'].clear()
  r.yes('nested returned mutations leave normal expectations isolated '+tag,lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'],CORE)
  normal_summaries.append({'context':fx['context'],'control':control,'scope':fx['output']['scope'],'flag':True,'original_pending':True,'runtime_observation':False})
  for kind in ('raise','process-termination','unobserved'):
   q=factory.normal(m,basis,idx,control=control,invocation='ec01-frontier',terminal=('append-call-attempt',kind))
   out=r.yes('append frontier '+tag+kind,lambda q=q:m._construct_checked(basis,q),CORE)['projection']
   expected=True if kind=='raise' else None
   r.yes('pending/replacement/None classification '+tag+kind,lambda out=out,expected=expected,kind=kind:check_pending(out,expected,original=kind!='raise') and out['close_normal_return_completed_in_model'] is True and out['close_itself_failed_established_in_model'] is False,'source-grounded frontier oracle')
   bad=flag(q['output'],False if expected is True else True);qbad=D(q);qbad['output']=bad
   r.no('contradictory frontier flag '+tag+kind,lambda qbad=qbad:m._construct_checked(basis,qbad),CORE,'CLEANUP-OUTPUT-CORRESPONDENCE')
   frontiers.append({'context':q['context'],'control':control,'kind':kind,'flag':expected,'scope':out['scope'],'replacement':out['replacement_error_in_model'],'partial_effects':out['cleanup_list_after_frontier']})
  gate=next(e['address'] for e in fx['projection']['close_result']['events'] if e['event']=='premise' and e['kind']=='call:self._retired.close')
  q=factory.normal(m,basis,idx,control=control,invocation='ec01-close-failure',terminal=('close-normal-return','raise'),close_outcomes={gate:'raise'})
  out=r.yes('close replacement exception retains True '+tag,lambda q=q:m._construct_checked(basis,q),CORE)['projection']
  r.yes('close failure remains distinct from append failure '+tag,lambda out=out:check_pending(out,True,original=False) and out['close_itself_failed_established_in_model'] is True and out['close_normal_return_completed_in_model'] is False,'source-grounded frontier oracle')
  qbad=D(q);qbad['output']=flag(q['output'],False);r.no('False after close replacement exception '+tag,lambda qbad=qbad:m._construct_checked(basis,qbad),CORE,'CLEANUP-OUTPUT-CORRESPONDENCE')
 r.no('historical receipt not silently substituted for corrected receipt',lambda:m._receipt_checked(basis,historical),'authenticated-basis receipt-comparison core','CLEANUP-STALE-OR-ALTERED-RECEIPT')
 r.save('normal-cases.json',normal_summaries);r.save('frontier-cases.json',frontiers)
 r.save('validation-layers.json',{'full_corrected_public_positive':1,'actual_unchanged_predecessor_public_positive':1,'full_public_negative_derivations':0,'negatives':'Each row names exact-input, authenticated-basis constructed/output/receipt core, or test-oracle layer. No core negative is a full public negative derivation.','historical_witness_execution':'Only the corrected code consumes retained witnesses; old completed campaigns are not replayed.'})
 signal.setitimer(signal.ITIMER_REAL,0);r.event('finalization-start',time_reserved_seconds=3600-(time.monotonic()-r.start))
 r.save('final-verification.json',verify_root(root));r.event('finished')
except BaseException:
 failure=traceback.format_exc();r.save('failure.json',{'traceback':failure});raise
finally:
 signal.setitimer(signal.ITIMER_REAL,0)
 r.finish(failure,requests=0,acquisitions=0,database_connections=0,session_operations=0,Git_saves=0,completed_campaigns_replayed=False)
