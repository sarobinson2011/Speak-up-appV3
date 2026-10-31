from pathlib import Path
import sys,json,ast,difflib,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
root=Path(sys.argv[1]);r=Records(sys.argv[2]);error=None
def require(condition):assert condition;return True
try:
 monitor,_=guard(root,r.path,r);c=module(root/'code/managed_coverage.py')
 entry=(root/'source-evidence/prospective_entry.py').read_bytes();launcher=(root/'source-evidence/lab_bootstrap.py').read_bytes();text=entry.decode();tree=ast.parse(text)
 parent={child:(node,field,index) for node in ast.walk(tree) for field,value in ast.iter_fields(node) for index,child in (enumerate(value) if isinstance(value,list) else [(None,value)]) if isinstance(child,ast.AST)}
 run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run')
 calls=[n for n in ast.walk(run) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='_Control'];assert len(calls)==1;construction=calls[0]
 call=parent[construction][0];statement=parent[call][0];guardnode=parent[statement][0];protected=parent[guardnode][0];withnode=parent[protected][0]
 assert isinstance(call,ast.Call) and ast.unparse(call.func)=='control' and call.args==[construction] and not call.keywords
 assert ast.unparse(construction)=='_Control(token)' and ast.unparse(guardnode.test)=='control is not None'
 assert isinstance(protected,ast.Try) and protected.handlers==[] and protected.orelse==[]
 pop=protected.finalbody[0];assert len(protected.finalbody)==1 and isinstance(pop,ast.Expr) and ast.unparse(pop)=='_OWNERS.pop(token, None)'
 client=next(x for x in protected.body if isinstance(x,ast.Try));assert client.lineno>call.lineno and ast.unparse(client.body[0])=='client(Client(token))'
 assert all(node is not client for node,_,_ in [parent[construction],parent[call],parent[statement],parent[guardnode]])
 initclass=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='_Control');init=next(n for n in initclass.body if isinstance(n,ast.FunctionDef) and n.name=='__init__')
 assert [x.arg for x in init.args.args]==['self','token'] and len(init.body)==1 and ast.unparse(init.body[0])=='self.__token = token'
 prefix=withnode.body[:withnode.body.index(protected)];assert [ast.unparse(x) for x in prefix]==['owner = _Owner(wrapper)','token = object()','_OWNERS[token] = owner']
 def site(n):return ':'.join(map(str,[n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__]))
 def loc(n):return {'site':site(n),'expression':ast.get_source_segment(text,n)}
 def guards(n):
  chain=[]
  while n in parent:
   p,f,i=parent[n]
   if isinstance(p,ast.If):chain.append({'kind':'if','arm':f,'test':loc(p.test)})
   elif isinstance(p,ast.Try):chain.append({'kind':'try','region':f,'handlers':[ast.unparse(h.type) if h.type else 'BaseException' for h in p.handlers]})
   elif isinstance(p,(ast.With,ast.AsyncWith)):chain.append({'kind':'with','contexts':[ast.unparse(i.context_expr) for i in p.items]})
   n=p
  return chain[::-1]
 receipt=json.loads((root/'results/primary/control-construction.json').read_bytes());old=json.loads((root/'retained/control/results/primary/control-exception.json').read_bytes())
 keys=['control_exception_revocation_correspondence','callback_bare_rethrow_correspondence','callback_stored_failure_correspondence','stored_failure_revocation_correspondence','token_registration_correspondence','client_handle_return_correspondence','client_state_return_correspondence']
 expected_nodes={'run':run,'construction_expression':construction,'control_guard':guardnode.test,'control_call_not_reached':statement,'client_handler_not_reached':client.handlers[0],'initializer_source':init,'initializer_assignment_source':init.body[0]}
 for index,row in enumerate(receipt['contexts']):
  cat=row['control_construction_revocation_correspondence']['declaration'];src=cat['source'];deps=[row[k]['declaration'] for k in keys]
  for name,n in expected_nodes.items():
   r.yes('source location/expression '+str((index,name)),lambda name=name,n=n:require(all(src[name][k]==v for k,v in loc(n).items())))
  r.yes('independent construction guard ancestry '+str(index),lambda:require(src['construction_expression']['guards']==guards(construction)))
  r.yes('argument precedes callback; initializer assignment only '+str(index),lambda:require(src['constructor_expression']=='_Control' and src['argument_expression']=='token' and src['guard_expression']=='control is not None' and src['selected_guard_result'] is True))
  r.yes('source registration prefix '+str(index),lambda:require(src['prefix_order']==['owner-create','token-create','registry-insert','control-guard','control-create']))
  for name,n in [('finally-enter',protected),('removal-attempt',pop.value),('removal-complete',pop)]:
   r.yes('independent continuation coordinate '+str((index,name)),lambda name=name,n=n:require(all(src['stages'][name][k]==v for k,v in loc(n).items()) and src['stages'][name]['source']==identity(entry)))
  r.yes('three mandatory regions without extra source statements '+str(index),lambda:require(src['order']==['finally-enter','removal-attempt','removal-complete'] and [d['id'] for d in cat['declarations']]==src['order'] and all(d['source_origin']==src['stages'][d['id']] and d['classification']=='UNKNOWN' and d['multiplicity'] is None and d['ordinal'] is None for d in cat['declarations'])))
  for field in ('allocation_progress_established','initializer_entry_established','initializer_assignment_established','completed_control_object_established','control_callback_execution_established','client_callback_execution_established','client_handler_applies','owner_failure_guard_applies','new_explicit_cause_assignment'):
   r.yes('source does not establish '+str((index,field)),lambda field=field:require(src[field] is False))
  r.yes('exact pop token None and discarded return '+str(index),lambda:require(src['pop_key']=='token' and src['pop_default'] is None and src['pop_return_consumed'] is False))
  r.yes('original context fields preserved '+str(index),lambda:require(all(row[k]==v for k,v in old['contexts'][index].items())))
  r.yes('current catalogue validates against actual source '+str(index),lambda:c.validate_control_construction(launcher,entry,*deps,cat))
  for field,value in [('guard_expression','bool(control)'),('completed_control_object_established',True),('argument_expression','other_token')]:
   bad=D(cat);bad['source'][field]=value;r.no('independent source catalogue mutation '+str((index,field)),lambda bad=bad:c.validate_control_construction(launcher,entry,*deps,bad),'CONSTRUCTION-SOURCE-CORRESPONDENCE')
  bad=D(cat);bad['declarations'].pop();bad['source']['order'].pop();del bad['source']['stages']['removal-complete'];r.no('coordinated source declaration and order omission '+str(index),lambda bad=bad:c.validate_control_construction(launcher,entry,*deps,bad),'CONSTRUCTION-SOURCE-CORRESPONDENCE')
  if index==0:
   changed=entry.replace(b'control(_Control(token))',b'control(_Control(None))');assert changed!=entry
   r.no('changed governing expression cannot inherit source shape',lambda:c.validate_control_construction(launcher,changed,*deps,cat))
 r.save('independent-source-expectations.json',{'entry':identity(entry),'locations':{k:loc(v) for k,v in expected_nodes.items()},'construction_guards':guards(construction),'prefix':[ast.unparse(n) for n in prefix],'cleanup':loc(pop),'source_effects':'Conditional; no concrete constructor mechanism, existing cause, runtime identity or observed cleanup'})
 # Declared byte changes and all inherited function bodies are read-only comparisons.
 changes=json.loads((root/'provenance/changed-files.json').read_bytes());diff='';definitions={}
 for n,pins in changes['intentional_changes'].items():
  before=(root/'retained/control'/n).read_bytes();after=(root/n).read_bytes();assert identity(before)==pins['before'] and identity(after)==pins['after']
  diff+=''.join(difflib.unified_diff(before.decode().splitlines(True),after.decode().splitlines(True),fromfile='retained/control/'+n,tofile=n))
  if n.endswith('managed_coverage.py'):
   oldtree=ast.parse(before);newtree=ast.parse(after);oldf={x.name:x for x in oldtree.body if isinstance(x,ast.FunctionDef)};newf={x.name:x for x in newtree.body if isinstance(x,ast.FunctionDef)}
   assert len(oldf)==117 and len(newf)-len(oldf)==6
   for name,f in oldf.items():assert ast.get_source_segment(before.decode(),f)==ast.get_source_segment(after.decode(),newf[name]),name
   assert ast.dump(ast.Module(body=[x for x in oldtree.body if not isinstance(x,ast.FunctionDef)],type_ignores=[]))==ast.dump(ast.Module(body=[x for x in newtree.body if not isinstance(x,ast.FunctionDef)],type_ignores=[]))
   definitions={'inherited_unchanged':117,'new':sorted(set(newf)-set(oldf))}
 assert diff==(root/'provenance/implementation.diff').read_text()
 for n in ('prospective_entry.py','lab_bootstrap.py'):assert (root/'source-evidence'/n).read_bytes()==(root/'retained/control/source-evidence'/n).read_bytes()
 # Reconcile actual supplied logs without re-executing them.
 supplied={}
 def parse_printed(p):
  rows=[]
  for line in p.read_text().splitlines():
   a=line.split(' ',1)
   if len(a)==2 and a[0].isdigit():
    name,status=a[1].rsplit(' ',1);rows.append((int(a[0]),name,status))
  return rows
 for label,stem,n in [('primary-interrupted','failures/interrupted-processes/primary',285),('completion-interrupted','failures/interrupted-completion',71)]:
  p=root/stem;progress=[json.loads(s) for s in (p/'results/progress.jsonl').read_text().splitlines()];stdout=parse_printed(p/'processes/stdout.log');assert len(progress)==len(stdout)==n
  assert [(i+1,x['check'],x['result']) for i,x in enumerate(progress)]==stdout
  assert not (p/'results/RESULT.json').exists() and not (p/'processes/exit-status.json').exists()
  supplied[label]={'corroborated_rows':n,'complete_group':False,'result_and_exit':'UNRECOVERED'}
 for label in ('source-completion','public-final-completion'):
  result=json.loads((root/'results'/label/'RESULT.json').read_bytes());progress=[json.loads(s) for s in (root/'results'/label/'progress.jsonl').read_text().splitlines()];stdout=parse_printed(root/'processes'/label/'stdout.log');ex=json.loads((root/'processes'/label/'exit-status.json').read_bytes())
  assert result['checks']==1 and len(progress)==len(stdout)==1 and result['rows']==progress
  assert [(1,progress[0]['check'],progress[0]['result'])]==stdout and ex['returncode']==0 and ex['timed_out'] is False
  supplied[label]={'checks':1,'rows':progress,'exit':ex,'separate_completed_group':True}
 rej=json.loads((root/'results/public-final-completion/validator-rejection.json').read_bytes());supplied['final_rejection_layer']='Public post-derivation receipt comparison only';supplied['saved_public_rejection']=rej
 assert 'CONSTRUCTION-STALE-OR-ALTERED-RECEIPT' in json.dumps(rej)
 limits=receipt['new_control_construction_limits'];assert limits['inventory_unknown_totals']==4 and limits['lifetime_unknown_totals']==14 and limits['all_eleven_obligations_preserved'] is True and limits['actual_admission'] is False
 r.save('preservation-and-supplied.json',{'definitions':definitions,'declared_diff_exact':True,'runtime_sources_unchanged':True,'all_old_context_fields_unchanged':True,'supplied':supplied,'scope_limits':limits,'intermediate_cut_original_outer_identity_freshly_verified':False,'prior_qualified_accounting':json.loads((root/'retained/review/CHECKPOINT.json').read_bytes())['prior_accounting']})
except BaseException:
 error=traceback.format_exc();(r.path/'failure.txt').write_text(error);raise
finally:r.finish(error,scope='Independent source-derived checks and read-only supplied-record audit')
