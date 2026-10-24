# I164 dependency-maintenance assessment — proposal v1, 2026-10-23

## Decision

Recommend a **separate CPython 3.12.14 / Cryptography 50.0.2 / cffi 2.1.1 / pycparser 3.11 compatibility environment**, Linux x86_64 glibc >=2.34, using only the three exact wheels in requirements-50.0.2.lock. The Cryptography wheel's expected bundled backend is OpenSSL 4.0.3. This is a proposed dependency baseline, not an adopted runtime profile, session migration or operational assurance.

Keep the original 41.0.7 environment and existing session bound to their original identities. No candidate, bootstrap, profile or evidence bytes were edited. No environment was installed during this assessment. New commands are prepared, not executed on Steve's host. The current assessment runtime already has 50.0.2; its inventory and small public primitive probe are fresh evidence, explicitly separate from Steve's host and from the completed independent review.

## Independent finite-consumer support incorporated

Review: Engineering-Anchor2-I164-finite-native-consumer-independent-review(1).zip, 19,999,861 bytes, 61 entries, SHA-256 df97d1842f52606e40365db0a98d3f5fa46ed38eaf07f34656aeb456d3d140cd. CRC, exact manifest membership and all member hashes verified. Its REVIEW.txt and manifest are retained here; completed review suites were not rerun.

**55 fresh independent controls remain distinct from 28 supplied controls.** Six additional fresh-process negatives are reported separately. Scoped consumer support is retained, including both contexts, preserved UNKNOWN/eleven obligations and exact historical preservation. The review itself ran on CPython 3.12.14 / Cryptography 50.0.2. The consumer is stdlib plus pinned pure lookup; that review did not exercise Cryptography signing or reauthenticate the saved acquisition. It therefore supports the finite consumer in that environment, not the full runtime under a new cryptographic baseline.

## Source-backed API inventory

Exact paths, hashes, imports and candidate call expressions are in provenance/api-sites.json. source-inventory.json retains the selected 24 source/text hits authenticated against the 666-member transport. Sixteen Python files directly import Cryptography. bootstrap-inventory.json identifies additional current/older/harness hits by archive chain and hash; old failure fixtures are not promoted to current implementation. runtime-layout.json records the source-owned 93-member runtime layout. The native consumer contains no Cryptography API call.

| Actual use | Defining source | Reachability and input form |
|---|---|---|
| Ed25519PrivateKey.from_private_bytes, public_key, sign | support/reference/runtime/authority.py:13–27; retained wire.py signing helper; lab fixture producers | Fixed-size raw seeds; domain-prefixed canonical bytes. Laboratory identities are not custody evidence. No signing executed in this assessment. |
| Ed25519PublicKey.from_public_bytes, verify | support/code/correspondence.py:9–15,103; authority.py:27,141; retained wire.py:138; outcome.py:137; transport.py:32; compiler/managed_observations.py:232–234 | Raw public bytes and decoded hex signatures; exact canonical/message or digest bytes. This is the relevant authentication path. |
| serialization.Encoding.Raw, PublicFormat.Raw, public_bytes | authority.py:19; wire.py:19 and fixtures | Exact raw public-key encoding; no X.509/PEM/PKCS12 parsing required. |
| InvalidSignature | retained wire.py and verification paths | Exception semantics must be retained; malformed lengths/bytes must still fail. |
| ec.derive_private_key(1, SECP256K1), ECDSA(Prehashed(SHA256)), encode_dss_signature | historical90/retained-candidate/code/test_signed.py:15–17 | Retained test using prime-field secp256k1, **not binary SECT**. The digest is produced elsewhere; Prehashed(SHA256) is not permission to change that digest. |
| version('cryptography') | retained C2 session_identity.py; bootstrap environment/bindings | Runtime identity input, not just an informational version string. |

No Cryptography X.509 path verification, PKCS12, PKCS7 decrypt, RSA decrypt, SECT ECDH/ECDSA, DH exchange or cipher API was found in this pinned usage inventory. This is a scoped static result, not a whole-installed-system or arbitrary-plugin reachability proof. Native helpers, Python's TLS library, installer traffic and external callers need their own applicable assessments.

## Build identity: established versus missing

**Steve host, retained evidence:** CPython 3.12.14, Cryptography 41.0.7, cffi 2.1.1, pycparser 3.11; SQLite 3.53.1. The interpreter is 30,976,376 bytes, SHA-256 5ebcd7993f0e40cb4b16e15d2c4c3c343ecad419966299b8e8f6f9e6a36bf779. ENVIRONMENT-RESULT.json is 1,720 bytes / d8314be91461a8307d0ff474865ac5b1dd86712a65d44141f6fc6dc8e12b4508; requirements.lock is 11,173 bytes / 93c41e8b77049d05a764127cad3b3d42832810e7742a14f3537c3f0e5ac4fa50. These identities are checked before prepared commands proceed.

