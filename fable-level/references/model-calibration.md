# Model Calibration: Deploying the Discipline on Any Model or Tool

Read this when installing the fable-level discipline onto a specific model
(Opus 4.8, Sonnet 5, Haiku 4.5, or a non-Claude tool) or when designing the
harness around one.

## The capability ladder (what actually closes the gap)

The gap to Fable-level output closes in six steps, in order. Each step multiplies
the value of the previous; skipping one caps everything above it. This is the
maturity model for any agent system:

1. **Grounding** — the model can observe reality (read files, run commands, make
   real calls) AND is bound by evidence rules (never cite memory as fact, open
   before designing). Tools without the rules = confident tool-assisted
   hallucination. Rules without tools = dead letter.
2. **A runnable check per task** — "done" is defined as a command/observation
   before work starts. Without a check, "looks done" is the only signal any model
   has, and every model's "looks done" fires early (atlas B1).
3. **The verification loop** — the finishing protocol (`verification.md`) runs
   before every "done". This single step converts more mid-tier output to
   senior-tier than any prompt phrasing ever will.
4. **Context economics** — external memory in files, precision loading, compaction
   survival, re-anchoring (`context-engineering.md`). This is what makes long tasks
   possible at all; below this step, quality is capped by session length.
5. **Adversarial self-review** — the ATTACK gate: hostile-reviewer pass, constructed
   failing cases, sibling sweeps. This is what catches the errors verification's
   happy-path misses.
6. **Calibrated reporting** — verified/assumed separation, evidence citations,
   honest incompletion. This is what makes the output *trustworthy* rather than
   merely good, and it is what lets a human safely NOT review everything.

Diagnose any underperforming agent by walking the ladder bottom-up: the first
missing rung is the problem. Do not tune step-6 prose on a system missing step 1.

## The universal transplant rules

Whatever the model, four rules govern how to install the discipline:

- **Standing, not per-message.** The discipline goes in the system prompt /
  rules file / CLAUDE.md-equivalent. Per-message reminders decay and get skipped
  under exactly the pressure that makes them matter.
