# Source-determined prospective retry specification and implementation gaps

Status: analysis/specification only. No endpoint or schema below is implemented or authorized for execution here. The slot-policy parameter in DECISION.md must be settled before completeness can be claimed. Existing signed sessions and historical files are unchanged.

## Permitted capability to implement, not an automatic entitlement

S2 permits an explicit proposal to rebroadcast the exact signed transaction only while unresolved and within retry capacity. It does not require an automatic retry, promise a successful retry, or authorize replacing a failed invocation. Complete prospective coverage of that permitted recovery domain would need the following guarded operation. It cannot be implemented by calling DECIDE again, clearing pending, re-signing, or resetting released=false.

Candidate request shape: authenticated `retry_release`, with exact current authority binding, pilot/session/U, expected HEAD, fresh challenge, immutable action ID, signed-byte reference, prior transport-attempt reference, and a unique retry request ID. The normal wire identity/role checks remain. The retry request selects no alternate nonce, template, branch, gas price, calldata or signer. It produces a new **transport-attempt authorization**, not a new immutable action or transaction.

Eligible state must have recoverable, validated persisted signed bytes and unresolved execution, with a prior release that may already have exposed those bytes. An initial SIGNED-but-unreleased action uses its existing first-release path, not a manufactured retry charge. DECIDED/SIGNING without safely persisted bytes is ineligible. No terminal SUCCESS, known REVERTED/FAILED outcome or reconciled abandonment may be retried as the old action. Pending ordinary begin/append/finalize, PROCEED, abandon and cleanup can be considered only under that same unresolved exact-byte rule; neither the ABANDON branch flag nor pending cleanup authorizes another petition. Once terminal abandonment is known, only already permitted cleanup remains, not another abandonment invocation.

## Atomic admission and one-shot release

1. After a lost connection, require the source-prescribed charged, authenticated reconciliation of the exact context before a new transmission proposal; a timeout alone grants no retry. Evidence may still leave execution unresolved, and must not be promoted to non-execution. Validate authenticated caller, exact state/action/transaction/context joins, unresolved eligibility and permanent ownership of the same chain/executor/nonce. Current retired U, intent and branch remain immutable. Consult the chosen shared-slot classification and all independent existing limits; do not use a new namespace or ledger as renewed headroom.
2. In one protected commit, charge shared and stage attempt counts, debit/reserve the selected policy's exceptional slot, reserve query headroom without treating an unperformed query as an observation, conservatively reserve verifier cost if the exact command is finalize or ZK PROCEED, and persist a new transport-attempt record. Bind it to the original action, exact bytes, prior attempt, charge ordinal, parent history and one-shot release authorization. Keep the original action's attempt_ordinal unchanged; append the new attempt relation rather than rewriting history.
3. Only a fresh successful commit may expose those same stored bytes or invoke a future approved transport. A recovered receipt is evidence, not a reusable callback capability. Concurrent proposals use current-head CAS and exact prior-attempt coordinates, so only one fresh authorization wins. A stale request or replay cannot emit bytes again or charge again as a hidden retry.
4. A crash after charge but before release remains a spent unresolved attempt. A crash after possible exposure never proves non-execution. Reopen the same durable records and ledger; do not regenerate signatures. Another explicit retry requires another independent charge and eligibility check. No scheduler loop may retry automatically.
5. A charged reconciliation must identify the logical transaction and relevant transport-attempt chain, not pretend a receipt identifies which identical-byte transmission caused inclusion. Record causal ambiguity honestly. Reconciliation may settle the transaction while preserving every prior charged transmission. Known terminal failure closes retry of that action; it does not reset U or ownership.

## Counter and observation contract

The same 2070 shared / 102 stage ceilings continue to apply to both first decisions and retransmission authorizations. The shared 16 classification must use a durable once-only key per charged attempt, not one counter per transaction kind. Every extra verifier-capable transmission must reserve the relevant shared64/staging18 cost conservatively, consistent with the retained finalization retry implementation. No second signature computation is needed merely to retransmit.

Before an external observation, charge a query and bind it to its exact request/attempt/evidence coordinate. Model one reconciliation per attempt and the source's 16 extra polls explicitly; merely staying below 2086 does not establish the intended schedule. Query/result loss and UNAVAILABLE must leave evidence and uncertainty intact. Do not copy the historical result=None restriction in a way that forbids all valid recovery after an unavailable observation, and do not clear evidence to make a retry eligible.

For choice A, add explicit contingent failure-slot reservations before possible exposure of a first attempt, durable disposition after qualified success/failure, and no double counting of a retry later found failed. With an exhausted pool, safe future failure accounting may be unavailable even when total attempts are below102; freeze before action. For choice B, debit shared slots only for additional-transmission authorization, while permanently retaining all initial failure attempt charges. These branches are alternatives, not simultaneous accounting rules. The precise policy cannot be encoded until Steve chooses.

Snapshot markers/callbacks retain their independent 130/85 limits and stable logical request identity. A failed/repeated backup must not be mislabeled a transaction retry, and a repeated observation must not be a free internal repair. No retention amendment follows from the new record types.

## Current gaps and boundaries

| Gap | Evidence | Required work after policy decision |
|---|---|---|
| No prospective retry method / scheduler route | authority.py methods and Scheduler; retries stays zero | Add explicit authenticated operation and transport-attempt record, not another DECIDE/sign. |
| No shared failure-slot classification | charge/observe only change existing totals/results | Implement selected once-only membership/hold contract; retain every disposition. |
| Single pending action/query is not a transport-attempt chain | current pending and immutable action schema | Add exact retry ancestry and query-to-attempt mapping without mutating action bytes. |
| One-shot release cannot be replayed for retry | release checks not released | New charged capability; no flag reset. |
| Extra polling classification not separately represented | query only checks shared/partition caps | Account first reconciliation versus extra polling under adopted schedule. |
| Existing historical STAGE_RETRY is narrower and no petition retry endpoint | stages.py / sole_service.py | Do not import this capability or migrate signed sessions; use it only as retained engineering evidence. |
| Operational outcome/custody/rollback prerequisites absent | prior reviews and Decision B | Remain separate prerequisites; no synthetic evidence substitution. |

Future focused checks should cover every eligible unresolved kind, both methods' verifier costs, known-terminal refusal, exact-byte identity, same owner, duplicate/stale/concurrent retries, post-charge loss, repeated reopening, first-failure versus retry-failure deduplication, contingency exhaustion and query classification. They must distinguish read-only recovery from new release. These are specified checks, **not executed checks in this slice**.

## Capacity / model consequences, not a new proof

Exact-byte retransmission adds no Ethereum coordinate and no new signature bytes, but adds charged transport-attempt, release-authorization, request, receipt, observation and classification/hold occurrences. Existing permanent branch-union ownership still applies. The current reviewed 4,730 event bound applies to the current no-retry schema; do not extend it to new hold/retry/disposition events without deriving their exact counts. HEAD and event byte envelopes must be recomputed for any added counter/record fields. Records must preserve exact original bytes; hashes alone do not replace required evidence.

The current 384000 journal-row cap remains fail-closed. Retries/recovery do not give a fresh journal or compaction entitlement. Lifetime multiplicity, physical workspace, external evidence representation, full model/register binding and qualification remain unresolved; changed stream identities are UNCOMPUTED. This specification does not change code identity or supply an implementation approval.
