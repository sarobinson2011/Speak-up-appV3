# Formal-Lab[6] independent owner-lock descriptor-finalization review

**SUPPORTED within the bounded mandatory SOURCE-ONLY normal owner-lock descriptor-finalization correspondence contract.** No residual defect witness was found in this slice. The target is **I164-owner-lock-finalization-correspondence-1.zip**, not the preceding normal-session-exit checkpoint.

Review author: **Formal-Lab[6]**. Construction author: **SU-Engineering[288D]**. I did not author this construction. Implementation code and existing evidence were left unchanged. Engineering's results were inspected separately from the fresh independent controls below. Review date: 29 October 2026.

## Input, recovery and preservation

The archive is exactly **74,161,617 bytes, 2,495 unique regular-file entries**, SHA-256 `09f8b6d8c527f4032977f4e2862ba9a23e0e678a6f8294a5050603a26fb43a9b`. CRC, safe relative paths, exact membership and all **2,494 manifested hashes** pass. Both independently extracted strict roots (`ol-input`, `ol-recovered`) contain 2,495 files and 736 implied directories and passed final membership/type/byte checks.

The exact previously verified original normal-exit archive and its independent review were available and reused for direct member-byte comparison. Their identities remain, respectively, 70,593,959 bytes / SHA-256 `c9c8d2106617970e8008fadc3c60f61813c64e7ce07e24a60bc92ac1029b954a`, and 71,870,780 bytes / SHA-256 `c6c1952bde68aef3e9434968cd8838cfcbd4ab606e39fcaba112e6f73dada3df`. All **2,331 predecessor members** match exactly under `retained/exit/`; all **103 non-input prior-review records** match under `retained/review/`. The redundant original input ZIP omitted from the compact review tree matches the retained decoded predecessor, and no recompression is represented as its original ZIP bytes.

Both declared implementation changes match their old/new identities and the complete supplied diff: `code/correspondence.py` and six additive functions in `code/managed_coverage.py`. All **89 inherited producer functions/classes**, their source bodies and the non-function AST are unchanged. The prior prefix is unchanged apart from a descriptive comment before the extension. Current source pins agree with actual source bytes. Historical validators and runtime source files are unchanged.

The assembled current receipt preserves every prior context field, historical identity, relationship, ordinal, obligation and scoped finding, adding only the new mandatory relation and declared extension bindings. Current receipt: **4,348,225 bytes**, SHA-256 `6f2d1ac375017fd2f92923522aeba36defb89992d7fd071dd385e11d991d3c42`.

All present required nested archives were inspected: **18 archive occurrences**, with CRC, safe membership and manifest hashes checked. The current tree contains **35 interpretable manifest documents**, including preserved compact review/forensic/provenance manifests. Their historical omitted or rebased entries remain explicitly recorded; they are not silently recast as newly recovered original outer ZIPs. Actual fresh mandatory-chain validation succeeds from the final recovered target using saved inputs only.

Engineering's intermediate recovery cut is recorded as 74,047,490 bytes / 2,460 entries / SHA-256 `df0392e30335948e3cd6b01f6209857a7b0c42cba9393fedc9abd774539d84b4`. Its retained manifest is 685,947 bytes / SHA-256 `ee966f6746f1c2dfa4478b5d05df205b6cd13395dadb56bb57ccf27902c71be3`. All **2,459 selected nonmanifest member bytes** match the final target. The intermediate outer ZIP itself was not freshly verified; independent recovery used the externally identified final target.

## Independently derived source requirements

The defining source is `source-evidence/lab_bootstrap.py`: **11,481 bytes**, SHA-256 `245d4f36d687834aeee064a60d4414b15f7b8babfdb5dec192aa995d93af2b78`. Its exact bytes match the validated predecessor chain. `prospective_entry.py` and `live_connection.py` remain unchanged at their previously verified identities, listed in CHECKPOINT.json.

Independent AST traversal finds one `fd` store at line 112, before the outer try/finally. It is the result of `os.open(parent/('.'+dest.name+'.owner.lock'), os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW, 0o600)`. There is no later `fd` assignment or deletion in owner_lock. The inner cooperative flock call uses that local with `LOCK_EX|LOCK_NB`, and its BlockingIOError handler raises the fixed contention failure. Normal continuation reaches `yield dest` at line 116.

The outer finalbody has exactly one expression statement at line 117: **`os.close(fd)`**, with one argument and no keyword arguments. The return value is discarded; no returned object or runtime None observation is manufactured. Open-result binding precedes entry to the protected region: a failed open alone cannot establish finalizer entry. Conversely, the source finally also applies to exceptional exits once its protected region has been entered; the new normal-only model does not deny those paths.

