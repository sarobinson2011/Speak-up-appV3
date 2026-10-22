# Separate-session independent confirmation — SD-01

**Verdict: independently confirmed closed within the exact pinned response-source domain below.** No remaining SD-01 counterexample was demonstrated in that domain. The original head-response omission reproduces against the preserved old checker and is rejected by the corrected checker before an incomplete catalogue is accepted.

This is a new-session technical review of supplied immutable correction bytes. The reviewer did not author or modify candidate code in this session. The supplied closure's 53 controls remain same-session self-review supporting evidence; they are not relabelled independent. This review is neither independent human assessment nor appointment/qualification and makes no canonical act.

## Inputs and integrity

| Input | Bytes | ZIP entries | SHA-256 |
|---|---:|---:|---|
| Engineering-288C-I164-SD01-correction.zip | 2,393,229 | 232 | e7d90f5ebc09d7bf69b3a10440f8a06e4ce84a86c0ec4528717d4cf479f2e200 |
| Formal-Lab-Engineering-288C-I164-SD01-closure-review.zip | 11,012,005 | 17 | d84178e75eeace33520b3cada2c9b53d0948f65d6f14031b9bd37460cfb69c9f |

Both supplied identities, CRCs, unique safe paths, exact membership against their manifests, and all member sizes/hashes passed before substantive review. The closure's source/input.zip equals the supplied correction byte for byte. Its predecessor (166 entries) and historical review (372 entries) also passed CRC, exact membership and manifests. Full identities are in results/input-integrity.json. Duplicate suffixes in uploaded filenames have no identity significance.

## Pinned domain and source inspection

The response-defining runtime pins are:

- reference/runtime/authority.py: `4565bb30cb637b3cef40a3f1da2b3722840b747ab110fa37eede0cbc2e3b313a`
- reference/runtime/accounting.py: `7c344469895db20062380e60ad60e055e6fc5121a167720bc64162f2e8aa26cc`

The candidate's 34 reference pins passed. SOURCE-IDENTITIES.json also binds the checked correction, old checker, framing implementation, correspondence specification, integration specification and witness.

Supported successful methods: **head, retire, open, decide, query, observe, backup, sign, release, retry_release**. The first seven return HEAD; sign returns SIGNED-RESULT; release and retry_release return their separate result records.

Supported record closure: **RESPONSE, SUCCESS-RESPONSE, ERROR-RESPONSE, SIGNED-RESULT, RELEASE-RESULT, RETRY-RELEASE-RESULT, HEAD, COUNTS, PARTITIONS, RESOURCES, U-ENTRY, STAGE, PENDING, LAST, QUERY, TRANSPORT-ENTRY**. This includes response success/error discrimination, returned nested/directory/null alternatives, source-consistent optional stage/result guards, associated request-method membership and exact body-key sets, and the ten framing members: presence, availability, encoding_length, member_count, exact_bytes, type_tag, key_encoding, separator_encoding, opening_delimiter, closing_delimiter.

I inspected Authority.handle/apply/save/sign and accounting record/query constructors directly. The head method returns s; ordinary mutation fall-through returns self.save's updated HEAD; observe explicitly returns its saved HEAD; release/retry_release construct distinct dictionaries. handle constructs success/error objects and signs the response inside the outer envelope. The two sign returns share fields but differ in recovered, retaining release=false. OPEN creates stage; the failed non-proceed observation branch assigns FAILED-FROZEN and result. LAST is constructed identically in two source branches. accounting supplies query and transport-entry structure. CORRESPONDENCE.md item 6 and INTEGRATION-SPEC.md's nested correspondence and exact source/selector ownership establish the relevant mapping boundary.

The fresh independent AST census compares source constructor field sets and dispatch targets with the corrected obligations, without using schemas to obtain its expected sets. Its source line anchors and field census are in the first control result. This complements direct inspection; it is not a general semantic proof.

## Why the correction closes this omission

response_obligations.source_obligations obtains dispatch and constructor obligations from the two pinned ASTs, rather than generated templates, schemas(), BODIES, a saved expected bundle, the checklist or fixtures. With schemas disabled entirely, identical obligations are still derived.

static_declarations.build calls check_catalogue before generating rows. Exact response-family equality and optional guard checks therefore reject omissions even if a proposed catalogue and regenerated expectation agree with each other. After generation, check_rows walks the independent obligations and requires nested/variant/key rows, types, guards, parents, presence and framing. Normal validate rebuilds through these checks, then compares the complete supplied bundle, including selector/source metadata. check_rows alone is not claimed to check every metadata property.

