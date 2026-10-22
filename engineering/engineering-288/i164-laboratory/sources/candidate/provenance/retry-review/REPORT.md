# Formal-Lab[3]: prospective retries / Option A review

Return route: Engineering-Anchor[2], then SU-Engineering[288C]. This is a noncanonical, single-session AI review, not appointed assessor qualification. Steve remains sole human project authority. STATE.md and SU-Engineering remain canonical. Actual admission remains disabled.

## Separate verdicts

**Accounting/retry mechanics: supported within the declared conditional offline laboratory scope.** No implementation defect was demonstrated in the reviewed changes. This is bounded source inspection and executable evidence, not proof over every input or operational assurance.

**Structural capacity derivation: supported as upper bounds of 101 ordinary / 61 ZK attempts for this implemented branch graph and conservative hold policy.** Concrete maximal-message attainability and full-domain capacity remain unestablished. The unchanged 102 cap is a guard, not evidence of an attainable 102-attempt path. No 103-attempt requirement is established.

Option A is adopted and was not reopened. No candidate code, adopted limits, policy, definition or historical session was changed.

## Verified replacement input

Engineering-288C-I164-prospective-retries-recovery-1.zip: 104,609,027 bytes; SHA-256 4b968d3c9fe5db96ce1c1d0092d321d83f6bf92c412fdc0c4e15dd7b55642a76; 505 entries. Fresh verification passed CRC, unique safe paths, exact recovery-manifest membership and all 504 covered identities. The checkpoint contains 499 files: its manifest plus 498 covered files, all verified.

This is the explicitly supplied replacement content basis. The original declared ZIP (54,899,989 bytes; SHA-256 1f06a4034fab8ab7e0c17ea409ea15d113c9106f63bbfad96291fcb1368e5f09) remains unavailable. The incomplete 50,045,652-byte copy with SHA-256 859cbc5f79a032ed07c24e8d64b707ef15da0d13f060fe50c5f37b7305631e74 remains preserved in the replacement archive. No historical recovery search or original-container reconstruction occurred. Recovery-report claims about the two former extracted directories and local-entry scan were inspected as recorded provenance, not independently re-performed here. Completeness is relative to the supplied manifests, not an independent signature of origin.

The nested adopted accounting archive freshly matches 46,264,582 bytes and SHA-256 94054453064f337ebe67716d82548e4bfe7bb5ecea69a56d5753aa76e969283d. Its CRC, exact 131-entry membership and 130 covered identities pass. DECISION.md, RETRY-SPEC.md, ACCOUNTING.md and PATHS.md match their retained source bytes. The later adoption record and TASK-AUTHORITY supply the prospective authority sequence; historical pending-policy text does not undo the later adoption.

All 90 historical candidate files were freshly compared byte-for-byte against that nested predecessor; all match. The predecessor authority matches basis/authority-before.py; ownership.py is unchanged. All 498 checkpoint-manifest-covered files still match after review. One failed review harness created an additional results file below the extracted template directory; it changed no supplied file. That file is preserved separately in this return as harness-failure evidence and is not treated as a candidate member.

## Exact reviewed code

| Source | SHA-256 |
|---|---|
| prospective/authority.py | 4565bb30cb637b3cef40a3f1da2b3722840b747ab110fa37eede0cbc2e3b313a |
| prospective/accounting.py | 7c344469895db20062380e60ad60e055e6fc5121a167720bc64162f2e8aa26cc |
| prospective/ownership.py | 484bb578e1fff08bd397fea25987c929400bb203ae72cf55b8091db5007b2b18 |
| basis/authority-before.py | c51c8397c57e28c4dc52380e2b6e4562742a4ed2bb2e9e3794092333593eaafd |
| basis/I164-RETRY-ACCOUNTING-ADOPTION-1.md | c68fbb8fdeca0a4ece064428dd37b1cbbf10c334cef245e2f7e4608847b6b059 |
| basis/RETRY-SPEC.md | 3e566de62f6efa24222a1ca226a096893d6b6f110f2e34d12bb904c700ac181a |

SOURCE-REFERENCES.json and SOURCE-MANIFEST.json identify the remaining evidence and source anchors. The runtime identity is I164-PROSPECTIVE-LAB-RETRY-3. The source differences implement new accounting.py and modify authority.py; this review does not enlarge the earlier kernel verdict to this new code without the conditional findings stated here.

## Source-to-behavior assessment

