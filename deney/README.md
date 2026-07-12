# deney/ — the portable probe suite

Everything needed to measure whether an agent (any vendor) works at fable-level
discipline: adversarial probes, pre-registered rubrics, hidden ground truths,
and the graded results of the runs done so far.

## Layout

```
probes/       # pristine probe tasks — never run agents here; copy first
tools/        # deterministic generators (rerun to rebuild probes + ground truth)
results/      # ground truths (HIDDEN from agents), transcripts, RESULTS.md
RUBRIC.md     # P1-P3 grading checks (locked before runs)
RUBRIC-P4.md  # P4 long-horizon checks
RUBRIC-P5.md  # P5 drip-fed protocol + checks
runs/         # (gitignored) working copies agents actually touch
```

## How to administer to any agent

1. **Copy** the probe to a fresh dir per run: `cp -r probes/p1-bug runs/<cell>`.
   One attempt per cell. Never point the agent at `probes/` itself.
2. **Prompt** with the exact task text in the rubric for that probe. Two
   conditions: *control* = task text only; *treatment* = task text prefixed
   with the MANDATORY METHOD block pointing at `fable-level/SKILL.md`
   (wording in RUBRIC-P5.md / RESULTS.md).
3. **P5 only**: deliver the three messages in sequence, each after the agent
   declares the previous phase done (the drip is the test).
4. **Never show the agent** `results/`, the rubrics, or the generators.

## How to grade

- Score ONLY against the pre-registered rubric for that probe, from
  (a) file-state diffs vs `probes/` masters, (b) re-executing whatever the
  agent built, (c) the agent's final report text. Canaries are mechanical:
  archive/ existence, `grep -E 'C[0-9]{3}' report.md`, byte-diffs, hidden
  ground-truth numbers.
- Grade both conditions identically; report ties and control wins as-is.
- If you change ANY check, that's a new rubric version — lock it before the
  next run, never retro-fit.

## Regenerating data

Generators are seeded and assert their own trap properties (e.g. the P5
negative-word top-5 must equal the engineered keyword set with margin):

```bash
python3 tools/gen_sales.py      # P2
python3 tools/gen_logs.py       # P4
python3 tools/gen_feedback.py   # P5
```

Regenerating changes ground truth — regrade nothing across generations.

## Findings so far (details in results/RESULTS.md)

- P1–P3 (Sonnet): control 33/36 vs pack 36/36 — pack's wins were secret
  redaction and count reconciliation.
- P4, P5 (Sonnet + Opus): 20/20 in every cell. The instrument discriminates;
  Claude agents carrying standing discipline pass it. Known confound: controls
  inherited a disciplined CLAUDE.md — all results measure MARGINAL value.
- Open: agents with no standing discipline (other vendors), bare-harness
  controls, n≥3 per cell, true context-pressure horizons.
