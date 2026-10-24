# Finite native consumer v1

This is a new prospective finite representation, not a historical full-model file.
The immutable Occurrence stores index, acquisition/context/local identity, class,
actual bytes, and canonical immutable source metadata. NativeContext contains
class groups, half-open token ranges, ordered typed endpoints and retained duties.
The JSON interchange preserves payloads as exact lowercase hex and retains the
source metadata. Reading it does not supply its own validation expectations.

Sources, unchanged and checked against the reviewed candidate manifest:
- native/code/expand_candidate.py:32–67 Seq/Group; 169–198 pairs.
- native/code/expand_candidate.py:69–167 historical prepare; 222–234 token/edge
  output. These full-model builders are NOT invoked.
- compiler/prospective_procedure.py:19–27 reviewed prospective Group/lookup.
- native/code/bind_ledger.py: retained duty contract, never executed.
- Reviewed finite_inputs.py native_contract(), _derive(), _consume() and the
  exact reviewed outputs/bundle.json are the prospective construction contract.

Explicit differences from historical construction:
1. Tokens hold actual selected-acquisition bytes, not arbitrary symbolic token
   placeholders. Keys and indices are local to one acquisition AND one context.
2. Group is immutable and implements the bounded entries(None), get(key), parts
   interface already used by prospective_procedure.Group. Missing/duplicate
   matches reject rather than historical first-match/None behavior. Prefix
   traversal is unsupported and rejects; no caller in this slice needs it.
3. All work uses role-separated PARENT-RECORD keyed lookup. Rule kinds and source
   metadata remain attached to duties. No semantic dependency classification is
   inferred from the mechanical lookup operator. No Cartesian rule is admitted.
4. Contexts are constructed independently, without the historical even-count or
   equal-halves assumption. No parent/base offsets or arrays are appended.
5. Twelve n-ary fold obligations/context remain separate duties, not pair rows.

Trust boundary: this consumer intentionally accepts only the exact independently
reviewed saved bundle from the pinned original component archive. It rechecks
archive identity, CRC, exact membership, all member hashes and native source
identities on every public run. It does not generalize input admission or rerun
predecessor authentication/projection suites. The completed independent review
and prepared-host result establish the reused bundle validity within their
scope. This is not capture-hash-only validation of a mutable native output:
expected occurrence objects/groups/ranges/endpoints are freshly constructed
from that trusted bundle, pure native lookup is executed, and submitted native
representation is compared using canonical exact-type serialization. Altering
both native payload and its metadata cannot alter trusted input expectations.

Public command:
python3 -I -B code/consumer.py --component /absolute/original-component.zip \
  --output /absolute/new-persistent-output

Reopening/validation:
python3 -I -B code/consumer.py --component /absolute/original-component.zip \
  --submitted /absolute/prior-output/native.json --output /absolute/new-output

The supplied path must be Engineering-288C-I164-finite-native-inputs.zip exact
45,747,644 bytes SHA256
94791c65c3502d85fc452c0e9c100391f5d0199f7690462e92b91c1a600caa8b.
No databases, builders, historical module imports, ledger binding, installation
or full universe are involved. Only the AST/source-pinned pure pairs function
is executed. Results mean acceptance by THIS finite native consumer, not complete
historical native-consumer acceptance, a complete model or a rebound ledger.

The work-row `new=True` flag is relative to this fresh finite construction only;
it is not a new runtime action or a claim about a historical appended model.
Byte positions retain the source record index/JSON pointer and local token index.
Payloads are the projection's exact canonical bytes (including newline), not
claims of physical substring offsets in an original database or wire packet.