The adopted clarification, paragraphs 1–3, requires once-only exceptional-slot classification, permanent attempt charges and atomic headroom before possible transmission. accounting.reserve (lines 21–30) checks attempt, consumed-plus-held slots, query reservations and applicable verifier budgets before incrementing any authoritative counters. DECIDE and retry_release call it inside Authority.transaction / BEGIN IMMEDIATE. Changes, ancestry blobs and published state commit together. Failure rolls back those changes; a request challenge can remain in the journal. Rejection therefore does not mean every database byte stays unchanged: retained request/rejection evidence is permitted, while state, events, blobs, ownership and charges remain conserved.

accounting.settle (53–59) converts only the first attempt's HELD entry to CONSUMED on definite revert or semantic FAILED. Retries enter CONSUMED at authorization and are never consumed a second time. Success releases only the first unused hold. Attempt charges and retry slots remain permanent. One original attempt plus one retry followed by logical failure consumes two slots, not three. This does not identify which identical-byte transmission caused inclusion.

The pending query carries its request hash, ordinal, exact attempt ID and ATTEMPT/EXTRA classification. authority.observe compares canonical query bytes and exact action/transaction coordinates; the observer role, source marker and explicit laboratory qualification marker are required. A stale first-attempt query cannot be substituted for a later retry query, even when transaction bytes match. Float/integer and boolean/integer substitutions in query coordinates rejected freshly. The current qualified observation settles the logical action and original hold while preserving every charged transport record and causal uncertainty.

retry_release requires an already released SIGNED action, no outstanding query, a fresh retry ID, exact latest ancestry and saved UNAVAILABLE reconciliation for that attempt. It rechecks ownership and validates the original signed bytes against the immutable template. Only a new successful commit returns those bytes. It does not invoke the signer, replace a transaction, reset released flags, rewrite the original action ordinal or create a new action. SIGNED recovery returns a reference with release=false. Known failure, terminal success, stale authorization and duplicate challenges cannot create another release.

Missing evidence and interrupted signing retain uncertainty. Query response loss keeps the outstanding query obligation; exact saved context can later be answered. A post-commit retry interruption leaves the retry charge, consumed slot and new query hold durable even if no bytes reached the caller. Another transmission needs a new reconciliation and explicit charged authorization. Local bookkeeping cannot prove external delivery, exactly-once execution or genuine chain outcome.

The six transaction kinds and both methods retain shared budgets. Finalize and ZK PROCEED reserve verifier resources per transmission. Early/final abandonment and cleanup are distinct actions; exhausted slots can stop their admission even with remaining attempt count. The branch guard and permanent owner checks remain. Fresh proceed/abandon competition produced one winner; retrying the winner could not authorize the competing action. A substituted owner blocked retry before charge or byte release. No prior A/B/C or F1 finding was reopened, and no regression of conditional nonce ownership was demonstrated.

## Fresh execution versus retained evidence

Fresh supplied main suite: nine groups, including both methods/all six kinds, exact-byte retries, first/retry failure deduplication, semantic FAILED, uncertainty, replay/races, independent resource exhaustion, actual shared-slot exhaustion and 16-extra-poll exhaustion. Its 11 actual process exits cover decision, sign claim/persistence, first release, retry commit and observation commit; pre-reopen journal cuts are preserved. Reopening retained committed charges/holds and rolled back uncommitted mutations at the tested cuts. This is process-exit evidence, not power-loss or hostile-storage durability.

Fresh independent checks: nine distinct completed groups (six in run02, three in run03). They cover eight signed observation substitutions; three callers competing for the last real retry slot; final-unit races at shared/stage attempt, shared/partition query and shared/partition verifier ceilings; query versus retry; nine authenticated context/ancestry substitutions; retry with the signer disabled and read-only signed recovery; owner substitution; outstanding-query reopening; and proceed/abandon competition for both methods. Boundary counter edits are explicit isolated synthetic fixtures, not claimed reachable lifetime histories. The slot race reaches its boundary through 14 real small retry transitions before competition.

The supplied current evidence totals 17 groups. All were inspected. Only its nine main groups were rerun; the five supplemental, two final-control and one signer-disabled supplied groups were reused as recorded evidence. The four saved n=4, 23-attempt/23-query completion paths were inspected, not repeated. Independently disabling the signer is a distinct fresh test. No actual-contract/Ubuntu lifecycle, native verifier, network transport, performance benchmark, 384,000-row boundary or full stream ran.

Preserved review harness failures:

1. /usr/bin/time was absent; exit 127 before candidate execution. Replaced with a timeout-bounded Python subprocess/resource runner.
2. Wildcard fixture import shadowed the harness BASE path. A missing-file failure occurred before a candidate transition. The corrected harness restores its own root after import.
3. Owner-substitution test correctly rejected with NONCE-NOT-OWNED; the harness incorrectly expected substring OWNER. Database/journal evidence preserves that rejection. Only the expected label was corrected; completed groups were not rerun. The failed group and two unfinished groups then passed.

