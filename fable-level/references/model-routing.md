# Model Routing: Escalate on Difficulty, Downshift on Mechanics

Read this when deciding which model should do a piece of work — delegating
subtasks, structuring an agent pipeline, or noticing that an expensive model is
doing cheap work (or a cheap one is failing at expensive work). The goal:
spend strong-model tokens ONLY where strong-model judgment changes the outcome.

## The economics, honestly

Most tokens in real sessions are spent on work that does not need the biggest
model: file reads, bulk edits by pattern, extraction, formatting, test runs,
first-draft prose. Routing that down saves real money. But the asymmetry
matters: **a wrong cheap answer usually costs more than the strong model would
have** — you pay for the wrong work, the discovery, and the redo. So the router
never optimizes tokens alone; it optimizes tokens *subject to* the discipline
holding at every rung.

## Route by task property, not task name

Four questions decide the rung; ask them per subtask, not per project:

1. **Is correctness mechanically checkable?** (count, diff, test, schema)
   Checkable → safe to downshift, because verification catches a cheap failure.
   Judgment-checkable-only → stay high.
2. **What is the blast radius?** Reversible sandbox → downshift OK.
   Irreversible/outward-facing (delete, send, publish, migrate) → the ACTION
   never routes down, whatever produced the plan.
3. **Is it novel?** Pattern-following (do X to these 40 files like this
   example) → down. Deciding WHAT the pattern should be → up.
4. **Has it failed before?** Any subtask that already failed once at a rung
   routes UP, never sideways. Retrying at the same rung with new wording is
   atlas C3 (cosmetic retry) wearing a cost-saving costume.

## Downshift catalog (delegate to the cheaper model)

- Mechanical transforms with a verifiable spec: extraction into a fixed schema,
  renames across files, format conversions, boilerplate from a template.
- Fan-out over independent items (N files to summarize, N endpoints to probe) —
  spawn ALL in parallel; the orchestrator merges and verifies.
- Broad search/reconnaissance where only the conclusion matters.
- First drafts the strong model will review anyway — drafting is cheap to
  check, expensive to produce.

**The iron rules of downshifting:**
- The cheap model NEVER self-certifies. Verification runs upstairs (orchestrator
  or a stronger model), against the deliverable, per `verification.md`.
- Give it the task spec of a competent stranger: exact deliverable format,
  constraints, one perfect input→output example (few-shot beats principles at
  the low rungs — see `model-calibration.md`).
- Downshift the WORK, never the FRAME: the orchestrator defines done, slices
  the task, and owns the requirement list.

## Escalation triggers (route up, immediately)

- Two failed fixes under the discipline → the diagnosis is beyond this rung.
- Verification keeps failing after the work "looks right".
- A one-way-door decision surfaced (schema, public API, irreversible action).
- The adversarial pass found a problem this rung can't resolve.
- Scorecard below the ship gate twice on the same deliverable.
- The task itself is judgment-dense from the start (architecture, debugging a
  mechanism, ambiguous requirements) — start high; downshifting the hard core
  to save tokens is atlas B4 (scope shrinkage) applied to quality.

**Escalation hygiene:** when escalating, hand up the EVIDENCE, not the failed
transcript — the reproduction, hypotheses eliminated, constraints discovered.
Feeding the stronger model the weaker model's confusion wholesale poisons the
fresh context you are paying for (atlas E4).

## Mechanics in Claude Code

- The main session model is user-chosen (`/model`); an agent cannot hot-swap
  itself. Automatic routing therefore lives in DELEGATION: keep the strong
  model as orchestrator and pass `model: haiku|sonnet|opus` per subagent —
  cheap rungs for the downshift catalog, strong rungs for review/verification.
- Fan-out: spawn all parallel subagents in one turn, cheapest model that
  clears the checkability bar.
- Escalation of the MAIN thread is the user's call: say it plainly ("this fork
  needs a stronger model; switch /model or let me route it to an opus
  subagent") rather than grinding at the wrong rung.

## Mechanics for API/harness builders (the cascade)

1. Route the request to the cheap rung with the runnable check attached.
2. Verify mechanically (tests, schema, counts) — never by asking the same
   model "are you sure".
3. On failure: escalate one rung WITH the evidence summary; cap at two
   escalations, then surface to a human.
4. Budget guard: hard token/cost ceiling per rung so a stuck cheap loop can't
   silently outspend the strong model it was avoiding.
5. Log rung + outcome per task; re-tune the routing table from observed failure
   rates, not vibes (same empiricism as `model-calibration.md` step 5).

## Anti-patterns

- **Ping-pong routing**: down, fail, up, "fixed", down again for the retry.
  Once a task escalates, it stays escalated for its remaining lifetime.
- **Downshifting verification**: the checker must be ≥ the rung of the work,
  or mechanical. A cheap model approving a cheap model is nobody checking.
- **Downshifting the irreversible step**: plans can come from anywhere; the
  delete/send/migrate executes at the top rung or behind a human.
- **Token anxiety as router**: shrinking or downshifting because the session
  feels expensive is hard line 9. The router runs on task properties, not fear.
- **Skipping the loop at low rungs**: routing changes WHO works, never HOW.
  Every rung still runs FRAME→…→REPORT scaled to its slice.
