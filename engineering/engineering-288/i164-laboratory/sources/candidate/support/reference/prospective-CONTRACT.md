# Concrete prospective laboratory interface and state contract

Version: I164-PROSPECTIVE-LAB-1. Authority(path, config, create=True) creates a new isolated LAB namespace only; it refuses any existing schema. Reopening checks an implementation/configuration/principal binding. Historical job imports are not supported. The public fixture EVM key is 1; no caller can supply an EVM signing key through this interface.

## Identity and wire boundary

Every request has exactly version, binding, pilot, session, principal, challenge, expected, method, u, body. Ed25519 signs the version-separated canonical JSON+LF. Principal credentials are fixed public LAB-only fixtures; executor may perform ordinary methods, observer only observe. A supplied role cannot grant authority. Challenge is a unique 32-byte hex value. Binding includes configuration, authority.py bytes, retained anchor/stages/signed_eth/lab_evm bytes, and principal public keys. All imported code and Python remain trusted runtime assumptions; this digest is not process isolation or operational code attestation.

Request bytes must be canonical, with duplicate keys rejected. A response signs the exact request hash, challenge and success/error/data. Scheduler verifies server signature and request hash. No transport server or network call is present.

Authenticated requests are durably retained before action handling. BEGIN IMMEDIATE serializes journal count/check/insert at the unchanged 384,000-row cap. Duplicate challenge rejects. There is no deletion or compaction. Rejected requests can change journal storage; they do not change authoritative HEAD/counters/retirements. Replay does not return a reusable old release response. Request/response loss may leave a retained request with null response; it does not create a new attempt allowance.

## Exact unsigned representation

Expanded carrier I164-UNSIGNED-INTENT-LAB-1 keeps the historical semantic fields, exact ABI invocation, gas fields and conditional laboratory capsule but excludes signed_evm_hex. The new compact representation I164-UNSIGNED-COMPACT-LAB-1 retains identity plus the complete original calldata in canonical base64. It reconstructs arguments through the pinned ABI decoder and validates the original ABI, U and decision bindings. Both forms are new-version inputs; the original submitted bytes are stored immutably. No exact invocation bytes are replaced by a digest. Expanded input ceiling remains 262,144; compact form avoids forcing duplicate full calldata and expanded arguments into that ceiling. Signed historical carriers and supplied signatures reject.

RETIRE stores the exact unsigned intent, permanent retirement, and reservation hash(chain, executor, normal signing nonce). At most 64 U. Existing U and coordinate conflicts reject. OPEN allows only one lifetime active stage; exact history prefix, U, configuration, method, original invocation, manager and executor bindings are checked. Original-message Ed25519 authentication is verified mathematically with the supplied LAB key; appointed issuer/source truth/qualification are NOT inferred. Conditional staging values and ABI bounds are preserved.

## Methods

| Method | Preconditions / durable action |
|---|---|
| head | Authenticated read of current state, no service event. |
| retire | Exact new unsigned intent and U; permanent reservation and retirement. |
| open | One lifetime stage, exact staged message/key/signature and bindings; retains original message/meta blobs. |
| decide(kind) | Exact current head, no pending action, source-compatible manager/branch state; atomically charge and select the command. Kinds: begin, append, finalize, proceed, abandon, cleanup. |
| sign(action) | Only the current exact DECIDED action can enter SIGNING. After actual LAB signature validation, exact bytes and SIGNED phase commit atomically. Already SIGNED returns the same reference without release authority. SIGNING ambiguity refuses regeneration. |
| release(action, tx) | Exact selected action and persisted signature; SIGNED and not already released. Commit released=true before returning exact bytes. No raw-send callback, retry or production transport. |
| query(action) | Charge shared/partition query budget before fixture observation; one outstanding exact query coordinate. |
| observe | Observer-only exact action, signed transaction reference and query binding. Explicit synthetic manager outcome. UNAVAILABLE never advances nonce or clears pending. SUCCESS/REVERTED require nonce-consumed=true. |
| backup(id) | Fixed digest ID; charge existing snapshot partition and retain RETAINED-UNCERTAIN obligation. No callback or completion assertion. Duplicate refuses. |

