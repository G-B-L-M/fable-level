# P4-opus-control final report — 8 tool uses, ~332s

Built analyze.py, ran, cross-verified. R7: INFO 600, WARN 176, ERROR 94; excluded 26; busiest hour 14 (205, confirmed unique via independent shell count). Anomalies 6 (legacy.log DD/MM/YYYY).

Consistency: 870 + 26 + 6 = 902 raw lines all accounted; excluded lines all INFO, exactly explaining 626->600 delta.

Produced: analyze.py, per_file/<basename>.txt ×6 (empty.log.txt all zeros), anomalies.txt (6 records), summary.json. logs/ only read (R6).

R8 (6 stated): exclusion-before-anomaly ordering; strict ISO shape + strptime calendar validation; anomaly filename = basename; level = 2nd token; tie-break to lowest hour (unneeded); per_file naming legacy.log.txt.