The original witness is preserved at 4,103 bytes, SHA-256 `0b24589fc1be5bcc63b1d1ef6c53af320b478c1a4d1f1b7d312cc7c2b0352c3d`. Freshly removing head from the old schemas and building its own expected catalogue permits 9,328 rows through old.validate; ingestion of that legitimate witness then fails REQUEST-METHOD-CONTEXT. With the correction, synchronized catalogue and expected-bundle omission rejects SOURCE-RESPONSE-COVERAGE:SUCCESS-RESPONSE. The same control passes for all ten method variants. The unmodified corrected bundle has 9,339 rows and accepts the original witness with five response joins.

The extractor contains local record bindings, type adapters, nullable/directory overrides and optional guard strings. For example, general Subscript/Attribute expressions default to STRING unless overridden. Those mappings have been inspected for these exact sources; they do not prove arbitrary Python inference. Changed source bytes fail the ordinary pin gate; updating the ordinary manifest still fails the separate exact-source compatibility gate. The identifier QUALIFIED_SOURCES names this implementation gate, not actual source qualification. No test bypassed or amended that gate.

## Fresh execution versus supplied evidence

**71 independent final controls passed**, in 13.126 seconds, peak Python process RSS 97,892 KiB, under a 60-second timeout. The total includes:

- source-constructor/dispatch census, catalogue independence and saved-bundle equality;
- original old-checker witness reproduction and ten synchronized catalogue/expectation omissions;
- a selected omitted field in each of the sixteen response families;
- adjacent error/null/type/return-family, optional-guard and request membership omissions;
- emitted nested, method, key and null-row omissions, all ten variant-framing omissions, and row-binding/selector/source-metadata corruption;
- the original head positive, five retained export positives, existing IA-01 projection/reparse comparison, framing distinction, and two source-pin controls.

Saved positives jointly cover successful responses for all ten methods, plus error and unanswered forms. They include ordinary and ZK examples, failed-state evidence and a saved signature-commit cut. This reopens and validates existing bytes only; no lifecycle or process interruption was rerun. No saved successful recovered=true signing response was found. Both recovered boolean alternatives pass synthetic declaration-shape controls, while recovered=true authenticated recovery remains supported only by prior evidence/source reasoning, not fresh lifecycle execution here. Exact saved forms are recorded in results/independent-controls.json.

The candidate's 109 focused checks, 67 affected regressions and six reconciliation controls, and the supplied closure's 50 targeted plus three boundary controls, were inspected with their scripts/results/command records. Their recorded PASS counts are verified in results/preservation.json. They were **not rerun or added to the 71 fresh controls**. Reconciliation testing here is inspection only.

Review-harness failures are separately retained under failures/ with failed scripts and available output. They concern archive prefixes, repeated identical LAST constructors, shared in-memory aliases, and a mistaken saved recovered=true fixture assumption. A separate fixture-inventory inspection also encountered list-valued INDEX.json. No failure was resolved by changing candidate code or weakening a candidate gate; no candidate counterexample is hidden by the final pass count. The original witness's expected old-checker failure is a successful reproduction control, not a new harness failure.

## Historical preservation and limits

Fresh byte verification confirms all 90 historical inventory entries against actual retained historical archive members, and all 43 relationships against their retained digest and predecessor bytes. All 9,339 declaration rows, context slots and constructor inventory remain equal as data. Of shared existing code modules, only static_declarations.py differs between predecessor and correction; the old module is preserved exactly. All 85 predecessor reference/fixture/provenance files are unchanged in the correction. The final candidate extraction still has exactly the manifest membership and all 231 covered files unchanged after review.

This verifies historical bytes and included copies, not an unseen current complete repository. Historical source availability does not establish latest canonical binding.

Excluded: independently derived completeness for all 59 catalogue families, full request-field typing, arbitrary source revisions, general Python control-flow/type proof, every symbolic expansion, complete old/new graph closure, full-domain capacity, operational durability/custody/finality, canonical authority, appointed assessment and qualification. Optional metadata checks are not a substitute for unchanged semantic state validation. Dynamic lifetime multiplicities and UNKNOWN classifications remain unresolved as recorded.

IA-01 closure and prior conditional findings are preserved within their established scopes. No code change, new policy or source-identity allocation follows. STATE.md and SU-Engineering remain canonical; Steve retains human authority. Canonical reconciliation remains blocked pending the exact authoritative baseline/HEAD, complete ordered deltas, current context bindings and traceable native-to-interchange inputs. No canonical registration, qualification or full-domain completeness follows. Stream identities remain **UNCOMPUTED** and actual admission remains **disabled**. No lifecycle, network execution, migration, retention/compaction, large model or stream regeneration occurred.

## Return to Engineering-Anchor[2]

Record this as separate-session independent technical confirmation of SD-01 closure **only within the domain above**, alongside the unchanged candidate and supporting self-review. The SD-01 independent-confirmation task is complete; no further SD-01 implementation change is recommended. Route the result through SU-Engineering[288C] while retaining the canonical-reconciliation block and prior conditional boundaries. This report creates no additional approval gate and authorizes no subsequent construction.
