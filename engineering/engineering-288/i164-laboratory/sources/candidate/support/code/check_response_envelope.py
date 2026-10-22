"""IA-01 focused adapter checks. Synthetic envelope keys are PUBLIC-LAB-ONLY.
No candidate scheduler, transaction signer or network execution.
"""
import copy,subprocess,sys,hashlib
from common import *
from ingest import validate_export
from pipeline import integrate
from register import build_register,project,validate_response_projection,validate_register
from model_adapter import declarations
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
results=[]
def check(n,fn):
 try:detail=fn();results.append({'name':n,'status':'PASS','detail':detail})
 except Exception as e:results.append({'name':n,'status':'FAIL','error':repr(e)});raise
 finally:(ROOT/'results/response-checks.json').write_bytes(enc(results))
 print(n,flush=True)
def reject(fn):
 try:fn()
 except (ValueError,KeyError,TypeError):return
 raise AssertionError('accepted invalid value')
def load(n):return parse((ROOT/'fixtures'/n).read_bytes(),200000000)
def sig(role,obj):return Ed25519PrivateKey.from_private_bytes(hashlib.sha256(('PUBLIC-LAB-ONLY-'+role).encode()).digest()).sign(VERSION.encode()+b'\0'+enc(obj)).hex()
x=parse((ROOT/'review/independent/F1-minimal.json').read_bytes(),200000000)
def old():
 script="import sys;sys.path[:0]=sys.argv[1:3];from common import *;from pipeline import integrate;x=parse(Path(sys.argv[3]).read_bytes(),200000000);p=integrate(x);n=sum(r['record']=='RESPONSE' and r['pointer']=='/signature' for r in p['actual_occurrences']);assert n==0;print(n)"
 z=subprocess.run([sys.executable,'-B','-c',script,str(ROOT/'review/old-code'),str(ROOT/'code'),str(ROOT/'review/independent/F1-minimal.json')],capture_output=True,text=True);need(z.returncode==0,z.stderr);return {'required':1,'old_observed':int(z.stdout)}
check('original-witness-old-omission',old)
def corrected():
 p=integrate(x);rows=[r for r in p['actual_occurrences'] if r['record']=='RESPONSE' and r['pointer']=='/signature'];need(len(rows)==1,'SIGNATURE');z=parse(hexbytes(x['journal'][0][2]));need(rows[0]['type']=='STRING' and rows[0]['exact_bytes_hex']==enc(z['signature']).hex(),'VALUE');need(len(p['response_selector_coverage'])==5,'COVERAGE');(ROOT/'results/minimal-corrected.json').write_bytes(enc(p));return {'rows':len(p['actual_occurrences']),'bytes':len(enc(p)),'signature_occurrences':1}
check('original-witness-corrected',corrected)
reg=build_register();forms=set()
for f in sorted((ROOT/'fixtures').glob('*.json')):
 if f.name=='INDEX.json':continue
 def run(f=f):
  v=validate_export(load(f.name));rows=[]
  for i,(kind,obj) in enumerate(v['objects']):
   if kind=='RESPONSE':rows+=project(obj,kind,i)
  c=validate_response_projection(v['objects'],rows,v['response_links'],reg)
  same(c,validate_response_projection(v['objects'],copy.deepcopy(rows),v['response_links'],reg),'REOPEN')
  for _,packet,res in load(f.name)['journal']:
   q=parse(hexbytes(packet));forms.add(q['request']['method']+':'+('unanswered' if res is None else 'success' if parse(hexbytes(res))['response']['ok'] else 'error'))
  return {'envelopes':len(v['response_links']),'selector_joins':len(c)}
 check('saved-forms-reopening:'+f.stem,run)
for label,fn in [('missing-signature',lambda z:z.pop('signature')),('altered-signature',lambda z:z.update(signature='00'*64)),('wrong-signature-type',lambda z:z.update(signature=1)),('missing-response',lambda z:z.pop('response')),('altered-data',lambda z:z['response'].update(data={})),('bool-confusion',lambda z:z['response'].update(ok=1)),('extra-envelope-field',lambda z:z.update(extra=True))]:
 y=copy.deepcopy(x);z=parse(hexbytes(y['journal'][0][2]));fn(z);y['journal'][0][2]=enc(z).hex();check(label,lambda y=y:reject(lambda:validate_export(y)))
