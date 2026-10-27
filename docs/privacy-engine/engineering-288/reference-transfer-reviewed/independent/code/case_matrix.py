"""Reviewer source-read expectations; all cases are constructed, not history."""
import ast,copy
def key(n):return ':'.join(map(str,(n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__)))
def cases(raw,context):
 cls=next(n for n in ast.parse(raw).body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority')
 methods={n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)}
 def find(fn,kind,text,index=0):return sorted([n for n in ast.walk(methods[fn]) if isinstance(n,kind) and ast.unparse(n)==text],key=lambda n:(n.lineno,n.col_offset))[index]
 def addr(frame,n,kind=None):return str(frame)+'/'+key(n)+('' if kind is None else '/'+kind)
 def case(method,live=None,retired=None,phase='CLOSED'):
  return {'kind':'CONSTRUCTED-REFERENCE-PATH','context':context,'scope':{'acquisition':'review-constructed-only','instance':'instance-A','invocation':'invocation-A'},'method':method,'initial':{'_live':live,'_retired':retired,'_phase':phase},'facts':{},'outcomes':{},'stop_after':None}
 def token(c,origin):return {'kind':'constructed-reference','scope':{'context':context,**c['scope']},'origin':origin}
 def fact(c,n,value,subject=None,frame=1):c['facts'][addr(frame,n)]={'value':value,'subject':subject};return c
 def gate(c,n,kind,outcome,frame=1):c['outcomes'][addr(frame,n,kind)]=outcome;return c
 def files(c):
  for text in ('self._path.is_file()','self._owners.is_file()'):fact(c,find('recover',ast.Call,text),True)
  return c
 alloc=find('recover',ast.Call,'self._runtime.Authority.__new__(self._runtime.Authority)');allocation='call-result:1:'+key(alloc)
 hasdb=find('recover',ast.Call,"hasattr(a, 'db')")
 ctor=next(n for n in ast.walk(methods['recover']) if isinstance(n,ast.Call) and ast.unparse(n.func)=='self._runtime.Authority.__init__')
 validation=find('recover',ast.Call,'self._validate(a)');close=find('_dispose',ast.Call,'self._retired.close()')
 def db(c,present):return fact(c,hasdb,present,token(c,allocation))
 wi=find('__init__',ast.Assign,'self._live = None');ri=find('__init__',ast.Assign,'self._retired = None')
 transfer=find('_quarantine',ast.Assign,'self._retired = self._live');clear=find('_quarantine',ast.Assign,'self._live = None')
 disposed=find('_dispose',ast.Assign,'self._retired = None')
 retain=find('recover',ast.Assign,'self._retired = a',0);handler_retain=find('recover',ast.Assign,'self._retired = a',1)
 publish=find('recover',ast.Assign,'self._live = a');pubclear=find('recover',ast.Assign,'self._retired = None',0);nodbclear=find('recover',ast.Assign,'self._retired = None',1)
 noinit={'kind':'uninitialized-slot'};rows=[]
 def write(n,value):return {'site':key(n),'slot':n.targets[0].attr,'origin':value}
 def add(name,c,phase,live=None,retired=None,completion='normal',writes=()):
  rows.append({'name':name,'case':c,'expected':{'completion':completion,'phase':phase,'live':live,'retired':retired,'writes':list(writes)}})
 c=case('__init__');condition=next(n.test for n in methods['__init__'].body if isinstance(n,ast.If));fact(c,condition,False)
 add('constructor normal',c,'CLOSED',writes=[write(wi,None),write(ri,None)])
 c=case('__init__');c['stop_after']=addr(1,wi);add('constructor interrupted between slot initialization',c,None,retired=noinit,completion='partial-prefix',writes=[write(wi,None)])
 c=case('__init__');fact(c,condition,True);add('constructor source mismatch after initialized slots',c,'CLOSED',completion='abrupt',writes=[write(wi,None),write(ri,None)])
 c=case('_quarantine','L',None,'READY');add('quarantine copy then clear',c,'QUARANTINED',retired='initial:L',writes=[write(transfer,'initial:L'),write(clear,None)])
 c=case('_quarantine',None,'R','CLEANUP_UNCERTAIN');add('quarantine with no live preserves retired',c,'QUARANTINED',retired='initial:R')
 c=case('_quarantine','L',None,'READY');c['stop_after']=addr(1,transfer);add('quarantine interrupted between copy and clear',c,'QUARANTINED','initial:L','initial:L','partial-prefix',[write(transfer,'initial:L')])
 c=case('_dispose',None,None,'QUARANTINED');add('empty disposal is early return not closure',c,'QUARANTINED')
 c=case('_dispose',None,'R','QUARANTINED');add('normal disposal clear follows close',c,'CLOSED',writes=[write(disposed,None)])
 for outcome,completion in [('raise','abrupt'),('stop','partial-prefix')]:
  c=case('_dispose',None,'R','QUARANTINED');gate(c,close,'call:self._retired.close',outcome);add('disposal close '+outcome,c,'CLEANUP_UNCERTAIN',retired='initial:R',completion=completion)
 c=case('_dispose',None,'R','QUARANTINED');c['stop_after']=addr(1,find('_dispose',ast.Expr,'self._retired.close()'));add('disposal stopped after close before clear',c,'CLEANUP_UNCERTAIN',retired='initial:R',completion='partial-prefix')
 normal=[write(retain,allocation),write(publish,allocation),write(pubclear,None)]
 c=files(case('recover'));add('recover successful publication',c,'READY',allocation,writes=normal)
 c=files(case('recover','L','L','QUARANTINED'));add('recover interrupted alias disposes before allocation',c,'READY',allocation,writes=[write(transfer,'initial:L'),write(clear,None),write(disposed,None)]+normal)
 c=case('recover',None,'R','CLEANUP_UNCERTAIN');gate(c,close,'call:self._retired.close','raise',2);add('recover old close failure prevents allocation',c,'CLEANUP_UNCERTAIN',retired='initial:R',completion='abrupt')
 c=case('recover','L',None,'READY');add('recover READY refusal retains references',c,'READY','initial:L',completion='abrupt')
 c=case('recover');fact(c,find('recover',ast.Call,'self._path.is_file()'),False);add('recover missing first file short circuits',c,'OPEN_FAILED',completion='abrupt')
 c=files(case('recover'));gate(c,alloc,'allocation-return','raise');add('allocation failure before retained assignment',c,'OPEN_FAILED',completion='abrupt')
 c=files(case('recover'));c['stop_after']=addr(1,find('recover',ast.Assign,ast.unparse(find('recover',ast.Assign,'a = self._runtime.Authority.__new__(self._runtime.Authority)'))));add('stop after allocation before retained assignment',c,'OPEN_FAILED',completion='partial-prefix')
 for step,phase,present in [(ctor,'OPEN_FAILED',False),(ctor,'OPEN_FAILED',True),(validation,'VALIDATION_FAILED',True)]:
  c=db(files(case('recover')),present);gate(c,step,'call:'+ast.unparse(step.func),'raise')
  add('failed '+phase+' db='+str(present),c,phase,completion='abrupt',writes=[write(retain,allocation),write(handler_retain,allocation),write(disposed if present else nodbclear,None)])
 c=db(files(case('recover')),True);gate(c,validation,'call:self._validate','raise');gate(c,close,'call:self._retired.close','raise',4)
 add('failed validation then failed cleanup retains partial object',c,'CLEANUP_UNCERTAIN',retired=allocation,completion='abrupt',writes=[write(retain,allocation),write(handler_retain,allocation)])
 c=files(case('recover'));c['stop_after']=addr(1,publish);add('stop after publication before retired clear',c,'VALIDATION_FAILED',allocation,allocation,'partial-prefix',normal[:2])
 c=db(files(case('recover')),True);gate(c,pubclear,'statement-entry','raise')
 add('exception between publication and clear',c,'VALIDATION_FAILED',completion='abrupt',writes=normal[:2]+[write(transfer,allocation),write(clear,None),write(handler_retain,allocation),write(disposed,None)])
 ret=next(n for n in ast.walk(methods['recover']) if isinstance(n,ast.Return));c=db(files(case('recover')),True);gate(c,ret,'return-expression','raise')
 add('return evaluation failure after READY cleans then quarantines',c,'QUARANTINED',completion='abrupt',writes=normal+[write(transfer,allocation),write(clear,None),write(handler_retain,allocation),write(disposed,None)])
 c=files(case('recover'));with_node=next(n for n in methods['recover'].body if isinstance(n,ast.With));gate(c,with_node,'context-exit','raise')
 add('context exit failure after publication does not invent cleanup',c,'READY',allocation,completion='abrupt',writes=normal)
 c=case('close','L',None,'READY');add('close successful source continuation',c,'CLOSED',writes=[write(transfer,'initial:L'),write(clear,None),write(disposed,None)])
 c=case('close','L',None,'READY');gate(c,close,'call:self._retired.close','raise',3);add('close failure retains retired',c,'CLEANUP_UNCERTAIN',retired='initial:L',completion='abrupt',writes=[write(transfer,'initial:L'),write(clear,None)])
 tests=sorted([n.test for n in ast.walk(methods['_run']) if isinstance(n,ast.If)],key=lambda n:n.lineno)
 c=case('_run','L',None,'READY')
 for n in tests:fact(c,n,False,token(c,'initial:L'))
 add('normal guarded dispatch preserves slots',c,'READY','initial:L')
 c=case('_run','L',None,'READY');fact(c,tests[0],True,token(c,'initial:L'));add('active transaction triggers quarantine transfer',c,'QUARANTINED',retired='initial:L',completion='abrupt',writes=[write(transfer,'initial:L'),write(clear,None)])
 c=case('_run','L',None,'READY');fact(c,tests[0],True,token(c,'initial:L'))
 q=next(n for n in ast.walk(methods['_run']) if isinstance(n,ast.Call) and ast.unparse(n.func)=='self._quarantine');gate(c,q,'argument-evaluation','raise')
 add('exception formatting can fail before quarantine',c,'READY','initial:L',completion='abrupt')
 c=case('_require','L','R','READY');add('retired slot forbids serving despite READY',c,'READY','initial:L','initial:R','abrupt')
 return rows,{'methods':methods,'addr':addr,'find':find,'allocation':allocation,'hasdb':hasdb,'token':token}

