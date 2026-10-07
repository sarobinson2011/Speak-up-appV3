"""Known authenticated observations override computational budgets."""
from collections import defaultdict
from v4_ingest.records import exact, primitive, require, digest
from v4_ingest.typed import Codec
from v4_ingest.wire import scalar


def observe(data, failures):
    require(isinstance(data, dict) and set(data) in ({'nodes','edges','visibility'}, {'nodes','edges','visibility','edge_visibility'}), 'observation shape')
    require(isinstance(data['nodes'], list) and isinstance(data['edges'], list), 'observation arrays')
    nodes = {}
    for n in data['nodes']:
        exact(n, ('id', 'context', 'exposure', 'reuse', 'value_hex', 'role', 'source_domain', 'action_hex'))
        for key in ('id', 'context', 'source_domain'): primitive('ID', n[key])
        primitive('BYTES', n['value_hex']); primitive('BYTES', n['action_hex'])
        require(n['role'] in ('n', 'a', 'r', 'NOT-APPLICABLE', 'PRIVATE-VALUE', 'REUSABLE-ACTOR-ID', 'PROTECTED-OPENING'), 'source-owned observed role/classification')
        if n['role'] in ('n', 'a', 'r'):
            require(n['exposure'] == 'PUBLIC', 'public PI role/exposure binding')
            scalar(Codec().decode(bytes.fromhex(n['value_hex']), 'PE-TSE-UINT'))
            if n['role'] == 'n':
                scalar(Codec().decode(bytes.fromhex(n['action_hex']), 'PE-TSE-UINT'))
        require(n['id'] not in nodes, 'distinct observed records')
        nodes[n['id']] = n
        if n['exposure'] == 'PUBLIC':
            code = {'PRIVATE-VALUE': 'PUBLIC-PRIVATE-VALUE', 'REUSABLE-ACTOR-ID': 'REUSABLE-IDENTIFIER', 'PROTECTED-OPENING': 'OPENING-DISCLOSURE'}.get(n['role'])
            if code:
                failures.add(code, 'authenticated source-established protected public value ' + n['id'])
                failures.add('ACTOR-RECONSTRUCTION-RISK', 'direct protected disclosure ' + n['id'])
        if n['exposure'] not in ('PUBLIC', 'CONFIDENTIAL', 'PRIVATE-ACTOR'):
            failures.add('INVALID-SURFACE-LABELS', 'UNKNOWN observed exposure')
            failures.add('INCOMPLETE-EVIDENCE-UNIVERSE', 'unknown complete view')
    visibility = data['visibility']
    require(isinstance(visibility, dict), 'qualified complete visibility directory')
    if set(visibility) != set(nodes) or any(v not in ('VISIBLE', 'HIDDEN') for v in visibility.values()):
        failures.add('INVALID-SURFACE-LABELS', 'unknown/missing observation visibility')
        failures.add('INCOMPLETE-EVIDENCE-UNIVERSE', 'complete observer view missing')
    for name, n in nodes.items():
        if n['exposure'] == 'PUBLIC' and visibility.get(name) != 'VISIBLE':
            failures.add('INVALID-SURFACE-LABELS', 'public observation cannot be hidden ' + name)
    # In this local single-view carrier, explicit per-edge visibility is mandatory
    # whenever edges exist. Full qualified coalition adapters remain separate.
    ev = data.get('edge_visibility', [])
    complete_ev = isinstance(ev, list) and len(ev) == len(data['edges']) and all(x in ('VISIBLE','HIDDEN') for x in ev)
    if not complete_ev: failures.add('INCOMPLETE-EVIDENCE-UNIVERSE', 'complete edge visibility missing')
    valid_actions = {}
    for name, n in nodes.items():
        if n['role'] == 'n':
            matches = [a for a in nodes.values() if a['role'] == 'a' and a['context'] == n['context'] and a['source_domain'] == n['source_domain'] and a['value_hex'] == n['action_hex']]
            valid_actions[name] = len(matches) == 1
            if not valid_actions[name]: failures.add('INCOMPLETE-EVIDENCE-UNIVERSE', 'nullifier lacks unique owning action value binding ' + name)
    def permitted(a,b):
        x,y = nodes[a],nodes[b]
        return (x['reuse'] == y['reuse'] == 'GENERATION-CONSTANT' or
                x['source_domain'] == y['source_domain'] and x['role'] == y['role'] and x['value_hex'] == y['value_hex'] and
                (x['role'] in ('r','a') or x['role'] == 'n' and valid_actions.get(a) and valid_actions.get(b) and x['action_hex'] == y['action_hex']))
    adjacency = defaultdict(set)
    observed = defaultdict(set)
    for ei, edge in enumerate(data['edges']):
        require(isinstance(edge, list) and len(edge) == 3 and edge[0] in nodes and edge[1] in nodes, 'source-established edge endpoints')
        a,b,k = edge
        require(a != b, 'no self edge')
        adjacency[a].add(b); adjacency[b].add(a)
        both = visibility.get(a) == visibility.get(b) == 'VISIBLE'
        state = ev[ei] if complete_ev else 'UNKNOWN'
        if state == 'VISIBLE' and not both: failures.add('INVALID-SURFACE-LABELS', 'edge visible with hidden endpoint')
        if k == 'EQUALS' and both:
            if state != 'VISIBLE': failures.add('INVALID-SURFACE-LABELS', 'visible equality cannot be hidden')
            state = 'VISIBLE'
        if both and state == 'VISIBLE' and not (k == 'EQUALS' and permitted(a,b)):
            observed[a].add(b); observed[b].add(a)
    def reach(start, graph=adjacency):
        seen, todo = set(), [start]
        while todo:
            n = todo.pop()
            if n not in seen: seen.add(n); todo.extend(graph[n] - seen)
        return seen
    actors = {n for n, v in nodes.items() if v['exposure'] == 'PRIVATE-ACTOR'}
    public = {n for n, v in nodes.items() if v['exposure'] == 'PUBLIC'}
    for p in public:
        if reach(p) & actors: failures.add('ACTOR-RECONSTRUCTION-RISK', 'full structural/source-established actor path ' + p)
    for p in public:
        if any(nodes[q]['context'] != nodes[p]['context'] for q in reach(p, observed) & public):
            failures.add('CORRELATION-FAILURE', 'source-established visible cross-context path ' + p)
    # Group equal actual bytes: no potential symbolic digest is a known match.
    groups = defaultdict(list)
    for name in public: groups[nodes[name]['value_hex']].append(name)
    for group in groups.values():
        for i, a in enumerate(group):
            for b in group[i+1:]:
                x, y = nodes[a], nodes[b]
                if x['context'] == y['context']: continue
                if not permitted(a,b):
                    failures.add('UNIQUENESS-FAILURE', 'observed protected equal value across actions')
                    failures.add('CORRELATION-FAILURE', 'observed cross-action relationship retained')
