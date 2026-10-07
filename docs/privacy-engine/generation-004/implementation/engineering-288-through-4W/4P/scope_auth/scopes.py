"""Independent source-owned scopes, exact closure and per-bundle view binding.

CP4E metadata is one concrete finite laboratory source mechanism; it adds no
accepted protocol fields and provides no actual source appointment.
"""
import io
from pathlib import Path
from v4_ingest.records import canonical,digest,exact,require,ValidationError
from admission_kernel.sources import MissingMaterial
from ledger_kernel.validate import COMP_ROLES
from .closure import Closure,ScopedModel
from .material import payload as source_payload
from link_stream.validator import ModelIndex,validate_reader,require_complete
SCOPES=('ROOT-ELIGIBLE','SCOPED-USED','NOT-APPLICABLE')
CODE_FILES=('ledger_kernel/construct.py','occurrence_values/generated.py','occurrence_values/projection.py','link_stream/validator.py','occurrence_values/acquire.py','occurrence_values/index.py','occurrence_values/codec.py','recovery_schedule/state.py','recovery_schedule/native.py','recovery_schedule/index.py','recovery_schedule/runner.py','link_recovery/cli.py','link_recovery/worker.cpp','link_recovery/worker','semantic_stream/storage.py','semantic_stream/provider.py','scope_auth/auth.py','scope_auth/closure.py','scope_auth/scopes.py','scope_auth/material.py','scope_auth/acquisition.py','admission_kernel/admission.py','v4_ingest/wire.py','integrated_auth/adapters.py','integrated_auth/backend.py','integrated_auth/collector.py','pure_auth/controller.py','large_auth/core.py','large_auth/message.py','crypto_backend/BUILD-MANIFEST.json','v4_ingest/records.py','v4_ingest/definition.py','amendments/PE-G4-FIELD-CLASS-REF-AMENDMENT-001/v1.0.0/BINDING.json')

