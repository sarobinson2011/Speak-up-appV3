# Recovery

Verify the delivered ZIP's externally reported byte length, entries and SHA-256. Check CRC, safe paths, exact membership and every MANIFEST.json hash/size. The manifest covers all members except itself. Read REPORT.md, RETURN-RECEIPT.json, changed-identities.json and CLOSURE-REVIEW-HANDOVER.md.

Preserve the received checkpoint. For reproduction, extract a disposable copy, then:

    mv results results-saved
    mkdir results
    python3 -B code/check_sd01.py
    python3 -B code/check_static.py
    python3 -B code/check_reconciliation_semantics.py
    python3 -B code/check_checklist.py
    python3 -B code/check_adjacent_positive.py

Run each under a 60-second local subprocess timeout, as recorded in results-saved/commands.json. Python 3 and the existing cryptography dependency are required. Do not install anything or invoke candidate lifecycle scripts. check_static.py creates a new fixture-only reconciliation tree and intentionally refuses an existing destination. check_sd01.py executes the exact preserved witness against old and current checkers using in-memory catalogue omissions; it never edits candidate or defining source files. Results are written only in the disposable copy. Absolute paths in recorded commands identify the original execution, not required recovery paths.

The original review witness script is retained as historical evidence and expects omission acceptance; use check_sd01.py for old/new comparison after correction. Old results, earlier reports and failed versions are not current verdicts. The source allowlist in response_obligations.py denotes supported AST/type-adapter compatibility only, not appointed qualification.

Compact preservation: this checkpoint does not nest the full prior review or 90-file historical tree. The original review remains identified as 14,147,242 bytes / 205 entries / 748d91a396bfc94fe6ce5b367d17241d464541c96df72bb6805257dccbc2c300. Do not relabel any checkpoint as an originally unavailable retry ZIP or reopen historical recovery searches.

Return to Engineering-Anchor[2] before independent closure review. Actual admission remains disabled; canonical reconciliation remains blocked; streams remain UNCOMPUTED.
