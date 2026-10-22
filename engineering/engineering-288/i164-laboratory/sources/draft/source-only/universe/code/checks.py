"""New bounded annotation/count composition tests; retained projections not re-executed."""
import sys,ast,copy,json,hashlib
from pathlib import Path
from collections import Counter
import universe as u
c=u.c;P=Path(__file__).resolve().parents[1];root=Path(sys.argv[1]).resolve();dest=Path(sys.argv[2]);dest.mkdir(parents=True,exist_ok=True)
x=c.load(P/'outputs/universe.json');results=[]
def ok(name,**more):
 results.append({'case':name,'result':'PASS',**more});(dest/'progress.json').write_bytes(c.enc(results))
def reject(name,fn):
 try:fn()
 except ValueError as e:ok(name,rejection=str(e))
 else:raise AssertionError(name)
u.validate(root,x);ok('exact-current-input')
# Independent enumeration of source writer syntax, not the submitted inventory.
tree=ast.parse((root/'support/code/ingest.py').read_bytes());required=[]
for n in ast.walk(tree):
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='objects':required.append((str(n.lineno)+':'+str(n.col_offset),n.func.attr))
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='objects' for t in n.targets):required.append((str(n.lineno)+':'+str(n.col_offset),'initialize'))
assert sorted(required)==sorted((n['site'],n['operation']) for n in x['source_emission_sites']['sites']);ok('source-emission-coverage',sites=len(required))
schemas=c.load(root/'candidate/schemas.json')['prospective'];assert set(schemas)=={f['family'] for f in x['families']};ok('defining-schema-family-coverage',families=len(schemas))
nd=c.load(root/'layout_outputs/directory.json')['directories'];assert len(nd)==len(x['directory_links'])==18678
assert {(d['context'],d['class']) for d in nd}=={tuple(d['required_procedure_range']) for d in x['directory_links']};ok('all-current-directories-and-contexts')
for row in x['protected_carriers']:
 for a in row['source_anchors']:
  nodes=[n for n in ast.walk(ast.parse((root/a['path']).read_bytes())) if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==a['name'] and n.lineno==a['line']]
  assert len(nodes)==1 and c.sha(ast.dump(nodes[0],include_attributes=False).encode())==a['ast_sha256']
ok('all-protected-carrier-source-anchors')
mutations=[
 ('omitted-family',lambda z:z['families'].pop()),
 ('wrong-occurrence-key',lambda z:z['families'][0].update(protected_occurrence_key=['value_hash'])),
 ('success-only-guard',lambda z:next(f for f in z['families'] if f['family']=='UNVALIDATED-BODY').update(creation_condition='successful requests only')),
 ('zero-read-lifetime',lambda z:next(r for r in z['protected_carriers'] if r['id']=='read-recovery-invocations').update(count_expression='0',finite_global_bound=0)),
 ('per-file-as-global',lambda z:next(r for r in z['protected_carriers'] if r['id']=='journal').update(finite_global_bound=384000)),
 ('omitted-uncertainty',lambda z:z['protected_carriers'].__delitem__(7)),
 ('missing-directory',lambda z:z['directory_links'].pop()),
 ('wrong-guard',lambda z:z['directory_links'][0].update(guard='False')),
 ('wrong-context',lambda z:z['directory_links'][0].update(context='SYMBOLIC-U-TWO')),
 ('stale-source',lambda z:z['sources']['support/code/ingest.py'].update(sha256='0'*64)),
 ('stale-candidate',lambda z:z['candidate_binding']['candidate'].update(sha256='0'*64)),
 ('cross-copy-cartesian',lambda z:z['relation_lifetime'].update(op='CARTESIAN')),
 ('qualification',lambda z:z['directory_links'][0].update(classification='QUALIFIED')),
 ('readiness',lambda z:z.update(full_expansion_ready=True,final_binding='PASS')),
 ('omitted-emission-and-family-links',lambda z:(z['source_emission_sites']['sites'].clear(),[f.update(direct_emission_site_ids=[]) for f in z['families']]))]
for name,mutate in mutations:
 bad=copy.deepcopy(x);mutate(bad);assert c.enc(bad)!=c.enc(x);reject(name,lambda:u.validate(root,bad))
u.validate(root,x);ok('pristine-after-submitted-mutations')
# Count composition uses exact retained independently reviewed projection bytes.
# No prior review, producer or Candidate.ingest is rerun.
records=[];enum=[]
for ctx in x['contexts']:
 p=c.load(P/'evidence'/('projection-'+ctx+'.json'));c.same(p['binding'],x['candidate_binding'],'SAVED-PROJECTION-CURRENT-BINDING')
 counts=dict(Counter(ctx+'|'+r['class'] for r in p['candidate_occurrences']))
 for acq in ['retained-acquisition-A','retained-acquisition-B']:
  records.append({'acquisition_id':acq,'context':ctx,'export_sha256':p['saved_export_sha256'],'counts':counts})
  enum.extend((acq,ctx,r['id'],ctx+'|'+r['class']) for r in p['candidate_occurrences'])
assert len({(a,ctx,i) for a,ctx,i,d in enum})==len(enum)
r=u.count_acquisition_bag(root,x,records);assert r['counts']==dict(Counter(d for a,ctx,i,d in enum));ok('equal-content-distinct-acquisitions-both-contexts',occurrences=len(enum))
# Toy keyed-parent agreement: each acquisition preserves its own source-target join.
pairs=[((a,ctx,i),(a,ctx,'parent')) for a,ctx,i,d in enum];assert len(pairs)==len(enum) and all(l[:2]==r[:2] for l,r in pairs);ok('acquisition-local-keyed-count-composition',scope='constructed count algebra only, not new semantic-rule qualification')
bad=copy.deepcopy(records);bad.append(copy.deepcopy(bad[0]));reject('replayed-acquisition-context',lambda:u.count_acquisition_bag(root,x,bad))
bad=copy.deepcopy(records);bad[2]['export_sha256']='0'*64;reject('mixed-acquisition-frontier',lambda:u.count_acquisition_bag(root,x,bad))
for n in [-1,True,1.5]:
 bad=copy.deepcopy(records);key=next(iter(bad[0]['counts']));bad[0]['counts'][key]=n;reject('count-type-'+repr(n),lambda:u.count_acquisition_bag(root,x,bad))
bad=copy.deepcopy(records);key=next(iter(bad[0]['counts']));bad[0]['counts'][key]=None;r=u.count_acquisition_bag(root,x,bad);assert r['counts'][key] is None;ok('unknown-not-zero')
for kind,cap in x['local_ceilings'].items():
 a=u.scoped_upper(root,x,kind,[cap,cap]);assert a['observed_sum']==2*cap and a['global_upper'] is None;ok('boundary-'+kind)
 reject('beyond-'+kind,lambda:u.scoped_upper(root,x,kind,[cap+1]));reject('bool-'+kind,lambda:u.scoped_upper(root,x,kind,[True]))
 assert u.scoped_upper(root,x,kind,[cap,None])['observed_sum'] is None;ok('unknown-scope-'+kind)
# Current native count-only/procedure input consumption; all duties remain blocked.
r=u.consume(root,x);c.same(r,c.load(P/'outputs/consumption.json'),'RECORDED-CONSUMPTION');ok('native-count-only-procedure-consumption',directories=r['directory_count'],duties=r['relation_duties'])
(dest/'results.json').write_bytes(c.enc({'groups':len(results),'checks':results,'retained_review_executed':False,'producer_execution':False}));print('PASS',len(results),'groups',flush=True)
