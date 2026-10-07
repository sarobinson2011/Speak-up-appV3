"""Read-only CLI; JSON report, exit 0 locally valid, 2 rejected, 3 resource/I/O."""
import argparse
import json
import sys
from pathlib import Path
from .records import ingest_evidence, ingest_security, ingest_record, ValidationError, DEFAULT_MAX_BYTES, digest, parse
from .wire import ingest_tables, decode_container, FILES


def main():
    p = argparse.ArgumentParser(description='Engineering[288] checkpoint-1 local ingestion. Never profile admission.')
    p.add_argument('mode', choices=('evidence', 'security', 'record', 'tables', 'container'))
    p.add_argument('path', type=Path)
    p.add_argument('--field-register', type=Path, help='canonical JSON array of complete source-owned field-class names; local membership only, not qualification')
    p.add_argument('--schema', help='required for record mode')
    p.add_argument('--template', action='store_true')
    p.add_argument('--materials', type=Path, help='optional digest-named exact auxiliary bytes; no source qualification')
    p.add_argument('--max-bytes', type=int, default=DEFAULT_MAX_BYTES, help='local read budget (default 16 MiB); not protocol cap')
    a = p.parse_args()
    if (a.mode == 'record') != bool(a.schema) or (a.template and a.mode != 'record'):
        p.error('--schema is required only for record mode; --template is record-only')
    def read(path):
        if a.max_bytes <= 0:
            raise ValidationError('invalid byte budget', category='RESOURCE-LIMIT')
        with path.open('rb') as f:
            raw = f.read(a.max_bytes + 1)
        if len(raw) > a.max_bytes:
            raise ValidationError('local byte budget exceeded; input was not accepted', category='RESOURCE-LIMIT')
        return raw
    def lookup(d):
        path = a.materials / d
        return read(path) if path.is_file() else None
    try:
        register = parse(read(a.field_register)) if a.field_register else None
        if register is not None and (type(register) is not list or not all(type(n) is str for n in register) or len(set(register))!=len(register)):
            raise ValidationError('unique field-class register array required')
        opts = {'field_register':register, 'material_lookup': lookup if a.materials else None, 'max_bytes': a.max_bytes}
        if a.mode == 'tables':
            files = {name: read(a.path / name) for name in FILES}
            report = ingest_tables(files)
        else:
            raw = read(a.path)
            if a.mode == 'evidence':
                _, report = ingest_evidence(raw, **opts)
            elif a.mode == 'security':
                _, report = ingest_security(raw, **opts)
            elif a.mode == 'record':
                ingest_record(raw, a.schema, a.template, a.max_bytes, field_register=register)
                report = {'result': 'LOCALLY-VALID-UNQUALIFIED', 'schema': a.schema, 'template': a.template,
                          'sha256': digest(raw), 'profile_admitted': False,
                          'limit': 'Single-record syntax and local invariants only; directory/model/source joins require contextual ingestion.'}
            else:
                members = decode_container(raw)
                report = {'result': 'CONTAINER-FRAMING-ONLY', 'profile_admitted': False,
                          'members': {k: {'bytes': len(v), 'sha256': digest(v)} for k, v in members.items()}}
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except ValidationError as e:
        print(json.dumps({'result': 'REJECTED', 'category': e.category, 'reason': str(e), 'profile_admitted': False}), file=sys.stderr)
        return 3 if e.category == 'RESOURCE-LIMIT' else 2
    except OSError as e:
        print(json.dumps({'result': 'IO-ERROR', 'reason': str(e), 'profile_admitted': False}), file=sys.stderr)
        return 3


if __name__ == '__main__':
    raise SystemExit(main())
