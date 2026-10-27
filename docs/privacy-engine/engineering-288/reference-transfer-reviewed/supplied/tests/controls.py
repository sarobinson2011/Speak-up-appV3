"""Focused reference-transfer extension controls; no prior suite or runtime run."""
import argparse,ast,copy,hashlib,json,os,sys,types
from pathlib import Path

def audit(event,args):
 if event in ('sqlite3.connect','socket.connect','socket.bind'):raise AssertionError('PROHIBITED:'+event)
 if event=='open' and isinstance(args[0],(str,bytes)) and os.fsdecode(args[0]).startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
sys.addaudithook(audit)
def profile(frame,event,arg):
 if event=='call' and frame.f_code.co_filename.rsplit('/',1)[-1] in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('APPLICATION-EXECUTION')
sys.setprofile(profile)
def module(p):
 m=types.ModuleType('_reference_controls');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--write',action='store_true');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 rows=[];paths={};error=None;original={n:identity((a.root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 def check(label,f):
  v=f();assert v is not False,label;rows.append({'check':label,'result':'PASS'});return v
 def reject(f):
  try:f()
  except (ValueError,TypeError,KeyError) as e:return str(e)
  raise AssertionError('Unexpected acceptance')
 try:
  m=module(a.root/'code/correspondence.py');data=m.reference_inputs(a.root);cat=m.reference_catalogue(data);source=cat['source'];mc=data['reference_coverage'];g=data['guards'];raw=data['manager']
  check('legitimate reference catalogue',lambda:m.check_reference_catalogue(data,cat))
  bundle=m.derive_reference(data,cat);saved=m.enc(bundle)
  if a.write:
   with (a.root/'results/reference-correspondence.json').open('xb') as f:f.write(saved)
  else:assert saved==(a.root/'results/reference-correspondence.json').read_bytes()
  check('legitimate public saved receipt',lambda:m.validate(a.root,saved))
  # A separate direct AST walk computes targets and RHS coverage; never derive
  # this set from declaration origin lists or catalogue-provided counts.
  tree=ast.parse(raw);cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority');methods={n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)}
  def attr(n):return n.attr if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id=='self' else None
  def key(n):return ':'.join(str(v) for v in (n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__))
  expected=[]
  for fn in methods.values():
   for n in ast.walk(fn):
    if isinstance(n,ast.Assign):
     for t in n.targets:
      if attr(t) in ('_live','_retired'):expected.append((key(n),fn.name,attr(t),ast.unparse(n.value)))
  check('independent direct source assignment domain',lambda:sorted(expected)==sorted((r['site'],r['function'],r['target'],ast.unparse(ast.parse(r['value']['expression']['expression'],mode='eval').body)) for r in source['writes']))
  check('existing two opaque reference declarations reused',lambda:[d['declaration']['id'] for d in cat['declarations']]==['managed-local:live','managed-local:retired'])
  def mutation(label,edit):
   c=copy.deepcopy(cat);edit(c);check(label,lambda:reject(lambda:m.check_reference_catalogue(data,c)))
  for i,r in enumerate(source['writes']):
   mutation('omit assignment '+r['site'],lambda c,i=i:c['source']['writes'].pop(i))
   mutation('alter target '+r['site'],lambda c,i=i:c['source']['writes'][i].update(target='_invented'))
   mutation('omit guard '+r['site'],lambda c,i=i:c['source']['writes'][i].update(guards=[]))
   mutation('omit continuation '+r['site'],lambda c,i=i:c['source']['writes'][i].update(continuation=[]))
   mutation('stale reference origin '+r['site'],lambda c,i=i:c['source']['writes'][i]['value'].update(kind='equal-recorded-value'))
  for i,r in enumerate(source['calls']):
   mutation('omit reference call '+r['site'],lambda c,i=i:c['source']['calls'].pop(i))
   mutation('alter call order/guard '+r['site'],lambda c,i=i:c['source']['calls'][i].update(continuation=[]))
  for i,r in enumerate(source['programs']):mutation('alter control programme '+r['function'],lambda c,i=i:c['source']['programs'][i].update(ast='invented'))
  mutation('reverse transfers',lambda c:c['source']['writes'].reverse())
  mutation('coordinate deletion of retired declarations and origins',lambda c:(c['declarations'].pop(),c['source'].update(writes=[r for r in c['source']['writes'] if r['target']!='_retired'])))
  mutation('invent physical connection identity',lambda c:c['connection_relation'].update(actual_object_and_connection_identity='ESTABLISHED'))
  mutation('omit allocation identity qualification',lambda c:c['source']['local_producers'][0].update(identity='one global object'))
  mutation('stale authority binding',lambda c:c['connection_relation']['source'].update(sha256='0'*64))
  mutation('static source becomes repetition completeness',lambda c:c.update(complete_symbolic_coverage=True))
  mutation('finite multiplicity invented',lambda c:c['declarations'][0].update(multiplicity=1))
  fake=types.SimpleNamespace(key=g['guard_relationships'].key)
  def altered(raw):
   values,bad=g['guard_relationships'].derive(raw);values[source['writes'][-1]['site']]=[];return values,bad
  fake.derive=altered
  check('independent guard oracle rejects coordinated generator omission',lambda:reject(lambda:mc.reference_source(raw,fake,g['guard_oracle'])))
  d=dict(data);d['values']=copy.deepcopy(data['values']);sites=d['values']['candidate/managed-route/producers.json']['source_inventory']['sites'];sites[:]=[r for r in sites if r['site']!=source['writes'][0]['site']]
  check('missing inherited site cannot narrow required coverage',lambda:reject(lambda:m.reference_catalogue(d)))
  d=dict(data);d['manager']=raw.replace(b'self._retired=self._live',b'self._retired=None')
  check('changed defining source rejected',lambda:reject(lambda:m.reference_catalogue(d)))
  d=dict(data);d['values']=copy.deepcopy(data['values']);next(dcl for dcl in d['values']['candidate/managed-route/model.json']['local_declarations'] if dcl['id']=='managed-local:live')['type']='serialized binding dictionary'
  check('reference and representation type conflation rejected',lambda:reject(lambda:m.reference_catalogue(d)))
  # Source-owned addresses for constructed route choices; no actual callbacks.
  def find(fn,typ,text):return next(n for n in ast.walk(methods[fn]) if isinstance(n,typ) and ast.unparse(n)==text)
  def addr(frame,node,suffix=None):return str(frame)+'/'+key(node)+('/'+suffix if suffix else '')
  def case(method,live=None,retired=None,phase='CLOSED',ctx='SYMBOLIC-U-ONE'):
   return {'kind':'CONSTRUCTED-REFERENCE-PATH','context':ctx,'scope':{'acquisition':'constructed-only','instance':'constructed-instance','invocation':'constructed-call'},'method':method,'initial':{'_live':live,'_retired':retired,'_phase':phase},'facts':{},'outcomes':{},'stop_after':None}
  def token(c,origin):return {'kind':'constructed-reference','scope':{'context':c['context'],**c['scope']},'origin':origin}
  def files(c):
   for text in ('self._path.is_file()','self._owners.is_file()'):c['facts'][addr(1,find('recover',ast.Call,text))]={'value':True,'subject':None}
   return c
  alloc=find('recover',ast.Call,'self._runtime.Authority.__new__(self._runtime.Authority)')
  constructor=next(n for n in ast.walk(methods['recover']) if isinstance(n,ast.Call) and ast.unparse(n.func)=='self._runtime.Authority.__init__')
  validate=find('recover',ast.Call,'self._validate(a)');close=find('_dispose',ast.Call,'self._retired.close()');hasdb=find('recover',ast.Call,"hasattr(a, 'db')")
  def allocation_token(c):return token(c,'call-result:1:'+key(alloc))
  def db_fact(c,value):c['facts'][addr(1,hasdb)]={'value':value,'subject':allocation_token(c)};return c
  def run(label,c,expect):
   out=check(label,lambda:m.reference_path(data,c));expect(out);check(label+' receipt',lambda:m.reference_path(data,c,out));paths[label]=out;return out
  def final(phase,live_origin=None,retired_origin=None,completion='normal'):
   def verify(o):
    assert o['completion']==completion and o['final']['_phase']==phase
    for slot,origin in (('_live',live_origin),('_retired',retired_origin)):
     assert o['final'][slot] is None if origin is None else o['final'][slot]['origin']==origin
    assert not o['actual_observation'] and not o['physical_close_established'] and not o['outstanding_obligations_discharged']
   return verify
  c=case('__init__');cond=next(n.test for n in methods['__init__'].body if isinstance(n,ast.If));c['facts'][addr(1,cond)]={'value':False,'subject':None};run('constructed initialization',c,final('CLOSED'))
  c=case('_quarantine','L',None,'READY');run('constructed quarantine transfer',c,final('QUARANTINED',None,'initial:L'))
  c=case('_quarantine',None,'R','CLEANUP_UNCERTAIN');run('constructed no-live retains retired',c,final('QUARANTINED',None,'initial:R'))
  c=case('_quarantine','L',None,'READY');transfer=find('_quarantine',ast.Assign,'self._retired = self._live');c['stop_after']=addr(1,transfer)
  alias=run('constructed interruption preserves temporary alias',c,final('QUARANTINED','initial:L','initial:L','partial-prefix'))
  check('partial prefix has no invented close',lambda:not any(e.get('kind')=='call:self._retired.close' for e in alias['events']))
  c=case('_dispose',None,'R','QUARANTINED');run('constructed normal disposal',c,final('CLOSED'))
  c=case('_dispose',None,'R','QUARANTINED');c['outcomes'][addr(1,close,'call:self._retired.close')]='raise';run('constructed failed disposal retains reference',c,final('CLEANUP_UNCERTAIN',None,'initial:R','abrupt'))
  c=case('_dispose',None,'R','QUARANTINED');c['outcomes'][addr(1,close,'call:self._retired.close')]='stop';run('constructed interrupted close retains reference',c,final('CLEANUP_UNCERTAIN',None,'initial:R','partial-prefix'))
  c=case('_dispose',None,None,'QUARANTINED');run('constructed no-retired early return is not closure',c,final('QUARANTINED'))
  c=files(case('recover'));run('constructed normal recovery publication',c,final('READY','call-result:1:'+key(alloc)))
  c=files(case('recover','L','L','QUARANTINED'));run('constructed recovery from interrupted alias',c,final('READY','call-result:1:'+key(alloc)))
  c=case('recover',None,'R','CLEANUP_UNCERTAIN');c['outcomes'][addr(2,close,'call:self._retired.close')]='raise';o=run('constructed old cleanup failure prevents allocation',c,final('CLEANUP_UNCERTAIN',None,'initial:R','abrupt'))
  check('failed old cleanup has no new local result',lambda:not any(e['event']=='local-reference' for e in o['events']))
  c=case('recover','L',None,'READY');run('constructed READY rejection',c,final('READY','initial:L',None,'abrupt'))
  for node,phase in ((constructor,'OPEN_FAILED'),(validate,'VALIDATION_FAILED')):
   for has_db in (False,True):
    c=db_fact(files(case('recover')),has_db);c['outcomes'][addr(1,node,'call:'+ast.unparse(node.func))]='raise'
    run('constructed '+phase+' db='+str(has_db),c,final(phase,None,None,'abrupt'))
  c=db_fact(files(case('recover')),True);c['outcomes'][addr(1,validate,'call:self._validate')]='raise';c['outcomes'][addr(4,close,'call:self._retired.close')]='raise';run('constructed validation and cleanup failure retain partial object',c,final('CLEANUP_UNCERTAIN',None,'call-result:1:'+key(alloc),'abrupt'))
  c=files(case('recover'));publication=find('recover',ast.Assign,'self._live = a');c['stop_after']=addr(1,publication);run('constructed interrupted publication retains both aliases',c,final('VALIDATION_FAILED','call-result:1:'+key(alloc),'call-result:1:'+key(alloc),'partial-prefix'))
  c=case('close','L',None,'READY');run('constructed clean close',c,final('CLOSED'))
  c=case('close','L',None,'READY');c['outcomes'][addr(3,close,'call:self._retired.close')]='raise';run('constructed failed close preserves cleanup obligation',c,final('CLEANUP_UNCERTAIN',None,'initial:L','abrupt'))
  c=case('_run','L',None,'READY');test=next(n.test for n in ast.walk(methods['_run']) if isinstance(n,ast.If));c['facts'][addr(1,test)]={'value':True,'subject':token(c,'initial:L')};q=next(n for n in ast.walk(methods['_run']) if isinstance(n,ast.Call) and attr(n.func)=='_quarantine');c['outcomes'][addr(1,q,'argument-evaluation')]='raise';run('constructed exception formatting fails before quarantine entry',c,final('READY','initial:L',None,'abrupt'))
  # Independently validate model output mutations: values/identity, ordering,
  # missing transfers and fabricated clear/closure cannot replace source replay.
  for label,o in list(paths.items()):
   b=copy.deepcopy(o);b['final']['_retired']=None if o['final']['_retired'] else token(o['case'],'invented')
   check('reject wrong final reference '+label,lambda o=o,b=b:reject(lambda:m.reference_path(data,o['case'],b)))
  o=paths['constructed normal recovery publication']
  for label,edit in [('missing transfer',lambda b:b['events'].pop(next(i for i,e in enumerate(b['events']) if e['event']=='reference-write'))),('reordered events',lambda b:b['events'].reverse()),('stale local reference',lambda b:next(e for e in b['events'] if e['event']=='reference-write' and e['target']=='_live')['rhs'].update(origin='initial:stale')),('false physical closure',lambda b:b.update(physical_close_established=True)),('wrong instance',lambda b:b['scope'].update(instance='other'))]:
   b=copy.deepcopy(o);edit(b);check('constructed rejects '+label,lambda b=b:reject(lambda:m.reference_path(data,o['case'],b)))
  c=copy.deepcopy(paths['constructed OPEN_FAILED db=False']['case']);c['facts'][addr(1,hasdb)]['subject']=token(c,'initial:wrong');check('no-db clear rejects stale fact subject',lambda:reject(lambda:m.reference_path(data,c)))
  c=copy.deepcopy(paths['constructed normal recovery publication']['case']);c['context']='SYMBOLIC-U-TWO';out=m.reference_path(data,c);check('second context keeps separate reference namespace',lambda:out['final']['_live']!=o['final']['_live'])
  for idx in (0,1):
   b=copy.deepcopy(bundle);b['contexts'][idx]['reference_declarations']['source']['writes'].pop();check('public omitted transfer context '+str(idx),lambda b=b:reject(lambda:m.validate(a.root,m.enc(b))))
   b=copy.deepcopy(bundle);b['contexts'][idx]['saved_reference_scope'][0]['observed_reference_transfers']=[];check('public unsupported observed transfer claim context '+str(idx),lambda b=b:reject(lambda:m.validate(a.root,m.enc(b))))
  b=copy.deepcopy(bundle);b['contexts'].pop();check('public missing context rejected',lambda:reject(lambda:m.validate(a.root,m.enc(b))))
  b=copy.deepcopy(bundle)
  for v in b['contexts']:v['reference_declarations']['source']['writes']=[];v['reference_declarations']['declarations']=[]
  check('public coordinated catalogue and origin deletion',lambda:reject(lambda:m.validate(a.root,m.enc(b))))
  b=copy.deepcopy(bundle);b['prior_field_receipt']['sha256']='0'*64;check('public stale reviewed field receipt',lambda:reject(lambda:m.validate(a.root,m.enc(b))))
  b=copy.deepcopy(bundle);b['contexts'][0]['saved_reference_scope'][0]['instance']={'id':'other-acquisition'};check('public mixed instance binding',lambda:reject(lambda:m.validate(a.root,m.enc(b))))
  # Existing sparse evidence checks are reused; inject one contradictory close
  # snapshot through the new internal seam, without a host or database call.
  evidence=dict(data['ctx']['e']);trace=json.loads(evidence['evidence/execution-trace.json']);event=next(e for e in trace['events'] if e['event']=='return' and e['function']=='ManagedAuthority.close');event['state']['_phase']='READY';evidence['evidence/execution-trace.json']=m.enc(trace)
  check('new seam preserves existing close completion rejection',lambda:reject(lambda:m.derive_reference(data,cat,evidence)))
  answer=m.validate(a.root,saved);answer['contexts'].clear();answer['receipt'].clear();bundle['contexts'][0]['reference_declarations']['source']['writes'].clear();cat['source']['writes'].clear()
  check('nested returned mutations cannot change public expectations',lambda:m.validate(a.root,saved))
  assert original=={n:identity((a.root/'code'/n).read_bytes()) for n in original}
 except BaseException as ex:error=repr(ex);raise
 finally:
  (a.output/'constructed-paths.json').write_text(json.dumps(paths,sort_keys=True,indent=2)+'\n')
  result={'result':'PASS' if error is None else 'FAIL','passed':len(rows),'checks':rows,'error':error,'source':original,'source_after':{n:identity((a.root/'code'/n).read_bytes()) for n in original},'root':str(a.root),'python':sys.version,'optimization':sys.flags.optimize,'prior_suites_rerun':False,'new_controls_only':True,'database_connections':0,'host_session_execution':False,'constructed_paths_are_not_observations':True}
  (a.output/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PASS',len(rows),'new reference-transfer controls')
if __name__=='__main__':main()
