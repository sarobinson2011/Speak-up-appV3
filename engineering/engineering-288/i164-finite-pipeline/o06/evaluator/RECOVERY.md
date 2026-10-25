# Exact recovery and bounded evaluation

Verify this archive CRC, safe unique membership and every MANIFEST.json hash before
extraction. code/package.py verify ARCHIVE --extract NEW_ROOT provides that check.
Use a new persistent directory, never /tmp. No installation or database opening.

Required predecessor: I164-O09-finite-integration.zip, 5,480,698 bytes, 68 entries,
SHA-256 eadb44f3b35ce4714a17e9c0919e09bf51f4364dad00fd2fdb860f731ecb40de.
Its exact recovery instructions and six external archive pins are retained in
provenance/O09-RECOVERY.md and provenance/O09-recover.py. Use the actual predecessor
code/recover.py with its original connect.py and provenance/pins.json; the isolated
reference copy here is not a standalone recovery package. Reuse already verified
roots. Do not run its finite pipeline or completed review suite merely for recovery.

Independent predecessor review: 32,159,843 bytes, 76 entries, SHA-256
164f8f3c6fd33d8393cc341deddc4f60b809a0ae94e1cec0488b2f6453a88ea4.
Original review and implementation archives remain separately preserved. Compact
source/provenance records and exact lineage receipt are included here.

After exact O09 recovery has produced config.json:

    python3 -I -B code/configure.py --recovered-config /persistent/O09/config.json --output /persistent/new-config.json
    python3 -I -B code/multiplicity.py --config /persistent/new-config.json --output /persistent/new-evaluation

Expected duration: approximately 20–60 seconds depending on source verification I/O.
No retry is automatic. Preserve any failure directory and logs. Output contains the
14 definitions, finite selected calculations or precise UNKNOWN dependencies,
context/count/procedure and source bindings, and all eleven obligations.

Focused new checks (not the predecessor reviews):

    python3 -I -B code/checks.py --config /persistent/new-config.json --output /persistent/new-checks
    python3 -I -B code/extra_checks.py --config /persistent/new-config.json --output /persistent/new-extra-checks

Allow several minutes because negative public-receipt checks revalidate current
inputs. --case positive / --case stale on checks.py supplies fresh-process controls.
Repeat from an exact recovered code root for path independence. Conditional fixtures
are labeled constructed arithmetic/source-selector fixtures, not saved execution.
Do not use conditional() or snapshot_rows() as independent authentication entry points.