The retained host result does **not** establish the installed Cryptography backend OpenSSL version, binary payload hashes or exact wheel origin. Published upstream wheel defaults cannot fill that gap. The inventory command reads the actual backend version and package METADATA/WHEEL/RECORD/native-extension identities without importing project code. These measurements are still not authentication of an old installed wheel's provenance.

**Fresh assessment runtime:** CPython 3.12.14 / Cryptography 50.0.2 / cffi 2.1.1 / pycparser 3.11. Cryptography backend OpenSSL 4.0.3 (29 Sep 2026); Python ssl uses a **different** OpenSSL 3.5.8 (25 Aug 2026). Exact metadata and binary hashes are in provenance/current-build-inventory.json. Never report `ssl.OPENSSL_VERSION` as Cryptography's backend version.

**Proposed installation:** exact wheel hashes, wheel CRC, and installed payload equality are required. Installer-generated RECORD is explicitly excepted from payload equality and separately hashed; wheel contents are not silently substituted. The bundled ensurepip installer is part of the prepared interpreter distribution and is recorded by its log; it is not part of the three-package application lock. This is not a complete interpreter/OS supply-chain attestation.

## Official advisory applicability, assessed 2026-10-23

Package-range membership does not establish exploitable reachability. No exploit was executed. The following is a bounded mapping of retrieved official advisories to the pinned API domain, not a claim that every transitive/native vulnerability has been excluded. Older advisory pagination was unavailable; individual primary sources and release history were used where retrievable. Recheck advisories before adopting/running a later host baseline.

| Advisory / official source | 41.0.7 / candidate disposition | Actual usage assessment |
|---|---|---|
| GHSA-r6ph-v2qm-q3c2 / CVE-2026-26007 (SECT subgroup), patched 46.0.5 | 41.0.7 is in affected package range; 50.0.2 includes fix and removes SECT APIs | Ed25519 and SECP256K1 are not SECT; affected path not demonstrated. |
| GHSA-6vqw-3v5j-54x4 / CVE-2024-26130, PKCS12 serialization, patched 42.0.4 | 41.0.7 in range; 50.0.2 patched | No PKCS12 serialization path found. |
| CVE-2024-0727, OpenSSL PKCS12 decoding; upstream fixes 3.1.5/3.2.1 etc. | Old upstream wheels may contain affected OpenSSL; actual host build must be read. Candidate 4.0.3 postdates fix | No PKCS12 loading path found. |
| GHSA-h4gh-qq45-vh27 / CVE-2024-6119, wheel OpenSSL X.509 name checks, patched Cryptography 43.0.1 | Official 41.0.7 wheel range affected; candidate patched | No certificate name-check path in inventoried I164 Cryptography use. Python/installer TLS is a separate library/use. |
| GHSA-537c-gmf6-5ccf, OpenSSL June 2026 bundle advisory, patched Cryptography 48.0.1 | Broad older-wheel affected range; candidate uses newer 4.0.3 | Advisory covers PKCS7/CMS, TLS/QUIC, ASN.1/cipher and other paths. None establishes an Ed25519 exploit in this slice. Old-host OpenSSL build and any additional consumers remain needed for broader applicability. |
| GHSA-m959-cc7f-wv43 (patched 46.0.6); GHSA-m2h6-j472-rp4c and GHSA-jwv3-5hgf-82ww (patched 49.0.0) | Broad metadata ranges must not be read as proof that 41 implements the affected verifier: X.509 path API introduced in 42. Candidate patched | No X.509 path verifier use. |
| GHSA-p423-j2cm-9vmq / CVE-2026-39892, non-contiguous buffers, introduced 45, patched 46.0.7 | 41 outside affected range; candidate patched | Observed source producers pass bytes; no strided-buffer source found. |
| GHSA-g6cj-pr64-35w5 / CVE-2026-69247, PKCS7 decrypt oracle, introduced 44, patched 50.0.0 | 41 outside affected range; candidate patched | No PKCS7 decrypt use. |
| GHSA-79v4-65xg-pq4g, wheel OpenSSL issue, 42.0.0–44.0.0 | 41 outside stated package range; candidate newer | No claim of a 41 vulnerability from this range. |
| Prior PKCS7 parsing CVE-2023-49083 | Already addressed before 41.0.7 | No new 41 regression inferred. |

RSA PKCS#1 v1.5 timing advisories (including CVE-2023-50782) are another reason not to generalize this assessment to arbitrary 41.0.7 users. No RSA decryption use was found; the primary project issue was unavailable here, so no independently verified fixed-version derivation is asserted for that row. This unresolved advisory-source retrieval does not affect the observed Ed25519 API classification, but prevents an exhaustive historical advisory audit claim.

