"""Verify exact parent artifacts; recompile catalogs, not expanded graph streams."""
import copy,importlib.util,json,shutil,sys,time,hashlib
from pathlib import Path
from ledger_kernel.retained import ROOT,CP2,sha,atomic
from ledger_kernel.inventory import metadata
from v4_ingest.definition import ACTIVE,BINDING
from v4_ingest.records import canonical,digest
OUT=ROOT/'rebinding'

def main():
    start=time.monotonic();OUT.mkdir(exist_ok=True);cp=CP2();base=ROOT/'work/catalog-4I'
    for rel in ('model_kernel/catalog.py','model_kernel/expand.py','model_kernel/build.py'):cp.get(rel)
    spec=importlib.util.spec_from_file_location('cp2_catalog_verified',cp.get('model_kernel/catalog.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    print('stage: verifying baseline source catalog',flush=True)
    old=module.Catalog(ROOT/'accepted')
    # Source-only overlay; no code or historical source is overwritten.
    if not base.exists():shutil.copytree(ROOT/'accepted',base)
    shutil.copyfile(ACTIVE/'security-fields.tsv',base/'definition-completion/security-fields.tsv')
    new=module.Catalog(base)
    for field in ('nodes','relations','selectors','join_rules','schemas','component_count','framing'):
        assert getattr(old,field)==getattr(new,field),field
    changes=[(i,a,b) for i,(a,b) in enumerate(zip(old.semantic,new.semantic),1) if a!=b]
    assert len(changes)==1
    row,a,b=changes[0];assert a['schema']=='FIELD-LABEL' and a['field']=='surface_id' and a['type']=='ID' and b==dict(a,type='FIELD-CLASS-REF')
    # Both types are ordinary scalar fields for all catalog/expansion branches.
    assert a['type'] not in ('SOURCE-REF','LIST-SOURCE-REF') and b['type'] not in ('SOURCE-REF','LIST-SOURCE-REF')
    for field in ('node_provenance','relation_provenance'):
        oldsaved=cp.data('results/expansion/'+('surface-provenance.json' if field=='node_provenance' else 'relation-provenance.json'))
        assert oldsaved==getattr(old,field),'catalog differs from retained provenance'
        atomic(OUT/('surface-provenance.json' if field=='node_provenance' else 'relation-provenance.json'),canonical(getattr(new,field)))
    print('stage: verifying saved model identity and exact catalog metadata',flush=True)
    model=cp.get('results/expansion/model.json');surfaces,relations=metadata(model)
    assert surfaces==old.nodes==new.nodes and relations==old.relations==new.relations
    oldcontract=json.loads((ROOT/'inputs/selected-contract.json').read_bytes());assert oldcontract==cp.data('contract/selected-contract.json')
    assert oldcontract['source_inputs']==old.input_hashes
    selected=copy.deepcopy(oldcontract);selected['source_inputs']=new.input_hashes;selected['contract_id']='G4-CP2-LOCAL-RECORD-PRODUCER-001-FCR-001'
    selected['parser']['input']='exact canonical amended S90-FCR-001 record bytes plus complete field_label_surfaces register from this bound contract'
    assert selected['field_label_surfaces']==[n['node_id'] for n in new.nodes]
    # Every expansion-relevant contract field is exactly unchanged. Parser text,
    # contract identity and source hash bindings are not serialized model fields.
    for k in oldcontract:
        if k not in ('source_inputs','contract_id','parser'):assert oldcontract[k]==selected[k],k
    for k in oldcontract['parser']:
        if k!='input':assert oldcontract['parser'][k]==selected['parser'][k]
    atomic(OUT/'selected-contract.json',canonical(selected))
    atomic(OUT/'field-class-register.json',canonical(selected['field_label_surfaces']))
    newcontracthash=sha(OUT/'selected-contract.json')
    oldsha=old.input_hashes[module.SEMANTIC];newsha=new.input_hashes[module.SEMANTIC]
    def rewrite(value):
        if isinstance(value,list):return [rewrite(v) for v in value]
        if not isinstance(value,dict):return value
        result={k:rewrite(v) for k,v in value.items()}
        if value.get('input_path')==module.SEMANTIC:
            assert value['input_sha256']==oldsha
            result['input_sha256']=newsha
            if value['data_row']==row:result['row_sha256']=digest(canonical(b))
        return result
    # Rebind the full saved model-duty and populated node/structural inventories.
    outputs=[]
    pairs=[(cp.get('results/expansion/model-duty-ledger.jsonl'),OUT/'model-duty-ledger.jsonl'),
           (ROOT/'ledger_data/node-duties.jsonl',OUT/'ledger/node-duties.jsonl'),
           (ROOT/'ledger_data/structural-duties.jsonl',OUT/'ledger/structural-duties.jsonl')]
    for src,dest in pairs:
        dest.parent.mkdir(parents=True,exist_ok=True);temp=dest.with_suffix('.part');count=changed=0
        with src.open('rb') as rd,temp.open('wb') as wr:
            for line in rd:
                original=json.loads(line);updated=rewrite(original);count+=1;changed+=original!=updated;wr.write(canonical(updated))
        temp.replace(dest);outputs.append({'path':str(dest.relative_to(ROOT)),'rows':count,'changed_rows':changed,'sha256':sha(dest),'parent_sha256':sha(src)})
    # Existing segment data depend on unchanged token/structural/provenance rows.
    # Verify their saved hashes, preserve their evidence, bind via a new receipt.
    inventory=json.loads((ROOT/'ledger_data/inventory-result.json').read_bytes());reuse=[]
    for e in inventory['derived_segments']:
        p=ROOT/'ledger_data'/e['path'];assert sha(p)==e['sha256'];obj=json.loads(p.read_bytes());assert digest(canonical(obj['data']))==obj['data_sha256'];reuse.append(e)
    report={'format':'CP4I-DEPENDENCY-REBINDING-1','result':'PASS','amendment_binding_sha256':sha(ACTIVE/'BINDING.json'),
        'schema_change':{'data_row':row,'before':a,'after':b,'old_sha256':oldsha,'new_sha256':newsha},
        'source_catalog':{'nodes':len(new.nodes),'relations':len(new.relations),'nodes_relations_selectors_join_rules_equal':True,'provenance_regenerated':True},
        'model':{'path_in_CP2':'results/expansion/model.json','bytes':model.stat().st_size,'sha256':sha(model),'serialization_changed':False,'reuse_verified':True,'basis':'Exact saved model hash and old/new ordered model metadata equality; unchanged selectors/join rules, contexts, multiplicities, exposure/reuse and all expansion-relevant contract fields. Type only enters SOURCE-REF branch tests; neither ID nor FIELD-CLASS-REF takes those branches.'},
        'contract':{'old_sha256':sha(ROOT/'inputs/selected-contract.json'),'new_sha256':newcontracthash,'new_path':'rebinding/selected-contract.json'},
        'regenerated':outputs,'reused_segment_receipts':reuse,'expansion_rerun':False,'full_pair_or_link_stream_processed':False,'actual_admission_enabled':False,'source_qualification_established':False,'seconds':round(time.monotonic()-start,6)}
    binding={'format':'CP4I-REBOUND-LEDGER-PROVENANCE-1','amendment_binding_sha256':report['amendment_binding_sha256'],'model_sha256':report['model']['sha256'],'selected_contract_sha256':newcontracthash,'baseline_inventory_sha256':sha(ROOT/'ledger_data/inventory-result.json'),'regenerated':outputs,'reused_segments':reuse,'qualification':'NOT-ESTABLISHED','meaning':'Mechanical coverage reused; new source provenance and contract binding. Historical construction journals are not current recovery receipts.'}
    hashes=json.loads((ROOT/'ledger_data/FILE-HASHES.json').read_bytes())['files']
    unchanged=[]
    for name in ('potential-domain.json','governing-slots.json','required-security-duties.json'):
        source=ROOT/'ledger_data'/name;assert sha(source)==hashes[name]['sha256']
        atomic(OUT/'ledger'/name,source.read_bytes());unchanged.append({'path':'rebinding/ledger/'+name,'sha256':sha(source),'reason':'no changed schema/type/source digest dependency in these bytes'})
    binding['verified_unchanged']=unchanged
    binding['rebinding_procedure_sha256']=sha(Path(__file__))
    report['verified_unchanged']=unchanged
    report['reviewed_dependency_code']={name:sha(cp.get('model_kernel/'+name)) for name in ('catalog.py','expand.py','build.py')}
    report['model']['surface_array_sha256']=digest(canonical(surfaces))
    report['model']['relation_array_sha256']=digest(canonical(relations))
    atomic(OUT/'ledger/BINDING.json',canonical(binding))
    atomic(OUT/'source-path-binding.json',canonical({'format':'CP4I-SOURCE-PATH-BINDING-1','logical_inputs':{n:{'path':str((ACTIVE/'security-fields.tsv').relative_to(ROOT)) if n==module.SEMANTIC else 'accepted/'+n,'sha256':h} for n,h in new.input_hashes.items()},'grammar':{'path':str((ACTIVE/'v4_record_grammar.py').relative_to(ROOT)),'sha256':sha(ACTIVE/'v4_record_grammar.py')},'qualification_established':False}))
    atomic(ROOT/'results/4I-dependency-impact.json',canonical(report));print(json.dumps({k:v for k,v in report.items() if k not in ('reused_segment_receipts','schema_change')},indent=2))
if __name__=='__main__':main()
