"""Offline, pinned release build. TOOLCHAIN/bin must contain rustc/cargo 1.85.1."""
import argparse,hashlib,json,os,platform,shutil,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--toolchain',required=True,type=Path);ap.add_argument('--target-dir',type=Path);ap.add_argument('--receipt',type=Path);a=ap.parse_args()
    tc=a.toolchain.resolve();target=(a.target_dir or ROOT/'target').resolve();env=os.environ.copy();env['PATH']=str(tc/'bin')+os.pathsep+env['PATH'];env['CARGO_TARGET_DIR']=str(target);env['CARGO_HOME']=str(target.parent/'cargo-offline');env['RUSTFLAGS']='--cfg curve25519_dalek_backend="serial" --remap-path-prefix='+str(ROOT)+'=/cp4g/backend';env['SOURCE_DATE_EPOCH']='0'
    version=subprocess.check_output([str(tc/'bin/rustc'),'--version','--verbose'],text=True)
    if not version.startswith('rustc 1.85.1 '):raise SystemExit('requires exact rustc 1.85.1')
    began=time.monotonic();subprocess.run([str(tc/'bin/cargo'),'build','--release','--locked','--offline'],cwd=ROOT,env=env,check=True)
    tree=subprocess.check_output([str(tc/'bin/cargo'),'tree','--locked','--offline','-e','features'],cwd=ROOT,env=env,text=True)
    if 'legacy_compatibility' in tree:raise SystemExit('forbidden legacy scalar feature')
    (ROOT/'FEATURES.txt').write_text(tree)
    binary=target/'release/pe-rfc8032-stream';dest=ROOT/'bin'/binary.name;dest.parent.mkdir(exist_ok=True);shutil.copy2(binary,dest);dest.chmod(0o755)
    sources={p:sha(ROOT/p) for p in ('Cargo.toml','Cargo.lock','src/main.rs','.cargo/config.toml')}
    vendors={p.relative_to(ROOT).as_posix():sha(p) for p in sorted((ROOT/'vendor').rglob('*')) if p.is_file()}
    r={'format':'CP4G-PINNED-BUILD-1','rustc':version,'cargo':subprocess.check_output([str(tc/'bin/cargo'),'--version'],text=True).strip(),'binary_sha256':sha(dest),'binary_bytes':dest.stat().st_size,'sources':sources,'vendor_file_hashes':vendors,'features_sha256':sha(ROOT/'FEATURES.txt'),'rustflags':env['RUSTFLAGS'].replace(str(ROOT),'<backend-root>'),'platform':platform.platform(),'seconds':time.monotonic()-began,'offline':True,'external_competent_qualification':False}
    (a.receipt or ROOT/'BUILD-MANIFEST.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='vendor_file_hashes'},indent=2))
if __name__=='__main__':main()
