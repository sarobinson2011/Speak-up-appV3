"""Documentary S90 grammar. No qualification, model completeness or admission.

These functions define record placement and absence bytes. They do not construct
a governing profile and do not replace independently qualified source parsers.
"""
import csv
import hashlib
import json
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIELDS = list(csv.DictReader((HERE / 'security-fields.tsv').open(), delimiter='\t'))
SCHEMAS = sorted({r['schema'] for r in FIELDS})
SPEC = {s: {r['field']: r['type'] for r in FIELDS if r['schema'] == s} for s in SCHEMAS}
IDENTITY = {s: next(iter(SPEC[s])) for s in SCHEMAS}
ENUM = {
    'EXPERIMENT': {'COLLISION', 'CROSS-ACTION-TRACKING', 'ACTOR-INFORMATION'},
    'QUALIFIED': {'VALID', 'INVALID', 'UNAVAILABLE'},
    'EXPOSURE': {'PUBLIC', 'CONFIDENTIAL', 'PRIVATE-ACTOR'},
    'OBLIGATION': {'EXACT', 'COMPUTATIONAL'},
    'DISPOSITION': {'EXACT-SATISFIED', 'EXACT-VIOLATION', 'COMPUTATIONALLY-BOUNDED', 'NOT-ESTABLISHED'},
    'COMPOSITION': {'UNION', 'SOURCE-QUALIFIED-THEOREM'},
    'ASSESSOR-EVENT': {'READ', 'CALL', 'RETURN', 'ERROR', 'RETRY', 'CACHE'},
    'STAGE': {'STATIC-ADMISSION', 'E', 'PRE-EXECUTION', 'PRE-COMMITMENT'},
}
OBLIGATION_TEMPLATE = ('obligation_id', 'kind', 'target_ids', 'coalition_id', 'node_ids', 'edge_ids', 'experiment_id')
COMPOSITION_TEMPLATE = ('composition_id', 'policy_id', 'experiment_id', 'method', 'theorem_ref', 'qualification_id')

def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')

