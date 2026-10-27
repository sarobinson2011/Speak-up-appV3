"""Bounded binding getter correspondence over the mandatory HF-01 chain.
No runtime/session operations. No getter execution is inferred from a state.
"""
import copy, hashlib, json, os, stat, types
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 83402, 'sha256': 'a626cb35ec63e7e7c50323b3db6bde4651a78c68af4ab9bc44b64cb193cb60bd'}
HF_MANIFEST={'bytes':165408,'sha256':'e485d6be8f79aa36fa178e296491e031c47bfc611fbd3daf6fb7599d630285ed'}
HF_RECEIPT={'bytes':704580,'sha256':'139d19185343c7821238faa7a9fc9b6cd91d379c32d80961ee2d490f0ab0a161'}
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def require(v,message):
 if not v:raise ValueError(message)
def same(a,b,message):require(enc(a)==enc(b),message)
def module(p,name):
 m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m

def predecessor_root(root):
 root=Path(root);base=root/'retained/hf01'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'BINDING-ROOT-TYPE')
 manifest_path=base/'MANIFEST.json';require(stat.S_ISREG(manifest_path.lstat().st_mode),'BINDING-MANIFEST-TYPE');raw=manifest_path.read_bytes()
 require(identity(raw)==HF_MANIFEST,'BINDING-PREDECESSOR-MANIFEST');manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'}
 dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};seen=set();seen_dirs=set()
 def walk(path):
  for entry in os.scandir(path):
   q=Path(entry.path);n=q.relative_to(base).as_posix();mode=entry.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'BINDING-UNDECLARED-DIRECTORY');seen_dirs.add(n);walk(q)
   else:require(stat.S_ISREG(mode) and n in expected,'BINDING-UNDECLARED-OR-NONREGULAR');seen.add(n)
 walk(base);require(seen==expected and seen_dirs==dirs,'BINDING-PREDECESSOR-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'BINDING-PREDECESSOR-BYTES:'+n)
 return base

def inputs(root=ROOT):
 root=Path(root);base=predecessor_root(root)
 producer=root/'code/managed_coverage.py';require(stat.S_ISREG(producer.lstat().st_mode),'BINDING-PRODUCER-TYPE');require(identity(producer.read_bytes())==PRODUCER_PIN,'BINDING-PRODUCER-SOURCE')
 prior=module(base/'code/correspondence.py','_binding_hf01_predecessor')
 data=prior.recovery_inputs(base)
 return {'root':root,'prior_root':base,'prior_module':prior,'prior_data':data,'coverage':module(producer,'_binding_managed_coverage')}

def catalogue(data):
 d=data['prior_data'];v=d['values'];g=d['guards'];m=data['coverage']
 refs=d['reference_module'].reference_catalogue(d)
 return m.compile_binding_return(d['manager'],d['authority'],v['candidate/managed-route/model.json'],v['candidate/managed-route/producers.json'],g['guard_relationships'],g['guard_oracle'],refs)

def _basis(data):
 # Only the root selector is taken from the caller. Reload all authoritative
 # sources and evidence, and invoke the mandatory reviewed predecessor afresh.
 # Nothing mutable returned by this module is a cached expectation.
 fresh=inputs(data['root']);d=fresh['prior_data'];p=fresh['prior_module']
 prior=p.derive_recovery(d,p.recovery_catalogue(d))
 saved=(fresh['prior_root']/'results/hf01-correspondence.json').read_bytes()
 require(identity(saved)==HF_RECEIPT,'BINDING-PREDECESSOR-RECEIPT-PIN');require(enc(prior)==saved,'BINDING-PREDECESSOR-RECEIPT')
 e=dict(d['ctx']['e']);require(all(type(k) is str and type(v) is bytes for k,v in e.items()),'BINDING-EVIDENCE-BYTES')
 return {'fresh':fresh,'prior':prior,'saved':saved,'evidence':e,'catalogue':catalogue(fresh)}

def _compare_evidence(expected,candidate,selector):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'BINDING-EVIDENCE-BYTES')
 path='evidence/recovery-export-0.json';require(path in candidate,'BINDING-MISSING-EXPORT')
 a=json.loads(candidate[path]);b=json.loads(expected[path]);ar=bytes.fromhex(a['head']);br=bytes.fromhex(b['head']);astate=json.loads(ar);bstate=json.loads(br)
 require(type(astate) is dict and selector in astate,'BINDING-MISSING-STATE-VALUE')
 require(type(astate[selector]) is str,'BINDING-STATE-VALUE-TYPE')
 same(astate[selector],bstate[selector],'BINDING-VALIDATED-INSTANCE-VALUE')
 same(astate,bstate,'BINDING-VALIDATED-STATE');same(a['config'],b['config'],'BINDING-VALIDATED-CONFIG');same(a['ownership_meta'],b['ownership_meta'],'BINDING-VALIDATED-OWNERSHIP')
 require(ar==br,'BINDING-VALIDATED-STATE-BYTES')
 # Semantic binding/state comparison precedes this exact record gate. A set
 # of mutually consistent substituted reports cannot authorize its own basis.
 require(set(candidate)==set(expected),'BINDING-EVIDENCE-MEMBERSHIP')
 for n in expected:require(candidate[n]==expected[n],'BINDING-EVIDENCE-BYTES:'+n)

