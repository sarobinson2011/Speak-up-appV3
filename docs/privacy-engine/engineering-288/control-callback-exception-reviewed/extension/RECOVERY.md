# Recovery

Verify the separately reported final ZIP bytes/SHA-256, CRC, unique safe regular-file membership and every MANIFEST.json entry. Extract into a new empty directory without repairing an existing failed root. The mandatory adapter checks exact predecessor filesystem membership, directories, entry types and pinned bytes before consuming candidate inputs. tests/offline.py gates the entire recovered root before loading the new adapter.

For separately authorized offline validation, use the recorded CPython 3.12.14 / Cryptography 50.0.2 environment:

`python3 -I -B NEW_ROOT/code/correspondence.py --root NEW_ROOT --receipt NEW_ROOT/results/primary/control-exception.json`

This is a saved-input static validator, not an application launcher. The receipt requires the new relation and every predecessor relation. Reuse completed results; recovery instructions do not authorize campaign reruns or session/database operations.

The exact predecessor input archive was 88,596,749 bytes, 2,938 entries, SHA-256 c24b08d598115b1118121aeb6c9d42bbdd780a58a98375a29b96224e8c825876. Every member is preserved under retained/bare. Its original archive remains external; recompression does not reproduce the original outer identity. The independent review was 86,457,161 bytes, 65 entries, SHA-256 cd33f568c226319866e2c03aec678bc623e364369b962f261176ec54743fb6ba. Its 64 non-input members are retained/review; the duplicate input archive is not embedded again.

Original forensic partials and failed attempts stay outside their strict predecessor roots, in their declared original failure paths. The old 308/307/303 discrepancy remains qualified. A frozen recovery cut of this new checkpoint supplies fresh-process and recovered-root validation; final packaging adds their results without changing tested code or inputs. New failed attempts, if any, remain documented outside completed totals. No Git save is part of this implementation.
