"""Deterministic materialization of the explicit CP4I approval; baseline read-only."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ID='PE-G4-FIELD-CLASS-REF-AMENDMENT-001'
DEST=ROOT/'amendments'/ID/'v1.0.0'
SOURCE='PE-G4-SOURCE-S90-FCR-001'

def sha(b):return hashlib.sha256(b).hexdigest()
def wire(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n').encode()
def main():
    DEST.mkdir(parents=True,exist_ok=True);base=ROOT/'accepted/definition-completion'
    approval=(ROOT/'amendment_tools/USER-APPROVAL.txt').read_bytes();proposal=(ROOT/'IDENTIFIER-PROPOSAL-4H.md').read_bytes()
    authority={'format':'PE-G4-COMPATIBILITY-AMENDMENT-AUTHORITY-V1','amendment_id':ID,'version':'1.0.0','authority':'Steve: explicit instruction in this Engineering[288] conversation','user_submission_local':'2026-10-04T11:21:31+01:00','approval_sha256':sha(approval),'approved_proposal_sha256':sha(proposal),'predecessor_checkpoint_sha256':'149c479f6ea7017190d6d13b3db40c1ae5f01a45bb3802d15d63f5a7c407bada','baseline_source_sha256':sha((ROOT/'accepted/sources/PE-G4-SOURCE-S90.md').read_bytes()),'scope':'FIELD-LABEL.surface_id type, exact field-class membership and dependent identity rebinding only','general_ID_changed':False,'OBLIGATION_changed':False,'source_or_mechanism_qualification_established':False,'publication_or_actual_admission_claimed':False}
    (DEST/'AUTHORITY.json').write_bytes(wire(authority));(DEST/'USER-APPROVAL.txt').write_bytes(approval)
    norm=f'''# {ID} version 1.0.0

Authority: explicit user approval, AUTHORITY.json SHA-256 {sha(wire(authority))}.
This is a narrow compatibility amendment to the preserved Engineering[287]/S90 baseline, not evidence of source or mechanism qualification or protocol publication.

FIELD-LABEL.surface_id has type FIELD-CLASS-REF. Its representation is the unchanged canonical JSON string containing the exact case-sensitive field-class name. Its spelling is either an existing ID or an existing ID immediately followed by `.$record`. Its value MUST be an exact member of the complete source-owned surface register bound to the model. Occurrence-qualified token IDs, aliases, names absent from that register and all other dollar spellings are invalid. Canonical JSON retains its accepted serialization; alternate byte encodings are not introduced.

This type applies solely to FIELD-LABEL.surface_id. General ID and OBLIGATION grammar are unchanged. Owner, coalition, visibility, complete field-class coverage and UNKNOWN rules remain unchanged. A supplied register is an input to local membership checks; only the independent source/model correspondence and qualification rules establish its authority and completeness. Missing register context cannot establish validity and must fail through INCOMPLETE-EVIDENCE-UNIVERSE at admission. Malformed spelling remains a schema failure; a well-spelled absent member is an incomplete-universe failure.

Revised normative schema/grammar/contract are the companion files. {SOURCE}.md consolidates the preserved S90 text with this exact amendment; its source identifier is {SOURCE}, version 1.0.0. BINDING.json pins all revised and reused normative bytes. Historical accepted/ and predecessor ZIPs remain immutable. Dependent source/procedure, finite contract, provenance, profile, invocation, evidence and signature bindings must be regenerated or verified unchanged; no prior receipt silently migrates.

Exact affected baseline clauses: security-fields.tsv data row 83 (file line 84), S90 line 890; v4_record_grammar.py ID lines 57–59; ACCEPTANCE-CONTRACT lines 385–390 (S90 451–456) and 615 onward (S90 681 onward). Earlier OBLIGATION edge-reference compatibility is unaffected and does not replace FIELD-LABEL references or prove duty coverage.
'''
    (DEST/'AMENDMENT.md').write_text(norm)
    schema=(base/'security-fields.tsv').read_text();old='SECURITY:FIELD-LABEL.surface_id\tFIELD-LABEL\tsurface_id\tID\t';new=old.replace('\tID\t','\tFIELD-CLASS-REF\t');assert schema.count(old)==1;schema=schema.replace(old,new)
    grammar=(base/'v4_record_grammar.py').read_text()
    grammar=grammar.replace('def primitive(kind, value):','def primitive(kind, value, field_register=None):')
    anchor="    elif kind == 'DIGEST':"
    branch="""    elif kind == 'FIELD-CLASS-REF':
        if type(value) is not str or re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:#-]*(?:\\.\\$record)?', value, re.ASCII) is None:
            raise ValueError('canonical field-class spelling')
        if type(field_register) not in (list, tuple, set, frozenset) or not all(type(n) is str for n in field_register) or value not in field_register:
            raise ValueError('exact complete source-owned field-class register membership required')
