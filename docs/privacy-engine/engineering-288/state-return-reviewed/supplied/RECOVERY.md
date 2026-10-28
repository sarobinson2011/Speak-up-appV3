# Recover this state-return extension

Verify the delivered ZIP's reported size/SHA-256, safe unique regular membership, CRC and every top-level MANIFEST.json hash before extraction into a new persistent directory. Never overwrite a session or evidence master. Preserve nested historical manifests unchanged.

The complete 918-member config checkpoint is decoded under retained/config/, with all executable saved-input predecessors. Its original outer identity is 41,158,663 bytes, SHA-256 e97feef76c75230c8ebc348844192d825a28ee2efd5b38ae27f0edd86f16c52f. retained/config-review/ contains the compact exact records of Formal-Lab's support. Its redundant input ZIP and 22,806,528-byte failed-root binary remain in the exact external review archive: 63,598,176 bytes, 43 entries, SHA-256 97ccc050f291230f667a8d1fde28d9f655d75a28d72ec6604654d728cb5dcf94. provenance/input-verification.json lists the omissions and their exact identities. They are archival preservation dependencies, not missing executable inputs. Historical manifests still retain their full original scopes.

Using Python 3.12.14, optimization disabled and bytecode writes disabled, the new guarded public check is:

```sh
python3 -I -B tests/fresh_check.py "$PWD"
```

It validates results/state-correspondence.json through the current mandatory entry. It does not invoke previous tests, review scripts or session/application entry points. No database connection is needed. The direct CLI is code/correspondence.py --root ROOT --receipt RECEIPT; the guarded wrapper is preferred.

For separately authorized independent review, the new focused controls accept:

```sh
python3 -I -B tests/controls.py --root "$PWD" --output /absolute/new/persistent/state-review
```

--recovered selects the smaller recovered-root set. Do not pass --write against the supplied receipt. These commands are recovery instructions, not authorization to repeat completed checks now.

results/recovery-input.json identifies the separately packaged/extracted stable input used for the supplied recovered-root check. Its code, tests, retained inputs, provenance, documentation and receipt are compared with this final deliverable. Primary in-progress/results files and later completed result records are not confused with that intermediate input. The final checkpoint has its own outer identity.

provenance/previous-git-receipt.json records the already completed config save at 16ece61efdb4189b9edcac1baf67759f49ca0232. No save is repeated or new unreviewed code committed here. The missing runtime chain, separate observer, constructed reference scope and all current privacy/readiness/admission boundaries remain explicit.
