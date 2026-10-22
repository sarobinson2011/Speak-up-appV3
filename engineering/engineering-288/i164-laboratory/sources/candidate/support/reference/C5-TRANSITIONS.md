# Proposed exact staged-authentication transition contract, version 1

Status: DESIGN PROPOSAL, NOT ADOPTED. Executable reference model only; no new Solidity registry, incremental SHA-512 implementation or live session exists. This does not replace accepted E/D/U, V2 evidence framing, EQ/MC or failure ORDER.

## Signed bytes, identity and authority

Propose a separately versioned authorization carrier, because the retained V1 carrier does not yet encode all required session/collector/network joins. Existing V1 signatures are not migrated or relabeled.

`M = ASCII("I164-ARCHITECTURE-A-AUTHORIZED-INPUTS-V2\n") || raw`.
The domain is exactly 41 bytes. `raw` is sorted-key, compact, ASCII-escaped canonical JSON followed by one LF, at most 1,048,576 bytes. Exactly three top-level keys: format=`I164-A-STAGED-AUTHORIZED-INPUTS-2`, bindings and authorized_values. Duplicate keys, noncanonical representations, unsupported types and trailing bytes reject. Maximum M remains **1,048,617 bytes**. This is an authorization engineering carrier, not canonical U and not the retained four-file V2 signed message.

Bindings are the exact keys in code/model.py KEYS, with the following representation:

- Digests: registry_code, auth_code, configuration, operation, inputs, profile, model, contract, program, appointment, public_key_hash, collector_inputs, collector_result, three_scopes, authorized_state, u, history_prefix: 32 bytes represented by 64 lowercase hex digits.
- Addresses: registry, auth_manager, actor, authorizer, executor: 20 bytes represented by 40 lowercase hex digits. These refer to candidate addresses only after real configuration evidence exists; fixtures use synthetic identifiers.
- network, epoch, expiry: canonical decimal uint64 strings, no leading zero. Network is the EVM chain ID; engine separately names the NEAR Engine account/network context. Expiry uses the governing chain timestamp convention, no local-clock substitution.
- method: exactly signPetition or signPetitionWithZKProof. phase: PRE-COMMITMENT.
- pilot, engine, issuer, decoder: nonempty canonical strings at most 256 characters, with exact register membership supplied by the owning profile. The complete encoded bindings object is at most 4,096 bytes.
- authorized_values: 1..19 lowercase even-length hex values, each at most 65,536 decoded bytes, total at most 524,288. Their ordered concrete types, projections and complete coverage come from the bound owning program and must validate before use. The transition tests use abstract synthetic byte values, not purported production typed records.

`operation` identifies the exact method/owning operation. `inputs` commits the complete canonical invocation, original actor/authorizer and arguments, not msg.sender-as-original-actor. `collector_inputs` and `collector_result` identify exact independently authenticated records, not untrusted PASS booleans. `three_scopes` identifies an ordered canonical descriptor of ROOT-ELIGIBLE, SCOPED-USED and NOT-APPLICABLE source/bundle/appointment joins. Those original evidence bytes and their existing authentication/qualification duties remain required; these references do not substitute for them.

`history_prefix` ends at the exact immutable intent and durable U retirement preceding begin. The later staging transcript extends history but is not recursively hashed into the message that authenticates its own session. `u` names the accepted U record by exact digest, not an invented substitute U. The retired U is associated with exactly one intent/session and cannot be reactivated.

Let A be exactly 32 key bytes and sig=R||S exactly 64 bytes. `message_id=SHA256(M)` is an identity commitment only. The proposed session ID is exactly:

`SHA256(ASCII("I164-STAGING-SESSION-1\0") || W(bindings) || message_id[32] || A[32] || sig[64] || uint64be(len(M)))`.

W emits the same canonical JSON+LF. Its escaped strings cannot contain a literal embedded LF, so the variable-length prefix is unambiguous; the remaining fields have fixed lengths. The message does not contain session_id or its own digest. This dependency graph is acyclic. Begin metadata must equal the parsed signed bindings, not merely share a caller label. A must hash to public_key_hash and match the appointed issuer key and scope/configuration records. Key authorization, source truth and qualification are independent of mathematical Ed25519 acceptance, including identity/small-order acceptance.

## Persistent state and original-message verification

OPEN state owns immutable bindings, message_id, total, A, sig, approved verifier/parser/code identities, next_offset, next_chunk_ordinal, SHA-512 eight chaining words, total hashed byte count, 0..127 pending bytes, canonical-parser continuation, authorized-value arena/index, deadline and terminal status. Only the contract's append transition may produce these states. No API imports caller-supplied chaining words, parser state, seals, counters or journals.

Initialize SHA-512 with raw R||A exactly once. Append M's actual bytes in order. Each append must be nonempty, start exactly at next_offset and contain exactly min(chunk_size, total−next_offset) bytes. Proposed chunk size is 512. No overlaps, gaps, alternate segmentation, extra bytes or silently accepted committed duplicates. Canonical parsing must be incremental and bounded across arbitrary token/block boundaries; unbounded string buffering is not permitted. It checks raw-to-begin equality and exact typed projections. The reference model stores bounded full bytes and uses the pinned native verifier, rather than claiming this new on-chain parser/hash path is implemented.

