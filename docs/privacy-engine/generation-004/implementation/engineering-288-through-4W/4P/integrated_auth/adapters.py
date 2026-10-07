"""Bounded file adapters; limits are implementation capabilities, not wire laws."""
import hashlib, os, stat
from pathlib import Path
from collections.abc import Mapping
from v4_ingest.records import require, digest, ValidationError, primitive
from v4_ingest.wire import TOKEN_HEADER, row_order
CAP=16*1024*1024

def checked_path(base,e):
    require(set(e)=={'path','bytes','sha256'},'exact file identity')
    p=Path(e['path']);require(not p.is_absolute() and '..' not in p.parts,'relative file path')
    p=(base/p).resolve();require(p.is_relative_to(base.resolve()),'file containment')
    return p

def chunks(base,e,chunk=65536):
    p=checked_path(base,e);h=hashlib.sha256();n=0
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb') as f:
        before=os.fstat(f.fileno());require(stat.S_ISREG(before.st_mode),'regular file')
        while b:=f.read(chunk):h.update(b);n+=len(b);yield b
        after=os.fstat(f.fileno())
    require(n==e['bytes'] and h.hexdigest()==e['sha256'],'consumed file identity '+str(p),category='INVALID-EVIDENCE-DIGEST')
    require((before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns),'input changed during read',category='INVALID-EVIDENCE-DIGEST')

def small(base,e,cap=CAP):
    require(e['bytes']<=cap,'local record adapter limit; qualification unavailable above capability',category='INCOMPLETE-EVIDENCE-UNIVERSE')
    out=bytearray()
    for b in chunks(base,e):
        require(len(out)+len(b)<=cap,'local record adapter limit',category='INCOMPLETE-EVIDENCE-UNIVERSE');out.extend(b)
    return bytes(out)

class SourceMap(Mapping):
    """Lazy exact bytes. No cache of the complete source/material directory."""
    def __init__(self,base,entries):self.base,self.entries=base,entries
    def __len__(self):return len(self.entries)
    def __iter__(self):return iter(self.entries)
    def __getitem__(self,k):
        e=self.entries[k];require(k==e['sha256'],'source directory key identity',category='INVALID-EVIDENCE-DIGEST')
        return small(self.base,e)

def token_lines(scoped,phase,values):
    yield ('\t'.join(TOKEN_HEADER)+'\n').encode()
    for i,t in enumerate(scoped.tokens,1):
        require(t['exposure'] in ('PUBLIC','ACTION-BOUNDED','CONFIDENTIAL','PRIVATE-ACTOR'),'token exposure')
        d=t['symbolic_digest'] if phase=='STATIC-ADMISSION' else (values.sha(t['id']) if hasattr(values,'group') else digest(values[t['id']]))
        yield ('\t'.join((row_order(i),t['surface'],t['context'],t['id'],d,t['exposure'],t['reuse']))+'\n').encode('ascii')

class TokenMatcher:
    def __init__(self,scoped,phase,values):
        self.it=iter(token_lines(scoped,phase,values));self.pending=bytearray();self.rows=0;self.seen=set()
        self.maximum=max(map(len,token_lines(scoped,phase,values)),default=1)
    def line(self,raw):
        expected=next(self.it,None)
        if self.rows==0:require(raw==('\t'.join(TOKEN_HEADER)+'\n').encode(),'exact token header')
        else:
            require(raw.endswith(b'\n') and b'\r' not in raw,'token terminal LF/no CR')
            try:cells=raw[:-1].decode('ascii').split('\t')
            except UnicodeError as e:raise ValidationError('canonical ASCII token fields') from e
            require(len(cells)==7 and all(c and not c.endswith(' ') for c in cells),'seven nonempty token cells')
            ordinal,surface,context,token,hashed,exposure,reuse=cells
            require(ordinal==row_order(self.rows),'contiguous token ordinal')
            primitive('ID',context);primitive('DIGEST',hashed)
            require(all(33<=ord(c)<=126 for c in surface+token),'model identifier framing')
            require(token not in self.seen,'duplicate token identifier');self.seen.add(token)
            require(exposure in ('PUBLIC','ACTION-BOUNDED','CONFIDENTIAL','PRIVATE-ACTOR'),'token exposure enum')
            require(reuse in ('NONE','GENERATION-CONSTANT'),'token reuse enum')
        require(expected is not None and raw==expected,'exact scoped token identity/value/order mismatch',category='INCOMPLETE-EVIDENCE-UNIVERSE')
        self.rows+=1
    def feed(self,b):
        off=0
        while off<len(b):
            end=b.find(b'\n',off);end=len(b) if end<0 else end+1
            require(len(self.pending)+end-off<=self.maximum,'token row exceeds maximum legal model row')
            self.pending.extend(b[off:end]);off=end
            if self.pending.endswith(b'\n'):self.line(bytes(self.pending));self.pending.clear()
    def finish(self):
        require(not self.pending,'truncated token row: terminal LF required')
        require(next(self.it,None) is None,'missing token rows',category='INCOMPLETE-EVIDENCE-UNIVERSE')
