"""Exact undirected graph closure, without potential-pair enumeration.

A static arbitrary node connects to every other node. Without arbitrary nodes,
exact symbolic-digest groups are cliques. Occurrence equality uses exact bytes.
Unioning a spanning star per clique preserves precisely its connected components;
this is a reachability computation, never a serialized-stream hash.
"""
from collections import Counter
from v4_ingest.records import require,digest
from v4_ingest.wire import TOKEN_HEADER,row_order
from admission_kernel.model import table

class Closure:
    def __init__(self,model,phase='STATIC-ADMISSION',values=None):
        self.model=model;self.phase=phase;self.values=values;n=len(model.tokens)
        require(phase in ('STATIC-ADMISSION','E','PRE-EXECUTION','PRE-COMMITMENT'),'accepted phase',category='INVALID-ACTION-CONTEXT')
        self.parent=list(range(n))
        for a,b,_,_ in model.edges:self.join(a,b)
        if phase=='STATIC-ADMISSION':
            arbitrary=next((t['index'] for t in model.tokens if t['arbitrary']),None)
            if arbitrary is not None:
                for i in range(n):self.join(arbitrary,i)
            else:
                first={}
                for t in model.tokens:self.join(first.setdefault(t['symbolic_digest'],t['index']),t['index'])
        else:
            from occurrence_values.index import ExactValues
            if isinstance(values,ExactValues):
                first={}
                for t in model.tokens:self.join(first.setdefault(values.group(t['id']),t['index']),t['index'])
                self.roots=[self.find(i) for i in range(n)];return
            require(isinstance(values, dict) and set(values)==set(model.ids) and all(type(v) is bytes for v in values.values()),'complete authenticated owning values',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            first={}
            for t in model.tokens:self.join(first.setdefault(values[t['id']],t['index']),t['index'])
        self.roots=[self.find(i) for i in range(n)]
    def find(self,i):
        while self.parent[i]!=i:
            self.parent[i]=self.parent[self.parent[i]];i=self.parent[i]
        return i
    def join(self,a,b):
        a,b=self.find(a),self.find(b)
        if a!=b:self.parent[b]=a
    def selected(self,seeds):
        require(isinstance(seeds, list) and seeds and len(seeds)==len(set(seeds)),'nonempty unique source-owned seeds',category='INCOMPLETE-EVIDENCE-UNIVERSE')
        require(all(x in self.model.ids for x in seeds),'seed outside complete model',category='INVALID-ACTION-CONTEXT')
        roots={self.roots[self.model.ids[x]] for x in seeds}
        return [i for i,r in enumerate(self.roots) if r in roots]

class ScopedModel:
    """Adapter retains ORIGINAL token indexes and relation orders; TSV ordinals reset."""
    def __init__(self,model,indices):
        selected=set(indices);self.model=model
        require(indices==sorted(selected) and all(type(i) is int and 0<=i<len(model.tokens) for i in indices),'ordered distinct scoped model indexes')
        self.tokens=[model.tokens[i] for i in indices];self.ids={t['id']:t['index'] for t in self.tokens}
        self.structural={row for row in model.structural if row[0] in self.ids and row[1] in self.ids}
        fixed=Counter(t['symbolic_digest'] for t in self.tokens if not t['arbitrary']);n=len(indices);f=sum(fixed.values())
        self.pair_count=n*(n-1)//2-f*(f-1)//2+sum(x*(x-1)//2 for x in fixed.values())
    def potential(self,a,b):return self.model.potential(a,b)
    def token_table(self,phase,values):
        return table(TOKEN_HEADER,[[row_order(i),t['surface'],t['context'],t['id'],t['symbolic_digest'] if phase=='STATIC-ADMISSION' else digest(values[t['id']]),t['exposure'],t['reuse']] for i,t in enumerate(self.tokens,1)])