`_session` enters this owner_lock invocation with `as dest` at line 137. Its normal protected body ends with the existing managed close, distinct local clear and ACTIVE.json unlink at lines 165–166. No further normal body statement or intervening successful cleanup is inserted between this validated tail and leaving the owner-lock context. Ordinary resumption into the finalbody remains an explicit modeled continuation, not an observed generator/context-manager frame.

| Required new point | Source basis | What a normal modeled point establishes |
| --- | --- | --- |
| owner-finalizer-enter | Containing try/finally, anchored at 113–117 | Acknowledged finalbody entry on the selected normal route |
| descriptor-close-attempt | Call expression at 117 | Normal argument/call-entry continuation using the selected local fd |
| descriptor-close-complete | Expression statement at 117 | Normal completion of that selected modeled call |

The independent oracle checks source coordinates, exact expressions, the close argument's finalbody guard, enclosing normal prefixes and the three-point ordering. The entry marker's anchor is the containing Try, explicitly labeled finally-entry; it is not a runtime event at the Try's first line. Expected coverage is derived from source rather than from the generated declaration list. Changing `os.close(fd)` to another argument, removing the call, or changing the os.open mode while updating the claimed source identity still rejects on defining-source validation.

## Mandatory chain and descriptor lineage

The new mandatory entry executes the predecessor's unchanged `_checked` and `_assemble`, exactly the validation/assembly performed by `derive_exit`, and reaches the underlying validated status chain. Monitored calls confirm actual execution of that chain rather than collection of detached results. The canonical predecessor must equal the exact saved reviewed normal-exit receipt. New source/catalogue expectations are regenerated from freshly loaded inputs; supplied evidence, candidate sources and bindings must match those actually consumed.

Both SYMBOLIC-U-ONE and SYMBOLIC-U-TWO require the new relation. A normal predecessor must report `normal-marker-unlink-completion` with its independently validated removal flag. It cannot be replaced by a mutually consistent caller report. The selected constructed exit case is revalidated against the same predecessor basis, context, anchor and invocation before new steps are admitted. The old normal-exit receipt cannot substitute for the current mandatory receipt.

Descriptor identity here is a **source-result lineage**, qualified by context, acquisition, validated instance, invocation, owner_lock occurrence and the os.open result occurrence. Its local `fd` use is tied to the source producer and close argument. Repeated equal operations remain distinct through their qualified scopes and invocation identities. Event-local strings are not global physical IDs, and the two symbolic contexts do not create a claim of two physical resources.

A bare descriptor integer, an invented numeric observation, another invocation's descriptor result, another scope's manager/session reference, or a substituted lock path rejects. Numeric descriptor observation, runtime descriptor identity and physical resource identity remain null. Unchanged local binding does not establish that a kernel descriptor was never closed/reused elsewhere, that the same physical resource still exists, or that the process has exclusive custody.

The path relation is source-qualified and uses the predecessor's exact destination/session records. Its nominal form is the recorded parent plus `.` + destination name + `.owner.lock`. The source resolves the destination's parent, but this construction does not resolve a host path, inspect an inode or establish physical path equivalence. Equal paths and descriptor numbers cannot prove resource identity.

Selected-owner continuity remains an explicit conditional premise. Unknown continuity stays admitted with selected-owner removal unestablished. Neither the predecessor's marker removal nor modeled descriptor close upgrades continuity to operational exclusivity, physical lock release, durable closure or new authorization.

## Prefix and failure meaning

Every next point requires normal completion of the preceding modeled point. A constructed raise, process termination or unobserved continuation ends the prefix. Missing, duplicated or reordered points reject. A failed/unknown close attempt does not establish successful call entry or close completion. The three milestones are separate; a finalizer-entry claim alone is not a completed-close claim.

Only an explicit modeled raise establishes a modeled Python-exception frontier. Termination and absent observations do not establish an exception, Python unwind, retained error, cleanup or renewed authorization. An explicit raise is still not runtime unwind evidence. Flags record acknowledged facts in this conditional prefix; False means unestablished, not proof that an unobserved effect could not have occurred.

For a non-normal predecessor, the result is outside-normal-finalization-slice with no new events. **This does not prove the finalizer did not run**: exceptional finalization and remaining outer cleanup are unexpanded. Existing normal close, local-clear and marker facts survive later uncertainty exactly as validated. An absent marker or earlier clear cannot fill missing finalizer/close observations. Even normal modeled descriptor-close completion leaves physical descriptor closure, physical lock release, exclusive ownership, durability, complete outer context exit and obligation discharge unestablished.

## Fresh independent testing versus supplied evidence

