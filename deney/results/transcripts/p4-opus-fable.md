# P4-opus-fable final report — 9 tool uses, ~309s

Built analyze.py; order: exclusion -> anomaly check -> level counts. Outputs: anomalies.txt, per_file/<name>.log.txt (all 6, empty.log at 0/0/0), summary.json.

R7: INFO 600, WARN 176, ERROR 94; busiest hour 14 (205, independently reconfirmed via grep/cut/sort); excluded 26. Anomalies 6 (legacy.log DD/MM/YYYY lines).

Verification: excluded cross-checked grep -cE -> 26 (noted all were INFO, explaining 626->600 delta); per-file sums equal grand totals; busiest hour recomputed independently from raw logs; stat shows all 6 mtimes unchanged (R6); anomalies.txt format exact.

R8 (6 stated): exclusion-before-anomaly ordering (no overlap in data, checked); ISO = shape regex, all shape-valid lines also calendrically valid; per_file naming kept full filename (app1.log.txt) for uniqueness; level = 2nd token of valid ISO line; ignore.txt parsing rules (comments, blanks, case-sensitive literal); busiest-hour tie-break rule stated (not needed).
