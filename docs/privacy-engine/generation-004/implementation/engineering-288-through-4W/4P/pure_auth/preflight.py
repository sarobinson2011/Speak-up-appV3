"""4F exact object/outer acquisition followed by 4G exact-message crypto.

This closes byte authentication under an explicitly supplied key, not the
source-owned three-scope/ledger/appointment qualification pipeline.
"""
import time
from pathlib import Path
from large_auth.core import execute
from .controller import verify_job

def run(job,checkpoint,key,public_key,*,resume=False,new_bytes=64*1024*1024,seconds=50,chunk_bytes=65536,progress=None):
    start=time.monotonic();ck=Path(checkpoint);byteck=Path(str(ck)+'.bytes.json');cryptock=Path(str(ck)+'.crypto.json')
    if not resume and (byteck.exists() or cryptock.exists()):raise ValueError('preflight journals exist; resume')
    br=execute(job,byteck,key,resume=resume and byteck.exists(),new_bytes=new_bytes,seconds=seconds,chunk_bytes=chunk_bytes,progress=progress)
    if not br['complete']:return {'result':'PAUSED','byte_stage':br,'cryptographic_signature_verified':False,'profile_admitted':False}
    remaining=seconds-(time.monotonic()-start)
    if remaining<=.1:return {'result':'PAUSED','byte_stage':br,'cryptographic_signature_verified':False,'profile_admitted':False}
    cr=verify_job(job,cryptock,key,public_key,resume=resume and cryptock.exists(),new_bytes=new_bytes,seconds=remaining,chunk_bytes=chunk_bytes,progress=progress)
    return {'result':'PASS-BYTE-AND-CRYPTO-PREFLIGHT' if cr['cryptographic_signature_verified'] else 'PAUSED','byte_stage':br,'crypto_stage':cr,'cryptographic_signature_verified':cr['cryptographic_signature_verified'],'four_file_outer_acquisition_checked':True,'source_authority_established':False,'actual_qualification_established':False,'profile_admitted':False,'ordered_admission_collector_complete':False}
