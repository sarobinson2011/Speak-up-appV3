Formal-Lab[6] SOC correction independent-review checkpoint

Verify the delivered review ZIP's stated size, SHA-256, CRC, safe unique regular membership and MANIFEST.json before extracting into a new persistent directory. MANIFEST.json lists every other review member with exact byte length and SHA-256; it does not hash itself. The complete exact target is retained as input/I164-SOC01-SOC02-correction.zip, including all prior recovery dependencies and original witness evidence.

The target is 21,703,078 bytes, 554 entries, SHA-256 6f90951280861fc27e4539cfd0596ecfb3c98a1c30b74bfe528042922b42a948. code/verify_input.py independently checks this identity, CRC, safe exact membership, manifest identities and nested archives. It can extract a new target root with --extract; it refuses to overwrite an existing root. code/verify_composition.py compares delivered composition and preserved sources against the exact included predecessor archives. Neither runs an application or a retained test suite.

The smallest residual is self-contained in minimal-recovered/. It changes one original trace byte and preserves the source, event identity, return snapshot and other evidence. The independently verified result records semantic and derive acceptance, public rejection, and subsequent pristine acceptance.

For a later explicitly authorized bounded reproduction on CPython 3.12.14, optimization disabled, with the target recovered at /absolute/new/target:

```bash
python3 -I -B code/minimal_residual.py \
  /absolute/new/target/corrected \
  /absolute/new/offline-residual-evidence
```

The output directory must not exist. This invokes only the offline occurrence adapter and its retained source/correspondence validators. It does not execute the worker, launch a session or connect to a database. Do not run any host worker, session launcher, historical smoke, boundary tests, completed pipelines or lifecycle as part of recovery. Do not install dependencies or change source code merely to execute this checkpoint.

The primary controls reproduce only the nine required old witnesses and perform new correction-focused checks. The focused recovered controls use the second independently extracted root. Their counts are review assertions, including assertions proving bad acceptance; they are not producer executions or evidence of general trace coverage. Supplied Engineering controls remain inside the target and were inspected, not rerun. No completed-review suite was rerun.

Report and checkpoint scope is noncanonical. All prior blockers, SOURCE-ONLY, UNKNOWN obligations/totals and admission-disabled status remain unchanged.
