# IS-01: exact in-memory types before normalization

This correction enforces the existing exact-type representation contract at return-input, submitted-output and semantic-claim boundaries of the internal status extension. It changes neither ManagedAuthority.status nor either runtime forwarder. Independent closure review is still required.

## Exact reviewed input and finding

Formal-Lab6-I164-internal-status-return-correspondence-independent-review(1).zip was verified as 66,394,354 bytes, 158 entries, SHA-256 b8135042b4638af1acebfd90ac07ba4aea844853148f8ce0c99804cac8643334. CRC, safe unique regular membership and all 157 manifest identities passed. The exact embedded target was 62,835,317 bytes, 1,845 entries, SHA-256 06d3b32fdf83757b40d9963a45a21ca5a5a80d2ca5c4af813655b4ad465f3864; CRC and all 1,844 hashes passed. Its original membership and directory/type structure remain checked before consumption.

The smallest witness changes a single reason value to a same-valued str subclass. JSON serialization is unchanged, but exact type is wrong. Submitted projections and semantic claims were accepted; the latter returned freshly reconstructed builtin values, hiding the input violation. A subclassed literal phase key also passed return-input and constructed validation. Related int/dict output subclasses were accepted. This was an in-memory acceptance defect, not a demonstrated forged public JSON receipt, operational bypass or admission.

Engineering reproduced the affected output/row/key paths in both contexts and the full semantic, derive_status and constructed_projection acceptances. The exact original review recipes and records are retained unchanged; tests/witnesses.py and results/original-witnesses record the bounded new reproductions. JSON cannot itself retain a Python subclass: the executable recipes, exact class definitions, mutation paths and pre-normalization assertions preserve that distinction. A normalized JSON value is not substituted for a witness.

## Correction and exact semantic meaning

status_exact_tree walks a finite representation without copying, encoding or comparing values. Containers must be exact builtin dict/list; every dictionary key must be exact builtin str. Representational scalar leaves must be exact builtin str/int/bool/float/NoneType. The existing field/shape/source checks then enforce the narrower types and values required at each location: phase/reason strings, epoch integer, and three exact False constants. An allowed generic scalar type is not permission to put that scalar in an incompatible field.

Class identity uses `is`, including the allowed-leaf test. It does not use a class name, isinstance, equality hooks, string conversion or a class's metaclass equality. Repeated aliases are accepted; cyclic structures are refused as non-finite JSON representations. No string length, call count, epoch cap, retention limit, phase restriction or new operational allowance is added. Existing JSON finite-number behavior remains unchanged. These representation checks do not establish physical object identity or imply that the runtime forwarders copy/serialize anything.

The producer adds status_typed_same and applies it only in the six existing internal-status functions. The inherited producer functions and preceding source bytes are unchanged. status_forward_source checks exact source bytes and type-checks field/boundary data before AST use. validate_status_forward checks submitted catalogues before construction/comparison. status_snapshot_value checks keys and nested representations before source selectors. status_forward_projection checks catalogue, return-input and validated premises before field access/comparison/copy. validate_status_forward_projection checks the submitted output before regeneration and equality.

The current adapter's local equality helper checks exact representation types first. _checked preflights submitted catalogues/claims before predecessor construction; _check_rows also checks its two row inputs directly, so coordinated contamination cannot evade typing. constructed_projection and _construct_checked check cases before source-derived branch selection/copying. Scope/reference helpers check their representational inputs. Candidate source maps require exact str keys and bytes values before equality. The public receipt still requires exact bytes and exact canonical JSON correspondence. Historical adapters and their equality helpers remain unchanged.

Expected field/source/instance/evidence values still come from the same fresh mandatory predecessor chain. Type preflight does not replace provenance, comparison, field guards or the two independently required contexts. Fresh rebuilding and separate deep copies continue to isolate validation expectations from returned objects. Invalid inputs are rejected; they are not repaired or normalized into legitimacy.

## Supported semantics preserved

The source is still ManagedAuthority.status -> ManagedSession.status -> _Control.status, with direct returns and source-defined owner/token routing. There is no _data, copy, _dispatch or additional READY guard on this path. Owner absence still takes the fixed failure; a prior owner failure does not block source-admitted diagnostics. Both contexts retain source-defined phases, unbounded reason content and instance-local epochs, exact six fields and all guarded declarations/relationships.

Modeled raises remain distinct from process termination. Termination establishes no Python exception, unwind, retained error, cleanup completion, nonexecution or renewed authorization. Existing permitted internal destinations remain; the general-client surface gains no status capability or output permission.

## Validation and preservation

RESULTS.json separates the new supplied controls, preserved independent review, prior supplied controls and any failures. The new focused controls cover subclasses with arbitrary and builtin-spoofing names, keys, nested lists/dictionaries/scalars, wrong builtin types, coordinated premises/claims, serialization-order tripwires, context substitution and nested mutation isolation. Source-admitted diagnostics and pristine public JSON remain accepted. Public entries and a fresh extracted recovery root are exercised separately using saved inputs only.

The independent review's 206 primary checks (107 PASS, 91 REJECTED, 8 DEFECT-ACCEPTED), 165 recovered checks (74 PASS, 82 REJECTED, 9 DEFECT-ACCEPTED), 17 residual confirmations and separate public CLI pass remain independent. Five zero-check membership refusals, two forensic partial files, their UNKNOWN cause and all older failed attempts remain preserved and excluded from completed totals. They are never treated as executable dependencies or repaired.

Primary test evidence records the exact producer and the pre-final adapter under provenance/. After that campaign, a single explicit correction-root lstat guard retained the predecessor's no-symlink-root requirement in the new layout. No semantic behavior or type algorithm changed. The fresh public-entry and recovered-root checks use the final code identities. The focused guard was also tightened to resolve relative paths and explicitly allow only its designated result directory; the original primary guard is preserved. This infrastructure adjustment is not a runtime change.

## Limits and boundaries

These are source-derived and constructed correspondence checks, not new runtime invocations or a lifetime/repetition proof. Missing ManagedSession.status/_Control.status frames, physical return/reference identity, actual forwarding counts and complete history remain unavailable. Sparse manager samples do not fill those gaps. The separate observer call remains unjoined. Original launcher-frame provenance and broader qualification remain unresolved.

All eleven obligations, four inventory and fourteen lifetime UNKNOWN totals, Decision B, retention, allowances and uncertainty protections are unchanged. SOURCE-ONLY unchanged; cumulative-envelope unadopted; readiness/final binding blocked; admission disabled. No requests, signatures, acquisitions, database connections, session operations, runtime changes, completed-review/suite/pipeline reruns or Git save occurred. The only recommendation is independent scoped closure review of this correction checkpoint.
