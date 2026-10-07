import ast
import copy
import json
import unittest
from pathlib import Path
from fractions import Fraction
from fixtures.construct import dataset, wire, sha, l64, tsv, EVIDENCE_HEADER, TOKEN_HEADER, LINK_HEADER
from admission_kernel.admission import collect
from admission_kernel.failures import ORDER, Failures
from admission_kernel.sources import ROLES, FiniteLabProvider, MissingMaterial
from admission_kernel.model import Model
from v4_ingest.records import ValidationError, field_digest
from v4_ingest.wire import decode_container, encode_container, object_digest, scalar, SCALAR_MODULUS
from v4_ingest.typed import Codec
from admission_kernel.observations import observe

ROOT = Path(__file__).resolve().parents[1]


def evidence(q): return json.loads(bytes.fromhex(q['security_records_hex']))
def set_evidence(q, e): q['security_records_hex'] = wire(e).hex()
def mutate_evidence(q, schema, fn):
    e = evidence(q); fn(e['records'][schema]['instances']); set_evidence(q, e)
def profile(q): return json.loads(decode_container(bytes.fromhex(q['outer_hex']))['PRIVACY'])
def mutate_profile(q, fn):
    members = decode_container(bytes.fromhex(q['outer_hex'])); p = json.loads(members['PRIVACY']); fn(p)
    members['PRIVACY'] = wire(p); q['outer_hex'] = encode_container(members).hex()
def bad_signature(q, scope='ROOT-ELIGIBLE'):
    files = q['bundles'][scope]['files']; sig = bytes.fromhex(files['signature.txt']).decode()
    issuer, value = sig.split(); value = ('0' if value[0]!='0' else '1')+value[1:]
    files['signature.txt'] = (issuer+' '+value+'\n').encode().hex()


