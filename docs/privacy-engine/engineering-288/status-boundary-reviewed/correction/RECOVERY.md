# Recovery and reproduction

Verify the outer archive's communicated byte size and SHA-256, safe unique membership, CRC and exact MANIFEST.json identities. Extract into a new persistent directory; never overlay a launcher, candidate tree or existing session. The package is self-contained for this boundary review and its disposable controls. It is not a complete application runtime recovery.

Read REPORT.md before running anything. These are the **new** focused controls, to be run only when independently authorized for review; no predecessor tests or lifecycle need repetition:

```bash
python3 -I -B tests/checks.py --output /absolute/new/review-boundary-controls
python3 -I -B tests/adjacent_checks.py /absolute/new/review-adjacent-controls
python3 -I -B tests/correspondence_checks.py /absolute/new/review-correspondence-controls
```

Each output directory must not exist. `--resume-after-copy-fix` records the author's bounded continuation after the retained harness failure; reviewers should normally use the full first command. Source inspection and exact binding validation alone need no backend:

```bash
python3 -I -B code/correspondence.py check provenance/status-correspondence.json
```

No general entry initialization or session-opening command is supplied for Steve's host. Future use requires the exact inherited candidate/draft/runtime and environment prerequisites and separate execution authorization. The new entry does not migrate session metadata, rewrite existing launcher bindings or claim that old bindings attested this new entry. The source/contract binding is the separately verified additive artifact.

The archive includes exact test evidence files and inventories for redundant recovered/mutation source trees. Those trees remain in the author's working checkpoint but are not duplicated in the delivery. Their source members are recoverable from retained/, basis/, code/, the retained harness version and the exact recorded copy/mutation operations. Special-file mutation fixtures are represented by type/path inventory and rejection stderr, not extracted as live FIFO/symlink entries. Original failed results are never replaced by successful ones.

Independent root-code trust and a stable trusted filesystem are required. Dependency checks reject undeclared entries before reading candidate payloads, but are not a defense against concurrent hostile filesystem mutation or a party replacing both verifier code and its authority. General clients cannot obtain status through the exposed API; arbitrary Python introspection/debugging can bypass that API boundary and is excluded honestly.
