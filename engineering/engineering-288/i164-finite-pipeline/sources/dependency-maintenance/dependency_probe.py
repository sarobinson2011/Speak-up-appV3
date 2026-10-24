"""Dependency-only inventory/probe. Never imports I164 or opens a database."""
import hashlib, importlib.metadata as md, json, platform, ssl, sys
from pathlib import Path

def identity(p):
    b=Path(p).read_bytes(); return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def inventory():
    from cryptography.hazmat.backends.openssl.backend import backend
    result={'python':platform.python_version(),'implementation':platform.python_implementation(),
      'optimize':sys.flags.optimize,'machine':platform.machine(),'libc':platform.libc_ver(),
      'executable':str(Path(sys.executable).resolve()),'executable_identity':identity(Path(sys.executable).resolve()),
      'cryptography_openssl':backend.openssl_version_text(),'stdlib_ssl':ssl.OPENSSL_VERSION,'packages':{}}
    for name in ['cryptography','cffi','pycparser']:
        d=md.distribution(name); files=[]
        for f in sorted(d.files or [],key=str):
            if str(f).endswith(('/METADATA','/WHEEL','/RECORD','.so','.pyd')):
                files.append({'member':str(f),'identity':identity(d.locate_file(f))})
        result['packages'][name]={'version':d.version,'requires':d.requires or [],'build_files':files}
    result['wheel_payload_authentication']='NOT ESTABLISHED BY INVENTORY ALONE'
    return result

def probe():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey,Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization,hashes
    from cryptography.hazmat.primitives.asymmetric import ec,utils
    from cryptography.exceptions import InvalidSignature
    # RFC 8032 section 7.1, TEST 1: public verification only; no secret keys.
    public=bytes.fromhex('d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a')
    signature=bytes.fromhex('e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b')
    key=Ed25519PublicKey.from_public_bytes(public)
    key.verify(signature,b'')
    if key.public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)!=public: raise RuntimeError('RAW-BYTES')
    checks=['RFC8032 public verification','Raw public byte equality']
    for sig,msg in [(signature,b'x'),(bytes([signature[0]^1])+signature[1:],b'')]:
        try: key.verify(sig,msg)
        except InvalidSignature: checks.append('InvalidSignature rejection')
        else: raise RuntimeError('INVALID-SIGNATURE-ACCEPTED')
    for raw in [b'',b'x'*31,b'x'*33]:
        try: Ed25519PublicKey.from_public_bytes(raw)
        except ValueError: checks.append('Raw key length rejection')
        else: raise RuntimeError('BAD-KEY-LENGTH-ACCEPTED')
    # Interface existence only, not a signing compatibility claim.
    if not all(callable(getattr(Ed25519PrivateKey,n,None)) for n in ['from_private_bytes','sign','public_key']): raise RuntimeError('PRIVATE-API-MISSING')
    checks.append('Private API presence only; not invoked')
    der=utils.encode_dss_signature(1,1)
    if utils.decode_dss_signature(der)!=(1,1): raise RuntimeError('DER-ROUNDTRIP')
    pub=ec.EllipticCurvePublicNumbers(
      55066263022277343669578718895168534326250603453777594175500187360389116729240,
      32670510020758816978083085130507043184471273380659243275938904335757337482424,ec.SECP256K1()).public_key()
    try: pub.verify(der,bytes(32),ec.ECDSA(utils.Prehashed(hashes.SHA256())))
    except InvalidSignature: checks.append('secp256k1/Prehashed interface rejects invalid signature')
    else: raise RuntimeError('INVALID-ECDSA-ACCEPTED')
    return {'passed':checks,'scope':'public primitive checks only; not I164 saved-export or signing validation',
      'signing_executed':False,'session_operated':False,'model_expanded':False,'admission':False}

if __name__=='__main__':
    result=inventory()
    if sys.argv[1:]==['--probe']: result['probe']=probe()
    elif sys.argv[1:]: raise SystemExit('unsupported arguments')
    print(json.dumps(result,indent=2))
