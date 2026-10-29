"""Mandatory normal _run token correspondence over the reviewed IS-01 chain.
Saved evidence only. No application method or database connection is invoked.
"""
import copy,hashlib,json,os,stat,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 205451, 'sha256': '4d485ad7df99bf6d0cd05c41d7091f126090eadc9ebcff39a80e1d25e623e5bc'}
PREDECESSOR_MANIFEST={'bytes':525136,'sha256':'ee20ab983c00fda52e6ada13ba8f34aec6aaf94ea3980c69da98fd34f42f4b2c'}
PREDECESSOR_RECEIPT={'bytes':2776568,'sha256':'4db6c9d4da0110055f483fdf5ef958a12edd9362b8315704ff0cf5143470c468'}
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
 root=Path(root);base=root/'retained/status'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'TOKEN-ROOT-TYPE')
 mp=base/'MANIFEST.json';require(stat.S_ISREG(mp.lstat().st_mode),'TOKEN-MANIFEST-TYPE');raw=mp.read_bytes();require(identity(raw)==PREDECESSOR_MANIFEST,'TOKEN-PREDECESSOR-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'TOKEN-UNDECLARED-DIRECTORY');seen.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'TOKEN-UNDECLARED-OR-NONREGULAR');files.add(n)
 walk(base);require(files==expected and seen==dirs,'TOKEN-PREDECESSOR-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'TOKEN-PREDECESSOR-BYTES:'+n)
 return base
def inputs(root=ROOT):
 root=Path(root);base=predecessor_root(root);path=root/'code/managed_coverage.py';require(stat.S_ISREG(path.lstat().st_mode),'TOKEN-PRODUCER-TYPE');require(identity(path.read_bytes())==PRODUCER_PIN,'TOKEN-PRODUCER-PIN')
 prior=module(base/'code/correspondence.py','_token_status_predecessor');return {'root':root,'prior_root':base,'prior_module':prior,'prior_data':prior.inputs(base),'coverage':module(path,'_token_coverage')}
def inner(data):return data['prior_module'].inner(data['prior_data'])
def sources(data):return data['prior_module'].sources(data['prior_data'])
def dependencies(data):
 p=data['prior_module'];pd=data['prior_data'];status=p.catalogue(pd)
 state=pd['prior_module'];sd=pd['prior_data'];client=sd['prior_module'].catalogue(sd['prior_data'])
 return status,client

def catalogue(data):return data['coverage'].compile_token_registration(*sources(data),*dependencies(data),inner(data)['ctx']['binding'])
def _basis(data):
 fresh=inputs(data['root']);p=fresh['prior_module'];pd=fresh['prior_data'];prior=p.derive_status(pd,p.catalogue(pd))
 saved=(fresh['prior_root']/'results/fresh/corrected-receipt.json').read_bytes();require(identity(saved)==PREDECESSOR_RECEIPT and enc(prior)==saved,'TOKEN-VALIDATED-PREDECESSOR-RECEIPT')
 return {'fresh':fresh,'prior':prior,'saved':saved,'catalogue':catalogue(fresh),'evidence':dict(inner(fresh)['ctx']['e'])}
def _rows(basis):
 rows=[];cat=basis['catalogue'];require(tuple(c['context'] for c in basis['prior']['contexts'])==CONTEXTS,'TOKEN-CONTEXT-DOMAIN')
 for context in basis['prior']['contexts']:
  status=context['internal_status_return_correspondence'];anchor=status['instance_anchor']
  same(anchor,context['client_state_return_correspondence']['validated_state_anchor'],'TOKEN-VALIDATED-INSTANCE')
  same(status['declaration']['source']['sources']['entry'],cat['source']['entry'],'TOKEN-VALIDATED-SOURCE')
  rows.append({'context':context['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(anchor),'predecessor_receipt':identity(basis['saved']),
   'reference_basis':copy.deepcopy(status['validated_reference_basis']),
   'conditional_links':[{'declaration':d['id'],'source_origin':copy.deepcopy(d['source_origin']),'invocation':None,'frame':None,'observed_value':None} for d in cat['declarations']],
   'scope':{'context':context['context'],'acquisition':anchor['record']['acquisition'],'instance':copy.deepcopy(anchor['instance']),'frontier':anchor['recovery_occurrence'],'invocation':None,'request_identifier':None},
   'runtime_registration_revocation_links':None,'actual_invocation_count':None,'physical_identity_observation':None,'classification':'UNKNOWN','multiplicity':None,'ordinal':None,
   'separate_observer':copy.deepcopy(status['separate_observer']),'observer_join':None,'outer_lifecycle_complete':False,
   'gap':'No _run token/owner creation, registry insertion, callback completion, finally-entry or pop-attempt/completion runtime frames. Selected finite cases remain constructed; exceptional/cleanup continuations remain partial.'})
 return rows
def _check_rows(basis,claims):
 exact(claims,'TOKEN-SEMANTIC-CLAIMS');want=_rows(basis)
 require(type(claims) is list and len(claims)==2,'TOKEN-CLAIM-CONTEXT-DOMAIN');same(claims,want,'TOKEN-SEMANTIC-CORRESPONDENCE')
def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'TOKEN-EVIDENCE-TYPES')
 # Compare to the actual validated predecessor's complete evidence, not to a
 # set of mutually agreeing candidate reports or their claimed archive pins.
 require(candidate==basis['evidence'],'TOKEN-VALIDATED-EVIDENCE')
def _checked(data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'TOKEN-CATALOGUE');exact(claims,'TOKEN-CLAIMS')
 basis=_basis(data);same(submitted_catalogue,basis['catalogue'],'TOKEN-CATALOGUE-SOURCE')
 d=inner(data);fd=inner(basis['fresh']);require(all(type(x) is bytes for x in sources(data)) and type(d['manager']) is bytes and type(d['ctx']['c']) is dict and all(type(k) is str and type(v) is bytes for k,v in d['ctx']['c'].items()),'TOKEN-CANDIDATE-SOURCE-TYPES')
 require(sources(data)==sources(basis['fresh']) and d['manager']==fd['manager'] and d['ctx']['c']==fd['ctx']['c'],'TOKEN-CANDIDATE-SOURCE');same(d['ctx']['binding'],fd['ctx']['binding'],'TOKEN-CANDIDATE-BINDING')
 _compare_evidence(basis,d['ctx']['e'] if evidence is None else evidence)
 if claims is not None:_check_rows(basis,claims)
 return _rows(basis),basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def _assemble(data,rows,basis):
 _check_rows(basis,rows)
 result=copy.deepcopy(basis['prior']);result['format']='I164-TOKEN-REGISTRATION-CORRESPONDENCE-1';result['prior_internal_status_components']=result.pop('extension_components');result['prior_internal_status_receipt']=identity(basis['saved']);result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(result['contexts'],rows):ctx['token_registration_correspondence']=copy.deepcopy(row)
 result['new_token_registration_limits']={'normal_conditional_slice':True,'runtime_registration_revocation':'UNAVAILABLE','observer_join':None,'physical_identity':None,'outer_lifecycle_complete':False,'registry_continuity_is_explicit_conditional_premise':True,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False}
 return result
def derive_token(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);return _assemble(data,rows,basis)
def invocation_scope(anchor,invocation):
 exact(anchor,'TOKEN-ANCHOR');exact(invocation,'TOKEN-INVOCATION');require(type(invocation) is str and bool(invocation),'TOKEN-INVOCATION')
 return {'context':anchor['context'],'acquisition':anchor['record']['acquisition'],'instance':copy.deepcopy(anchor['instance']),'frontier':anchor['recovery_occurrence'],'invocation':invocation}
def _construct_checked(basis,case):
 exact(case,'TOKEN-CONSTRUCTED-INPUT');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','control_present','owner_failure_none','registry_continuity','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-TOKEN-REGISTRATION','TOKEN-CONSTRUCTED-CASE')
 rows=_rows(basis);selected=[r for r in rows if r['context']==case['context']];require(len(selected)==1,'TOKEN-CONSTRUCTED-CONTEXT');anchor=selected[0]['instance_anchor'];same(case['anchor'],anchor,'TOKEN-CONSTRUCTED-ANCHOR')
 scope=invocation_scope(anchor,case['invocation']);validated={'occurrence':case['invocation'],'scope':scope,**{k:copy.deepcopy(case[k]) for k in ('control_present','owner_failure_none','registry_continuity','outcomes')}}
 c=basis['fresh']['coverage'];p=c.token_registration_projection(basis['catalogue'],case['projection'],validated)
 c.validate_token_registration_projection(basis['catalogue'],case['projection'],validated,case['output'])
 return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(anchor),'projection':p,'premises':'Explicit finite constructed outcomes and registry continuity, source-derived references; selected acquisition frontier is not runtime execution evidence','runtime_observation':False}
def constructed_projection(data,submitted_catalogue,case):
 exact(case,'TOKEN-CONSTRUCTED-INPUT');_,basis=_checked(data,submitted_catalogue);return _construct_checked(basis,case)
def derive(root=ROOT):
 data=inputs(root);return derive_token(data,catalogue(data))
def validate(root,saved):
 require(type(saved) is bytes,'TOKEN-RECEIPT-BYTES');v=json.loads(saved);require(type(v) is dict and v.get('format')=='I164-TOKEN-REGISTRATION-CORRESPONDENCE-1' and type(v.get('contexts')) is list and len(v['contexts'])==2 and all(type(c) is dict and 'token_registration_correspondence' in c for c in v['contexts']),'TOKEN-MANDATORY-RELATION')
 require(saved==enc(derive(root)),'TOKEN-STALE-OR-ALTERED-RECEIPT');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(saved),'runtime_registration_revocation':'UNAVAILABLE','actual_admission':False}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
