"""Generates probes/p4-longrun/ (6 log files + ignore.txt) and prints ground truth.

Planted traps:
  - empty.log is 0 bytes (tail case)
  - legacy.log contains 6 non-ISO timestamps (anomalies)
  - ~25 lines contain ignore.txt substrings (must be excluded)
  - hour 14 is boosted so the busiest clock hour is unique
"""
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

random.seed(13)
BASE = Path(__file__).resolve().parent.parent / "probes" / "p4-longrun"
LOGS = BASE / "logs"
LOGS.mkdir(parents=True, exist_ok=True)

LEVELS = ["INFO"] * 7 + ["WARN"] * 2 + ["ERROR"]
MSGS = [
    "user login ok", "cache miss for key K{n}", "payment processed id={n}",
    "queue depth {n}", "retrying connection to shard-{n}", "request served in {n}ms",
    "session expired for u{n}", "disk usage {n}%", "sync complete batch {n}",
    "token refreshed for svc-{n}",
]
IGNORE_SUBSTRINGS = ["healthcheck ping", "keepalive tick"]


def iso_ts():
    day = random.randint(1, 9)
    hour = random.choices(range(24), weights=[1] * 14 + [7] + [1] * 9)[0]
    return f"2026-07-{day:02d}T{hour:02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"


def normal_line():
    lvl = random.choice(LEVELS)
    msg = random.choice(MSGS).replace("{n}", str(random.randint(1, 999)))
    return f"{iso_ts()} {lvl} {msg}"


def ignore_line():
    return f"{iso_ts()} INFO {random.choice(IGNORE_SUBSTRINGS)} ok"


def malformed_line():
    return f"0{random.randint(1,9)}/07/2026 {random.randint(0,23):02d}:{random.randint(0,59):02d} INFO legacy batch ok"


FILES = {"app1.log": 200, "app2.log": 180, "web.log": 220, "worker.log": 150, "legacy.log": 120, "empty.log": 0}

for name, n in FILES.items():
    lines = [normal_line() for _ in range(n)]
    if name != "empty.log" and n:
        for _ in range(random.randint(4, 7)):
            lines.insert(random.randrange(len(lines)), ignore_line())
    if name == "legacy.log":
        for _ in range(6):
            lines.insert(random.randrange(len(lines)), malformed_line())
    (LOGS / name).write_text("\n".join(lines) + ("\n" if lines else ""))

(BASE / "ignore.txt").write_text(
    "# literal substrings, one per line; log lines containing any are excluded\n"
    + "\n".join(IGNORE_SUBSTRINGS) + "\n"
)

# ---- independent ground-truth pass over the written files ----
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2} ")
per_file = {}
anomalies = []
excluded_total = 0
hours = Counter()
totals = defaultdict(int)

for name in sorted(FILES):
    counts = {"INFO": 0, "WARN": 0, "ERROR": 0}
    for lineno, line in enumerate((LOGS / name).read_text().splitlines(), 1):
        if any(s in line for s in IGNORE_SUBSTRINGS):
            excluded_total += 1
            continue
        if not ISO.match(line):
            anomalies.append(f"{name}:{lineno}")
            continue
        lvl = line.split(" ", 2)[1]
        counts[lvl] += 1
        totals[lvl] += 1
        hours[int(line[11:13])] += 1
    per_file[name] = counts

print("GROUND TRUTH P4")
print(json.dumps(per_file, indent=1))
print(f"grand totals: {dict(totals)}")
print(f"excluded_total: {excluded_total}")
print(f"anomalies ({len(anomalies)}): {anomalies}")
top = hours.most_common(3)
print(f"busiest hours top3: {top}")
assert top[0][1] > top[1][1], "TIE at busiest hour — regenerate!"
