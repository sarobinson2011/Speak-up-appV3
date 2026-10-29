"""Mandatory bounded normal session-exit correspondence over the reviewed token chain.
Saved evidence only. No application method or database connection is invoked.
"""
import copy,hashlib,json,os,stat,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 216678, 'sha256': 'dc0217d5395de31fc2f72c456a7b156116652b8c9d395a4931e631a7342861c8'}
PREDECESSOR_MANIFEST={'bytes':577591,'sha256':'37bed36d549e530632d0939e379f53a49815a3145f30e13d49256de08397bf6a'}
PREDECESSOR_RECEIPT={'bytes':3328177,'sha256':'1184bbf9366a2c7a8ced902836566b6610a8844cbf97698e78d10e6e91107145'}
CONTEXTS=('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO')
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def require(ok,code):
 if not ok:raise ValueError(code)
def exact(value,code):
 stack=[(value,False)];active=set()
 while stack:
  node,leave=stack.pop();kind=type(node)
  if leave:active.remove(id(node));continue
  if kind is dict or kind is list:
   require(id(node) not in active,code+':CYCLE');active.add(id(node));stack.append((node,True))
   if kind is dict:
    for k,v in node.items():require(type(k) is str,code+':KEY-TYPE');stack.append((v,False))
   else:
    for v in node:stack.append((v,False))
  else:require(any(kind is t for t in (str,int,bool,float,type(None))),code+':VALUE-TYPE')
