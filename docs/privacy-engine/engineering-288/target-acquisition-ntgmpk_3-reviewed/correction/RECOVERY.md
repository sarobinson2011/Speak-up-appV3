# Correction checkpoint recovery

Verify this ZIP's external SHA-256, unique safe regular membership, CRC and MANIFEST.json before use. Code and input identities are pinned separately from generated evaluation outputs. All deliberate changes relative to the predecessor are listed in CHANGED-IDENTITIES.json; code differences are also included.

The corrected checkpoint includes unchanged candidate/draft transports and both retained acquisition forms. It does not need an original database, running session or network service. Do not rerun the completed chain merely for continuity.

For a separately authorized closure review, recover source roots into an unused isolated directory and validate the saved outputs:

```sh
python3 -I -B code/evaluate.py recover --roots /tmp/I164-TE-closure-roots-NEW
python3 -I -B code/evaluate.py validate --roots /tmp/I164-TE-closure-roots-NEW --output evaluation
```

The entire directory layout and entry types must match the manifests. Do not remove unexplained files or weaken checks to force acceptance. Recovery rejects an existing destination. Current process environment is recorded in evaluation/RESULT.json; wheel installation provenance is not established by this checkpoint.

Witnesses are under witnesses/, the supplied independent findings under prior-review/, and new controls/logs under results/. Failures are separate under failures/. The correction-tools scripts use a workpaths JSON to identify explicit predecessor, corrected, root and fixture directories; those paths are historical scratch bindings and must be rebound before an authorized reproduction. The original implementation and full independent review are exact external dependencies listed in provenance/verified-dependencies.json. The original completed review is never invoked by these correction controls.
