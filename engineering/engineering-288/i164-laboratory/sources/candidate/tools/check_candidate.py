"""Fresh metadata checks plus saved-evidence ingestion; no lifecycle/signing execution."""
import copy,json,time,traceback
from baseline import *
from static_ingest import ingest
from ingest import validate_export
from register import validate_response_projection
from common import parse,hexbytes
checks=[];start=time.monotonic()
def check(name,fn):
 fn();checks.append({'name':name,'status':'PASS'});print(name,flush=True)
def reject(fn):
 try:fn()
 except (Invalid,ValueError,KeyError,TypeError):return
 raise AssertionError('malformed input accepted')
def check_mutation(name,path,mutate):
 x=copy.deepcopy(expected[path]);mutate(x)
 check(name,lambda:reject(lambda:validate_values({**expected,path:x},expected)))
try:
 expected=construct();actual={p.name:json.loads(p.read_bytes()) for p in (ROOT/'candidate').iterdir() if p.is_file()}
 check('all-13-artifacts-match-source-construction',lambda:validate_values(actual,expected))
 check('exact-canonical-candidate-bytes',lambda:need(all(read('candidate/'+p)==enc(v) for p,v in expected.items()),'CANONICAL'))
 check('native-retained-roundtrip',lambda:roundtrip(mapping('retained/registers/fields.json'),'retained/registers/fields.json'))
 check('native-added-roundtrip',lambda:roundtrip(mapping('records/added-fields.json'),'records/added-fields.json'))
 rows=mapping('records/added-fields.json');rows[0]['native']['slots']=float(rows[0]['native']['slots'])
 check('roundtrip-rejects-type-coercion',lambda:reject(lambda:roundtrip(rows,'records/added-fields.json')))
 bundle=load('support/declarations/static.json');ns=namespace();f=expected['fields.json']['prospective']
 check('full-45043-class-namespace',lambda:need(len(ns)==45043 and not set(ns)&set(r['id'] for r in f),'NAMESPACE'))
 check('proposed-historical-collision-rejected',lambda:reject(lambda:declarations(bundle,ns+[f[0]['id']])))
 bb=copy.deepcopy(bundle);bb['templates'][1]['parent']='missing'
 check('missing-template-parent-rejected',lambda:reject(lambda:declarations(bb,ns)))
 bb=copy.deepcopy(bundle);bb['templates'][0]['source_sha256']='0'*64
 check('altered-source-hash-rejected',lambda:reject(lambda:declarations(bb,ns)))
 for name,fn in [('missing',lambda x:x['prospective'].pop()),('wrong-type',lambda x:x['prospective'][0]['native_template'].update(type='INTEGER')),('wrong-guard',lambda x:x['prospective'][0]['native_template'].update(guard='always')),('wrong-parent',lambda x:x['prospective'][1].update(parent=None)),('duplicate-id',lambda x:x['prospective'][1].update(id=x['prospective'][0]['id'])),('unknown-promoted',lambda x:x['prospective'][0]['native_template'].update(visibility='PUBLIC'))]:
  check_mutation('field-'+name,'fields.json',fn)
 check_mutation('omitted-family','schemas.json',lambda x:x['prospective'].pop('HEAD'))
 check_mutation('missing-source-form','source-forms.json',lambda x:x['prospective'].pop())
 check_mutation('lost-ancestry-association','associations.json',lambda x:x['prospective'].pop(0))
 check_mutation('stale-runtime-binding','profile-binding.json',lambda x:x['runtime'][0].update(sha256='0'*64))
 check_mutation('mixed-register-binding','profile-binding.json',lambda x:x['metadata']['fields.json'].update(sha256='1'*64))
 check_mutation('wrong-context','contexts.json',lambda x:x['associations'][0].update(context='SUBSTITUTED'))
 check_mutation('omitted-context','contexts.json',lambda x:x['associations'].pop())
 check_mutation('lost-lifetime-blocker','directories.json',lambda x:x.update(lifetime_acquisition_recovery_diagnostics={'bound':1,'status':'COMPLETE'}))
 check_mutation('increased-attempt-cap','directories.json',lambda x:x['local']['attempt'].update(max=103))
 check_mutation('qualified-ledger-claim','ledger-duties.json',lambda x:x.update(full_ledger_bound=True))
 check_mutation('canonical-status-promotion','status.json',lambda x:x.update(canonical_registration='COMPLETE'))
 check('no-caller-boolean-final-binding',lambda:reject(lambda:final_binding(actual,{'all':True,'qualified':True,'authority':'Steve'})))
 check('no-final-binding-with-removed-blockers',lambda:reject(lambda:final_binding({**actual,'status.json':{'blockers':[]}}, {'all':True})))
 # Reuse saved small exports. New work is the adapter into candidate identities.
 examples=[];methods=set();kinds=set();has_retry=set();classmap={r['template_id']:r['id'] for r in f}
 names=['ord-early','zk-early','ord-finalized','zk-finalized','ord-abandon','zk-abandon','ord-cleanup','zk-cleanup','failed-ord-proceed','failed-zk-proceed','exit-after_retry_commit','exit-after_signature_commit']
 for name in names:
  raw=read('support/fixtures/'+name+'.json');export=parse(raw,200000000)
  out=ingest(export,bundle)
  need(not out['canonical_registration'] and out['final_binding']=='BLOCKED','SUPPORTING-BOUNDARY')
  head=parse(hexbytes(export['head']));blobmap={x[0]:hexbytes(x[1]) for x in export['blobs']}
  attempts=[];actions=[];links=[]
  for ref,b in blobmap.items():
   try:v=parse(b,200000000)
   except Invalid:continue
   if type(v) is not dict:continue
   if {'parent','retry_id','ordinal','transaction','action'}<=set(v):
    attempts.append({'reference':ref,'exact_bytes_hex':b.hex(),'parsed':v,'class':classmap['ATTEMPT:']})
   if {'template','branch','kind','attempt_ordinal'}<=set(v):
    actions.append({'reference':ref,'exact_bytes_hex':b.hex(),'parsed':v,'class':classmap['ACTION:']});kinds.add(v['kind'])
   if v.get('method') in ['signPetition','signPetitionWithZKProof']:methods.add(v['method'])
   if type(v.get('identity')) is dict and v['identity'].get('method') in ['signPetition','signPetitionWithZKProof']:methods.add(v['identity']['method'])
  for link in out['response_selector_coverage']:
   if link['pointer']=='/signature':
    row=next(r for r in out['actual_occurrences'] if r['id']==link['occurrence_id'])
    need(row['type']=='STRING','SIGNATURE-TYPE')
    links.append({**link,'candidate_class':classmap['RESPONSE:/signature'],'exact_bytes_hex':row['exact_bytes_hex']})
  need(links,'NO-ENVELOPE-JOIN')
  for a in attempts:
   if a['parsed']['parent'] is not None:has_retry.add(name)
  result={'fixture':ident('support/fixtures/'+name+'.json'),'profile_sha256':sha(read('candidate/profile-binding.json')),'contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'context_status':'candidate scope, not two actual executions','attempt_occurrences':attempts,'action_occurrences':actions,'response_signature_joins':links,'retained_state':{'counts':head['counts'],'resources':head['resources'],'u':head['u']},'saved_evidence_only':True,'new_lifecycle_executions':0,'canonical_registration':False}
  save('results/examples/'+name+'.json',result)
  examples.append({'name':name,'attempts':len(attempts),'actions':len(actions),'signature_joins':len(links),'sha256':sha(enc(result))})
  check('candidate-saved-example:'+name,lambda:need(bool(result['response_signature_joins']),'ENVELOPE'))
  # Reopening correspondence is re-ingestion of exact saved bytes, not a new process-exit experiment.
  check('saved-reopen:'+name,lambda e=export,o=out:same({k:v for k,v in validate_export(e).items() if k!='objects'},o['validation'],'REOPEN'))
  if name=='ord-early':
   bad=copy.deepcopy(export);bad['expected_head']='0'*64
   check('saved-stale-head-rejected',lambda:reject(lambda:validate_export(bad)))
   bad=copy.deepcopy(export);bad['owners'].clear()
   check('saved-owner-omission-rejected',lambda:reject(lambda:validate_export(bad)))
   bad=copy.deepcopy(export);j=next(x for x in bad['journal'] if x[2] is not None);packet=parse(hexbytes(j[2]));packet['signature']='00'*64;j[2]=enc(packet).hex()
   check('altered-response-envelope-rejected',lambda:reject(lambda:validate_export(bad)))
 check('both-methods-and-required-action-kinds',lambda:need(methods=={'signPetition','signPetitionWithZKProof'} and {'proceed','abandon','cleanup'}<=kinds,'EXAMPLE-COVERAGE'))
 check('saved-explicit-retry-present',lambda:need(bool(has_retry),'RETRY-COVERAGE'))
 check('all-inputs-and-historical-90-still-exact',pin_inputs)
 receipt={'fresh_checks':checks,'count':len(checks),'saved_examples':examples,'methods':sorted(methods),'action_kinds':sorted(kinds),'retry_examples':sorted(has_retry),'elapsed_seconds':time.monotonic()-start,'new_lifecycle_executions':0,'new_process_exit_executions':0,'prior_reviews_rerun':False,'final_binding':'BLOCKED','actual_admission':False}
 save('results/focused.json',receipt);print(json.dumps({'PASS':len(checks),'examples':len(examples),'seconds':receipt['elapsed_seconds']}))
except Exception:
 save('results/partial-checks.json',checks);raise
