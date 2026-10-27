"""Independent bounded SOC-02-R1 controls. Never executes retained suites or runtime."""
from pathlib import Path
import argparse,ast,copy,hashlib,importlib.metadata,json,os,sys,traceback,types
TRACE='evidence/execution-trace.json';EXPORT='evidence/recovery-export-0.json'
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def module(p):
 m=types.ModuleType('independent_r1');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',required=True,type=Path);ap.add_argument('--output',required=True,type=Path);ap.add_argument('--recovered',action='store_true');a=ap.parse_args();root=a.root.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
 def audit(event,args):
  if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo'):raise AssertionError('FORBIDDEN:'+event)
  if event=='open' and isinstance(args[0],(str,bytes)):
   s=os.fsdecode(args[0])
   if s.startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
   if s.startswith(str(root)+'/') and len(args)>2 and type(args[2]) is int and args[2]&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC):raise AssertionError('INPUT-WRITE')
 sys.addaudithook(audit)
 def profile(f,event,arg):
  name=f.f_code.co_filename.rsplit('/',1)[-1]
  if event=='call' and (name in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py') or name=='prospective_entry.py' and f.f_code.co_name in ('main','run','run_controlled','_run','_dispatch','__init__','state','handle','status')):raise AssertionError('APPLICATION-EXECUTION')
 sys.setprofile(profile);rows=[];witnesses=[]
 def record(label,**facts):
  rows.append({'check':label,**facts})
  with (out/'progress.jsonl').open('ab') as f:f.write(enc(rows[-1]))
 def good(label,condition):
  assert condition,label;record(label,result='PASS')
 def reject(label,fn):
  try:fn()
  except (ValueError,TypeError,KeyError,FileNotFoundError) as ex:
   result={'type':type(ex).__name__,'message':str(ex)};record(label,result='REJECTED',error=result);return result
  raise AssertionError('UNEXPECTED ACCEPTANCE: '+label)
 try:
  current=root/'corrected';src=current/'code/smoke_occurrences.py';before=identity(src.read_bytes());m=module(src);ctx=m.load(current);raw=(current/'results/occurrence-connection.json').read_bytes();e=ctx['e'];trace=json.loads(e[TRACE]);export=json.loads(e[EXPORT]);head=json.loads(bytes.fromhex(export['head']));owner_digest=hashlib.sha256(bytes.fromhex(export['ownership_meta'])).hexdigest()
  good('pristine public validation',m.validate(current,raw)['result']=='PASS')
  good('pristine derivation byte identity',enc(m.derive(ctx))==raw)
  good('pristine semantic frame count',len(m.semantic(ctx,e)['frames'])==18)
  # Independent source and record expectations, without calling the correction's
  # AST reader to manufacture an expected result.
  source=ctx['c']['retained/candidate/support/reference/runtime/authority.py'];tree=ast.parse(source);cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Authority');close=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='close')
  good('pinned close has only self.db.close effect',[ast.unparse(n) for n in close.body]==['self.db.close()'])
  worker=ast.parse(e['preparation/worker.py']);snap=next(n for n in worker.body if isinstance(n,ast.FunctionDef) and n.name=='snapshot');projection=next(n.value for n in snap.body if isinstance(n,ast.Return));keys=set(ast.literal_eval(projection.generators[0].iter))
  assigned={t.attr for n in ast.walk(cls) if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Attribute) and isinstance(t.value,ast.Name) and t.value.id=='self'}&keys
  good('source assignments intersect observer projection',assigned=={'binding','ownership_binding'})
  calls={v['frame']:v for v in trace['events'] if v['event']=='call' and not v['resumed_generator']};ends={v['frame']:v for v in trace['events'] if v['event']=='return' and v['normal_return']}
  closes={('managed' if calls[v['parent']]['function']=='ManagedAuthority.close' else 'raw'):fid for fid,v in calls.items() if v['function']=='Authority.close'}
  good('raw and managed invocations independently identified',set(closes)=={'raw','managed'} and len(set(closes.values()))==2)
  for role,fid in closes.items():
   good(role+' call return and exact export bindings',calls[fid]['state']==ends[fid]['state']=={'binding':head['binding'],'ownership_binding':owner_digest})
  auditdata={'source':identity(source),'worker':identity(e['preparation/worker.py']),'close_source':ast.unparse(close),'projected_identity_fields':sorted(assigned),'head':identity(bytes.fromhex(export['head'])),'ownership_raw':identity(bytes.fromhex(export['ownership_meta'])),'roles':{role:{'frame':fid,'call_seq':calls[fid]['seq'],'return_seq':ends[fid]['seq']} for role,fid in closes.items()}}
  (out/'source-audit.json').write_text(json.dumps(auditdata,indent=2)+'\n')
  for label in ('managed-close-binding-one-byte','raw-close-ownership-one-byte','coordinated-close-bindings'):
   folder=root/'review/independent-primary/residuals'/label;alt=dict(e);alt[TRACE]=(folder/'altered-trace.json').read_bytes();saved=(folder/'derived-receipt.json').read_bytes()
   if not a.recovered:
    old=module(root/'original/code/smoke_occurrences.py');oldctx=old.load(current)
    good('old semantic acceptance '+label,len(old.semantic(oldctx,alt)['frames'])==18)
    good('old exact derived witness '+label,enc(old.derive(dict(oldctx,e=alt)))==saved)
    reject('old public pin protection '+label,lambda:old.validate(current,saved))
   sem=reject('corrected semantic '+label,lambda:m.semantic(ctx,alt));der=reject('corrected derive '+label,lambda:m.derive(dict(ctx,e=alt)));pub=reject('corrected public '+label,lambda:m.validate(current,saved))
   witnesses.append({'variant':label,'trace':identity(alt[TRACE]),'saved_receipt':identity(saved),'semantic_rejection':sem,'derive_rejection':der,'public_rejection':pub})
  if not a.recovered:
   def mutation(label,fn):
    t=copy.deepcopy(trace);fn(t['events']);alt=dict(e);alt[TRACE]=enc(t)
    reject('semantic '+label,lambda:m.semantic(ctx,alt));reject('derive '+label,lambda:m.derive(dict(ctx,e=alt)))
   def select(es,role,event):return next(v for v in es if v['frame']==closes[role] and v['event']==event)
   def flip(v):return ('f' if v[0]!='f' else 'e')+v[1:]
   for role in ('raw','managed'):
    for event in ('call','return'):
     for key in sorted(assigned):
      mutation(role+' '+event+' '+key,lambda es,role=role,event=event,key=key:select(es,role,event)['state'].update({key:flip(select(es,role,event)['state'][key])}))
    for key in sorted(assigned):
     mutation(role+' coordinated both endpoints '+key,lambda es,role=role,key=key:[select(es,role,event)['state'].update({key:flip(select(es,role,event)['state'][key])}) for event in ('call','return')])
   def all_identical(es,include_constructor=False):
    for v in es:
     if (v['function']=='Authority.close' or include_constructor and v['function']=='Authority.__init__' and v['event']=='return'):
      for k in assigned:v['state'][k]=flip(v['state'][k])
   mutation('coordinated both closes and fields',all_identical)
   mutation('coordinated constructors and both closes',lambda es:all_identical(es,True))
   for role in ('raw','managed'):
    mutation(role+' swapped identity roles',lambda es,role=role:[v['state'].update(binding=v['state']['ownership_binding'],ownership_binding=v['state']['binding']) for v in es if v['frame']==closes[role]])
    mutation(role+' missing projected field',lambda es,role=role:select(es,role,'call')['state'].pop('ownership_binding'))
    mutation(role+' extra projected field',lambda es,role=role:select(es,role,'return')['state'].update(unobserved='invented'))
   for value in (None,False,0,[],{}):
    mutation('exact identity type '+repr(value),lambda es,value=value:select(es,'managed','call')['state'].update(binding=value))
   # Anchor changes are tested separately from trace mutations. Matching trace
   # fields cannot excuse disagreement with retained HEAD/ownership bytes.
   for label,fn in [('HEAD binding',lambda x:x.update(head=enc({**head,'binding':flip(head['binding'])}).hex())),('ownership exact bytes',lambda x:x.update(ownership_meta=(bytes.fromhex(x['ownership_meta'])+b' ').hex()))]:
    alt=dict(e);x=copy.deepcopy(export);fn(x);alt[EXPORT]=enc(x)
    reject('semantic altered '+label,lambda:m.semantic(ctx,alt));reject('derive altered '+label,lambda:m.derive(dict(ctx,e=alt)))
   for missing in (EXPORT,'evidence/client-handoff.json'):
    alt=dict(e);del alt[missing];reject('semantic missing '+missing,lambda:m.semantic(ctx,alt));reject('derive missing '+missing,lambda:m.derive(dict(ctx,e=alt)))
   # In-memory changed-source negative only: implementation files stay intact.
   altered_c=dict(ctx['c']);key='retained/candidate/support/reference/runtime/authority.py';altered_c[key]=source.replace(b'def close(self):self.db.close()',b"def close(self):self.db.close();self.binding='changed'")
   good('unsupported-effect fixture is not no-op',altered_c[key]!=source)
   reject('unsupported source effect has no identity-preservation assumption',lambda:m.semantic(dict(ctx,c=altered_c),e))
  # Small preservation controls, not a rerun of the completed SOC-01 review.
  response=m.validate(current,raw);response['contexts'].clear();response['receipt'].clear()
  d=m.derive(ctx);d['contexts'][0]['occurrences'][0]['source'].clear();d['contexts'][1]['joins'].clear()
  good('returned and nested mutations leave expectations intact',enc(m.derive(ctx))==raw and m.validate(current,raw)['result']=='PASS')
  receipt=json.loads(raw)
  good('both contexts retain declared order',[v['context'] for v in receipt['contexts']]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
  for i,view in enumerate(receipt['contexts']):
   traced=[v for v in view['occurrences'] if v['kind']=='traced-invocation'];obs=[v for v in view['occurrences'] if v['kind']=='explicit-observer-call']
   good('18 traced plus separate observer '+view['context'],len(traced)==18 and len({v['id'] for v in traced})==18 and len(obs)==1 and obs[0]['frame'] is None and obs[0]['parent_frame'] is None and obs[0]['source']['qualified']=='Client.state')
   good('UNKNOWN classifications retained '+view['context'],all(v['classification']=='UNKNOWN' and v['canonical_ordinal'] is None for v in view['occurrences']))
   if not a.recovered:
    d=copy.deepcopy(receipt);d['contexts'].pop(i);reject('context individually required '+str(i),lambda:m.validate(current,enc(d)))
  good('all obligations and UNKNOWN totals retained',receipt['all_eleven_obligations_preserved'] is True and receipt['inventory_unknown_totals']==4 and receipt['lifetime_unknown_totals']==14 and receipt['actual_admission'] is False)
  if not a.recovered:
   d=copy.deepcopy(receipt);d['contexts'][0]['occurrences'][0]['call']['acquisition']='stale';reject('public stale acquisition receipt',lambda:m.validate(current,enc(d)))
   d=copy.deepcopy(receipt);d['contexts'].reverse();reject('public context order substitution',lambda:m.validate(current,enc(d)))
   d=copy.deepcopy(receipt);d['actual_admission']=True;d['lifetime_unknown_totals']=0;reject('public unsupported status and unknown-zero',lambda:m.validate(current,enc(d)))
  good('final pristine accepted unchanged',enc(m.derive(ctx))==raw and m.validate(current,raw)['result']=='PASS')
  good('implementation bytes unchanged',identity(src.read_bytes())==before)
  result={'result':'PASS bounded SOC-02-R1 correction; no residual found in tested scope','assertions':len(rows),'checks':rows,'witnesses':witnesses,'old_variants_reproduced':0 if a.recovered else 3,'recovered_root':a.recovered,'source':before,'pristine_receipt':identity(raw),'environment':{'python':sys.version,'optimization':sys.flags.optimize,'cryptography_installed':importlib.metadata.version('cryptography'),'operations':'offline source and saved-evidence validation only'},'supplied_tests_executed':False,'completed_reviews_rerun':False,'host_session_execution':False,'database_connections':0}
  (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'assertions':len(rows),'recovered':a.recovered,'result':result['result']}))
 except BaseException:
  (out/'PARTIAL.json').write_text(json.dumps({'checks':rows,'witnesses':witnesses,'failure':traceback.format_exc()},indent=2)+'\n');raise
 finally:sys.setprofile(None)
if __name__=='__main__':main()
