"""Explicit capability boundary: no invented incremental Ed25519 verifier.

The pinned candidate ed25519-dalek 2.2.0 verify_stream is NOT enabled: its
ZIP-215 public-key decoding and strict/non-strict acceptance need a reviewed
RFC8032 compatibility resolution and reproducibly built/vendored dependencies.
"""
import ctypes,ctypes.util,hashlib
from pathlib import Path

def capabilities():
    import cryptography
    from cryptography.hazmat.backends.openssl.backend import backend
    return {'incremental_pure_ed25519':'NOT-IMPLEMENTED',
        'candidate':'ed25519-dalek=2.2.0; hazmat VerifyingKey::verify_stream',
        'blocker':'RFC8032 point/encoding acceptance compatibility review and pinned executable/dependency build unavailable',
        'bounded_reference':{'cryptography':cryptography.__version__,'openssl':backend.openssl_version_text()},
        'ed25519ph_substitution':False,'bespoke_curve_arithmetic':False}

def sodium_verify(public_key,signature,message):
    """Independent established one-shot test oracle ONLY. No streaming claim."""
    if len(public_key)!=32 or len(signature)!=64:return False
    lib=ctypes.CDLL(ctypes.util.find_library('sodium'));lib.sodium_init()
    f=lib.crypto_sign_verify_detached;f.argtypes=(ctypes.c_void_p,ctypes.c_void_p,ctypes.c_ulonglong,ctypes.c_void_p);f.restype=ctypes.c_int
    return f(signature,message,len(message),public_key)==0