def unique_object(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError('duplicate JSON key')
        out[k] = v
    return out

def parse(raw):
    if type(raw) is not bytes:
        raise ValueError('byte input')
    value = json.loads(raw.decode('ascii'), object_pairs_hook=unique_object,
                       parse_float=lambda _: (_ for _ in ()).throw(ValueError('floating point')),
                       parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite number')))
    if canonical(value) != raw:
        raise ValueError('noncanonical JSON')
    return value

def exact(value, keys):
    if type(value) is not dict or set(value) != set(keys):
        raise ValueError('exact object keys')

def primitive(kind, value):
    if kind == 'ID':
        if type(value) is not str or re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:#-]*', value, re.ASCII) is None:
            raise ValueError('canonical ID')
    elif kind == 'DIGEST':
        if type(value) is not str or re.fullmatch('[0-9a-f]{64}', value) is None:
            raise ValueError('digest')
    elif kind == 'BYTES':
        if type(value) is not str or re.fullmatch('(?:[0-9a-f]{2})*', value) is None:
            raise ValueError('hex bytes')
    elif kind == 'UINT':
        if type(value) is not int or value < 0:
            raise ValueError('unsigned integer')
    elif kind == 'RATIONAL':
        if type(value) is not list or len(value) != 2 or any(type(x) is not int for x in value):
            raise ValueError('rational pair')
        a, b = value
        if b <= 0 or not 0 <= a <= b or math.gcd(a, b) != 1:
            raise ValueError('reduced probability')
    elif kind == 'SOURCE-REF':
        exact(value, ('owner_source_id', 'source_sha256', 'source_anchor', 'material_sha256'))
        for k in ('owner_source_id', 'source_anchor'):
            primitive('ID', value[k])
        for k in ('source_sha256', 'material_sha256'):
            primitive('DIGEST', value[k])
    elif kind.startswith('LIST-'):
        if type(value) is not list:
            raise ValueError('array')
        for item in value:
            primitive(kind[5:], item)
        if kind == 'LIST-ID' and len(set(value)) != len(value):
            raise ValueError('duplicate identity')
    elif kind.startswith('ENUM-'):
        if type(value) is not str or value not in ENUM[kind[5:]]:
            raise ValueError('enum')
    else:
        raise ValueError('unrecognized primitive')

def nullable(schema, record, field):
    # A missing applicable source field is never made zero/empty/VALID.
    if schema == 'ASSESSMENT' and field == 'validated_bound':
        return record.get('complete_result') in {'INVALID', 'UNAVAILABLE'}
    if schema == 'ASSESSOR-EVENT' and field in {'input_bytes', 'output_bytes'}:
        return True  # Source-qualified event grammar establishes exact applicability.
    if schema == 'COMPOSITION' and field == 'theorem_ref':
        return record.get('method') == 'UNION'
    if schema == 'OBLIGATION' and field == 'experiment_id':
        return record.get('kind') == 'EXACT'
    return False

def record_shape(schema, value, template=False):
    keys = OBLIGATION_TEMPLATE if template and schema == 'OBLIGATION' else COMPOSITION_TEMPLATE if template and schema == 'COMPOSITION' else SPEC[schema]
    exact(value, keys)
    for key in keys:
        if value[key] is None:
            if not nullable(schema, value, key):
                raise ValueError('unjustified field absence')
        else:
            primitive(SPEC[schema][key], value[key])
    if schema == 'ASSESSMENT' and value['complete_result'] != 'VALID' and value['validated_bound'] is not None:
        raise ValueError('nonvalid assessment carries bound')
    if schema == 'COMPOSITION' and value['method'] == 'UNION' and value['theorem_ref'] is not None:
        raise ValueError('UNION has no theorem reference')
    if schema == 'OBLIGATION' and value['kind'] == 'EXACT' and value['experiment_id'] is not None:
        raise ValueError('exact obligation has no experiment')
    if schema == 'EXPERIMENT' and value['maximum'][0] >= value['maximum'][1]:
        raise ValueError('computational maximum must be strictly below one')
    return value

def records(schema, values, template=False):
    if type(values) is not list:
        raise ValueError('record array')
    for value in values:
        record_shape(schema, value, template)
    ids = [v[IDENTITY[schema]] for v in values]
    if ids != sorted(set(ids)) or any('::' in x for x in ids):
        raise ValueError('unique ordered record IDs')
    return values

def security_shape(value):
    exact(value, ('contract_sha256', 'policy', 'schema_sha256', 'qualification_interface_sha256',
                  'experiments', 'assumptions', 'qualification_contracts', 'operating_envelope',
                  'leakage', 'obligations', 'composition_rules'))
    for k in ('contract_sha256', 'schema_sha256', 'qualification_interface_sha256'):
        primitive('DIGEST', value[k])
    p = value['policy']
    exact(p, ('record', 'algorithms', 'artifacts', 'observers', 'field_labels'))
    record_shape('POLICY', p['record'])
    for key, schema in [('algorithms', 'ALGORITHM'), ('artifacts', 'ARTIFACT'),
                        ('observers', 'OBSERVER'), ('field_labels', 'FIELD-LABEL')]:
        records(schema, p[key])
    for key, schema in [('experiments', 'EXPERIMENT'), ('assumptions', 'ASSUMPTION'),
                        ('qualification_contracts', 'QUALIFICATION')]:
        records(schema, value[key])
    record_shape('ENVELOPE', value['operating_envelope'])
    record_shape('LEAKAGE', value['leakage'])
    records('OBLIGATION', value['obligations'], True)
    c = value['composition_rules']
    exact(c, ('directory_id', 'records'))
    primitive('ID', c['directory_id'])
    records('COMPOSITION', c['records'], True)
    if c['directory_id'] != p['record']['composition_id']:
        raise ValueError('composition directory join')
    # Nonempty directories and all semantic/source joins are independent duties.
    # In particular this function grants no validity to an empty experiment set.
    return value

def evidence_shape(value):
    exact(value, ('format', 'profile_digest', 'phase', 'records'))
    if value['format'] != 'PE-G4-SECURITY-RECORDS-V4':
        raise ValueError('evidence format')
    primitive('DIGEST', value['profile_digest'])
    primitive('ENUM-STAGE', value['phase'])
    exact(value['records'], SCHEMAS)
    for schema in SCHEMAS:
        d = value['records'][schema]
        exact(d, ('status', 'justification', 'instances'))
        if type(d['status']) is not str or d['status'] not in {'PRESENT', 'UNAVAILABLE', 'INAPPLICABLE'}:
            raise ValueError('record status')
        if d['justification'] is not None:
            primitive('SOURCE-REF', d['justification'])
        records(schema, d['instances'])
        if (d['status'] == 'PRESENT') != bool(d['instances']):
            raise ValueError('status/instances mismatch')
        if d['status'] == 'INAPPLICABLE' and d['justification'] is None:
            raise ValueError('inapplicability needs owning source justification')
        if schema in {'POLICY', 'ENVELOPE', 'LEAKAGE'} and d['status'] == 'PRESENT' and len(d['instances']) != 1:
            raise ValueError('single record schema')
    return value

def field_digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()
