"""Source/class/relation catalog with exact row provenance, no pair enumeration."""
import csv
import hashlib
from collections import Counter
from pathlib import Path
from v4_ingest.records import canonical, digest, require

CONTEXTS = ('SYMBOLIC-U-ONE', 'SYMBOLIC-U-TWO')
SEMANTIC = 'definition-completion/security-fields.tsv'
FRAMING = 'definition-completion/security-framing-fields.tsv'
SEC_RELS = 'definition-completion/security-relations.tsv'
OLD_NODES = 'producer/augmented-nodes.tsv'
OLD_RELS = 'producer/augmented-edges.tsv'
ROLES = ('carrier', 'diagnostic-cache', 'governing-source', 'profile-issuer',
         'qualified-assessor', 'required-coalition', 'transport-observer')
REF_PARTS = ('owner_source_id', 'source_sha256', 'source_anchor', 'material_sha256')
PARSER_FIELDS = ('schema_id', 'record_id', 'input_record', 'output_record', 'result_kind',
                 'phase', 'attempt_ordinal', 'owner_reference', 'grammar_reference', 'parent_invocation')
MATERIAL_FIELDS = ('exact_bytes', 'lookup_status', 'owning_reference')


def read_rows(base, path):
    raw = (Path(base) / path).read_bytes()
    file_sha = digest(raw)
    require(b'\r' not in raw and raw.endswith(b'\n'), 'source TSV framing')
    rows = list(csv.DictReader(raw.decode('utf-8').splitlines(), delimiter='\t'))
    return [(row, {'input_path': path, 'input_sha256': file_sha, 'data_row': i,
                   'row_sha256': digest(canonical(row))}) for i, row in enumerate(rows, 1)]


