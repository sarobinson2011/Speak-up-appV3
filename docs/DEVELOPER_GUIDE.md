# Developer and research guide

[STATE.md](../STATE.md) controls architecture, deployment records, invariants and governance. The [accepted G4 baseline](privacy-engine/generation-004/accepted-definition/engineering-287/README.md) identifies the operative specification and defining source inventory. G4 remains unpublished. Read the [threat model](PRIVACY_THREAT_MODEL.md) and [custody model](CONTINUITY_CUSTODY_MODEL_V1.md) before treating any lab result as applicable to another deployment.

## App interfaces

| Entry point | Inputs and outputs |
| --- | --- |
| [Browser proof hook](../frontend/src/hooks/useZKProof.js) | `generateProof(path, petitionId, memberSecret)` consumes local secret and depth-16 membership material. It returns proof arrays, nullifier and public signals. The active order is `[nullifier, petitionId, membershipRoot]` per `STATE.md`, the relay and the contract. |
| [Petitions](../backend/src/routes/petitions.js) | `GET /api/petitions` returns `{ ok, petitions }` from the SQLite index. `GET /api/petitions/:id` and `GET /api/petitions/:id/signature-count` use a nonnegative integer petition ID. |
| [Membership](../backend/src/routes/membership.js) | `GET /api/membership/status` returns coarse readiness and depth. `/api/membership/leaf-status?leaf=…`, `/api/membership/path?leaf=…` and `/api/membership/pathByIndex?index=…` expose lookup or prepared proof-path material. |
| [Admission lookup](../backend/src/routes/admission.js) | `GET /api/admission/:admissionCommitment` takes a 32-byte hex commitment. On success it returns `{ ok, admissionRight: { admissionCommitment, state } }` from the index. |
| [Relay submission](../backend/src/routes/relay.js) | `POST /api/relay/sign` takes `petitionId`, `nullifier`, `pA`, `pB`, `pC` and three `pubSignals`. It checks shape, consistency and index freshness. A successful response contains `ok` and `alreadySigned`, with `txHash` when supplied by execution. This is a transaction submission endpoint. |
| [Petition registry](../contracts/src/PetitionRegistry.sol) and [verifier](../contracts/src/v3/Groth16Verifier.sol) | The registry accepts `signPetitionWithZKProof(...)`. The verifier’s `verifyProof` accepts Groth16 arrays and three public signals and returns a Boolean. |
| [REFLECT publication objects](../backend/src/services/reflect/publicationObjects.js) | `buildLocalPublicationObjects({ material, chunkSize })` builds a descriptor, connector and chunks. The [local fixture](../backend/src/services/reflect/publicationObjects.test.js) shows the input material and verifies digest consistency, reconstruction and rejection of tampered state. |

On a configured local backend, `curl --fail-with-body http://localhost:3001/api/petitions` reads the indexed petition list. This is a read example, contingent on the backend configuration and database state.

The [frontend](../frontend/package.json) provides `npm ci` followed by `npm run build` from `frontend/`. With Node.js 22 and npm, the source-derived expected result is a Vite bundle in `frontend/dist/`. This build and the end-to-end testnet setup were not exercised in the documentation review. The backend’s actual template is [backend/.env.example](../backend/.env.example). Starting [the server](../backend/src/server.js) requires the intended RPC, contract addresses and local SQLite state. Relay use additionally requires the intended test relayer setup. The health route returns the configured RPC URL, so use a credential-free URL for shared diagnostics. Treat lockfiles and contract submodule revisions as the dependency inputs for a reproduction. Consult `STATE.md` before using deployment or signing scripts.

## Evidence and reproduction

- Use the [independent static validation record](privacy-engine/generation-004/implementation/engineering-288-independent-validation-complete/README.md) for saved scope, identities and results. The [I164 laboratory](../engineering/engineering-288/i164-laboratory/README.md) and [finite pipeline](../engineering/engineering-288/i164-finite-pipeline/README.md) describe exactly which source members are in Git and which require retained external archives.
- Start by comparing manifests, recorded hashes and result/exit records at the exact commit. To reproduce a strict laboratory run, first obtain and verify the named external archives and restore them into a fresh isolated directory using the checkpoint’s instructions. The public checkout alone supplies source selections. Results from a different runtime or input set need their own scope.
- [The golden-proof example](../zk/v3-groth16/test-golden-proof.js) expects the pinned witness WASM, proving key and verification key at its declared paths. The public checkout omits the expected build WASM, build R1CS and proving key at their manifest paths. The [artifact verifier](../scripts/zk/verify_manifest.sh) expects those files and checks their hashes. Keep the original manifest intact. Older artifact documents and the manifest’s order label disagree with the active `[nullifier, petitionId, membershipRoot]` interface. Use `STATE.md` and the active code for that interface. These examples are not a verified fresh-clone proof quickstart.

## Issues and contributions

Use [GitHub Issues](https://github.com/sarobinson2011/Speak-up-appV3/issues) for reproducible problems and to discuss scope. Include the commit, environment, exact command and expected versus actual result. Use test-only material in examples and keep secrets and private participant data out of reports. Ask for a private reporting route for sensitive details.

For a contribution, propose one bounded change, link the relevant `STATE.md` invariant and include the evidence for your change. Open a focused pull request for maintainer review. Keep protocol or architecture decisions in the existing Engineering[n] process and preserve frozen evidence. Disclose any included third-party source and its terms.
