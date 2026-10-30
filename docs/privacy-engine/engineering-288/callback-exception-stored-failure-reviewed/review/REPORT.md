Independent review of I164-callback-exception-stored-failure-correspondence-1.zip

Review author: Formal-Lab[6]. Construction author: SU-Engineering[288D]. The reviewer did not author this construction. Review date: 30 October 2026.

**Verdict: SUPPORTED within the bounded mandatory SOURCE-ONLY callback-exception/stored-failure correspondence contract.** No residual witness was found within this scope. Runtime execution, physical cleanup and qualification remain unestablished.

The target is exactly 84,555,031 bytes, 2,807 entries, SHA-256 0a39361622d3c05c7f46b258bfd7570d632ab57ee87317103cacce1f52822255. CRC, safe unique regular-file membership and all 2,806 manifested hashes pass. Exact dependency recovery and declared changes were checked. Implementation and original evidence remain unchanged.

Source-derived findings

The defining source is source-evidence/prospective_entry.py, 9,485 bytes, SHA-256 a1d80c523ae220228a6b27cac42b5e57a006336e858a8e7db0a75355d6cf2ae9. Independent AST traversal selects the callback call and its own handler rather than assuming the generated catalogue's positions. It distinguishes the guarded callback-exception raise at 181–182 from the normal-callback guard/raise at 184–185.

| Source point | Supported meaning | Limit |
| --- | --- | --- |
| 164 | The selected dispatch handler stores its original error in owner.failure. | Constructed failure provenance, not a newly observed exception object. |
| 179–180 | The selected callback raises; its BaseException handler names client_error. | The role template does not establish completed handler binding before the entry flag. |
| 181 | The selected local owner.failure is tested for non-None. | Same-stored-original continuity at this guard is an explicit conditional premise. |
| 182 | Raise the stored original with client_error as explicit cause. | Cause direction is original → callback cause; separate roles do not prove distinct physical objects. |
| 186–188 | Enter finally, attempt _OWNERS.pop(token, None), then acknowledge normal completion separately. | Entry/attempt are not completion. Pop's return is discarded. |

The six selected points are callback-handler-enter, callback-failure-guard, callback-stored-rethrow, finally-enter, removal-attempt and removal-complete. Each source coordinate, relevant ancestor guard and containing region is checked independently. Source and matching-pin mutations of the cause, catch family, guard and pop key reject through defining-source checks, not just archive identity. Wrong normal-branch guard attribution and catalogue omissions reject.

The mandatory adapter freshly executes the reviewed stored-failure predecessor's validation and assembly, then matches its exact corrected 5,337,262-byte receipt (SHA-256 2523144c01a3bfa57d7e85b51ec3c907dab787ff23057bb4be5763ac9edc4548). Both contexts require the new and the existing normal-callback relations. The retained handle/state failure projectors recompute stored-original provenance. The token-registration prefix must end at the selected callback raise, with registration established and normal callback completion unestablished. A supplied error summary, old receipt, or mutually substituted report fields cannot replace those checks.

The original error is qualified by the child client-operation occurrence. The callback-error role belongs to the selected parent invocation and source handler; its exact producer/history/type/value remain unavailable. Owner, token, client/session/manager forwarding, acquisition, context and instance bindings come from the validated predecessor basis. Equal values do not merge occurrences. The guard-slot continuity premise is separate from selected-owner registry continuity. UNKNOWN registry continuity remains admitted, and cannot establish removal of the selected owner.

A completed source raise establishes the explicit-cause assignment and source-defined implicit-context suppression in the model. It does not observe __context__, rendering, retained evidence bytes or a physical error reference. The source has no inequality guard between the two errors. Enforced role names therefore do not exclude an actual alias/self-cause or establish physical sameness/difference. Unsupported assertions of either physical identity relation reject.

Exception, termination and cleanup limits

A modeled evaluation/interruption exception during handler entry, guard evaluation or source rethrow skips the remaining handler points and proceeds conditionally to finally. Its pending error is distinct as a semantic role from the stored original and callback error; no completed explicit-cause assignment is invented. A later finally/removal exception replaces the pending outward error for this finite prefix. It does not erase the earlier established storage fact or a cause assignment already completed before that failure. No guarantee is made that the original reaches the launcher.

Termination and unobserved continuation establish neither a terminal Python exception nor unwind, later propagation, cleanup or removal. Earlier acknowledged model facts remain preserved. False completion flags mean unestablished, not proof of absence of unobserved effects. Normal pop establishes the selected key absent at that modeled completion only; selected-owner removal additionally requires explicit continuity. Permanent revocation, physical lock release, exclusivity and durability remain unestablished. Normal _run success is never inferred from this branch.

The successful normal-callback branch remains mandatory. Its prior receipt fields are exact, its implementation is unchanged, and focused validation includes the new public bridge to an exact reviewed normal-callback input. The stored-error-none/bare-raise branch, control-callback failures, full launcher retention/cleanup and exceptional owner-lock finalization remain outside this bounded slice; they are not excluded from the real source domain.

