# Exact actual reconciliation blockers

Owner: canonical SU-Engineering register/profile custodian under Steve, coordinated by Engineering-Anchor[2]. No external request has been sent.

Required missing input:

1. An authoritative statement identifying the exact current baseline and current delta HEAD, with the canonical record establishing its authority and a completeness statement covering intervening changes.
2. Exact current register/schema/source-form/dependency/custody metadata and the associated expanded-contract, relation-rule, profile, candidate-identity and ledger-binding metadata; exact path/size/hash manifest and source bytes referenced by class declarations. Existing large model/stream objects may remain referenced by retained exact identities.
3. Every intervening delta in order, with predecessor/base/context bindings and exact contents. No claim that a historical package has no successors can be inferred from its contents.
4. Current authoritative binding of the two known inherited context identities. Their historical names are established; their current profile association is not.

The new reconciliation transport contract is defined by reconcile_baseline.py: baseline/manifest.json, baseline members, deltas/000001/manifest.json onward, and a separately pinned I164-CANONICAL-INPUT-PIN-1 statement. It is a local interchange contract, not a newly adopted canonical record format. An owner must provide a byte-preserving, traceable mapping from native artifacts into it, or a subsequent explicit adapter must be added. Existing native artifacts must not be silently rewritten into the fixture format. JSON and TSV custody bytes are accepted as exactly manifested metadata; this tool does not infer their classifications.

`authority_record_sha256` must resolve to a genuine canonical record outside the fixture. The program checks its exact agreement but cannot establish its authority. A user-set true flag is not a substitute. Missing classifications remain missing even when the canonical baseline is pinned.

Other blockers preserved: qualified dependency/visibility/seven-role custody and observer views; actual owning phases, producers, scoped appointments and assessments; operational exclusive key control, full same-account writer coverage, protected ledger/anchor/lifetime scope and rollback resistance; finite lifetime acquisition/recovery/diagnostic directory and retained-storage accounting; genuine external outcome/finality/source serialization evidence. Responsible roles remain the source producers, executor/signer/storage owners and appropriately appointed assessors identified in the prior canonical-binding brief. General project approval cannot supply these technical or qualification facts.

Unfinished implementation after this slice: full two-context expansion, old/new dependency/equality/actor reachability closure, positive consistent model/profile/procedure/register/ledger binding, and separately authorized stream construction/validation. No local test in this package claims their completion.
