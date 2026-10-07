"""Full conditional token/structural expansion and exact pair predicate/count.

No full equality enumeration or table digest calculation occurs in this module.
All supplied accepted source relations retain independent row provenance.
"""
from collections import Counter, defaultdict
from .catalog import Catalog, CONTEXTS, PARSER_FIELDS, REF_PARTS, default_contract
from v4_ingest.records import canonical, digest, primitive, require
from v4_ingest.wire import uint, ord6, model_wire_limits

PAIR_HEADER = b'PE-G4-POTENTIAL-EQUALITY-PAIRS-V1\n'
PAIR_PREDICATE = 'left.arbitrary OR right.arbitrary OR equal symbolic_digest'


def validate_contract(cat, c):
    expected = set(default_contract(cat))
    require(type(c) is dict and set(c) == expected, 'exact contract keys')
    require(c['format'] == 'G4-CP2-FINITE-PRODUCER-CONTRACT-V1' and c['contexts'] == list(CONTEXTS), 'contract format / two contexts')
    require(c['source_inputs'] == cat.input_hashes, 'exact accepted input hash bindings')
    require(set(c['schema_directories']) == set(cat.schemas), 'complete 16-schema directory')
    for s, ids in c['schema_directories'].items():
        require(type(ids) is list and ids and all(type(x) is str and x and '::' not in x for x in ids), 'nonempty exact source record directory')
        require(ids == sorted(set(ids)), 'unique ordered record directory')
        for ident in ids:
            primitive('ID', ident)
        if s in ('POLICY', 'ENVELOPE', 'LEAKAGE'):
            require(len(ids) == 1, 'sole owning record')
    require(c['field_label_surfaces'] == [n['node_id'] for n in cat.nodes], 'complete field class directory with canonical provenance order')
    require(len(c['schema_directories']['FIELD-LABEL']) == len(cat.nodes), 'one field label for every declared surface')
    for k in ('reference_list_elements', 'record_parser_attempts'):
        require(type(c[k]) is int and c[k] > 0, 'explicit finite positive multiplicity')
    require(c['parser']['event_fields'] == list(PARSER_FIELDS), 'no parser metadata class omission')
    require(c['material_acquisition']['fields'] == ['exact_bytes', 'lookup_status', 'owning_reference'], 'complete material acquisition fields')
    trace = c['assessor_trace']
    require(trace['kinds'] == ['READ', 'CALL', 'RETURN', 'ERROR', 'RETRY', 'CACHE'], 'all assessor trace branches')
    require(type(trace['assessments']) is int and type(trace['attempts']) is int and trace['assessments'] > 0 and trace['attempts'] > 0, 'finite trace counts')
    require(trace['assessments'] == len(c['schema_directories']['ASSESSMENT']), 'assessment trace count join')
    require(trace['assessments'] * trace['attempts'] * len(trace['kinds']) == len(c['schema_directories']['ASSESSOR-EVENT']), 'complete finite assessor event directory')
    require(c['source_qualified'] is False and c['observer_qualified'] is False and c['profile_admitted'] is False, 'prototype cannot self qualify')
    require(c['inherited_repeat_kinds'] == ['READ-OBJECT-METADATA', 'PROPOSED-EVIDENCE-FIELD', 'PROGRAM-FIELD'], 'required repeated acquisition/record classes')
    require(c['inherited_repeat_slots'] == ['RETRY', 'ERROR', 'CACHE'], 'required retry/error/cache slots')


