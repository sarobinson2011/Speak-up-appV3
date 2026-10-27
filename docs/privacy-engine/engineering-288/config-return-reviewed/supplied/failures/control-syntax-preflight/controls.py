"""Focused new config controls; no completed suite or runtime entry invoked."""
import argparse,ast,copy,hashlib,json,os,sys,time,types
from pathlib import Path
def audit(event,args):
 if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system','os.fork','os.posix_spawn'):raise AssertionError('PROHIBITED:'+event)
 if event=='open' and isinstance(args[0],(str,bytes)) and os.fsdecode(args[0]).startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
 if event=='exec' and args[0].co_filename.rsplit('/',1)[-1] in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('APPLICATION-EXECUTION')
sys.addaudithook(audit)
_file_kind={}
def guard(frame,event,arg):
 if event!='call':return None
 filename=frame.f_code.co_filename;kind=_file_kind.get(filename)
 if kind is None:
  name=filename.rsplit('/',1)[-1];kind=1 if name in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py') else 2 if name=='prospective_entry.py' else 0;_file_kind[filename]=kind
 if kind==1 or kind==2 and frame.f_code.co_name in ('main','run','run_controlled','_run','_dispatch','__init__','state','handle','status'):raise AssertionError('APPLICATION-EXECUTION')
 return None