def _rows(basis):
 cat=basis['catalogue'];e=basis['evidence'];rows=[]
 for context in basis['prior']['contexts']:
  name=context['context'];hb=context['hf01_evidence_binding'];record=hb['head_record'];occ=hb['occurrence'];instance=hb['instance']
  path=record['artifact'];require(path=='evidence/recovery-export-0.json' and record['pointer']=='/head','BINDING-HEAD-SELECTOR')
  require({k:record[k] for k in ('bytes','sha256')}==identity(e[path]),'BINDING-HEAD-IDENTITY')
  require(record['acquisition']==occ['call']['acquisition'] and occ['source']['qualified']=='ManagedAuthority.recover','BINDING-ACQUISITION-RECOVERY')
  refs=[r for r in context['saved_reference_scope'] if r['occurrence']==occ['id']];require(len(refs)==1,'BINDING-REFERENCE-SCOPE-JOIN');ref=refs[0]
  same(ref['instance'],instance,'BINDING-INSTANCE-JOIN');require(ref['frame']==occ['frame'] and ref['call_pointer']==occ['call']['pointer'],'BINDING-FRAME-JOIN')
  raw=bytes.fromhex(json.loads(e[path])['head']);state=json.loads(raw);value=state[cat['source']['state_selector']]
  require(type(value) is str,'BINDING-EXPECTED-VALUE-TYPE');same(value,instance['binding'],'BINDING-INSTANCE-STATE-RELATION')
  # There is no fabricated getter occurrence. This is the exact existing
  # recovery frontier to which a conditional source value relation can attach.
  anchor={'context':name,'instance':copy.deepcopy(instance),'recovery_occurrence':occ['id'],
   'recovery_frame':occ['frame'],'recovery_parent':occ['parent_frame'],'call':copy.deepcopy(occ['call']),'completion':copy.deepcopy(occ['completion']),
   'record':copy.deepcopy(record),'decoded_state':identity(raw),'selector':'/'+cat['source']['state_selector'],'binding_value':value,
   'predecessor_receipt':identity(basis['saved']),'reference_relation_ids':copy.deepcopy(ref['source_relation_ids']),
   'object_identity':None,'underlying_connection_identity':None,'getter_frame':None,
   'meaning':'Validated recorded instance binding at this recovery frontier; conditional source forwarding only. Not a getter result, current state, reference identity or connection identity.'}
  rows.append({'context':name,'declaration':copy.deepcopy(cat),'validated_binding_anchor':anchor,
   'getter_observations':None,'missing':'No ManagedAuthority.binding call/return frame or attribute/assignment observation is supplied. Absence in this sparse capture is not evidence it was never called.'})
 return rows

def _check_rows(submitted,expected):
 require(type(submitted) is list and len(submitted)==len(expected)==2,'BINDING-CONTEXT-DOMAIN')
 for row,want in zip(submitted,expected):
  require(type(row) is dict and set(row)==set(want),'BINDING-ROW-FIELDS')
  require(row['context']==want['context'],'BINDING-CONTEXT-IDENTITY')
  a=row['validated_binding_anchor'];b=want['validated_binding_anchor']
  require(type(a) is dict and set(a)==set(b),'BINDING-ANCHOR-FIELDS')
  require(type(a['binding_value']) is str,'BINDING-ANCHOR-VALUE-TYPE');same(a['binding_value'],b['binding_value'],'BINDING-ANCHOR-VALUE')
  same(a,b,'BINDING-ANCHOR-LINEAGE');same(row,want,'BINDING-CONTEXT-CORRESPONDENCE')

