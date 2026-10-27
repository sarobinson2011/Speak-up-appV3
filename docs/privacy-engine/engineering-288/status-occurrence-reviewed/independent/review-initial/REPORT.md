# Independent review — I164-status-smoke-occurrence-connection-1.zip

**Scoped verdict: NOT SUPPORTED for closure as submitted.** The original saved receipt is consistent with the bounded capture, but the new public validator exposes mutable context authority (SOC-01). Separate source/observer semantic checks also have demonstrated gaps (SOC-02). These findings concern the new occurrence connection, not the previously supported status-boundary implementation or a rerun of the host smoke.

Review author: **Formal-Lab[6] (Codex, independent reviewer)**. Construction author: **SU-Engineering[288D]**. Date: 26 October 2026. The reviewer did not author the implementation and made no implementation changes.

## Target reconciliation and integrity

The target is **I164-status-smoke-occurrence-connection-1.zip**, supplied locally with the duplicate-download suffix `(1)`. Its exact identity is:

- **8,512,513 bytes; 485 entries**.
- SHA-256 **20be027e282cf14a2dd1c790b60b788abab585a554152096e80ab29b5e1034f3**.
- CRC, unique safe regular-file membership, exact flat-manifest membership and **484 member hashes: PASS**.

The exact bytes are available. There is no missing-input blocker. The earlier **4,494,310-byte**, SHA-256 `3ef0c2943582101f58646503482d20e28da17e3ccfefcdd4cef03714d6d2c517` archive is the completed boundary review; it was verified and reused as predecessor support, not treated as this review target.

The two embedded dependency archives also pass CRC, safe exact membership and manifests:

| Dependency | Verified identity | Preservation |
|---|---|---|
| `inputs/correction.zip` | 4,269,431 bytes; 463 entries; SHA-256 `983e8aa849be387c4f92a54953fd24e2271bb090a01a0fb589230f0edad53185` | Identical to the input embedded in the completed independent boundary review; every one of the 463 `retained/correction/` members matches |
| `inputs/smoke.zip` | 77,696 bytes; 37 entries; SHA-256 `bbea8f904a91b5c13b4b79653b702154352c68471f0ed8e51035cdf27becc6e8` | All 36 manifest member identities pass; saved review report/checkpoint match the prior review |

The new adapter is `code/smoke_occurrences.py`, 22,323 bytes, SHA-256 `c2668ed97ef3b08ba7ef24184dcc6c2940affd322fb56c236bc5d65291dd7cd0`. The saved receipt is 103,441 bytes, SHA-256 `1d4e8f19ead8096f3fef97fc70048661b0021af4f1a7c3d95fdb01cf665d0830`.

The full recovered correction root is required and present. Recovery of this connection is self-contained for offline validation; it needs no host session or database connection. Predecessor support for the 666 candidate members, 163 draft members, historical identities/relationships/ordinals and runtime source composition is reused through exact correction equality. Those completed component reviews were not repeated.

## SOC-01 — returned contexts mutate validation authority

**This is a public validation defect with unchanged implementation and evidence bytes.** `validate` returns the module's actual `CONTEXTS` list (`code/smoke_occurrences.py:205–206`). `derive` later iterates that same mutable list (`:189`). The original list is declared at `:13`.

Smallest concrete witness, after loading the unchanged module as `m`:

```python
answer = m.validate(root, original_receipt)
answer["contexts"].clear()
changed = json.loads(original_receipt)
changed["contexts"] = []
m.validate(root, m.enc(changed))  # returns PASS with contexts=[]
```

The resulting zero-context receipt is **1,718 bytes**, SHA-256 `e7832c0e45f17d84b61a9f105b84cab665ab2dcf0f4f3b20e7b6e52d2a492818`. All input archives, source files, evidence and obligations remain unchanged. Nevertheless both required context views, all their occurrences and duty links are absent from an accepted receipt. The untouched original receipt now rejects with `OCCURRENCE-RECEIPT-MISMATCH`.

Independent adjacent variants reproduced acceptance after removing one context, reversing their order and duplicating the first context. Each alteration also causes subsequent pristine validation to reject in that same module. A fresh unaffected module still accepts the original. Both normal-root and recovered-root fresh processes reproduced the defect. No private-attribute introspection or arbitrary code replacement is needed; the writable alias is an ordinary returned result.

