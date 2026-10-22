"""Independent decoding of retained signed transaction vectors; no execution."""
import json
from pathlib import Path
import stages
P=Path(__file__).resolve().parents[1]
def rlp(b,i=0):
 p=b[i]
 if p<128:return bytes([p]),i+1
 if p<=183:n=p-128;return b[i+1:i+1+n],i+1+n
 if p<=191:k=p-183;n=int.from_bytes(b[i+1:i+1+k],'big');return b[i+1+k:i+1+k+n],i+1+k+n
 if p<=247:n=p-192;a=i+1
 else:k=p-247;n=int.from_bytes(b[i+1:i+1+k],'big');a=i+1+k
 end=a+n;result=[]
 while a<end:v,a=rlp(b,a);result.append(v)
 assert a==end;return result,end
rows=[]
for t in json.loads((P/'evidence/prepared-calldata-vectors.json').read_text())['transactions']:
 raw=bytes.fromhex(t['signed_transaction']);tx,end=rlp(raw);assert end==len(raw);data=tx[5];b=data[4:]
 def n(off):return int.from_bytes(b[off:off+32],'big')
 def dyn(off):length=n(off);return b[off+32:off+32+length]
 if t['stage']=='begin':
  off=n(0);vals=[b[off+i*32:off+(i+1)*32] for i in range(4)];c=json.loads(dyn(off+n(off+160)));meta={'key':vals[0].hex(),'signature':(vals[1]+vals[2]).hex(),'message_sha256':vals[3].hex(),'total':n(off+128),'bindings':c,'invocation':dyn(n(32)).hex()}
  got=stages.calldata(meta,'',{'kind':'begin'})
 elif t['stage']=='append-0':got=stages.calldata({},b[:32].hex(),{'kind':'append','offset':n(32),'bytes':dyn(n(64)).hex()})
 else:got=stages.calldata({},'',{'kind':'finalize'})
 assert got==data,t['stage'];rows.append({'stage':t['stage'],'bytes':len(data),'exact_calldata_equal':True})
print(json.dumps({'result':'PASS-RETAINED-ABI-BYTE-CORRESPONDENCE','vectors':rows,'transactions_executed':False,'actual_admission':False}))
