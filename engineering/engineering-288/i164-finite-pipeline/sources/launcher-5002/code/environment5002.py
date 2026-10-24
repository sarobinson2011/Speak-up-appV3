"""Exact prospective host profile. Trusted interpreter/process; not custody assurance."""
import base64, copy, csv, hashlib, importlib.metadata as md, io, json, os, platform, stat, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PROFILE_SHA='c8ef014644072c358282b8864f338a2c0331ef685a6f765894fd47136b846cad'
class Rejected(RuntimeError):pass
def need(ok,why):
    if not ok:raise Rejected(why)
def regular(p):
    p=Path(p);need(stat.S_ISREG(p.lstat().st_mode),'NONREGULAR:'+str(p));return p.read_bytes()
def ident(p):
    b=regular(p);return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load_profile():
    raw=regular(ROOT/'environment-profile.json');need(hashlib.sha256(raw).hexdigest()==PROFILE_SHA,'PROFILE-IDENTITY')
    p=json.loads(raw)
    need(ident(ROOT/'laboratory-configuration.json')==p['configuration'],'CONFIGURATION-IDENTITY')
    need(ident(ROOT/'requirements.lock')==p['lock'],'LOCK-IDENTITY')
    need(ident(ROOT/'provenance/host-compatibility.json')==p['compatibility_report'],'HOST-EVIDENCE-IDENTITY')
    for n,v in p['manifests'].items():need(ident(ROOT/'provenance'/n)==v,'SOURCE-MANIFEST:'+n)
    return copy.deepcopy(p)
def collect():
    from cryptography.hazmat.backends.openssl.backend import backend
    import ssl
    result={'python':platform.python_version(),'implementation':platform.python_implementation(),'optimize':sys.flags.optimize,
      'machine':platform.machine(),'libc':list(platform.libc_ver()),'executable':str(Path(sys.executable).resolve()),
      'executable_identity':ident(Path(sys.executable).resolve()),'cryptography_openssl':backend.openssl_version_text(),
      'stdlib_ssl':ssl.OPENSSL_VERSION,'packages':{},'wheel_payload_authentication':'NOT ESTABLISHED BY INVENTORY ALONE'}
    for name in ('cryptography','cffi','pycparser'):
        d=md.distribution(name);files=[]
        for f in sorted(d.files or [],key=str):
            if str(f).endswith(('/METADATA','/WHEEL','/RECORD','.so','.pyd')):files.append({'member':str(f),'identity':ident(d.locate_file(f))})
        result['packages'][name]={'version':d.version,'requires':d.requires or [],'build_files':files}
    return result

def validate_observation(observation,prefix):
    # Expectations are read afresh from pinned source bytes, never returned aliases.
    p=load_profile()
    need(type(prefix) is str and prefix==p['venv_prefix'],'EXACT-VENV-PREFIX')
    need(enc(observation)==enc(p['expected_environment']),'EXACT-ENVIRONMENT')
    return copy.deepcopy(observation)

def check_installed_records():
    """Check all RECORD-hashed installed files after checking the pinned RECORD bytes.
    Generated pyc and RECORD's own row may be unhashed. No wheel-origin claim.
    """
    result={}
    for name in ('cryptography','cffi','pycparser'):
        d=md.distribution(name);records=[f for f in d.files or [] if str(f).endswith('.dist-info/RECORD')]
        need(len(records)==1,'RECORD-COUNT');raw=regular(d.locate_file(records[0]));count=0
        for row in csv.reader(io.StringIO(raw.decode())):
            need(len(row)==3,'RECORD-ROW');member,hashfield,size=row
            target=Path(d.locate_file(member)).absolute()
            need(target.is_relative_to(Path(sys.prefix).absolute()),'RECORD-OUTSIDE-VENV')
            if not hashfield:
                need(member==str(records[0]) or member.endswith('.pyc'),'UNHASHED-INSTALLED-MEMBER');continue
            alg,sep,value=hashfield.partition('=');need(alg=='sha256' and sep,'RECORD-HASH-ALGORITHM')
            b=regular(target);need(size.isdigit() and len(b)==int(size),'RECORD-SIZE')
            actual=base64.urlsafe_b64encode(hashlib.sha256(b).digest()).rstrip(b'=').decode()
            need(actual==value,'RECORD-PAYLOAD:'+member);count+=1
        result[name]=count
    return result

def enforce():
    p=load_profile()
    # Reject other environments before importing Cryptography.
    need(sys.prefix==p['venv_prefix'],'EXACT-VENV-PREFIX')
    need(platform.python_implementation()=='CPython' and platform.python_version()=='3.12.14' and sys.flags.optimize==0,'INTERPRETER')
    need(ident(Path(sys.executable).resolve())==p['expected_environment']['executable_identity'],'INTERPRETER-IDENTITY')
    observation=collect();validate_observation(observation,sys.prefix);check_installed_records();return observation

def session_frontier(destination,create):
    """Read metadata only; no lock, runtime import, database, write or migration."""
    p=load_profile();cfg=json.loads(regular(ROOT/'laboratory-configuration.json'))
    need(type(create) is bool,'CREATE-TYPE');dest=Path(destination).absolute()
    if create:
        need(not os.path.lexists(dest),'DESTINATION-EXISTS');return
    need(dest.is_dir() and not dest.is_symlink(),'MISSING-SESSION')
    b=json.loads(regular(dest/'binding.json'))
    need(type(b) is dict and b.get('format')=='I164-LAB-BOOTSTRAP-BINDING-5002-1','NO-LEGACY-SESSION-MIGRATION')
    need(enc(b.get('configuration'))==enc(cfg),'SESSION-CONFIGURATION')
    need(enc(b.get('environment_profile'))==enc(ident(ROOT/'environment-profile.json')),'SESSION-PROFILE')
    need(enc(b.get('environment'))==enc(p['expected_environment']),'SESSION-ENVIRONMENT')
