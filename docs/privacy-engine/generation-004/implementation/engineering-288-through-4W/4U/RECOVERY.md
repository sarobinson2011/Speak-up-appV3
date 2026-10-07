# Recovery and reproducible commands

Extract the delivered ZIP into a fresh directory. Keep historical packages and local textual job untouched. These commands operate on the package, do not change cwd, do not use Speak-up-appV3 and do not read .env. Substitute only the absolute package/input paths.

Read-only metadata and saved-evidence verification:

```bash
python3 -B /absolute/path/Engineering-288-checkpoint-4U/tools/verify.py
```

Focused metadata tests (stdout/stderr only; no regression rerun):

```bash
python3 -B /absolute/path/Engineering-288-checkpoint-4U/tools/check_metadata.py
```

If the unchanged 4S model is already extracted, add:

```bash
python3 -B /absolute/path/Engineering-288-checkpoint-4U/tools/verify.py --model /absolute/path/Engineering-288-checkpoint-4S/candidate/model.json
```

Otherwise restore only that model, to a fresh output path:

```bash
python3 -B /absolute/path/Engineering-288-checkpoint-4U/tools/restore_model.py --archive /absolute/path/Engineering-288-checkpoint-4S.zip --output /absolute/path/new-model-copy/model.json
```

The archive must be exactly 512,084,676 bytes, SHA-256 ae4f7fa4469c1b90345fb05858be3e661ae67265dfab4cdf933d7fb825aacbbf. Restoration writes only the exact 382,700,006-byte model, checks SHA dd946419e4fd4c657a0a0d663b145e958ddf3c4957bf006b94b5c3f7ec96e74d, refuses overwrite and publishes after file fsync. Allow ~383 MB additional disk if used. No model expansion occurs.

The original 4T completion snapshot and kit are included under retained/. Completed return evidence and verifier are under historical/4T/. Optional reproduction of that prior metadata-only check:

```bash
python3 -B /absolute/path/Engineering-288-checkpoint-4U/historical/4T/verify-4T-return.py /absolute/path/Engineering-288-checkpoint-4U/retained/Engineering-288-checkpoint-4T.zip /absolute/path/Engineering-288-checkpoint-4U/retained/Engineering-288-4T-textual-completion.zip /absolute/path/new-return-check.json
```

This optional check extracts saved metadata temporarily, uses libcrypto.so.3 solely for finalizing saved SHA states, and invokes only retained verify-completion. It does not run/resume native stream computation. 4U reuses its completed result by default. Do not restore the completed job under a new identity or start another run.

Metadata derivation is deterministic: tools/bind_text.py regenerates only derived/ in an extracted working copy; it does not mutate historical/ or any kernel/source/model file. Re-run verify afterward; generated derived bytes must match the sealed manifest. Each ordinary verification can be restarted from the immutable ZIP after interruption; no expensive stream state is involved. Seal tools publish ZIP via temporary file, CRC verification, fsync, atomic replace and directory fsync.

The original 4Q archive (464,223,570 bytes, SHA-256 353d158a0a7cbbd8f0a33619f4123eb7fc3e95921f3c92aed3b3312aebc7cd32) is an exact historical reference. Its needed inventories are already included. Earlier signed fixtures and journal scopes are never relabelled. Local integrity receipts are not authority or qualification.