This alone prevents closure. The minimum correction is to preserve source-owned context membership/order independently of returned containers, while returning detached values. It must prevent missing, duplicate and reordered contexts from becoming new expectations and leave repeated pristine validation unaffected. No new host evidence is needed to demonstrate that correction.

## SOC-02 — source/observer-inconsistent claims pass the semantic seam

The review request explicitly distinguishes semantic rejection from the whole-archive pin. The internal `semantic(ctx, evidence)` seam was therefore tested with altered in-memory evidence, while retaining the pinned source and all other records. **These are not public archive-pin bypasses:** public `validate` rejects the resulting changed receipts against the original pinned smoke. The original capture is not shown to contain these defects.

The following source/observer contradictions nevertheless pass `semantic`, and `derive` produces corresponding output:

| Witness | Observed result | Source basis for rejection |
|---|---|---|
| Managed constructor return snapshot `_epoch: 0` → `17` | Accepted; `managed-local:epoch` becomes 17 in that invocation's output | Pinned `ManagedAuthority.__init__` sets `_epoch=0` and has no later assignment before its normal return; the following recorded recovery call still has epoch 0 |
| Reattribute the top `main` call/return to the old launcher, changing their path and compatible source lines to 188/194 | Accepted and source-bound to the historical status-printing main | The pinned observer's launcher watch set excludes `main`; only the prospective entry's main is watched. The old main does not call the new `run` chain or return integer zero |
| Prospective main return value `0` → `false` | Accepted | Its successful source return is integer `0`; `semantic:119` uses Python `== 0`, which also accepts `False` |
| Add `{"_phase":"READY","_epoch":99}` as the main return's `state` | Accepted and published as observed local values | The pinned observer's `snapshot` returns None when no `self` local exists; prospective main has no such local |
| Generator resume flag `true` → integer `1` | Accepted | The pinned observer computes this field as a Boolean; truthiness alone is not exact source correspondence |

The constructor epoch is a one-value witness. The source-attribution witness changes four trace fields and demonstrates why compatible function names/line-opcode pairs do not by themselves establish the recorded producer. All variants are preserved, including altered traces, derived receipts and public rejection observations. They reproduced against both roots.

These checks concern facts available from the actual pinned producer/observer and recorded fields. They do **not** require invented bytecode offsets, argument snapshots, missing frames, or full execution-path reconstruction. Tightening those available source/type constraints is the bounded next repair; sparse observations must still retain their genuine limits. This finding should not be described as resistance to a forged observer or as proof of complete trace semantics.

## What the unchanged original receipt does establish

The original receipt passes public validation in fresh processes against both exact roots. Independent examination of the saved trace found **40 events** comprising **18 distinct completed traced invocations**, plus two generator suspensions and their two resumptions. Suspended/resumed `_session` and `session` frames remain the same invocation identities.

The source sequence covers prospective `main → run → _run`, the retained `session/_session`, raw Authority construction/close, managed opening/construction/recovery/validation, two status calls, client construction/handoff, managed close and backend close. The two equal-valued status returns have distinct frames **13 and 14** and different owning parents. Raw creation and managed reopening remain distinct Authority invocation frames **6 and 11**. Normal completion is correlated with the saved source line/opcode and recorded successful disposition; it is not full instruction-path proof.

The observer source `preparation/worker.py:check_handoff` contains exactly one explicit `cap.state()` call. Its saved handoff record is separate because the observer does not recursively trace that call. Each context view correctly represents it as `explicit-observer-call`, with `frame=None`, `parent_frame=None`, exact observer/source/artifact bindings and association with handoff frame **16**. No synthetic Client.state frame or internal state/ingest frames were added. `handle` is an observed available method, **not an invoked method** in this smoke. No request or response was manufactured for the empty journal.

Both original context views contain **18 traced rows plus one observer-call row**, with exact acquisition-qualified IDs, source hashes, call/completion pointers and parent frame references. They are two symbolic views of the same capture, not 38 executions, doubled storage or independent allowances. The fixture workspace, binding, ownership incarnation and managed-constructor reference distinguish it from either earlier acquisition; a reused configuration session label is not treated as shared invocation identity.

