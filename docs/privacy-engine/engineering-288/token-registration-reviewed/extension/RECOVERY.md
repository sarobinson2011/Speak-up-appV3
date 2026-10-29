# Recovery and independent-review entry

Verify the externally reported checkpoint byte count, entry count and SHA-256 first. Verify CRC, safe unique regular membership and all root MANIFEST.json identities before consuming candidate code. tools/checkpoint.py supplies read-only archive verification/extraction. Extract into a new persistent directory, without overlaying previous evidence, sessions or acquisitions. Preserve failed roots. No repair, removal of undeclared entries or automatic retry is authorized by these instructions.

The extracted root is executable offline using CPython 3.12.14, optimization disabled and Cryptography 50.0.2, as recorded. No application method, request, database connection or session is needed. A newly authorized independent validation may use:

```
python3 -I -B ROOT/code/correspondence.py --root ROOT --receipt ROOT/results/primary/token-registration-correspondence.json
```

The receipt contains both required contexts and all prior relations. code/correspondence.py validates exact retained/status membership, directories, regular entry types and hashes before consuming it. It then invokes the unchanged IS-01 predecessor and its mandatory earlier chain. The current producer is separately pinned. Returned result mutation does not alter freshly reconstructed expectations. tests/cli.py is the guarded public-CLI wrapper. tests/focused.py and tests/fresh.py document the new construction's tests, not permission to rerun completed campaigns.

retained/status is the exact decoded I164-IS01-correction.zip: 68,317,556 bytes; 2,053 entries; SHA-256 5915d8d409d043e9dd95535e91880263e26c776220b8c6d48bf75690e3fc60a9. Its MANIFEST.json is unchanged. The closure review was 67,410,780 bytes; 81 entries; SHA-256 6af86c83868178d81323b20705ae7c3c160da48bca29ee2d774d92be45d4e4fd. Its 80 non-input files are unchanged under retained/closure-review. That review manifest's single omitted input/I164-IS01-correction.zip is the redundant outer archive of retained/status. Exact outer archive identity was verified before decoding. The unchanged manifest is not falsely reinterpreted as a compact-root manifest. Historical outer-archive and compact-manifest qualifications in the predecessor remain in force. All bytes consumed by current validation are included.

A separate recovery input archive is assembled from the frozen current code, dependencies and primary receipt. Its exact identity and recovered results are recorded under provenance/ and results/. Final packaging adds documentation and new results; no executable code, predecessor input or receipt is changed after recovered validation. The final archive gets its own exact manifest. Supplied, independent and failed attempts remain separately attributed.

Runtime observations, complete repetition coverage, physical references, continuity/exclusivity and full outer-lifecycle qualification remain unavailable. No new acquisition, request, session operation, retention permission, policy adoption or admission follows from recovering this checkpoint.