At maximum M: R||A||M is 1,048,681 bytes, 8,192 complete 128-byte blocks plus 105 bytes. Finalization adds SHA-512's 0x80/zero padding and 128-bit big-endian bit length once, completing block 8,193. It then applies the pinned reduction and canonical A/R/S, uncofactored equation rules. It does NOT verify a signature on message_id or an Ed25519ph digest. Premature finalization is not success. Mathematical failure is a terminal FAILED result where an ordinary nonreverting transition can commit it; out-of-gas/revert is reconciled by the durable executor, never assumed to preserve a contract write.

## Transitions

| Transition | Preconditions and atomic update | Outcome / accounting |
|---|---|---|
| prepare/retire | Existing normal collector prerequisites and immutable intent; retire U in durable executor before first stage submission | Retirement survives all contract rollback. Signature cannot establish qualification. |
| begin | Restricted executor, exact intended configuration/key/issuer, unique retired U/session, resource reservations and unexpired domain; create OPEN | One transport attempt; returned reconciliation is one query. Rejected pre-reservation request performs no governed action. |
| append | Restricted executor; exact domain, OPEN, next offset/ordinal and chunk length; one transaction updates hash/parser/value state and offset together | Revert leaves contract prefix unchanged. The attempted action remains charged externally. |
| finalize | Exact length, canonical parser at EOF, exact metadata and raw byte identity; verify original-message signature | AUTHENTICATED only, or FAILED. It never stores a live EQ/MC PASS. |
| release through either signing method | Same executor; same immutable session and exact invocation; original method guards; ZK verifier where applicable; current appointments/config/qualification; live comparison at owning cut | Consume once and signing writes/events are one atomic section. No external call after the final live comparison. No synthetic qualification may authorize real use. |
| reject/revert | Missing, invalid, unavailable or insufficiently qualified facts, inequality/materiality, stale context, original guard/verifier failure | No signing effect. Durable executor freezes the retired U; do not infer on-chain failed-U persistence from a revert. |
| abandon/expire | Authorized explicit abandonment or expired/incompatible configuration; no signing effect | Terminal tombstone; no U refund or session reuse. Cleanup is separately bounded and retains anti-replay identity. |
| cleanup | Terminal, finalized canonical state | May delete hash/parser/value workspace; retains session/U terminal tombstone, configuration/history linkage and accounting. Chain/calldata/history exposure is not erased. |

Unauthenticated direct calls cannot enter the trusted executor interface. Contract checks must independently enforce executor restriction on both registry methods and authentication-manager mutators. A hostile call cannot spend the project's off-chain allowance merely by sending arbitrary calldata. Such rejected adversarial traffic remains in the observer/resource model and is not falsely represented as a permitted project occurrence.

## Atomic comparison/effect integration

Both methods retain their respective existing checks; ordinary signing does not acquire an invented ZK check and its existing guards are not treated as admission. msg.sender is the executor, while original actor/authorizer is explicitly bound and separately authorized. For the ZK path, the verifier call and applicable guards occur before the cut. After any external calls, read/revalidate all required current state and configuration. Under a shared nonreentrant gate, execute the accepted live evaluator and the adopted exact-invocation/state materiality rule. Compare exact canonical typed values, required availability/status/coverage and history; do not replace them by a digest-equality shortcut. Consume the seal and commit the signing state/event immediately, with no intervening untrusted interaction.

Collector failure collection and its existing ORDER remain authoritative. Staging adds prerequisite failures to that collector; the reference model's Reject labels and illustrative failure list are NOT a new canonical admission order. Independently discoverable failures must still be collected. A value not observed because the cut was never reached remains unavailable. Test-only `qualified=True` is explicitly an assumption in a conditional design model that can return only conditional_effect with actual_admission=false; it is not an operational provider.

## Recovery and uncertainty

A lost connection never creates a new session/U. Freeze submissions until a charged, authenticated/finality-qualified reconciliation establishes exact network/account/code, transaction/request, session, ordinal, prefix and outcome. Canonical confirmed prefix N resumes at N; it never resets the hash or allowance. An exact signed-transaction rebroadcast may be proposed only while unresolved and within the retry cap; it must not create a new invocation or silently count as confirmed. A known semantic failure, failed release or abandonment cannot be retried with the retired U. A pre-reservation refusal performs no operation; a reserved attempt counts even if interrupted before action.

On-chain state is canonical only subject to the genuine network/finality trust assumptions. Fork/rollback uncertainty freezes the executor; local journals are not chain truth. Restoring a local backup cannot lower independently protected allowance/retirement anchors. If both authority and anchor are rolled back together, local MAC/checksum integrity cannot detect it: operational rollback resistance and key custody remain unestablished requirements. Internal repair may restore consistency without returning an observation; every externally returned reconciliation still needs its own pre-action charge and exact receipt coordinates.

The model serializes a bounded full-byte transcript protected by a local test MAC and separately supplied exact anchor/context. Restart reconstructs from those bytes (at most M+64 bytes per session), not a fabricated saved SHA-512 state. This models recovery invariants only. A production on-chain incremental implementation would resume its committed words/buffer directly, while independent off-chain audit reconstruction would reread the prefix. It must not inherit the native streaming verifier's unavailable state export by assumption.
