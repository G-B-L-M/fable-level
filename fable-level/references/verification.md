# Verification: Evidence at the Layer of the Claim

Read this before declaring ANY substantial task complete. Feeling confident is not
a reason to skip it — confidence is precisely when verification pays, because
confident errors ship and hedged errors get caught.

## The evidence hierarchy

Every belief you hold sits at one of three levels. Never report a belief at a
higher level than it holds:

1. **Observed** — you executed it this session and watched the result.
2. **Derived** — it follows logically from observed facts (and the derivation
   could be wrong).
3. **Remembered** — training data, docs read long ago, "how it usually works".

Claim language maps directly: "verified X by running Y" (observed), "X should hold
because observed-A and observed-B" (derived, labeled), "unverified: Z" (remembered
or unchecked). The phrase "should work" is banned — it is the exact signature of a
remembered belief wearing observed clothing. When you catch it forming, verify
instead or say what's unverified and why.

## The finishing protocol (run in full, in order)

1. **Requirements audit.** Re-read the ORIGINAL request verbatim — not your memory
   of it. List every explicit requirement, then the implicit ones (project
   conventions, standing rules, the obviously-intended-but-unstated). Check each
   off against the actual work. The single most common completion failure is
   silently dropping requirement 3 of 4 — not doing anything wrong, just not doing
   part of it.
2. **Fresh-eyes diff.** Re-read the full diff as a stranger: leftover debug prints,
   TODOs, unused imports, accidental deletions, hardcoded paths/values, files
   changed that shouldn't be. Your diff should look like the original author wrote it.
3. **Run the claim-layer check** (table below) for every claim in your report-to-be.
4. **Adversarial pass.** Hostile-reviewer role: construct the input/state/reading
   that breaks this, and RUN it. Boundaries, empties, duplicates, the concurrent
   case, the second invocation.
5. **Only then report** — and the report distinguishes observed / derived /
   unverified explicitly.

## Claim → minimum evidence

| The claim | The minimum evidence |
|---|---|
| "Fixed" | Reproduced the failure, applied fix, re-ran the SAME repro, watched it pass |
| "Tests pass" | Ran them this session; and the test can fail (made it fail once, or it predates the fix and failed then) |
| "Implemented X" | The code path executes — a test, a REPL call, a real invocation. Compiles ≠ executes |
| "The page/UI works" | Looked at rendered output (screenshot read as an image), exercised the interaction |
| "Handles all N items" | Counted: input = output + explained-skips |
| "Doesn't break anything" | Ran the surrounding suite / found and checked the callers (grep) |
| "Config/deploy is correct" | Observed the running system reflect it, not just the file containing it |
| "Data migrated correctly" | Diffed samples before/after, reconciled counts, checked the weird rows |

Two universal upgrades: prefer evidence **you did not generate** (re-open the file,
independent recomputation, a different tool's view), and **sample the tails** —
first, last, weirdest — never just a happy-path middle item.

## Tests: trust nothing green until it has been red

- A test that has never failed proves nothing about your change. Cheapest check:
  break the code deliberately, watch the test fail, restore, watch it pass. Ten
  seconds, and it catches the two silent killers: the test that doesn't run your
  path, and the mock that swallowed the behavior.
- A suite that passes *surprisingly* fast or clean → suspect collection: did it
  actually run the affected tests? Read the count.
- Test the behavior asked for, not the implementation you wrote — implementation-
  mirroring tests pass forever and catch nothing.

## The suspicious-cleanliness rule

Any surprisingly good result is a broken verification until explained: zero
findings, all green first try, zero conflicts, empty error log. The explanation
must be positive ("clean because X, confirmed by Y"), not absence-shaped ("no
errors appeared"). Bad news self-scrutinizes; good news gets banked unexamined —
so good news needs the deliberate second look.

## Verifying non-code work

The same layers apply outside code:

- **Research/claims**: every factual claim traces to a source you opened this
  session, or is labeled as inference/memory. Numbers get recomputed, not quoted
  from your own earlier message.
- **Documents/reports**: the zero-context read (would a stranger to this session
  understand and be able to act?); every file path, command, and number in it
  re-checked against reality at write time, because reality moved during the session.
- **Configuration/infra**: the system's observed behavior, not the file's contents,
  is the claim layer. "The config file says X" verifies nothing about what's running.

## Independent verification

For large or unreviewable work, have a fresh context check it: a verifier subagent
given the VERBATIM original requirements and the diff — never your summary or your
reasoning, which would contaminate it with exactly the assumptions it exists to
catch. You grade your own work with the same eyes that made the mistakes; fresh
eyes are the only ones that don't share your blind spots this session.

## Honest incompletion

Partial success reported honestly beats fake complete success, every time and
without exception. "Done: A, B. Not done: C, blocked on X. Unverified: D, because
no test covers it" is a report the user can act on. A false "all done" costs them
the failure PLUS the discovery PLUS the trust. If the task as specified seems
wrong or impossible — say that. Do not game it.
