import argparse,copy,importlib.util,sys,json,time
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--component',required=True);ap.add_argument('--output',required=True);ap.add_argument('--skip-completed-positives',action='store_true');a=ap.parse_args();out=Path(a.output);out.mkdir()
s=importlib.util.spec_from_file_location('finite_native_consumer',Path(__file__).with_name('consumer.py'));c=importlib.util.module_from_spec(s);sys.modules[s.name]=c;s.loader.exec_module(c)
results=[]
def record(name,status='PASS'):
 results.append({'name':name,'status':status});(out/'checks.json').write_text(json.dumps(results,indent=2));print(name,status,flush=True)
b,p=c.trusted(a.component);fn=c.sources(b,p);objects=c.construct(b,fn);v=c.representation(b,objects)
for ctx,orig,obj in ([] if a.skip_completed_positives else zip(v['contexts'],b['contexts'],objects)):
 assert len(obj.tokens)==2376 and len(obj.groups)==9339 and len(obj.edges)==2368
 assert len({t.key for t in obj.tokens})==2376
 assert all(t.payload==bytes.fromhex(src['exact_bytes_hex']) and list(t.key)==src['key'] for t,src in zip(obj.tokens,orig['tokens']))
 for g,r in zip(obj.groups,orig['directory_ranges']):
  lo,hi=r['range'];assert [x[0] for x in g.entries()]==list(range(lo,hi))
  for i,k,parent,new in g.entries():assert g.get(k)==(i,True)
 expected=[(q['ordinal'],q['from_index'],q['to_index']) for step in orig['lookup_steps'] for q in orig['structural_pairs']+orig['semantic_pairs'] if q['ordinal']==step['ordinal']]
 assert [(x[0],x[1],x[2]) for x in obj.edges]==expected
 record(ctx['context']+' independent bytes/keys/ranges/group access/ordered endpoints')
mutations=[
 ('range-overlap',lambda x:next(g for g in x['contexts'][0]['groups'] if g['range']['range'][0]>0)['range']['range'].__setitem__(0,0)),
 ('range-negative',lambda x:x['contexts'][0]['groups'][0]['range']['range'].__setitem__(0,-1)),
 ('range-bool',lambda x:x['contexts'][0]['groups'][0]['range']['range'].__setitem__(0,False)),
 ('missing-token',lambda x:x['contexts'][0]['occurrences'].pop()),
 ('duplicate-token',lambda x:x['contexts'][0]['occurrences'].append(copy.deepcopy(x['contexts'][0]['occurrences'][0]))),
 ('altered-bytes',lambda x:x['contexts'][0]['occurrences'][0].__setitem__('payload_hex','00')),
 ('coordinated-bytes',lambda x:(x['contexts'][0]['occurrences'][0].__setitem__('payload_hex','00'),x['contexts'][0]['occurrences'][0]['metadata'].__setitem__('exact_bytes_hex','00'))),
 ('index-float',lambda x:x['contexts'][0]['occurrences'][0].__setitem__('index',0.0)),
 ('endpoint',lambda x:x['contexts'][0]['ordered_edges'][0].__setitem__('target_index',999999)),
 ('edge-order',lambda x:x['contexts'][0]['ordered_edges'].reverse()),
 ('edge-missing',lambda x:x['contexts'][1]['ordered_edges'].pop()),
 ('stale-source',lambda x:x.__setitem__('component_sha256','0'*64)),
 ('stale-bindings',lambda x:x.__setitem__('bindings',{})),
 ('mixed-context',lambda x:x['contexts'][0]['occurrences'][0]['key'].__setitem__(1,'SYMBOLIC-U-TWO')),
 ('context-order',lambda x:x['contexts'].reverse()),
 ('cross-acquisition',lambda x:x['contexts'][1]['occurrences'][0]['key'].__setitem__(0,'OTHER')),
 ('omitted-duty',lambda x:x['contexts'][0].__setitem__('duties',{})),
 ('omitted-obligations',lambda x:x.__setitem__('obligations',{})),
 ('qualified',lambda x:x.__setitem__('classification','QUALIFIED')),
 ('readiness',lambda x:x.__setitem__('full_expansion_ready',True)),
 ('admission',lambda x:x.__setitem__('actual_admission',True)),
 ('model-completion',lambda x:x.__setitem__('complete_native_model',True)),
 ('ledger-bound',lambda x:x.__setitem__('ledger_rebound',True)),
 ('zero-lifetime',lambda x:x.__setitem__('global_lifetime_bound',0)),
]
for name,mutate in mutations:
 x=copy.deepcopy(v);mutate(x);assert c.enc(x)!=c.enc(v),'INEFFECTIVE-MUTATION:'+name
 try:c.run(a.component,x)
 except c.Rejected:record(name)
 else:raise AssertionError('ACCEPTED:'+name)
returned=c.run(a.component,v);returned['contexts'].reverse();returned['obligations'].clear()
assert c.run(a.component,v)==v;record('mutable-return/pristine-repeated-validation')
try:objects[0].tokens[0].payload=b'changed'
except Exception:record('immutable-occurrence')
else:raise AssertionError('mutable')
(out/'summary.json').write_text(json.dumps({'passed':len(results),'completed':True,'scope':'fresh finite-consumer controls; no predecessor suites rerun'},indent=2))
