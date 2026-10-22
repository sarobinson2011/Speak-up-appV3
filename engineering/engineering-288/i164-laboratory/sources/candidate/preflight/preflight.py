"""I164 prospective model preflight. No expansion/streams/admission path.
python3 preflight.py --root CORRECTED_ROOT --output result.json
"""
import argparse,ast,hashlib,json,sys,time,resource,tempfile,shutil,copy
from pathlib import Path
H=lambda b:hashlib.sha256(b).hexdigest()
PINS={'candidate/identity.json':'d2b76814433f1d3c96bccdb2eaaa6ddb1521cafcd2c616fc1b93d064995a2130','integration/candidate_pipeline.py':'dde0eea9641b79cfe11e8c25965f4d4e0db68d1062f6d7a9b9e34f2949215bb6','native/code/expand_candidate.py':'d4d0f560b088a05191cba845e0b3e9a3f37463604f1b1ec91be20ddde73d7479'}
CONTEXTS=['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']
def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def require(x,msg):
 if not x:raise ValueError(msg)
def inspect_plan(p,classes):
 require(p['contexts']==CONTEXTS,'context bindings')
 require(set(p['directories'])==set(classes),'complete class-directory membership')
 for k,v in p['directories'].items():
  require(type(v.get('count')) is int and v['count']>=0,'unknown multiplicity')
  require(v.get('source') and v.get('guard') and (v['count']>0 or v.get('inapplicability')),'source/guard/inapplicability')
 require(set(p['relations'])==set(p['required_relations']),'missing relation rule')
 for v in p['relations'].values():require(v['operator'] in ['INDEX-EQUAL','PARENT-SLOT','CARTESIAN'] and v.get('source') and all(e in classes for e in v['endpoints']),'relation rule/endpoint')
 require(p['status']=='DRAFT-UNQUALIFIED' and p['admission'] is False,'scope escalation')
 return 2*sum(v['count'] for v in p['directories'].values())