def compare(case,expected,actual):
 scope={'context':case['context'],**case['scope']}
 def expand(v):
  if v is None or isinstance(v,dict):return copy.deepcopy(v)
  return {'kind':'constructed-reference','scope':scope,'origin':v}
 assert actual['scope']==scope and actual['case']==case
 assert actual['completion']==expected['completion']
 assert actual['final']=={'_live':expand(expected['live']),'_retired':expand(expected['retired']),'_phase':expected['phase']}
 for flag in ['actual_observation','object_identity_evidence','physical_close_established','outstanding_obligations_discharged']:assert actual[flag] is False
 writes=[e for e in actual['events'] if e['event']=='reference-write'];assert len(writes)==len(expected['writes'])
 prior={slot:expand(None if value is None else 'initial:'+value) for slot,value in case['initial'].items() if slot!='_phase'}
 if case['method']=='__init__':prior={s:{'kind':'uninitialized-slot'} for s in ('_live','_retired')}
 for observed,wanted in zip(writes,expected['writes']):
  assert observed['site']==wanted['site'] and observed['target']==wanted['slot'] and observed['rhs']==expand(wanted['origin'])
  assert all(observed['before'][s]==prior[s] for s in prior)
  prior[wanted['slot']]=expand(wanted['origin'])
  assert all(observed['after'][s]==prior[s] for s in prior)
 # A completed opaque close remains only a premise over the current symbolic
 # receiver. It never becomes object/connection evidence or discharged duty.
 state={s:expand(None if case['initial'][s] is None else 'initial:'+case['initial'][s]) for s in ('_live','_retired')}
 for event in actual['events']:
  if event['event']=='reference-write':state[event['target']]=event['rhs']
  if event.get('kind')=='call:self._retired.close':assert event['subject']==state['_retired'] and state['_retired'] is not None
 return True
