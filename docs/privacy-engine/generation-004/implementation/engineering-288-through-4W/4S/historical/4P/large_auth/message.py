"""Exact original V2 signed-message iterator; NOT a signature verifier.

All yielded original bytes must be consumed; early consumer termination proves
nothing. No lengths/signature.txt/object digest enter the signed message.
"""
import contextlib,fcntl,hashlib,os
from pathlib import Path
from v4_ingest.wire import SIGN_DOMAIN,FILES
from .core import validate_manifest,mark,CHUNK
from link_recovery.cli import RecoveryError

def signed_message(manifest,base,chunk_bytes=65536):
    base=Path(base).resolve();validate_manifest(manifest,base)
    if type(chunk_bytes) is not int or not 1<=chunk_bytes<=CHUNK:raise RecoveryError('message chunk bound')
    with contextlib.ExitStack() as stack:
        opened=[]
        for name in FILES[:3]:
            entry=manifest['files'][name];fd=os.open(base/entry['path'],os.O_RDONLY|os.O_NOFOLLOW);stack.callback(os.close,fd);fcntl.flock(fd,fcntl.LOCK_SH|fcntl.LOCK_NB)
            initial=mark(fd)
            if initial[2]!=entry['bytes']:raise RecoveryError('signed file size mismatch')
            opened.append((entry,fd,initial))
        yield SIGN_DOMAIN
        for entry,fd,initial in opened:
            h=hashlib.sha256();count=0
            while count<entry['bytes']:
                b=os.read(fd,min(chunk_bytes,entry['bytes']-count))
                if not b:raise RecoveryError('truncated original message')
                count+=len(b);h.update(b);yield b
            if os.read(fd,1) or h.hexdigest()!=entry['sha256']:raise RecoveryError('changed signed message bytes')
        for entry,fd,initial in opened:
            if mark(fd)!=initial:raise RecoveryError('signed input changed during processing')