def validate(provider,trusted,request,profile,security,model,ledger,role_ready,bundles,authentication,values,failures,adapter=None):
    report={'source_acquired':False,'scopes':{},'ready':False,'qualification':'NOT-ESTABLISHED',
            'actual_qualification_established':False,'profile_admitted':False,'potential_pairs_enumerated':False}
    def attempt(fn,label):
        try:return fn()
        except MissingMaterial as e:failures.add('MISSING-EVIDENCE','scope '+label+': '+str(e))
        except (ValidationError,ValueError,KeyError,TypeError,IndexError,OSError) as e:
            from admission_kernel.failures import ORDER
            code='MISSING-EVIDENCE' if isinstance(e,OSError) else getattr(e,'category','INVALID-PROFILE-SCHEMA')
            failures.add(code if code in ORDER else 'INVALID-PROFILE-SCHEMA','scope '+label+': '+str(e))
        return None
    ref=trusted.get('scope_source_ref')
    if ref is None:
        failures.add('MISSING-EVIDENCE','independent source-owned component seeds/scope law absent')
        failures.add('INCOMPLETE-EVIDENCE-UNIVERSE','complete three-scope closure unavailable');return report
    def source():
        s=source_payload(provider,ref);provider.construction([ref])
        exact(s,('format','model_digest','security_digest','body_sha256','program_sha256','validator_sha256','seeds','required_views'))
        require(s['format']=='CP4E-FINITE-SCOPE-SOURCE-V1','supported source scope grammar',category='INCOMPLETE-EVIDENCE-UNIVERSE')
        require(s['model_digest']==model.digest and s['security_digest']==digest(canonical(security)) and s['body_sha256']==digest(__import__('semantic_stream.storage',fromlist=['unhex']).unhex(trusted['body_hex'])) and s['program_sha256']==digest(__import__('semantic_stream.storage',fromlist=['unhex']).unhex(trusted['program_hex'])),'source model/security/body/program binding',category='INVALID-ACTION-CONTEXT')
        require(s['validator_sha256']=={n:digest((Path(__file__).resolve().parents[1]/n).read_bytes()) for n in CODE_FILES},'exact scope/acquisition/authentication mechanism code identities',category='INVALID-EVIDENCE-AUTHORITY')
        exact(s['seeds'],SCOPES[:2]);exact(s['required_views'],SCOPES)
        expected=[];rules=security['composition_rules']['records']
        for x in security['experiments']:
            rs=[r for r in rules if r['experiment_id']==x['experiment_id']]
            require(len(rs)==1,'complete experiment rule',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            expected.append({'experiment_id':x['experiment_id'],'target_id':x['target_id'],'coalition_id':x['coalition_id'],
                 'qualification_id':rs[0]['qualification_id'],'composition_id':rs[0]['composition_id'],
                 'obligation_ids':[o['obligation_id'] for o in security['obligations'] if o['experiment_id']==x['experiment_id']],
                 'coverage':'WHOLE-EXPERIMENT-VIEW'})
        require(expected and all(s['required_views'][scope]==expected for scope in SCOPES),'finite source law requires every whole experiment/target/view in each scope',category='INCOMPLETE-EVIDENCE-UNIVERSE')
        return s
    s=attempt(source,'source acquisition/binding')
    if s is None:return report
    report['source_acquired']=True;report['source_reference']=ref
    graph=attempt(lambda:Closure(model,request['phase'],values),'full graph closure')
    if graph is None:return report
    refs=trusted.get('scope_binding_refs',{})
    if set(refs)!=set(SCOPES):failures.add('MISSING-EVIDENCE','three independently bound scope result source objects required')
    for scope in SCOPES:
        item={'closure_established':False,'bundle_bound':False,'ready':False,'qualification':'NOT-ESTABLISHED'}
        report['scopes'][scope]=item
        def one(scope=scope,item=item):
            indices=list(range(len(model.tokens))) if scope=='NOT-APPLICABLE' else graph.selected(s['seeds'][scope])
            scoped=ScopedModel(model,indices)
            item['node_indices']=indices;item['seed_ids']=[] if scope=='NOT-APPLICABLE' else s['seeds'][scope]
            item['closure_established']=True
            if scope not in bundles:raise MissingMaterial('parsed authenticated bundle '+scope)
            files,parsed=bundles[scope]
            def scoped_files():
                if adapter is not None:return adapter.scoped_files(scope,scoped,request,values,parsed)
                phase='STATIC-ADMISSION' if request['phase']=='STATIC-ADMISSION' else 'E'
                sv=None if values is None else {k:values[k] for k in scoped.ids}
                stream=require_complete(validate_reader(io.BytesIO(files['links.tsv']),ModelIndex(scoped,phase,sv),parsed['evidence']['links_sha256']))
                require(files['tokens.tsv']==scoped.token_table(request['phase'],values),'exact scoped token bytes in retained order',category='INCOMPLETE-EVIDENCE-UNIVERSE')
                return stream
            # Source assertion failure must not hide independently detectable TSV
            # grammar/universe failures or change their accepted ORDER precedence.
            stream=attempt(scoped_files,scope+' scoped files')
            if stream is not None:item['link_validation']=stream
            if scope not in refs:raise MissingMaterial('bound source assertion '+scope)
            a=source_payload(provider,refs[scope])
            exact(a,('format','scope','source_scope_ref','profile_digest','model_digest','phase','bundle_object_sha256',
                     'file_identities','security_records_sha256','ledger_source_ref','closure_node_indices','views'))
            require(a['format']=='CP4E-FINITE-SCOPE-BINDING-V1','scope binding source grammar')
            require(a['scope']==scope and a['phase']==request['phase'] and a['source_scope_ref']==ref and a['model_digest']==model.digest,'scope source/phase/model correspondence',category='INVALID-ACTION-CONTEXT')
            require(a['profile_digest']==request['profile_digest'],'scope final outer-profile binding',category='PROFILE-DIGEST-MISMATCH')
            require(a['ledger_source_ref']==trusted['ledger_source_ref'] and a['security_records_sha256']==(adapter.security_digest() if adapter is not None else digest(bytes.fromhex(request['security_records_hex']))),'scope exact ledger/evidence invocation correspondence',category='INVALID-ACTION-CONTEXT')
            require(a['bundle_object_sha256']==parsed['object_sha256'] and a['file_identities']==(adapter.file_identities(scope) if adapter is not None else {n:{'bytes':len(b),'sha256':digest(b)} for n,b in files.items()}),'scope source exact four-file object correspondence',category='INVALID-EVIDENCE-DIGEST')
            require(a['closure_node_indices']==indices,'source assertion complete least closure (no omitted or extraneous nodes)',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            require(a['views']==s['required_views'][scope],'every exact relevant experiment/target/whole view bound independently for this bundle',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            item['bundle_bound']=stream is not None
            needed=set(COMP_ROLES)|{'evidence-authority','profile-adequacy','applicability'}
            ready=(stream is not None and request['mode']=='CONDITIONAL-LAB' and all(role_ready.get(r) for r in needed)
                   and authentication.get(scope,{}).get('complete',False) and ledger['classification_ready']
                   and all(v['composition_id'] in ledger['ready_rules'] and v['experiment_id'] in ledger['nv_ready'] for v in a['views']))
            require(ready,'scope authentication/ledger/qualification prerequisites unavailable',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            item['ready']=True;item['qualification']='EXPLICIT-LAB-ASSUMPTIONS-ONLY';return True
        attempt(one,scope)
    report['ready']=all(x['ready'] for x in report['scopes'].values())
    if report['ready']:report['qualification']='EXPLICIT-LAB-ASSUMPTIONS-ONLY'
    else:failures.add('INCOMPLETE-EVIDENCE-UNIVERSE','three distinct scopes not all completely bound and conditionally qualified')
    return report