def _checked(data,submitted_catalogue,claims=None,evidence=None):
 basis=_basis(data);fresh=basis['fresh'];same(submitted_catalogue,basis['catalogue'],'BINDING-SOURCE-CATALOGUE')
 # Candidate source/context dictionaries cannot replace the reloaded basis.
 d=data['prior_data'];fd=fresh['prior_data']
 for k in ('manager','authority'):require(d[k]==fd[k],'BINDING-CANDIDATE-SOURCE:'+k)
 require(d['ctx']['c']==fd['ctx']['c'],'BINDING-CANDIDATE-CONTEXT:c')
 same(d['ctx']['binding'],fd['ctx']['binding'],'BINDING-CANDIDATE-CONTEXT:binding')
 _compare_evidence(basis['evidence'],d['ctx']['e'] if evidence is None else evidence,basis['catalogue']['source']['state_selector'])
 rows=_rows(basis)
 if claims is not None:_check_rows(claims,rows)
 return rows,basis

def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)

def derive_binding(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence)
 result=copy.deepcopy(basis['prior']);result['format']='I164-MANAGED-BINDING-RETURN-CORRESPONDENCE-1'
 result['prior_recovery_components']=result.pop('extension_components');result['prior_recovery_receipt']=identity(basis['saved'])
 result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for context,row in zip(result['contexts'],rows):
  require(context['context']==row['context'],'BINDING-DERIVATION-CONTEXT');context['binding_return_correspondence']=copy.deepcopy(row)
 result['new_binding_slice_limits']={'static_conditional_correspondence':True,'saved_getter_execution_evidence':'UNAVAILABLE','actual_getter_count':None,
  'source_binding_value_is_not_object_or_connection_identity':True,'validated_frontier_is_not_current_or_lifetime_state':True,'no_new_state_authentication':True,
  'separate_observer_Client_state_call':True,'observer_frame':None,'missing_historical_producer_frames':True,'traced_invocations':18,
  'complete_repetition_coverage':False,'multiplicity':None,'no_runtime_changes':True,'no_new_logging_or_retention_permission':True,
  'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED',
  'SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False}
 return result

def reference_scope(anchor):
 return {'context':anchor['context'],'acquisition':anchor['record']['acquisition'],'recorded_instance':copy.deepcopy(anchor['instance']),'frontier':anchor['recovery_occurrence']}

def constructed_projection(data,submitted_catalogue,case):
 """Source/evidence-checked hypothetical getter case; never observation input."""
 rows,basis=_checked(data,submitted_catalogue)
 require(type(case) is dict and set(case)=={'kind','context','anchor','premise','returned'},'BINDING-CASE-FIELDS')
 require(case['kind']=='CONSTRUCTED-CONDITIONAL-GETTER','BINDING-CASE-NOT-EXECUTION')
 selected=[r for r in rows if r['context']==case['context']];require(len(selected)==1,'BINDING-CASE-CONTEXT');anchor=selected[0]['validated_binding_anchor']
 same(case['anchor'],anchor,'BINDING-CASE-ANCHOR')
 premise=case['premise'];require(type(premise) is dict and 'live_reference' in premise,'BINDING-CASE-PREMISE')
 live=premise['live_reference'];require(type(live) is dict and 'scope' in live,'BINDING-CASE-REFERENCE')
 same(live['scope'],reference_scope(anchor),'BINDING-CASE-REFERENCE-SCOPE')
 require(type(premise.get('underlying')) is dict and 'binding' in premise['underlying'],'BINDING-CASE-UNDERLYING')
 same(premise['underlying']['binding'],anchor['binding_value'],'BINDING-CASE-INSTANCE-BINDING')
 projected=basis['fresh']['coverage'].binding_value_projection(basis['catalogue'],premise,case['returned'])
 return {'kind':'CONSTRUCTED-CONDITIONAL-GETTER','context':case['context'],'anchor':copy.deepcopy(anchor),'projection':copy.deepcopy(projected),'runtime_observation':False}

def derive(root=ROOT):
 data=inputs(root);return derive_binding(data,catalogue(data))
def validate(root,saved):
 require(type(saved) is bytes and saved==enc(derive(root)),'STALE-OR-ALTERED-BINDING-CORRESPONDENCE')
 return {'result':'PASS','contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'receipt':identity(saved),'getter_runtime_evidence':'UNAVAILABLE','actual_admission':False,'complete_repetition_coverage':False}

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args()
 print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
