"""V2 byte authentication, separate from independent appointment/qualification.

The pure Ed25519 backend consumes the original message, not SHA256(message).
The hex carrier retains a local allocation cap. Both carriers use the same backend.
"""
from v4_ingest.records import exact,primitive,digest,ValidationError
from v4_ingest.wire import FILES,object_digest,verify_signature,read_table,EVIDENCE_HEADER

MAX_MESSAGE_BYTES=64*1024*1024

def authenticate(item, appointment, failures):
    report={'four_file_identity':False,'signature_valid':False,'complete':False,
            'source_authority_established':False,'profile_admitted':False,
            'algorithm':'ED25519-RFC8032','message_limit_bytes':MAX_MESSAGE_BYTES}
    def failure(code,text):failures.add(code,'bundle authentication: '+text)
    try:
        exact(item,('files','object_sha256'));exact(item['files'],FILES)
        primitive('DIGEST',item['object_sha256'])
        for v in item['files'].values():
            if not isinstance(v,str) or len(v)>2*MAX_MESSAGE_BYTES:
                failure('INCOMPLETE-EVIDENCE-UNIVERSE','bounded authentication capability exceeded');return None,report
            primitive('BYTES',v)
        files={k:bytes.fromhex(v) for k,v in item['files'].items()}
    except (ValidationError,TypeError,KeyError,ValueError) as e:
        failure('MISSING-EVIDENCE','unusable four-file object: '+str(e));return None,report
    report['file_identities']={n:{'bytes':len(files[n]),'sha256':digest(files[n])} for n in FILES}
    report['object_sha256']=object_digest(files)
    report['four_file_identity']=report['object_sha256']==item['object_sha256']
    if not report['four_file_identity']:failure('INVALID-EVIDENCE-DIGEST','exact four-file object digest')
    size=len(b'PE-TSE-PRIVACY-EVIDENCE-V2\n')+sum(len(files[n]) for n in FILES[:3])
    report['signed_message_bytes']=size
    if appointment is None:
        failure('INVALID-EVIDENCE-AUTHORITY','externally supplied appointment unavailable')
    else:
        try:
            __import__("integrated_auth.backend",fromlist=["verify"]).verify(files,bytes.fromhex(appointment['public_key']),appointment['authority_id'])
            report['signature_valid']=True
        except (ValidationError,ValueError,KeyError,TypeError) as e:
            failure('INVALID-EVIDENCE-AUTHENTICATION',str(e))
    # Collect digest and issuer inconsistencies independently of signature status.
    table_ok=False
    try:
        rows=read_table(files['evidence.tsv'],EVIDENCE_HEADER)
        if len(rows)==1:
            row=rows[0]
            table_ok=(row['tokens_sha256']==digest(files['tokens.tsv']) and row['links_sha256']==digest(files['links.tsv']))
            if not table_ok:failure('INVALID-EVIDENCE-DIGEST','signed table identities differ from consumed bytes')
            if appointment and (row['issued_by']!=appointment['authority_id'] or row['algorithm']!=appointment['algorithm']):
                failure('INVALID-EVIDENCE-AUTHORITY','evidence issuer/algorithm differs from external appointment');table_ok=False
    except (ValidationError,ValueError,KeyError,TypeError):pass # Grammar collector still runs.
    report['complete']=bool(report['four_file_identity'] and report['signature_valid'] and table_ok)
    return files,report
