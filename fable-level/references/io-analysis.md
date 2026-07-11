# Input/Output Analysis: Never Trust a Description of Data

Read this before consuming any unfamiliar input (file, API, dataset, user-provided
artifact) and before trusting any output you produced.

## The prime rule

**A description of data is a claim about data, not the data.** The user's
description, the API docs, the schema file, the column names, your memory of the
format — all claims. The only fact is the bytes. Open them before building on them.

The costliest sessions all share one shape: an hour of correct logic built on a
ten-second-checkable false premise about the input.

## Analyzing inputs

### First contact protocol (any new file/dataset/API)

1. **Size and shape first**: `wc -l`, row count, file size, number of keys. Decides
   whether you sample or read whole, script or hand-process.
2. **Head AND tail AND a random middle slice.** Files change format partway through:
   headers repeat, a second section starts, the last line is truncated, the export
   tool appended a summary row. The head lies about the tail.
3. **The weirdest item.** Sort by length, find nulls, find duplicates, find the row
   with the most/fewest fields. The weird item is the one your code will crash on
   at item 34,812 — meet it now.
4. **Count what you'll depend on.** If the plan assumes one record per user, verify:
   `cut -d, -f1 | sort | uniq -d`. Assumed uniqueness is the classic silent killer.
5. **Encodings and formats**: UTF-8 vs Latin-1 (Turkish text breaks loudly here),
   `\r\n`, date formats (is `03/04` March or April?), decimal comma vs point,
   timezone-naive timestamps, numbers stored as strings, `"null"` the string vs
   null the value, empty string vs missing key.

### APIs and libraries

- Verify the signature against the **installed** source, not memory: read the type
  definitions in node_modules / site-packages, check the lockfile version, run
  `--help`. Training memory of fast-moving libraries is reliably stale, and it
  fails confidently, not loudly.
- Make one real call and read the actual response before designing the consumer.
  Pagination, envelope wrappers (`{"data": ...}`), error-as-200, rate-limit
  headers — none of these appear in your imagined response.
- Probe error behavior deliberately once: what does a 404 / empty result / malformed
  request actually return? The error path is half the integration and the half
  nobody probes.

### User-provided inputs

- Requirements hide in artifacts: a screenshot contains the actual error text;
  a "roughly like this" example encodes format expectations the prose never states.
  Extract them explicitly and add them to the requirement list.
- Convert every relative reference to absolute before it enters your plan:
  "the new file" → which path, "yesterday" → which date, "the latest run" → which ID.

## Analyzing outputs

### Verify at the layer of the claim

Exit code 0 proves the process ran. Each claim needs evidence from its own layer:

| Claim | Minimum evidence |
|---|---|
| "The script processed the data" | Output file exists AND has ~expected row count |
| "The output is correct" | You read a sample of the output and checked it against the input |
| "The page renders" | Screenshot, read as an image — not "the server returned 200" |
| "The test passes" | You watched it pass AND confirmed it exercises your change (make it fail once) |
| "All N items were handled" | You counted; input count reconciles with output count + skipped count |
| "The migration is safe" | You ran it against a copy and diffed |

### Numerical sanity

- Reconcile totals: input rows = output rows + filtered rows, and you can name the
  filtered ones. An unexplained delta of 3 is a bug you haven't met yet.
- Orders of magnitude: does the aggregate pass the smell test against a known
  anchor? A "daily average" larger than the total is caught by arithmetic, not
  by re-reading code.
- Spot-check by independent path: verify one output item by computing it a
  different way (by hand, by a one-liner, by a different tool). One independent
  confirmation is worth fifty same-path re-runs.

### Sample the tails, always

First item, last item, weirdest item — never just item one. Off-by-one lives at
the boundaries; encoding bugs live in the weird item; truncation lives at the tail.
The middle of the output is where bugs are least likely and where lazy verification
always looks.

### The suspicious-cleanliness rule

A result that is *too* good — zero errors on first run, every test green, perfectly
uniform output — is a broken verification until explained. Common explanations:
the test never ran your code, the filter excluded everything, the loop ran zero
times, you checked the wrong file. Find the explanation ("it's clean because X,
which I confirmed by Y") or keep digging. Good news requires MORE scrutiny than
bad news, because bad news gets scrutinized by default and good news gets banked.

### The zero-context test

Before shipping any user-facing output, re-read it as someone with none of this
session's context: no knowledge of the codenames you invented, the dead-ends you
explored, or the shorthand you developed. Would they understand it and be able to
act on it? If a sentence needs the session to make sense, rewrite it in place.
