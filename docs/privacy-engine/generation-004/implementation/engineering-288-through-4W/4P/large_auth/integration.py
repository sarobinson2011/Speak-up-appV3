"""Recoverable byte stage -> inherited CP4C link validation -> binding collector.

The entire evidence bundle is NEVER materialized. Small metadata files have
explicit local caps; large token/link bytes stay in the incremental hash stage.
No positive admission or large-input signature capability is manufactured.
"""
import argparse,json,time
from pathlib import Path
from v4_ingest.records import digest,parse,primitive,profile_identity
from v4_ingest.wire import EVIDENCE_HEADER,read_table,signature_line
from admission_kernel.failures import Failures
from admission_kernel.admission import appointment
from link_recovery import cli as links
from .core import execute,load
from .backend import capabilities

def run(job,checkpoint,key,*,resume=False,new_bytes=64*1024*1024,seconds=50,chunk_bytes=65536,appointment_value=None,progress=None):
    started=time.monotonic();f=Failures();job=Path(job).resolve();base=job.parent
    with job.open('rb') as stream:raw=stream.read(1024*1024+1)
    if len(raw)>1024*1024:raise links.RecoveryError('job manifest local limit')
    m=parse(raw)
    # Invalid carrier prevents safe independent file acquisition. Protocol
    # failures with a valid carrier are collected, never replaced by last error.
    from .core import validate_manifest
    try:validate_manifest(m,base)
    except (ValueError,TypeError,KeyError) as e:
        from admission_kernel.failures import ORDER
        category=getattr(e,'category',None)
        f.add(category if category in ORDER else 'INVALID-PROFILE-SCHEMA',str(e));return f.result('ACTUAL-DISABLED')
    try:byte_result=execute(job,checkpoint,key,new_bytes=new_bytes,seconds=seconds,chunk_bytes=chunk_bytes,resume=resume,progress=progress)
    except (ValueError,OSError,links.RecoveryError) as e:
        text=str(e)
        code='MISSING-EVIDENCE' if isinstance(e,FileNotFoundError) else 'INVALID-PROFILE-SCHEMA' if 'outer ' in text and 'digest' not in text else 'INVALID-EVIDENCE-DIGEST' if any(x in text for x in ('digest','prefix','size changed','input changed')) else 'INCOMPLETE-EVIDENCE-UNIVERSE'
        if 'digest mismatch outer' in text:code='PROFILE-DIGEST-MISMATCH'
        f.add(code,text);byte_result={'complete':False,'result':'FAILED','complete_object_sha256':None,'profile_admitted':False}
    if byte_result['result']=='PAUSED':return {'result':'PAUSED','byte_stage':byte_result,'profile_admitted':False}
    try:appointed=appointment(appointment_value)
    except (ValueError,TypeError,KeyError):appointed=None;f.add('INVALID-EVIDENCE-AUTHORITY','independent external appointment unavailable or malformed')
    def metadata(name,limit):
        try:
            with (base/m['files'][name]['path']).open('rb') as stream:b=stream.read(limit+1)
        except OSError as e:f.add('MISSING-EVIDENCE',str(e));return None
        if len(b)>limit:f.add('INCOMPLETE-EVIDENCE-UNIVERSE','metadata local capability '+name);return None
        if digest(b)!=m['files'][name]['sha256']:f.add('INVALID-EVIDENCE-DIGEST','metadata changed after byte acquisition '+name);return None
        return b
    eb=metadata('evidence.tsv',1024*1024);sb=metadata('signature.txt',4096)
    row=None
    if eb is not None:
        try:
            rows=read_table(eb,EVIDENCE_HEADER)
            if len(rows)!=1:raise ValueError('one evidence row')
            row=rows[0]
            for k,v in row.items():
                if k.endswith('sha256'):primitive('DIGEST',v)
                elif k.endswith('result'):
                    if v not in ('PASS','FAIL'):raise ValueError('result enum')
                elif k!='algorithm':primitive('ID',v)
            profile_identity(row['profile_id'])
            kind='ADMISSION-COMPOSITION' if m['scope']=='NOT-APPLICABLE' else 'ADMISSION-COMPONENT'
            if row['profile_sha256']!=m['profile_sha256']:f.add('PROFILE-DIGEST-MISMATCH','signed final outer-profile identity')
            if row['component_id']!=m['scope'] or row['evidence_kind']!=kind or row['scope_id']!=row['profile_id']+'#ADMISSION-V1':f.add('INVALID-ACTION-CONTEXT','signed scope/phase')
            for name in ('tokens.tsv','links.tsv'):
                if row[name.split('.')[0]+'_sha256']!=m['files'][name]['sha256']:f.add('INVALID-EVIDENCE-DIGEST','signed consumed table bytes '+name)
            expected_id=row['profile_id']+'#'+kind+'-'+('ALL' if m['scope']=='NOT-APPLICABLE' else m['scope'])
            if row['evidence_id']!=expected_id:f.add('INVALID-ACTION-CONTEXT','evidence identity constructor')
            if row['algorithm']!='ED25519-RFC8032':f.add('INVALID-EVIDENCE-AUTHENTICATION','signature variant')
            if appointed and (row['issued_by']!=appointed['authority_id'] or row['algorithm']!='ED25519-RFC8032'):f.add('INVALID-EVIDENCE-AUTHORITY','external authority/algorithm mismatch')
        except (ValueError,KeyError):f.add('INVALID-PROFILE-SCHEMA','evidence metadata grammar')
    if sb is not None:
        try:
            issuer,sig=signature_line(sb)
            if row is not None and issuer!=row['issued_by']:f.add('INVALID-EVIDENCE-AUTHENTICATION','signature/evidence issuer mismatch')
            if appointed and issuer!=appointed['authority_id']:f.add('INVALID-EVIDENCE-AUTHENTICATION','signature line appointed identity')
        except ValueError:f.add('INVALID-EVIDENCE-AUTHENTICATION','signature line encoding')
    # Separate journal retains parser, order, counts and SHA state exactly as CP4C.
    # CP4C re-hashes the consumed prefix on EVERY continuation, including terminal.
    remaining=seconds-(time.monotonic()-started)
    if remaining<=.2:return {'result':'PAUSED','byte_stage':byte_result,'detail':'time reserved for next semantic invocation','profile_admitted':False}
    link_ck=Path(str(checkpoint)+'.links.json');operation='resume' if link_ck.exists() else 'start'
    a=argparse.Namespace(operation=operation,key=Path(key),checkpoint=link_ck,
        input=None if operation=='resume' else base/m['files']['links.tsv']['path'],
        input_sha256=None if operation=='resume' else m['files']['links.tsv']['sha256'],
        model=None if operation=='resume' else base/m['model']['path'],
        model_sha256=None if operation=='resume' else m['model']['sha256'],
        contract=None if operation=='resume' else base/m['contract']['path'],
        contract_sha256=None if operation=='resume' else m['contract']['sha256'],
        new_bytes=new_bytes,chunk_bytes=chunk_bytes,seconds=remaining)
    try:
        if operation=='resume':
            previous=links.load(link_ck,links.read_key(key))['binding']
            expected={'input':(base/m['files']['links.tsv']['path'],m['files']['links.tsv']['sha256']),
                      'model':(base/m['model']['path'],m['model']['sha256']),'contract':(base/m['contract']['path'],m['contract']['sha256'])}
            for k,(path,h) in expected.items():
                if previous[k]['path']!=str(path.resolve()) or previous[k]['sha256']!=h:raise links.RecoveryError('cross-job link journal substitution')
        lr=links.execute(a)
    except (ValueError,OSError,links.RecoveryError) as e:
        f.add('INCOMPLETE-EVIDENCE-UNIVERSE',str(e));lr={'result':'REJECTED','complete':False,'detail':str(e)}
    if lr['result']=='PAUSED':return {'result':'PAUSED','byte_stage':byte_result,'link_stage':lr,'profile_admitted':False}
    if not lr['complete']:
        code=lr.get('failure',{}).get('code','INCOMPLETE-EVIDENCE-UNIVERSE')
        from admission_kernel.failures import ORDER
        f.add(code if code in ORDER else 'INCOMPLETE-EVIDENCE-UNIVERSE','supplied link stage rejected')
    f.add('INCOMPLETE-EVIDENCE-UNIVERSE','incremental pure Ed25519 backend acceptance review/build unavailable; signature unverified')
    f.add('INCOMPLETE-EVIDENCE-UNIVERSE','source appointment competence, full scope/ledger/semantic qualification not established by byte acquisition')
    result=f.result('ACTUAL-DISABLED',{'byte_stage':byte_result,'link_stage':lr,'backend':capabilities(),'canonical_model_sha256':m['canonical_model_sha256'],'complete_authentication':False})
    return result
