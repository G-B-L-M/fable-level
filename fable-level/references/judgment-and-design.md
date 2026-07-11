# Judgment and Design: How Decisions Get Made

Read this when facing a design fork (architecture, approach, interface, library),
when writing new code, or when the task's hard part is choosing rather than
executing. The other references cover working correctly; this one covers deciding
well — the layer where "competent" and "senior" actually diverge.

## 1. The decision protocol

- **Two real options, minimum.** A decision with one option is not a decision; it
  is the first idea wearing a decision's clothes. Generate a genuine alternative
  before committing — if you cannot name the alternative you rejected and why, you
  haven't decided, you've defaulted.
- **Weight by reversibility.** Two-way doors (internal naming, file layout, an
  easily-swapped implementation) get decided in minutes with a reasonable default,
  noted in the report. One-way doors (public API shapes, data schemas, wire
  formats, anything with external consumers or persisted state) get decided
  slowly: evidence gathered, alternative steelmanned, user consulted when the cost
  of wrong is theirs to bear. Most decision-making failure is applying one door's
  process to the other's stakes.
- **Decide with named criteria.** "A over B because we need X and A gives it at
  lower complexity" — one sentence, in the report. Criteria-free decisions get
  re-litigated forever and can't be audited when they turn out wrong.
- A decision that new evidence has invalidated is not sunk cost (atlas C5).
  Reversing a wrong call early is the cheap version of reversing it late.

## 2. Simplicity economics

- **Complexity must pay rent now.** Every layer, option, abstraction, and
  configuration point must justify itself against a requirement that exists
  today. "We might need it later" is a reason to make the change easy later, not
  to build it now — later, you'll know more.
- **The fewest-concepts test**: of the designs that meet the stated requirements,
  prefer the one a newcomer must learn the fewest new concepts to understand.
- **Duplication is cheaper than the wrong abstraction.** Tolerate the second
  copy; abstract at the third, when the true shape of the commonality is visible
  (the rule of three). A premature abstraction forces every future variant
  through a shape chosen before the variants existed.
- Boring beats clever. Clever code optimizes the writing experience; boring code
  optimizes the hundred readings that follow. Cleverness needs a stated reason
  (measured performance, a real constraint) to earn its place.

## 3. Chesterton's fence, operationalized

Before changing existing code you didn't write:

- Assume it is that way for a reason and go FIND the reason: read the callers
  (grep), read the git history of the lines (`git log -p`, blame), read the test
  that pins the behavior. Five minutes of archaeology beats re-learning the
  original bug in production.
- Found a plausible reason → respect it, or argue past it explicitly in the
  report. Found none after looking → change it, and say you looked.
- Match the local idiom even where you'd choose differently: consistency within a
  codebase beats your preference. Diffs that read as the original author's are
  reviewable; style-mixing diffs hide the real change.

## 4. Writing code that reads senior

- **Naming is design.** If a function is hard to name, its boundary is wrong —
  fix the boundary, not the thesaurus. Names state what something IS
  (`pending_invoices`), not its history (`new_helper2`, `data_final`).
- **One altitude per function.** A function either orchestrates steps or performs
  one — mixing wire-level details into an orchestration function is the main
  reason code becomes unreadable. If you must scroll to understand a function's
  shape, it has two jobs.
- **Errors: loud at the boundary, trusted inside.** Validate at the edges where
  data enters (API handlers, file parsers, user input); past the boundary, let
  violated assumptions crash loudly. Silent defaults (`?? []`, `except: pass`,
  fallback values) at interior layers convert bugs into corruption — the smoke
  detector rule from `debugging-e2e.md`.
- Comments only for constraints the code cannot express ("must run before X
  because Y", "the API returns 200 on failure, hence the body check"). Never
  narrate the next line, never explain your change (that's the report's job).
- **Refactor and behavior-change never share a diff.** A mixed diff makes both
  the refactor unverifiable and the change unreviewable. Two commits, or refactor
  in the report as a suggestion.

## 5. The premortem (60 seconds that saves sessions)

Before building anything substantial, one minute on: **"It is a month later and
this failed or caused pain — what happened?"** Answer honestly; the top answers
are usually: the input assumption broke, the scale assumption broke, the
concurrent case, the second consumer, the person who had to modify it. Convert
the top 2–3 answers into either (a) a check in the ATTACK/VERIFY phases or (b) a
named, reported limitation. A premortem is the cheapest form of the adversarial
pass — it runs before the work instead of after.

## 6. Interfaces from the caller's side

Design any API/function/CLI by writing its ideal call site first — the code you
WISH could be written — then implement toward it. Interfaces designed from the
implementation's side leak the implementation: parameters callers must thread
without understanding, orderings only the internals justify. One imagined caller
is the cheapest usability test that exists.

## 7. Choosing tools and libraries

Preference order: what the project already uses → the standard library → a
popular, pinned, verified dependency (see `security-and-trust.md` §5) → writing
it yourself → a novel dependency. Each step rightward is an architecture decision
that outlives the task; each gets one line of justification in the report. The
project's existing choice beats your favorite: consistency is a feature the next
maintainer feels every day.

## 8. Estimation and uncertainty honesty

- Report uncertainty where it is real, as a range or a named risk — not as
  blanket hedging that makes everything sound equally unsure. "This handles up to
  ~100k rows; beyond that the sort needs to move to the DB" is calibrated;
  "should generally scale fairly well" is noise.
- When a task is bigger than the request implies, say so BEFORE starting the long
  road, with the fork: "correct version costs X; quick version costs Y and skips
  Z — which?" Silently choosing either is a scope decision that belonged to the
  user.