| Evidence class | Completed checks | Results |
| --- | ---: | --- |
| Independent primary | 265 | 59 positive; 206 expected rejections |
| Independent recovered-root subset | 49 | 15 positive; 34 expected rejections |
| Independent fresh semantic/derivation process | 3 | 2 positive; 1 expected rejection |
| Independent fresh public constructed process | 2 | 1 positive; 1 expected rejection |
| Independent fresh public/CLI process | 4 | 1 actual CLI positive; 3 expected rejections |
| **Independent total** | **323** | **78 positive; 245 expected rejections; CLI counted once** |
| Engineering primary, inspected only | 218 | 73 positive; 145 rejections |
| Engineering recovered-root, inspected only | 57 | 23 positive; 34 rejections |
| Engineering process records, inspected only | 9 | 4 positive; 5 rejections; CLI included |

Fresh controls exercise both contexts; optional control and unknown continuity; each stage's raise, termination and unobserved frontier; every omitted/duplicated point and noncanonical ordering; false continuation; non-normal predecessor joins; wrong invocation/acquisition/instance/session/owner references; descriptor producer/argument/path substitution; coordinated report and evidence changes; stale/missing inputs; exact nested types and literal keys; boolean/integer confusion; and unsupported physical/qualification/status conclusions.

Nested returned-object mutations, context reversal and lineage-copy mutations cannot change validation expectations. Fresh semantic/derivation calls reproduce the exact pristine receipt after returned mutations, then reject a coordinated saved-destination/lineage substitution. Fresh public constructed validation rejects a coordinated foreign descriptor occurrence. The actual recovered offline CLI accepts the exact two-context receipt; invented descriptor observations, missing mandatory relation and partial legacy receipt substitution reject.

Environment: **CPython 3.12.14 / Cryptography 50.0.2**, isolated mode, optimization 0, bytecode writes disabled. Control guards prohibited application/session methods, database/network operations, host-session access and writes outside review outputs. Only saved evidence and finite constructed premises were used. No descriptor-producing or finalizing launcher runtime operation was executed. This is not prepared-host 41.0.7 compatibility, installed-wheel authentication or new runtime/OS/filesystem qualification.

## Preserved interrupted attempt and historical failures

Engineering's interrupted derivation attempt has **zero completed assertions**, exit 137 / shell “Killed”, no completed result/progress record and cause **UNESTABLISHED**. Its exact ATTEMPT.json and stdout remain under `failures/derive-attempt-1/` in the target. It is excluded from every completed total; no cause such as resource exhaustion is inferred. The frozen earlier attempts.json predates the process checks; process-attempts.json and RESULTS.json explicitly reconcile the later interruption and successful attempt. No completed check is silently repeated or counted twice.

All earlier failures remain unchanged. In particular, the earlier unexplained partial file is preserved as `retained/review/failures/recovered-membership/forensic-extra.bin`, **25,690,112 bytes**, SHA-256 `ed75ee885f67eca2938340b1aa5c423a9e60c04bceedfd3f90933cba0c44345e`, with its original metadata and failed-gate records. It remains outside `retained/exit`, the strict predecessor root. Its origin is not established and it is neither adopted as an input nor silently deleted. No new independent control attempt failed in this review.

## Limits and disposition

The source correspondence and bounded constructed normal path are supported. Runtime descriptor allocation, finalizer entry, close attempt and close completion remain **unobserved/unjoined**. The 18 saved traced invocations and separate frameless Client.state observer retain their distinct provenance; the observer remains unjoined. Saved confirmed-close and cooperative-lock assertions are retained predecessor evidence, not evidence of the new descriptor chain.

Exceptional finalization, outer cleanup, actual descriptor lifetime/resource continuity, operational custody/exclusivity, physical lock-release semantics, host path/inode identity, durability and complete lifetime/repetition coverage remain unresolved. No additional host/session check is needed for this expressly static/constructed verdict. Any later claim that this chain actually executed requires separately authorized, invocation-linked observations of the missing producer/finalizer/call steps and the relevant operational qualifications.

O01–O11 remain bound to the unchanged 56,813-byte obligations document, SHA-256 `2c92141711e260a2ef0271635562cbac5a71aae82ac7e1a52b5dbc6f228d3a45`. All four inventory UNKNOWN totals and fourteen lifetime UNKNOWN totals, Decision B, retention, allowances, accounting/reservations/uncertainty protections and prior scoped closures remain unchanged. SOURCE-ONLY remains; cumulative-envelope is unadopted; backup remains kernel-only; streams remain UNCOMPUTED; readiness/final binding stay blocked; **admission remains disabled**.

No requests, acquisitions, runtime changes, session/database operations, host smoke, completed pipeline/review/suite or lifecycle reruns, policy changes or adoption occurred. The reusable predecessor fixture helper generated finite case inputs only; its old review suite was not run. This checkpoint is prepared for Engineering-Anchor[2]; no external message was sent.
