"""Exact V4 model/token/link adapter. Counts pairs; never enumerates them.

The source-qualified full model is an input. This module does not expand it.
Large checkpoint-2 evidence is reused by retained archive identity separately.
"""
import re
from collections import Counter
from v4_ingest.records import canonical, digest, exact, primitive, require
from v4_ingest.wire import TOKEN_HEADER, LINK_HEADER, row_order, uint


def table(header, rows):
    return ('\t'.join(header) + '\n' + ''.join('\t'.join(str(v) for v in r) + '\n' for r in rows)).encode('utf-8')


class Model:
    def __init__(self, model):
        exact(model, ('surfaces', 'relations', 'tokens', 'structural_edges', 'equality_stream', 'actor_graph_policy'))
        self.value = model
        require(model['actor_graph_policy'] == 'ALL structural and equality edges; no visibility/permission filtering', 'complete actor graph; no pruning')
        for field in ('surfaces', 'relations', 'tokens', 'structural_edges'):
            require(isinstance(model[field], list), 'model array ' + field)
        self.tokens, self.edges = model['tokens'], model['structural_edges']
        self.ids = {}
        require(len(self.tokens) <= 2**32, 'U32 token domain')
        surfaces = [s['node_id'] for s in model['surfaces']]
        require(len(set(surfaces)) == len(surfaces), 'unique full surface classes')
        for i, t in enumerate(self.tokens):
            exact(t, ('index', 'id', 'surface', 'context', 'record', 'exposure', 'reuse', 'arbitrary', 'symbolic_digest'))
            require(type(t['index']) is int and t['index'] == i, 'contiguous zero-based token indexes')
            uint(i, 32)
            primitive('ID', t['context'])
            # Accepted inherited expand_privacy.py uses positive numeric record
            # ordinals; CP2's new owning directories use exact string identities.
            if type(t['record']) is int:require(t['record']>=1,'positive inherited record ordinal')
            else:primitive('ID',t['record'])
            for field in ('id','surface'):
                require(type(t[field]) is str and bool(t[field]) and all(33<=ord(c)<=126 for c in t[field]), 'exact model-derived ASCII identity; not primitive PE-TSE-ID')
            primitive('DIGEST', t['symbolic_digest'])
            require(t['id'] not in self.ids and t['surface'] in surfaces, 'token class/identity join')
            require(type(t['arbitrary']) is bool, 'arbitrary boolean')
            require(t['reuse'] in ('NONE', 'GENERATION-CONSTANT'), 'reuse class')
            require(t['context'] in ('SYMBOLIC-U-ONE', 'SYMBOLIC-U-TWO'), 'both fixed distinct symbolic contexts')
            fresh = t['surface'].startswith('CORE:') and t['surface'].split('.')[-1].replace('-', '_') == 'transition_occurrence_id'
            constant = t['reuse'] != 'NONE'
            symbol = 'FRESH:' + t['context'] if fresh else 'CONSTANT:' + t['surface'] if constant else 'ARBITRARY'
            require(t['arbitrary'] == (not fresh and not constant) and t['symbolic_digest'] == digest(symbol.encode()), 'exact inherited symbolic field law')
            self.ids[t['id']] = i
        require(set(t['surface'] for t in self.tokens) == set(surfaces), 'no unused/missing field class')
        require({(t['surface'], t['context']) for t in self.tokens} == {(s,c) for s in surfaces for c in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO')}, 'complete class/context membership')
        self.structural = set()
        for edge in self.edges:
            require(isinstance(edge, list) and len(edge) == 4 and all(type(x) is int for x in edge[:3]), 'structural layout')
            a, b, order, kind = edge
            require(0 <= a < len(self.tokens) and 0 <= b < len(self.tokens) and 1 <= order <= len(model['relations']), 'structural endpoint/order domain')
            relation = model['relations'][order - 1]
            require(relation['from_node'] == self.tokens[a]['surface'] and relation['to_node'] == self.tokens[b]['surface'] and relation['relation'] == kind, 'exact source relation join')
            self.structural.add((self.tokens[a]['id'], self.tokens[b]['id'], row_order(order), kind))
        fixed = Counter(t['symbolic_digest'] for t in self.tokens if not t['arbitrary'])
        n, f = len(self.tokens), sum(fixed.values())
        self.pair_count = n*(n-1)//2 - f*(f-1)//2 + sum(k*(k-1)//2 for k in fixed.values())
        uint(self.pair_count, 64)
        eq = model['equality_stream']
        exact(eq, ('format','row_encoding','ordering','predicate','rows','sha256','bytes'))
        require(eq['format'] == 'PE-G4-POTENTIAL-EQUALITY-PAIRS-V1' and eq['row_encoding'] == 'U32-BE left index; U32-BE right index' and eq['ordering'] == 'lexicographic index pairs, i<j' and eq['predicate'] == 'left.arbitrary OR right.arbitrary OR equal symbolic_digest', 'inherited exact pair-stream law')
        if eq['sha256'] is not None: primitive('DIGEST', eq['sha256'])
        uint(eq['rows'], 64)
        require(eq['rows'] == self.pair_count, 'exact potential-pair count law')
        uint(eq['bytes'], 64)
        require(eq['bytes'] == len(b'PE-G4-POTENTIAL-EQUALITY-PAIRS-V1\n') + 8*self.pair_count, 'pair byte count')
        self.digest = digest(canonical(model))
        self.surface_digest = digest(canonical(model['surfaces']))
        self.relation_digest = digest(canonical(model['relations']))

    def potential(self, a, b):
        if not (type(a) is int and type(b) is int and 0 <= a < b < len(self.tokens)):
            return False
        x, y = self.tokens[a], self.tokens[b]
        return x['arbitrary'] or y['arbitrary'] or x['symbolic_digest'] == y['symbolic_digest']

    def edge_identity(self, value):
        m = re.fullmatch(r'G4-STRUCTURAL-EDGE-([1-9][0-9]*)', value)
        if m:
            return int(m[1]) <= len(self.edges)
        m = re.fullmatch(r'G4-EQUALITY-PAIR-(0|[1-9][0-9]*)-(0|[1-9][0-9]*)', value)
        return bool(m and self.potential(int(m[1]), int(m[2])))

    def obligation(self, o):
        require(all(n in self.ids for n in o['node_ids']), 'obligation exact token IDs')
        require(all(self.edge_identity(e) for e in o['edge_ids']), 'obligation exact structural/potential identity')

    def token_table(self, phase, values=None):
        if phase != 'STATIC-ADMISSION':
            require(isinstance(values, dict) and set(values) == set(self.ids), 'complete actual owning values; no symbolic fallback')
            require(all(type(v) is bytes for v in values.values()), 'exact actual source-owned octets')
        rows = []
        for i, t in enumerate(self.tokens, 1):
            value_digest = t['symbolic_digest'] if phase == 'STATIC-ADMISSION' else digest(values[t['id']])
            rows.append([row_order(i), t['surface'], t['context'], t['id'], value_digest, t['exposure'], t['reuse']])
        return table(TOKEN_HEADER, rows)

    def validate_link_stream(self, reader, phase, values=None, expected_sha256=None, chunk_bytes=65536):
        from link_stream.validator import ModelIndex,validate_reader,require_complete
        return require_complete(validate_reader(reader,ModelIndex(self,phase,values),expected_sha256,chunk_bytes))

    def validate_links(self, rows, phase, values=None):
        # Compatibility for legacy parsed-row callers. Original-byte authentication
        # MUST use validate_link_stream; this adapter cannot recover original bytes.
        from link_stream.validator import ModelIndex,validate_chunks,require_complete,HEADER
        def chunks():
            yield HEADER
            for row in rows:yield ('\t'.join(row[k] for k in LINK_HEADER)+'\n').encode('ascii')
        require_complete(validate_chunks(chunks(),ModelIndex(self,phase,values)))
        return True
