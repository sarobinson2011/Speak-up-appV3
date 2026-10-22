"""Focused correspondence checks only. No candidate execution or signing."""
import copy,json,sys
from common import *
from ingest import validate_export
from pipeline import integrate
from register import *
results=[]
def check(name,fn):
 fn();results.append({'name':name,'status':'PASS'});print(name,flush=True)
def reject(fn):
 try:fn()
 except (Invalid,KeyError,TypeError,ValueError):return
 raise AssertionError('accepted malformed input')
fixtures={p.stem:parse(p.read_bytes(),200000000) for p in (ROOT/'fixtures').glob('*.json') if p.name!='INDEX.json'}
for n,x in sorted(fixtures.items()):
 def good(x=x):
  a=validate_export(x);b=validate_export(copy.deepcopy(x));same(a,b,'REOPEN-DIFFERENCE');need(not a['actual_admission'] and not a['canonical_registration'],'STATUS')
 check('saved-ingestion-and-reopening:'+n,good)
x=fixtures['ord-early']
def mutate(name,fn):
 y=copy.deepcopy(x);fn(y);check(name,lambda:reject(lambda:validate_export(y)))
mutate('missing-event',lambda y:y['events'].pop())
mutate('missing-blob',lambda y:y['blobs'].pop())
mutate('missing-owner',lambda y:y['owners'].clear())
mutate('conflicting-owner',lambda y:y['owners'].append(y['owners'][0]))
mutate('duplicate-challenge',lambda y:y['journal'].append(y['journal'][0]))
mutate('stale-anchor',lambda y:y.update(expected_head=ZERO))
mutate('wrong-session',lambda y:y['config'].update(session='substituted'))
mutate('float-config',lambda y:y['config'].update(start_nonce=float(y['config']['start_nonce'])))
mutate('bool-config',lambda y:y['config'].update(start_nonce=True))
mutate('wrong-signature',lambda y:y['journal'][0].__setitem__(1,enc(dict(parse(hexbytes(y['journal'][0][1])),signature='00'*64)).hex()))
for key in ['counts','resources','u']:
 def change(y,key=key):
  h=parse(hexbytes(y['head']));h[key]={};y['head']=enc(h).hex()
 mutate('nested-head-'+key,change)
# Rehash an altered final event and HEAD: must fail semantic fold, not merely hash join.
for label,change in [
 ('float-counter',lambda s:s['counts'].update(attempt=float(s['counts']['attempt']))),
 ('bool-counter',lambda s:s['counts'].update(attempt=True)),
 ('charge-refund',lambda s:s['counts'].update(attempt=0)),
 ('lost-hold',lambda s:s['resources'].update(holds=0)),
 ('unretirement',lambda s:next(iter(s['u'].values())).update(retired=False)),
 ('reservation-substitution',lambda s:next(iter(s['u'].values())).update(reservation=ZERO)),
 ('ancestry-substitution',lambda s:next(iter(s['u'].values()))['stage']['pending'].update(first=ZERO))]:
 y=copy.deepcopy(fixtures['exit-after_decision_commit']);e=parse(hexbytes(y['events'][-1][1]));change(e['after']);raw=enc(e);y['events'][-1][1]=raw.hex();y['head']=enc(dict(e['after'],head=sha(raw))).hex();y['expected_head']=sha(raw)
 check('rehash-'+label,lambda y=y:reject(lambda:validate_export(y)))
for raw in [b'{"a":1,"a":1}\n',b'{"a":NaN}\n',b'{ "a":1}\n']:
 check('noncanonical-'+sha(raw)[:8],lambda raw=raw:reject(lambda:parse(raw)))
reg=build_register();check('424-fields-41-families',lambda:need(len(reg['fields'])==424 and len({r['record'] for r in reg['fields']})==41,'COVERAGE'))
for change in [lambda r:r['fields'].pop(),lambda r:r['fields'][0].update(visibility='PUBLIC'),lambda r:r.update(canonical_registration=True)]:
 r=copy.deepcopy(reg);change(r);check('register-substitution-'+str(len(results)),lambda r=r:reject(lambda:validate_register(r)))
check('canonical-gate',lambda:reject(lambda:final_binding(reg,{'all':True})))
old=json.loads((ROOT/'reference/added-fields.json').read_text());b=enc(old)
check('historical-baseline-reconciliation',lambda:need(reconcile(reg,b,sha(b))['existing_rows']==876,'BASELINE'))
conflict=enc(old+[dict(reg['fields'][0],visibility='PUBLIC')]);check('baseline-conflict',lambda:reject(lambda:reconcile(reg,conflict,sha(conflict))))
check('baseline-wrong-identity',lambda:reject(lambda:reconcile(reg,b,ZERO)))
from model_adapter import potential_equal,declarations,validate_declarations
for a,b,e in [(False,False,False),(True,False,True),(False,True,True)]:
 check('potential-equality-'+str(a)+'-'+str(b),lambda a=a,b=b,e=e:need(potential_equal({'arbitrary':a,'symbolic_digest':ZERO},{'arbitrary':b,'symbolic_digest':'1'*64})==e,'PREDICATE'))
check('equal-symbolic-digest',lambda:need(potential_equal({'arbitrary':False,'symbolic_digest':ZERO},{'arbitrary':False,'symbolic_digest':ZERO}),'EQUALITY'))
d=declarations(reg);d['full_expansion_permitted']=True
check('reject-full-expansion-claim',lambda:reject(lambda:validate_declarations(d,reg)))
p=integrate(x);need(p['final_binding']=='BLOCKED','GATE');(ROOT/'results/example-projection.json').write_bytes(enc(p))
check('projection-nested-exact-bytes',lambda:need(all(len(hexbytes(r['exact_bytes_hex']))==r['encoding_length'] for r in p['actual_occurrences']),'EXACT'))
(ROOT/'results/focused.json').write_bytes(enc({'fresh_execution':'correspondence integration checks only','groups':results,'groups_passed':len(results),'saved_fixture_count':len(fixtures),'new_lifecycle_executions':0,'new_process_exit_executions':0,'projection_rows':len(p['actual_occurrences']),'projection_bytes':len(enc(p))}))
