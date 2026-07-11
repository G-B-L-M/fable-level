# End-to-End Debugging: The Mechanism Rule

Read this when a bug has survived one fix attempt, before starting any bug reported
as "weird / flaky / impossible", and whenever you catch yourself guessing.

## The one rule everything else serves

**You are not allowed to change code until you can state the mechanism of the
failure in one sentence.** ("The session is null because the middleware runs before
the cookie parser registers.") Every shortcut around this rule costs more than it
saves. If you cannot state the mechanism, you are still gathering evidence —
that is legitimate work; patching without it is not.

## Phase 0 — Reproduce on demand

- Find the smallest command that shows the failure: one test, one curl, one REPL
  call. Save it verbatim — it is your proof-of-fix later.
- Cannot reproduce → you have a different task: gathering the missing condition
  (data, env, timing, version). Say so; do not fix blind.
- Flaky bugs: run the repro 5–10 times, record the failure rate. Without a baseline
  rate you cannot distinguish "fixed" from "got lucky twice".

## Phase 1 — Read the actual error

- The WHOLE error: the second exception ("caused by"), the middle of the stack, the
  warning three lines above. The first line is where it died, rarely why.
- Distinguish the error's **site** from its **source**. `undefined is not a
  function` at line 40 means a bad value was *born* somewhere else and *arrived*
  at line 40. Trace the value backwards to its birth; fix at the birth.
- Go to the exact file:line named and read 20 lines around it. Not the file you
  assume corresponds to it — the one named.

## Phase 2 — Locate by evidence

- **Instrument, don't stare.** Targeted logging (input values, branch taken, timing)
  at the suspected boundary, run the repro, read the output. One instrumented run
  beats ten minutes of squinting.
- **Bisect the pipeline.** Is the data already wrong at the midpoint? Wrong → bug is
  upstream; right → downstream. Halve again. For regressions, `git bisect` with the
  repro script finds the commit mechanically — no cleverness required.
- **Diff the working case.** Works in A, fails in B → enumerate every difference
  (data, config, order, env, version) and eliminate one at a time.

### E2E: isolate the layer first

For failures spanning a stack (browser → network → server → queue → DB), do not
debug "the app". Establish which layer the corruption enters at:

- Walk the request down the layers, checking the data at each boundary: what did the
  client send (devtools/network log)? What did the server receive (access log,
  entry-point log)? What hit the DB (query log)? The first boundary where reality
  diverges from expectation is where the bug lives — everything downstream is a
  symptom.
- Time-correlate across layers with the request ID / timestamp. In distributed
  failures, "what happened at 14:32:07 in every log" beats reading any single log
  end to end.
- Environment parity check early: same versions, same config, same data shape as
  the environment where it works? "Works locally" bugs are environment diffs until
  proven otherwise.
- Heisenbugs (vanish under observation) are timing/ordering bugs until proven
  otherwise: race, uninitialized read, cache warm-vs-cold. Adding a log changed the
  timing — that is itself evidence.

## Phase 3 — The hypothesis loop

State one falsifiable mechanism sentence, then run the **cheapest test that could
prove it false** — a log line, a reorder in a scratch copy, a controlled unit call.
Not a full fix.

- Confirmed → Phase 4.
- Falsified → excellent, a branch is eliminated; form the next from what the test
  showed.
- No mechanism statable → back to Phase 2; more evidence.

Keep a written scratch list: hypothesis → test → outcome. It prevents re-trying a
falsified idea 20 minutes later, and it is the raw material of an honest escalation
report if you end up stuck.

## Phase 4 — Fix, prove, sweep

1. Fix at the layer where the wrong value/order is **born**, not where it explodes.
2. Re-run the Phase-0 repro and watch it pass. Flaky bugs: as many runs as the
   failing baseline.
3. Run surrounding tests for collateral damage.
4. **Sweep for siblings**: the same wrong pattern usually exists elsewhere. Grep for
   it. Report siblings even when fixing them is out of scope.

## The assumption audit (when three strategies have failed)

One of your assumptions is wrong and it is usually an embarrassing one. Check by
OBSERVING, not reasoning:

1. Is the code I'm editing the code that runs? (build output vs source, deployed vs
   local, right service, right branch, right container)
2. Is my change loaded? (restart, cache, memoized module, correct env, stale bundle —
   quick test: add a deliberate print/crash; if it doesn't appear, nothing you do
   to this file matters)
3. Is the input what I think? (log it at the entry point; never assume it)
4. Is the version what I think? (lockfile, `--version`, node_modules reality)
5. Does the test exercise this path at all? (deliberate crash in the path; test
   still green → it never got there)
6. Does the doc match this version's behavior? (docs drift; the source doesn't)

All six clean → escalate honestly: the repro, the hypotheses eliminated with their
evidence, the audit results. That report is valuable; a cosmetic "fix" is negative
value.

## Anti-patterns — each converts a loud bug into a silent one

- **Shotgun debugging**: several changes at once, re-run, it passes — you learned
  nothing and one of the changes broke something else quietly.
- **Patch-and-pray**: null check / try-except / retry / `?? default` at the crash
  site without knowing why the bad value exists. The crash was the smoke detector;
  the bad value is now corrupting data silently.
- **Cosmetic retries**: same approach, renamed variables. Mechanism unchanged →
  outcome unchanged. Two failures of one approach = the diagnosis is wrong, not
  the syntax.
- **Blaming the platform**: occasionally true, always the LAST hypothesis, and only
  with a minimal reproduction outside your code.
- **Fix-by-deletion**: removing the assertion/test/validation that caught the
  problem. That is destroying the smoke detector and calling the fire out.
- **Fix-by-fallback**: adding a fallback path so the failing path "doesn't matter".
  Now there are two paths, one of them broken, both unowned.