- **If-then triggers for anything below frontier.** Frontier models generalize
  from principles ("verify before claiming"); mid-tier models need the condition
  and action spelled out ("IF about to write 'done', 'fixed', or 'works' THEN run
  the named check first and paste its output"). When in doubt, write the if-then —
  it costs nothing on strong models.
- **Explain the why behind unusual constraints.** Modern models generalize
  correctly from motivation ("output feeds a TTS engine, so never use ellipses")
  and misapply bare rules.
- **Never filter in the finder.** Any instruction like "only report serious
  issues" depresses recall in the model doing the finding — borderline findings
  get self-censored. Ask for everything; filter in a separate downstream step.

## Claude models

### Opus 4.8 — documented quirks and settings

Opus 4.8 is the strongest non-Fable option and needs the least scaffolding, but has
documented defaults to counter:

- **Literal instruction following**: it won't generalize "rename the button" to the
  three analogous pages. Add: *when an instruction plausibly applies to analogous
  cases, apply consistently and say which you did.*
- **Reasons instead of acting**: answers about files it never opened. Add the hard
  rule: *never speculate about code you haven't opened this session.*
- **Under-spawns subagents / over-asks permission / narrates heavily**: give
  explicit fan-out triggers; add the autonomy snippet (*minor choices: pick and
  note, don't ask*); delete forced-summary scaffolding — it narrates on its own.
- **Context anxiety**: wraps up early to "save budget". Add: *never stop or shrink
  a task for token-budget reasons.*
- **Config**: `effort: xhigh` for agentic coding (never below `high`);
  `thinking: {"type": "adaptive"}` is REQUIRED on the API (no thinking otherwise);
  temperature/top_p and prefills are rejected — steer with prompting.
- **Delete Claude-3.x-era scaffolding**: "CRITICAL: you MUST use this tool",
  anti-laziness prompts, forced progress summaries — all now backfire.

### Sonnet 5 — the discipline is the difference

Sonnet-class models have the raw capability for most tasks; what they lack is the
*unprompted* discipline. The full fable-level pack, stated as explicit if-then
rules, closes most of the visible gap:

- Mandate the loop by name: FRAME before touching, GROUND before designing,
  finishing protocol before "done". Sonnet follows named procedures well; it just
  doesn't invent them.
- Shorter leash on long autonomy: checkpoint to files more often; re-anchor to the
  original request more often (drift onset is earlier).
- Force the two-failure rule mechanically ("after 2 failed fixes, STOP and write
  the assumption audit") — Sonnet's cosmetic-retry loop (atlas C3) is stickier.
- Route genuinely hard forks upward: if a task keeps failing UNDER the discipline,
  that's the escalate-to-a-stronger-model signal. Keep the discipline either way.

### Haiku 4.5 and small/fast models — shrink the task, not the discipline

Do NOT hand a small model the whole method; it will perform the ceremony and miss
the substance. Instead, the discipline lives in the ORCHESTRATOR, and the small
model lives inside one step of it:

- Give it narrow, mechanical, individually-verifiable subtasks with exact
  deliverable formats ("extract every function name from these 12 files into this
  JSON shape") — the kind of task where correctness is checkable by count/diff.
- Verification of its output happens OUTSIDE it, by the orchestrator or a stronger
  model. Never let a small model self-certify.
- Few-shot examples beat abstract rules at this tier: show one perfect input→output
  pair rather than three paragraphs of principle.

## Non-Claude tools (any vendor)

The discipline is model-agnostic — it was designed from failure modes shared by all
current LLMs (see the atlas: those mechanisms are properties of LLM training, not
of any vendor). Deployment recipe:

1. Put SKILL.md's loop + hard lines into the tool's standing-rules channel
   (system prompt, `.cursorrules`/`AGENTS.md`-style file, custom instructions).
2. Convert to if-then form throughout (see transplant rules).
3. Audit the harness against the ladder: does the model have file access, command
   execution, a scratchpad directory, and a way to persist notes? Every missing
   rung caps the result regardless of prompt quality.
4. Add the four highest-value atlas countermeasures first if you must prioritize:
   A1 (no APIs from memory), B1 (runnable check before "done"), C2 (mechanism rule
   before patching), D2 (never weaken a check). These four stop the majority of
   real-world agent damage. If the agent has tool access, Class F (trust
   boundaries — `security-and-trust.md`) is not optional: injected-instruction
   compliance and destructive pattern-matching are where agents cause damage
   rather than merely produce bad output.
5. Calibrate empirically, not by brand reputation: run the same three probe tasks
   (a multi-step build, a planted bug, an ambiguous request) and score against the
   atlas tells. Tune the rules against observed failures — a model's actual quirk
   profile is discovered, not assumed.
6. Re-inject critical rules periodically on long runs if the harness allows it
   (counters atlas E2, instruction decay).

## What no prompt can transfer — harness it instead

Be honest about the residual gap. Below Fable-level raw capability, no prompt
fixes: subtler long-horizon coherence, judgment on genuinely novel problems,
noticing the unasked question. The mitigation is architectural, not prompt-based:

- **Escalation routes**: hard forks and repeated failures route to a stronger model.
- **Independent verification**: a fresh-context checker (stronger or equal model,
  given verbatim requirements + the diff, never the implementer's summary) reviews
  anything shipping without human eyes.
- **Blast-radius limits**: weaker models get reversible sandboxes (branches,
  worktrees, staging) and never hold irreversible permissions directly.
- **Ship gates**: the scorecard (`scorecard.md`) as a mandatory pre-ship gate,
  self-graded below the gate threshold → escalate to fresh-context grading.

A mid-tier model inside this harness ships more reliable work than a frontier
model outside it. That is the entire thesis of this pack, applied to itself.
