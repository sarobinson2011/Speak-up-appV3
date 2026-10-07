"""Bounded, restartable construction; immutable hashed segments and atomic state.

Run state is committed only after both data and provenance segment files exist.
Recovery regenerates deterministic tokens/edges and reuses verified segments.
There is no equality-enumeration entry point here.
"""
import argparse
import json
import os
import time
from collections import Counter
from pathlib import Path
from .catalog import Catalog, default_contract
from .expand import expand_tokens, structural_edges, equality_plan, estimate, validate_contract
from v4_ingest.records import canonical, digest, require


def file_digest(path):
    import hashlib
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def atomic_bytes(path, raw):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.part')
    with temp.open('wb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp, path)


class Build:
    def __init__(self, base, contract, output, max_seconds=180, segment_rows=25000):
        self.base, self.output = Path(base), Path(output)
        self.output.mkdir(parents=True, exist_ok=True)
        self.started, self.last_progress = time.monotonic(), 0
        self.max_seconds, self.segment_rows = max_seconds, segment_rows
        require(type(segment_rows) is int and 0 < segment_rows <= 100000, 'bounded segment size')
        require(type(max_seconds) in (int, float) and max_seconds > 0, 'positive runtime budget')
        self.cat = Catalog(base)
        validate_contract(self.cat, contract)
        self.contract = contract
        code = {str(p.relative_to(Path(__file__).parent.parent)): file_digest(p)
                for directory in ('model_kernel', 'v4_ingest')
                for p in (Path(__file__).parent.parent / directory).rglob('*')
                if p.is_file() and '__pycache__' not in p.parts}
        self.binding = {'contract_sha256': digest(canonical(contract)), 'source_inputs': self.cat.input_hashes,
                        'implementation_sha256': code}
        self.state_path = self.output / 'RECOVERY.json'
        if self.state_path.exists():
            self.state = json.loads(self.state_path.read_bytes())
            require(self.state['binding'] == self.binding, 'recovery source/contract/code binding mismatch; use a new output directory')
        else:
            self.state = {'format': 'G4-CP2-RECOVERY-V1', 'binding': self.binding, 'sections': {},
                          'result': 'IN-PROGRESS', 'full_equality_stream': 'NOT-EXECUTED'}
            self.save()

    def save(self):
        atomic_bytes(self.state_path, canonical(self.state))

    def progress(self, stage, *counts, force=False):
        now = time.monotonic()
        if force or now - self.last_progress >= 10:
            item = {'stage': stage, 'counts': counts, 'seconds': round(now - self.started, 3),
                    'last_committed_sections': {k: len(v) for k, v in self.state['sections'].items()}}
            with (self.output / 'progress.jsonl').open('ab') as log:
                log.write(canonical(item))
                log.flush()
            print(json.dumps(item), flush=True)
            self.last_progress = now
        if now - self.started > self.max_seconds:
            self.state['result'] = 'PAUSED-RUNTIME-BUDGET'
            self.save()
            raise TimeoutError('runtime budget reached; completed immutable segments and RECOVERY.json preserved')

    def segment(self, section, number, data, prov):
        entries = self.state['sections'].setdefault(section, [])
        path = self.output / section / f'{number:06}.jsonl'
        provenance_path = self.output / (section + '-provenance') / f'{number:06}.jsonl'
        data_bytes = b''.join(canonical(v) for v in data)
        prov_bytes = b''.join(canonical(v) for v in prov)
        entry = {'path': str(path.relative_to(self.output)), 'sha256': digest(data_bytes), 'rows': len(data), 'bytes': len(data_bytes),
                 'provenance_path': str(provenance_path.relative_to(self.output)), 'provenance_sha256': digest(prov_bytes), 'provenance_bytes': len(prov_bytes)}
        if number < len(entries):
            require(entries[number] == entry and file_digest(path) == entry['sha256'] and file_digest(provenance_path) == entry['provenance_sha256'], 'committed recovery segment mismatch')
        else:
            require(number == len(entries), 'noncontiguous recovery segments')
            for target, raw in ((path, data_bytes), (provenance_path, prov_bytes)):
                if target.exists():
                    require(file_digest(target) == digest(raw), 'uncommitted existing segment has different bytes')
                else:
                    atomic_bytes(target, raw)
            entries.append(entry)
            self.save()
        self.progress(section, number + 1, sum(e['rows'] for e in entries))

    def stream_model(self, pair_plan):
        target = self.output / 'model.json'
        temp = target.with_name(target.name + '.part')
        with temp.open('wb') as out:
            out.write(b'{')
            items = [('actor_graph_policy', 'ALL structural and equality edges; no visibility/permission filtering'),
                     ('equality_stream', pair_plan), ('relations', self.cat.relations),
                     ('structural_edges', None), ('surfaces', self.cat.nodes), ('tokens', None)]
            for i, (key, value) in enumerate(items):
                if i:
                    out.write(b',')
                out.write(canonical(key)[:-1] + b':')
                if key in ('structural_edges', 'tokens'):
                    section = 'edges' if key == 'structural_edges' else 'tokens'
                    out.write(b'[')
                    first = True
                    for entry in self.state['sections'][section]:
                        with (self.output / entry['path']).open('rb') as inp:
                            for line in inp:
                                if not first:
                                    out.write(b',')
                                out.write(line[:-1])
                                first = False
                        self.progress('assemble-model', key, entry['path'])
                    out.write(b']')
                else:
                    out.write(canonical(value)[:-1])
            out.write(b'}\n')
            out.flush()
            os.fsync(out.fileno())
        os.replace(temp, target)
        return {'path': target.name, 'sha256': file_digest(target), 'bytes': target.stat().st_size}

    def run(self, stop_after_token_segments=None):
        self.progress('start', force=True)
        expected = estimate(self.cat, self.contract)
        atomic_bytes(self.output / 'estimate.json', canonical(expected))
        atomic_bytes(self.output / 'surface-provenance.json', canonical(self.cat.node_provenance))
        atomic_bytes(self.output / 'relation-provenance.json', canonical(self.cat.relation_provenance))
        tokens, prov, lookup, parents, inherited_count = expand_tokens(self.cat, self.contract, self.progress)
        require(len(tokens) == expected['tokens_exact'], 'independent multiplicity estimate / actual expansion mismatch')
        for number, start in enumerate(range(0, len(tokens), self.segment_rows)):
            self.segment('tokens', number, tokens[start:start + self.segment_rows], prov[start:start + self.segment_rows])
            if stop_after_token_segments is not None and number + 1 >= stop_after_token_segments:
                self.state['result'] = 'PAUSED-REQUESTED-BOUNDARY'
                self.save()
                return {'result': self.state['result'], 'token_segments': number + 1}
        pair_plan = equality_plan(tokens)
        atomic_bytes(self.output / 'equality-plan.json', canonical(pair_plan))
        inherited = json.loads((self.base / 'privacy/expanded/PRIVACY.candidate.json').read_bytes())
        require(tokens[:inherited_count] == inherited['tokens'], 'inherited original token identity mismatch')
        old_edges = []
        per_relation = Counter()
        edge_buffer, edge_prov = [], []
        number, count = 0, 0
        for edge, ep in structural_edges(self.cat, self.contract, tokens, lookup, parents, self.progress):
            count += 1
            per_relation[edge[2]] += 1
            if edge[0] < inherited_count and edge[1] < inherited_count and edge[2] <= len(inherited['relations']):
                old_edges.append(edge)
            edge_buffer.append(edge)
            # Source row and complete owning records are losslessly obtained by
            # these ordinal joins to relation-provenance and token-provenance.
            edge_prov.append([count, edge[2], 0 if ep['context'] == 'SYMBOLIC-U-ONE' else 1])
            if len(edge_buffer) == self.segment_rows:
                self.segment('edges', number, edge_buffer, edge_prov)
                edge_buffer, edge_prov = [], []
                number += 1
        if edge_buffer:
            self.segment('edges', number, edge_buffer, edge_prov)
        require(count <= expected['structural_edges_upper_bound'], 'structural count exceeds preflight bound')
        require(old_edges == inherited['structural_edges'], 'inherited original edge identity/order mismatch')
        require(set(per_relation) == set(range(1, len(self.cat.relations) + 1)), 'missing instantiated relation template')
        model_identity = self.stream_model(pair_plan)
        ledger = []
        for order, (rel, source) in enumerate(zip(self.cat.relations, self.cat.relation_provenance), 1):
            ledger.append({'duty_id': f'CP2-MODEL-RELATION-{order:06}', 'relation_order': order,
                           'relation_class': rel['relation'], 'expanded_structural_occurrences': per_relation[order],
                           'source_provenance': source, 'disposition': 'NOT-ESTABLISHED',
                           'meaning': 'Complete model construction inventory; no source/privacy duty is discharged'})
        atomic_bytes(self.output / 'model-duty-ledger.jsonl', b''.join(canonical(r) for r in ledger))
        report = {'result': 'COMPLETE-MECHANICAL-EXPANSION-FOR-DECLARED-CONDITIONAL-CONTRACT',
                  'tokens': len(tokens), 'structural_edges': count, 'surface_classes': len(self.cat.nodes),
                  'relation_templates': len(self.cat.relations), 'semantic_fields_preserved': len(self.cat.semantic),
                  'framing_classes_preserved': len(self.cat.framing), 'inherited_original_tokens': inherited_count,
                  'inherited_original_edges': len(old_edges), 'inherited_identity_comparison': 'EXACT-TOKEN-AND-STRUCTURAL-ARRAYS',
                  'old_stream_hash_provenance': 'Retained accepted/Lab evidence; not newly streamed in this checkpoint',
                  'equality_plan': pair_plan, 'model_identity': model_identity,
                  'model_identity_scope': 'Canonical provisional six-key model; equality_stream.sha256 is null until CP4 exact-stream verification',
                  'seconds': round(time.monotonic() - self.started, 3),
                  'schema_record_counts': {s: len(ids) for s, ids in self.contract['schema_directories'].items()},
                  'source_qualified': False, 'observer_qualified': False, 'profile_admitted': False,
                  'actual_profile_complete': False, 'full_pair_enumeration_executed': False,
                  'immutable_obligation_ledger_instantiated': False,
                  'ledger_boundary': 'model-duty-ledger is provenance/completeness inventory; qualified S90 obligation classification/evidence is separate'}
        atomic_bytes(self.output / 'expansion-results.json', canonical(report))
        self.state['result'] = 'COMPLETE-CONDITIONAL-MECHANICAL-EXPANSION'
        self.state['model_identity'] = model_identity
        self.save()
        self.progress('complete', len(tokens), count, force=True)
        return report


def main():
    ap = argparse.ArgumentParser(description='CP2 complete finite-contract expansion; never enumerate equality pairs')
    ap.add_argument('--base', type=Path, default=Path('accepted'))
    ap.add_argument('--contract', type=Path, default=Path('contract/selected-contract.json'))
    ap.add_argument('--output', type=Path, default=Path('results/expansion'))
    ap.add_argument('--max-seconds', type=float, default=180)
    ap.add_argument('--segment-rows', type=int, default=25000)
    ap.add_argument('--stop-after-token-segments', type=int, help='test/recovery boundary; does not proceed to edges')
    a = ap.parse_args()
    try:
        builder = Build(a.base, json.loads(a.contract.read_bytes()), a.output, a.max_seconds, a.segment_rows)
        report = builder.run(a.stop_after_token_segments)
        print(json.dumps(report, indent=2))
        return 0
    except TimeoutError as e:
        print(json.dumps({'result': 'PAUSED-RECOVERABLE', 'reason': str(e)}), flush=True)
        return 3


if __name__ == '__main__':
    raise SystemExit(main())