class AdmissionTests(unittest.TestCase):
    def rejected(self, q, t, code):
        r = collect(q, t)
        self.assertEqual(r['result'], 'REJECTED', r)
        self.assertIn(code, r['failures'], r)
        self.assertFalse(r['profile_admitted'])
        return r

    def test_exact_inherited_order_from_accepted_ast(self):
        tree = ast.parse((ROOT/'accepted/privacy/observation_correlation.py').read_text())
        assignment = next(n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ORDER' for t in n.targets))
        self.assertEqual(ORDER, tuple(ast.literal_eval(assignment.value)))

    def test_two_independent_datasets_and_distinct_source_preimages(self):
        results = []
        for name in ('GAMMA','DELTA'):
            q,t = dataset(name); r = collect(q,t)
            self.assertEqual(r['earliest_failure'],'NONE',r)
            self.assertFalse(r['profile_admitted']);self.assertFalse(r['full_model_integration_witness'])
            results.append(r)
        self.assertNotEqual(results[0]['bindings']['model_sha256'],results[1]['bindings']['model_sha256'])
        self.assertEqual(results[0]['bindings']['computed_budgets']['G-EXP-CROSS-ACTION-TRACKING']['bound'],[0,1])
        self.assertEqual(results[1]['bindings']['computed_budgets']['D-EXP-CROSS-ACTION-TRACKING']['bound'],[1,4])

    def test_actual_mode_rejects_even_with_every_lab_hypothesis(self):
        for name in ('GAMMA','DELTA'):
            q,t=dataset(name);q['mode']='ACTUAL'
            r=self.rejected(q,t,'INVALID-EVIDENCE-AUTHORITY')
            self.assertEqual(r['earliest_failure'],'INVALID-EVIDENCE-AUTHORITY')

    def test_no_external_authority_rejects(self):
        q,t=dataset();r=self.rejected(q,None,'INVALID-EVIDENCE-AUTHORITY')
        self.assertFalse(r['actual_qualification_established'])

    def test_remove_each_qualification_separately(self):
        for name in ROLES:
            with self.subTest(role=name):
                q,t=dataset();del t['laboratory_assumptions'][name]
                self.rejected(q,t,'INVALID-EVIDENCE-AUTHORITY')

    def test_unqualified_invalid_is_not_a_known_violation(self):
        q,t=dataset(invalid_certificate=True);del t['laboratory_assumptions']['assessor-competence']
        r=self.rejected(q,t,'INVALID-EVIDENCE-AUTHORITY')
        self.assertNotIn('UNIQUENESS-FAILURE',r['failures'])

    def test_caller_valid_or_invalid_flags_do_not_establish_result(self):
        q,t=dataset()
        mutate_evidence(q,'ASSESSMENT',lambda rs:rs[0].update(complete_result='INVALID',validated_bound=None))
        r=self.rejected(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
        self.assertNotIn('ACTOR-RECONSTRUCTION-RISK',r['failures'])

    def test_qualified_invalid_uses_all_protected_experiment_codes(self):
        q,t=dataset(invalid_certificate=True);r=self.rejected(q,t,'UNIQUENESS-FAILURE')
        self.assertIn('CORRELATION-FAILURE',r['failures']);self.assertIn('ACTOR-RECONSTRUCTION-RISK',r['failures'])
        self.assertTrue(any('INVALID-ARGUMENT' in x for x in r['reasons']['UNIQUENESS-FAILURE']))

    def test_qualified_unavailable_null_bound_is_never_zero(self):
        q,t=dataset(unavailable=True);r=self.rejected(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
        self.assertEqual(r['bindings']['computed_budgets'],{})
        self.assertNotIn('UNIQUENESS-FAILURE',r['failures'])

    def test_unavailable_bound_with_number_is_schema_failure(self):
        q,t=dataset(unavailable=True)
        mutate_evidence(q,'ASSESSMENT',lambda rs:rs[0].update(validated_bound=[0,1]))
        self.rejected(q,t,'INVALID-PROFILE-SCHEMA')

    def test_bad_signature_and_later_unavailable_preserve_precedence(self):
        q,t=dataset(unavailable=True);bad_signature(q)
        r=self.rejected(q,t,'INVALID-EVIDENCE-AUTHENTICATION')
        self.assertEqual(r['earliest_failure'],'INVALID-EVIDENCE-AUTHENTICATION')
        self.assertIn('INCOMPLETE-EVIDENCE-UNIVERSE',r['failures']);self.assertIn('INVALID-EVIDENCE-DIGEST',r['failures'])

    def test_malformed_external_does_not_erase_authentication_failure(self):
        q,t=dataset();bad_signature(q);q['security_records_hex']=b'{'.hex()
        r=self.rejected(q,t,'INVALID-PROFILE-SCHEMA')
        self.assertIn('INVALID-EVIDENCE-AUTHENTICATION',r['failures'])

    def test_outer_vs_member_digest_binding(self):
        q,t=dataset();q['profile_digest']=sha(decode_container(bytes.fromhex(q['outer_hex']))['PRIVACY'])
        r=self.rejected(q,t,'PROFILE-DIGEST-MISMATCH');self.assertEqual(r['earliest_failure'],'PROFILE-DIGEST-MISMATCH')

    def test_signature_object_digest_is_distinct_from_signed_preimage(self):
        q,t=dataset();q['bundles']['SCOPED-USED']['object_sha256']='0'*64
        r=self.rejected(q,t,'INVALID-EVIDENCE-DIGEST');self.assertNotIn('INVALID-EVIDENCE-AUTHENTICATION',r['failures'])

    def test_missing_exact_policy_bytes_is_not_invented_bad_scope(self):
        q,t=dataset();p=profile(q);ref=p['security_contract']['policy']['record']['policy_source'];del q['materials'][ref['material_sha256']]
        r=self.rejected(q,t,'MISSING-EVIDENCE');self.assertEqual(r['earliest_failure'],'MISSING-EVIDENCE',r)

    def test_corrupt_exact_material_digest(self):
        q,t=dataset();ref=profile(q)['security_contract']['policy']['record']['policy_source'];q['materials'][ref['material_sha256']]=b'corrupt'.hex()
        self.rejected(q,t,'INVALID-EVIDENCE-DIGEST')

    def test_forged_anchor_with_matching_bytes_cannot_establish_source_assertion(self):
        q,t=dataset();e=evidence(q);ref=e['records']['ASSESSMENT']['instances'][0]['source_assertion_evidence'];raw=wire({'format':'CP3-LAB-MATERIAL-V1','payload':{'caller':'PASS'},'dependencies':[]})
        q['materials'][sha(raw)]=raw.hex();ref['material_sha256']=sha(raw);set_evidence(q,e)
        self.rejected(q,t,'INVALID-EVIDENCE-AUTHORITY')

    def test_missing_invocation_material_does_not_become_factual_invalid(self):
        q,t=dataset();ref=evidence(q)['records']['ASSESSMENT']['instances'][0]['invocation_source'];del q['materials'][ref['material_sha256']]
        r=self.rejected(q,t,'MISSING-EVIDENCE');self.assertNotIn('ACTOR-RECONSTRUCTION-RISK',r['failures'])

    def test_mechanism_code_and_codec_are_exact_contract_inputs(self):
        q,t=dataset();t['mechanism']['checker_sha256']='0'*64
        self.rejected(q,t,'INVALID-EVIDENCE-AUTHORITY')
        q,t=dataset();t['mechanism']['invocation_codec']='GENERIC-PASS'
        self.rejected(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')

    def test_hidden_final_digest_construction_input_rejects(self):
        q,t=dataset(static_cycle=True);self.rejected(q,t,'INVALID-PROFILE-SCHEMA')

    def test_exact_node_and_edge_identity_adapters(self):
        q,t=dataset();m=Model(t['model'])
        self.assertTrue(m.edge_identity('G4-STRUCTURAL-EDGE-1'));self.assertTrue(m.edge_identity('G4-EQUALITY-PAIR-0-1'))
        for value in ('G4-STRUCTURAL-EDGE-0','G4-STRUCTURAL-EDGE-01','G4-STRUCTURAL-EDGE-9','G4-EQUALITY-PAIR-1-0','G4-EQUALITY-PAIR-00-1','G4-EQUALITY-PAIR-0-8'):
            self.assertFalse(m.edge_identity(value),value)

    def test_orphan_obligation_model_ids_reject(self):
        q,t=dataset();mutate_profile(q,lambda p:p['security_contract']['obligations'][0]['node_ids'].append('ORPHAN'))
        self.rejected(q,t,'INVALID-PROFILE-SCHEMA')

    def test_omitted_and_misclassified_ledger_cannot_lower_required_coverage(self):
        q,t=dataset();mutate_evidence(q,'OBLIGATION',lambda rs:rs.pop())
        self.rejected(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
        q,t=dataset();mutate_evidence(q,'OBLIGATION',lambda rs:rs[0].update(disposition='EXACT-SATISFIED'))
        self.rejected(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')

    def test_unknown_visibility_overrides_low_budget(self):
        obs={'nodes':[{'id':'N','context':'C','exposure':'CONFIDENTIAL','reuse':'NONE','value_hex':'00','role':'NOT-APPLICABLE','source_domain':'LAB','action_hex':''}],
             'edges':[],'visibility':{'N':'UNKNOWN'}}
        q,t=dataset(observation=obs);r=self.rejected(q,t,'INVALID-SURFACE-LABELS');self.assertIn('INCOMPLETE-EVIDENCE-UNIVERSE',r['failures'])

    def test_known_actor_path_and_equal_cross_action_n_override_budgets(self):
        def node(n,c,exposure,role,v,a):return {'id':n,'context':c,'exposure':exposure,'reuse':'NONE','value_hex':Codec().encode('PE-TSE-UINT',v).hex() if role!='NOT-APPLICABLE' else 'aa',
                                             'role':role,'source_domain':'LAB','action_hex':Codec().encode('PE-TSE-UINT',a).hex() if role=='n' else ''}
        ns=[node('N1','ONE','PUBLIC','n',7,1),node('N2','TWO','PUBLIC','n',7,2),node('ACTOR','ONE','PRIVATE-ACTOR','NOT-APPLICABLE',0,0)]
        q,t=dataset(observation={'nodes':ns,'edges':[['N1','ACTOR','SOURCE']], 'visibility':{n['id']:'VISIBLE' for n in ns}})
        r=self.rejected(q,t,'UNIQUENESS-FAILURE');self.assertIn('CORRELATION-FAILURE',r['failures']);self.assertIn('ACTOR-RECONSTRUCTION-RISK',r['failures'])

    def test_scoped_public_root_action_duplicate_permissions(self):
        for role in ('r','a','n'):
            nodes=[{'id':n,'context':c,'exposure':'PUBLIC','reuse':'NONE','value_hex':Codec().encode('PE-TSE-UINT',4).hex(),'role':role,'source_domain':'EXACT-SOURCE-SCOPE',
                    'action_hex':Codec().encode('PE-TSE-UINT',9).hex() if role=='n' else ''} for n,c in [('A','ONE'),('B','TWO')]]
            if role=='n':
                nodes += [dict(nodes[i],id='ACTION-'+nodes[i]['context'],role='a',value_hex=nodes[i]['action_hex'],action_hex='') for i in (0,1)]
            f=Failures();observe({'nodes':nodes,'edges':[],'visibility':{n['id']:'VISIBLE' for n in nodes}},f);self.assertEqual(f.reasons,{})
            nodes[1]['source_domain']='OTHER-SCOPE';f=Failures();observe({'nodes':nodes,'edges':[],'visibility':{'A':'VISIBLE','B':'VISIBLE'}},f)
            self.assertIn('UNIQUENESS-FAILURE',f.reasons)

    def test_nonvacuity_identical_alternatives_rejects(self):
        q,t=dataset(degenerate=True);self.rejected(q,t,'INVALID-ACTION-CONTEXT')

    def test_zero_maximum_accepts_only_established_zero(self):
        q,t=dataset('GAMMA',maximum=[0,1]);self.assertEqual(collect(q,t)['earliest_failure'],'NONE')
        q,t=dataset('DELTA',maximum=[0,1]);r=self.rejected(q,t,'CORRELATION-FAILURE');self.assertIn('ACTOR-RECONSTRUCTION-RISK',r['failures'])

    def test_union_multiplicities_exact_sum_cap_and_exceeded_budget(self):
        q,t=dataset('DELTA',multiplicity=2);r=collect(q,t);self.assertEqual(r['earliest_failure'],'NONE',r)
        self.assertEqual(r['bindings']['computed_budgets']['D-EXP-ACTOR-INFORMATION']['bound'],[1,2])
        q,t=dataset('DELTA',multiplicity=5);r=self.rejected(q,t,'ACTOR-RECONSTRUCTION-RISK')
        self.assertEqual(r['bindings']['computed_budgets']['D-EXP-ACTOR-INFORMATION']['bound'],[1,1])

    def test_wrong_or_missing_composition_multiplicity_rejects(self):
        q,t=dataset('DELTA');mutate_evidence(q,'COMPOSITION',lambda rs:rs[0].update(multiplicities=[2]))
        self.rejected(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
        q,t=dataset();mutate_evidence(q,'COMPOSITION',lambda rs:rs[0].update(multiplicities=[0]))
        self.rejected(q,t,'INVALID-PROFILE-SCHEMA')

    def test_single_joint_qualified_theorem_and_no_generic_product(self):
        q,t=dataset('DELTA',theorem=True);self.assertEqual(collect(q,t)['earliest_failure'],'NONE')
        q,t=dataset('DELTA',theorem=True,multiplicity=2);self.rejected(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')

    def test_changed_invocation_preimage_or_source_premise_rejects(self):
        q,t=dataset();mutate_evidence(q,'ASSESSMENT',lambda rs:rs[0].update(exact_input_digest='0'*64))
        self.rejected(q,t,'INVALID-ACTION-CONTEXT')
        q,t=dataset();t['premises'].clear();self.rejected(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')

    def test_assessor_missing_retry_cache_and_bad_return_bytes(self):
        for event_kind in ('RETRY','CACHE'):
            q,t=dataset();mutate_evidence(q,'ASSESSOR-EVENT',lambda rs,k=event_kind:rs.__setitem__(slice(None),[r for r in rs if r['event_kind']!=k]))
            self.rejected(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
        q,t=dataset();mutate_evidence(q,'ASSESSOR-EVENT',lambda rs:next(r for r in rs if r['event_kind']=='RETURN').update(output_bytes='00'))
        self.rejected(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')

    def test_event_cycles_attempts_and_applicability_context(self):
        q,t=dataset();mutate_evidence(q,'ASSESSOR-EVENT',lambda rs:rs[0].update(predecessor_ids=[rs[0]['event_id']]))
        self.rejected(q,t,'INVALID-ACTION-CONTEXT')
        for field,value in [('mapping_digest','0'*64),('attempt_ordinal',9),('stage','E')]:
            q,t=dataset();mutate_evidence(q,'POLICY-APPLICABILITY',lambda rs:rs[0].update(**{field:value}))
            self.rejected(q,t,'INVALID-ACTION-CONTEXT')

    def test_missing_required_directories_and_issuer_inapplicability(self):
        for status in ('UNAVAILABLE','INAPPLICABLE'):
            q,t=dataset();e=evidence(q);d=e['records']['ASSESSMENT'];d.update(status=status,instances=[],justification=t['laboratory_assumptions']['assessor-competence'] if status=='INAPPLICABLE' else None)
            set_evidence(q,e);self.rejected(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')

    def test_actual_values_have_no_symbolic_fallback_and_canonical_typed_hash(self):
        q,t=dataset();m=Model(t['model'])
        with self.assertRaises(ValidationError):m.token_table('E',None)
        self.assertNotEqual(field_digest(None),field_digest(''))
        values={n:wire(i) for i,n in enumerate(m.ids)}
        raw=m.token_table('E',values);self.assertIn(sha(wire(0)).encode(),raw);self.assertNotIn(sha(b'ARBITRARY').encode(),raw)

    def test_full_static_links_membership_plus_count_without_pair_enumeration(self):
        q,t=dataset();m=Model(t['model'])
        from v4_ingest.wire import read_table
        rows=read_table(bytes.fromhex(q['bundles']['NOT-APPLICABLE']['files']['links.tsv']),LINK_HEADER)
        self.assertTrue(m.validate_links(rows,'STATIC-ADMISSION'))
        with self.assertRaises(ValidationError):m.validate_links(rows[:-1],'STATIC-ADMISSION')
        rows[0]['relation_class']='FAKE'
        with self.assertRaises(ValidationError):m.validate_links(rows,'STATIC-ADMISSION')

    def test_unverified_stream_null_cannot_be_final_member(self):
        q,t=dataset();mutate_profile(q,lambda p:p['model']['equality_stream'].update(sha256=None))
        self.rejected(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')

    def test_strict_scalar_and_no_field_reduction(self):
        self.assertEqual(scalar(SCALAR_MODULUS-1),SCALAR_MODULUS-1)
        for n in (-1,SCALAR_MODULUS,True):
            with self.assertRaises(ValidationError):scalar(n)

    def test_issuer_extra_true_flag_is_schema_failure(self):
        q,t=dataset();q['profile_admitted']=True
        self.rejected(q,t,'INVALID-PROFILE-SCHEMA')

    def test_public_private_reusable_identifier_and_opening_failures(self):
        for role,code in [('PRIVATE-VALUE','PUBLIC-PRIVATE-VALUE'),('REUSABLE-ACTOR-ID','REUSABLE-IDENTIFIER'),('PROTECTED-OPENING','OPENING-DISCLOSURE')]:
            node={'id':'PUBLIC-DISCLOSURE','context':'C','exposure':'PUBLIC','reuse':'NONE','value_hex':'aa','role':role,'source_domain':'OWNING-SOURCE','action_hex':''}
            q,t=dataset(observation={'nodes':[node],'edges':[],'visibility':{'PUBLIC-DISCLOSURE':'VISIBLE'}})
            self.rejected(q,t,code)

    def test_unnecessary_component_is_retained_alongside_count_failure(self):
        q,t=dataset();mutate_profile(q,lambda p:p['components'].append(dict(p['components'][0],id='EXTRA')))
        r=self.rejected(q,t,'COMPONENT-COUNT-MISMATCH');self.assertIn('UNNECESSARY-COMPONENT',r['failures'])

    def test_extra_material_accounting_order_and_effects_reject_two_bit_profile(self):
        for field in ('extra_material_predicates','extra_ordering','extra_effects'):
            q,t=dataset();e=evidence(q);ref=e['records']['POLICY-APPLICABILITY']['instances'][0]['context_source']
            obj=json.loads(bytes.fromhex(q['materials'][ref['material_sha256']]));obj['payload'][field]=['ADDITIONAL-REQUIREMENT']
            raw=wire(obj);q['materials'][sha(raw)]=raw.hex();ref['material_sha256']=sha(raw)
            t['anchors'][ref['source_anchor']]=sha(raw);t['applicability_context']=obj['payload'];set_evidence(q,e)
            self.rejected(q,t,'INVALID-ACTION-CONTEXT')

    def test_component_modes_types_and_duplicate_ids_are_closed(self):
        for field,value in [('mode','SOURCE-OWNED'),('canonical_type','PE-TSE-UINT'),('privacy','PUBLIC')]:
            q,t=dataset();mutate_profile(q,lambda p:p['components'][0].update(**{field:value}))
            self.rejected(q,t,'INVALID-PROFILE-SCHEMA')

    def test_symbolic_law_context_and_no_actor_graph_pruning(self):
        q,t=dataset()
        for field,value in [('arbitrary',False),('symbolic_digest','0'*64),('context','SAMPLED-ONE')]:
            m=copy.deepcopy(t['model']);m['tokens'][0][field]=value
            with self.assertRaises(ValidationError):Model(m)
        m=copy.deepcopy(t['model']);m['actor_graph_policy']='DROP-HIDDEN-EDGES'
        with self.assertRaises(ValidationError):Model(m)


if __name__=='__main__':unittest.main()