def same(a,b,code):exact(a,code);exact(b,code);require(enc(a)==enc(b),code)
def module(p,name):
 m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def predecessor_root(root):
 root=Path(root);base=root/'retained/token'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'EXIT-ROOT-TYPE')
 mp=base/'MANIFEST.json';require(stat.S_ISREG(mp.lstat().st_mode),'EXIT-MANIFEST-TYPE');raw=mp.read_bytes();require(identity(raw)==PREDECESSOR_MANIFEST,'EXIT-PREDECESSOR-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'EXIT-UNDECLARED-DIRECTORY');seen.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'EXIT-UNDECLARED-OR-NONREGULAR');files.add(n)
 walk(base);require(files==expected and seen==dirs,'EXIT-PREDECESSOR-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'EXIT-PREDECESSOR-BYTES:'+n)
 return base
def inputs(root=ROOT):
 root=Path(root);base=predecessor_root(root);path=root/'code/managed_coverage.py';require(stat.S_ISREG(path.lstat().st_mode),'EXIT-PRODUCER-TYPE');require(identity(path.read_bytes())==PRODUCER_PIN,'EXIT-PRODUCER-PIN')
 prior=module(base/'code/correspondence.py','_exit_token_predecessor');return {'root':root,'prior_root':base,'prior_module':prior,'prior_data':prior.inputs(base),'coverage':module(path,'_exit_coverage')}
def inner(data):return data['prior_module'].inner(data['prior_data'])
def sources(data):return (*data['prior_module'].sources(data['prior_data']),inner(data)['manager'])
def dependencies(data):
 p=data['prior_module'];d=inner(data);v=d['values'];g=d['guards'];c=data['coverage']
 return p.catalogue(data['prior_data']),c.compile_reference_transfers(d['manager'],v['candidate/managed-route/model.json'],v['candidate/managed-route/producers.json'],g['guard_relationships'],g['guard_oracle'],d['authority'])
def catalogue(data):return data['coverage'].compile_session_exit(*sources(data),*dependencies(data))
def _basis(data):
 fresh=inputs(data['root']);p=fresh['prior_module'];pd=fresh['prior_data']
 # These are exactly derive_token's validation and assembly, executed once.
 # Retaining its validated basis permits selected invocation checking against
 # the same evidence without taking expectations from candidate reports.
 rows,tb=p._checked(pd,p.catalogue(pd));prior=p._assemble(pd,rows,tb)
 saved=(fresh['prior_root']/'results/primary/token-registration-correspondence.json').read_bytes();require(identity(saved)==PREDECESSOR_RECEIPT and enc(prior)==saved,'EXIT-VALIDATED-PREDECESSOR-RECEIPT')
 return {'fresh':fresh,'prior':prior,'saved':saved,'token_basis':tb,'catalogue':catalogue(fresh),'evidence':dict(inner(fresh)['ctx']['e'])}
def session_binding(basis,anchor):
 e=basis['evidence'];start='evidence/SMOKE-ABOUT-TO-START.json';binding='evidence/session-records/binding.json';s=json.loads(e[start]);b=json.loads(e[binding]);require(type(s['destination']) is str,'EXIT-DESTINATION-TYPE')
 require(b['configuration']['config']['session']==anchor['instance']['session_label'],'EXIT-SESSION-INSTANCE');same(b['launcher'],basis['catalogue']['source']['launcher'],'EXIT-SESSION-SOURCE')
 return {'acquisition':anchor['record']['acquisition'],'instance':copy.deepcopy(anchor['instance']),'recorded_destination':s['destination'],'start_record':{'path':start,'identity':identity(e[start]),'pointer':'/destination'},'binding_record':{'path':binding,'identity':identity(e[binding]),'pointer':'/configuration/config/session'},'source_owner_lock':copy.deepcopy(basis['catalogue']['source']['owner_lock_destination']),'physical_resolved_destination':None,'resolution':'owner_lock yields dest after parent.resolve(); recorded destination is nominal, no host resolution performed'}
def marker_path(basis,anchor,scope):
 sb=session_binding(basis,anchor);component=basis['catalogue']['source']['marker_component']
 return {'kind':'SOURCE-QUALIFIED-SESSION-MARKER','scope':copy.deepcopy(scope),'session_binding':sb,'root':'owner-lock-yielded-dest','component':component,'expression':basis['catalogue']['source']['marker_expression'],'nominal_recorded_path':sb['recorded_destination'].rstrip('/')+'/'+component,'physical_resolved_path':None}
def _rows(basis):
 cat=basis['catalogue'];rows=[];require(tuple(r['context'] for r in basis['prior']['contexts'])==CONTEXTS,'EXIT-CONTEXT-DOMAIN')
 for row in basis['prior']['contexts']:
  token=row['token_registration_correspondence'];anchor=token['instance_anchor'];same(token['declaration']['source']['entry'],cat['source']['entry'],'EXIT-VALIDATED-ENTRY');same(row['reference_declarations']['source']['source']['sha256'],cat['source']['manager']['sha256'],'EXIT-VALIDATED-MANAGER')
  scope=copy.deepcopy(token['scope']);scope.pop('request_identifier');path='evidence/confirmed-close.json';closed=json.loads(basis['evidence'][path])
  rows.append({'context':row['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(anchor),'predecessor_receipt':identity(basis['saved']),'scope':scope,'session_binding':session_binding(basis,anchor),'marker_path':marker_path(basis,anchor,scope),
   'reference_basis':copy.deepcopy(token['reference_basis']),'conditional_links':[{'declaration':d['id'],'source_origin':copy.deepcopy(d['source_origin']),'invocation':None,'frame':None,'observed_value':None} for d in cat['declarations']],
   'saved_close_evidence':{'path':path,'identity':identity(basis['evidence'][path]),'value':closed,'join_to_selected_constructed_invocation':None,'meaning':'Predecessor-validated saved manager close and marker observations; not runtime token-pop/local-clear/unlink forwarding frames'},
   'selected_owner_continuity':'Explicit constructed premise, not runtime exclusivity','runtime_exit_chain':None,'physical_identity_observation':None,'actual_invocation_count':None,'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'observer_join':None,'separate_observer':copy.deepcopy(token['separate_observer']),'outer_lifecycle_complete':False,
   'gap':'No runtime normal-pop to selected launcher close/local clear/unlink chain; path resolution, physical identity, durability, exceptional/outer cleanup and continuity remain unestablished.'})
 return rows
def _check_rows(basis,claims):
 exact(claims,'EXIT-SEMANTIC-CLAIMS');require(type(claims) is list and len(claims)==2,'EXIT-CLAIM-CONTEXT-DOMAIN');same(claims,_rows(basis),'EXIT-SEMANTIC-CORRESPONDENCE')
def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'EXIT-EVIDENCE-TYPES');require(candidate==basis['evidence'],'EXIT-VALIDATED-EVIDENCE')
def _checked(data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'EXIT-CATALOGUE');exact(claims,'EXIT-CLAIMS');basis=_basis(data);same(submitted_catalogue,basis['catalogue'],'EXIT-CATALOGUE-SOURCE')
 d=inner(data);fd=inner(basis['fresh']);require(all(type(x) is bytes for x in sources(data)) and type(d['ctx']['c']) is dict and all(type(k) is str and type(v) is bytes for k,v in d['ctx']['c'].items()),'EXIT-CANDIDATE-SOURCE-TYPES');require(sources(data)==sources(basis['fresh']) and d['ctx']['c']==fd['ctx']['c'],'EXIT-CANDIDATE-SOURCE');same(d['ctx']['binding'],fd['ctx']['binding'],'EXIT-CANDIDATE-BINDING')
 _compare_evidence(basis,d['ctx']['e'] if evidence is None else evidence)
 if claims is not None:_check_rows(basis,claims)
 return _rows(basis),basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def _assemble(data,rows,basis):
 _check_rows(basis,rows);result=copy.deepcopy(basis['prior']);result['format']='I164-NORMAL-SESSION-EXIT-CORRESPONDENCE-1';result['prior_token_components']=result.pop('extension_components');result['prior_token_receipt']=identity(basis['saved']);result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(result['contexts'],rows):ctx['normal_session_exit_correspondence']=copy.deepcopy(row)
 result['new_normal_exit_limits']={'normal_conditional_slice':True,'runtime_exit_chain':'UNAVAILABLE','observer_join':None,'physical_identity':None,'durability':None,'outer_lifecycle_complete':False,'registry_continuity_is_explicit_conditional_premise':True,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False};return result
def derive_exit(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);return _assemble(data,rows,basis)
def close_scope(anchor,invocation):return {'acquisition':anchor['record']['acquisition'],'instance':'validated-instance:'+hashlib.sha256(enc(anchor['instance'])).hexdigest(),'invocation':invocation+'/managed-close'}
def _premises(basis,case):
 exact(case,'EXIT-CONSTRUCTED-INPUT');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','token_case','close_case','outcomes','marker_at_unlink','projection','output'} and case['kind']=='CONSTRUCTED-NORMAL-SESSION-EXIT','EXIT-CONSTRUCTED-CASE')
 selected=[r for r in _rows(basis) if r['context']==case['context']];require(len(selected)==1,'EXIT-CONSTRUCTED-CONTEXT');anchor=selected[0]['instance_anchor'];same(case['anchor'],anchor,'EXIT-CONSTRUCTED-ANCHOR')
 p=basis['fresh']['prior_module'];tc=case['token_case'];same({k:tc[k] for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'EXIT-TOKEN-INVOCATION');token=p._construct_checked(basis['token_basis'],tc)['projection'];scope=p.invocation_scope(anchor,case['invocation'])
 cc=case['close_case'];cr=None
 if cc is not None:
  require(type(cc) is dict,'EXIT-CLOSE-CASE');same(cc['scope'],close_scope(anchor,case['invocation']),'EXIT-CLOSE-SCOPE');require(cc['context']==case['context'] and cc['method']=='close','EXIT-CLOSE-RECEIVER-METHOD')
  d=inner(basis['fresh']);g=d['guards'];cr=basis['fresh']['coverage'].constructed_reference_path(d['manager'],g['guard_relationships'],g['guard_oracle'],cc)
 return {'scope':scope,'references':copy.deepcopy(token['reference_bindings']),'session_binding':session_binding(basis,anchor),'marker_path':marker_path(basis,anchor,scope),'token_result':token,'close_result':cr,'outcomes':copy.deepcopy(case['outcomes']),'marker_at_unlink':case['marker_at_unlink']}
def _construct_checked(basis,case):
 v=_premises(basis,case);c=basis['fresh']['coverage'];cat=basis['catalogue'];out=c.session_exit_projection(cat,case['projection'],v);c.validate_session_exit_projection(cat,case['projection'],v,case['output'])
 return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(case['anchor']),'projection':out,'premises':'Explicit finite constructed outcomes, close-path initial references and selected-owner continuity; evidence-qualified source references are not runtime physical identity','runtime_observation':False}
def constructed_projection(data,submitted_catalogue,case):
 exact(case,'EXIT-CONSTRUCTED-INPUT');_,basis=_checked(data,submitted_catalogue);return _construct_checked(basis,case)
def derive(root=ROOT):
 data=inputs(root);return derive_exit(data,catalogue(data))
def validate(root,saved):
 require(type(saved) is bytes,'EXIT-RECEIPT-BYTES');v=json.loads(saved);require(type(v) is dict and v.get('format')=='I164-NORMAL-SESSION-EXIT-CORRESPONDENCE-1' and type(v.get('contexts')) is list and len(v['contexts'])==2 and all(type(c) is dict and 'normal_session_exit_correspondence' in c for c in v['contexts']),'EXIT-MANDATORY-RELATION');require(saved==enc(derive(root)),'EXIT-STALE-OR-ALTERED-RECEIPT');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(saved),'runtime_exit_chain':'UNAVAILABLE','actual_admission':False}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