Primary URLs (no third-party scanner result used as the basis of a technical conclusion):
- https://cryptography.io/en/stable/changelog/ (50.0.2 official wheels OpenSSL 4.0.3; X.509 API introduced 42; changed/removed APIs)
- https://cryptography.io/en/41.0.7/changelog/
- https://github.com/pyca/cryptography/security/advisories (individual GHSA identifiers above appended to this URL)
- https://openssl-library.org/news/secadv/20240125.txt
- https://openssl-library.org/news/secadv/20240903.txt
- https://openssl-library.org/news/secadv/20260609.txt
- https://openssl-library.org/news/vulnerabilities-4.0/
- https://pypi.org/project/cryptography/50.0.2/
- https://pypi.org/project/cffi/2.1.1/
- https://pypi.org/project/pycparser/3.11/

The 50.0.2 wheel uses abi3 for CPython >=3.11 and the selected platform requires glibc >=2.34. Its declared CPython dependency is cffi>=2.0.0; cffi requires pycparser. typing-extensions is conditional on Python<3.11 and therefore not applicable here; bcrypt is an SSH extra not requested. Retaining cffi 2.1.1 / pycparser 3.11 minimizes this proposal's change. Their complete independent security audit is not claimed. 50.0.2's removal of SECT/obsolete aliases and parser tightening do not require a change in the inventoried raw-key APIs; this inference still needs saved-export compatibility on the proposed host.

## Exact gate and binding changes required before new-runtime use

Current corrected launcher: overlay/implementation/code/lab_bootstrap.py, 11,148 bytes, SHA-256 b2ce7f0fdf9aabb578da7330a9987a34b7c76e1fe1f543f913ba759aededc2f6. `enforce_environment()` requires CPython 3.12.14, optimize=0, **Cryptography == 41.0.7**. `binding()` includes launcher identity and source manifests. Its BR-01 archive was checked: 15,341,542 bytes, SHA-256 1ca0a131a5b0e43799577388ad23752b53306f8067d92fe5b61ce366db777c3e; CRC and all 48 manifest members passed.

1. A separately authorized prospective launcher/profile revision would need an exact 50.0.2 gate, new wheel/backend/runtime identity fields and corresponding launcher/configuration pins. Do not replace equality with a permissive minimum, accept either version on an old session, or monkey-patch verification.
2. Update only prospective host wrappers that currently enforce 41.0.7. Preserve original-record reconciliation assertions, old locks and saved checks as historical facts. Their expected 41.0.7 value is not a defect.
3. Generate new environment/result identities for the new environment; do not rewrite ENVIRONMENT-RESULT.json or session_identity runtime bindings. Existing session-001 remains with its original environment. This assessment authorizes no migration or new session.
4. Keep the supported Requires-Dist marker handling; 50.0.2 adds/uses platform_python_implementation and python_full_version conditions. Check complete applicability on the new interpreter using pip check plus exact installed metadata, not an omitted-marker workaround. The old successful marker correction remains supported, not retested here.
5. The finite consumer has no such Cryptography gate; no consumer source amendment is needed just to run it under the proposed dependency environment. Its successful stdlib operation cannot replace cryptographic saved-export compatibility.

No gate changes are applied in this deliverable. The new helper has its own explicit, dependency-only 50.0.2 scope, never invokes a gated launcher and does not claim that an old launcher passed.

## Completed checks and precise remaining task

Fresh here: source/hash inspection, current assessment build inventory, syntax checks for both prepared scripts, five isolated helper controls (payload/membership rejection), and nine public primitive/interface checks in results/assessment-runtime-probe.json. No keys generated, no signing, no saved application validation campaign, no review suite rerun. Setup/download/install have NOT been executed; official hashes have been read from PyPI, not presented as locally downloaded wheel verification.

Smallest next input: run **inventory only** on Steve's preserved interpreter, obtaining its actual backend OpenSSL and binary/build identities. This is read-only except a new persistent report. It resolves host-build applicability, not installed-wheel provenance. The separate setup/check commands are prepared for adoption of the proposed baseline. They download only the locked wheels into a new directory, then check installed payloads, versions/backend and public API behavior.

After those pass, the next bounded code task is the explicit prospective gate/profile revision plus one saved-authenticated-export compatibility run under that revised profile; exact bytes, rejection behavior and both contexts must agree. Signing-runtime compatibility still needs its own authorized laboratory tests before any new session may use the profile. The primitive probe and independent finite consumer review alone do not establish that result.

All eleven obligations, source-only designation, historical identities, limits, unapproved retention boundary, Decision B and operational custody/rollback/lifetime/capacity blockers remain. No dependency update establishes model completion, native global acceptance, canonical registration, qualification, readiness or final binding. Streams UNCOMPUTED; admission disabled.
