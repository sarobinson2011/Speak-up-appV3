"""One-pass exact supplied-link bytes, O(model + chunk + longest legal row).

No collection of supplied links, equalities, or per-row visitation state. The
model index is complete and independently bound outside this local operation.
"""
import hashlib,re
from collections import Counter
from v4_ingest.records import ValidationError,require
from v4_ingest.wire import LINK_HEADER,row_order
HEADER=('\t'.join(LINK_HEADER)+'\n').encode('ascii')
ID=re.compile(rb'[A-Za-z0-9][A-Za-z0-9._:#-]*\Z')
ORD=re.compile(rb'[0-9]{6}\Z')

class ModelIndex:
    def __init__(self,model,phase='STATIC-ADMISSION',values=None):
        require(phase in ('STATIC-ADMISSION','E','PRE-EXECUTION','PRE-COMMITMENT','D','U'), 'exact phase', category='INVALID-ACTION-CONTEXT')
        self.model,self.phase=model,phase
        self.tokens={k.encode('ascii'):i for k,i in model.ids.items()}
        self.structural={tuple(x.encode('ascii') for x in row) for row in model.structural}
        self.structural_count=len(self.structural)
        self.values=values
        if phase=='STATIC-ADMISSION':self.potential_count=model.pair_count
        elif hasattr(values,'group'):
            self.potential_count=values.count(model.tokens)
        else:
            require(type(values) is dict and set(values)==set(model.ids) and all(type(v) is bytes for v in values.values()), 'complete independently acquired owning values',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            groups=Counter(values.values());self.potential_count=sum(n*(n-1)//2 for n in groups.values())
        self.expected=self.structural_count+self.potential_count
        self.max_id=max((len(k) for k in self.tokens),default=1)
        self.max_kind=max([len(b'EQUALS')]+[len(r[3]) for r in self.structural])
        # Derived maximum of any LEGAL row in this exact finite universe; not a
        # new protocol field-length cap. Header has its own exact length.
        self.max_line=max(len(HEADER)-1, max(6,len(str(max(1,self.expected))))+2*self.max_id+6+self.max_kind+4)
    def membership(self,cells):
        a,b,order,kind=cells
        require(a in self.tokens and b in self.tokens, 'orphan endpoint',category='INCOMPLETE-EVIDENCE-UNIVERSE')
        if order==b'000000':
            require(kind==b'EQUALS','zero order requires EQUALS')
            i,j=self.tokens[a],self.tokens[b]
            require(i<j,'potential orientation i<j',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            if self.phase=='STATIC-ADMISSION':allowed=self.model.potential(i,j)
            elif hasattr(self.values,'group'):allowed=self.values.group(a.decode())==self.values.group(b.decode())
            else:allowed=self.values[a.decode()]==self.values[b.decode()]
            require(allowed,'illegal equality membership',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            return 'potential'
        require(tuple(cells) in self.structural,'structural relation/provenance membership',category='INCOMPLETE-EVIDENCE-UNIVERSE')
        return 'structural'

class State:
    def __init__(self,index):
        self.index=index;self.rows=0;self.structural=0;self.potential=0
        self.previous=None;self.header=False
    def line(self,line):
        if not self.header:
            require(line+b'\n'==HEADER,'exact LINK_HEADER / UTF-8 no BOM');self.header=True;return
        cells=line.split(b'\t');require(len(cells)==5,'exact five nonempty cells')
        ordinal,a,b,order,kind=cells
        require(all(x and all(33<=v<=126 for v in x) for x in (a,b)), 'model token identifier framing: printable ASCII, no whitespace')
        require(ID.fullmatch(kind) is not None, 'canonical relation class')
        require(ORD.fullmatch(order) is not None,'closed relation ORD6')
        require(ordinal==row_order(self.rows+1).encode('ascii'),'contiguous minimum-width link ordinal')
        row=(a,b,order,kind)
        require(self.previous is None or self.previous<row, 'strict lexical four-cell order; duplicate forbidden')
        category=self.index.membership(row)
        self.rows+=1
        if category=='structural':self.structural+=1
        else:self.potential+=1
        self.previous=row
        require(self.structural<=self.index.structural_count and self.potential<=self.index.potential_count,'too many rows in separate universe',category='INCOMPLETE-EVIDENCE-UNIVERSE')
    def finish(self):
        require(self.header,'missing header')
        require(self.structural==self.index.structural_count,'missing structural rows',category='INCOMPLETE-EVIDENCE-UNIVERSE')
        require(self.potential==self.index.potential_count,'missing potential rows',category='INCOMPLETE-EVIDENCE-UNIVERSE')

def validate_chunks(chunks,index,expected_sha256=None,max_chunk_bytes=1024*1024):
    """Iterate to actual StopIteration. Empty chunks are boundaries, not EOF.

    On rejection, consumed_sha256 hashes exactly chunks obtained, including
    read-ahead in the last chunk; no unread suffix is hashed or claimed consumed.
    """
    state=State(index);h=hashlib.sha256();consumed=0;pending=bytearray();eof=False;failure=None;peak=0
    try:
        require(type(max_chunk_bytes) is int and 0<max_chunk_bytes<=16*1024*1024,'local chunk budget',category='RESOURCE-LIMIT')
        if expected_sha256 is not None:require(type(expected_sha256) is str and re.fullmatch('[0-9a-f]{64}',expected_sha256) is not None,'expected digest shape')
        for chunk in chunks:
            require(type(chunk) is bytes,'reader must supply bytes')
            # Already obtained bytes are always accounted for, even on a budget failure.
            h.update(chunk);consumed+=len(chunk)
            require(len(chunk)<=max_chunk_bytes,'reader chunk exceeds local budget',category='RESOURCE-LIMIT')
            start=0
            while start<len(chunk):
                end=chunk.find(b'\n',start)
                if end<0:end=len(chunk)
                size=len(pending)+end-start
                require(size<=index.max_line,'row exceeds maximum legal size in this bound model')
                pending.extend(chunk[start:end]);peak=max(peak,len(pending))
                if end==len(chunk):break
                state.line(bytes(pending));pending.clear();start=end+1
        eof=True
        require(not pending,'truncated row: terminal LF required')
        state.finish()
        require(expected_sha256 is None or h.hexdigest()==expected_sha256,'exact consumed input digest mismatch',category='INVALID-EVIDENCE-DIGEST')
    except (ValidationError,OSError) as e:
        failure={'code':getattr(e,'category','MISSING-EVIDENCE'),'detail':str(e)}
    complete=eof and failure is None
    return {'result':'PASS-SUPPLIED-LINK-STREAM' if complete else 'REJECTED','complete':complete,'eof_observed':eof,'bytes_consumed':consumed,'consumed_sha256':h.hexdigest(),'complete_stream_sha256':h.hexdigest() if complete else None,'rows_validated':state.rows,'structural_rows':state.structural,'potential_rows':state.potential,'expected_structural_rows':index.structural_count,'expected_potential_rows':index.potential_count,'peak_pending_line_bytes':peak,'chunk_budget_bytes':max_chunk_bytes,'failure':failure,'profile_admitted':False,'actual_qualification_established':False}

def validate_reader(reader,index,expected_sha256=None,chunk_bytes=65536):
    require(type(chunk_bytes) is int and 0<chunk_bytes<=16*1024*1024,'local chunk budget',category='RESOURCE-LIMIT')
    def chunks():
        while True:
            b=reader.read(chunk_bytes)
            if b==b'':return
            yield b
    return validate_chunks(chunks(),index,expected_sha256,max_chunk_bytes=chunk_bytes)

def require_complete(result):
    if not result['complete']:
        f=result['failure'];raise ValidationError(f['detail'],category='INCOMPLETE-EVIDENCE-UNIVERSE' if f['code']=='RESOURCE-LIMIT' else f['code'])
    return result
