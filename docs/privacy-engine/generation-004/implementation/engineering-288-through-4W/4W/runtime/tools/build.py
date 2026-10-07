#!/usr/bin/env python3
import hashlib,json,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
began=time.monotonic();commands=[]
for name in ['emitter_service','validator_service']:
 args=['g++','-O3','-std=c++17','-Wno-deprecated-declarations',str(R/'native'/(name+'.cpp')),'-lcrypto','-o',str(R/'native'/name)]
 cp=subprocess.run(args,capture_output=True,text=True,timeout=60)
 if cp.returncode:raise RuntimeError(cp.stderr)
 commands.append({'argv':args,'returncode':cp.returncode,'stderr':cp.stderr})
 subprocess.run([str(R/'native'/name),'--selftest'],check=True,timeout=5)
print(json.dumps({'result':'PASS-BUILD','commands':commands,'seconds':time.monotonic()-began,'compiler':subprocess.check_output(['g++','--version'],text=True).splitlines()[0]}))
