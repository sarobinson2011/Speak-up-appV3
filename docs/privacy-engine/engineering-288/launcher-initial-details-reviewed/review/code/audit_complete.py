"""Read-only reconciliation of supplied and retained evidence. No validator campaigns."""
from pathlib import Path
import sys,json,hashlib,ast,dis,types,collections,traceback
sys.path.insert(0,str(Path(__file__).parent))
from integrity import ident,enc,js,verify_root
BASE=Path('/workspace/scratch/ace5c9b2f18b');root=Path(sys.argv[1]);out=BASE/'ld01-review/results/audit-completed';out.mkdir(exist_ok=False)
def reconcile(result,progress,stdout,exit):
 r=js(result.read_bytes());rows=[js(x) for x in progress.read_text().splitlines()] if progress.exists() else [];assert progress.exists() or r['checks']==0;printed=[x for x in stdout.read_text().splitlines() if x and x.split(' ',1)[0].isdigit()];e=js(exit.read_bytes());assert r['rows']==rows and r['checks']==len(rows)==len(printed)
 assert printed==[f"{i} {row['check']} {row['result']}" for i,row in enumerate(rows,1)]
 return {'rows':len(rows),'row_kinds':dict(collections.Counter(x['result'] for x in rows)),'result':r['result'],'result_identity':ident(result.read_bytes()),'exit':e,'reconciled':True,'error':r.get('error'),'scope':r['scope']}
try:
 supplied=js((root/'ld01/RESULTS.json').read_bytes());groups={}
 for name,v in supplied['new_groups_separate'].items():
  a=root/'ld01/results'/name;p=root/'ld01/processes'/name;g=reconcile(a/'RESULT.json',a/'progress.jsonl',p/'stdout.log',p/'exit-status.json');assert g['rows']==v['recorded_rows'] and g['result_identity']==v['result'] and g['exit']==v['exit'];assert g['result']=='PASS' and g['exit']['returncode']==0 and not g['exit']['timed_out'];g['classification']=v['kind'];groups[name]=g
  if name in ('primary','recovered'):
   launch=js((p/'launch.json').read_bytes());calls=js((a/'calls.json').read_bytes());counts={tag:dict(collections.Counter(c['function'] for c in calls if c['file']==path)) for tag,path in [('current',launch['root']+'/code/correspondence.py'),('predecessor',launch['root']+'/retained/client-construction/code/correspondence.py')]}
   for tag in v['recorded_calls']:
    for key,num in v['recorded_calls'][tag].items():assert counts[tag][key]==num
   groups[name]['call_counts']=counts;groups[name]['full_public_negative_derivations']=0
 prior=root/'retained/ld01-review/review';priorcp=js((prior/'CHECKPOINT.json').read_bytes());priorgroups={}
 for label,actual in [('fresh-recovered','fresh-recovered'),('source-monitor-qualified','source-monitor'),('audit-completion','audit-completion'),('monitor-interruption','monitor-interruption')]:
  a=prior/'results'/actual;p=prior/'processes'/actual;g=reconcile(a/'RESULT.json',a/'progress.jsonl',p/'stdout.log',p/'exit-status.json');assert g['rows']==priorcp['independent_groups'][label]['rows'];assert g['result_identity']==priorcp['independent_groups'][label]['result_identity'];priorgroups[label]=g
 assert priorgroups['fresh-recovered']['rows']==523 and priorgroups['fresh-recovered']['exit']['returncode']==0
 assert priorgroups['source-monitor-qualified']['rows']==80 and priorgroups['source-monitor-qualified']['exit']['returncode']==1
 assert priorgroups['audit-completion']['rows']==0 and priorgroups['monitor-interruption']['rows']==2
 # Saved source/current-receipt provenance and root historical result status.
 integrity=js((BASE/'ld01-review/results/integrity.json').read_bytes());orig=root/'retained/ld01-original/MANIFEST.json';assert ident(orig.read_bytes())=={'bytes':1279025,'sha256':'8a09c3fa6a7036ea043009c9dc3b8aa7485e1d243a143878cd8c5d4af77ecc6b'}
 old_manifest=js(orig.read_bytes());historical={n:ident((root/n).read_bytes()) for n in ('README.txt','RECOVERY.txt','RESULTS.json','SEMANTICS.txt','START-HERE.txt')};assert all(pin==old_manifest[n] for n,pin in historical.items())
 source_checks={}
 for label,path in [('old',root/'retained/ld01-original/code/correspondence.py'),('corrected',root/'code/correspondence.py')]:
  raw=path.read_bytes();code=compile(raw,str(path),'exec');fn=next(x for x in code.co_consts if isinstance(x,types.CodeType) and x.co_name=='_public_predecessor');tree=ast.parse(raw);f=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_public_predecessor');capture=next(n for n in ast.walk(f) if isinstance(n,ast.FunctionDef) and n.name=='capture');acq=next(n for n in ast.walk(f) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='use_tool_id')
  exceptions=[dict(start=x.start,end=x.end,target=x.target,depth=x.depth,lasti=x.lasti) for x in dis.Bytecode(fn).exception_entries];instructions=[{'offset':i.offset,'opname':i.opname,'argrepr':i.argrepr,'line':i.positions.lineno,'end_line':i.positions.end_lineno} for i in dis.get_instructions(fn)];cap=[i for i in instructions if i['line']==capture.lineno and i['opname']=='MAKE_FUNCTION'];calls=[i for i in instructions if i['line']==acq.lineno and i['opname']=='CALL']
  source_checks[label]={'identity':ident(raw),'capture_definition_line':capture.lineno,'acquisition_line':acq.lineno,'exception_table':exceptions,'acquisition_line_calls':calls,'callback_make_function':cap,'all_instructions':instructions}
  assert len(cap)==1
  covered=any(e['start']<=cap[0]['offset']<e['end'] for e in exceptions);assert covered==(label=='corrected')
 source_checks['scope']='Recorded CPython3.12.14 bytecode inspection only; not compiled-runtime binary authentication or application execution'
 result={'supplied_correction_groups':groups,'prior_independent_groups':priorgroups,'prior_review_verdict':priorcp['verdict'],'prior_source_support':priorcp['bounded_source_correspondence'],'prior_Engineering':priorcp['supplied_Engineering_groups'],'prior_Engineering_failures':priorcp['supplied_failures'],'historical_qualifications':priorcp['historical_qualifications'],'root_historical_documents_unchanged':historical,'both_contexts_prefixes_source_mappings_unchanged':True,'preservation':supplied['preservation'],'declared_changes':integrity['implementation'],'no_campaigns_executed':True,'rows_replayed':0}
 (out/'supplied-and-preserved.json').write_bytes(enc(result));(out/'source-bytecode.json').write_bytes(enc(source_checks));(out/'final-verification.json').write_bytes(enc(verify_root(root)));(out/'RESULT.json').write_bytes(enc({'result':'PASS','controls_replayed':0,'scope':'Read-only evidence and source audit; no control count added'}));print(json.dumps({'result':'PASS','supplied_groups':{k:v['rows'] for k,v in groups.items()},'prior_independent_groups':{k:v['rows'] for k,v in priorgroups.items()},'controls_replayed':0}),flush=True)
except BaseException:
 (out/'failure.txt').write_text(traceback.format_exc());raise