There is no raw sign/template endpoint, arbitrary transaction import, restore, counter reset, state import, nonce-reassignment endpoint, resubmission endpoint or operational permit. Authority's Python helper methods and readable test keys are not a security boundary against an adversary controlling the interpreter/filesystem.

## Action authorization

The immutable action blob binds version, authority binding, pilot, session, staging sid, U, intent digest, permanent reservation, selected branch, kind, stage index, complete transaction template, originating decision-request hash and charged attempt ordinal. The template contains exact signer, chain, Ethereum nonce, target, calldata, value, gas limit and gas price. The action ID is the hash of these original bytes. The signer takes the action ID, not caller-supplied alternative transaction bytes.

Decision/charge/signing ordering:

1. In one SQLite BEGIN IMMEDIATE transaction, check current head, manager state, pending state, budget and source-defined next action; charge attempt (plus applicable verifier reservation), permanently choose branch when needed, and persist DECIDED plus the exact action blob/event.
2. A later authenticated sign request atomically changes DECIDED to SIGNING. Competing claims cannot both claim the action.
3. Only then call the public-key-1 laboratory signing primitive. Validate its decoded signature against every template field and the existing 75,088-byte transaction cap.
4. In another transaction, require the same action and SIGNING phase; retain exact signed bytes and SIGNED event together. No bytes are returned before this commit.
5. Release is separately recorded once before its response can expose exact bytes.

A signature-computation failure or interruption after step 2 leaves SIGNING. The implementation deliberately offers no inference that no signature exists and no competing-action authorization. After step 4 an interrupted response can recover the same signature reference/bytes from protected storage; it grants no fresh release. An interrupted release response leaves released=true. This is fail-closed safety, not unconditional progress.

## Branches and manager states

b=start_nonce; n=ceil(message_length/512). Normal path: begin b, append b+1..b+n, finalize b+n+1, proceed b+n+2, cleanup b+n+3. A reconciled Open boundary uses next q for abandon and q+1 for cleanup. After finalization, abandon uses b+n+2 and cleanup b+n+3. The prospective intent fixes the normal signing nonce and approved branch policy; current signed sessions do not inherit this permission.

ABANDON sets the irreversible branch before signing its management transaction and forbids proceed forever. PROCEED immediately changes petition status to UNCERTAIN and charges before signing. Pending actions block another decision. A synthetic definite nonce-consumed petition revert leaves REVERTED and allows abandonment at the next nonce, followed by cleanup; proceed never becomes available again. A successful petition effect is represented CONSUMED and can only clean up, never be relabeled non-execution.

Manager SUCCESS observation for append/finalize may report FAILED for a nonreverting semantic failure; this preserves retirement and permits cleanup only. Other failed management transactions remain FAILED-FROZEN pending: no guessed replacement, nonce gap repair or cancellation. Manager UNUSED cannot be abandoned. Abandoned/Failed/Consumed permit cleanup, not another signing attempt. All pending backup markers survive terminal changes and reopening.

Evidence in this interface is deliberately synthetic. The observer binds manager state and nonce consumption to the exact signed action/query, but no actual receipt/log/finality acquisition is implemented. The recorded manager states are conditional fixture assertions, not measured chain truth. Genuine C4 evidence integration and expiry/configuration assurance remain separate requirements.

## Persistence and refusal

HEAD canonical bytes bind the latest immutable event; load compares canonical byte encodings of after versus HEAD-without-head, retaining the F1 type distinction. Each event hashes its predecessor and contains the complete next aggregate state, exact request hash and any result reference. Original authenticated requests remain in journal, original actions/transactions/intents/results in immutable blobs. No history is deleted. SQLite transaction rollback leaves HEAD/events/blobs unchanged on ordinary rejection. Crash testing does not establish resistance to an administrator restoring the entire database.
