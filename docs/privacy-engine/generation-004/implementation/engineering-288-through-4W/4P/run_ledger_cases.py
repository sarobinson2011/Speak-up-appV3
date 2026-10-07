"""Saved conditional/adversarial ledger cases and executable constructor CLI."""
import copy,json,subprocess,sys,time
from pathlib import Path
from fixtures.construct import dataset,wire
from admission_kernel.admission import collect
from tests.test_admission import profile,bad_signature
from tests.test_ledger import change_source
from ledger_kernel.retained import sha

ROOT=Path(__file__).resolve().parent

def main():
    out=ROOT/'results/ledger-cases';out.mkdir(parents=True,exist_ok=False);rows=[]
    def case(name,q,t,expected):
        t0=time.monotonic();r=collect(q,t)
        ok=(r['earliest_failure']=='NONE') if expected=='PASS' else expected in r['failures']
        if expected=='PASS':assert r['result']=='CONDITIONAL-BINDING-AND-ADMISSION-CHECKS-PASS'
        assert ok and r['profile_admitted'] is False,(name,r)
        (out/(name+'.json')).write_text(json.dumps(r,indent=2)+'\n')
        rows.append({'case':name,'result':'PASS','expected':expected,'earliest_failure':r['earliest_failure'],'failures':r['failures'],
                     'request_sha256':sha_bytes(wire(q)),'source_contract_sha256':sha_bytes(wire(t)),
                     'seconds':time.monotonic()-t0,'profile_admitted':False})
    for name in ('GAMMA','DELTA'):
        q,t=dataset(name);case(name.lower()+'-conditional',q,t,'PASS');actual=copy.deepcopy(q);actual['mode']='ACTUAL';case(name.lower()+'-actual',actual,t,'INVALID-EVIDENCE-AUTHORITY')
        qp=ROOT/'fixtures'/(name.lower()+'-request.json');tp=ROOT/'fixtures'/(name.lower()+'-lab-contract.json')
        target=out/(name.lower()+'-constructed-static.json')
        run=subprocess.run([sys.executable,'-m','ledger_kernel',str(qp),'--lab-contract',str(tp),'--output',str(target)],capture_output=True,text=True,timeout=15)
        (out/(name.lower()+'-constructor.stdout.txt')).write_text(run.stdout);(out/(name.lower()+'-constructor.stderr.txt')).write_text(run.stderr)
        assert run.returncode==0,(run.stdout,run.stderr)
        r=json.loads(target.read_bytes());assert r['templates']=={k:profile(q)['security_contract'][k] for k in ('obligations','composition_rules')}
    q,t=dataset();del q['materials'][t['ledger_source_ref']['material_sha256']];case('missing-source-bytes',q,t,'MISSING-EVIDENCE')
    q,t=dataset();change_source(q,t,lambda v:v['duty_assignments'].pop());case('missing-duty',q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
    q,t=dataset();change_source(q,t,lambda v:v['obligations'][0].update(node_ids=['NO-SUCH-NODE']));case('incorrect-reference',q,t,'INVALID-PROFILE-SCHEMA')
    q,t=dataset();change_source(q,t,lambda v:v['duty_assignments'][0].update(obligation_ids=['G-OB-COLLISION']));case('conflicting-classification',q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
    q,t=dataset();change_source(q,t,lambda v:v['coverage'][0].update(structural=[]));case('insufficient-whole-view',q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
    q,t=dataset();del t['laboratory_assumptions']['composition-decomposition'];case('absent-qualification',q,t,'INVALID-EVIDENCE-AUTHORITY')
    q,t=dataset();change_source(q,t,lambda v:v['compositions']['G-RULE-COLLISION'].update(multiplicities=[2]));case('incorrect-multiplicity',q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
    q,t=dataset('DELTA',maximum=[1,8]);case('exceeded-budget',q,t,'CORRELATION-FAILURE')
    q,t=dataset(degenerate=True);case('nonvacuity-scope-failure',q,t,'INVALID-ACTION-CONTEXT')
    q,t=dataset(unavailable=True);case('unavailable-not-zero',q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
    q,t=dataset();bad_signature(q);change_source(q,t,lambda v:v['duty_assignments'].pop());case('authentication-precedence',q,t,'INVALID-EVIDENCE-AUTHENTICATION')
    (out/'results.json').write_text(json.dumps({'result':'PASS','cases':rows,'constructor_cli_cases':2,'full_model_admission':False,'full_pair_or_link_stream_executed':False},indent=2)+'\n')
    print(json.dumps({'result':'PASS','ledger_cases':len(rows),'constructor_CLI_cases':2}))

def sha_bytes(raw):
    import hashlib
    return hashlib.sha256(raw).hexdigest()

if __name__=='__main__':main()
