"""Explicit active version; baseline accepted/ remains immutable historical input."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ACTIVE=ROOT/'amendments/PE-G4-FIELD-CLASS-REF-AMENDMENT-001/v1.0.0'
BINDING=json.loads((ACTIVE/'BINDING.json').read_bytes())
SOURCE_ID=BINDING['source_id']
SOURCE_SHA256=BINDING['files'][SOURCE_ID+'.md']['sha256']

def verify():
    for n,e in BINDING['files'].items():
        raw=(ACTIVE/n).read_bytes()
        if len(raw)!=e['bytes'] or hashlib.sha256(raw).hexdigest()!=e['sha256']:raise ValueError('active amendment identity mismatch '+n)
    for n in ('security-fields.tsv','v4_record_grammar.py'):
        if (ROOT/'v4_ingest/data'/n).read_bytes()!=(ACTIVE/n).read_bytes():raise ValueError('runtime projection differs from versioned amendment '+n)
    return BINDING
verify()

def definition_hashes():
    return {k:BINDING['files'][n]['sha256'] for k,n in [('contract_sha256','ACCEPTANCE-CONTRACT.txt'),('schema_sha256','security-fields.tsv'),('qualification_interface_sha256','qualification-interface.tsv')]}
