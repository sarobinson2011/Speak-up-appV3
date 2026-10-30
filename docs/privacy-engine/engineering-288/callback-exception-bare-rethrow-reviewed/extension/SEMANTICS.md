# Exact selected branch

Defining source: source-evidence/prospective_entry.py, 9,485 bytes, SHA-256 a1d80c523ae220228a6b27cac42b5e57a006336e858a8e7db0a75355d6cf2ae9.

The selected client callback call at 179 raises into its BaseException handler at 180. At 181, `owner.failure is not None` evaluates false because the selected same-owner slot is exactly None. The following expression-free `raise` at 183 reraises the active callback exception. The protected finally at 186 calls `_OWNERS.pop(token, None)` at 188 and discards its result.

The six conditional points are callback-handler-enter, callback-none-guard, callback-bare-rethrow, finally-enter, removal-attempt and removal-complete. The producer derives the handler, guard, bare raise, source coordinates and containing guards from the defining AST independently of submitted declarations. Existing token/reference/revocation mappings supply the prefix, exact acquisition/instance/context and invocation-qualified role references. Both prior stored-failure relations remain mandatory and are compared with the exact freshly validated predecessor receipt.

The None state is a selected-guard premise. Arbitrary callback safety, absence of intervening mutations, no earlier stored failure and a permission to clear retained evidence do not follow. Selected-owner registry continuity is a separate explicit premise; UNKNOWN continuity remains admitted and cannot establish removal of that owner.

Bare raise preserves the selected callback-error semantic reference. It introduces no new explicit cause assignment. This does not establish that existing __cause__, __context__ or __suppress_context__ is absent, false or unchanged by arbitrary earlier callback activity. No exception chain, producer type/value/history, bytes, runtime object address or frame is fabricated. Current saved inputs provide no new chain evidence. Separate role names for a later evaluation or cleanup error neither prove physical inequality nor merge actual occurrences.

Normal handler and guard progression reaches bare rethrow. A modeled evaluation/interruption exception at handler, guard or rethrow skips the remaining handler points and conditionally enters finally with that replacement pending. A finally/removal exception ends the slice with a cleanup-error role; callback propagation and normal removal are not guaranteed. Termination or unobserved continuation stops without inferred Python exception/unwind or later completion. Earlier acknowledged prefix facts are retained; false completion flags mean unestablished, not absence of unobserved effects.

Normal pop establishes selected-key absence at that modeled point only. Finally entry, removal attempt and completion are separate claims. Selected-owner removal additionally requires continuity. No `_run` success, launcher arrival, full outer cleanup, physical revocation/lock release, exclusivity, durability, qualification or authorization renewal follows. The None branch does not erase earlier established failure storage or any original retained evidence.

The exact-type contract covers nested scalars, containers and literal dictionary keys before normalization/comparison. Fresh validation expectations are isolated from returned mutable results. No runtime source is changed. No lifetime or repetition completeness is claimed.
