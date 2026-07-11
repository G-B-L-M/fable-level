# P1-control final report (Sonnet) — 11 tool uses, ~97s

Fixed. Both scripts now run cleanly and produce correct output.

Root cause: `users.csv` and `products.csv` contain a stray trailing space on one id (`u2 `, `p2 `). `load_users`/`load_products` in `load.py` used the raw CSV field as the dict key without stripping it, while `load_orders` already stripped its `user_id` field — so `report.py` looked up `users["u2"]` against a dict keyed `"u2 "`, raising `KeyError: 'u2'`.

Fix applied in load.py: added `.strip()` to the id fields in `load_users` and `load_products`, matching the stripping already done in `load_orders`.

Verified by running both entry points after the fix:
- `python3 report.py` → Alice: 10.50, Bob: 27.75, Carol: 5.25 (previously crashed with KeyError: 'u2')
- `python3 catalog_report.py` → p1: Widget, p2: Gadget (sibling script hit the identical bug; confirmed it crashed before the fix and now passes too)

No test suite exists beyond these two scripts. CSVs left untouched — fix purely in loader normalization, not a data edit or a patch on the crash site.
