from pathlib import Path
import sys,json,ast,difflib,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
root=Path(sys.argv[1]);r=Records(sys.argv[2]);error=None
def require(v):assert v;return True
try:
 r.save('input-verification.json',verify_root(root));guard(root,r.path,r);c=module(root/'code/managed_coverage.py')
 entry=(root/'source-evidence/prospective_entry.py').read_bytes();launcher=(root/'source-evidence/lab_bootstrap.py').read_bytes();text=entry.decode();tree=ast.parse(text)
 parent={child:(node,field,index) for node in ast.walk(tree) for field,value in ast.iter_fields(node) for index,child in (enumerate(value) if isinstance(value,list) else [(None,value)]) if isinstance(child,ast.AST)}
 run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run')
 expressions=[n for n in ast.walk(run) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='Client'];assert len(expressions)==1;attempt=expressions[0]
 call=parent[attempt][0];statement=parent[call][0];client_try=parent[statement][0];protected=parent[client_try][0];withnode=parent[protected][0]
 assert ast.unparse(call.func)=='client' and call.args==[attempt] and not call.keywords and ast.unparse(attempt)=='Client(token)'
 assert isinstance(client_try,ast.Try) and client_try.body==[statement] and len(client_try.handlers)==1 and not client_try.finalbody and not client_try.orelse
 handler=client_try.handlers[0];guardnode=handler.body[0];bare=handler.body[1]
 assert ast.unparse(handler.type)=='BaseException' and handler.name=='client_error'
 assert ast.unparse(guardnode.test)=='owner.failure is not None' and not guardnode.orelse
 assert isinstance(bare,ast.Raise) and bare.exc is bare.cause is None
 assert len(protected.finalbody)==1;pop=protected.finalbody[0];assert ast.unparse(pop)=='_OWNERS.pop(token, None)'
 control=protected.body[0];assert ast.unparse(control.test)=='control is not None' and ast.unparse(control.body[0])=='control(_Control(token))'
 assert protected.body==[control,client_try,protected.body[-1]] and ast.unparse(protected.body[-1])=='if owner.failure is not None:\n    raise owner.failure'
 prefix=withnode.body[:withnode.body.index(protected)];assert [ast.unparse(n) for n in prefix]==['owner = _Owner(wrapper)','token = object()','_OWNERS[token] = owner']
 client=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Client');init=next(n for n in client.body if isinstance(n,ast.FunctionDef) and n.name=='__init__')
 assert [a.arg for a in init.args.args]==['self','token'] and len(init.body)==1 and ast.unparse(init.body[0])=='self.__token = token'
 def loc(n):return {'site':':'.join(map(str,[n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__])),'expression':ast.get_source_segment(text,n)}
 def guards(n):
  chain=[]
  while n in parent:
   p,f,i=parent[n]
   if isinstance(p,ast.If):chain.append({'kind':'if','arm':f,'test':loc(p.test)})
   elif isinstance(p,ast.Try):chain.append({'kind':'try','region':f,'handlers':[ast.unparse(h.type) if h.type else 'BaseException' for h in p.handlers]})
   elif isinstance(p,(ast.With,ast.AsyncWith)):chain.append({'kind':'with','contexts':[ast.unparse(i.context_expr) for i in p.items]})
   n=p
  return chain[::-1]
 receipt=json.loads((root/'results/primary/client-construction-none.json').read_bytes());old=json.loads((root/'retained/control-construction/results/primary/control-construction.json').read_bytes())
 keys=['control_construction_revocation_correspondence','control_exception_revocation_correspondence','callback_bare_rethrow_correspondence','callback_stored_failure_correspondence','stored_failure_revocation_correspondence','token_registration_correspondence','client_handle_return_correspondence','client_state_return_correspondence']
 nodes={'run':run,'construction_expression':attempt,'initializer_source':init,'initializer_assignment_source':init.body[0],'client_call_not_reached':statement,'handler':handler,'guard':guardnode.test,'raise':bare,'control_guard':control.test}
 stages=[('callback-handler-enter',handler),('callback-none-guard',guardnode.test),('callback-bare-rethrow',bare),('finally-enter',protected),('removal-attempt',pop.value),('removal-complete',pop)]
 for idx,row in enumerate(receipt['contexts']):
  cat=row['client_construction_none_correspondence']['declaration'];src=cat['source'];deps=[row[k]['declaration'] for k in keys]
  for name,n in nodes.items():r.yes('independently derived location '+str((idx,name)),lambda name=name,n=n:require(all(src[name][k]==v for k,v in loc(n).items())))
  r.yes('argument construction protected by client handler '+str(idx),lambda:require(src['construction_expression']['guards']==guards(attempt)))
  r.yes('source exact None branch and bare raise '+str(idx),lambda:require(src['guard_expression']=='owner.failure is not None' and src['selected_guard_result'] is False and src['selected_slot_value'] is None and src['selected_slot_exact_type']=='NoneType' and src['raise_syntax']=='raise' and src['bare_raise_has_explicit_cause_clause'] is False))
  r.yes('independently derived both prefix sequences '+str(idx),lambda:require(src['prefix_order_control_absent']==['owner-create','token-create','registry-insert','control-guard','client-create'] and src['prefix_order_control_present']==['owner-create','token-create','registry-insert','control-guard','control-create','control-callback','client-create']))
  for name,n in stages:r.yes('independent stage coordinate '+str((idx,name)),lambda name=name,n=n:require(all(src['stages'][name][k]==v for k,v in loc(n).items()) and src['stages'][name]['source']==identity(entry)))
  r.yes('six mandatory semantic boundaries retain source order '+str(idx),lambda:require(src['order']==[n for n,_ in stages] and [d['id'] for d in cat['declarations']]==src['order'] and all(d['source_origin']==src['stages'][d['id']] and d['classification']=='UNKNOWN' and d['multiplicity'] is None and d['ordinal'] is None for d in cat['declarations'])))
  for field in ('allocation_progress_established','initializer_entry_established','initializer_assignment_established','completed_client_object_established','client_callback_execution_established','new_explicit_cause_assignment'):r.yes('source does not establish '+str((idx,field)),lambda field=field:require(src[field] is False))
  r.yes('all original context fields and ordinals preserved '+str(idx),lambda:require(all(row[k]==v for k,v in old['contexts'][idx].items()) and set(row)-set(old['contexts'][idx])=={'client_construction_none_correspondence'}))
  r.yes('current catalogue accepts actual defining source '+str(idx),lambda:c.validate_client_construction(launcher,entry,*deps,cat))
  for field,val in [('guard_expression','not owner.failure'),('selected_slot_value',0),('selected_guard_result',0),('client_callback_execution_established',True),('argument_expression','other_token')]:
   bad=D(cat);bad['source'][field]=val;r.no('source-derived catalogue rejects alteration '+str((idx,field)),lambda bad=bad:c.validate_client_construction(launcher,entry,*deps,bad),'CLIENT-CONSTRUCTION-SOURCE-CORRESPONDENCE')
  bad=D(cat);bad['source']['order'].remove('callback-none-guard');bad['declarations']=[d for d in bad['declarations'] if d['id']!='callback-none-guard'];del bad['source']['stages']['callback-none-guard'];r.no('coordinated source guard omission '+str(idx),lambda bad=bad:c.validate_client_construction(launcher,entry,*deps,bad),'CLIENT-CONSTRUCTION-SOURCE-CORRESPONDENCE')
  if idx==0:
   for before,after in [(b'client(Client(token))',b'client(Client(None))'),(b'if owner.failure is not None:',b'if owner.failure != None:')]:
    changed=entry.replace(before,after);assert changed!=entry;r.no('substituted producer source cannot inherit shape '+before.decode(),lambda changed=changed:c.validate_client_construction(launcher,changed,*deps,cat))
 r.save('independent-source-expectations.json',{'entry':identity(entry),'locations':{k:loc(n) for k,n in nodes.items()},'stage_locations':{k:loc(n) for k,n in stages},'guards':guards(attempt),'registration_prefix':[ast.unparse(n) for n in prefix],'independent_source_claim':'Conditional Client argument failure before invocation, same-owner exact-None premise, existing-cause uncertainty, three separate finally/removal boundaries'})
 changes=json.loads((root/'provenance/changed-files.json').read_bytes());diff='';definitions={}
 for n in ('code/managed_coverage.py','code/correspondence.py'):
  before=(root/'retained/control-construction'/n).read_bytes();after=(root/n).read_bytes();assert identity(before)==changes['intentional_changes'][n]['before'] and identity(after)==changes['intentional_changes'][n]['after']
  diff+=''.join(difflib.unified_diff(before.decode().splitlines(True),after.decode().splitlines(True),fromfile='retained/control-construction/'+n,tofile=n))
  if n.endswith('managed_coverage.py'):
   a=ast.parse(before);b=ast.parse(after);af={n.name:n for n in a.body if isinstance(n,ast.FunctionDef)};bf={n.name:n for n in b.body if isinstance(n,ast.FunctionDef)}
   assert len(af)==123 and len(bf)==129
   for name,node in af.items():assert ast.get_source_segment(before.decode(),node)==ast.get_source_segment(after.decode(),bf[name]),name
   assert all(ast.dump(x)==ast.dump(y) for x,y in zip(a.body,b.body)) and len(b.body)==len(a.body)+6
   definitions={'inherited_unchanged':123,'new':sorted(set(bf)-set(af))}
 assert diff==(root/'provenance/implementation.diff').read_text()
 for n in ('prospective_entry.py','lab_bootstrap.py'):assert (root/'source-evidence'/n).read_bytes()==(root/'retained/control-construction/source-evidence'/n).read_bytes()
 # Independent log reconciliation, never execution of the supplied campaign.
 supplied={}
 for label,n in [('primary',498),('recovered',210)]:
  result=json.loads((root/'results'/label/'RESULT.json').read_bytes());progress=[json.loads(s) for s in (root/'results'/label/'progress.jsonl').read_text().splitlines()];stdout=[]
  for line in (root/'processes'/label/'stdout.log').read_text().splitlines():
   a=line.split(' ',1)
   if len(a)==2 and a[0].isdigit():name,status=a[1].rsplit(' ',1);stdout.append((int(a[0]),name,status))
  ex=json.loads((root/'processes'/label/'exit-status.json').read_bytes());assert result['result']=='PASS' and result['checks']==n and len(progress)==len(stdout)==n and result['rows']==progress
  assert [(i+1,x['check'],x['result']) for i,x in enumerate(progress)]==stdout and ex['returncode']==0 and not ex['timed_out']
  supplied[label]={'corroborated_rows':n,'result':identity((root/'results'/label/'RESULT.json').read_bytes()),'exit':ex,'environment':result['environment'],'not_independent_controls':True}
 limits=receipt['new_client_construction_limits'];assert limits['inventory_unknown_totals']==4 and limits['lifetime_unknown_totals']==14 and limits['all_eleven_obligations_preserved'] is True and limits['actual_admission'] is False
 r.save('preservation-and-supplied.json',{'definitions':definitions,'declared_diff_exact':True,'runtime_sources_unchanged':True,'all_old_context_fields_unchanged':True,'supplied':supplied,'scope_limits':limits,'intermediate_cut_outer_identity_freshly_verified':False,'qualified_prior_records':json.loads((root/'provenance/prior-review-incorporation.json').read_bytes()),'new_failures':json.loads((root/'RESULTS.json').read_bytes())['new_failed_attempts']})
 r.save('final-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(r.path/'failure.txt').write_text(error);raise
finally:r.finish(error,scope='New source-derived catalogue controls and read-only preservation/supplied-record audit; no prior campaign reruns')