for field in ['request','challenge']:
 y=copy.deepcopy(x);z=parse(hexbytes(y['journal'][0][2]));z['response'][field]=ZERO;z['signature']=sig('server',z['response']);y['journal'][0][2]=enc(z).hex();check('authentic-but-mismatched-'+field,lambda y=y:reject(lambda:validate_export(y)))
y=copy.deepcopy(x);y['journal'][0][2]=None
check('unanswered-no-invented-signature',lambda:need(not integrate(y)['response_selector_coverage'],'UNANSWERED'))
v=validate_export(x);rows=[]
for i,(kind,obj) in enumerate(v['objects']):
 if kind=='RESPONSE':rows+=project(obj,kind,i)
check('downstream-missing-signature-row',lambda:reject(lambda:validate_response_projection(v['objects'],[r for r in rows if r['pointer']!='/signature'],v['response_links'],reg)))
rr=copy.deepcopy(rows);next(r for r in rr if r['pointer']=='/signature')['type']='INTEGER'
check('downstream-type-substitution',lambda:reject(lambda:validate_response_projection(v['objects'],rr,v['response_links'],reg)))
links=copy.deepcopy(v['response_links']);links[0]['request_hash']=ZERO
check('downstream-association-substitution',lambda:reject(lambda:validate_response_projection(v['objects'],rows,links,reg)))
r=copy.deepcopy(reg);next(z for z in r['fields'] if z['record']=='RESPONSE' and z['selector']=='signature')['projection_pointer']='/response/signature'
check('register-path-substitution',lambda:reject(lambda:validate_register(r)))
check('model-declaration-consumes-path',lambda:need(next(z for z in declarations(reg)['fields'] if z['record']=='RESPONSE' and z['selector']=='signature')['projection_pointer']=='/signature','PATH'))
# Synthetic parser-only HEAD and BACKUP envelopes exercise absent saved entry-point variants.
for method in ['head','backup']:
 y=copy.deepcopy(load('ord-early.json'));head=parse(hexbytes(y['head']));q=copy.deepcopy(parse(hexbytes(y['journal'][0][1]))['request']);q.update(principal='executor',method=method,expected=head['head'],challenge=sha(('synthetic-envelope-'+method).encode()),body={} if method=='head' else {'id':sha(b'synthetic-backup')},u=head['active']);packet={'request':q,'signature':sig('executor',q)}
 if method=='backup':
  after=copy.deepcopy(head);after.pop('head');after['seq']+=1;after['counts']['snapshot']+=1;after['partitions']['snapshot']+=1;after['u'][q['u']]['stage']['backups'][q['body']['id']]='RETAINED-UNCERTAIN';event={'previous':head['head'],'request':sha(enc(q)),'kind':'backup','proof':None,'after':after};raw=enc(event);head=dict(after,head=sha(raw));y['events'].append([after['seq'],raw.hex()]);y['head']=enc(head).hex();y['expected_head']=head['head']
 res={'request':sha(enc(packet)),'challenge':q['challenge'],'ok':True,'data':head};envelope={'response':res,'signature':sig('server',res)};y['journal'].append([q['challenge'],enc(packet).hex(),enc(envelope).hex()]);(ROOT/'results'/('synthetic-'+method+'.json')).write_bytes(enc(y))
 check('synthetic-parser-only-'+method,lambda y=y:need(len(integrate(y)['response_selector_coverage'])==40,'SYNTHETIC-COVERAGE'))
p=integrate(load('ord-early.json'));(ROOT/'results/example-projection.json').write_bytes(enc(p))
(ROOT/'results/response-summary.json').write_bytes(enc({'fresh_groups':len(results),'saved_exports':37,'forms':sorted(forms),'ordinary_example_rows':len(p['actual_occurrences']),'ordinary_example_bytes':len(enc(p)),'minimal_witness_unchanged':sha((ROOT/'review/independent/F1-minimal.json').read_bytes()),'new_lifecycles':0,'new_process_exits':0,'synthetic_fixtures':'parser-only public-lab signed HEAD and BACKUP envelopes, not candidate execution'}))
