"""Create and verify the self-contained recoverable checkpoint 4P ZIP."""
import hashlib,json,pathlib,zipfile,os

ROOT=pathlib.Path(__file__).resolve().parent
EXCLUDE={'retained/Engineering-288-checkpoint-4J.zip','retained/Engineering-288-checkpoint-4I.zip','retained/Engineering-288-checkpoint-4H.zip','PACKAGE-MANIFEST.json','inputs/links.txt','inputs/links.part','retained/Engineering-288-checkpoint-4G.zip','retained/Engineering-288-checkpoint-4A.zip','retained/Engineering-288-checkpoint-4C.zip','retained/Engineering-288-checkpoint-4D.zip','retained/Engineering-288-checkpoint-4E.zip','retained/Engineering-288-checkpoint-4F.zip'}

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        while b:=f.read(1048576):h.update(b)
    return h.hexdigest()

def main():
    files=[]
    for p in sorted(ROOT.rglob('*')):
        rel=p.relative_to(ROOT);name=rel.as_posix()
        if p.is_file() and not (rel.parts[0]=='retained' and (p.name.startswith('.') or p.suffix=='.zip' and p.name!='Engineering-288-checkpoint-4O.zip')) and name not in EXCLUDE and not any(x in rel.parts for x in ('work','__pycache__','target')):
            files.append({'path':name,'bytes':p.stat().st_size,'sha256':sha(p)})
    manifest={'format':'Engineering-288-CP4P-PACKAGE-1','files':files,'full_pair_or_link_stream_executed':False,'profile_admitted':False,
              'exact_byte_acquisition_recovery':'IMPLEMENTED-AND-VERIFIED','incremental_pure_ed25519':'IMPLEMENTED-BUILT-TESTED-CANONICAL-ADAPTER','large_signature_recovery':'IMPLEMENTED-FULL-PREFIX-RECONSTRUCTION','three_scope_authentication_integration':'IMPLEMENTED-SEMANTIC-FILE-BACKED-CONDITIONAL-WITH-EXPLICIT-SCALAR-AND-INDEX-CAPS','qualified_full_model_ledger':'NOT-ESTABLISHED','semantic_record_acquisition':'DISK-INDEXED-IMPLEMENTED-TESTED','exact_assessor_invocation':'STREAMED-BOTH-INHERITED-CODECS-TESTED','finite_assessor_distribution':'DISK-INDEXED-EXACT-CONDITIONAL','practical_full_scale_recovery':'IMPLEMENTED-STATIC-SCOPED-STAGE-COMPOSITION; EXACT-RECHECK-AND-PREFIX-REPLAY-COSTS-REMAIN',
              'owning_occurrence_values':'IMPLEMENTED-BOUNDED-TSEV1-S90-JSON-LF-EXACT-DISK-EQUALITY','first_kernel_code_complete_for_declared_finite_conditional_contract':True,'full_retained_model_execution_witness':False,'s90_containing_projections':'IMPLEMENTED-596-REGISTERED-CLASSES; EXTERNAL-EVENT-QUALIFICATION-REQUIRED','semantic_document_lifetime':'BOUNDED-FOUR-INDEX-POOL-BYTE-CACHES-EXACT-REOPEN-VERIFIED','metadata_catalogs':'DISK-BACKED-COMPLETE-426984-TOKEN-METADATA-COVERAGE-VERIFIED','generated_event_projections':'IMPLEMENTED-13-FORMS-ALL-BRANCHES-AND-STATUSES','remaining_demonstrated_selected_contract_code_gaps':[],'field_label_identifier_obstacle':'RESOLVED-BY-APPROVED-FIELD-SPECIFIC-AMENDMENT','active_amendment':'amendments/PE-G4-FIELD-CLASS-REF-AMENDMENT-001/v1.0.0/BINDING.json','historical_identifier_finding':'results/identifier-reconciliation.json'}
    (ROOT/'PACKAGE-MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    target=ROOT.with_suffix('.zip')
    temporary=target.with_name(target.name+'.tmp')
    with zipfile.ZipFile(temporary,'w',zipfile.ZIP_DEFLATED,compresslevel=6,strict_timestamps=False) as z:
        for e in files:z.write(ROOT/e['path'],ROOT.name+'/'+e['path'])
        z.write(ROOT/'PACKAGE-MANIFEST.json',ROOT.name+'/PACKAGE-MANIFEST.json')
    with temporary.open('rb') as f:os.fsync(f.fileno())
    with zipfile.ZipFile(temporary) as z:
        assert z.testzip() is None
        for e in files:
            name=ROOT.name+'/'+e['path'];assert z.getinfo(name).file_size==e['bytes'],name
            with z.open(name) as f:assert hashlib.file_digest(f,'sha256').hexdigest()==e['sha256'],name
    os.replace(temporary,target)
    directory=os.open(target.parent,os.O_RDONLY)
    try:os.fsync(directory)
    finally:os.close(directory)
    receipt={'result':'PASS','zip':target.name,'bytes':target.stat().st_size,'sha256':sha(target),'manifested_files':len(files),
             'zip_crc':'PASS','all_member_hashes':'PASS','full_pair_or_link_stream_executed':False,'profile_admitted':False}
    ROOT.with_name(ROOT.name+'-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
