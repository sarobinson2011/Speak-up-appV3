"""The same pinned canonical pure Ed25519 executable for in-memory callers."""
import json,subprocess
from pure_auth.controller import BINARY,identity
from v4_ingest.records import require,ValidationError
from v4_ingest.wire import FILES,SIGN_DOMAIN,signature_line

def verify(files,public_key,authority_id):
    identity();issuer,sig=signature_line(files['signature.txt'])
    require(issuer==authority_id,'signature authority identity mismatch')
    total=len(SIGN_DOMAIN)+sum(len(files[n]) for n in FILES[:3])
    p=subprocess.Popen([str(BINARY),'verify',public_key.hex(),sig.hex(),str(total),str(total)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for raw in [SIGN_DOMAIN]+[files[n] for n in FILES[:3]]:
            for off in range(0,len(raw),65536):p.stdin.write(raw[off:off+65536])
        p.stdin.close();out=p.stdout.read();p.wait(timeout=60)
        r=json.loads(out)
        require(p.returncode==0 and r['verified'],'invalid canonical pure Ed25519 signature',category='BYTE-AUTHENTICATION')
    except (BrokenPipeError, json.JSONDecodeError, subprocess.TimeoutExpired) as e:
        p.kill();p.wait();raise ValidationError("canonical backend rejected or interrupted",category="BYTE-AUTHENTICATION") from e
    except Exception:
        p.kill();p.wait();raise
    finally:p.stdout.close();p.stderr.close()
    return {'bytes_authenticated':True,'source_authority_established':False,'profile_admitted':False}