def record_keys(cat, c, selector):
    kind = selector[0]
    dirs = c['schema_directories']
    if kind == 'OLD':
        sid = selector[1]
        n = cat.component_count if sid.startswith('CORE:COMPONENT-BINDING.') else 1
        return [(i, None) for i in range(1, n + 1)]
    if kind == 'SCHEMA':
        return [(rid, None) for rid in dirs[selector[1]]]
    if kind in ('SINGLE', 'DIRECTORY'):
        return [('CP2-' + kind + '-' + selector[1], None)]
    if kind == 'REF':
        _, schema, field, typ = selector
        elements = c['reference_list_elements'] if typ == 'LIST-SOURCE-REF' else 1
        return [(f'{rid}:REF:{field}:{i:06}', rid) for rid in dirs[schema] for i in range(1, elements + 1)]
    if kind == 'PARSER':
        return [(f'{schema}:{rid}:PARSE:{attempt:06}', rid)
                for schema in cat.schemas for rid in dirs[schema] for attempt in range(1, c['record_parser_attempts'] + 1)]
    if kind == 'MATERIAL':
        keys = []
        for field in cat.semantic:
            if field['type'] in ('SOURCE-REF', 'LIST-SOURCE-REF'):
                n = c['reference_list_elements'] if field['type'] == 'LIST-SOURCE-REF' else 1
                keys += [(f"{field['schema']}:{rid}:REF:{field['field']}:{i:06}", rid)
                         for rid in dirs[field['schema']] for i in range(1, n + 1)]
        return keys
    raise ValueError('unknown selector')


def inherited_component(surface):
    if surface.startswith('CORE:COMPONENT-0'):
        return int(surface.split('COMPONENT-')[1].split('.')[0])
    if surface.startswith('FIELD:PE-TSE-FIELD-COMPONENT-'):
        return int(surface.split('COMPONENT-')[1].split('-')[0])
    return None


def inherited_allowed(left, right):
    a, b = left['surface'], right['surface']
    comp_b, comp_a = inherited_component(b), inherited_component(a)
    return not ((a.startswith('CORE:COMPONENT-BINDING.') and comp_b is not None and left['record'] != comp_b)
                or (b.startswith('CORE:COMPONENT-BINDING.') and comp_a is not None and right['record'] != comp_a))


def symbolic_token(index, surface, context, record, ident):
    sid = surface['node_id']
    fresh = sid.startswith('CORE:') and sid.split('.')[-1].replace('-', '_') == 'transition_occurrence_id'
    constant = surface['reuse'] != 'NONE'
    text = 'FRESH:' + context if fresh else 'CONSTANT:' + sid if constant else 'ARBITRARY'
    return {'index': index, 'id': ident, 'surface': sid, 'context': context, 'record': record,
            'exposure': surface['declared_exposure'], 'reuse': surface['reuse'],
            'arbitrary': not fresh and not constant, 'symbolic_digest': digest(text.encode())}