Preservation and recovery

All 2,661 predecessor members match the exact previously verified original archive, as do all 95 retained non-input review members. All 100 inherited producer functions/classes and nonfunction AST are unchanged. The exact declared two-file diff matches; six producer functions are added. Runtime sources, original receipts/evidence, prior context fields, historical identities, relationships, ordinals and scoped findings are preserved.

Eighteen present nested archive occurrences and 71 interpretable manifest documents were checked, retaining historical compact/rebased/forensic qualifications. All 2,788 nonmanifest members selected by the supplied process recovery cut are unchanged in the final target. That intermediate outer archive is a retained continuity identity, not freshly verified bytes or a recompression reconstruction. Independent recovery uses the final exact supplied archive and new empty persistent roots.

Engineering's 423 primary, 70 recovered-root and four process/public controls reconcile with their exact progress logs and result identities. They are inspected supporting evidence, separate from fresh independent testing. Engineering's zero-assertion membership failure is preserved, including the 27,000,832-byte undeclared partial (SHA-256 83b8f28be31221022e346d7ae698b8e3440e39261d261707e0db8a24f40058ad), outside the strict predecessor root. Its origin remains UNESTABLISHED. Prior independent 374-current/four-old-checker results, supplied 66/37/3 and earlier 366/75/7, interruptions, failed attempts and partial evidence remain exact and outside new completed totals. No completed campaign was rerun.

Retained boundaries

Runtime callback/storage/error/cause/finally/pop frames remain unavailable. The 18 saved traced invocations and separate frameless Client.state observer remain distinct and unjoined. Constructed controls do not establish actual execution, physical reference identity, full cleanup, lifetime/repetition completeness or qualification. The trusted-process and mandatory-entry boundary remains unchanged; guard-slot and selected-owner continuity remain explicit premises.

All O01–O11 obligations remain bound to 56,813 bytes / SHA-256 2c92141711e260a2ef0271635562cbac5a71aae82ac7e1a52b5dbc6f228d3a45. Four inventory totals and fourteen lifetime totals remain UNKNOWN. Decision B, retention, allowances, accounting, reservations and uncertainty protections remain unchanged. SOURCE-ONLY; cumulative-envelope unadopted; backup kernel-only; streams UNCOMPUTED; readiness/final binding blocked; admission disabled.

No implementation/runtime changes, requests, acquisitions, database/session operations, host-smoke execution, Git saves, policy changes or completed-suite/review/lifecycle reruns were performed. Only necessary predecessor validation dependencies and the new bounded independent controls executed.

Independent completed validation

537 independent completed control records, separate from supplied results and all prior review campaigns. Integrity/composition assertions are additional audits and are not inflated into this count.

| Campaign | Controls | PASS | Expected rejection |
| --- | ---: | ---: | ---: |
| primary | 337 | 92 | 245 |
| recovered | 121 | 44 | 77 |
| source-controls | 46 | 26 | 20 |
| completion | 24 | 0 | 24 |
| fresh-public | 6 | 1 | 5 |
| fresh-normal | 3 | 2 | 1 |

The fresh public CLI accepts the exact current receipt; both mandatory relations and both contexts are required. A coordinated reversal of cause roles in both receipt contexts rejects after fresh derivation. The public normal-callback bridge accepts an exact reviewed state case; nested mutation of its returned result leaves the input intact, and a following fresh semantic call rejects altered authenticated evidence. The new primary/recovered runs exercise both handle/state provenance routes, source-admitted helper escape, no-control and unknown-continuity paths, handler-evaluation jumps, every stage termination/unknown/raise frontier, wrong bindings, reversed cause direction, omitted/duplicate/reordered stages, exact scalar/container/key types, unsupported runtime claims, and mutable expectations.

Twenty-four targeted pure output-validator negatives use fixtures already validated by the new independent mandatory-adapter run. They reject false handler/finally entry, false removal completion and erasure of completed cause facts. They are separate from fresh evidence-binding checks and establish no runtime observation. The six-stage source oracle independently selects AST nodes/guards and rejects coordinated source/pin changes. Both successful roots remain exact: 2,807 regular files, 801 implied directories, all original hashes unchanged after testing.

No new independent control attempt failed. All supplied and inherited failed/interrupted/partial evidence remains in the unchanged input. The supplied 27,000,832-byte partial remains outside strict predecessor membership; its origin is not inferred.

Environment: isolated CPython 3.12.14, optimization 0, bytecode writes disabled, Cryptography 50.0.2. Safety guards prohibit application/session methods, database/network operations, host-session access and writes outside each review-output directory. Static module/class construction and read-only dependency verification are permitted. This provides no new Cryptography 41.0.7 or Steve-host compatibility, wheel-byte authentication, original-record reconciliation or operational qualification.
