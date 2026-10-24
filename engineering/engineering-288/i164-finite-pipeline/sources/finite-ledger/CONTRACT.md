# Finite mechanical duty ledger contract v1

Scope: a new prospective ledger serialization for the already verified finite
representation only. It is NOT I164-MECHANICAL-LEDGER-BINDING-1, a registered
ledger, a complete native model, or a call to historical bind_ledger.build().

Source-determined parts:
- native/code/bind_ledger.py::DUTIES: eight exact node-duty names. They are read
  by literal AST evaluation from authenticated source bytes, never imported.
- bind_ledger.py::build node duties: binding to actual saved model, node token
  ranges and undischargeable duties. Historical complete-model offsets and slot
  constants in build are inapplicable and are NOT copied to the finite ledger.
- bind_ledger.py::check_binding: exact model/contract association, false
  qualification/admission and no invented stream identities.
- compiler/prospective_procedure.py::duty_names/count_only/consume/validate_result:
  per-class/context duties, local finite ranges, UNKNOWN/NOT-ESTABLISHED status,
  ordered keyed relation duties, n-ary obligations and unqualified procedure inputs.
- Reviewed finite representation: its exact directory members, ordered edges,
  mechanical/fold duties and retained procedure result define this acquisition's
  complete finite row domain. The independently reviewed verifier authenticates
  that representation against its immutable input bundle before construction.

New mechanical serialization fields are explicitly introduced by this slice:
format I164-FINITE-MECHANICAL-LEDGER-1; entry_key=[NODE|RELATION|FOLD, context,
class|ordinal]; binding={finite_model:{bytes,sha256}, acquisition, context}; and
local half-open token_range/edge_range. They express existing associations; they
are not canonical identities, appointments, authority records or new semantics.
The model identity is the exact submitted finite bytes, not a full-model identity.
A valid reserialization receives a different exact binding, not historical-byte
attribution. Each public call revalidates the representation; receipts alone
cannot authorize a ledger. No caller-supplied ledger supplies its expectations.

Node entries retain complete directory metadata and all occurrence keys in their
range, including empty directories and their unresolved production expressions.
Relation entries retain the exact source duty and ordered edge rows in one local
edge interval, including every zero-count duty. Endpoints retain acquisition,
context and occurrence keys; matching contents never collapse occurrences.
Fold entries retain the exact n-ary source duty and resolve each endpoint class's
members to local token ranges/indices. They have no manufactured pair/edge range.
Each entry is bound to model bytes and acquisition/context. A context contains
its complete retained procedure result. All three O01–O11 obligation collections
are retained exactly. Classification stays UNKNOWN; qualification UNAVAILABLE;
disposition NOT-ESTABLISHED. No duty is discharged by ledger construction.

Public interfaces: ledger.run(component, consumer, model, submitted=None) and CLI.
The bundled unchanged verifier source is hash-checked before import. Its public
run authenticates inputs and checks the actual model bytes. The second read is
matched to its receipt; duties come from separately authenticated archive bytes.
Expected entries are freshly derived every call, and exact canonical comparisons
reject altered/missing/duplicate entries and extra or escalated status fields.
Internal derive() assumes authenticated inputs and is not an admission API.
Trusted process/source integrity and immutable input expectations remain required;
this is not hostile concurrent filesystem or resource-exhaustion assurance.

Full canonical ledger contract remains unavailable for this finite object:
complete current model descriptors/serialization/global ranges, applicable full
verification and canonical profile/procedure designation are absent. Qualified
appointments/assessments and operational evidence are also absent. No substitute
is made for these requirements. The finite mechanical slice is independently
constructible under the retained prospective procedure contract above.
