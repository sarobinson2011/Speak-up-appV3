"""Concrete finite LAB interface, with explicit external assumption boundary.

No arbitrary PASS callbacks. No actual authority appointment is implemented.
Preimages are selected by this exact mechanism contract, never protocol defaults.
"""
from collections import Counter
from fractions import Fraction
from v4_ingest.records import canonical, digest, exact, parse, primitive, require, ValidationError, _source_refs
from v4_ingest.wire import lp

ROLES = ('policy-governance', 'assessor-competence', 'observer-completeness', 'model-ledger-classification',
         'composition-decomposition', 'source-producer-correspondence', 'proof-soundness',
         'profile-adequacy', 'applicability', 'evidence-authority', 'non-vacuity')


def pair(q):
    return [q.numerator, q.denominator]


class MissingMaterial(ValueError):
    pass


class FiniteLabProvider:
    def __init__(self, trusted, materials, sources):
        require(isinstance(trusted, dict) and trusted.get('format') == 'CP3-FINITE-LAB-SOURCE-CONTRACT-V1', 'explicit external LAB contract')
        require(trusted.get('scope') == 'CONDITIONAL-LOCAL-BINDING-TESTS-ONLY', 'LAB scope cannot be actual appointment')
        self.trusted, self.materials, self.sources = trusted, materials, sources
        from pathlib import Path
        require(trusted['mechanism']['checker_sha256'] == digest(Path(__file__).read_bytes()), 'exact independently selected mechanism code digest', category='INVALID-EVIDENCE-AUTHORITY')

    def raw(self, ref):
        primitive('SOURCE-REF', ref)
        source = self.sources.get(ref['source_sha256'])
        material = self.materials.get(ref['material_sha256'])
        if source is None or material is None:
            raise MissingMaterial('exact source/material unavailable: ' + ref['source_anchor'])
        require(digest(source) == ref['source_sha256'] and digest(material) == ref['material_sha256'], 'source/material octet digest mismatch', category='INVALID-EVIDENCE-DIGEST')
        require(ref['owner_source_id'] == self.trusted['source_id'] and ref['source_sha256'] == self.trusted['source_sha256'], 'independently supplied LAB owner/source mismatch', category='INVALID-EVIDENCE-AUTHORITY')
        require(ref['source_anchor'] in self.trusted['anchors'], 'unbound source anchor', category='INVALID-EVIDENCE-AUTHORITY')
        require(self.trusted['anchors'][ref['source_anchor']] == ref['material_sha256'], 'independent source-anchor/material assertion binding', category='INVALID-EVIDENCE-AUTHORITY')
        return material

    def payload(self, ref):
        obj = parse(self.raw(ref))
        exact(obj, ('format', 'payload', 'dependencies'))
        require(obj['format'] == 'CP3-LAB-MATERIAL-V1' and isinstance(obj['dependencies'], list), 'source-owned material grammar')
        for d in obj['dependencies']: primitive('DIGEST', d)
        return obj['payload']

    def role(self, name):
        ref = self.trusted.get('laboratory_assumptions', {}).get(name)
        require(ref is not None, 'missing independently supplied LAB hypothesis ' + name, category='INVALID-EVIDENCE-AUTHORITY')
        p = self.payload(ref)
        require(p == {'role': name, 'scope': 'FINITE-CONDITIONAL', 'statement': 'Independent qualification is explicitly assumed for these local tests only.'}, 'role assertion scope/meaning', category='INVALID-EVIDENCE-AUTHORITY')
        return ref

    def construction(self, roots):
        # Source-owned parser exposes ALL dependencies; unsupported opaque formats
        # reject instead of being assumed dependency-free. External results are
        # not preconstruction roots and may bind the completed outer digest.
        done, active = set(), set()
        stack = [(r['material_sha256'], False) for r in roots]
        while stack:
            key, leave = stack.pop()
            if leave:
                active.remove(key); done.add(key); continue
            if key in done: continue
            require(key not in active, 'cyclic exact-byte construction')
            raw = self.materials.get(key)
            if raw is None: raise MissingMaterial('construction dependency bytes ' + key)
            require(digest(raw) == key, 'construction dependency digest', category='INVALID-EVIDENCE-DIGEST')
            obj = parse(raw); exact(obj, ('format', 'payload', 'dependencies'))
            require(obj['format'] == 'CP3-LAB-MATERIAL-V1', 'unsupported construction parser')
            p = obj['payload']
            pending = [p]
            while pending:
                value = pending.pop()
                if isinstance(value, dict):
                    require(not (value.get('requires_final_profile') or value.get('requires_admission_result')), 'static construction must precede final digest/result at every depth')
                    pending.extend(value.values())
                elif isinstance(value, list): pending.extend(value)
            active.add(key); stack.append((key, True))
            require(isinstance(obj['dependencies'], list), 'complete parsed dependency directory')
            for dep in obj['dependencies']:
                primitive('DIGEST', dep); stack.append((dep, False))
        return len(done)

    def invocation(self, argument, security, model_digest):
        # Complete mechanism-specific consumed input, including exact referenced
        # source/material bytes, artifacts and independently bound premise bytes.
        consumed = {}
        for _, ref in _source_refs([argument, security]):
            self.raw(ref)
            consumed[ref['source_sha256']] = self.sources[ref['source_sha256']].hex()
            consumed[ref['material_sha256']] = self.materials[ref['material_sha256']].hex()
        premises = self.trusted['premises']
        for name in argument['premise_ids']:
            require(name in premises, 'missing qualified reduction premise', category='INCOMPLETE-EVIDENCE-UNIVERSE')
            self.raw(premises[name]); consumed[premises[name]['material_sha256']] = self.raw(premises[name]).hex()
        # The mechanism consumes the complete declared material dependency closure.
        # Digest-addressed opaque/absent dependencies cannot silently disappear.
        pending = list(consumed)
        done = set()
        while pending:
            key = pending.pop()
            if key in done: continue
            done.add(key)
            if key in self.sources: continue
            raw = self.materials.get(key)
            if raw is None: raise MissingMaterial('invocation dependency bytes ' + key)
            require(digest(raw) == key, 'invocation dependency digest', category='INVALID-EVIDENCE-DIGEST')
            obj = parse(raw); exact(obj, ('format', 'payload', 'dependencies'))
            require(obj['format'] == 'CP3-LAB-MATERIAL-V1' and isinstance(obj['dependencies'], list), 'supported complete dependency grammar')
            consumed[key] = raw.hex()
            for dep in obj['dependencies']:
                primitive('DIGEST', dep); pending.append(dep)
        parts = [('argument', canonical(argument)), ('security', canonical(security)),
                 ('model-digest', model_digest.encode('ascii')), ('consumed-source-bytes', canonical(consumed)),
                 ('premise-directory', canonical({n: premises[n] for n in argument['premise_ids']}))]
        codec = self.trusted['mechanism']['invocation_codec']
        if codec == 'NAMED-L64-V1':
            return b'CP3-LAB-ASSESSMENT-A\n' + b''.join(lp(n.encode()) + lp(b) for n, b in parts)
        if codec == 'CANONICAL-JSON-V1':
            return canonical({'mechanism': 'CP3-LAB-ASSESSMENT-B', 'inputs': {n: b.hex() for n, b in parts}})
        raise ValidationError('unsupported exact source-specific invocation grammar', category='INCOMPLETE-EVIDENCE-UNIVERSE')

    def evaluate(self, argument, experiment, artifacts):
        require(argument['certificate_artifact_ids'], 'certificate absent', category='INCOMPLETE-EVIDENCE-UNIVERSE')
        certs = [parse(__import__('semantic_stream.storage',fromlist=['unhex']).unhex(artifacts[a]['exact_bytes'])) for a in argument['certificate_artifact_ids']]
        require(len(certs) == 1, 'LAB checker supports one complete certificate, not a generic PASS', category='INCOMPLETE-EVIDENCE-UNIVERSE')
        c = certs[0]
        exact(c, ('format', 'experiment_id', 'left_world', 'right_world', 'premise_ids'))
        if c['format'] != 'CP3-FINITE-DISTRIBUTION-CERTIFICATE-V1':
            return {'status': 'UNAVAILABLE', 'bound': None, 'reason': 'unsupported exact finite certificate'}
        if c['experiment_id'] != experiment['experiment_id'] or c['premise_ids'] != argument['premise_ids']:
            return {'status': 'INVALID', 'bound': None, 'reason': 'certificate experiment/premise mismatch'}
        left, right = self.payload(experiment['left_world']), self.payload(experiment['right_world'])
        if c['left_world'] != left or c['right_world'] != right:
            return {'status': 'INVALID', 'bound': None, 'reason': 'certificate differs from source-owned worlds'}
        nv = self.nonvacuity(experiment)
        if nv['status'] != 'VALID': return nv
        if experiment['kind'] == 'COLLISION':
            values = left['distribution']
            groups = Counter(v[0] for v in values)
            n = len(values)
            q = Fraction(sum(v*(v-1)//2 for v in groups.values()), n*(n-1)//2)
        else:
            l, r = self.distribution(left), self.distribution(right)
            q = sum((abs(l.get(v, Fraction()) - r.get(v, Fraction())) for v in set(l) | set(r)), Fraction()) / 2
        return {'status': 'VALID', 'bound': pair(q), 'reason': 'exact finite whole-view distribution; no primitive-security claim'}

    @staticmethod
    def distribution(world):
        rows = world['distribution']
        out = {}
        for key, probability in rows:
            primitive('BYTES', key); primitive('RATIONAL', probability)
            require(key not in out, 'duplicate finite outcome')
            out[key] = Fraction(*probability)
        require(sum(out.values(), Fraction()) == 1 and all(q > 0 for q in out.values()), 'genuine positive normalized world support')
        return out

    def nonvacuity(self, experiment):
        self.role('non-vacuity')
        a, b = self.payload(experiment['left_world']), self.payload(experiment['right_world'])
        keys = ('world_id', 'protected_alternative', 'distribution', 'schedule', 'leakage', 'target', 'coalition', 'occurrences')
        exact(a, keys); exact(b, keys)
        require(a['target'] == b['target'] == experiment['target_id'] and a['coalition'] == b['coalition'] == experiment['coalition_id'], 'world target/coalition join', category='INVALID-ACTION-CONTEXT')
        if a['protected_alternative'] == b['protected_alternative'] or a['world_id'] == b['world_id'] or a['occurrences'] < 1 or b['occurrences'] < 1 or a['schedule'] != b['schedule'] or a['leakage'] != b['leakage']:
            return {'status': 'INVALID', 'bound': None, 'reason': 'NV2 degenerate/mismatched source scope'}
        if experiment['kind'] == 'COLLISION':
            require(len(a['distribution']) >= 2 and all(isinstance(x, list) and len(x) == 2 for x in a['distribution']), 'nonempty distinct relation-valid finite tuples', category='INVALID-ACTION-CONTEXT')
            require(len({x[1] for x in a['distribution']}) == len(a['distribution']), 'distinct finite canonical input tuples', category='INVALID-ACTION-CONTEXT')
        else:
            self.distribution(a); self.distribution(b)
        return {'status': 'VALID', 'bound': None, 'reason': 'finite complete-support contract; independent adequacy is a LAB hypothesis'}
