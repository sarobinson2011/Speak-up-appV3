"""Exact bytes, atomic existing observation commit; no separate upload authorization."""
from anchor import enc,parse,sha,need,digest
FORMAT='I164-C4-EXACT-EVIDENCE-CHUNKS-2'
MAX_BODY=3145728
CHUNK=131072
MAX_PARTS=24
def store(raw,put):
 need(type(raw) is bytes and 0<len(raw)<=MAX_BODY,'EVIDENCE-BODY-BOUND')
 parts=[raw[n:n+CHUNK] for n in range(0,len(raw),CHUNK)]
 refs=[{'sha256':put(b,CHUNK),'bytes':len(b)} for b in parts]
 return put(enc({'format':FORMAT,'bytes':len(raw),'sha256':sha(raw),'parts':refs}),4096)
def load(ref,get):
 raw=get(ref,262144);m=parse(raw,262144)
 if type(m) is not dict or m.get('format')!=FORMAT:return m # unchanged legacy body, revalidated by caller
 need(set(m)=={'format','bytes','sha256','parts'} and type(m['bytes']) is int and 0<m['bytes']<=MAX_BODY and digest(m['sha256']),'EVIDENCE-MANIFEST')
 need(type(m['parts']) is list and 1<=len(m['parts'])<=MAX_PARTS,'EVIDENCE-PARTS')
 chunks=[]
 for n,p in enumerate(m['parts']):
  need(type(p) is dict and set(p)=={'sha256','bytes'} and digest(p['sha256']) and type(p['bytes']) is int and 0<p['bytes']<=CHUNK,'EVIDENCE-PART')
  need(n==len(m['parts'])-1 or p['bytes']==CHUNK,'EVIDENCE-CHUNK-ORDER')
  b=get(p['sha256'],CHUNK);need(len(b)==p['bytes'] and sha(b)==p['sha256'],'EVIDENCE-CHUNK-BYTES');chunks.append(b)
 full=b''.join(chunks);need(len(full)==m['bytes'] and sha(full)==m['sha256'],'EVIDENCE-EXACT-BODY')
 return parse(full,MAX_BODY)
