"""Versioned, bounded legacy EIP-155 carrier. No signing or network API.
Only the retained fixture's protected legacy form, low-s, target call (not creation).
Original bytes are the stored/submitted object; encoding below only checks canonicality.
"""
from functools import lru_cache
from lab_evm import keccak,rlp,P,N,G,add
VERSION='I164-SIGNED-ETHEREUM-LEGACY-1'
MAX_BYTES=131072
FIELDS={'signer','chain','nonce','target','calldata','value','gas_limit','gas_price'}
def need(x,m):
 if not x:raise ValueError(m)
def multiply(k,p):
 out=None
 while k:
  if k&1:out=add(out,p)
  p=add(p,p);k>>=1
 return out
def decode_rlp(raw):
 def read(i,depth):
  need(depth<=1 and i<len(raw),'RLP-BOUND');tag=raw[i];i+=1
  if tag<128:return bytes([tag]),i
  list_=tag>=192;base=192 if list_ else 128;n=tag-base
  if n>55:
   width=n-55;need(i+width<=len(raw) and raw[i]!=0,'RLP-LENGTH');n=int.from_bytes(raw[i:i+width],'big');i+=width;need(n>=56,'RLP-LONG-SHORT')
  end=i+n;need(end<=len(raw),'RLP-TRUNCATED')
  if list_:
   out=[]
   while i<end:
    x,i=read(i,depth+1);need(type(x) is bytes,'RLP-NESTED');out.append(x);need(len(out)<=9,'RLP-FIELDS')
   need(i==end,'RLP-LIST-LENGTH');return out,end
  need(not(n==1 and raw[i]<128),'RLP-NONCANONICAL');return raw[i:end],end
 x,end=read(0,0);need(end==len(raw) and type(x) is list and len(x)==9 and rlp(x)==raw,'LEGACY-CANONICAL');return x
@lru_cache(maxsize=32)
def _decode(raw):
 need(type(raw) is bytes and 0<len(raw)<=MAX_BYTES and raw[0]>=192,'UNSUPPORTED-TRANSACTION-FORM')
 x=decode_rlp(raw)
 def uint(b):
  need(len(b)<=32 and (not b or b[0]!=0),'INTEGER-CANONICAL');return int.from_bytes(b,'big')
 nonce,price,gas=map(uint,x[:3]);value=uint(x[4]);v,r,s=map(uint,x[6:]);need(len(x[3])==20,'TARGET-CALL-ONLY');need(v>=35,'UNPROTECTED-LEGACY')
 chain=(v-35)//2;parity=(v-35)%2;need(chain==1313161555,'UNSUPPORTED-NETWORK');need(0<r<N and 0<s<=N//2,'SIGNATURE-SCALAR')
 # Ethereum recovery IDs are 0/1: x=r, not r+N. Recover Q = r^-1(sR-zG).
 xx=r;yy=pow((xx**3+7)%P,(P+1)//4,P);need(yy*yy%P==(xx**3+7)%P,'SIGNATURE-POINT')
 if yy%2!=parity:yy=P-yy
 R=(xx,yy);need(multiply(N,R) is None,'SIGNATURE-SUBGROUP')
 z=int.from_bytes(keccak(rlp(x[:6]+[chain,0,0])),'big');Q=multiply(pow(r,-1,N),add(multiply(s,R),multiply((-z)%N,G)));need(Q is not None,'SIGNATURE-KEY')
 # Explicit independent equation check for recovered Q.
 w=pow(s,-1,N);V=add(multiply(z*w%N,G),multiply(r*w%N,Q));need(V is not None and V[0]%N==r,'SIGNATURE-EQUATION')
 signer=keccak(Q[0].to_bytes(32,'big')+Q[1].to_bytes(32,'big'))[-20:].hex()
 return (signer,str(chain),str(nonce),x[3].hex(),x[5].hex(),str(value),str(gas),str(price),keccak(raw).hex())
def decode(raw):
 a=_decode(bytes(raw));return dict(zip(['signer','chain','nonce','target','calldata','value','gas_limit','gas_price','transaction_hash'],a))
def validate(raw,expected):
 need(type(expected) is dict and set(expected)==FIELDS and all(type(v) is str for v in expected.values()),'EXPECTED-FIELDS')
 d=decode(raw)
 for k in FIELDS:need(d[k]==expected[k],'SIGNED-INTENT:'+k)
 return d
