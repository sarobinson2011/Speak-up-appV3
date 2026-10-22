"""Fresh small declaration/reconciliation tests; no candidate lifecycle."""
import copy,shutil,tempfile
from common import *
from static_declarations import *
from reconcile_baseline import reconcile,REQUIRED
from static_ingest import ingest
results=[]
def check(name,fn):
 try:d=fn();results.append({'name':name,'status':'PASS','detail':d})
 except Exception as e:results.append({'name':name,'status':'FAIL','error':repr(e)});raise
 finally:(ROOT/'results/checks.json').write_bytes(enc(results))
 print(name,flush=True)
def reject(fn):
 try:fn()
 except (ValueError,KeyError,TypeError,FileNotFoundError):return
 raise AssertionError('invalid input accepted')
b=build();(ROOT/'declarations/static.json').write_bytes(enc(b))
for label,mut in [('omit-field',lambda x:x['templates'].pop(10)),('omit-frame',lambda x:x['templates'].pop(2)),('omit-variant',lambda x:x['constructor_guard_inventory'].pop()),('wrong-type',lambda x:x['templates'][0].update(type='INTEGER')),('wrong-guard',lambda x:x['templates'][5].update(guard='always')),('missing-parent',lambda x:x['templates'][1].update(parent='missing')),('duplicate-class',lambda x:x['templates'].append(x['templates'][0])),('changed-source',lambda x:x['templates'][0].update(source_sha256=ZERO)),('context-substitution',lambda x:x['context_slots'][0].update(identity='made-up'))]:
 y=copy.deepcopy(b);mut(y);check(label,lambda y=y:reject(lambda:validate(y)))
for p in sorted((ROOT/'fixtures').glob('*.json')):
 if p.name in ['INDEX.json','minimal-response.json']:continue
 check('saved-typed-coverage:'+p.stem,lambda p=p:validate_export_templates(parse(p.read_bytes(),200000000),b))
x=parse((ROOT/'fixtures/ord-early.json').read_bytes(),200000000)
def response():
 p=ingest(x,b);need(len([r for r in p['actual_occurrences'] if r['record']=='RESPONSE' and r['pointer']=='/signature'])==7,'IA-01');need(len(p['response_selector_coverage'])==35,'ASSOCIATIONS');return {'signature_occurrences':7,'selector_joins':35}
check('corrected-envelope-downstream',response)
for v in [1,1.0,'true',None]:
 z={'signature':'00'*64,'response':{'request':ZERO,'challenge':ZERO,'ok':v,'data':{}}}
 check('invalid-response-discriminator:'+repr(v),lambda z=z:reject(lambda:validate_value('RESPONSE',z,'head')))
# Known-null and absent are not interchangeable.
check('missing-required-head-field',lambda:reject(lambda:validate_value('HEAD',{})))
check('recursive-open-capsule',lambda:validate_value('CONDITIONAL-CAPSULE',{'format':'I164-COMPUTED-COMPARISON-CAPSULE-1','permit_for_conditional_test':True,'extra':[None,3,3.0,False,{'escaped':'a\\b'}]}))
check('fixed-ABI-array-length',lambda:reject(lambda:validate_value('ABI-signPetitionWithZKProof',{})))
fixture=ROOT/'results/reconciliation-fixture';fixture.mkdir(exist_ok=False);base=fixture/'baseline';base.mkdir();(fixture/'deltas').mkdir();contexts=['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']
def write(root,files):
 m={}
 for n,raw in files.items():
  p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw);m[n]={'bytes':len(raw),'sha256':sha(raw)}
 return m
source=b'# fixture only\n';row=lambda id,parent,src,h:{'id':id,'source':src,'source_sha256':h,'selector':'/x','type':'STRING','guard':'present','parent':parent}
rows=[row('FIXTURE:ROOT',None,'source.py',sha(source))];files={n:enc({'fixture_only':True}) for n in REQUIRED|{'register/custody.json'}};files['relationships-43.json']=(ROOT/'reference/relationships-43.json').read_bytes();files['register/fields.json']=enc(rows);files['source.py']=source
m={'format':'I164-BASELINE-MANIFEST-1','files':write(base,files),'contexts':contexts,'authority_record_sha256':sha(b'FIXTURE-NOT-AUTHORITY')};raw=enc(m);(base/'manifest.json').write_bytes(raw);baseline=head=sha(raw);dhash=[]
for i in [1,2]:
 dr=fixture/'deltas'/str(i).zfill(6);dr.mkdir();newsource=('fixture-source-'+str(i)).encode();name='source-'+str(i)+'.py';newrow=row('FIXTURE:CHILD'+str(i),'FIXTURE:ROOT',name,sha(newsource));rows.append(newrow)
 d={'format':'I164-REGISTER-DELTA-1','ordinal':i,'previous':head,'baseline':baseline,'contexts':contexts,'files':write(dr,{'added-fields.json':enc([newrow]),name:newsource}),'after_classes_sha256':sha(enc(sorted(rows,key=lambda x:x['id'])))};raw=enc(d);(dr/'manifest.json').write_bytes(raw);head=sha(raw);dhash.append(head)
a={'format':'I164-CANONICAL-INPUT-PIN-1','baseline_manifest_sha256':baseline,'delta_sha256':dhash,'head':head,'contexts':contexts,'authority_record_sha256':m['authority_record_sha256'],'historical_relationships_sha256':sha(files['relationships-43.json'])};pin=enc(a);(ROOT/'results/fixture-pin.json').write_bytes(pin)
check('valid-fixture-reconciliation',lambda:reconcile(fixture,pin,sha(pin)))
for label,mut in [('stale-head',lambda z:z.update(head=baseline)),('mixed-baseline',lambda z:z.update(baseline_manifest_sha256=ZERO)),('reordered-chain',lambda z:z['delta_sha256'].reverse()),('incomplete-chain',lambda z:z['delta_sha256'].pop()),('wrong-context',lambda z:z.update(contexts=['other','contexts']))]:
 z=copy.deepcopy(a);mut(z);p=enc(z);check(label,lambda p=p:reject(lambda:reconcile(fixture,p,sha(p))))
check('authority-pin-substitution',lambda:reject(lambda:reconcile(fixture,pin,ZERO)))
for label,path,mut in [('source-altered','baseline/source.py',lambda raw:raw+b'change'),('missing-class','baseline/register/fields.json',lambda raw:enc([])),('duplicate-class','baseline/register/fields.json',lambda raw:enc(parse(raw)*2)),('conflicting-class','deltas/000002/added-fields.json',lambda raw:enc([dict(parse(raw)[0],id='FIXTURE:ROOT')])),('missing-parent','deltas/000002/added-fields.json',lambda raw:enc([dict(parse(raw)[0],parent='MISSING')]))]:
 with tempfile.TemporaryDirectory() as td:
  dest=Path(td)/'copy';shutil.copytree(fixture,dest);p=dest/path;p.write_bytes(mut(p.read_bytes()));check(label,lambda:reject(lambda:reconcile(dest,pin,sha(pin))))
check('canonical-status-never-granted',lambda:need(reconcile(fixture,pin,sha(pin))['canonical_registration'] is False,'STATUS'))
(ROOT/'results/summary.json').write_bytes(enc({'completed_groups':len(results),'templates':len(b['templates']),'source_inventory':len(b['constructor_guard_inventory']),'schema_families':len(schemas()[0]),'actual_canonical_reconciliation':'BLOCKED-MISSING-AUTHORITATIVE-CURRENT-PIN-AND-CHAIN','fixture_only_reconciliation':'PASS','lifecycles':0,'stream_identities':'UNCOMPUTED','actual_admission':False}))
