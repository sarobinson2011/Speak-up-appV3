# Finite coverage against the unchanged selected contract

Machine-readable complete class mapping: PROJECTION-COVERAGE-4O.json. Reproduce with `python3 coverage_4o.py`. It reads all 4,119 registered classes; it does not expand the model or enumerate pairs. Class coverage is not a full 426,984-token occurrence witness.

| Required form | Classes | Implemented adapter and test | Exact retained source basis |
|---|---:|---|---|
| S90 typed semantic fields, including conditional null |156|Complete record validation then canonical field projection; exhaustive all-S90 oracle and null tests|S90 correction§1–2, lines 309–423; active security-fields.tsv; v4_record_grammar.record_shape/nullable, with4I amendment|
| Complete security records, literal `.$record` |16|Canonical whole-record projection and exact record-ID join; exhaustive oracle and integrated READ record|S90 lines 405–412 and 420–423; CP2 catalog one complete record class per schema|
| ROOT/directory/status/justification/count/identity/presence framing |224|Complete object/directory derivation and explicit source-rule interpretation; exhaustive frame oracle, missing/unavailable/inapplicable tests|S90 lines 372–423; exact security-framing-fields.tsv, including cardinalities|
| SOURCE-REF keys and LIST-SOURCE-REF element keys |200|Complete owning record plus exact parent/item occurrence; exhaustive present-reference oracle and integrated scalar/list cases|S90 typed SOURCE-REF/LIST-SOURCE-REF grammar; CP2 Catalog._build REF and record_keys REF law, bound by selected contract.reference_list_elements|
| Generated record-parser event fields |10|**Required containing-event adapter not implemented.** Generic standalone bytes may not substitute.|selected contract.parser.event_fields and branch_domain; CP2 PARSER selector/record_keys; S90 correction§3 complete parser/occurrence coverage|
| Generated reference-material acquisition fields |3|**Required containing-event adapter not implemented.**|selected contract.material_acquisition.fields/status_domain; CP2 MATERIAL selector/record_keys; S90 correction§3 complete acquisition coverage|
| Other retained classes |3,510|Existing direct source-owned typed-value acquisition/equality retained and regression tested; no new universal containing grammar claim|Exact inherited sources and selected finite envelope; supplied derived TSEV1 type declarations and qualified source correspondence remain necessary|

The 596 implemented projection classes have finite generic dispatch and source-type checks; the small exhaustive oracle covers every S90 schema and registered field/framing family, plus all present SOURCE-REF subfields. The integrated signed model exercises 32 required occurrences, not the complete retained universe. Null SOURCE-REFs cannot provide child keys; applicability/guards must come from a qualified actual-occurrence directory, not fabricated null subfields.

## Concrete remaining code blockers

`python3 -m unittest tests.test_projections.ProjectionTests.test_required_generated_parser_boundary_is_explicit` and `python3 coverage_4o.py` reproduce the boundary. Required classes include `CP2-RECORD-PARSER:input_record` and `CP2-REFERENCE-MATERIAL:lookup_status`; the active dispatch rejects them with INCOMPLETE-EVIDENCE-UNIVERSE. All 13 exact class names are listed in results/4O-required-code-boundary.json. These are already in the selected contract and full retained model, not speculative future extensions. Their fields exist in the model and low-level codecs can carry data, but a complete source-grounded event interpretation/join adapter is unfinished.

Implement complete parser-attempt/source-acquisition records with exact input/output, branch/status, reference/grammar/owner and parent-invocation correspondence before calling the first finite kernel code-complete. Derive the actual guarded occurrence mapping from those owning event records, including unavailable/inapplicable branches; do not require nonexistent reference child fields or silently erase their class/guard obligations.

## Missing concrete/authoritative inputs, not a new universal-parser coding requirement

The selected contract explicitly marks material semantic-parser qualification UNAVAILABLE and says no generic source-specific witness/assessment parser is claimed. Unknown production source/certificate/observer grammars are not silently supported; concrete independently qualified definitions and inputs are required. Direct byte transport or local source-rule assertions do not provide that qualification. Source-owned projections outside the declared finite grammar require their exact supplied grammar before a production adapter can be assessed; this checkpoint does not invent those inputs or reopen the definition.
