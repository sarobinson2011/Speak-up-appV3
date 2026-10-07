# Focused textual byte-law review

No definition was reopened. The exact retained generator and 4A controller are unchanged. The portable supervisor/preflight are 4T derivatives of the tested 4R glue.

| Obligation | Source and implementation correspondence |
| --- | --- |
| Header | S70.md lines 745–748: five LINK_HEADER cells. Exact 67 bytes are `link_order\tfrom_token_id\tto_token_id\trelation_order\trelation_class\n`. |
| Encoding | Active S90-FCR.md lines 786–788 preserve TAB/LF UTF-8, no BOM/CR. Every retained token ID is checked printable ASCII, a subset of UTF-8; worker emits the exact ASCII bytes. No identifier rewriting, normalization or aliasing. |
| Structural rows | S90-FCR.md lines 748–764 and 773–776: exact original endpoint indexes, one-based template order and relation class. Distinct template orders retain distinct provenance even when endpoints/class coincide. |
| Potential rows | S90-FCR.md lines 775–779 and unchanged model predicate: original index i<j, with left arbitrary OR right arbitrary OR equal symbolic digest. Lexical sorting never swaps endpoints; a lexically larger from-ID is valid when its original index is smaller. |
| Merge and duplicates | S90-FCR.md lines 779–781: set union of four-string tuples, sorted lexically. Worker sorts/deduplicates structural tuples. Potential rows use relation order 000000 and EQUALS; structural order is positive, so the two sets do not collide. Numeric structural ordering equals string ordering because every relation order is exactly six decimal digits within 1..999999. |
| Ordinals | S90-FCR.md lines 782–785 and S70 link_bytes, lines 966–967: global one-based link_order, minimum six digits. 1000000 and larger remain valid. relation_order remains closed ORD6 and never exceeds 999999. |
| Exact identity | Hash the one header and every serialized row, including every terminal LF, in this exact order. Each committed segment exports cumulative SHA-256 state; whole-stream identity follows only from contiguous coverage from the header to the last lexical source boundary. Segment digest concatenation is never used. |
| Evidence boundary | S90-FCR.md lines 789–795 retain scopes and whole-view duties. Same-generator replay is not the independent supplied-row validator, signature authentication, source qualification or actual admission. |

Pinned executable source: runner/links.cpp. Its Edge sorting key is (lexical from-rank, lexical to-rank, ORD6 numeric value, relation class); this equals the required four-string sort for the verified fixed-width relation domain. The loop emits a legal equality tuple first (order 000000), then sorted positive-order structural tuples for that endpoint pair. Structural duplicate removal compares all four fields exactly. Explicit tests include duplicate structural tuples, same endpoints with distinct order, structural EQUALS at positive order, reverse lexical endpoint orientation, self structural links, literal .$record names and global ordinals above six digits.

The generic native descriptor parser is not offered as an untrusted input validator. Its descriptor is an exact manifest-pinned private input. Corrupted/substituted descriptors fail before a job starts. Every descriptor token, fixed group and structural row was compared to the exact 4S model, without expansion or potential-pair enumeration.

The independent small Python oracle constructs combinations directly, forms the full four-string set, sorts it, assigns global ordinals and writes exact TSV bytes. The worker hashes and lengths match these independently constructed bytes at every tested split. Oracle agreement verifies these bounded serialization cases; it is not full-universe conformance. The current full stream SHA-256 remains null.