Each view retains five exact inherited requirement/duty/producer/directory joins: `managed:entry`, `managed:normal`, `managed:restored`, `managed:close-confirmed` and `managed:obligation-preservation`. Local declarations and the HEAD/CONFIG/OWNERSHIP-META record declarations match the governing basis. The joins are relevance/preservation links, not proof that every invocation directly establishes every requirement. In particular, raw-close and callback/source associations must not discharge managed recovery/close/dispatch obligations. All duty dispositions remain **NOT-ESTABLISHED**, classifications **UNKNOWN**, ranges/counts unallocated; the inherited twelve preservation labels are not a renumbering of O01–O11.

Four exact retained-copy relationships are represented without adding invocations. Existing declaration labels/classifications are preserved instead of rewriting historical records as new execution evidence. Fixed stdout is derived from the prospective main source and compared with saved bytes; stderr is empty, the saved process reports success, and the close event/retained file identities agree. Selected database files were hashed only as bytes. Lock reacquisition, absence of sidecars/failure markers, host environment and execution remain **saved observer assertions**, not fresh observations by this review or independent storage/custody proofs.

## Validator reuse and limits

The adapter calls the existing exact source-correspondence validator and reuses `managed_observations.fixed_status` for the recorded phase/epoch/constants and recovery-child status relation. The added reason check compares against the recorded reason snapshot. The older full occurrence validator expects a different layout with offsets, line events, arguments and before/after authenticated exports. Manufacturing that layout would manufacture evidence; it is correctly not invoked here. Neither export ingestion nor model construction is rerun. Existing model/duty/source artifacts are authenticated and joined; this is not complete-model or canonical-ledger verification.

The sparse capture still lacks bytecode offsets, argument snapshots, full exception propagation and live/retired snapshots. Matching a return opcode at a source line is only compatibility evidence. No generalized exceptional-path, signed-request, transaction, service, lifecycle, complete lifetime-domain or privacy qualification follows. Historical launcher-frame gaps remain historical gaps. Trusted-observer and stable-filesystem premises, exclusive ownership, custody and real-storage durability remain unresolved to their existing scopes.

## Evidence separation and test record

Engineering's supplied **57 assertions and two process checks** were inspected separately; none was rerun. Their saved result contains 59 labeled passes, including the fresh/recovered process checks. The development source/empty-output failure for permission-only ZIP type bits remains present. The first packaging omission of nested manifests is documented, but its failed ZIP is not supplied; it remains an unavailable author-workspace artifact. The delivered package does retain all nested manifests and all 463 correction members.

Fresh independent review performed **84 assertions**, including explicit reproduction of **nine witness variants**: four SOC-01 variants and five SOC-02 variants. The same assertions/witnesses reproduced in a separate fresh process against the recovered root; repetitions are not additional semantic coverage. These counts mean review checks completed, not that all candidate behavior passed. A further **10 process checks** passed: two legitimate public validations and eight recovery/input negatives, each negative exercising both load and validation. Actual undeclared file, empty directory, FIFO and symlink cases, missing nested manifest, stale decision and altered/mixed archives rejected before executing a retained validator module. No socket/device execution claim was added.

An initial reviewer archive-inspection command assumed a wrapped manifest and stopped with `KeyError: members` after size/hash/CRC/path checks. The actual manifest is a flat map. The assumption was corrected before extraction or application execution, all 484 entries were then verified, and the reviewer failure is preserved separately. It is not a candidate defect.

Review environment: CPython **3.12.14**, optimization disabled, `-I -B`; installed Cryptography metadata **50.0.2**. Tests were offline evidence/source/receipt checks, not stubs executing the application. Audit/profile guards prohibited database/network operations, existing Steve-host paths, and execution of the worker, launcher, Authority or managed runtime. The saved host's 50.0.2 environment is retained evidence; this review does not authenticate installed host wheels or establish 41.0.7 compatibility. No boundary review, host smoke, session operation, pipeline, lifecycle or Git save was rerun.

## Disposition

Return this checkpoint to **Engineering-Anchor[2]** for the bounded SOC-01 correction and disposition/correction of SOC-02's available-source checks. Reuse this saved smoke and predecessor support. No new host execution is needed for these findings, and no implementation or policy change is performed by this review.

All eleven obligations, four UNKNOWN inventory totals, fourteen UNKNOWN lifetime totals, Decision B, existing allowances/reservations/retention and earlier acquisition identities remain preserved. Cumulative-envelope remains unadopted; SOURCE-ONLY unchanged; readiness/final binding BLOCKED; backup KERNEL-ONLY; streams UNCOMPUTED; admission disabled. The findings do not reopen the accepted definition or withdraw the prior scoped status-boundary support.
