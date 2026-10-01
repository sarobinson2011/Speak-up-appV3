# Exact verification-completion interface draft

Documentary owner E284-DRAFT-VERIFIER-INTERFACE-SOURCE. This is proposed source wording, not a published/appointed successor source or implementation edit. It preserves the on-chain authority role and exact proof relation. It does not create a new first-class verification-outcome subject, wire format or PE-TSE operator.

<a id="qualification"></a>
## VI01 — qualified result, not raw return

The consumed proof result is bound to one bounded V, exact Z, ordered PI=(n,a,r), governing relation, compatible verifier/artifact material and protocol-relevant context. Before authoritative admission, apply the selected canonical scalar/domain assessment. During the proof component, classify proof-valid or proof-invalid only if every computation required by the identified verification semantics completed, produced a determinate result and is supported by the competent source's exact correspondence evidence. Completed valid maps to TRUE; completed invalid maps to FALSE. Inability to establish completion or its exact binding maps to no usable completed result/UNRESOLVED at the existing Boolean interface. It cannot map to FALSE merely because the implementation returned false or reverted.

This qualification is a validity condition on the existing VERIFICATION-BINDING and PROOF-VALID reads. It does not add a caller-controlled completed flag. The source assessment must establish completion independently from the same return bit. Failed source assessment follows S70's failure precedence; it does not generate a successful E package. Unknown proof result cannot be masked by a known negative root/uniqueness result.

<a id="evidence"></a>
## VI02 — exact required correspondence

The owning source must distinguish: all required verifier steps successfully completed with relation satisfied; all required steps successfully completed with relation unsatisfied; and inability to establish either completed case. It must bind the exact executed verifier identity/artifacts, proof bytes/encoding, PI ordering and values, relation, context and outcome. Evidence must establish the relevant branch and every contributing operation at its actual governed boundary. A trace obtained from an unappointed provider or an unchecked success bit is not sufficient. No requirement to publish this internal evidence is introduced; full privacy/custody assessment remains necessary.

A bare Boolean interface is usable only if its governing source establishes that every FALSE in its admitted domain means a completed negative. Otherwise its value alone is insufficient. The archived Groth16Verifier does not satisfy that condition from its source return behavior: failed mul/add/pairing calls and a completed negative pairing can return the same FALSE. Source inspection proves an ambiguity of the offered value, not a live reachable attack or an impossibility of future adequate evidence.

<a id="non-equivalence"></a>
## VI03 — information-loss proof

Let x be a completed, correspondence-valid negative verification and y an inability to complete a required underlying operation. The inspected return mapping can give b(x)=FALSE=b(y). Any downstream deterministic classifier whose only distinguishing input is b must give f(b(x))=f(b(y)). The required semantics distinguish completed proof-invalid from inability. Therefore the Boolean alone cannot provide the required classifier. Exact completion evidence or a faithful changed realization is necessary; changing the error label does not recover the lost information. This is a two-case semantic argument, not execution of an archived verifier.

<a id="boundary"></a>
## VI04 — full-program consequence

The typed E candidate already separates proof identity/bytes, V, relation, artifact binding, PI and proof result. VI01–03 specify what the source must establish for those reads. The remaining task is concrete correspondence/evidence integration, including all contributing calls/reads and private observability surfaces. Neither a local source ID nor a digest appoints that source. Preserve source-call failure, input incoherence and complete negative distinctions throughout E. At U gates retain validation-first and independently sufficient material conflict; do not replace gate semantics with the complete-E aggregation guard.
