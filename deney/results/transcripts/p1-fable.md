# P1-fable final report (Sonnet) — 11 tool uses, ~90s

Fixed. `python3 report.py` now runs cleanly and produces correct output.

**Root cause**: In `load.py`, `load_users()` read the `id`/`name` fields from `users.csv` without stripping whitespace, while `load_orders()` (same file) already does `.strip()` on `user_id`/`order_id`. `users.csv` has a row `u2 ,Bob` with a trailing space in the id column, so `load_users()` produced the key `"u2 "` while `load_orders()` produced the clean key `"u2"` from `orders.csv`. The lookup `users[o["user_id"]]` in `report.py:9` then raised `KeyError: 'u2'`.

**Fix**: in `load_users()`, changed `users[row["id"]] = row["name"]` to `users[row["id"].strip()] = row["name"].strip()`. This matches the stripping convention `load_orders()` already uses — a one-line, in-idiom fix rather than editing the CSV data or adding a broad sanitization layer.

**Verification**: Reproduced the crash first (`KeyError: 'u2'`, traceback at `report.py:9` → `load.py`), applied the fix, re-ran the identical command:
Alice: 10.50 / Bob: 27.75 / Carol: 5.25, exit code 0.
Checked the numbers by hand against `orders.csv`: Alice=10.50 (o1), Bob=20.00+7.75=27.75 (o2+o4), Carol=5.25 (o3) — all correct.

Note (not fixed, out of scope): `products.csv` has the identical trailing-space issue on `p2 ,Gadget`, and `load_products()` has the same unstripped-key bug. It doesn't affect `report.py`, but `catalog_report.py` would hit the same `KeyError` if run — flagging it since the task was scoped only to `report.py`.