"""
    grammar=grammar.replace(anchor,branch+anchor,1)
    grammar=grammar.replace('def record_shape(schema, value, template=False):','def record_shape(schema, value, template=False, field_register=None):').replace('primitive(SPEC[schema][key], value[key])','primitive(SPEC[schema][key], value[key], field_register)')
    grammar=grammar.replace('def records(schema, values, template=False):','def records(schema, values, template=False, field_register=None):').replace('record_shape(schema, value, template)','record_shape(schema, value, template, field_register)')
    grammar=grammar.replace('def security_shape(value):','def security_shape(value, field_register=None):').replace('def evidence_shape(value):','def evidence_shape(value, field_register=None):').replace('records(schema, p[key])','records(schema, p[key], field_register=field_register)').replace("records(schema, d['instances'])","records(schema, d['instances'], field_register=field_register)")
    contract=(base/'ACCEPTANCE-CONTRACT.txt').read_text()+'\n\nAPPROVED COMPATIBILITY AMENDMENT '+ID+' v1.0.0\n'+norm
    for n,b in [('security-fields.tsv',schema.encode()),('v4_record_grammar.py',grammar.encode()),('ACCEPTANCE-CONTRACT.txt',contract.encode()),('qualification-interface.tsv',(base/'qualification-interface.tsv').read_bytes())]:(DEST/n).write_bytes(b)
    source=(ROOT/'accepted/sources/PE-G4-SOURCE-S90.md').read_text()
    for n,newtext in [('security-fields.tsv',schema),('v4_record_grammar.py',grammar),('ACCEPTANCE-CONTRACT.txt',contract)]:
        oldtext=(base/n).read_text();assert source.count(oldtext)==1;source=source.replace(oldtext,newtext)
    source=f'# {SOURCE} version 1.0.0 — authorized FIELD-CLASS-REF consolidation\n\n'+norm+'\n\n## Preserved S90 body with the three explicit replacements above\n\n'+source
    (DEST/(SOURCE+'.md')).write_text(source)
    names=['AUTHORITY.json','USER-APPROVAL.txt','AMENDMENT.md','security-fields.tsv','v4_record_grammar.py','ACCEPTANCE-CONTRACT.txt','qualification-interface.tsv',SOURCE+'.md']
    pins={n:{'bytes':(DEST/n).stat().st_size,'sha256':sha((DEST/n).read_bytes())} for n in names}
    (DEST/'BINDING.json').write_bytes(wire({'amendment_id':ID,'version':'1.0.0','source_id':SOURCE,'files':pins,'baseline_preserved':True,'actual_admission_enabled':False}))
    # Explicit runtime projections; these are not historical accepted inputs.
    for n in ('security-fields.tsv','v4_record_grammar.py'):(ROOT/'v4_ingest/data'/n).write_bytes((DEST/n).read_bytes())
    print(json.dumps({'result':'MATERIALIZED','directory':str(DEST),'source_sha256':pins[SOURCE+'.md']['sha256']}))
if __name__=='__main__':main()
