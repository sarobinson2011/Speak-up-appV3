"""New binding correspondence controls only; prior suites are not executed."""
import argparse,ast,copy,hashlib,json,os,sys,time,types
from pathlib import Path
def audit(event,args):
 if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo'):raise AssertionError('PROHIBITED:'+event)
 if event=='open' and isinstance(args[0],(str,bytes)) and os.fsdecode(args[0]).startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
sys.addaudithook(audit)
def profile(frame,event,arg):
 name=frame.f_code.co_filename.rsplit('/',1)[-1]
 if event=='call' and (name in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py') or name=='prospective_entry.py' and frame.f_code.co_name in ('main','run','run_controlled','_run','_dispatch','__init__','state','handle','status')):raise AssertionError('APPLICATION-EXECUTION')
sys.setprofile(profile)
def module(p):
 m=types.ModuleType('_binding_controls');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--write',action='store_true');p.add_argument('--recovered',action='store_true');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 rows=[];error=None;cases=[];start=time.monotonic()
 def check(label,fn):
  v=fn();assert v is not False,label;rows.append({'check':label,'result':'PASS'})
  with (a.output/'progress.jsonl').open('a') as f:f.write(json.dumps(rows[-1])+'\n')
  return v
 def reject(fn,reason=None):
  try:fn()
  except (ValueError,TypeError,KeyError) as e:
   if reason is not None:assert str(e)==reason,(str(e),reason)
   return True
  raise AssertionError('Unexpected acceptance')
 def replace_binding(e,new):
  # Coordinated JSON representation substitutions across every retained record
  # that carries the old value, including embedded hex HEAD bytes.
  old=json.loads(bytes.fromhex(json.loads(e['evidence/recovery-export-0.json'])['head']))['binding'];out=dict(e);changes=[]
  for name,b in e.items():
   if not name.endswith('.json'):continue
   value=json.loads(b)
   def walk(v):
    if isinstance(v,str):
     if v==old:return new
     try:
      decoded=bytes.fromhex(v);j=json.loads(decoded)
     except (ValueError,TypeError,UnicodeDecodeError):return v
     changed=walk(j)
     if changed!=j:return json.dumps(changed,sort_keys=True,separators=(',',':')).encode().hex()
     return v
    if isinstance(v,list):return [walk(x) for x in v]
    if isinstance(v,dict):return {k:walk(x) for k,x in v.items()}
    return v
   changed=walk(value)
   if changed!=value:out[name]=(json.dumps(changed,sort_keys=True,separators=(',',':'))+'\n').encode();changes.append({'path':name,'before':identity(b),'after':identity(out[name])})
  return out,changes
 try:
  m=module(a.root/'code/correspondence.py');data=m.inputs(a.root);cat=check('source-derived binding catalogue',lambda:m.catalogue(data))
  # Independently read the defining AST, not a generated expected-field list.
  tree=ast.parse(data['prior_data']['manager']);cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority');getter=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='binding');ret=next(n for n in ast.walk(getter) if isinstance(n,ast.Return))
  check('independent AST return selector and receiver',lambda:cat['source']['field']==ret.value.attr and cat['source']['slot']==ret.value.value.attr and cat['source']['return']['expression']==ast.get_source_segment(data['prior_data']['manager'].decode(),ret))
  claims=check('pristine semantic correspondence',lambda:m.semantic(data,cat));bundle=check('pristine derivation',lambda:m.derive_binding(data,cat));saved=m.enc(bundle)
  receipt=a.root/'results/binding-correspondence.json'
  if a.write:
   with receipt.open('xb') as f:f.write(saved)
  else:assert receipt.read_bytes()==saved
  check('pristine public validation',lambda:m.validate(a.root,saved))
  prior=json.loads((a.root/'retained/hf01/results/hf01-correspondence.json').read_bytes())
  for i,row in enumerate(claims):
   name=row['context'];anchor=row['validated_binding_anchor'];old=prior['contexts'][i];now=bundle['contexts'][i]
   check('prior context members unchanged '+name,lambda old=old,now=now:all(m.enc(now[k])==m.enc(v) for k,v in old.items()))
   check('instance/acquisition/frontier joins '+name,lambda anchor=anchor,old=old:anchor['instance']==old['hf01_evidence_binding']['instance'] and anchor['recovery_occurrence']==old['saved_recovery_fields'][0]['occurrence'] and anchor['record']==old['hf01_evidence_binding']['head_record'])
   check('no getter frame, object identity or execution invented '+name,lambda row=row,anchor=anchor:row['getter_observations'] is None and anchor['getter_frame'] is None and anchor['object_identity'] is None and anchor['underlying_connection_identity'] is None)
   ref={'scope':m.reference_scope(anchor),'symbol':'rho-live'}
   case={'kind':'CONSTRUCTED-CONDITIONAL-GETTER','context':name,'anchor':copy.deepcopy(anchor),'premise':{'phase':cat['source']['ready_phase'],'live_reference':copy.deepcopy(ref),'retired_reference':None,'underlying':{'reference':copy.deepcopy(ref),'binding':anchor['binding_value']},'lock_enter_completed':True,'attribute_completed':True,'lock_exit_completed':True},'returned':anchor['binding_value']}
   check('legitimate constructed forwarding '+name,lambda case=case:m.constructed_projection(data,cat,case));cases.append(copy.deepcopy(case))
   other=copy.deepcopy(case);other['premise']['live_reference']['symbol']='rho-distinct';other['premise']['underlying']['reference']['symbol']='rho-distinct'
   check('equal binding permits a distinct constructed symbol without identity collapse '+name,lambda other=other:m.constructed_projection(data,cat,other)['projection']['reference_symbol']['symbol']=='rho-distinct')
   bad=copy.deepcopy(case);bad['premise']['underlying']['reference']['symbol']='different-receiver'
   check('equal strings cannot substitute a different reference '+name,lambda bad=bad:reject(lambda:m.constructed_projection(data,cat,bad),'BINDING-RECEIVER-REFERENCE'))
   bad=copy.deepcopy(case);bad['premise']['live_reference']['scope']['recorded_instance']['managed_constructor_frame']+=1;bad['premise']['underlying']['reference']=copy.deepcopy(bad['premise']['live_reference'])
   check('coordinated wrong-instance symbols reject '+name,lambda bad=bad:reject(lambda:m.constructed_projection(data,cat,bad),'BINDING-CASE-REFERENCE-SCOPE'))
   bad=copy.deepcopy(case);bad['returned']=17
   check('wrong constructed return type '+name,lambda bad=bad:reject(lambda:m.constructed_projection(data,cat,bad),'BINDING-VALUE-TYPE'))
   bad=copy.deepcopy(case);bad['returned']='f'*64
   check('wrong constructed value '+name,lambda bad=bad:reject(lambda:m.constructed_projection(data,cat,bad),'BINDING-VALUE-ORIGIN'))
   bad=copy.deepcopy(case);del bad['returned']
   check('omitted constructed return '+name,lambda bad=bad:reject(lambda:m.constructed_projection(data,cat,bad),'BINDING-CASE-FIELDS'))
   if not a.recovered:
    for key,value in [('phase','CLOSED'),('live_reference',None),('retired_reference',copy.deepcopy(ref)),('lock_enter_completed',False),('attribute_completed',False),('lock_exit_completed',False)]:
     bad=copy.deepcopy(case);bad['premise'][key]=value
     check('normal guard '+key+' '+name,lambda bad=bad:reject(lambda:m.constructed_projection(data,cat,bad)))
    bad=copy.deepcopy(case);bad['kind']='OBSERVED-GETTER'
    check('constructed case cannot become execution evidence '+name,lambda bad=bad:reject(lambda:m.constructed_projection(data,cat,bad)))
   # Candidate correspondence mutations go through both semantic and derive.
   mutations=[('omitted value',lambda a:a.pop('binding_value')),('wrong type',lambda a:a.update(binding_value=False)),('wrong binding',lambda a:a.update(binding_value='f'*64)),('wrong instance',lambda a:a['instance'].update(managed_constructor_frame=99)),('stale frontier',lambda a:a.update(recovery_occurrence='stale')),('mixed acquisition',lambda a:a['record'].update(acquisition='other')),('invented frame',lambda a:a.update(getter_frame=99))]
   if a.recovered:mutations=[mutations[x] for x in (0,2,3,5)]
   for label,mutate in mutations:
    bad=copy.deepcopy(claims);mutate(bad[i]['validated_binding_anchor'])
    check('semantic rejects '+label+' '+name,lambda bad=bad:reject(lambda:m.semantic(data,cat,bad)))
    if not a.recovered or label=='wrong binding':check('derivation rejects '+label+' '+name,lambda bad=bad:reject(lambda:m.derive_binding(data,cat,bad)))
   bad=copy.deepcopy(bundle);bad['contexts'][i]['binding_return_correspondence']['validated_binding_anchor']['binding_value']='f'*64
   check('public rejects altered binding '+name,lambda bad=bad:reject(lambda:m.validate(a.root,m.enc(bad))))
   bad=copy.deepcopy(bundle);bad['contexts'][i]['binding_return_correspondence']['validated_binding_anchor']['instance']['binding']='f'*64;bad['contexts'][i]['binding_return_correspondence']['validated_binding_anchor']['binding_value']='f'*64
   check('public rejects coordinated instance/value '+name,lambda bad=bad:reject(lambda:m.validate(a.root,m.enc(bad))))
  # Independent coverage oracle is re-derived from the defining source.
  cat_mutations=[('omit return',lambda c:c['source'].pop('return')),('wrong type',lambda c:c['declaration'].update(type='int')),('wrong origin',lambda c:c['declaration']['origin'].update(expression='self._retired.binding')),('omit readiness',lambda c:c['source']['readiness_call'].update(expression='pass')),('wrong ready phase',lambda c:c['source'].update(ready_phase='CLOSED')),('omit live link',lambda c:c['reference_links'].pop('live_read')),('omit lock guard',lambda c:c['source']['return'].update(guards=[])),('changed writer',lambda c:c['source']['underlying_writer'].update(expression="self.binding='f'*64"))]
  if a.recovered:cat_mutations=cat_mutations[:2]
  for label,mutate in cat_mutations:
   bad=copy.deepcopy(cat);mutate(bad)
   check('source oracle rejects '+label,lambda bad=bad:reject(lambda:m.semantic(data,bad), 'BINDING-SOURCE-CATALOGUE'))
  bad=copy.deepcopy(cat);bad['source']['value']['expression']='self._retired.binding';bad['declaration']['origin']['expression']='self._retired.binding';bad['source']['slot']='_retired';bad['reference_links']['live_read']['slot']='_retired'
  check('coordinated catalogue/origin/reference substitution rejects',lambda:reject(lambda:m.derive_binding(data,bad),'BINDING-SOURCE-CATALOGUE'))
  evidence=data['prior_data']['ctx']['e'];altered,changes=replace_binding(evidence,'f'*64)
  (a.output/'coordinated-binding-substitution.json').write_bytes(m.enc(changes))
  for label,fn in [('semantic',m.semantic),('derivation',m.derive_binding)]:check(label+' rejects coordinated saved report substitution',lambda fn=fn:reject(lambda:fn(data,cat,evidence=altered),'BINDING-VALIDATED-INSTANCE-VALUE'))
  d=dict(data);d['prior_data']=dict(data['prior_data']);d['prior_data']['ctx']=dict(data['prior_data']['ctx']);d['prior_data']['ctx']['e']=altered
  check('candidate baseline plus reports cannot replace expectation',lambda:reject(lambda:m.semantic(d,cat),'BINDING-VALIDATED-INSTANCE-VALUE'))
  if not a.recovered:
   for label,fn in [('omitted',lambda s:s.pop('binding')),('wrong type',lambda s:s.update(binding=17)),('stale head',lambda s:s.update(head='f'*64))]:
    bad=dict(evidence);x=json.loads(bad['evidence/recovery-export-0.json']);state=json.loads(bytes.fromhex(x['head']));fn(state);x['head']=m.enc(state).hex();bad['evidence/recovery-export-0.json']=m.enc(x)
    check('evidence rejects '+label,lambda bad=bad:reject(lambda:m.semantic(data,cat,evidence=bad)))
   bad=dict(evidence);bad.pop('evidence/client-handoff.json');check('missing saved binding evidence rejects',lambda:reject(lambda:m.semantic(data,cat,evidence=bad),'BINDING-EVIDENCE-MEMBERSHIP'))
  # Returned mutable trees are never reused as expectations; contexts are also
  # separate trees. A nested mutation must not affect another output context.
  pristine=m.enc(claims);mut=m.semantic(data,cat);second=m.enc(mut[1]);mut[0]['declaration']['source']['ready_phase']='CLOSED';mut[0]['validated_binding_anchor']['instance']['binding']='changed'
  check('context outputs have no shared nested aliases',lambda:m.enc(mut[1])==second)
  check('nested semantic result cannot alter acceptance',lambda:reject(lambda:m.semantic(data,cat,mut)))
  check('fresh pristine semantic remains unchanged',lambda:m.enc(m.semantic(data,cat))==pristine)
  bundle['contexts'].clear();check('cleared derived contexts rejected',lambda:reject(lambda:m.validate(a.root,m.enc(bundle))))
  check('pristine public receipt survives returned-result mutation',lambda:m.validate(a.root,saved))
  check('both source contexts remain required',lambda:reject(lambda:m.semantic(data,cat,claims[:1]),'BINDING-CONTEXT-DOMAIN'))
  # source-owned catalogue object mutations cannot change the next catalogue.
  original=m.enc(cat);cat['declaration']['inherited_binding']['native_template']['type']='INTEGER'
  check('mutated catalogue does not change fresh expectations',lambda:m.enc(m.catalogue(data))==original)
  check('pristine final derivation byte-identical',lambda:m.enc(m.derive(a.root))==saved)
 except BaseException as e:error=repr(e);raise
 finally:
  result={'result':'PASS' if error is None else 'FAIL','checks':len(rows),'rows':rows,'error':error,'seconds':time.monotonic()-start,'mode':'recovered' if a.recovered else 'primary','source':{n:identity((a.root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')},'constructed_cases':len(cases),'constructed_cases_are_runtime_evidence':False,'database_connections':0,'session_operations':0,'host_execution':False,'completed_suites_rerun':False}
  (a.output/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(a.output/'constructed-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
  print(json.dumps({k:result[k] for k in ('result','checks','seconds','error')}),flush=True)
if __name__=='__main__':main()