No failed attempt was overwritten or hidden. Every command, exit code, elapsed time and process-memory observation is retained under evidence/. Main suite: about 4.33 seconds, child peak 24,320 KiB. Independent run02: about 0.82 seconds, child peak 23,728 KiB; continuation: about 0.42 seconds, child peak 22,784 KiB. These are current Python resource observations, not native-worker or operational performance measurements. No native worker was launched. Recovery-cut costs are within the recorded suite group time; no separate per-cut recovery-cost benchmark is claimed.

## Capacity derivation and limits

stages.py sets 512-byte chunks and local message ceilings 41,972 ordinary / 21,376 ZK, yielding append upper bounds ceil(length/512) = 82 / 42. These are this implementation's representation ceilings, not new protocol allowances.

For append count n, normal completion or post-finalization abandonment has D=n+4 first actions. The longest completed post-PROCEED-revert branch has D=n+5, including the failed first PROCEED. Its extra abandonment is not a retry. Latest Open abandonment has at most n+3 actions; semantic-failure and frozen prefixes are shorter.

Each unresolved first action needs one hold. With no previous failure, at most 15 retries can coexist with that hold: A <= n+4+15 = n+19. On the longer reverted branch, one consumed failure slot remains and a later action still needs a hold, so at most 14 retries can coexist: A <= n+5+14 = n+19. A terminal failure can consume the last hold but supplies no extra action or retry. A prefix that spends 15 retries on PROCEED then learns its revert can reach n+19 and freeze before abandonment; it does not complete a longer path.

Hence 101 / 61 are supported structural envelopes, not asserted maxima attainable by accepted maximum-size messages. Retry placement also matters: verifier-capable retries consume their reserved budget. As an arithmetic compatibility example, placing 15 retries on cleanup has base verifier cost 1 ordinary / 2 ZK; placing 14 on the reverted ZK PROCEED gives 16 total, within 18. Query counts can be one per attempt; extras consume their separate allowance. These compatible resource counts do not supply concrete maximum-message, provider, custody or operational evidence. The four saved small paths each have 23 attempts, 23 queries, 15 consumed slots and zero holds under synthetic outcomes.

Fresh arithmetic/byte inspection reproduced the saved component lengths 136,487 HEAD / 136,676 event, under unchanged 196,608 / 212,992 limits. That envelope deliberately combines incompatible maxima and is not an admitted state. The loose event sum 64+1+4*102+2*(102+16)+85=794 and blob sum 64+2+87+87+102+118=460 are consistent with this schema. The resulting 289,898,496 value-byte product excludes SQLite pages, indexes, journals, copies, request/response journal growth, physical workspace, lifetime multiplicity and external evidence. It is not a total capacity or storage assurance. The prior record-envelope derivation was inspected and reused, not a full new representation review.

## Remaining conditions and smallest next task

Shared ownership must cover every relevant signed/prospective writer on one complete protected ledger. Guarded APIs, unchanged code and a trusted runtime remain prerequisites. Raw SQL, omitted stores, copied databases, alternate signers and use of the public test secret bypass the laboratory boundary. Restoring both databases is not cryptographic rollback protection. Existing C2 in-flight-commit limitations remain. Namespace counters must ultimately bind the actual protected lifetime; fresh fixture namespaces never renew Pilot001 or project allowances.

LAB-ASSUMED-QUALIFIED and LAB-SYNTHETIC-NOT-FINALITY are explicit premises, not operational authentication, genuine appointments, provider truth or NEAR consensus finality. Decision B remains in force. Full-domain capacity, physical workspace, lifetime recovery, external-evidence bounds, operational custody, rollback resistance and qualification remain open. Retention and compaction remain unapproved. Existing signed sessions cannot migrate. Pilot001 is unchanged. The 43 inherited relationships and prior scoped A/B/C, F1 and nonce-ownership support are preserved; no full model/register correspondence is newly established. Changed stream identities remain UNCOMPUTED.

No candidate correction is required by this bounded review. The smallest next substantive task is an append-only, bounded model/register delta specification for the adopted Option A implementation: identify exact occurrences and ownership joins for first-attempt holds, disposition, immutable retry ancestry, one-shot release, query-headroom conversion, extra polling, verifier reservation and exhaustion/recovery; distinguish the actual lifetime ledger from isolated namespaces. Resolve the mapping and finite remaining input obligations before any large regeneration or further implementation. Route this recommendation through Engineering-Anchor[2]; this review neither authorizes that work nor changes canonical authority.
