"""Offline fixture encoding ONLY. Public keys 1/2; never use for operational signing."""
import hashlib
MASK=(1<<64)-1
RC=[0x1,0x8082,0x800000000000808a,0x8000000080008000,0x808b,0x80000001,0x8000000080008081,0x8000000000008009,0x8a,0x88,0x80008009,0x8000000a,0x8000808b,0x800000000000008b,0x8000000000008089,0x8000000000008003,0x8000000000008002,0x8000000000000080,0x800a,0x800000008000000a,0x8000000080008081,0x8000000000008080,0x80000001,0x8000000080008008]
ROT=[[0,36,3,41,18],[1,44,10,45,2],[62,6,43,15,61],[28,55,25,21,56],[27,20,39,8,14]]
def rol(x,n):return ((x<<n)|(x>>(64-n)))&MASK if n else x
def keccak(b):
 b=bytearray(b);b.append(1)
 while len(b)%136!=135:b.append(0)
 b.append(128);a=[0]*25
 for pos in range(0,len(b),136):
  for i in range(17):a[i]^=int.from_bytes(b[pos+8*i:pos+8*i+8],'little')
  for rc in RC:
   c=[a[x]^a[x+5]^a[x+10]^a[x+15]^a[x+20] for x in range(5)]
   d=[c[(x-1)%5]^rol(c[(x+1)%5],1) for x in range(5)]
   z=[0]*25
   for x in range(5):
    for y in range(5):z[y+5*((2*x+3*y)%5)]=rol(a[x+5*y]^d[x],ROT[x][y])
   for x in range(5):
    for y in range(5):a[x+5*y]=z[x+5*y]^((~z[(x+1)%5+5*y])&z[(x+2)%5+5*y])
   a[0]^=rc
 return b''.join(x.to_bytes(8,'little') for x in a)[:32]
def rlp(x):
 if isinstance(x,int):x=x.to_bytes((x.bit_length()+7)//8,'big')
 if isinstance(x,list):b=b''.join(rlp(v) for v in x);base=192
 else:
  b=x
  if len(b)==1 and b[0]<128:return b
  base=128
 if len(b)<56:return bytes([base+len(b)])+b
 n=len(b).to_bytes((len(b).bit_length()+7)//8,'big');return bytes([base+55+len(n)])+n+b
P=2**256-2**32-977;N=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
G=(55066263022277343669578718895168534326250603453777594175500187360389116729240,32670510020758816978083085130507043184471273380659243275938904335757337482424)
def add(a,b):
 if a is None:return b
 if b is None:return a
 x,y=a;u,v=b
 if x==u and (y+v)%P==0:return None
 k=((3*x*x)*pow(2*y,-1,P) if a==b else (v-y)*pow(u-x,-1,P))%P
 z=(k*k-x-u)%P;return z,(k*(x-z)-y)%P
def mul(n):
 a=None;b=G
 while n:
  if n&1:a=add(a,b)
  b=add(b,b);n>>=1
 return a
def tx(nonce,to,data,gas=30000000,key=1):
 chain=1313161555;x=[nonce,0,gas,bytes.fromhex(to),0,data];h=keccak(rlp(x+[chain,0,0]));k=int.from_bytes(hashlib.sha256(b'PUBLIC-LAB-KEY-ONLY'+h+bytes([key])).digest(),'big')%(N-1)+1
 X,Y=mul(k);r=X%N;s=(pow(k,-1,N)*(int.from_bytes(h,'big')+r*key))%N;parity=Y%2
 assert X<N
 if s>N//2:s=N-s;parity^=1
 return rlp(x+[chain*2+35+parity,r,s]).hex()
def word(n):return n.to_bytes(32,'big')
def call(sig,*args):return keccak(sig.encode())[:4]+b''.join(word(a) if isinstance(a,int) else a for a in args)
assert keccak(b'').hex()=='c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'
assert keccak(b'finalize()')[:4].hex()=='4bb278f3'
assert keccak(b''.join(word(x) for x in G))[-20:].hex()=='7e5f4552091a69125d5dfcb7b8c2659029395bdf'
