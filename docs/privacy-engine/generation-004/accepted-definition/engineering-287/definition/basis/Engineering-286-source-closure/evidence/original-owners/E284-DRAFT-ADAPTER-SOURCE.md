# Canonical source-read adapter proposal

Local owner E284-DRAFT-ADAPTER-SOURCE. This is a concrete documentary adapter design for the existing S70 authenticated-read boundary. It is not installed, published, appointed or admitted. The proposal chooses the already declared canonical TSEV1 boundary: it does not design an RPC, appoint a blockchain observer, or import archived implementation behavior as protocol meaning. Exact source authority remains an external admission input.

<a id="carrier"></a>
## AD01 — exact carrier and decoder

input-dispatch.tsv declares all 94 ordered root fields, exact existing types, documentary owning anchors and equality definitions. For each field supply one complete TSEV1 value plus the existing S70 ReadObject metadata: object identity, source and anchor, authentication evidence identity/bytes and authority endpoint evidence. The canonical value is decoded against the exact field type, with no trailing bytes, reduction, default, reordering or normalization of malformed input. Primitive and derived tuple encoding follows S70. The types reachable from the 94 root-field signatures are primitives or tuples. The program also declares a static component SET, handled by its existing expression machinery; this root-input adapter does not decode SET values. The supplied canonical-carrier.py is a fresh documentary decoder for that declared subset, not an authority validator or historical constructor execution.

The external representation at this boundary is therefore concrete. A producer starting with RPC/ABI/JSON/chain data must supply its separately adequate translation and evidence to this exact boundary. That producer is not silently included in this decoder or deemed trustworthy because its output parses.

<a id="assembly"></a>
## AD02 — deterministic assembly

1. Load the exact candidate type, field, definition and operation declarations and the 94-row dispatch. Reject missing, duplicate, extra or reordered root-field assignments and mismatched declared types/owners/anchors. Preserve every read occurrence separately; no identity groups are selected.
2. Decode every supplied canonical value. Apply IF02 scalar assessment to the candidate public inputs before authoritative admission, and the complete root-suffix/scoped-state assessments to source values at their governed validation boundary. Canonical UINT parsing alone is not scalar validation.
3. Require independently established competent source validation of each supplied fact and its exact evidence binding. Source references in this draft remain unappointed labels until that basis exists. Never accept caller-supplied authoritative/valid/authenticated flags as proof. A missing validation basis produces no successful source-read assembly.
4. Establish exact fixed A/type/R/C/PI joins, OC01–10 scope/cut/joint-currentness requirements, root/state binding tuples and VI01–04 qualified proof-result meaning. In particular, a raw archived verifier FALSE does not become a completed negative. Establish the complete applicable rule assignment before E begins; no catch-all TRUE.
5. Pass the exact ordered source-validated values through S70's existing ReadObject boundary to E284-DRAFT-E-VALID-DOMAIN-ENTRY. The root consumes all 94 fields. Every actual source/authentication/input/argument/control/operation dependency is retained by the existing constructor. The adapter itself does not mint D or redefine the successful E/D boundary.
6. At a U gate independently supply source-validated CURRENT component values/statuses and complete owning authorization/attempt/currentness records. Preserve authorized bindings. Use the existing comparison procedure and its failure precedence, not the E completeness fold.
7. Recovery uses the complete actual least Dep(D) closure and a fresh validation/equality map under the original 21-row function. The field dispatch is not that map. Failed U stays terminal.

These are normative proposal steps at the adapter boundary, not an assertion that a real source has executed them. An actual producer may require more operations; every such contribution must be integrated rather than hidden behind this interface.

<a id="failure"></a>
## AD03 — failure mapping

Malformed/out-of-domain candidate n,a,r or inability to assess them refuses authoritative admission under the selected rule; no A/E/D/acceptance/rejection is created. After E begins, unavailable required verification/source/completion evidence cannot yield a rejecting D. At a gate, invalid identity/context/source/authorization material follows validation-first indeterminate handling; a validated independently sufficient material conflict follows the existing MC rule. After successful E/D, later adapter delivery failure does not alter D or reopen E. These phases must not be collapsed into one generic false result.

<a id="dependency"></a>
## AD04 — dependency and privacy integration

The concrete boundary's field, equality, type and owner joins are exactly input-dispatch.tsv plus the integrated 118-field inventory. The 24 component-stage fields remain distinct from 94 E root fields. Their declared phase/custody and two-context relations are in observation-interface-draft. Existing S70 evidence/authority nodes bind the actual source evidence bytes; opaque bytes do not discharge missing source semantics.

No new public field is introduced. Internal joined records, completion evidence and cut/source metadata remain confidential within their authorized boundaries; existing public PI equality joins remain in the model. A producer's additional source/API/trace/log/observer surface must be declared and assessed before claiming full privacy completeness. The proposed adapter boundary is closed as a declaration; a concrete producer and independent evidence are not supplied by it.

<a id="admission"></a>
## AD05 — exact admission dependencies

To admit a realization of this proposal requires: (a) an adequate governing source/lifecycle basis for the four selected semantics and exact new source clauses; (b) competent source ownership and concrete producer/decoder/currentness/verification correspondence; (c) final canonical body/program/privacy joins and required coordinate sets after producer dependencies are known; and (d) independent privacy appointment and evidence for those exact bytes. Actual A/E/D/U/current facts belong at use. No successful runtime, conformance, adoption or lifecycle claim is made.

The next construction step is to compose the proposed source changes into an exact successor-source delta and admission basis. It is not another request that Steve find unspecified authoritative files. The existing local contracts are its authored inputs. Missing authority must remain explicit through that construction; it cannot be manufactured by signatures or by a numbering rollover.
