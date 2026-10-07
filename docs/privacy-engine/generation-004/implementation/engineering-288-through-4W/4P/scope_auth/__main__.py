"""Small file-backed acquisition and ordered-collector CLI; never actual admission."""
import argparse,json
from pathlib import Path
from v4_ingest.records import parse,canonical,ValidationError
from admission_kernel.sources import MissingMaterial
from admission_kernel.failures import Failures
from admission_kernel.admission import collect
from .acquisition import acquire

def main():
    p=argparse.ArgumentParser();p.add_argument('manifest',type=Path);p.add_argument('--lab-contract',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
    if a.output.exists():p.error('choose a fresh output; evidence is never overwritten')
    try:
        acquisition_failures=Failures()
        q,receipt=acquire(parse(a.manifest.read_bytes()),a.manifest.parent,acquisition_failures)
        r=collect(q,parse(a.lab_contract.read_bytes()))
        if acquisition_failures.reasons:
            for code,reasons in r['reasons'].items():
                for reason in reasons:acquisition_failures.add(code,reason)
            bindings=r['bindings']
            if bindings:
                bindings['computed_dispositions']={k:'NOT-ESTABLISHED' for k in bindings.get('computed_dispositions',{})}
                bindings['computed_budgets']={}
                if 'scope_validation' in bindings:
                    bindings['scope_validation'].update(ready=False,conditional_checks_pass=False,qualification='NOT-ESTABLISHED')
                    for value in bindings['scope_validation']['scopes'].values():value.update(ready=False,qualification='NOT-ESTABLISHED')
            r=acquisition_failures.result(q.get('mode','ACTUAL'),bindings)
        r['acquisition']=receipt
    except (MissingMaterial,ValidationError,OSError,ValueError,KeyError,TypeError) as e:
        f=Failures();code='MISSING-EVIDENCE' if isinstance(e,(MissingMaterial,OSError)) else getattr(e,'category','INVALID-PROFILE-SCHEMA');f.add(code,'file acquisition: '+str(e));r=f.result('ACTUAL' if 'q' not in locals() else q.get('mode','ACTUAL'))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open('xb') as out:out.write(canonical(r))
    print(json.dumps({'result':r['result'],'earliest_failure':r['earliest_failure'],'profile_admitted':False,'output':str(a.output)}))
    return 0 if r['result']=='CONDITIONAL-BINDING-AND-ADMISSION-CHECKS-PASS' else 2
if __name__=='__main__':raise SystemExit(main())
