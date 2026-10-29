# Bounded internal status forwarding

The declaration producer and mandatory correspondence validator now bind the typed direct-return chain ManagedAuthority.status -> ManagedSession.status -> _Control.status in both symbolic contexts. Current exact results/counts are in RESULTS.json. The new extension is ready for independent review, not independently closed or operationally qualified.

## Source and guards

The defining live_connection.py is 5,717 bytes / 7344170ca01a2dbbd3afbeb4a6a55c0b95db0edb1a8d74e4fa4638b6dcfc6da5. Its lines 23-24 construct the six-field result under the instance lock. The existing reviewed status producer supplies exact selectors, types, literals, assignment origins, guards, exception-derived reason expressions and recovery embedding. No arbitrary reason length or epoch/lifetime cap is introduced.

lab_bootstrap.py is 11,481 bytes / 245d4f36d687834aeee064a60d4414b15f7b8babfdb5dec192aa995d93af2b78. ManagedSession.status at line 122 directly returns self.__managed.status(), without arguments, copying or a catch. prospective_entry.py is 9,485 bytes / a1d80c523ae220228a6b27cac42b5e57a006336e858a8e7db0a75355d6cf2ae9. _Control.__init__ stores its token at 130-131; status at 132-136 looks up _OWNERS, invokes the existing _fail when owner is None, and otherwise directly returns owner.wrapper.status(). Its source does not test owner.failure, phase or readiness. _run supplies the token/owner/control callback under the existing explicit control condition and revokes the token in finally. run_controlled remains the designated trusted integration route, not caller authentication.

The producer independently parses exact forwarding/constructor/helper shapes, source locations, normal prefixes, the control-call condition, token storage and revocation. It retains the existing boundary sites/contract/adoption and rederives the manager-field catalogue from its defining source. Required hops and field coverage do not come from submitted declarations. Stale/coordinated source-catalogue substitutions cannot replace those expectations.

The successful manager result is a newly constructed dictionary. Both forwarding methods return that same result reference. The model records this source-established relationship through scoped symbolic references and exact field values/types. It does not claim observed physical object identity, even when recorded values match. There is no _data conversion, deepcopy, new serializer, automatic logging, public status method or output destination.

All six source-written phases are available to conditional status-value cases: CLOSED, READY, QUARANTINED, CLEANUP_UNCERTAIN, OPEN_FAILED and VALIDATION_FAILED. This does not establish that every combination of phase, reason, epoch and integration history is reachable. The epoch constraint is derived only from the constructor's initial integer and positive source increments; it remains instance-local, with no upper bound or global identity meaning. Constructed snapshots/outcomes are explicit premises, not proofs of assignment execution, complete history, resource feasibility or later call timing.

## Evidence and executable connection

The current public path is validate -> derive -> derive_status -> _checked. It reloads exact inputs, invokes the reviewed predecessor derive_client_state, compares its saved serialization and rebuilds current expectations. The same validated evidence supplies the acquired instance, ownership incarnation, constructor frame, recovery frontier, HEAD/configuration/reference bindings and the actual saved manager-status samples. A mutually consistent set of replacement reports cannot supply another authority.

Both ordered contexts must contain internal_status_return_correspondence. Its return templates bind the source-defined fields, arguments, owner/token/session/manager relationships, designated internal destination and instance/invocation scope. Saved manager return samples remain separate records with exact trace identities and pointers. They do not become ManagedSession.status or _Control.status frames. Selecting a saved manager value in a constructed example means a conditional forwarding of those values; it never joins a hypothetical invocation to that recorded manager call. Constructed invocations carry distinct identities even when values are equal. No packet, request identifier or journal row is fabricated.

Candidate scope, sample, source and evidence claims are compared with independently regenerated expectations. The adapter returns detached validation results. Exact builtin types are enforced in both manager snapshots and forwarded values, beyond JSON serialization equality. The six underlying status fields retain their original meanings, including the three literal False values.

## Failure interpretation

Each modeled evaluation/return stage requires a stated normal, unexpected-raise or process-termination outcome. Missing-owner handling uses a separate intended-raise outcome for the existing _fail helper. The fixed message and raise-from-None semantics come from source; suppression of displayed context does not establish absence of an ambient exception context.

Neither forwarding method contains a local catch, and this route is not a _dispatch invocation. Source-level return/exception relationships do not establish actual Python unwinding. An unexpected modeled raise, a source-intended fixed raise, process termination and location relative to catches remain distinct. In particular, termination supplies no terminal Python exception, retained error, completed cleanup, external nonexecution or renewed authorization. Outer control callback handling, revocation, launcher retention and cleanup are not inferred from this limited path. Earlier client classification support and its partial outer-continuation scope remain unchanged.

## Controls and preserved attempts

The initial control campaign's omitted-guard mutation accidentally left an already-empty syntactic guard list unchanged. That failed 17-check attempt, source, logs and traceback remain exact and excluded. The corrected campaign then passed 204 checks before additional exact-type hardening; those results and their original component identities remain separate.

Focused follow-up controls preserve and reproduce acceptance of same-named builtin subclasses in snapshots and serialization-equivalent subclasses in returned representations. The correction checks exact Python types rather than type names or serialization alone. No runtime source or prior producer function changed. The recovered-root campaign validates the corrected code, and fresh public/semantic/derivation controls exercise its actual mandatory chain. See RESULTS.json for distinct completed counts, process statuses and any failures. No completed historical test or review suite was rerun.

## Limits preserved

The 18 traced invocations and separate frameless Client.state observer remain distinct and unjoined. No new runtime status-forwarding, physical reference, owner-token lifetime, lock timing, exception/unwind or cleanup observations exist. Sparse evidence does not establish unseen transfers, complete repetition coverage, feasible interruption histories, canonical authority, exclusive ownership, storage durability or qualification. Existing reason/history and lifetime parameters remain unresolved; no string/call cap, deletion rule or cumulative-envelope architecture was adopted.

All eleven obligations, four inventory and fourteen lifetime UNKNOWN totals, Decision B, retention, allowances, reservations, accounting, signing/recovery uncertainty and both acquisitions remain preserved. SOURCE-ONLY unchanged; cumulative-envelope unadopted; backup kernel-only; streams UNCOMPUTED; readiness/final binding blocked; admission disabled. No runtime changes, requests, signatures, acquisitions, database connections, session operations, old-suite reruns or Git save were performed.
