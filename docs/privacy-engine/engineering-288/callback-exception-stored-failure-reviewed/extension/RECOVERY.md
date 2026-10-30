# Saved-input recovery

Verify the final archive's supplied byte count/SHA-256, CRC, exact safe membership and every MANIFEST.json identity before candidate use. Extract to a new persistent empty directory, never overlay a failed root. tests/offline.py verifies exact filesystem files, implied directories and entry types before candidate consumption. The mandatory adapter separately gates the full retained/stored tree.

For a separately authorized offline validation, the public entry is:

`python3 -I -B NEW_ROOT/code/correspondence.py --root NEW_ROOT --receipt NEW_ROOT/results/primary/callback-stored-failure.json`

Use the recorded isolated CPython 3.12.14 / Cryptography 50.0.2 profile. This does not qualify a host installation, other versions, physical ownership or durability. Saved completed results should be reused; recovery itself does not authorize repeating suites.

The exact predecessor is I164-stored-failure-revocation-correspondence-1.zip, 76,307,999 bytes, 2,661 entries, SHA-256 cd36a49cf2366c95aa96d8407e182eec716e6e77d261a1b0908ec250266230bf. All its members are retained/stored. Its corrected receipt is 5,337,262 bytes, SHA-256 2523144c01a3bfa57d7e85b51ec3c907dab787ff23057bb4be5763ac9edc4548. Its independent review is 78,909,450 bytes, 96 entries, SHA-256 7ea2c551a2f6cf12472bf4a2396b4f2146763deb4fff9a3420a25cea9e13d0cf; all 95 non-input review members are retained/review. Recompression of a decoded tree does not reconstruct the original outer ZIP stream. All prior intermediate-cut and forensic limitations remain in effect.

The initial new-control attempt failed the predecessor membership gate with zero assertions before candidate consumption. The failed root was left intact; its unexpected partial bytes and metadata are preserved under failures/initial-membership, outside the strict retained/stored tree. Its origin is UNESTABLISHED. A separate clean root was recovered from the same exact archive without deleting or repairing the failed root. Historical Engineering and independent failed/partial attempts remain separately retained.

The new process checks use a frozen packaging cut containing exact code, primary receipt and tests. Its manifest and identity are retained in provenance; the final checkpoint adds only completed process results/provenance without changing tested bytes. Read RESULTS.json for actual counts and limits. New implementation review is pending. No Git save or application operation is part of this checkpoint.