sys.settrace(guard)
def module(p):
 m=types.ModuleType('_config_controls');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--write',action='store_true');p.add_argument('--recovered',action='store_true');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 rows=[];cases=[];error=None;start=time.monotonic()
 def check(label,fn):
  value=fn();assert value is not False,label;row={'check':label,'result':'PASS'};rows.append(row)
  with (a.output/'progress.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
  print(str(len(rows))+' '+label,flush=True);return value
 def reject(fn,code=None):
  try:fn()
  except (ValueError,TypeError,KeyError) as e:
   if code is not None:assert str(e)==code,(str(e),code)
   return True
  raise AssertionError('Unexpected acceptance')
 try:
  m=module(a.root/'code/correspondence.py');data=m.inputs(a.root);cat=check('source-derived catalogue',lambda:m.catalogue(data));c=data['coverage'];d=data['prior_data']['prior_data'];g=d['guards']
  raw=d['manager'];tree=ast.parse(raw);cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority');methods={n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)}
  getter=methods['config'];ret=next(n for n in ast.walk(getter) if isinstance(n,ast.Return));stores=[n for n in ast.walk(cls) if isinstance(n,ast.Assign) and any(ast.unparse(t)=='self._config' for t in n.targets)]
  check('independent constructor/getter AST copy origins',lambda:len(stores)==1 and ast.unparse(stores[0].value)=='copy.deepcopy(config)' and ast.unparse(ret.value)=='copy.deepcopy(self._config)' and cat['source']['return']['expression']==ast.get_source_segment(raw.decode(),ret))
  at=ast.parse(d['authority']);exact=next(n for n in ast.walk(at) if isinstance(n,ast.Call) and ast.unparse(n.func)=='exact' and ast.unparse(n.args[0])=='config');fields=ast.literal_eval(exact.args[1])
  check('expected field coverage from defining Authority source',lambda:set(fields)==set(cat['declaration']['fields'])==set(cat['declaration']['inherited_config']['native_template']['type']['object']))
  claims=check('pristine semantic',lambda:m.semantic(data,cat));bundle=check('pristine derivation',lambda:m.derive_config(data,cat));saved=m.enc(bundle);receipt=a.root/'results/config-correspondence.json'
  if a.write:
   with receipt.open('xb') as f:f.write(saved)
  else:assert receipt.read_bytes()==saved
  check('pristine mandatory public validator',lambda:m.validate(a.root,saved))
  prior=json.loads((a.root/'retained/binding/results/binding-correspondence.json').read_bytes())
  for i,row in enumerate(claims):
   name=row['context'];anchor=row['validated_configuration_anchor'];value=copy.deepcopy(anchor['configuration']);now=bundle['contexts'][i];old=prior['contexts'][i]
   check('prior context unchanged '+name,lambda now=now,old=old:all(m.enc(now[k])==m.enc(v) for k,v in old.items()))
   check('unobserved getter remains distinct '+name,lambda row=row,anchor=anchor:row['getter_observations'] is None and row['actual_getter_count'] is None and anchor['getter_frame'] is None and anchor['copy_identity_observations'] is None)
   premise={'phase':'READY','live_present':True,'retired_absent':True,'lock_enter_completed':True,'copy_completed':True,'lock_exit_completed':True}
   case={'kind':'CONSTRUCTED-CONDITIONAL-CONFIG','context':name,'anchor':copy.deepcopy(anchor),'premise':premise,'constructor_input_at_copy':copy.deepcopy(value),'stored':copy.deepcopy(value),'returned':copy.deepcopy(value)}
   result=check('instance-qualified constructed copy chain '+name,lambda case=case:m.constructed_projection(data,cat,case));cases.append(result)
   # Legitimate type/value variants are conditional producer algebra only,
   # never replacement configurations for the retained instance.
   variants=[copy.deepcopy(value),dict(value,start_nonce=value['start_nonce']+1),dict(value,pilot='another-pilot',session='another-session')]
   for j,v in enumerate(variants):check('typed conditional variant '+str(j)+' '+name,lambda v=v:c.config_value_projection(cat,premise,v,copy.deepcopy(v)))
   for field in fields:
    bad=copy.deepcopy(value);bad.pop(field)
    check('missing field '+field+' '+name,lambda bad=bad:reject(lambda:c.config_value_projection(cat,premise,value,bad)))
    bad=copy.deepcopy(value);bad[field]=True if type(value[field]) is int else 17
    check('wrong type '+field+' '+name,lambda bad=bad:reject(lambda:c.config_value_projection(cat,premise,value,bad)))
    if not a.recovered:
     bad=copy.deepcopy(value);bad[field]=value[field]+1 if type(value[field]) is int else value[field]+'x'
     check('altered value '+field+' '+name,lambda bad=bad:reject(lambda:c.config_value_projection(cat,premise,value,bad)))
   for k in premise:
    bad=dict(premise);bad[k]='CLOSED' if k=='phase' else False
    check('normal continuation '+k+' '+name,lambda bad=bad:reject(lambda:c.config_value_projection(cat,bad,value,copy.deepcopy(value))))
   check('returned manager dict alias rejects '+name,lambda:reject(lambda:c.config_value_projection(cat,premise,value,value),'COPY-MUTABLE-SHARING'))
   bad=copy.deepcopy(claims);bad[i]['validated_configuration_anchor']['instance']['managed_constructor_frame']+=1
   check('semantic wrong instance '+name,lambda bad=bad:reject(lambda:m.semantic(data,cat,bad),'CONFIG-ANCHOR-LINEAGE'))
   bad=copy.deepcopy(claims);bad[i]['validated_configuration_anchor']['configuration']['session']='stale-session'
   check('derivation wrong configuration '+name,lambda bad=bad:reject(lambda:m.derive_config(data,cat,bad),'CONFIG-ANCHOR-VALUE'))
   bad=copy.deepcopy(bundle);bad['contexts'][i].pop('config_return_correspondence')
   check('mandatory public rejection of omitted extension '+name,lambda bad=bad:reject(lambda:m.validate(a.root,m.enc(bad))))
   if not a.recovered:
    bad=copy.deepcopy(case);bad['anchor']['record']['acquisition']='mixed-acquisition'
    check('constructed mixed anchor '+name,lambda bad=bad:reject(lambda:m.constructed_projection(data,cat,bad),'CONFIG-CASE-ANCHOR'))
  # Direct deepcopy controls include aliases, cycles and post-copy mutation.
  shared=[{'x':1}];source={'left':shared,'right':shared,'scalar':'same'};stored=copy.deepcopy(source);returned=copy.deepcopy(stored)
  for label,x,y in [('constructor',source,stored),('getter',stored,returned)]:
   check('nested '+label+' isolation preserves internal aliases',lambda x=x,y=y:c.validate_copy_graph(c.copy_graph(x,y)))
   check('nested shallow '+label+' substitution rejects',lambda x=x:reject(lambda:c.validate_copy_graph(c.copy_graph(x,copy.copy(x))),'COPY-MUTABLE-SHARING'))
  split={'left':copy.deepcopy(shared),'right':copy.deepcopy(shared),'scalar':'same'}
  check('alias splitting rejects',lambda:reject(lambda:c.validate_copy_graph(c.copy_graph(source,split)),'COPY-ALIAS-SPLIT'))
  distinct={'left':[1],'right':[1]};merged=[];merged.append(1)
  check('alias merging rejects',lambda:reject(lambda:c.validate_copy_graph(c.copy_graph(distinct,{'left':merged,'right':merged})),'COPY-ALIAS-MERGE'))
  cyc=[];cyc.append(cyc);check('cyclic deepcopy relation',lambda:c.validate_copy_graph(c.copy_graph(cyc,copy.deepcopy(cyc))))
  for scalar in (None,True,17,-0.0,'same'):
   check('immutable sharing permitted '+repr(scalar),lambda scalar=scalar:c.validate_copy_graph(c.copy_graph(scalar,scalar)))
  check('wrong scalar type even bool/int rejects',lambda:reject(lambda:c.validate_copy_graph(c.copy_graph([1],[True]))))
  check('wrong container type rejects',lambda:reject(lambda:c.validate_copy_graph(c.copy_graph([],{})))))
  graph=c.copy_graph(stored,returned);source['left'][0]['x']=91
  check('constructor input mutation does not change stored nested value',lambda:stored['left'][0]['x']==1 and stored['left'] is stored['right'] and c.validate_copy_graph(graph))
  returned['right'][0]['x']=52
  check('nested result mutation preserves storage; internal returned aliases remain',lambda:stored['left'][0]['x']==1 and returned['left'][0]['x']==52)
  check('later input need not equal storage',lambda:reject(lambda:c.validate_copy_graph(c.copy_graph(source,stored))))
  graph=c.copy_graph({'a':[]}, {'a':[]});graph['nodes']['unused']={'kind':'list','items':[]}
  check('undeclared unreachable graph node rejects',lambda:reject(lambda:c.validate_copy_graph(graph),'COPY-UNREACHABLE-NODE'))
  check('tuple/custom domain unsupported without stronger claim',lambda:reject(lambda:c.copy_graph((1,))))
  # Expected coverage is re-derived from retained sources, not this catalogue.
  def validate_cat(bad):
   return c.validate_config_return(d['manager'],d['authority'],d['values']['candidate/managed-route/model.json'],d['values']['candidate/managed-route/producers.json'],g['guard_relationships'],g['guard_oracle'],d['reference_module'].reference_catalogue(d),bad)
  mutations=[('omitted field',lambda x:x['declaration']['fields'].pop('session')),('shallow getter origin',lambda x:x['source']['copy_call'].update(expression='copy.copy(self._config)')),('constructor alias assignment',lambda x:x['source']['constructor_storage'].update(expression='self._config=config')),('wrong return origin',lambda x:x['declaration']['origin'].update(expression='self._live.config')),('omitted guard',lambda x:x['source']['return'].update(guards=[])),('invented immutable isolation',lambda x:x['copy_relation'].update(immutable_identity='all leaves freshly allocated'))]
  for label,fn in mutations:
   bad=copy.deepcopy(cat);fn(bad);check('independent source oracle '+label,lambda bad=bad:reject(lambda:validate_cat(bad)))
  bad=copy.deepcopy(cat);bad['source']['copy_call']['expression']='copy.copy(self._config)';bad['declaration']['origin']['expression']='copy.copy(self._config)'
  check('semantic rejects coordinated source substitution',lambda:reject(lambda:m.semantic(data,bad),'CONFIG-SOURCE-CATALOGUE'))
  evidence=d['ctx']['e'];old=claims[0]['validated_configuration_anchor']['configuration']['session'];new=old+'-substituted';altered={};changes=[]
  for n,b in evidence.items():
   changed=b.replace(old.encode(),new.encode());altered[n]=changed
   if changed!=b:changes.append({'path':n,'before':identity(b),'after':identity(changed)})
  (a.output/'coordinated-substitution.json').write_bytes(m.enc(changes))
  check('semantic rejects coordinated report configurations',lambda:reject(lambda:m.semantic(data,cat,evidence=altered),'CONFIG-VALIDATED-INSTANCE-VALUE'))
  check('derivation rejects coordinated report configurations',lambda:reject(lambda:m.derive_config(data,cat,evidence=altered),'CONFIG-VALIDATED-INSTANCE-VALUE'))
  baseline=dict(data);baseline['prior_data']=dict(data['prior_data']);baseline['prior_data']['prior_data']=dict(d);baseline['prior_data']['prior_data']['ctx']=dict(d['ctx']);baseline['prior_data']['prior_data']['ctx']['e']=altered
  check('candidate baseline cannot replace validated expectation',lambda:reject(lambda:m.semantic(baseline,cat),'CONFIG-VALIDATED-INSTANCE-VALUE'))
  if not a.recovered:
   for label,fn in [('missing',lambda x:x.pop('config')),('bool nonce',lambda x:x['config'].update(start_nonce=True)),('stale head binding',lambda x:x.update(head=m.enc(dict(json.loads(bytes.fromhex(x['head'])),binding='f'*64)).hex()))]:
    bad=dict(evidence);record=json.loads(bad['evidence/recovery-export-0.json']);fn(record);bad['evidence/recovery-export-0.json']=m.enc(record)
    check('semantic export '+label,lambda bad=bad:reject(lambda:m.semantic(data,cat,evidence=bad)))
   bad=copy.deepcopy(claims);bad[0]['validated_configuration_anchor']['recovery_occurrence']='stale';check('stale frontier rejects',lambda:reject(lambda:m.derive_config(data,cat,bad),'CONFIG-ANCHOR-LINEAGE'))
  # Returned expectation trees must never become authority for future checks.
  pristine=m.enc(claims);other=m.enc(claims[1]);claims[0]['declaration']['copy_relation']['phases'].clear();claims[0]['validated_configuration_anchor']['configuration']['pilot']='changed'
  check('nested returned contexts isolated',lambda:m.enc(claims[1])==other)
  check('mutated semantic result rejects',lambda:reject(lambda:m.semantic(data,cat,claims)))
  check('fresh semantic expectations unchanged',lambda:m.enc(m.semantic(data,cat))==pristine)
  bundle['contexts'].clear();check('cleared result cannot alter public expectations',lambda:reject(lambda:m.validate(a.root,m.enc(bundle))))
  check('pristine receipt survives output mutations',lambda:m.validate(a.root,saved))
  check('both contexts required',lambda:reject(lambda:m.semantic(data,cat,[]),'CONFIG-CONTEXT-DOMAIN'))
  (a.output/'constructed-copy-graph.json').write_bytes(m.enc({'initial_relation_before_mutations':graph,'cases':cases}))
 except BaseException as e:error=repr(e);raise
 finally:
  result={'result':'PASS' if error is None else 'FAIL','checks':len(rows),'rows':rows,'error':error,'seconds':time.monotonic()-start,'mode':'recovered' if a.recovered else 'primary','source':{n:identity((a.root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')},'runtime_getter_observations':None,'database_connections':0,'session_operations':0,'host_execution':False,'completed_suites_rerun':False}
  (a.output/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('result','checks','seconds','error')}),flush=True)
if __name__=='__main__':main()