class Catalog:
    def __init__(self, base):
        self.base = Path(base)
        self.nodes, self.node_provenance, self.selectors = [], [], {}
        self.relations, self.relation_provenance, self.join_rules = [], [], []
        self.semantic = [r for r, _ in read_rows(base, SEMANTIC)]
        self.framing = [r for r, _ in read_rows(base, FRAMING)]
        self.schemas = sorted({r['schema'] for r in self.semantic})
        self.component_count = len(read_rows(base, 'profile/fragments/candidate-components.tsv'))
        self.input_hashes = {}
        self._build()

    def node(self, row, prov, selector):
        sid = row['node_id']
        require(sid not in self.selectors, 'duplicate surface class: ' + sid)
        self.nodes.append(row)
        self.node_provenance.append(prov)
        self.selectors[sid] = selector
        if 'input_path' in prov:
            self.input_hashes[prov['input_path']] = prov['input_sha256']

    def generated(self, sid, kind, selector, prov, owner='CP2-CONDITIONAL-CONTRACT', anchor='declared-envelope'):
        self.node({'node_id': sid, 'kind': kind, 'owner_source_id': owner, 'owner_anchor': anchor,
                   'declared_exposure': 'UNKNOWN', 'reuse': 'NONE', 'source_data': 'Conditional symbolic class; no qualified fact'}, prov, selector)

    def relation(self, left, right, kind, prov, join='CARTESIAN'):
        self.relations.append({'from_node': left, 'to_node': right, 'relation': kind})
        self.relation_provenance.append(prov)
        self.join_rules.append(join)
        if 'input_path' in prov:
            self.input_hashes[prov['input_path']] = prov['input_sha256']

    def derived(self, prov, rule):
        return dict(prov, derivation=rule)

    def _build(self):
        for row, p in read_rows(self.base, OLD_NODES):
            self.node(row, p, ('OLD', row['node_id']))
        for row, p in read_rows(self.base, OLD_RELS):
            self.relation(row['from_node'], row['to_node'], row['relation'], p, 'INHERITED-COMPONENT')
        for f, p in read_rows(self.base, SEMANTIC):
            self.generated(f['surface_id'], 'SECURITY-FIELD-TEMPLATE', ('SCHEMA', f['schema']), p,
                           f['owner_source_id'], f['owner_anchor'])
        for s in self.schemas:
            p = {'contract_rule': 'one complete record class for every S90 schema', 'schema': s}
            self.generated('SECURITY:' + s + '.$record', 'SECURITY-RECORD-TEMPLATE', ('SCHEMA', s), p, 'PE-G4-SOURCE-S90', 'schemas')
        for f, p in read_rows(self.base, FRAMING):
            selector = ('SCHEMA', f['schema']) if f['cardinality'] == 'ONE-PER-RECORD-FIELD' else ('DIRECTORY', f['schema'])
            self.generated(f['surface_id'], 'SECURITY-FRAMING-TEMPLATE', selector, p,
                           f['owner_source_id'], f['owner_anchor'])
        for role in ROLES:
            self.generated('CP2-CUSTODIAN:' + role, 'CONDITIONAL-CUSTODIAN-ROLE', ('SINGLE', role), {'contract_rule': 'role is a potential custodian, never an appointed actor'})
        # Explicit parsed SOURCE-REF keys. LIST-SOURCE-REF additionally binds every
        # finite-contract item; no opaque reference carrier stands in for its keys.
        for f, p in read_rows(self.base, SEMANTIC):
            if f['type'] not in ('SOURCE-REF', 'LIST-SOURCE-REF'):
                continue
            for part in REF_PARTS:
                sid = 'CP2-REF-PARSER:' + f['schema'] + '.' + f['field'] + '.' + part
                selector = ('REF', f['schema'], f['field'], f['type'])
                self.generated(sid, 'PARSED-SOURCE-REFERENCE-FIELD', selector, self.derived(p, 'exact SOURCE-REF key parse'))
                self.relation(sid, f['surface_id'], 'PARSED-FROM-OWNING-REFERENCE', self.derived(p, 'parsed key/value dependency'), 'PARENT-RECORD')
        for field in PARSER_FIELDS:
            self.generated('CP2-RECORD-PARSER:' + field, 'CONDITIONAL-RECORD-PARSER-EVENT', ('PARSER',), {'contract_rule': 'fixed record parser observer envelope', 'field': field})
        for field in MATERIAL_FIELDS:
            self.generated('CP2-REFERENCE-MATERIAL:' + field, 'CONDITIONAL-MATERIAL-ACQUISITION', ('MATERIAL',), {'contract_rule': 'reference material acquisition bytes/status/owning reference', 'field': field})
        for r, p in read_rows(self.base, SEC_RELS):
            # Preserve every source template. Its OWNS relation is instantiated
            # at the exact owning record, as required by S90's typed record law.
            # The documentary template constructor is not a qualified instance
            # parser and cannot establish cross-record ownership by Cartesian product.
            join = 'SAME-RECORD' if r['relation'] == 'OWNS-RECORD-FIELD' else 'CARTESIAN'
            self.relation(r['from_node'], r['to_node'], r['relation'], p, join)
        for f, p in read_rows(self.base, SEMANTIC):
            rec = 'SECURITY:' + f['schema'] + '.$record'
            self.relation(f['surface_id'], rec, 'EXACT-OWNING-RECORD-FIELD', self.derived(p, 'same owning record identity'), 'SAME-RECORD')
            presence = 'SECURITY-FRAME:' + f['schema'] + '.present:' + f['field']
            self.relation(presence, f['surface_id'], 'PRESENCE-AND-NULL-TAG', self.derived(p, 'registered per-record field presence'), 'SAME-RECORD')
        for f, p in read_rows(self.base, FRAMING):
            if f['schema'] == 'ROOT':
                for s in self.schemas:
                    self.relation(f['surface_id'], 'SECURITY:' + s + '.$record', 'OWNS-SECURITY-OBJECT-DIRECTORY', self.derived(p, 'root/schema object ownership'))
            elif f['cardinality'] == 'ONE-PER-SCHEMA-DIRECTORY':
                self.relation(f['surface_id'], 'SECURITY:' + f['schema'] + '.$record', 'DIRECTORY-RECORD-METADATA', self.derived(p, 'complete schema directory metadata'))
        for path in ('definition-completion/security-custody.tsv', 'definition-completion/framing-custody.tsv'):
            for c, p in read_rows(self.base, path):
                self.relation(c['surface_id'], 'CP2-CUSTODIAN:' + c['potential_role'], 'POTENTIAL-CUSTODY-UNKNOWN', p)
        for s in self.schemas:
            record = 'SECURITY:' + s + '.$record'
            for field in PARSER_FIELDS:
                self.relation('CP2-RECORD-PARSER:' + field, record, 'PARSER-RECORD-CORRESPONDENCE', {'contract_rule': 'parser event joins exact schema and record', 'schema': s, 'field': field}, 'PARSER-SCHEMA')
        for f, p in read_rows(self.base, SEMANTIC):
            if f['type'] in ('SOURCE-REF', 'LIST-SOURCE-REF'):
                for field in MATERIAL_FIELDS:
                    self.relation('CP2-REFERENCE-MATERIAL:' + field, f['surface_id'], 'MATERIAL-REFERENCE-ACQUISITION', self.derived(p, 'source material owning join'), 'MATERIAL-FIELD')
        for node in self.nodes:
            if node['node_id'].startswith(('CP2-REF-PARSER:', 'CP2-RECORD-PARSER:', 'CP2-REFERENCE-MATERIAL:')):
                for role in ROLES:
                    self.relation(node['node_id'], 'CP2-CUSTODIAN:' + role, 'POTENTIAL-CUSTODY-UNKNOWN', {'contract_rule': 'complete conditional parser/material custody', 'surface': node['node_id'], 'role': role})
        ids = set(self.selectors)
        require(all(r['from_node'] in ids and r['to_node'] in ids for r in self.relations), 'unresolved source relation endpoint')

    def class_counts(self):
        return dict(Counter(n['kind'] for n in self.nodes))


