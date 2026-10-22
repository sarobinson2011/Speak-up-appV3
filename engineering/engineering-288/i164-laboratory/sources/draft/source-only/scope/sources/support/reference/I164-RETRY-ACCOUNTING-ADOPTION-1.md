# I164 prospective pilot — accounting adoption

Record: I164-RETRY-ACCOUNTING-ADOPTION-1
Authority: Steve, explicit approval in SU-Engineering[288C], 2026-10-16.
Canonical route: SU-Engineering; return to Engineering-Anchor[2]. STATE.md and SU-Engineering remain canonical. This is an append-only prospective pilot decision record, not a claim to have edited the repository STATE.md or completed model/register integration.

## Exact adopted basis

Steve approved option A and the complete proposed clarification in DECISION.md of Engineering-288C-I164-retry-accounting.zip (46,264,582 bytes; SHA-256 94054453064f337ebe67716d82548e4bfe7bb5ecea69a56d5753aa76e969283d). Its historical proposal and analysis remain unchanged. This later record resolves their pending A/B choice for prospective new-version laboratory sessions only.

DECISION.md SHA-256: d426532c078ee4575553e2c72579d2a4f1203810addd7e9cdac06c97eea164d3
RETRY-SPEC.md SHA-256: 3e566de62f6efa24222a1ca226a096893d6b6f110f2e34d12bb904c700ac181a

## Adopted clarification — exact quoted text

> For prospective new-version laboratory sessions, clarify the adopted shared 16 retry/failed-attempt slots as follows. A distinct durably charged transaction attempt consumes at most one such slot if it is an explicitly authorized exact-byte rebroadcast, or if qualified reconciliation establishes that its first submission failed. A charged retry that is later found failed does not consume a second slot. A first-attempt failure includes a definite transaction revert and a committed semantic FAILED result of the governed action, even when the outer transaction succeeded. Missing evidence, timeout, interrupted signing and unavailable outcomes remain unresolved; none is classified as failure merely to settle accounting. Pre-reservation refusal, read-only recovery, polling and off-chain backup failure are not transaction-retry debits; they retain their own applicable accounting.
>
> The transaction-attempt charge is permanent and independent of this classification. Before authorizing any possible transmission, a future implementation must atomically secure the attempt charge, applicable query/verifier obligations and sufficient shared-slot headroom for its possible failure/retry classification. It may retain conservative holds and freeze when safe accounting cannot be established. Releasing an unused contingency hold after qualified success must not refund a charged attempt, erase a consumed retry slot, reset allowances or delete evidence. Ambiguous outcomes keep their protection. Do not authorize transmission on an assumption that a future failure can be charged after the shared pool is exhausted.
>
> Apply this clarification to both signing methods and every governed prospective transaction kind. Known failed actions and terminal abandonment do not acquire resubmission rights. The approved post-revert abandonment and cleanup remain distinct actions, each requiring its own existing resources; exhaustion still stops before action. Keep the local 102-attempt cap, all shared limits, permanent U retirement, exact intents, nonce ownership, immutable evidence and uncertainty unchanged. Existing signed sessions cannot migrate. This approves an accounting clarification only; retry implementation and execution still require their own bounded instruction. It does not assert that a complete 102-attempt or 62-attempt path is attainable or that operational evidence/custody exists.

## RETRY-SPEC provisions now resolved

- The policy parameter in Atomic admission and one-shot release, steps 1–2, is option A: inclusive, once-only shared-slot classification plus atomic pre-action headroom protection.
- The Counter and observation contract selects its choice-A contingent reservation and qualified-disposition branch. Choice B is not adopted. An authorized retry subsequently established failed consumes no second shared slot.
- The missing shared failure-slot classification in Current gaps now has an approved rule. Its implementation, durable attempt ancestry, authenticated retry route, one-shot authorization, query classification and verification remain outstanding.
- Unknown outcomes retain protection; actual attempt charges and consumed slots are never refunded. Only an unused contingency hold may be released after qualified success, without deleting evidence or renewing allowances. Known failure creates no resubmission right. Abandonment and cleanup retain their separate resource requirements.

## Concrete bounded task ready for separate authorization

Implement the approved option-A contract in the prospective laboratory authority only: durable per-attempt failure-slot holds and once-only dispositions; authenticated exact-byte retry_release and scheduler route for eligible unresolved transactions; atomic attempt/query-headroom/verifier/slot reservation; immutable transport-attempt ancestry; one-shot release and restart recovery; explicit reconciliation versus extra-poll accounting. Cover ordinary and ZK methods and all affected transaction kinds while preserving permanent nonce ownership and the existing signing boundary. No new signature, replacement transaction or reset may implement retransmission.

Use focused offline fixtures for first-attempt failure, retry-then-failure deduplication, qualified success and unused-hold disposition, unresolved protection, exhaustion, exact bytes, known-terminal refusal, replay/concurrency and interruption/reopening. Recompute affected record/event/resource bounds within unchanged limits; identify model/register consequences and return one implementation checkpoint to Engineering-Anchor[2] before focused review. These are the next task's intended contents, not authorization to execute it now.

## Preserved limits and status

This approval is accounting clarification only: no retry implementation or execution is authorized. No code changed and no completed tests were repeated for this record. Keep the 102-attempt cap, shared16-slot limit and all other adopted limits unchanged. Existing signed sessions cannot migrate. Permanent U retirement, immutable intents, nonce ownership, exact evidence, prior nonce-review support, A/B/C support, F1 closure, all90 historical candidate files, accepted semantics,43 inherited relationships and Pilot001 remain preserved.

Full retry coverage and capacity remain unestablished. Shared-ledger coverage remains conditional. External-outcome Decision B remains in force; retention/compaction remain unapproved. Custody, rollback resistance, genuine external evidence, physical/lifetime capacity, model/register integration and qualification remain open. Changed stream identities remain UNCOMPUTED. Actual admission remains disabled.
