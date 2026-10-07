import copy,json,unittest
from fractions import Fraction
from fixtures.construct import dataset,wire,sha
from tests.test_admission import evidence,set_evidence,profile,bad_signature,mutate_profile
from admission_kernel.admission import collect
from admission_kernel.failures import ORDER
from ledger_kernel.coverage import normalized,union,potential_stripe_counts,weighted_count
from v4_ingest.records import ValidationError

def source(q,t):return json.loads(bytes.fromhex(q['materials'][t['ledger_source_ref']['material_sha256']]))['payload']
def change_source(q,t,fn):
    r=t['ledger_source_ref'];v=source(q,t);fn(v);raw=wire({'format':'CP3-LAB-MATERIAL-V1','payload':v,'dependencies':[]});d=sha(raw)
    q['materials'][d]=raw.hex();r['material_sha256']=d;t['anchors'][r['source_anchor']]=d
def mutate_e(q,schema,fn):
    v=evidence(q);fn(v['records'][schema]['instances']);set_evidence(q,v)

class LedgerTests(unittest.TestCase):
    def reject(self,q,t,*codes):
        r=collect(q,t);self.assertEqual(r['result'],'REJECTED',r)
        for code in codes:self.assertIn(code,r['failures'],r)
        self.assertEqual(r['failures'],[c for c in ORDER if c in r['failures']])
        self.assertFalse(r['profile_admitted']);return r
    def test_independent_full_finite_sources_pass_conditionally(self):
        for name,n,s,p in [('GAMMA',4,2,6),('DELTA',6,2,15)]:
            q,t=dataset(name);r=collect(q,t);self.assertEqual(r['earliest_failure'],'NONE',r)
            v=r['bindings']['ledger_validation'];self.assertEqual(v['coverage'],{'nodes':n,'structural_occurrences':s,'potential_pairs':p,'pair_enumeration':False})
            self.assertEqual(len(v['ready_obligations']),4);self.assertEqual(len(v['ready_rules']),3);self.assertEqual(len(v['nv_ready']),3)
            self.assertEqual(v['qualification'],'EXPLICIT-LAB-ASSUMPTIONS-ONLY');self.assertFalse(v['actual_qualification_established'])
    def test_remove_ledger_source_is_missing_not_empty_success(self):
        q,t=dataset();del t['ledger_source_ref'];r=self.reject(q,t,'MISSING-EVIDENCE','INCOMPLETE-EVIDENCE-UNIVERSE')
        self.assertTrue(all(x=='NOT-ESTABLISHED' for x in r['bindings']['computed_dispositions'].values()));self.assertEqual(r['bindings']['computed_budgets'],{})
    def test_absent_source_bytes_digest_and_anchor_errors(self):
        for change,code in [('missing','MISSING-EVIDENCE'),('digest','INVALID-EVIDENCE-DIGEST'),('anchor','INVALID-EVIDENCE-AUTHORITY')]:
            q,t=dataset();ref=t['ledger_source_ref'];d=ref['material_sha256']
            if change=='missing':del q['materials'][d]
            elif change=='digest':q['materials'][d]=b'wrong'.hex()
            else:t['anchors'][ref['source_anchor']]='0'*64
            self.reject(q,t,code,'INCOMPLETE-EVIDENCE-UNIVERSE')
    def test_every_exact_duty_family_is_required(self):
        for i in range(8):
            q,t=dataset();change_source(q,t,lambda v:v['duty_assignments'].pop(i));self.reject(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
    def test_conflicting_exact_computational_assignment(self):
        q,t=dataset();change_source(q,t,lambda v:v['duty_assignments'][0].update(obligation_ids=['G-OB-COLLISION']))
        self.reject(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
    def test_duplicate_classification_and_missing_obligation(self):
        q,t=dataset();change_source(q,t,lambda v:v['duty_assignments'].append(v['duty_assignments'][0]));self.reject(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
        q,t=dataset();change_source(q,t,lambda v:v['obligations'].pop());self.reject(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
    def test_missing_node_structural_and_potential_coverage(self):
        for field in ('nodes','structural','potential_left'):
            q,t=dataset();change_source(q,t,lambda v:[r.update({field:[]}) for r in v['coverage']]);self.reject(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
    def test_illegal_or_duplicate_coverage_intervals(self):
        for ranges in ([[0,5]],[[0,2],[1,4]],[[0,2],[2,4]],[[0,0]],[[True,4]]):
            q,t=dataset();change_source(q,t,lambda v:v['coverage'][0].update(nodes=ranges));self.reject(q,t)
    def test_duplicate_count_cannot_replace_missing_stripe(self):
        q,t=dataset();change_source(q,t,lambda v:[r.update(potential_left=[[0,1]]) for r in v['coverage'] if r['potential_left']])
        r=self.reject(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE');self.assertLessEqual(r['bindings']['ledger_validation']['coverage']['potential_pairs'],3)
    def test_wrong_model_policy_target_and_coalition_binding(self):
        for field,val,code in [('model_digest','0'*64,'INVALID-ACTION-CONTEXT'),('policy_id','OTHER','INVALID-ACTION-CONTEXT'),('target_ids',[],'INCOMPLETE-EVIDENCE-UNIVERSE'),('coalition_ids',[],'INCOMPLETE-EVIDENCE-UNIVERSE')]:
            q,t=dataset();change_source(q,t,lambda v:v.update({field:val}));self.reject(q,t,code)
    def test_reference_outside_claimed_scope(self):
        q,t=dataset();change_source(q,t,lambda v:v['coverage'][0].update(nodes=[[1,4]]));self.reject(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
    def test_missing_external_disposition(self):
        q,t=dataset();mutate_e(q,'OBLIGATION',lambda rs:rs.pop());self.reject(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
    def test_forged_exact_disposition_and_computational_waiver(self):
        q,t=dataset();mutate_e(q,'OBLIGATION',lambda rs:next(r for r in rs if r['kind']=='EXACT').update(disposition='COMPUTATIONALLY-BOUNDED',argument_ids=['G-ARG-COLLISION']))
        self.reject(q,t,'INVALID-PROFILE-SCHEMA','INCOMPLETE-EVIDENCE-UNIVERSE')
    def test_missing_classification_and_composition_qualification_cannot_budget_pass(self):
        for role in ('model-ledger-classification','composition-decomposition','non-vacuity','observer-completeness'):
            q,t=dataset();del t['laboratory_assumptions'][role];r=self.reject(q,t,'INVALID-EVIDENCE-AUTHORITY','INCOMPLETE-EVIDENCE-UNIVERSE')
            self.assertEqual(r['bindings']['computed_budgets'],{})
            if role in ('model-ledger-classification','observer-completeness'):
                self.assertEqual(r['bindings']['computed_dispositions']['G-OB-EXACT'],'NOT-ESTABLISHED')
            for oid,disp in r['bindings']['computed_dispositions'].items():
                if oid!='G-OB-EXACT':self.assertEqual(disp,'NOT-ESTABLISHED')
    def test_missing_composition_terms_or_wrong_multiplicity(self):
        for which in ('delete','count','ids','scope'):
            q,t=dataset()
            def change(v):
                r=v['compositions']['G-RULE-COLLISION']
                if which=='delete':del v['compositions']['G-RULE-COLLISION']
                elif which=='count':r['multiplicities']=[2]
                elif which=='ids':r['argument_ids']=['G-ARG-ACTOR-INFORMATION']
                else:r['experiment_sha256']='0'*64
            change_source(q,t,change);self.reject(q,t)
    def test_insufficient_whole_view_and_missing_nv_binding(self):
        for fn in (lambda v:v['whole_view_experiments'].pop(),lambda v:v.update(nv_input_sha256='0'*64),lambda v:v['compositions']['G-RULE-COLLISION'].update(obligation_ids=[])):
            q,t=dataset();change_source(q,t,fn);r=self.reject(q,t)
            self.assertLess(len(r['bindings']['ledger_validation']['ready_rules']),3)
    def test_nv_runs_even_when_argument_omitted(self):
        q,t=dataset(degenerate=True);v=evidence(q);v['records']['ARGUMENT']={'status':'UNAVAILABLE','justification':None,'instances':[]};set_evidence(q,v)
        self.reject(q,t,'INVALID-ACTION-CONTEXT','INCOMPLETE-EVIDENCE-UNIVERSE')
    def test_maximum_one_schema_fail_and_zero_maximum_meaning(self):
        q,t=dataset(maximum=[1,1]);self.reject(q,t,'INVALID-PROFILE-SCHEMA')
        q,t=dataset('GAMMA',maximum=[0,1]);self.assertEqual(collect(q,t)['earliest_failure'],'NONE')
        q,t=dataset('DELTA',maximum=[0,1]);self.reject(q,t,'CORRELATION-FAILURE','ACTOR-RECONSTRUCTION-RISK')
    def test_exact_union_multiplicities_cap_and_exceeded(self):
        q,t=dataset('DELTA',multiplicity=5);r=self.reject(q,t,'CORRELATION-FAILURE','ACTOR-RECONSTRUCTION-RISK')
        self.assertEqual(r['bindings']['computed_budgets']['D-EXP-CROSS-ACTION-TRACKING']['bound'],[1,1])
    def test_source_repetitions_exceeding_envelope_fail_scope(self):
        q,t=dataset('DELTA',multiplicity=101);r=self.reject(q,t,'INVALID-ACTION-CONTEXT','INCOMPLETE-EVIDENCE-UNIVERSE')
        self.assertEqual(r['bindings']['computed_budgets'],{})
    def test_repetition_unit_and_exact_count_required(self):
        for fn in (lambda r:r.update(multiplicity_units=['UNKNOWN']),lambda r:r.update(repetition_indices=[[[0,2]]])):
            q,t=dataset();change_source(q,t,lambda v:fn(v['compositions']['G-RULE-COLLISION']));self.reject(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
    def test_unknown_assessment_is_not_zero_term(self):
        q,t=dataset(unavailable=True);r=self.reject(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE');self.assertEqual(r['bindings']['computed_budgets'],{})
    def test_bad_signature_not_masked_by_bad_ledger(self):
        q,t=dataset();bad_signature(q);change_source(q,t,lambda v:v['duty_assignments'].pop())
        r=self.reject(q,t,'INVALID-EVIDENCE-AUTHENTICATION','INCOMPLETE-EVIDENCE-UNIVERSE');self.assertEqual(r['earliest_failure'],'INVALID-EVIDENCE-AUTHENTICATION')
    def test_laboratory_qualification_never_actual(self):
        q,t=dataset();q['mode']='ACTUAL';r=self.reject(q,t,'INVALID-EVIDENCE-AUTHORITY')
        self.assertFalse(r['actual_qualification_established']);self.assertEqual(r['bindings']['ledger_validation']['qualification'],'NOT-ESTABLISHED')
        self.assertEqual(r['bindings']['computed_budgets'],{})
        self.assertTrue(all(x=='NOT-ESTABLISHED' for x in r['bindings']['computed_dispositions'].values()))
        self.assertEqual(r['bindings']['ledger_validation']['nv_ready'],[])
    def test_other_experiment_coverage_cannot_fill_missing_interaction_scope(self):
        q,t=dataset();change_source(q,t,lambda v:next(r for r in v['coverage'] if r['obligation_id']=='G-OB-COLLISION').update(structural=[]))
        self.reject(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
    def test_unsupported_composition_has_no_computational_disposition(self):
        q,t=dataset(theorem=True)
        # Remove exact theorem bytes while leaving all argument arithmetic valid.
        rule=profile(q)['security_contract']['composition_rules']['records'][0]
        del q['materials'][rule['theorem_ref']['material_sha256']]
        r=self.reject(q,t,'MISSING-EVIDENCE','INCOMPLETE-EVIDENCE-UNIVERSE')
        for oid,d in r['bindings']['computed_dispositions'].items():
            if oid!='G-OB-EXACT':self.assertEqual(d,'NOT-ESTABLISHED')
    def test_unavailable_nv_never_establishes_a_bound(self):
        from unittest.mock import patch
        with patch('admission_kernel.sources.FiniteLabProvider.nonvacuity',return_value={'status':'UNAVAILABLE','bound':None,'reason':'missing support assessment'}):
            q,t=dataset();r=self.reject(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE');self.assertEqual(r['bindings']['computed_budgets'],{})
    def test_potential_stripe_counts_independent_exhaustive_oracle(self):
        import random
        for seed in range(50):
            rnd=random.Random(seed);ts=[{'arbitrary':bool(rnd.randrange(2)),'symbolic_digest':str(rnd.randrange(3))} for i in range(rnd.randrange(2,18))]
            expected=[sum(ts[i]['arbitrary'] or ts[j]['arbitrary'] or ts[i]['symbolic_digest']==ts[j]['symbolic_digest'] for j in range(i+1,len(ts))) for i in range(len(ts))]
            self.assertEqual(potential_stripe_counts(ts),expected)
            self.assertEqual(weighted_count(union([[[0,len(ts)-1]],[[0,1]]]),expected),sum(expected))

if __name__=='__main__':unittest.main()
