"""DI-01 focused live/alias/reopen checks. No signing or network actions."""
import sys,copy,gzip,json,subprocess,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'integration'))
from candidate_pipeline import *
R=ROOT/'di01/results';R.mkdir(exist_ok=True);checks=[]
def ok(n,b=True):
 assert b,n
 checks.append({'name':n,'result':'PASS'})
def reject(n,f):
 try:f()
 except Invalid as e:checks.append({'name':n,'result':'PASS','rejection':str(e)});return
 raise AssertionError('ACCEPTED '+n)
def main():
 c=Candidate();e=parse((ROOT/'support/preserved-review/SD-01-minimal.json').read_bytes(),200000000)
 mutations=[('binding',lambda x:x['binding'].pop('downstream_adapter')),('blockers',lambda x:x['blockers'].clear()),('nested-runtime',lambda x:x['binding']['runtime'][0].update(sha256='0'*64)),('profile-through-model',lambda x:x['model_input']['candidate_profile'].update(sha256='0'*64)),('association-source',lambda x:x['association_index'][0]['source'].update(sha256='0'*64)),('blocker-value',lambda x:x['blockers'].__setitem__(0,'QUALIFIED')),('context',lambda x:x.update(context='SYMBOLIC-U-TWO')),('admission',lambda x:x.update(actual_admission=True)),('canonical',lambda x:x.update(canonical_registration=True)),('final-binding',lambda x:x.update(final_binding='PASS'))]
 initial=c.binding;import baseline
 blockers=enc(baseline.BLOCKERS)
 for name,mut in mutations:
  for form in ['live','deepcopy','shallow-alias']:
   out=c.ingest(e,'SYMBOLIC-U-ONE',c.binding);ok(name+'/'+form+'/unchanged',c.validate_output(out,e))
   target=copy.deepcopy(out) if form=='deepcopy' else copy.copy(out) if form=='shallow-alias' else out
   mut(target)
   reject(name+'/'+form+'/same-instance',lambda:c.validate_output(target,e))
   reject(name+'/'+form+'/repeat',lambda:c.validate_output(target,e))
   same(c.binding,initial,'EXPECTATION-MUTATION');ok(name+'/'+form+'/policy-intact',enc(baseline.BLOCKERS)==blockers)
   if form=='live' and name in ['binding','blockers']:
    path=R/(name+'-corrected-mutant.json');path.write_bytes(enc(target))
    cmd=[sys.executable,str(ROOT/'integration/candidate_pipeline.py'),'validate','--export',str(ROOT/'support/preserved-review/SD-01-minimal.json'),'--input',str(path)]
    p=subprocess.run(cmd,capture_output=True,text=True);(R/(name+'-fresh.stdout')).write_text(p.stdout);(R/(name+'-fresh.stderr')).write_text(p.stderr)
    ok(name+'/fresh-process-reject',p.returncode!=0 and ('MIXED-CANDIDATE-BINDING' in p.stderr or 'DOWNSTREAM-SUBSTITUTION' in p.stderr))
    reject(name+'/serialized-same-process',lambda:c.validate_output(parse(path.read_bytes(),500000000),e))
    path.with_suffix('.json.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0));path.unlink()
 # Detached input and property views cannot poison the next validation.
 b=c.binding;out=c.ingest(e,'SYMBOLIC-U-ONE',b);b.clear();ok('input binding mutation isolated',c.validate_output(out,e))
 view=c.binding;view['reviewed_adapters'].clear();ok('property nested mutation isolated',c.validate_output(out,e))
 reject('missing top-level binding',lambda:c.validate_output({'context':'SYMBOLIC-U-ONE'},e))
 reject('nondict result',lambda:c.validate_output([],e))
 for ctx in sorted(c.contexts):
  x=c.ingest(e,ctx,c.binding);ok(ctx+'/unchanged',c.validate_output(x,e));ok(ctx+'/serialized',c.validate_output(parse(enc(x),500000000),e))
 reject('final binding remains blocked',lambda:c.final_binding({'qualified':True}))
 # Affected ordinary/ZK saved-evidence regression, no runtime re-execution.
 for fn,ctx in [('ord-early','SYMBOLIC-U-ONE'),('zk-early','SYMBOLIC-U-TWO'),('exit-after_retry_commit','SYMBOLIC-U-ONE')]:
  ex=parse((ROOT/'support/fixtures'/ (fn+'.json')).read_bytes(),200000000);x=c.ingest(ex,ctx,c.binding)
  ok(fn+'/reopen',c.validate_output(parse(enc(x),500000000),ex))
  ok(fn+'/blocked',x['final_binding']=='BLOCKED' and len(x['blockers'])==7 and x['actual_admission'] is False and x['canonical_registration'] is False)
  (R/(fn+'-receipt.json')).write_bytes(enc({'binding':x['binding'],'export_sha256':sha(enc(ex)),'output_bytes':len(enc(x)),'output_sha256':sha(enc(x)),'counts':x['supporting_pipeline']['validation']['counts'],'resources':x['supporting_pipeline']['validation']['resources']}))
 (R/'checks.json').write_bytes(enc({'count':len(checks),'checks':checks,'scope':'fresh adapter validation over saved evidence; no runtime actions'}));print('PASS',len(checks))
if __name__=='__main__':
 try:main()
 except Exception:
  (R/'FAILED.json').write_bytes(enc(checks));(R/'FAILED.txt').write_text(traceback.format_exc());raise