def run(root):
 started=time.monotonic();root=root.resolve();ident=lambda p:{'path':p,'bytes':(root/p).stat().st_size,'sha256':H((root/p).read_bytes())}
 for p,h in PINS.items():require(ident(p)['sha256']==h,'stale input '+p)
 sys.path.insert(0,str(root/'integration'));from candidate_pipeline import Candidate
 c=Candidate();fields=c.c['fields.json']['prospective'];classes=[r['id'] for r in fields];parents=sum(r['parent'] is not None for r in fields)
 require(sorted(c.contexts)==CONTEXTS,'inherited contexts');require(len(set(classes))==len(classes),'duplicate classes')
 inherited=set(c.c['namespace.json']['historical_classes']);require(not inherited&set(classes),'inherited conflict')
 for row in fields:require(row['parent'] is None or row['parent'] in classes,'missing parent')
 steps=[{'id':'prospective-contract','status':'SOURCE-WORK-REQUIRED','output':'guarded per-class/per-context directory program with exact selectors, parent/index rules and explicit unresolved multiplicity cells','inputs':['candidate/fields.json','candidate/schemas.json','candidate/directories.json','support/reference/runtime/authority.py','support/reference/runtime/accounting.py','support/reference/runtime/ownership.py']},
 {'id':'relation-lowering','status':'SOURCE-WORK-REQUIRED','output':'ordered append-only relation rows; typed join operators/guards; inherited ordinal preservation; no qualified dependency inferred','inputs':['candidate/associations.json','native/records/relation-rules.json','candidate/native-mapping.json','support/code/ingest.py','integration/candidate_pipeline.py']},
 {'id':'source-coverage','status':'SOURCE-WORK-REQUIRED','output':'independent coverage inventory beyond pinned SD01 response domain; requests, ABI, wrappers, keys, framing, variants and extraction carriers','inputs':['candidate/source-forms.json','support/code/static_declarations.py','support/code/response_obligations.py']},
 {'id':'procedure-ledger','status':'SOURCE-WORK-REQUIRED','output':'prospective expansion input adapter/count-only compiler and exact node/relation duty templates; bound procedure identities','inputs':['native/code/expand_candidate.py','native/code/bind_ledger.py','native/code/finalize_records.py','candidate/ledger-duties.json']},
 {'id':'finite-domain','status':'UNESTABLISHED','inputs':['source-owned lifetime acquisition/recovery/diagnostic multiplicities','Decision B external exact serialization bounds','complete physical and retained-storage accounting']},
 {'id':'classification-qualification','status':'FINAL-BINDING-BLOCKED','inputs':['qualified dependency/visibility/seven-role custody','appointments/phase evidence','operational custody/rollback/deployment','risk/non-vacuity/finality evidence']},
 {'id':'registration','status':'NOT-OCCURRED','inputs':['exact target/native format/limits and membership designation','owning canonical registration procedure and eligible status']},
 {'id':'parent-array-materialization','status':'NOT-VERIFIED-BY-THIS-PREFLIGHT','inputs':['historical full saved model matching native/candidate/identity.json; before byte reuse, verify exact whole/array bytes'] }]
 # Actual candidate currently supplies guarded descriptions, not a complete per-class expansion plan.
 require(c.c['directories.json']['lifetime_acquisition_recovery_diagnostics']['bound'] is None,'reassess changed lifetime premise')
 tests=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,TypeError) as e:tests.append({'name':name,'rejected':str(e)});return
  raise AssertionError('unexpected acceptance '+name)
 fixture={'contexts':CONTEXTS,'directories':{'a':{'count':2,'source':'fixture-only','guard':'present'},'b':{'count':1,'source':'fixture-only','guard':'present'}},'required_relations':['ab'],'relations':{'ab':{'operator':'CARTESIAN','source':'fixture-only','endpoints':['a','b']}},'status':'DRAFT-UNQUALIFIED','admission':False}
 require(inspect_plan(fixture,['a','b'])==6,'small count');tests.append({'name':'small fixture 6 tokens/4 Cartesian edges','passed':True})
 for name,edit in [('missing class',lambda p:p['directories'].pop('b')),('unknown count',lambda p:p['directories']['a'].update(count=None)),('boolean count',lambda p:p['directories']['a'].update(count=True)),('missing guard',lambda p:p['directories']['a'].pop('guard')),('missing relation',lambda p:p['relations'].clear()),('bad endpoint',lambda p:p['relations']['ab'].update(endpoints=['a','x'])),('mixed context',lambda p:p.update(contexts=['SYMBOLIC-U-ONE'])),('admission claim',lambda p:p.update(admission=True)),('classification elevation',lambda p:p.update(status='QUALIFIED'))]:
  bad=copy.deepcopy(fixture);edit(bad);reject(name,lambda:inspect_plan(bad,['a','b']))
 # Reuse actual historical segment writer alone, with three rows, no model construction/import side effects.
 tree=ast.parse((root/'native/code/expand_candidate.py').read_bytes());node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='segmented')
 import gzip
 with tempfile.TemporaryDirectory() as tmp:
  t=Path(tmp)
  def atomic(p,b):p.write_bytes(b)
  env={'R':t,'load':lambda p:json.loads(p.read_bytes()),'need':require,'sha':lambda p:H(p.read_bytes()),'save':lambda p,v:p.write_bytes(enc(v)),'W':lambda v:enc(v).rstrip(b'\n'),'H':H,'gzip':gzip,'atomic':atomic,'shutil':shutil,'json':json}
  exec(compile(ast.Module(body=[node],type_ignores=[]),'<retained segmented>', 'exec'),env)
  rows=lambda skip:iter([{'index':i} for i in range(skip,3)])
  s=env['segmented']('fixture',rows,'fixture-pin',1);require(s['rows']==3 and not s['complete'],'checkpoint');tests.append({'name':'three-row checkpoint','passed':True})
  s=env['segmented']('fixture',rows,'fixture-pin');require(s['complete'] and s['rows']==3,'resume');tests.append({'name':'resume exact prefix','passed':True})
  reject('mixed resume binding',lambda:env['segmented']('fixture',rows,'different'))
  p=t/'segments/fixture/000000.jsonl.gz';p.write_bytes(b'corrupt');reject('corrupt committed segment',lambda:env['segmented']('fixture',rows,'fixture-pin'))
 hist=json.loads((root/'native/candidate/identity.json').read_bytes());metadata=[ident('candidate/'+p.name) for p in sorted((root/'candidate').iterdir())]
 return {'preflight_code':{'bytes':Path(__file__).stat().st_size,'sha256':H(Path(__file__).read_bytes())},'result':'BLOCKED-FULL-EXPANSION; READY-SOURCE-DERIVED-CONTRACT-AND-RELATION-WORK','closure':{'DI-01':'INDEPENDENTLY-CLOSED-WITHIN-REVIEWED-SCOPE','review_sha256':'81a164abfc0c93af39a809c5794fb2249bdc0237e20f4e3d35d0a36aef38994d','review_controls':125,'reviews_rerun':False},'binding':c.binding,'candidate_artifacts':metadata,'context_definition_references':c.c['contexts.json']['historical_definitions'],'contexts':CONTEXTS,'counts':{'historical_classes':len(inherited),'proposed_classes':len(classes),'union_classes':len(inherited)+len(classes),'declaration_parent_links':parents,'source_families':len(c.groups),'association_templates':len(c.c['associations.json']['prospective']),'complete_new_tokens':None,'complete_new_edges':None,'complete_model_bytes':None},'steps':steps,'historical_size_only':{k:hist[k] for k in ['model_bytes','compressed_bytes','tokens','structural_edges','model_sha256']},'resource_status':{'full_run_runtime_seconds':None,'full_run_peak_memory':None,'full_run_disk_bound':None,'reason':'unknown complete directories and join cardinalities; historical estimates are not prospective bounds','retained_writer':'100000 rows per buffered segment; gzip level1; hash reread all committed segments; 2GiB free-space stop is not total-capacity assurance','historical_2x_raw_plus_2GiB_planning_scenario_not_proven_bound':2*hist['model_bytes']+2*1024**3},'checks':tests,'fixture_only':True,'measurements':{'preflight_seconds':time.monotonic()-started,'process_peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'free_disk_bytes':shutil.disk_usage(root).free,'candidate_artifact_bytes':sum(x['bytes'] for x in metadata)},'final_binding':'BLOCKED','canonical_registration':False,'stream_identities':'UNCOMPUTED','actual_admission':False}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--root',type=Path,required=True);a.add_argument('--output',type=Path,required=True);a.add_argument('--current-inputs',type=Path);a.add_argument('--validate-result',type=Path);a.add_argument('--legacy',action='store_true');x=a.parse_args()
 require(not x.output.exists(),'output exists')
 if x.current_inputs:
  require(not x.legacy,'mixed legacy/current entry');sys.path.insert(0,str(x.root.resolve()/'compiler'));import layout_consumers as current
  inputs=json.loads(x.current_inputs.read_bytes())
  if x.validate_result:
   current.validate_current_result(x.root,inputs,x.current_inputs.parent,json.loads(x.validate_result.read_bytes()));out={'format':'I164-CURRENT-RESULT-VALIDATED-1','validated':True,'full_expansion_ready':False,'final_binding':'BLOCKED','actual_admission':False}
  else:out=current.validate_current(x.root,inputs,x.current_inputs.parent)
 else:
  require(x.legacy and not x.validate_result,'current validation requires --current-inputs; legacy is explicit and cannot establish current validation');out=run(x.root)
 x.output.write_bytes(enc(out));print('PASS bounded current correspondence; readiness/final binding BLOCKED' if x.current_inputs else 'HISTORICAL PREFLIGHT ONLY')
