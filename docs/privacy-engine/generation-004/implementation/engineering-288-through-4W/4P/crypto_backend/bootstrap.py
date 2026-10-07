"""Install exact hash-pinned Linux x86_64 Rust 1.85.1 components in local work."""
import argparse,hashlib,json,subprocess,tarfile,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser();p.add_argument('--directory',required=True,type=Path);a=p.parse_args();root=a.directory.resolve();root.mkdir(parents=True,exist_ok=True)
    pin=json.loads((ROOT/'TOOLCHAIN.json').read_bytes())
    for name,e in pin['components'].items():
        archive=root/e['url'].split('/')[-1]
        if not archive.exists() or hashlib.sha256(archive.read_bytes()).hexdigest()!=e['sha256']:
            temporary=archive.with_suffix(archive.suffix+'.part')
            with urllib.request.urlopen(e['url'],timeout=55) as src,temporary.open('wb') as dst:
                while b:=src.read(1048576):dst.write(b)
            if hashlib.sha256(temporary.read_bytes()).hexdigest()!=e['sha256']:raise SystemExit('component SHA mismatch: '+name)
            temporary.replace(archive)
        with tarfile.open(archive) as t:t.extractall(root,filter='data')
        installer=root/archive.name[:-7]/'install.sh'
        subprocess.run(['bash',str(installer),'--prefix='+str(root/'installed'),'--disable-ldconfig'],check=True)
        print(name+' verified and installed',flush=True)
    print('Toolchain: '+str(root/'installed'))
if __name__=='__main__':main()
