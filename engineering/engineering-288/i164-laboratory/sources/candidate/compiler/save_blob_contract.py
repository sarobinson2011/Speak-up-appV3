"""Bounded Authority.sign save/blob joins, independently rooted in authenticated input.

No capture hash gate. This is a source-pinned pure model of the admitted save
expressions, not execution of runtime source or an oracle built from observations.
Unsupported expressions fail closed. Caller exception propagation remains outside.
"""
import ast,copy,hashlib,json
from observation_contract import AUTH,raw_source,fn,position,call_node,need,exact
from value_observer import untyped

def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def ev(n,env):
 if isinstance(n,ast.Constant):return n.value
 if isinstance(n,ast.Name) and n.id in env:return env[n.id]
 if isinstance(n,ast.Subscript):return ev(n.value,env)[ev(n.slice,env)]
 if isinstance(n,ast.Dict):return {ev(k,env):ev(v,env) for k,v in zip(n.keys,n.values)}
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('enc','sha') and len(n.args)==1 and not n.keywords:return {'enc':enc,'sha':sha}[n.func.id](ev(n.args[0],env))
 raise ValueError('SAVE-BLOB-UNSUPPORTED-EXPRESSION')
def check(x,root,signed):
 raw=raw_source(root,AUTH);sign=fn(raw,'Authority.sign');save=fn(raw,'Authority.save')
 # Bind the modeled mutation/order to exact defining source forms, not submitted metadata.
 saves=sorted([n for n in ast.walk(sign) if isinstance(n,ast.Call) and ast.unparse(n.func)=='self.save'],key=lambda n:(n.lineno,n.col_offset))
 blobs=[n for n in ast.walk(sign) if isinstance(n,ast.Call) and ast.unparse(n.func)=='self.blob']
 need(len(saves)==2 and len(blobs)==1,'SAVE-BLOB-SOURCE-DOMAIN')
 phases=sorted([n for n in ast.walk(sign) if isinstance(n,ast.Assign) and len(n.targets)==1 and ast.unparse(n.targets[0])=="p['phase']"],key=lambda n:(n.lineno,n.col_offset))
 need(len(phases)==2 and all(isinstance(n.value,ast.Constant) and type(n.value.value) is str for n in phases),'SAVE-PHASE-SOURCE')
 txassign=[n for n in ast.walk(sign) if isinstance(n,ast.Assign) and len(n.targets)==1 and ast.unparse(n.targets[0])=="p['tx']"]
 need(len(txassign)==1 and txassign[0].value is blobs[0] and ast.unparse(blobs[0])=='self.blob(raw)','BLOB-CALL-SOURCE')
 for n,p in zip(saves,phases):need(p.lineno<=n.lineno and not n.keywords and ast.unparse(n.args[0])=='s' and ast.unparse(n.args[1])=='r','SAVE-CALL-SOURCE')
 need(len(saves[0].args)==3 and len(saves[1].args)==4 and ast.unparse(saves[1].args[3])=="p['tx']",'SAVE-PROOF-SOURCE')
 # Source-checked pure save calculation, including the exact event encoder.
 forms=[ast.unparse(n) for n in save.body]
 for form in ['new = copy.deepcopy(s)',"previous = new.pop('head')","new['seq'] += 1","new['head'] = sha(event)"]:
  need(form in forms,'SAVE-TRANSFORM-SOURCE')
 events=[n.value for n in save.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='event' for t in n.targets)]
 need(len(events)==1 and len(save.args.defaults)==1,'SAVE-EVENT-SOURCE')
 request=json.loads(bytes.fromhex(x['request_hex']))['request'];state=json.loads(bytes.fromhex(x['input']['head']))
 p=state['u'][request['u']]['stage']['pending'];initial=copy.deepcopy(p)
 eligible=p['phase']=='DECIDED' and request['body']['action']==p['action']
 count=0;blobcount=0;expected_state=copy.deepcopy(state);frames={}
 for e in x['observations']:
  if e['source']!=AUTH or e['function'] not in ('Authority.save','Authority.blob'):continue
  vals={k:untyped(v) for k,v in e['values'].items()}
  if e['event']=='call':
   need(eligible,'SAVE-BLOB-INELIGIBLE');node=call_node(e,root)
   exact([e['caller']['source'],e['caller']['function']],[AUTH,'Authority.sign'],'SAVE-BLOB-CALLER')
   if e['function']=='Authority.blob':
    exact(position(node),position(blobs[0]),'BLOB-SOURCE-SITE');need(count==1 and blobcount==0 and type(signed) is bytes,'BLOB-PRODUCER-ORDER')
    need(type(vals['raw']) is bytes and vals['raw']==signed,'BLOB-SOURCE-RAW');frames[e['frame']]=('blob',sha(signed));blobcount+=1
   else:
    need(count<2,'SAVE-EXTRA');exact(position(node),position(saves[count]),'SAVE-SOURCE-ORDER')
    pending=expected_state['u'][request['u']]['stage']['pending']
    pending['phase']=phases[count].value.value
    if count==1:
     need(blobcount==1 and signed is not None,'SAVE-MISSING-BLOB');pending['tx']=sha(signed)
    env={'s':expected_state,'r':request,'p':pending}
    expected={'s':expected_state,'request':request,'kind':ev(node.args[2],env),'proof':ev(node.args[3],env) if len(node.args)==4 else ev(save.args.defaults[0],env)}
    for k,v in expected.items():exact(vals[k],v,'SAVE-SOURCE-ARGUMENT:'+k)
    new=copy.deepcopy(expected_state);previous=new.pop('head');new['seq']+=1
    event=ev(events[0],dict(expected,new=new,previous=previous));need(type(event) is bytes,'SAVE-EVENT-BYTES');new['head']=sha(event)
    frames[e['frame']]=('save',copy.deepcopy(new));expected_state=new;count+=1
    # If persisted, the exact modeled event must appear in authenticated output.
    if count==1 or x['inject'] in (None,'after_signature_commit'):
     need([new['seq'],event.hex()] in x['export']['events'],'SAVE-AUTHENTICATED-EVENT')
  elif e['event']=='return':
   need(e['frame'] in frames,'SAVE-BLOB-MISSING-CALL');kind,want=frames[e['frame']]
   got=untyped(e['result']);exact(got,want,'SAVE-BLOB-SOURCE-RESULT')
   if kind=='save':exact(vals['new'],want,'SAVE-SOURCE-NEW')
   else:exact(vals['ref'],want,'BLOB-SOURCE-REF')
  else:raise ValueError('SAVE-BLOB-EXCEPTION-UNSUPPORTED')
 expected_count=0 if not eligible else 1 if x['inject'] in ('after_sign_claim','after_signature_created') else 2
 need(count==expected_count and blobcount==max(0,expected_count-1),'SAVE-BLOB-MISSING-EVIDENCE')
 return True
