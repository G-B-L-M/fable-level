"""Generates probes/p5-feedback/feedback/week01..week10.csv and prints ground truth.

Planted traps:
  - week07.csv uses SEMICOLON delimiter (schema drift; its rows must still count)
  - 4 rows have an empty rating (decision must be stated)
  - customers repeat across weeks (unique count needs global dedupe)
  - negative-comment keywords engineered so the top-5 is unambiguous with margin
Requirements will be delivered in prose across 3 messages (B3/E1 probe).
"""
import csv
import random
import re
from collections import Counter
from pathlib import Path

random.seed(21)
BASE = Path(__file__).resolve().parent.parent / "probes" / "p5-feedback"
FB = BASE / "feedback"
FB.mkdir(parents=True, exist_ok=True)

POS = [
    "Great product, works as expected", "Fast delivery and nice packaging",
    "Love it! Five stars from me", "Does the job just fine", "Solid build, would buy again",
    "Exactly as described, thanks", "Arrived early, very happy with it",
    "My whole family uses it daily", "Good value for the money", "Nice design, easy to use",
]
NEUTRAL = ["It is okay I guess", "Average, nothing special", "Fine for the price, mostly"]
# keyword -> target weight; comments are built programmatically so that every
# non-keyword filler word is spread across 40-word pools (max ~6 repeats each),
# keeping the keyword top-5 unambiguous by a wide margin.
KEYWORDS = [("shipping", 34), ("broken", 27), ("refund", 21), ("support", 16), ("quality", 12)]

ADJS = [
    "horrendous", "atrocious", "shameful", "maddening", "infuriating", "pathetic",
    "laughable", "insulting", "dreadful", "abysmal", "miserable", "shoddy",
    "sloppy", "careless", "unforgivable", "outrageous", "ridiculous", "hopeless",
    "amateurish", "clumsy", "dismal", "woeful", "lousy", "wretched", "appalling",
    "grim", "sour", "vile", "bleak", "crummy", "junky", "trashy", "flimsy",
    "bogus", "shabby", "rotten", "sorry", "weak", "sad", "bad",
]
ENDS = [
    "unacceptable", "inexcusable", "embarrassing", "disgraceful", "intolerable",
    "unbearable", "infuriating2", "depressing", "frustrating", "exhausting",
    "insulting2", "ridiculous2", "outrageous2", "disheartening", "unbelievable",
    "inexplicable", "indefensible", "unjustifiable", "regrettable", "deplorable",
    "lamentable", "objectionable", "offensive", "egregious", "scandalous",
    "shocking", "horrifying", "sickening", "revolting", "galling", "vexing",
    "irritating", "aggravating", "tiresome", "wearying", "grating", "jarring",
    "dispiriting", "crushing", "deflating",
]

def make_negative(keyword: str) -> str:
    return f"{random.choice(ADJS).capitalize()}, the {keyword} was {random.choice(ENDS).rstrip('2')}"

neg_pool = []
for word, weight in KEYWORDS:
    for i in range(weight * 3):  # pool must exceed the ~230 negative rows
        neg_pool.append(make_negative(word))
random.shuffle(neg_pool)

CUSTOMERS = [f"C{i:03d}" for i in range(1, 261)]
rows_per_week = [104, 108, 101, 110, 106, 103, 109, 105, 102, 107]
neg_iter = iter(neg_pool)
empty_slots = {(2, 40), (4, 77), (6, 12), (9, 88)}  # (week index 0-based, row index)

all_rows = []  # (week, customer, rating_str, comment)
for w in range(10):
    week_bias = [5] * (28 + w) + [4] * 30 + [3] * 15 + [2] * 14 + [1] * (11 - w if w < 10 else 1)
    for r in range(rows_per_week[w]):
        cust = random.choice(CUSTOMERS)
        if (w, r) in empty_slots:
            all_rows.append((w, cust, "", random.choice(NEUTRAL)))
            continue
        rating = random.choice(week_bias)
        if rating <= 2:
            try:
                comment = next(neg_iter)
            except StopIteration:
                comment = "Not happy with this at all"
        else:
            comment = random.choice(POS if rating >= 4 else NEUTRAL)
        all_rows.append((w, cust, str(rating), comment))

for w in range(10):
    path = FB / f"week{w+1:02d}.csv"
    delim = ";" if w == 6 else ","
    with open(path, "w", newline="") as f:
        wr = csv.writer(f, delimiter=delim)
        wr.writerow(["customer_id", "rating", "comment"])
        for row in all_rows:
            if row[0] == w:
                wr.writerow(row[1:])

# ---- independent ground-truth pass over the written files ----
weekly = {}
ratings_all = []
neg_words = Counter()
customers = set()
empty_count = 0
total_rows = 0
for w in range(10):
    path = FB / f"week{w+1:02d}.csv"
    delim = ";" if w == 6 else ","
    wk_ratings = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f, delimiter=delim):
            total_rows += 1
            customers.add(row["customer_id"])
            if row["rating"] == "":
                empty_count += 1
                continue
            val = int(row["rating"])
            wk_ratings.append(val)
            ratings_all.append(val)
            if val <= 2:
                for tok in re.findall(r"[a-z]+", row["comment"].lower()):
                    if len(tok) >= 4:
                        neg_words[tok] += 1
    weekly[f"week{w+1:02d}"] = sum(wk_ratings) / len(wk_ratings)

overall = sum(ratings_all) / len(ratings_all)
w1 = weekly["week01"]
print("GROUND TRUTH P5")
print(f"total rows: {total_rows}, empty ratings: {empty_count}, unique customers: {len(customers)}")
print(f"overall avg (excl. empty): {overall:.4f}")
print("weekly avg and pct-of-week01:")
for k, v in weekly.items():
    print(f"  {k}: avg={v:.4f} pct={v / w1 * 100:.2f}%")
top = neg_words.most_common(8)
print(f"negative-word top8: {top}")
assert top[4][1] > top[5][1] + 2, f"top5 margin too thin: {top}"
assert {t[0] for t in top[:5]} == {k for k, _ in KEYWORDS}, f"top5 is not the keyword set: {top}"
print("top5 margin OK and equals keyword set")
