"""Focused candidate connection checks; saved exports only, no signer/lifecycle."""
import json,copy,gzip,sys,traceback
from pathlib import Path
from candidate_pipeline import *
R=ROOT/'integration/results';R.mkdir(exist_ok=True)
checks=[];examples=[]
def ok(name,condition=True):
 assert condition,name
 checks.append({'name':name,'result':'PASS'})
def reject(name,fn):
 try:fn()
 except Invalid as e:checks.append({'name':name,'result':'PASS','rejection':str(e)});return
 raise AssertionError('accepted '+name)
def main():
 c=Candidate();(R/'binding.json').write_bytes(enc(c.binding))
 ok('exact reviewed candidate + 377 pinned inputs including historical90/43',len(c.c['namespace.json']['historical_classes'])==45043)
 source=ROOT/'support/fixtures'
 for name in ['ord-early','zk-early','ord-finalized','zk-finalized','ord-abandon','zk-abandon','ord-cleanup','zk-cleanup','failed-ord-proceed','failed-zk-proceed','exit-after_retry_commit','exit-after_signature_commit']:
  e=parse((source/(name+'.json')).read_bytes(),200000000)
  for context in sorted(c.contexts):
   x=c.ingest(e,context,c.binding)
   ok(name+'/'+context+'/candidate-fields',len(x['candidate_occurrences'])>0)
   ok(name+'/'+context+'/response-binding',len(x['response_associations'])==len(x['supporting_pipeline']['response_selector_coverage']))
   ok(name+'/'+context+'/final-blockers',x['final_binding']=='BLOCKED' and not x['canonical_registration'] and not x['actual_admission'])
   examples.append({'fixture':identity('support/fixtures/'+name+'.json'),'context':context,'result_sha256':sha(enc(x)),'result_bytes':len(enc(x)),'links':len(x['candidate_occurrences']),'framing':len(x['derived_framing']),'indices':len(x['derived_indices']),'unassigned':x['unassigned_extraction_wrappers'],'actions':x['supporting_pipeline']['validation']['action_kinds'],'counts':x['supporting_pipeline']['validation']['counts'],'resources':x['supporting_pipeline']['validation']['resources']})
   if name=='ord-early' and context=='SYMBOLIC-U-ONE':
    # Keep one complete small-example output, including exact originals and candidate associations.
    (R/'ordinary-example.json.gz').write_bytes(gzip.compress(enc(x),mtime=0));first=(e,x)
  print(name,'two contexts PASS',flush=True)
 e,x=first
 # Reopening reads the saved output and rederives against the saved authenticated export.
 loaded=parse(gzip.decompress((R/'ordinary-example.json.gz').read_bytes()),500000000)
 ok('reopening exact correspondence',c.validate_output(loaded,e))
 for field,value in [('candidate_occurrences',[]),('response_associations',[]),('blockers',[]),('final_binding','PASS'),('canonical_registration',True)]:
  bad=copy.deepcopy(x);bad[field]=value
  reject('output substitution '+field,lambda:c.validate_output(bad,e))
 for key in ['candidate','profile','contexts','directories','duties','downstream_adapter']:
  b=copy.deepcopy(c.binding);b[key]['sha256']='0'*64
  reject('stale/mixed '+key,lambda:c.ingest(e,'SYMBOLIC-U-ONE',b))
 for path in ['../candidate/identity.json','/etc/passwd','candidate/missing.json']:
  b=copy.deepcopy(c.binding);b['candidate']['path']=path
  reject('directory rejection '+path,lambda:c.check_binding(b))
 b=copy.deepcopy(c.binding);del b['register']['fields'];reject('missing register',lambda:c.check_binding(b))
 b=copy.deepcopy(c.binding);b['runtime'][0]['sha256']='0'*64;reject('altered runtime',lambda:c.check_binding(b))
 b=copy.deepcopy(c.binding);b['reviewed_adapters'][0]['sha256']='0'*64;reject('altered reviewed adapter',lambda:c.check_binding(b))
 reject('unknown context',lambda:c.ingest(e,'SYMBOLIC-U-THREE',c.binding))
 bad=copy.deepcopy(e)
 for row in bad['journal']:
  if row[2] is not None:
   obj=parse(bytes.fromhex(row[2]));obj['signature']='0'*len(obj['signature']);row[2]=enc(obj).hex();break
 reject('altered authenticated signature',lambda:c.ingest(bad,'SYMBOLIC-U-ONE',c.binding))
 reject('UNKNOWN cannot qualify',lambda:c.final_binding({'qualification':True,'classifications':'KNOWN'}))
 # Candidate artifact mutation is caught at the actual file boundary. Always restore exact bytes.
 p=ROOT/'candidate/fields.json';raw=p.read_bytes()
 try:
  p.write_bytes(raw+b' ')
  reject('changed candidate bytes after initialization',lambda:c.check_binding(c.binding))
 finally:p.write_bytes(raw)
 ok('restored candidate verification',baseline.validate_disk()['metadata_correspondence']=='PASS')
 (R/'checks.json').write_bytes(enc({'checks':checks,'count':len(checks),'examples':examples,'fresh':'adapter checks over saved evidence; no fresh runtime actions','prior_review_controls_not_rerun':37,'final_binding':'BLOCKED'}))
 print('PASS',len(checks))
if __name__=='__main__':
 try:main()
 except Exception:
  (R/'failed-checks.json').write_bytes(enc(checks));(R/'failure.txt').write_text(traceback.format_exc());raise