def expand_tokens(cat, c, progress=lambda *x: None):
    """Preserve inherited tokens exactly as a prefix, then append every new slot."""
    tokens, provenance, lookup, parents = [], [], defaultdict(list), {}
    old = [(i, n) for i, n in enumerate(cat.nodes) if cat.selectors[n['node_id']][0] == 'OLD']
    new = [(i, n) for i, n in enumerate(cat.nodes) if cat.selectors[n['node_id']][0] != 'OLD']
    def append(class_index, node, context, rid, parent, ident, occurrence):
        index = len(tokens)
        tokens.append(symbolic_token(index, node, context, rid, ident))
        lookup[(context, node['node_id'])].append(index)
        parents[index] = parent
        p = {'token_index': index, 'surface_order': class_index + 1,
                           'context': context, 'record': rid, 'parent_record': parent,
                           'occurrence': occurrence}
        # Row provenance is factored once in the class catalog, with this exact
        # surface_order as the join. This saves repeated source text, not edges.
        selector = cat.selectors[node['node_id']]
        if selector == ('SCHEMA', 'ASSESSOR-EVENT'):
            position = c['schema_directories']['ASSESSOR-EVENT'].index(rid)
            trace = c['assessor_trace']
            assessment_index = position // (len(trace['kinds']) * trace['attempts'])
            kind_index = (position // trace['attempts']) % len(trace['kinds'])
            p['symbolic_guard'] = {'assessment_record': c['schema_directories']['ASSESSMENT'][assessment_index],
                                   'event_kind': trace['kinds'][kind_index], 'attempt': position % trace['attempts'] + 1}
        provenance.append(p)
    for context in CONTEXTS:
        for ci, node in old:
            keys = record_keys(cat, c, cat.selectors[node['node_id']])
            for rid, parent in keys:
                ident = context + '::' + node['node_id'] + (f'::RECORD-{rid:06}' if len(keys) > 1 else '')
                append(ci, node, context, rid, parent, ident, 'INHERITED-ORIGINAL')
    inherited_count = len(tokens)
    progress('inherited-tokens', inherited_count)
    for context in CONTEXTS:
        for ci, node in new:
            for rid, parent in record_keys(cat, c, cat.selectors[node['node_id']]):
                append(ci, node, context, rid, parent, context + '::' + node['node_id'] + '::' + str(rid), 'CONDITIONAL-DECLARED-SLOT')
        for ci, node in old:
            if node['kind'] in c['inherited_repeat_kinds']:
                for slot in c['inherited_repeat_slots']:
                    for old_record, _ in record_keys(cat, c, ('OLD', node['node_id'])):
                        rid = f'CP2-{slot}-{old_record:06}'
                        append(ci, node, context, rid, old_record,
                               context + '::' + node['node_id'] + '::' + rid, 'INHERITED-' + slot + '-SLOT')
        progress('context-tokens-complete', len(tokens))
    require(len({t['id'] for t in tokens}) == len(tokens), 'unique expanded token IDs')
    uint(len(tokens) - 1, 32)
    return tokens, provenance, lookup, parents, inherited_count


def structural_edges(cat, c, tokens, lookup, parents, progress=lambda *x: None):
    """Yield canonical edge array rows and exact relation/occurrence provenance.

    Indexed joins avoid accidental quadratic owning/parser joins. Source-required
    Cartesian dependency/custody relations are retained, with no pruning.
    """
    count = 0
    for order, (rel, rule) in enumerate(zip(cat.relations, cat.join_rules), 1):
        ord6(order)
        for context in CONTEXTS:
            left, right = lookup[(context, rel['from_node'])], lookup[(context, rel['to_node'])]
            if rule == 'PARSER-SCHEMA':
                schema = rel['to_node'].split(':', 1)[1].split('.', 1)[0]
                right_by_record = {str(tokens[j]['record']): j for j in right}
                pairs = ((i, right_by_record[parents[i]]) for i in left if str(tokens[i]['record']).startswith(schema + ':'))
            elif rule == 'MATERIAL-FIELD':
                schema_field = rel['to_node'].split(':', 1)[1]
                schema, field = schema_field.split('.', 1)
                right_by_record = {str(tokens[j]['record']): j for j in right}
                pairs = ((i, right_by_record[parents[i]]) for i in left
                         if str(tokens[i]['record']).startswith(schema + ':') and (':REF:' + field + ':') in str(tokens[i]['record']))
            elif rule == 'PARENT-RECORD':
                right_by_record = {str(tokens[j]['record']): j for j in right}
                pairs = ((i, right_by_record[parents[i]]) for i in left)
            elif rule == 'SAME-RECORD':
                right_by_record = {str(tokens[j]['record']): j for j in right}
                pairs = ((i, right_by_record[str(tokens[i]['record'])]) for i in left)
            elif rule == 'INHERITED-COMPONENT':
                # Originals are byte-for-byte retained. Repetition slots repeat
                # the relevant source relation, and are connected to unchanged
                # source classes when only one endpoint is a repeated acquisition.
                def pairs_gen():
                    for i in left:
                        for j in right:
                            a, b = tokens[i], tokens[j]
                            repeat_a, repeat_b = type(a['record']) is str, type(b['record']) is str
                            if repeat_a and repeat_b and a['record'].split('-')[1] != b['record'].split('-')[1]:
                                continue
                            ca = dict(a, record=parents[i]) if repeat_a else a
                            cb = dict(b, record=parents[j]) if repeat_b else b
                            if inherited_allowed(ca, cb):
                                yield i, j
                pairs = pairs_gen()
            else:
                pairs = ((i, j) for i in left for j in right)
            for i, j in pairs:
                count += 1
                yield [i, j, order, rel['relation']], {'edge_order': count, 'relation_order': order,
                                                     'context': context, 'left_record': tokens[i]['record'],
                                                     'right_record': tokens[j]['record'], 'join_rule': rule}
        if order % 500 == 0:
            progress('structural-relations', order, count)


def equality_plan(tokens):
    n = len(tokens)
    fixed = Counter(t['symbolic_digest'] for t in tokens if not t['arbitrary'])
    f = sum(fixed.values())
    choose = lambda x: x * (x - 1) // 2
    count = choose(n) - choose(f) + sum(choose(k) for k in fixed.values())
    size = model_wire_limits(n, n - 1 if n else None, 0, count, len(PAIR_HEADER))
    return {'format': 'PE-G4-POTENTIAL-EQUALITY-PAIRS-V1', 'row_encoding': 'U32-BE left index; U32-BE right index',
            'ordering': 'lexicographic index pairs, i<j', 'predicate': PAIR_PREDICATE,
            'rows': count, 'bytes': size, 'sha256': None}


def potential_pair(tokens, left, right):
    require(type(left) is int and type(right) is int and 0 <= left < right < len(tokens), 'canonical equality pair indexes')
    a, b = tokens[left], tokens[right]
    return a['arbitrary'] or b['arbitrary'] or a['symbolic_digest'] == b['symbolic_digest']


def estimate(cat, c):
    """Exact symbolic multiplicities and safe structural upper bound, O(classes)."""
    validate_contract(cat, c)
    one = {n['node_id']: len(record_keys(cat, c, cat.selectors[n['node_id']])) for n in cat.nodes}
    repeats = {n['node_id']: len(c['inherited_repeat_slots']) * one[n['node_id']]
               for n in cat.nodes if n['kind'] in c['inherited_repeat_kinds'] and cat.selectors[n['node_id']][0] == 'OLD'}
    total_one = {sid: count + repeats.get(sid, 0) for sid, count in one.items()}
    tokens = 2 * sum(total_one.values())
    max_edges = 0
    for r, rule in zip(cat.relations, cat.join_rules):
        a, b = total_one[r['from_node']], total_one[r['to_node']]
        if rule in ('SAME-RECORD', 'PARENT-RECORD'):
            max_edges += 2 * a
        elif rule == 'PARSER-SCHEMA':
            s = r['to_node'].split(':')[1].split('.')[0]
            max_edges += 2 * len(c['schema_directories'][s]) * c['record_parser_attempts']
        elif rule == 'MATERIAL-FIELD':
            s, field = r['to_node'].split(':')[1].split('.', 1)
            typ = next(f['type'] for f in cat.semantic if f['schema'] == s and f['field'] == field)
            max_edges += 2 * len(c['schema_directories'][s]) * (c['reference_list_elements'] if typ == 'LIST-SOURCE-REF' else 1)
        else:
            max_edges += 2 * a * b
    uint(tokens - 1, 32)
    ord6(len(cat.relations))
    return {'tokens_exact': tokens, 'surface_classes': len(cat.nodes), 'relation_templates': len(cat.relations),
            'structural_edges_upper_bound': max_edges, 'all_pairs_upper_bound': tokens * (tokens - 1) // 2,
            'raw_pair_bytes_upper_bound': len(PAIR_HEADER) + 8 * (tokens * (tokens - 1) // 2),
            'model_and_provenance_bytes_conservative_estimate': tokens * 1700 + max_edges * 260,
            'memory_bytes_conservative_estimate': tokens * 4000 + len(cat.nodes) * 12000,
            'construction_runtime_estimate_seconds': [5, 120],
            'full_pair_enumeration_in_this_checkpoint': False,
            'method': 'linear directory count and indexed-join cardinalities; no equality iteration or output allocation'}
