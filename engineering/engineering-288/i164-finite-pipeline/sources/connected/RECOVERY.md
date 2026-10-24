# Recover the CF-01 correction

Verify the supplied ZIP size/SHA-256, CRC, exact membership and all MANIFEST.json
hashes before use. `code/package.py verify ARCHIVE --extract NEW-PERSISTENT-DIR`
performs archive/member verification and fresh-extraction checks. Never use /tmp
or overwrite an existing result directory.

The correction is standalone beside unchanged predecessors. `code/connect.py` is
the corrected entry point; worker.py, recover.py, package.py and pins.json are
exact unchanged copies. CHANGED-IDENTITIES.json records exact before/after source
identities. No candidate/draft overlay or changed input archive is required.

Six original dependencies, exact identities in provenance/recovery-dependencies.json:
- Engineering-288C-I164-finite-native-inputs.zip
- Engineering-288C-I164-finite-native-consumer-verified.zip
- I164-finite-ledger-independent-review.zip (embeds the exact author ledger)
- Engineering-288C-I164-source-only-model-ledger-inputs.zip
- Engineering-Anchor2-I164-discriminator-type-closure-review.zip
- Engineering-Anchor2-I164-unknown-method-closure-review.zip

Use existing verified roots when available. Otherwise create locations.json with
keys inputs, consumer, ledger_review, draft, discriminator, unknown and absolute
archive paths. Then run under CPython 3.12.14, optimization disabled, with the
already prepared compatible dependencies:

```sh
python3 -B /ABS/correction/code/recover.py --locations /ABS/locations.json --output /ABS/NEW-RECOVERY
python3 -I -B /ABS/correction/code/connect.py --config /ABS/NEW-RECOVERY/config.json --output /ABS/NEW-VALIDATION
```

Full validation normally takes 5–15 minutes and prints progress every 30 seconds.
It runs saved-evidence validators only. No installation, session or database
connection occurs. Recovery or validation failure must retain its directory and
logs; do not silently admit extra members, reset state or automatically retry.

The separate CF-01 review archive is also needed to reproduce exact original
witness fixtures: I164-connected-finite-independent-review.zip, 34,472,947 bytes,
76 entries, SHA-256 633f343a9301c3311bbd9779fcef826cc97c396595f404fa4423eac5d2528201.
It embeds the exact original connected checkpoint and full false-receipt run.
The correction retains selected original members and their provenance, but does
not repeatedly nest the complete review and large unchanged output bytes.

Focused controls (do not run old component review suites):

```sh
python3 -I -B /ABS/correction/code/cf01_checks.py --review /ABS/EXACT-REVIEW-ROOT --connect /ABS/correction/code/connect.py --output /ABS/NEW-CF-CONTROLS
python3 -I -B /ABS/correction/code/full_fault.py --connect /ABS/correction/code/connect.py --config /ABS/RECOVERY/config.json --output /ABS/NEW-FAULT-RUN
```

The first command tests the narrow linkage boundary using authentic saved stage
outputs. Add --case witness, coordinated or positive for small fresh-process
controls. The second deliberately changes node_duties after the real ledger stage;
its expected outcome is LEDGER-RESULT-CORRESPONDENCE, no final receipt, and four
successful underlying stage executions. This is not a pristine acceptance test.

Large unchanged bundle/model/ledger outputs recover from the pinned components
and review members; generated-member manifests identify exact fresh run files.
Original archives, captures, failure evidence and unavailable-original retry ZIP
provenance remain unchanged. CF-01 independent closure is not claimed.
