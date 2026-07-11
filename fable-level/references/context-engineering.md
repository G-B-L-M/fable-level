# Context Engineering: The Window as a Budget, the World as Memory

Read this on long sessions, before broad exploration, when compaction is coming,
or when you notice the session getting confused about things it once knew.

## The core model

The context window is not a notebook; it is **attention budget**. Every token in it
competes with every other token for influence over the next decision. Three
consequences follow, and everything in this file derives from them:

1. **Context rot is real.** As the window fills, retrieval of any specific fact from
   it degrades — not to zero, but enough that a rule read 80k tokens ago no longer
   reliably shapes behavior. Long context ≠ long attention.
2. **Wrong tokens are worse than missing tokens.** A missing fact triggers a lookup;
   a wrong "fact" sitting in context gets silently retrieved and built upon. Context
   poisoning — an early bad assumption, a hallucinated detail, a stale plan —
   compounds, because the model trusts its own transcript more than it should.
3. **The filesystem is free.** Files persist, don't compete for attention, don't
   decay, and survive compaction. Anything that must outlive the next 50 tool calls
   belongs in a file, not in the conversation.

## Loading: precision over volume

- Read the *part* of the file you need, not the whole file. Know what question
  you're asking before you open anything; a read without a question is noise intake.
- For broad sweeps ("where is X handled across the repo?"), delegate to a search
  subagent and keep only the conclusion. The transcript of 40 file excerpts is
  exactly what context isolation exists to keep out of your window.
- Never paste large data into context to "look at it". Sample it: head, tail,
  a random slice, a count. Write the full data to a file and query it with tools.
- Resist completionism. "I should read everything first" is a budget-burning
  disguise of not knowing what you're looking for. Ground the load-bearing unknowns;
  skip the rest until a specific question demands it.

## The freshness hierarchy

When sources conflict, trust in this order — and notice that your own memory is last:

1. Tool output you observed **this session** (and the more recent, the better)
2. The current content of files on disk
3. What the user stated this session
4. Project documentation (which drifts from the code it describes)
5. Your training memory (a hypothesis generator, never citable)

Corollary: when the session's earlier statements conflict with a fresh tool result,
the tool result wins — *including when the earlier statement was yours.* Models
defend their own prior output as if it were ground truth; it is just old cache.

## Anti-poisoning protocol

- When confused, do not reason harder over the transcript — re-verify from source.
  Confusion late in a session usually means something false entered context early
  and has been load-bearing ever since.
- Mark speculation AS speculation when you write it ("hypothesis:", "unverified:").
  Future-you retrieving the sentence will otherwise read it as fact — the label is
  a message to your own later self.
- After discovering an earlier belief was wrong, say so explicitly and restate the
  correction. An uncorrected wrong statement stays retrievable; the explicit
  correction is what competes with it.
- Never re-litigate decided things and never re-derive established facts — but DO
  re-verify when the cost of being wrong is high and the "fact" was established
  long ago in context-time.

## External memory: files as the real state

- Plans, decisions with their reasons, eliminated hypotheses, reproduction commands,
  progress state — into files at natural boundaries. Conversation is cache; files
  are storage.
- Write checkpoints BEFORE risky or long operations, not after. The checkpoint you
  meant to write after is the one that doesn't exist when things go wrong.
- The resumability test: a fresh instance with only the files resumes in two minutes
  without repeating work or re-making decided decisions. If it couldn't, the notes
  are missing the *reasons* — bare decisions without reasons get re-litigated.
- Convert relative to absolute at write time: "tomorrow" → the date, "the latest
  version" → the number, "the file we discussed" → the path. Notes are read without
  the conversation that made the shorthand meaningful.

## Compaction survival

When the harness summarizes the conversation, what survives is the summary plus
files. Design for it:

- Assume any detail not in a file will be lossily compressed. The three things
  compaction loses most: exact commands, exact error text, and the *reason* behind
  a decision. Those three go in files as a rule.
- After a compaction, re-read your own checkpoint files and the original request
  before continuing. The summary tells you what you were doing; the files tell you
  what is true.
- Do not wrap up early or shrink scope because the context is getting long. That is
  the harness's problem to manage, not a reason to degrade the work.

## Instruction decay and re-anchoring

- Standing rules (system prompt, CLAUDE.md, this skill) shape behavior strongly at
  token 1k and weakly at token 150k. At every major boundary — phase finished,
  approach changed, about to declare done — re-read the original request verbatim
  and re-skim the standing rules.
- Context drift produces its own anesthesia: the drifted task feels like the real
  task. No internal signal fires. Only mechanical re-reading of the source text
  catches it, which is why it must be a scheduled habit, not a felt need.

## Budgeting the turn

- Independent tool calls go in ONE message, in parallel: multiple reads, read+test,
  multiple greps. Serial-by-default doubles wall-clock time and doubles the context
  spent on turn overhead.
- Don't fill the window with what you'll immediately discard: pipe through `grep`,
  `head`, `wc -l`; ask for counts before contents.
- Between tool calls, keep narration to load-bearing findings and direction changes.
  Everything the user needs must be restated in the final message anyway — interim
  narration is for signal, not process journaling.
