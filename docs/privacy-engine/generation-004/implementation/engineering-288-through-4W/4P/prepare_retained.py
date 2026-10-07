"""Materialize retained descriptor required by original streaming regressions."""
import shutil,zipfile,json,hashlib,os
from ledger_kernel.retained import ROOT,archive
from link_stream.cli import prepare,sha,CP4A

def main():
    parent=ROOT/'retained/Engineering-288-checkpoint-4O.zip'
    if sha(parent)!='53a1c31381641fe8056a855fd2c2edf48c0617187e9e212e1205be08dae228bf':raise ValueError('retained CP4O identity')
    child=ROOT/'retained/Engineering-288-checkpoint-4N.zip'
    if not child.exists():
        with zipfile.ZipFile(parent) as z:raw=z.read('Engineering-288-checkpoint-4O/retained/'+child.name)
        from ledger_kernel.retained import atomic
        atomic(child,raw)
    newest=ROOT/'retained/Engineering-288-checkpoint-4N.zip'
    if sha(newest)!='ed47173e3d90a6168d164914553387b854bdb1a7d7b300b470b75486c55ffa82':raise ValueError('retained CP4N identity')
    child=ROOT/'retained/Engineering-288-checkpoint-4M.zip'
    if not child.exists():
        with zipfile.ZipFile(newest) as z:raw=z.read('Engineering-288-checkpoint-4N/retained/'+child.name)
        from ledger_kernel.retained import atomic
        atomic(child,raw)
    newest=ROOT/'retained/Engineering-288-checkpoint-4M.zip'
    if sha(newest)!='119413ad8fe330afa823576f3c46efb528b90729162ae46d6f3a7a8a5612cecf':raise ValueError('retained CP4M identity')
    child=ROOT/'retained/Engineering-288-checkpoint-4L.zip'
    if not child.exists():
        with zipfile.ZipFile(newest) as z:raw=z.read('Engineering-288-checkpoint-4M/retained/'+child.name)
        from ledger_kernel.retained import atomic
        atomic(child,raw)
    newest=ROOT/'retained/Engineering-288-checkpoint-4L.zip'
    if sha(newest)!='1a6e28017bed5939aa4af1d2e855ff56d570bcc673343195dd73a5a6064336db':raise ValueError('retained CP4L identity')
    child=ROOT/'retained/Engineering-288-checkpoint-4K.zip'
    if not child.exists():
        with zipfile.ZipFile(newest) as z:raw=z.read('Engineering-288-checkpoint-4L/retained/'+child.name)
        from ledger_kernel.retained import atomic
        atomic(child,raw)
    newest=ROOT/'retained/Engineering-288-checkpoint-4K.zip'
    if sha(newest)!='d4b75689e3531b890511e46ecdef5ba1298620e45152076bf05f867857abcb4d':raise ValueError('retained CP4K identity')
    child=ROOT/'retained/Engineering-288-checkpoint-4J.zip'
    if not child.exists():
        with zipfile.ZipFile(newest) as z:raw=z.read('Engineering-288-checkpoint-4K/retained/'+child.name)
        from ledger_kernel.retained import atomic
        atomic(child,raw)

    newest=ROOT/'retained/Engineering-288-checkpoint-4J.zip'
    if sha(newest)!='3c41c14f851210a36e521f11b16c54a5ae6cc43f099120d53243f2baa4c7f3b5':raise ValueError('retained CP4J identity')
    child=ROOT/'retained/Engineering-288-checkpoint-4I.zip'
    if not child.exists():
        with zipfile.ZipFile(newest) as z:raw=z.read('Engineering-288-checkpoint-4J/retained/'+child.name)
        from ledger_kernel.retained import atomic
        atomic(child,raw)

    parent=ROOT/'retained/Engineering-288-checkpoint-4I.zip'
    if sha(parent)!='896402e444a65920a1b5b3989780d35ad0949756643627b3cb0d0b2816443391':raise ValueError('retained CP4I identity')
    child=ROOT/'retained/Engineering-288-checkpoint-4H.zip'
    if not child.exists():
        with zipfile.ZipFile(parent) as z:raw=z.read('Engineering-288-checkpoint-4I/retained/'+child.name)
        from ledger_kernel.retained import atomic
        atomic(child,raw)
    # CP4I transports the verified CP4H parent without rewriting history.
    top=ROOT/'retained/Engineering-288-checkpoint-4H.zip'
    if sha(top)!='149c479f6ea7017190d6d13b3db40c1ae5f01a45bb3802d15d63f5a7c407bada':raise ValueError('retained CP4H identity')
    child=ROOT/'retained/Engineering-288-checkpoint-4G.zip'
    if not child.exists():
        with zipfile.ZipFile(top) as z:raw=z.read('Engineering-288-checkpoint-4H/retained/'+child.name)
        from ledger_kernel.retained import atomic
        atomic(child,raw)
    newest=ROOT/'retained/Engineering-288-checkpoint-4G.zip'
    if sha(newest)!='7e5e0506cc088c51b0f904f6c61ebfb20e8936fd309116d5a29b180941c8d1eb':raise ValueError('retained CP4G identity')
    parent=ROOT/'retained/Engineering-288-checkpoint-4F.zip'
    if not parent.exists():
        with zipfile.ZipFile(newest) as z:raw=z.read('Engineering-288-checkpoint-4G/retained/'+parent.name)
        from ledger_kernel.retained import atomic
        atomic(parent,raw)
    # CP4G transports the exact CP4F parent once.
    newest=ROOT/'retained/Engineering-288-checkpoint-4F.zip'
    if sha(newest)!='905e2e55a0826adbcd339b1c8f2cf0150256c47060cd3d241a5fa3a57756cbb4':raise ValueError('retained CP4F identity')
    current=ROOT/'retained/Engineering-288-checkpoint-4E.zip'
    if not current.exists():
        with zipfile.ZipFile(newest) as z:raw=z.read('Engineering-288-checkpoint-4F/retained/'+current.name)
        if hashlib.sha256(raw).hexdigest()!='02b231f4ef29f38f73dd862fcaf9771fca3827d3d251f87be95088f29b4a108e':raise ValueError('nested CP4E identity')
        from ledger_kernel.retained import atomic
        atomic(current,raw)
    (ROOT/'crypto_backend/bin/pe-rfc8032-stream').chmod(0o755)
    # CP4F transports the exact CP4E parent once.
    current=ROOT/'retained/Engineering-288-checkpoint-4E.zip'
    if sha(current)!='02b231f4ef29f38f73dd862fcaf9771fca3827d3d251f87be95088f29b4a108e':raise ValueError('retained CP4E identity')
    parent=ROOT/'retained/Engineering-288-checkpoint-4D.zip'
    if not parent.exists():
        with zipfile.ZipFile(current) as z:raw=z.read('Engineering-288-checkpoint-4E/retained/'+parent.name)
        if hashlib.sha256(raw).hexdigest()!='59d4f36f3daf2a11fcf1abf50c82ae0e72c53cd0d632614bb2dd751035c08ef1':raise ValueError('nested CP4D identity')
        from ledger_kernel.retained import atomic
        atomic(parent,raw)
    # CP4E transports the exact CP4D parent once; recover its unchanged CP4C
    # member before invoking the inherited recovery/acquisition code.
    parent=ROOT/'retained/Engineering-288-checkpoint-4D.zip'
    expected='59d4f36f3daf2a11fcf1abf50c82ae0e72c53cd0d632614bb2dd751035c08ef1'
    if sha(parent)!=expected:raise ValueError('retained CP4D identity')
    child=ROOT/'retained/Engineering-288-checkpoint-4C.zip'
    child_hash='ca4c968c22e738b5e98a4a90c0214bbcbd6d7b44fd9c15acafb8c71cb1dda9f7'
    if not child.exists():
        with zipfile.ZipFile(parent) as z:
            raw=z.read('Engineering-288-checkpoint-4D/retained/'+child.name)
        if hashlib.sha256(raw).hexdigest()!=child_hash:raise ValueError('nested CP4C identity')
        from ledger_kernel.retained import atomic
        atomic(child,raw)
    if sha(child)!=child_hash:raise ValueError('changed retained CP4C identity')
    for rel in ('link_stream/native','link_recovery/worker'):
        (ROOT/rel).chmod(0o755)
    p=archive('4A');dest=ROOT/'retained/Engineering-288-checkpoint-4A.zip'
    if not dest.exists():shutil.copy2(p,dest)
    if sha(dest)!=CP4A:raise ValueError('retained CP4A identity')
    print(prepare())
    for rel in ('link_stream/native','link_recovery/worker','crypto_backend/bin/pe-rfc8032-stream'):(ROOT/rel).chmod(0o755)

if __name__=='__main__':main()
