"""Generates probes/p2-data/sales.csv with 5 planted traps and prints ground truth.

Traps:
  1. Header row repeated mid-file (export artifact)
  2. Three amounts in European format ("1.234,56"), quoted
  3. One exact duplicate transaction row (same txn_id -> must count once)
  4. Mixed date formats (ISO and DD/MM/YYYY)
  5. Final line truncated mid-field (must be excluded/reported)

Ground truth = sum of canonical rows, duplicate counted once, truncated row excluded.
"""
import random
from collections import defaultdict
from pathlib import Path

random.seed(7)
REGIONS = ["North", "South", "East", "West"]

canonical = []
tid = 1000
for i in range(28):
    tid += 1
    amount = round(random.uniform(50, 3000), 2)
    day = (i % 27) + 1
    month = (i % 6) + 1
    if i % 2 == 0:
        date = f"2026-{month:02d}-{day:02d}"
    else:
        date = f"{day:02d}/{month:02d}/2026"
    canonical.append((f"T{tid}", date, REGIONS[i % 4], amount))


def eur(a: float) -> str:
    s = f"{a:,.2f}"  # 1,234.56
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


lines = ["txn_id,date,region,amount"]
for i, (t, d, r, a) in enumerate(canonical):
    if i == 14:
        lines.append("txn_id,date,region,amount")  # trap 1: repeated header
    if i in (5, 12, 19):
        lines.append(f'{t},{d},{r},"{eur(a)}"')  # trap 2: European decimals
    else:
        lines.append(f"{t},{d},{r},{a}")
    if i == 8:
        lines.append(f"{t},{d},{r},{a}")  # trap 3: exact duplicate txn
lines.append("T9999,2026-07-0")  # trap 5: truncated final line

out = Path(__file__).resolve().parent.parent / "probes" / "p2-data" / "sales.csv"
out.write_text("\n".join(lines) + "\n")

per_region = defaultdict(float)
for t, d, r, a in canonical:
    per_region[r] += a
grand = sum(per_region.values())

print(f"file: {out}")
print(f"data lines written (incl. traps): {len(lines) - 1}")
print("GROUND TRUTH (canonical 28 txns, dupe once, truncated excluded):")
for r in sorted(per_region):
    print(f"  {r}: {per_region[r]:.2f}")
print(f"  GRAND TOTAL: {grand:.2f}")
