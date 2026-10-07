"""Reproduce pinned bounded crypto-oracle acceptance observations."""
import ctypes,ctypes.util,hashlib,json,platform,sys
from pathlib import Path
from .backend import capabilities
from tests.test_auth_crypto import probe,VECTORS

def report():
    import cryptography.hazmat.bindings._rust as rust
    lib=ctypes.CDLL(ctypes.util.find_library('sodium'));lib.sodium_version_string.restype=ctypes.c_char_p
    sodium=lib.sodium_version_string().decode();paths={str(Path(rust.__file__).resolve())}
    for line in Path('/proc/self/maps').read_text().splitlines():
        if 'libsodium.so' in line:paths.add(line.split()[-1])
    identities={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in sorted(paths)}
    caps=capabilities();pinned=caps['bounded_reference']=={'cryptography':'46.0.0','openssl':'OpenSSL 3.5.3 16 Sep 2025'} and sodium=='1.0.18'
    return {'format':'CP4F-BACKEND-OBSERVATIONS-1','reference_versions_match_pins':pinned,'capabilities':caps,'libsodium':sodium,'python':platform.python_version(),'binary_sha256':identities,'vectors':VECTORS,'cases':probe(),'incremental_verifier_implemented':False,'acceptance_equivalence_established':False,'actual_admission':False}
if __name__=='__main__':print(json.dumps(report(),indent=2))
