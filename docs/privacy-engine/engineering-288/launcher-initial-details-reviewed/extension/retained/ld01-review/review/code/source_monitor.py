from pathlib import Path
import sys,json,ast,difflib,traceback,contextlib,inspect,types
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from cases import ORDER,ROUTE,FIELDS
root=Path(sys.argv[1]);r=Records(sys.argv[2]);error=None
def req(x):assert x;return True
try:
 r.save('input-verification.json',verify_root(root));guard(root,r.path,r);c=module(root/'code/managed_coverage.py');m=module(root/'code/correspondence.py')
 entry=(root/'source-evidence/prospective_entry.py').read_bytes();launcher=(root/'source-evidence/lab_bootstrap.py').read_bytes();et=ast.parse(entry);lt=ast.parse(launcher)
 def fn(t,n):return next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name==n)
 run=fn(et,'_run');session=fn(lt,'session');private=fn(lt,'_session')
 rw=next(n for n in ast.walk(run) if isinstance(n,ast.With));sw=session.body[-1];sy=sw.body[0]
 tr=next(n for n in ast.walk(private) if isinstance(n,ast.Try) and any(h.name=='e' for h in n.handlers));h=tr.handlers[0];py=next(n for n in tr.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Yield));assignment=h.body[0];d=assignment.value
 assert ast.unparse(rw.items[0].context_expr)=='launcher.session(candidate, draft, runtime, destination, create=create)' and ast.unparse(rw.items[0].optional_vars)=='wrapper'
 assert [ast.unparse(x) for x in session.decorator_list]==[ast.unparse(x) for x in private.decorator_list]==['contextlib.contextmanager']
 assert ast.unparse(sw.items[0].context_expr)=='_session(*args, **kwargs)' and ast.unparse(sy)=='yield managed' and ast.unparse(py)=='yield ManagedSession(managed)'
 assert ast.unparse(h.type)=='BaseException' and h.name=='e' and ast.unparse(assignment.targets[0])=='details'
 names=[n.value for n in d.keys];expr=[ast.unparse(n) for n in d.values];assert names==FIELDS and expr==['type(e).__name__','str(e)','traceback.format_exc()','False','False','[]']
 assert isinstance(h.body[1],ast.For) and h.body[1].lineno==169 and h.lineno==167 and assignment.lineno==168
 excluded=tr.body[tr.body.index(py)+1:];assert [ast.unparse(n) for n in excluded]==['managed.close()','managed = None',"(dest / 'ACTIVE.json').unlink()"]
 nodes=[rw,sy,sw,py,h,assignment]+[n for pair in zip(d.keys,d.values) for n in pair]+[d,assignment.targets[0],assignment]
 def loc(n,raw):return {'site':':'.join(map(str,[n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__])),'expression':ast.get_source_segment(raw.decode(),n)}
 receipt=json.loads((root/'results/primary/launcher-details.json').read_bytes());old=json.loads((root/'retained/client-construction/results/primary/client-construction-none.json').read_bytes())
 for idx,row in enumerate(receipt['contexts']):
  cat=row[m.RELATION]['declaration'];src=cat['source'];parent=row['client_construction_none_correspondence']['declaration']
  r.yes('source order independent of catalogue '+str(idx),lambda:req(src['order']==ORDER and [x['id'] for x in cat['declarations']]==ORDER))
  for i,(name,node) in enumerate(zip(ORDER,nodes)):
   raw=entry if i==0 else launcher
   r.yes('independent coordinate and defining bytes '+str((idx,name)),lambda name=name,node=node,raw=raw:req(all(src['stages'][name][k]==v for k,v in loc(node,raw).items()) and src['stages'][name]['source']==identity(raw)))
  r.yes('field expression origins and literal types '+str(idx),lambda:req([(f['name'],f['expression']) for f in src['fields']]==list(zip(FIELDS,expr)) and d.values[3].value is False and d.values[4].value is False and isinstance(d.values[5],ast.List) and not d.values[5].elts))
  r.yes('normal close clear unlink excluded; stop before cleanup '+str(idx),lambda:req(all(all(claim[k]==v for k,v in loc(n,launcher).items()) for claim,n in zip(src['excluded_normal_stages'],excluded)) and all(src['stop_before'][k]==v for k,v in loc(h.body[1],launcher).items())))
  r.yes('UNKNOWN duties and inherited context fields retained '+str(idx),lambda:req(all(x['classification']=='UNKNOWN' and x['multiplicity'] is None and x['ordinal'] is None for x in cat['declarations']) and all(row[k]==v for k,v in old['contexts'][idx].items()) and set(row)-set(old['contexts'][idx])=={m.RELATION}))
  r.yes('catalogue accepted under exact defining source '+str(idx),lambda:c.validate_launcher_details(launcher,entry,parent,cat))
  for field,val in [('catch_binding','other'),('order',list(reversed(ORDER)))]:
   x=D(cat);x['source'][field]=val;r.no('source mapping altered '+str((idx,field)),lambda x=x:c.validate_launcher_details(launcher,entry,parent,x),'DETAILS-SOURCE-CORRESPONDENCE')
  x=D(cat);x['source']['fields'][3]['expression']='0';r.no('False is not integer zero '+str(idx),lambda:c.validate_launcher_details(launcher,entry,parent,x),'DETAILS-SOURCE-CORRESPONDENCE')
  x=D(cat);x['source']['order'].remove('details-dict-completion');del x['source']['stages']['details-dict-completion'];x['declarations']=[v for v in x['declarations'] if v['id']!='details-dict-completion'];r.no('coordinated omission cannot redefine source requirements '+str(idx),lambda:c.validate_launcher_details(launcher,entry,parent,x),'DETAILS-SOURCE-CORRESPONDENCE')
  if idx==0:
   for a,b,code in [(b"'message':str(e)",b"'message':str(other)",'DETAILS-FIELD-ORIGINS'),(b"'new_authorization':False",b"'new_authorization':0",'DETAILS-FIELD-ORIGINS'),(b'with _session(*args,**kwargs) as managed:',b'with _session(*args) as managed:','DETAILS-PUBLIC-PRIVATE-BRIDGE'),(b'except BaseException as e:',b'except Exception as e:','DETAILS-PRIVATE-CATCH')]:
    altered=launcher.replace(a,b);assert altered!=launcher;pp=D(parent);pp['source']['sources']['launcher']=identity(altered)
    r.no('changed source with coordinated source pin '+a.decode(),lambda altered=altered,pp=pp:c.validate_launcher_details(altered,entry,pp,cat),code)
 r.save('independent-source-expectations.json',{'entry':identity(entry),'launcher':identity(launcher),'order':ORDER,'locations':{name:loc(node,entry if i==0 else launcher) for i,(name,node) in enumerate(zip(ORDER,nodes))},'fields':list(zip(FIELDS,expr)),'excluded_normal':[ast.unparse(n) for n in excluded],'stop':loc(h.body[1],launcher),'runtime_or_opcode_history_established':False})
 # Inspect current CPython contextmanager exception bridge without executing it.
 raw=Path(contextlib.__file__).read_bytes();source=inspect.getsource(contextlib._GeneratorContextManager.__exit__)
 assert 'self.gen.throw(value)' in source and 'if exc is not value:' in source
 r.save('contextmanager-source-reference.json',{'python':sys.version,'path':contextlib.__file__,'identity':identity(raw),'source':source,'use':'Inspected environment source; conditional propagation explanation only; no generator or session executed; not installed-wheel authentication'})
 # Synthetic monitoring-plumbing checks. These are never authentic predecessor validations.
 sm=sys.monitoring
 def toy(mode):
  state={'calls':0,'basis_calls':0};value={'fresh':{},'marker':'toy-basis'}
  def basis():state['basis_calls']+=1;return value
  public={'result':'PASS','contexts':list(m.CONTEXTS),'receipt':D(m.PREDECESSOR_RECEIPT)}
  def validate(root,saved):
   state['calls']+=1
   if mode!='missing':basis()
   if mode=='extra':basis()
   if mode=='raise':raise ValueError('REVIEWER-SYNTHETIC-PREDECESSOR-FAILURE')
   return public
  p=types.SimpleNamespace(_basis=basis,validate=validate,_rows=lambda b:[],_assemble=lambda fresh,rows,b:b'wrong' if mode=='wrong-basis' else b'toy',enc=lambda x:x)
  if mode=='wrong-result':public['receipt']['sha256']='0'*64
  return {'prior_module':p,'prior_root':root,'prior_saved':b'toy'},state,public,value
 for mode in ('normal','missing','extra','raise','wrong-result','wrong-basis'):
  data,counts,stub_result,stub_basis=toy(mode)
  if mode=='normal':
   out=m._public_predecessor(data);r.yes('synthetic monitoring captures exact returned object',lambda:out[0] is stub_basis and counts=={'calls':1,'basis_calls':1});out[1]['contexts'].reverse();out[1]['receipt'].clear();r.yes('synthetic returned result is detached',lambda:stub_result['contexts']==list(m.CONTEXTS) and stub_result['receipt']==m.PREDECESSOR_RECEIPT)
  else:
   code={'missing':'DETAILS-PUBLIC-PREDECESSOR-RESULT','extra':'DETAILS-UNEXPECTED-BASIS-RETURN','raise':'REVIEWER-SYNTHETIC-PREDECESSOR-FAILURE','wrong-result':'DETAILS-PUBLIC-PREDECESSOR-RESULT','wrong-basis':'DETAILS-AUTHENTICATED-BASIS-RECEIPT'}[mode]
   r.no('synthetic monitoring rejects '+mode,lambda data=data:m._public_predecessor(data),code)
  r.yes('monitoring released on '+mode,lambda data=data:sm.get_tool(2) is None and sm.get_events(2)==0 and sm.get_local_events(2,data['prior_module']._basis.__code__)==0)
 data,counts,_,_=toy('normal');sm.use_tool_id(2,'reviewer-contention-owner')
 try:
  r.no('monitoring contention rejects before predecessor call',lambda:m._public_predecessor(data),'DETAILS-MONITORING-CONTENTION')
  r.yes('contention preserves other owner and makes no call',lambda:sm.get_tool(2)=='reviewer-contention-owner' and counts=={'calls':0,'basis_calls':0})
 finally:sm.free_tool_id(2)
 # The public authentication path ignores caller-supplied module/basis fields:
 # read exact AST wiring, avoiding another expensive completed predecessor validation.
 adapter=ast.parse((root/'code/correspondence.py').read_bytes());af={n.name:n for n in adapter.body if isinstance(n,ast.FunctionDef)}
 bsrc=ast.unparse(af['_basis']);assert 'fresh = inputs(data[\'root\'])' in bsrc and '_public_predecessor(fresh)' in bsrc and "p.sources(pb['fresh'])[:2]" in bsrc
 r.yes('public basis reloads inputs before unchanged public predecessor and source check',lambda:True)
 r.save('monitoring-scope.json',{'synthetic_tests':'Monitoring plumbing only; not actual predecessor authentication','actual_validation':'Separate fresh-recovered process must call exact unchanged predecessor public validator once','source_wiring':bsrc,'slot':2,'reviewer_monitor_slot':4})
 changes=json.loads((root/'provenance/changed-files.json').read_bytes());diff=''
 for n in ('code/managed_coverage.py','code/correspondence.py'):
  a=(root/'retained/client-construction'/n).read_bytes();b=(root/n).read_bytes();assert identity(a)==changes['intentional_changes'][n]['before'] and identity(b)==changes['intentional_changes'][n]['after']
  diff+=''.join(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile='retained/client-construction/'+n,tofile=n))
  if n.endswith('managed_coverage.py'):
   assert b==a+b'\n\n'+(root/'tools/producer-addition.py').read_bytes();aa=ast.parse(a);bb=ast.parse(b);assert len(bb.body)==len(aa.body)+6 and sum(isinstance(x,ast.FunctionDef) for x in aa.body)==129 and all(ast.dump(x)==ast.dump(y) for x,y in zip(aa.body,bb.body))
 assert diff==(root/'provenance/implementation.diff').read_text()
 for n in ('prospective_entry.py','lab_bootstrap.py'):assert (root/'source-evidence'/n).read_bytes()==(root/'retained/client-construction/source-evidence'/n).read_bytes()
 allowed={'format','extension_components','contexts'}
 assert receipt['prior_client_construction_components']==old['extension_components']
 for k,v in old.items():
  if k not in allowed:assert receipt[k]==v,k
 supplied={}
 for label,n in [('source-corrected',66),('primary',862),('recovered',391)]:
  result=json.loads((root/'results'/label/'RESULT.json').read_bytes());progress=[json.loads(x) for x in (root/'results'/label/'progress.jsonl').read_text().splitlines()];out=[]
  for line in (root/'processes'/label/'stdout.log').read_text().splitlines():
   part=line.split(' ',1)
   if len(part)==2 and part[0].isdigit():a,b=part[1].rsplit(' ',1);out.append((int(part[0]),a,b))
  ex=json.loads((root/'processes'/label/'exit-status.json').read_bytes());assert result['result']=='PASS' and result['checks']==n and result['rows']==progress and len(progress)==len(out)==n and [(i+1,x['check'],x['result']) for i,x in enumerate(progress)]==out and ex['returncode']==0 and not ex['timed_out']
  supplied[label]={'controls':n,'result_identity':identity((root/'results'/label/'RESULT.json').read_bytes()),'exit':ex,'scope':result['scope']}
 failure=json.loads((root/'failures/source-initial/results/RESULT.json').read_bytes());assert failure['checks']==0 and json.loads((root/'failures/source-initial/processes/exit-status.json').read_bytes())['returncode']==1
 r.save('preservation-and-supplied.json',{'inherited_producer_functions':129,'new_functions':6,'producer_prefix_bytes_exact':True,'declared_diff_exact':True,'runtime_sources_unchanged':True,'all_prior_context_fields_preserved':True,'prior_envelope_preserved_except_declared_extension':True,'supplied':supplied,'supplied_failures':{n:(root/n).read_text() for n in ('failures/source-initial/RECORD.json','failures/recovery-cut-preparation/RECORD.json','failures/preparation-textencoder/RECORD.txt')},'historical_qualifications':json.loads((root/'provenance/prior-review-incorporation.json').read_bytes()),'limits':receipt['new_launcher_details_limits']})
 r.save('final-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(r.path/'failure.txt').write_text(error);raise
finally:r.finish(error,scope='Independent source derivation; synthetic monitoring plumbing, not actual predecessor authentication; read-only preservation and supplied-record reconciliation')
