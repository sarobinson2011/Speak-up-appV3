"""Fresh Formal-Lab[6] HF-01 controls. Saved bytes only; no producer execution."""
from pathlib import Path
import argparse,copy,hashlib,importlib.metadata,json,os,re,sys,time,traceback,types
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def canonical(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def module(p):
 m=types.ModuleType('independent_hf01');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def substitute(e,head):
 # Independent length-preserving reconstruction, not the supplied test helper.
 x=json.loads(e['evidence/recovery-export-0.json']);raw=bytes.fromhex(x['head']);old=json.loads(raw)['head']
 assert type(head) is str and len(head)==len(old) and head!=old
 def named(b,name):
  pattern=rb'("'+name.encode()+rb'"\s*:\s*")'+re.escape(old.encode())+rb'(")'
  changed,count=re.subn(pattern,lambda q:q[1]+head.encode()+q[2],b);assert count==1
  return changed
 out=dict(e);newraw=named(raw,'head')
 for n in ['evidence/execution-trace.json','evidence/client-handoff.json','evidence/session-records/BOOTSTRAP-COMPLETE.json','new-session-records/BOOTSTRAP-COMPLETE.json']:out[n]=named(e[n],'head')
 out['evidence/recovery-export-0.json']=named(e['evidence/recovery-export-0.json'],'expected_head').replace(raw.hex().encode(),newraw.hex().encode())
 out['evidence/smoke-result.json']=named(e['evidence/smoke-result.json'],'head').replace(raw.hex().encode(),newraw.hex().encode())
 oldhash=identity(e['evidence/session-records/BOOTSTRAP-COMPLETE.json'])['sha256'].encode();newhash=identity(out['evidence/session-records/BOOTSTRAP-COMPLETE.json'])['sha256'].encode()
 assert e['evidence/confirmed-close.json'].count(oldhash)==2
 out['evidence/confirmed-close.json']=e['evidence/confirmed-close.json'].replace(oldhash,newhash)
 changed={n:{'before':identity(e[n]),'after':identity(b),'changed_offsets':[i for i,(v,w) in enumerate(zip(e[n],b)) if v!=w]} for n,b in out.items() if b!=e[n]}
 assert len(changed)==7 and all(v['before']['bytes']==v['after']['bytes'] for v in changed.values())
 return out,changed
def main():
 parser=argparse.ArgumentParser();parser.add_argument('root',type=Path);parser.add_argument('output',type=Path);parser.add_argument('--recovered',action='store_true');a=parser.parse_args()
 root=a.root.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False);rows=[];error=None;profile_rows=[];constructed=[]
 def audit(event,args):
  if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo'):raise AssertionError('PROHIBITED:'+event)
  if event=='open' and isinstance(args[0],(str,bytes)):
   p=Path(os.fsdecode(args[0])).absolute();flags=args[2] or 0
   if str(p).startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
   if p.is_relative_to(root) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC):raise AssertionError('INPUT-WRITE')
 sys.addaudithook(audit)
 def profile(frame,event,arg):
  if event!='call':return
  filename=frame.f_code.co_filename.rsplit('/',1)[-1].lower();name=frame.f_code.co_name
  if filename in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py') or filename=='prospective_entry.py' and name in ('main','run','run_controlled','_run','_dispatch','__init__','state','handle','status'):raise AssertionError('PRODUCER-EXECUTION')
  parent=frame.f_back.f_code.co_name if frame.f_back else None
  if name=='derive_reference' and parent=='_validated_predecessor_basis':
   evidence=frame.f_locals['data']['ctx']['e'];profile_rows.append({'event':'mandatory predecessor consumes evidence','export':identity(evidence['evidence/recovery-export-0.json']),'trace':identity(evidence['evidence/execution-trace.json'])})
  if name=='_compare_validated_head' and parent=='_bind_predecessor_evidence':
   profile_rows.append({'event':'head value comparison','candidate':frame.f_locals['candidate_export']['expected_head'],'expected':frame.f_locals['expected_export']['expected_head']})
 sys.setprofile(profile)
 def record(label,category,result,**kw):
  row={'check':label,'category':category,'result':result,**kw};rows.append(row)
  with (out/'progress.jsonl').open('a') as f:f.write(json.dumps(row,sort_keys=True)+'\n')
 def check(label,f,category='independent'):
  v=f();assert v is not False,label;record(label,category,'PASS');return v
 def reject(label,f,reason=None,category='negative'):
  try:f()
  except (ValueError,TypeError,KeyError) as ex:
   if reason is not None:assert str(ex)==reason,(label,str(ex),reason)
   record(label,category,'REJECTED',error={'type':type(ex).__name__,'message':str(ex)});return
  raise AssertionError('UNEXPECTED-ACCEPTANCE:'+label)
 try:
  assert sys.version_info[:3]==(3,12,14) and not sys.flags.optimize
  m=module(root/'code/correspondence.py');source={n:identity((root/'code'/n).read_bytes()) for n in ('correspondence.py','managed_coverage.py')}
  data=m.recovery_inputs(root);cat=m.recovery_catalogue(data);e=dict(data['ctx']['e']);pristine_e=dict(e)
  saved=(root/'results/hf01-correspondence.json').read_bytes();old=json.loads((root/'original/results/recovery-field-correspondence.json').read_bytes())
  observed,capture,row=check('legitimate semantic validation',lambda:m.connected_recovery(data,cat))
  bundle=check('legitimate derivation exact saved bytes',lambda:m.derive_recovery(data,cat));check('derived bytes equal saved receipt',lambda:canonical(bundle)==saved)
  answer=check('legitimate public validation',lambda:m.validate(root,saved))
  export=json.loads(e['evidence/recovery-export-0.json']);state=json.loads(bytes.fromhex(export['head']));trace=json.loads(e['evidence/execution-trace.json'])['events']
  recovery_calls=[t for t in trace if t['event']=='call' and t['function']=='ManagedAuthority.recover'];assert len(recovery_calls)==1
  call=recovery_calls[0];ret=next(t for t in trace if t['event']=='return' and t['frame']==call['frame'])
  for i,ctx in enumerate(bundle['contexts']):
   name=ctx['context'];binding=ctx['hf01_evidence_binding'];r=ctx['saved_recovery_fields'][0]
   check('preserved entire predecessor context '+name,lambda ctx=ctx,i=i:all(canonical(ctx[k])==canonical(v) for k,v in old['contexts'][i].items()))
   check('independent recovery frame and exact value '+name,lambda r=r: r['frame']==call['frame'] and r['parent']==call['parent'] and {f['name']:f['value'] for f in r['fields']}=={k:ret['value'][k] for k in ('head','recovery_only','new_attempt_authorized')})
   check('exact boolean types and source constants '+name,lambda r=r:all(type(f['value']) is bool and f['value'] is (f['name']=='recovery_only') for f in r['fields'] if f['name']!='head'))
   check('same evidence trace acquisition occurrence and instance '+name,lambda ctx=ctx,b=binding,r=r: b['trace_identity']==r['trace_identity']==identity(e['evidence/execution-trace.json']) and b['head_record']['acquisition']==b['occurrence']['call']['acquisition'] and b['occurrence']['id']==r['occurrence'] and b['instance']==r['instance'] and any(x['occurrence']==r['occurrence'] and x['trace_identity']==r['trace_identity'] for x in ctx['saved_reference_scope']))
   check('independent exact HEAD member binding '+name,lambda b=binding:{k:b['head_record'][k] for k in ('bytes','sha256')}==identity(e['evidence/recovery-export-0.json']) and b['head_record']['pointer']=='/head' and b['head_declaration']['template_id']=='HEAD:')
  check('both declared context identities and ordering',lambda:[c['context'] for c in bundle['contexts']]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
  check('missing observations are not invented',lambda:not capture['scalar_return_recorded'] and all(f['head_relation'] is None or f['head_relation']['validator_scalar_pointer'] is None and f['head_relation']['state_or_ingest_frame'] is None for f in row['fields']) and bundle['new_recovery_slice_limits']['observer_frame'] is None)
  altered,changes=substitute(e,'1'+'0'*63)
  folder=root/'retained/review/head-witness-primary/mutated'
  check('independently reconstructed original seven-report witness exact',lambda:len(changes)==7 and sum(len(v['changed_offsets']) for v in changes.values())==128 and all((folder/n).read_bytes()==altered[n] for n in changes))
  (out/'original-witness-changes.json').write_text(json.dumps(changes,indent=2)+'\n')
  for n in changes:
   p=out/'original-witness'/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(altered[n])
  reject('original witness semantic',lambda:m.connected_recovery(data,cat,altered),'HF01-HEAD-EXPECTED-STATE')
  reject('original witness derivation',lambda:m.derive_recovery(data,cat,altered),'HF01-HEAD-EXPECTED-STATE')
  reject('original mixed receipt public rejection retained',lambda:m.validate(root,(root/'retained/review/head-witness-primary/altered-derived-receipt.json').read_bytes()),'STALE-OR-ALTERED-RECOVERY-CORRESPONDENCE')
  if not a.recovered:
   adjacent,adj_changes=substitute(e,'0'*63+'a')
   reject('adjacent last-digit coordinated substitution semantic',lambda:m.connected_recovery(data,cat,adjacent),'HF01-HEAD-EXPECTED-STATE')
   reject('adjacent last-digit coordinated substitution derivation',lambda:m.derive_recovery(data,cat,adjacent),'HF01-HEAD-EXPECTED-STATE')
   (out/'adjacent-substitution.json').write_text(json.dumps(adj_changes,indent=2)+'\n')
  substituted_data=dict(data);substituted_data['ctx']=dict(data['ctx']);substituted_data['ctx']['e']=altered
  reject('caller baseline plus reports cannot alter semantic expectation',lambda:m.connected_recovery(substituted_data,cat),'HF01-HEAD-EXPECTED-STATE')
  if not a.recovered:reject('caller baseline plus reports cannot alter derivation expectation',lambda:m.derive_recovery(substituted_data,cat),'HF01-HEAD-EXPECTED-STATE')
  missing=dict(e);del missing['evidence/session-records/binding.json']
  reject('missing instance binding semantic',lambda:m.connected_recovery(data,cat,missing))
  reject('missing instance binding derivation',lambda:m.derive_recovery(data,cat,missing))
  if not a.recovered:
   mixed=dict(e);mixed['evidence/execution-trace.json']=altered['evidence/execution-trace.json']
   reject('mixed acquisition reports semantic',lambda:m.connected_recovery(data,cat,mixed))
   reject('mixed acquisition reports derivation',lambda:m.derive_recovery(data,cat,mixed))
   stale_data=dict(data);stale_data['ctx']=dict(data['ctx']);stale_data['ctx']['binding']=copy.deepcopy(data['ctx']['binding']);stale_data['ctx']['binding']['unexpected']='substituted'
   reject('stale caller boundary cannot replace current basis',lambda:m.connected_recovery(stale_data,cat),'HF01-SOURCE-AND-BOUNDARY-BASIS')
  basis=m._validated_predecessor_basis(data)
  reject('value comparison rejects before whole-map identities',lambda:m._bind_predecessor_evidence(basis,altered,observed,cat),'HF01-HEAD-EXPECTED-STATE',category='internal_relation')
  if not a.recovered:
   def relation(label,edit,reason):
    candidate=copy.deepcopy(export);edit(candidate);reject(label,lambda:m._compare_validated_head(candidate,export,'head'),reason,category='internal_relation')
   relation('changed decoded selector',lambda x:x.update(head=canonical(dict(state,head='f'*64)).hex()),'HF01-HEAD-STATE-SELECTOR')
   relation('changed non-head state',lambda x:x.update(head=canonical(dict(state,seq=123)).hex()),'HF01-COMPLETE-VALIDATED-STATE')
   relation('same state altered exact bytes',lambda x:x.update(head=(bytes.fromhex(x['head'])+b'\n').hex()),'HF01-EXACT-VALIDATED-STATE-BYTES')
   relation('duplicate parsed head cannot hide different raw bytes',lambda x:x.update(head=(b'{"head":"bogus",'+bytes.fromhex(x['head'])[1:]).hex()),'HF01-EXACT-VALIDATED-STATE-BYTES')
   relation('changed configuration',lambda x:x.update(config={'other':True}),'HF01-CONFIGURATION-BASIS')
   relation('changed ownership representation',lambda x:x.update(ownership_meta='00'),'HF01-OWNERSHIP-BASIS')
   relation('integer cannot equal boolean head expectation',lambda x:x.update(expected_head=0),'HF01-HEAD-EXPECTED-STATE')
   for idx in (0,1):
    for label,edit in [('instance',lambda c:c['instance'].clear()),('occurrences',lambda c:c['occurrences'].clear()),('context name',lambda c:c.update(context='SYMBOLIC-U-THREE')),('record join',lambda c:c['record_declaration_joins'].clear())]:
     bad=copy.deepcopy(observed);edit(bad['contexts'][idx]);reject(f'internal binding altered {label} context {idx}',lambda bad=bad:m._bind_predecessor_evidence(basis,e,bad,cat),'HF01-ACQUISITION-INSTANCE-OCCURRENCE-BASIS',category='internal_relation')
   absent=dict(e);absent.pop('MANIFEST.json');reject('internal missing evidence member',lambda:m._bind_predecessor_evidence(basis,absent,observed,cat),'HF01-EVIDENCE-MEMBERSHIP',category='internal_relation')
   extra=dict(e);extra['invented.json']=b'{}';reject('internal invented member',lambda:m._bind_predecessor_evidence(basis,extra,observed,cat),'HF01-EVIDENCE-MEMBERSHIP',category='internal_relation')
   changed=dict(e);changed['MANIFEST.json']+=b' ';reject('internal unused evidence byte substitution',lambda:m._bind_predecessor_evidence(basis,changed,observed,cat),'HF01-EVIDENCE-BYTES:MANIFEST.json',category='internal_relation')
   for context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
    for value in ('f'*64,'', '\u03bb\x00\n'+'z'*20001):
     x=copy.deepcopy(export);x['expected_head']=value;x['head']=canonical(dict(state,head=value)).hex()
     check('constructed equal nonzero/empty/unbounded premise '+context+' '+str(len(value)),lambda x=x:m._compare_validated_head(x,x,'head'),'constructed_only')
     constructed.append({'context':context,'head':value,'authenticated':False,'runtime_observation':False,'new_limit':False})
  for idx in (0,1):
   bad=copy.deepcopy(bundle);bad['contexts'][idx]['hf01_evidence_binding']['head_record'].clear()
   reject('public missing head binding context '+str(idx),lambda bad=bad:m.validate(root,canonical(bad)),'STALE-OR-ALTERED-RECOVERY-CORRESPONDENCE',category='public_negative')
  if not a.recovered:
   bad=copy.deepcopy(bundle)
   for c in bad['contexts']:
    c['saved_recovery_fields'][0]['fields'][0]['value']='f'*64;c['hf01_evidence_binding']['occurrence']['observed_local_values']['managed-local:recovery-result']['head']='f'*64
   reject('coordinated false public receipt both contexts',lambda:m.validate(root,canonical(bad)),'STALE-OR-ALTERED-RECOVERY-CORRESPONDENCE',category='public_negative')
   for label,edit in [('missing context',lambda b:b['contexts'].pop()),('duplicated context',lambda b:b['contexts'].__setitem__(1,copy.deepcopy(b['contexts'][0]))),('stale predecessor',lambda b:b['prior_reference_receipt'].update(sha256='0'*64)),('status escalation',lambda b:b['new_recovery_slice_limits'].update(actual_admission=True,readiness='READY',all_eleven_obligations_preserved=False))]:
    bad=copy.deepcopy(bundle);edit(bad);reject('public '+label,lambda bad=bad:m.validate(root,canonical(bad)),'STALE-OR-ALTERED-RECOVERY-CORRESPONDENCE',category='public_negative')
  # Returned data must never become the next invocation's expectation.
  answer['contexts'].reverse();answer['receipt'].clear();observed['contexts'][0]['occurrences'].clear();observed['contexts'][1]['instance'].clear();capture.clear();row['fields'].clear()
  basis['prior']['contexts'].clear();basis['observed']['contexts'].clear();basis['evidence'].clear();basis['bindings'].clear()
  bundle['contexts'].reverse()
  for c in bundle['contexts']:c['hf01_evidence_binding']['occurrence'].clear();c['saved_recovery_fields'][0]['instance'].clear()
  check('semantic pristine after all nested mutations',lambda:m.connected_recovery(data,cat))
  check('derivation unchanged after all nested mutations',lambda:canonical(m.derive_recovery(data,cat))==saved)
  check('public pristine after all nested mutations',lambda:m.validate(root,saved))
  reject('mutated returned receipt cannot be accepted',lambda:m.validate(root,canonical(bundle)),'STALE-OR-ALTERED-RECOVERY-CORRESPONDENCE',category='public_negative')
  check('candidate evidence not repaired or mutated',lambda:data['ctx']['e']==pristine_e and altered!=pristine_e)
  check('current predecessor actually invoked',lambda:any(r['event']=='mandatory predecessor consumes evidence' and r['export']==identity(e['evidence/recovery-export-0.json']) for r in profile_rows))
  check('observed head comparison uses original independent expectation',lambda:any(r['event']=='head value comparison' and r['candidate']=='1'+'0'*63 and r['expected']=='0'*64 for r in profile_rows))
  check('source bytes unchanged',lambda:source=={n:identity((root/'code'/n).read_bytes()) for n in source})
 except BaseException as ex:
  error={'type':type(ex).__name__,'message':str(ex)};(out/'failure.txt').write_text(traceback.format_exc());raise
 finally:
  sys.setprofile(None)
  (out/'constructed-premises.json').write_text(json.dumps(constructed,indent=2)+'\n');(out/'call-observations.json').write_text(json.dumps(profile_rows,indent=2)+'\n')
  result={'result':'PASS' if error is None else 'FAIL','assertions':len(rows),'categories':{k:sum(r['category']==k for r in rows) for k in sorted({r['category'] for r in rows})},'checks':rows,'failure':error,'root':str(root),'recovered':a.recovered,'environment':{'python':sys.version,'optimization':sys.flags.optimize,'cryptography_installed':importlib.metadata.version('cryptography')},'source':locals().get('source'),'no_runtime_session_database_operations':True,'no_completed_review_rerun':True}
  (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PASS',len(rows),'fresh independent HF-01 controls')
if __name__=='__main__':main()
