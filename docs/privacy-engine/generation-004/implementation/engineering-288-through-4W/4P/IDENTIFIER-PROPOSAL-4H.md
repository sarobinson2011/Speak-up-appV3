# Decision requested: FIELD-LABEL.surface_id only

Recommendation: approve an explicitly versioned, field-specific `FIELD-CLASS-REF` domain for **FIELD-LABEL.surface_id**, preserving the literal string `SECURITY:ALGORITHM.$record` and every existing register spelling. Do not change primitive ID globally, rename `$record`, percent-encode it, replace the field with an edge reference, or apply this proposal to accepted bytes in this checkpoint.

Exact demonstrated conflict:

* accepted/definition-completion/security-fields.tsv line 84, repeated in accepted/sources/PE-G4-SOURCE-S90.md line 890, assigns `ID` to FIELD-LABEL.surface_id.
* accepted/definition-completion/v4_record_grammar.py lines 57–59 accepts ID only under `[A-Za-z0-9][A-Za-z0-9._:#-]*`, excluding `$`.
* ACCEPTANCE-CONTRACT.txt lines 385–390 (S90 lines 451–456) requires the exact complete field-class register, including framing fields, and inherited qualified labels. Lines 615 onward (S90 681 onward) preserve declared full-model coverage and qualified scope.
* S90 structural register lines 970 onward explicitly references `SECURITY:POLICY.$record`; the retained selected model also contains `SECURITY:ALGORITHM.$record`. The exact reproducible example and incident edges are in results/identifier-reconciliation.json. Model SHA-256 08d6e7fb1e0cf37cc7effa76b50eaff0459abc158d9c6f0da52c6c58372b14f1; selected contract c92f3411df0ee6f97d0e97d19f3c145fca15172b6d067471d384a3c1a5065710.

Proposed normative text (decision-only):

“FIELD-LABEL.surface_id has type FIELD-CLASS-REF. Its representation is the unchanged canonical JSON string containing the exact case-sensitive field-class name. Its spelling is either an existing ID or an existing ID immediately followed by `.$record`. Its value must be an exact member of the complete source-owned surface register bound to the model. Occurrence-qualified token IDs, aliases, escapes representing a different value, names absent from that register and all other dollar spellings are invalid. Owner, coalition, visibility, complete field-class coverage and UNKNOWN rules remain unchanged.”

Canonical JSON escaping remains the already accepted canonical serializer's responsibility; the proposal does not introduce an alternate wire spelling. Schema row type changes from ID to FIELD-CLASS-REF only for this field. The grammar dispatcher needs this field-specific domain and the model join needs exact register membership. `proposal/field_class.py` is an isolated executable acceptance prototype; it is not imported into either production validator.

Compatibility: previously conforming ID field references retain the same bytes and meaning. Old validators reject the newly representable literal framing references, so this requires an authoritative versioned clarification/amendment, updated schema/grammar/procedure identities and rebinding/requalification of dependent sources, model/contract/profile artifacts as required by their hash dependencies. It is not safe to promise unchanged downstream digests or to edit the immutable candidate in place. This checkpoint leaves all accepted inputs unchanged. Subsequent work must trace which constructed model fields actually consume the revised type before asserting that the retained model serialization can be reused identically.

OBLIGATION is a separate case. Its node_ids still use accepted ID and cannot embed the literal occurrence token spelling. Accepted incident `G4-STRUCTURAL-EDGE-...` or `G4-EQUALITY-PAIR-...` edge_ids remain available with node_ids empty when the governing duty really permits those references. That workaround does not discharge exact node-duty coverage, and it cannot supply FIELD-LABEL.surface_id. No OBLIGATION change is proposed.

Tests: current accepted rejection remains true; prototype accepts exact ordinary and literal-record register members; rejects missing members, occurrence IDs, percent substitution, Unicode dollar, whitespace and other dollar forms; primitive ID remains unchanged. See tests/test_field_class_proposal.py. No authoritative approval or competent qualification is claimed.
