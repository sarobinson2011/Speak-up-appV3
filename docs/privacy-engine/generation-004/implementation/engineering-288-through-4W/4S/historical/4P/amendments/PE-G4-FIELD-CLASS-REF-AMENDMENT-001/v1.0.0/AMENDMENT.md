# PE-G4-FIELD-CLASS-REF-AMENDMENT-001 version 1.0.0

Authority: explicit user approval, AUTHORITY.json SHA-256 5a33a07373db842ed9efc898cf682407d2032175eb7d2c9cb645ad5c6f24cd63.
This is a narrow compatibility amendment to the preserved Engineering[287]/S90 baseline, not evidence of source or mechanism qualification or protocol publication.

FIELD-LABEL.surface_id has type FIELD-CLASS-REF. Its representation is the unchanged canonical JSON string containing the exact case-sensitive field-class name. Its spelling is either an existing ID or an existing ID immediately followed by `.$record`. Its value MUST be an exact member of the complete source-owned surface register bound to the model. Occurrence-qualified token IDs, aliases, names absent from that register and all other dollar spellings are invalid. Canonical JSON retains its accepted serialization; alternate byte encodings are not introduced.

This type applies solely to FIELD-LABEL.surface_id. General ID and OBLIGATION grammar are unchanged. Owner, coalition, visibility, complete field-class coverage and UNKNOWN rules remain unchanged. A supplied register is an input to local membership checks; only the independent source/model correspondence and qualification rules establish its authority and completeness. Missing register context cannot establish validity and must fail through INCOMPLETE-EVIDENCE-UNIVERSE at admission. Malformed spelling remains a schema failure; a well-spelled absent member is an incomplete-universe failure.

Revised normative schema/grammar/contract are the companion files. PE-G4-SOURCE-S90-FCR-001.md consolidates the preserved S90 text with this exact amendment; its source identifier is PE-G4-SOURCE-S90-FCR-001, version 1.0.0. BINDING.json pins all revised and reused normative bytes. Historical accepted/ and predecessor ZIPs remain immutable. Dependent source/procedure, finite contract, provenance, profile, invocation, evidence and signature bindings must be regenerated or verified unchanged; no prior receipt silently migrates.

Exact affected baseline clauses: security-fields.tsv data row 83 (file line 84), S90 line 890; v4_record_grammar.py ID lines 57–59; ACCEPTANCE-CONTRACT lines 385–390 (S90 451–456) and 615 onward (S90 681 onward). Earlier OBLIGATION edge-reference compatibility is unaffected and does not replace FIELD-LABEL references or prove duty coverage.
