"""Small CLI, no expansion or large stream entry point."""
import argparse
import json
from pathlib import Path
from v4_ingest.records import parse, ValidationError
from .admission import collect


def main():
    ap = argparse.ArgumentParser(description='CP3 evidence binding and ordered admission checks')
    ap.add_argument('request', type=Path)
    ap.add_argument('--lab-contract', type=Path, help='explicit external CONDITIONAL test hypotheses; never an actual appointment')
    ap.add_argument('--output', type=Path)
    a = ap.parse_args()
    try:
        request = parse(a.request.read_bytes())
        trusted = parse(a.lab_contract.read_bytes()) if a.lab_contract else None
        result = collect(request, trusted)
    except (OSError, ValidationError) as e:
        result = {'result': 'REJECTED', 'earliest_failure': 'INVALID-PROFILE-SCHEMA',
                  'failures': ['INVALID-PROFILE-SCHEMA'], 'reason': str(e), 'profile_admitted': False}
    raw = json.dumps(result, indent=2) + '\n'
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        with a.output.open('x') as f: f.write(raw)
    print(raw, end='')
    return 0 if result['result'] == 'CONDITIONAL-BINDING-AND-ADMISSION-CHECKS-PASS' else 2


if __name__ == '__main__':
    raise SystemExit(main())
