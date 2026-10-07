import copy,hashlib,io,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat
from fixtures.construct import dataset,wire,sha,l64,tsv,EVIDENCE_HEADER
from fixtures.scope_cases import disconnected,export,change_material
from tests.test_admission import profile,evidence,set_evidence,bad_signature
from admission_kernel.admission import collect
from admission_kernel.model import Model
from admission_kernel.failures import Failures,ORDER
from admission_kernel.sources import MissingMaterial
from scope_auth.auth import authenticate
from scope_auth.closure import Closure,ScopedModel
from scope_auth.acquisition import acquire,read_blob
from link_stream.validator import ModelIndex,validate_chunks
from v4_ingest.records import ValidationError

class ScopeAuthTests(unittest.TestCase):
    def reject(self,q,t,code):
        r=collect(q,t);self.assertEqual(r['result'],'REJECTED',r);self.assertIn(code,r['failures'],r)
        self.assertEqual(r['failures'],[x for x in ORDER if x in r['failures']]);self.assertFalse(r['profile_admitted']);return r
    def test_connected_and_disconnected_signed_integration(self):
        for q,t in (dataset(),disconnected()):
            r=collect(q,t);self.assertEqual(r['failures'],[],r);self.assertTrue(r['bindings']['scope_validation']['ready']);self.assertFalse(r['actual_qualification_established'])
        sizes={k:len(v['node_indices']) for k,v in r['bindings']['scope_validation']['scopes'].items()}
        self.assertEqual(sizes,{'ROOT-ELIGIBLE':2,'SCOPED-USED':2,'NOT-APPLICABLE':6})
    def test_exact_compact_closure_against_independent_exhaustive_oracle(self):
        import random
        rng=random.Random(2884)
        # Pure graph oracle includes no validator closure or pair-count helper.
        for trial in range(80):
            n=9;tokens=[{'index':i,'id':str(i),'arbitrary':rng.choice([True,False]) if trial<40 else False,'symbolic_digest':str(rng.randrange(3))} for i in range(n)]
            edges=[[i,j,1,'R'] for i in range(n) for j in range(i+1,n) if rng.random()<.04]
            class M:pass
            m=M();m.tokens=tokens;m.ids={t['id']:t['index'] for t in tokens};m.edges=edges
            values={str(i):bytes([rng.randrange(4)]) for i in range(n)}
            for phase in ('STATIC-ADMISSION','PRE-EXECUTION','PRE-COMMITMENT'):
                adj=[set() for _ in range(n)]
                for i,j,_,_ in edges:adj[i].add(j);adj[j].add(i)
                for i in range(n):
                    for j in range(i+1,n):
                        legal=tokens[i]['arbitrary'] or tokens[j]['arbitrary'] or tokens[i]['symbolic_digest']==tokens[j]['symbolic_digest'] if phase=='STATIC-ADMISSION' else values[str(i)]==values[str(j)]
                        if legal:adj[i].add(j);adj[j].add(i)
                c=Closure(m,phase,values)
                for seed in range(n):
                    seen={seed};todo=[seed]
                    while todo:
                        for j in adj[todo.pop()]:
                            if j not in seen:seen.add(j);todo.append(j)
                    self.assertEqual(c.selected([str(seed)]),sorted(seen))
    def test_scoped_stream_preserves_original_indexes_across_chunks(self):
        q,t=disconnected();model=Model(t['model'])
        for scope,indices in [('ROOT-ELIGIBLE',[0,3]),('SCOPED-USED',[1,4]),('NOT-APPLICABLE',list(range(6)))]:
            raw=bytes.fromhex(q['bundles'][scope]['files']['links.tsv']);index=ModelIndex(ScopedModel(model,indices))
            for size in (1,2,7,31,4096):
                r=validate_chunks((raw[i:i+size] for i in range(0,len(raw),size)),index,sha(raw));self.assertTrue(r['complete'],r)
    def test_missing_external_authority(self):
        q,t=dataset();del t['appointment'];self.reject(q,t,'INVALID-EVIDENCE-AUTHORITY')
    def test_wrong_external_key_and_self_appointment_rejected(self):
        q,t=dataset();t['appointment']['public_key']='ab'*32;t['appointment']['key_fingerprint_sha256']=sha(bytes.fromhex('ab'*32));r=self.reject(q,t,'INVALID-EVIDENCE-AUTHORITY');self.assertIn('INVALID-EVIDENCE-AUTHENTICATION',r['failures'])
    def test_missing_evidence_authority_role(self):
        q,t=dataset();del t['laboratory_assumptions']['evidence-authority'];r=self.reject(q,t,'INVALID-EVIDENCE-AUTHORITY');self.assertFalse(r['bindings']['scope_validation']['ready'])
    def test_missing_scope_source(self):
        q,t=dataset();del t['scope_source_ref'];self.reject(q,t,'MISSING-EVIDENCE')
    def test_missing_source_bytes(self):
        q,t=dataset();del q['materials'][t['scope_source_ref']['material_sha256']];self.reject(q,t,'MISSING-EVIDENCE')
    def test_changed_source_bytes_same_digest_key(self):
        q,t=dataset();q['materials'][t['scope_source_ref']['material_sha256']]+='20';self.reject(q,t,'INVALID-EVIDENCE-DIGEST')
    def test_wrong_source_owner(self):
        q,t=dataset();t['scope_source_ref']['owner_source_id']='WRONG';self.reject(q,t,'INVALID-EVIDENCE-AUTHORITY')
    def test_empty_or_foreign_seed(self):
        for seeds,code in [([], 'INCOMPLETE-EVIDENCE-UNIVERSE'),(['FOREIGN'],'INVALID-ACTION-CONTEXT')]:
            q,t=dataset();change_material(q,t,t['scope_source_ref'],lambda s:s['seeds'].__setitem__('ROOT-ELIGIBLE',seeds));self.reject(q,t,code)
    def test_incomplete_or_extraneous_claimed_closure(self):
        for selected in ([0],[0,1,3]):
            q,t=disconnected();change_material(q,t,t['scope_binding_refs']['ROOT-ELIGIBLE'],lambda s:s.__setitem__('closure_node_indices',selected));self.reject(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
    def test_wrong_scope_cross_bundle_substitution(self):
        q,t=disconnected();q['bundles']['ROOT-ELIGIBLE']=copy.deepcopy(q['bundles']['SCOPED-USED']);self.reject(q,t,'INVALID-ACTION-CONTEXT')
    def test_source_assertion_cross_bundle_substitution(self):
        q,t=dataset();t['scope_binding_refs']['ROOT-ELIGIBLE']=copy.deepcopy(t['scope_binding_refs']['NOT-APPLICABLE']);self.reject(q,t,'INVALID-ACTION-CONTEXT')
    def test_missing_composition_cannot_be_replaced_by_component(self):
        q,t=dataset();del q['bundles']['NOT-APPLICABLE'];self.reject(q,t,'MISSING-EVIDENCE')
    def test_wrong_experiment_target_or_view(self):
        for field in ('experiment_id','target_id','coalition_id','qualification_id','coverage'):
            q,t=dataset();change_material(q,t,t['scope_binding_refs']['SCOPED-USED'],lambda s:s['views'][0].__setitem__(field,'WRONG'));self.reject(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
    def test_missing_required_experiment_in_source_law(self):
        q,t=dataset();change_material(q,t,t['scope_source_ref'],lambda s:s['required_views']['NOT-APPLICABLE'].pop());self.reject(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE')
    def test_wrong_outer_binding_in_source(self):
        q,t=dataset();change_material(q,t,t['scope_binding_refs']['ROOT-ELIGIBLE'],lambda s:s.__setitem__('profile_digest','0'*64));self.reject(q,t,'PROFILE-DIGEST-MISMATCH')
    def test_changed_record_bytes_not_transferable_to_old_scope(self):
        q,t=dataset();e=evidence(q);e['records']['ASSESSOR-EVENT']['instances'][0]['attempt_ordinal']+=1;set_evidence(q,e);self.reject(q,t,'INVALID-ACTION-CONTEXT')
    def test_digest_and_signature_failures_collected_before_malformed_records(self):
        q,t=dataset();bad_signature(q);q['security_records_hex']='00';r=self.reject(q,t,'INVALID-EVIDENCE-AUTHENTICATION');self.assertIn('INVALID-EVIDENCE-DIGEST',r['failures']);self.assertEqual(r['earliest_failure'],'INVALID-PROFILE-SCHEMA')
    def test_no_positive_ledger_disposition_through_signature_failure(self):
        q,t=dataset();bad_signature(q);r=self.reject(q,t,'INVALID-EVIDENCE-AUTHENTICATION');self.assertEqual(set(r['bindings']['computed_dispositions'].values()),{'NOT-ESTABLISHED'});self.assertEqual(r['bindings']['computed_budgets'],{})
    def test_signature_over_digest_is_rejected(self):
        q,t=dataset();b=q['bundles']['ROOT-ELIGIBLE'];files={n:bytes.fromhex(v) for n,v in b['files'].items()};key=Ed25519PrivateKey.from_private_bytes(sha(b'PUBLIC CP3 UNIT FIXTURE KEY GAMMA').encode()[:32])
        msg=b'PE-TSE-PRIVACY-EVIDENCE-V2\n'+b''.join(files[n] for n in ('evidence.tsv','tokens.tsv','links.tsv'))
        files['signature.txt']=(t['appointment']['authority_id']+' '+key.sign(hashlib.sha256(msg).digest()).hex()+'\n').encode()
        b['files']={n:v.hex() for n,v in files.items()};b['object_sha256']=sha(b'PE-TSE-PRIVACY-EVIDENCE-OBJECT-V2\n'+b''.join(l64(files[n]) for n in ('evidence.tsv','tokens.tsv','links.tsv','signature.txt')))
        self.reject(q,t,'INVALID-EVIDENCE-AUTHENTICATION')
    def test_exact_four_file_object_includes_signature(self):
        q,t=dataset();b=q['bundles']['ROOT-ELIGIBLE'];b['object_sha256']='0'*64;r=self.reject(q,t,'INVALID-EVIDENCE-DIGEST');self.assertNotIn('INVALID-EVIDENCE-AUTHENTICATION',r['failures'])
    def test_explicit_large_message_capability_fails_closed(self):
        q,t=dataset();f=Failures()
        with patch('scope_auth.auth.MAX_MESSAGE_BYTES',1):files,r=authenticate(q['bundles']['ROOT-ELIGIBLE'],t['appointment'],f)
        self.assertFalse(r['complete']);self.assertIn('INCOMPLETE-EVIDENCE-UNIVERSE',f.reasons)
    def test_file_acquisition_roundtrip(self):
        q,t=disconnected()
        with tempfile.TemporaryDirectory() as d:
            p=export(q,t,Path(d)/'fixture');out,receipt=acquire(json.loads(p.read_bytes()),p.parent)
            self.assertEqual(out,q);self.assertFalse(receipt['authentication_established_by_acquisition']);self.assertEqual(collect(out,t)['failures'],[])
    def test_same_size_changed_source_not_authenticated_by_metadata(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'source';p.write_bytes(b'abc');entry={'path':'source','bytes':3,'sha256':sha(b'abc')};self.assertEqual(read_blob(d,entry),b'abc');p.write_bytes(b'abd')
            with self.assertRaises(ValidationError):read_blob(d,entry)
    def test_missing_truncated_extraneous_file_bytes(self):
        for raw in (b'a',b'abcd'):
            with tempfile.TemporaryDirectory() as d:
                Path(d,'source').write_bytes(raw)
                with self.assertRaises(ValidationError):read_blob(d,{'path':'source','bytes':3,'sha256':sha(b'abc')})
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(MissingMaterial):read_blob(d,{'path':'missing','bytes':0,'sha256':sha(b'')})
    def test_path_escape_rejected(self):
        with self.assertRaises(ValidationError):read_blob('.',{'path':'../secret','bytes':0,'sha256':sha(b'')})
    def test_missing_transitive_source_binding_dependency(self):
        q,t=dataset();ref=t['scope_binding_refs']['ROOT-ELIGIBLE'];obj=json.loads(bytes.fromhex(q['materials'][ref['material_sha256']]))
        obj['dependencies']=['f'*64];raw=wire(obj);ref['material_sha256']=sha(raw);q['materials'][sha(raw)]=raw.hex();t['anchors'][ref['source_anchor']]=sha(raw)
        self.reject(q,t,'MISSING-EVIDENCE')
    def test_unavailable_arguments_cannot_report_ready_scope(self):
        q,t=dataset(unavailable=True);r=self.reject(q,t,'INCOMPLETE-EVIDENCE-UNIVERSE');self.assertFalse(r['bindings']['scope_validation']['ready'])
    def test_edge_reference_workaround_does_not_repair_field_label(self):
        import runpy
        from v4_ingest.records import validate_record,primitive
        g=runpy.run_path(str(Path(__file__).resolve().parents[1]/'accepted/definition-completion/v4_record_grammar.py'))
        row={'obligation_id':'REPRO','kind':'EXACT','target_ids':['TARGET'],'coalition_id':'COALITION','node_ids':[],
             'edge_ids':['G4-EQUALITY-PAIR-1-36511'],'experiment_id':None}
        g['record_shape']('OBLIGATION',row,True);validate_record('OBLIGATION',row,True)
        for fn in (primitive,g['primitive']):
            with self.assertRaises(ValueError):fn('ID','SECURITY:ALGORITHM.$record')
    def test_partial_acquisition_keeps_available_authentication_checks(self):
        q,t=dataset();bad_signature(q)
        with tempfile.TemporaryDirectory() as d:
            path=export(q,t,Path(d)/'fixture');manifest=json.loads(path.read_bytes())
            (path.parent/manifest['objects'][0]['blob']['path']).unlink()
            f=Failures();acquired,_=acquire(manifest,path.parent,f)
            self.assertIn('MISSING-EVIDENCE',f.reasons)
            result=collect(acquired,t);self.assertIn('INVALID-EVIDENCE-AUTHENTICATION',result['failures'])
    def test_scope_mechanism_identity_is_independently_bound(self):
        q,t=dataset();change_material(q,t,t['scope_source_ref'],lambda s:s['validator_sha256'].__setitem__('scope_auth/auth.py','0'*64));self.reject(q,t,'INVALID-EVIDENCE-AUTHORITY')
    def test_actual_mode_remains_disabled(self):
        q,t=disconnected();q['mode']='ACTUAL';r=self.reject(q,t,'INVALID-EVIDENCE-AUTHORITY');self.assertFalse(r['bindings']['scope_validation']['ready'])

if __name__=='__main__':unittest.main()
