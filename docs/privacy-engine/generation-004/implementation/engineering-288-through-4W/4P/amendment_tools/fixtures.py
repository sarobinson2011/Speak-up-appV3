"""Regenerate independent conditional profiles and every dependent signed bundle."""
import json,sys,copy
from pathlib import Path
from fixtures.construct import dataset,wire,sha
from fixtures.field_class import literal
from fixtures.integrated import export
from v4_ingest.wire import decode_container
from v4_ingest.definition import ACTIVE,BINDING
from admission_kernel.admission import collect
ROOT=Path(__file__).resolve().parents[1]

def description(q,t):
    members=decode_container(bytes.fromhex(q['outer_hex']));p=json.loads(members['PRIVACY'])
    e=bytes.fromhex(q['security_records_hex'])
    return {'profile_id':p['profile_id'],'profile_sha256':sha(bytes.fromhex(q['outer_hex'])),'privacy_member_sha256':sha(members['PRIVACY']),
        'body_sha256':sha(members['SOURCE-OWNED-BODY']),'program_sha256':sha(members['EXPRESSION-PROGRAM']),
        'model_sha256':sha(wire(t['model'])),'security_sha256':sha(wire(p['security_contract'])),'external_records_sha256':sha(e),
        'source_id':p['format_source'],'source_sha256':p['format_source_sha256'],'definition_hashes':t['definition_hashes'],
        'procedure_bindings':p['procedures_sha256'],'selected_evidence_contract_sha256':sha(wire(t['evidence_contract'])),
        'source_materials':sorted(q['materials']),'source_objects':sorted(q['source_objects']),
        'bundles':{s:{'object_sha256':b['object_sha256'],'files':{n:{'bytes':len(bytes.fromhex(v)),'sha256':sha(bytes.fromhex(v))} for n,v in b['files'].items()}} for s,b in q['bundles'].items()}}

def historical(name):
    root=ROOT/('fixtures/4H-'+name);m=json.loads((root/'manifest.json').read_bytes());q=copy.deepcopy(m['request']);t=json.loads((root/'trusted.json').read_bytes())
    for n,e in m['records'].items():q[n]=(root/e['path']).read_bytes().hex()
    for n in ('materials','source_objects'):q[n]={h:(root/e['path']).read_bytes().hex() for h,e in m[n].items()}
    q['bundles']={s:{'object_sha256':b['object_sha256'],'files':{n:(root/e['path']).read_bytes().hex() for n,e in b['files'].items()}} for s,b in m['bundles'].items()}
    return q,t

def main():
    report={'format':'CP4I-CONDITIONAL-PROFILE-REBINDING-1','amendment_binding_sha256':sha((ACTIVE/'BINDING.json').read_bytes()),'cases':[],'full_retained_profile':'NOT-CONSTRUCTED: no complete qualified full profile existed to migrate','full_stream_processed':False,'actual_admission_enabled':False}
    for name in ('GAMMA','DELTA'):
        old=description(*historical(name))
        for kind,factory in [('ORDINARY',dataset),('RECORD',literal)]:
            q,t=factory(name);out=ROOT/('fixtures/4I-'+('RECORD-' if kind=='RECORD' else '')+name);m,tr=export(out,q,t)
            p=json.loads(decode_container(bytes.fromhex(q['outer_hex']))['PRIVACY']);register=[s['node_id'] for s in t['model']['surfaces']]
            (out/'field-register.json').write_bytes(wire(register));(out/'security.json').write_bytes(wire(p['security_contract']))
            label=next((r for r in p['security_contract']['policy']['field_labels'] if r['surface_id'].endswith('.$record')),p['security_contract']['policy']['field_labels'][0]);(out/'field-label.json').write_bytes(wire(label))
            (out/'request-hex.json').write_bytes(wire(q))
            r=collect(q,t);assert r['failures']==[],r
            new=description(q,t)
            changes={k:{'before':old[k],'after':new[k],'changed':old[k]!=new[k]} for k in old if k not in ('source_materials','source_objects','bundles')}
            unchanged_materials=set(old['source_materials'])&set(new['source_materials'])
            for h in unchanged_materials:assert bytes.fromhex(historical(name)[0]['materials'][h])==bytes.fromhex(q['materials'][h])
            if kind=='ORDINARY':
                assert old['model_sha256']==new['model_sha256']
                for scope in q['bundles']:
                    for n in ('tokens.tsv','links.tsv'):assert old['bundles'][scope]['files'][n]==new['bundles'][scope]['files'][n]
            assert old['profile_id']!=new['profile_id'] and old['profile_sha256']!=new['profile_sha256']
            report['cases'].append({'family':name,'kind':kind,'path':str(out.relative_to(ROOT)),'identities':changes,'old_bundles':old['bundles'],'new_bundles':new['bundles'],
                'verified_unchanged_materials':sorted(unchanged_materials),'new_or_changed_materials':sorted(set(new['source_materials'])-set(old['source_materials'])),
                'conditional_collector_result':r['result'],'profile_admitted':r['profile_admitted'],'external_qualification_established':r['actual_qualification_established']})
    (ROOT/'results/4I-profile-dependencies.json').write_bytes(wire(report));print(json.dumps({'result':'PASS','rebuilt_profiles':len(report['cases']),'rebound_bundles':3*len(report['cases'])}))
if __name__=='__main__':main()
