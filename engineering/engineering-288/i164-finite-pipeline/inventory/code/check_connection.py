"""Focused new linkage controls; not a repeat of predecessor review suites."""
import argparse,copy,importlib.util,json,pathlib,sys,time,traceback

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--code',required=True);ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);ap.add_argument('--case',default='suite');a=ap.parse_args();out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=False)
 s=importlib.util.spec_from_file_location('tested_inventory',a.code);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);cfg=m.parse(m.read(a.config));start=time.monotonic();results=[]
 def record(name,fn,reject=False):
  try:fn()
  except (ValueError,KeyError,TypeError) as e:
   if not reject:raise
   if a.case in ('mixed','claim') and str(e)!='INVENTORY-CONNECTION-CORRESPONDENCE':raise AssertionError('WRONG REJECTION BOUNDARY: '+str(e))
   results.append({'name':name,'result':'REJECTED','exception':type(e).__name__,'reason':str(e)});return
  if reject:raise AssertionError('MUTANT ACCEPTED: '+name)
  results.append({'name':name,'result':'PASS'})
 try:
  if a.case!='suite':
   submitted=m.parse(m.read(pathlib.Path(a.config).parent/'expected.json'))
   if a.case=='mixed':submitted['inventory_records'][-1]['recorded_session']='I164-lab-session-001'
   if a.case=='claim':submitted['runtime_93_file_claim']='ALL 93 RUNTIME BYTES VERIFIED'
   record('public-'+a.case,lambda:m.run(cfg,submitted),a.case in ('mixed','claim'))
  else:
   print('Validate actual saved evaluator and derive inventory connection',flush=True)
   baseline=m.run(cfg);(out/'receipt.json').write_bytes(m.enc(baseline)+b'\n')
   raw=m.read(cfg['inventory_archive']);prior=m.read(cfg['expression_receipt']);base=copy.deepcopy(baseline['evaluation'])
   def validate(sub):m.same(m._attach(base,m.inventory(raw),raw,prior),sub,'ATTACHMENT-CORRESPONDENCE')
   record('legitimate-derived',lambda:validate(baseline))
   mutations=[
    ('missing-record',lambda x:x['inventory_records'].pop()),
    ('duplicate-record',lambda x:x['inventory_records'].append(copy.deepcopy(x['inventory_records'][0]))),
    ('record-count-as-invocations',lambda x:x.update(record_count_unit='INVOCATIONS')),
    ('stale-acquisition',lambda x:x.update(acquisition_id='other')),
    ('mixed-inventory',lambda x:x['bindings']['inventory'].update(sha256='0'*64)),
    ('runtime-proof-escalation',lambda x:x.update(runtime_93_file_claim='VERIFIED')),
    ('physical-total-zero',lambda x:x.update(physical_storage_bytes=0)),
    ('lifetime-zero',lambda x:x.update(global_lifetime_bound=0)),
    ('cross-acquisition',lambda x:x.update(cross_acquisition_joins=True)),
    ('drop-obligation',lambda x:x['obligations'].pop(next(iter(x['obligations'])))),
    ('qualified',lambda x:x.update(classification='QUALIFIED')),
    ('operational',lambda x:x.update(assessment='OPERATIONAL')),
    ('readiness',lambda x:x.update(readiness='READY')),
    ('final-binding',lambda x:x.update(final_binding='PASS')),
    ('admission',lambda x:x.update(actual_admission=True)),
    ('O06-closure',lambda x:x.update(global_O06_closed=True)),
    ('O09-closure',lambda x:x.update(global_O09_closed=True)),
    ('contexts-reverse',lambda x:x['contexts'].reverse()),
    ('context-duplicate',lambda x:x['contexts'].__setitem__(1,copy.deepcopy(x['contexts'][0]))),
    ('stale-code',lambda x:x['bindings']['code'].update(sha256='0'*64)),
    ('drop-fact',lambda x:x['recorded_facts'].pop()),
    ('assertion-becomes-observation',lambda x:x['recorded_facts'][0].update(execution_independently_observed=True)),
    ('93-altered',lambda x:x['recorded_facts'][0]['exact_recorded_value'].update(files=94)),
    ('reopened-sequence',lambda x:x['recorded_facts'][1]['exact_recorded_value']['state'].update(seq=1)),
    ('reopened-charge',lambda x:x['recorded_facts'][1]['exact_recorded_value']['state']['counts'].update(attempt=1)),
    ('fact-stale-record',lambda x:x['recorded_facts'][0].update(record_id=x['recorded_facts'][1]['record_id'])),
    ('root-correction-drop',lambda x:x['root_corrections'].pop()),
    ('root-correction-wrong-root',lambda x:x['root_corrections'][0].update(correct_root='checkpoint')),
   ]
   hist=next(i for i,r in enumerate(baseline['inventory_records']) if r['provenance_scope'].startswith('HISTORICAL'))
   cop=next(i for i,r in enumerate(baseline['inventory_records']) if r['copy_of'])
   new=next(i for i,r in enumerate(baseline['inventory_records']) if r['provenance_scope']=='SEPARATE-5002-HOST-FIXTURE')
   mutations += [('history-as-host',lambda x:x['inventory_records'][hist].update(provenance_scope='ORIGINAL-4107-SESSION-RECORD')),('mixed-session',lambda x:x['inventory_records'][new].update(recorded_session='I164-lab-session-001')),('copy-as-invocation',lambda x:x['inventory_records'][cop].update(adds_invocation=True)),('erase-copy-link',lambda x:x['inventory_records'][cop].update(copy_of=None)),('physical-copy-inference',lambda x:x['inventory_records'][cop].update(physical_alias_relationship='DISTINCT-ALLOCATION'))]
   for i in range(4):
    mutations.append(('gap-zero-'+str(i),lambda x,i=i:x['inventory_associations'][i].update(value=0,status='COMPLETE')))
    mutations.append(('gap-refs-omitted-'+str(i),lambda x,i=i:x['inventory_associations'][i].update(evidence_record_ids=[])))
   for name,fn in mutations:
    mutant=copy.deepcopy(baseline);fn(mutant);m.need(m.enc(mutant)!=m.enc(baseline),'NO-OP-MUTATION');record(name,lambda:validate(mutant),True)
   record('repeat-pristine',lambda:validate(copy.deepcopy(baseline)))
   record('serialized-pristine',lambda:validate(m.parse(m.enc(baseline))))
   record('altered-archive',lambda:m.inventory(raw[:-1]+bytes([raw[-1]^1])),True)
   # Mutation of public returned aliases cannot change a later public derivation.
   mutated=baseline;mutated['contexts'].reverse();mutated['recorded_facts'][0]['exact_recorded_value']['files']=0;mutated['inventory_records'][0]['adds_invocation']=True
   pristine=m.parse(m.read(out/'receipt.json'))
   print('Revalidate pristine receipt after mutating returned nested structures',flush=True)
   record('public-pristine-after-return-mutation',lambda:m.run(cfg,pristine))
  summary={'status':'PASS','controls':len(results),'case':a.case,'results':results,'seconds':time.monotonic()-start,'scope':'new inventory linkage only; internal mutation checks distinguished from public validator calls'}
  (out/'results.json').write_bytes(m.enc(summary)+b'\n');print('PASS',len(results),a.case,flush=True)
 except BaseException:
  (out/'failure.txt').write_text(traceback.format_exc());(out/'partial-results.json').write_bytes(m.enc(results));raise
if __name__=='__main__':main()