def default_contract(catalog):
    """A declared finite test source contract, never an actual source appointment.

    Directory counts are explicit prototype choices, not defaults in a profile.
    FIELD-LABEL includes every declared surface, including its own stable classes.
    """
    counts = {'POLICY': 1, 'ENVELOPE': 1, 'LEAKAGE': 1, 'ALGORITHM': 2, 'ARTIFACT': 2,
              'EXPERIMENT': 3, 'ASSUMPTION': 2, 'QUALIFICATION': 2, 'ARGUMENT': 3,
              'ASSESSMENT': 3, 'OBLIGATION': 4, 'COMPOSITION': 3, 'ASSESSOR-EVENT': 36,
              'OBSERVER': 2, 'FIELD-LABEL': len(catalog.nodes), 'POLICY-APPLICABILITY': 4}
    directories = {s: [f'CP2-{s}-{i:06}' for i in range(1, counts[s] + 1)] for s in catalog.schemas}
    return {
        'format': 'G4-CP2-FINITE-PRODUCER-CONTRACT-V1', 'contract_id': 'G4-CP2-LOCAL-RECORD-PRODUCER-001',
        'contexts': list(CONTEXTS), 'source_inputs': catalog.input_hashes,
        'schema_directories': directories,
        'field_label_surfaces': [n['node_id'] for n in catalog.nodes],
        'reference_list_elements': 2,
        'record_parser_attempts': 2,
        'inherited_repeat_kinds': ['READ-OBJECT-METADATA', 'PROPOSED-EVIDENCE-FIELD', 'PROGRAM-FIELD'],
        'inherited_repeat_slots': ['RETRY', 'ERROR', 'CACHE'],
        'parser': {'code': 'v4_ingest.records.ingest_record', 'input': 'exact canonical S90 record bytes',
                   'output': 'typed owning record or explicit local rejection; neither establishes authority',
                   'event_fields': list(PARSER_FIELDS), 'branch_domain': ['VALID-LOCAL', 'INVALID-LOCAL', 'UNAVAILABLE', 'INAPPLICABLE'],
                   'observer_envelope': 'exact input/output records, fixed event fields, raw material acquisition fields and all inherited registered potential observers',
                   'source_material_interpretation': 'No generic source-specific witness/assessment parser is claimed; unknown actual parser outputs are an admission barrier'},
        'assessor_trace': {'assessments': 3, 'kinds': ['READ', 'CALL', 'RETURN', 'ERROR', 'RETRY', 'CACHE'], 'attempts': 2,
                           'semantics': '36 distinct guarded symbolic event slots; not one observed invocation'},
        'material_acquisition': {'fields': list(MATERIAL_FIELDS), 'status_domain': ['PRESENT', 'UNAVAILABLE', 'INVALID'],
                                 'semantic_parser_qualification': 'UNAVAILABLE'},
        'source_qualified': False, 'observer_qualified': False, 'profile_admitted': False,
        'claim': 'Complete mechanical expansion for this explicit finite conditional contract only',
        'assumptions': ['The supplied finite directories/slots are the entire selected test-source envelope.',
                        'Exact parser and observer correspondence would require independent source qualification.',
                        'No unknown actual source-specific output or production observer class is silently deemed absent.']}
