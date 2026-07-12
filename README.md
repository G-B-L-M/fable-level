# fable-level

**The Fable 5 operating discipline as a portable skill — lift any AI agent's
reliability to frontier level.**

A skill file can't transfer raw intelligence. It CAN transfer the four
disciplines that account for most of the visible gap between frontier-model
output and everything below it: epistemic hygiene, context economics,
verification instinct, and calibrated autonomy. This pack writes them down as an
operating loop, twelve hard lines, eleven deep references, and a 100-point
pre-ship scorecard — deployable on Claude (Opus/Sonnet/Haiku) or any other
model via its rules channel.

## What's inside

```
fable-level/
├── SKILL.md                      # the operating loop, hard lines, router
├── CARD.md                       # one-page digest for periodic re-injection
└── references/
    ├── complex-work.md           # decomposition, live plans, long-run survival
    ├── context-engineering.md    # the window as budget, files as memory
    ├── io-analysis.md            # never trust a description of data
    ├── debugging-e2e.md          # the mechanism rule, root-cause protocol
    ├── verification.md           # evidence at the layer of the claim
    ├── judgment-and-design.md    # decisions, simplicity economics, premortem
    ├── security-and-trust.md     # prompt injection, secrets, safe retries
    ├── self-improvement.md       # the error→rule loop that compounds
    ├── scorecard.md              # 100-point pre-ship self-grade
    ├── blind-spot-atlas.md       # 25 failure modes: mechanism → tell → counter
    └── model-calibration.md      # per-model tuning + deployment recipe
deney/                            # validation experiments: probes, pre-registered
                                  # rubrics, ground truths, graded results —
                                  # see deney/README.md to run the suite on ANY agent
```

## Install (Claude Code)

```bash
git clone https://github.com/G-B-L-M/fable-level.git /tmp/fable-level \
  && mkdir -p ~/.claude/skills \
  && cp -r /tmp/fable-level/fable-level ~/.claude/skills/ \
  && rm -rf /tmp/fable-level
```

Then in any session: the skill auto-triggers on non-trivial work, or invoke it
explicitly. Update later by re-running the same command.

## Install (other tools — Cursor, Codex CLI, Gemini CLI, ...)

Paste `fable-level/SKILL.md` (and the references your tasks need) into the
tool's standing-rules channel — `AGENTS.md`, `.cursorrules`, `GEMINI.md`,
system prompt. Full recipe, per-model calibration, and the capability ladder:
`fable-level/references/model-calibration.md`.

## Validation

A/B tested against pre-registered mechanical rubrics (see `deney/results/`):
adversarial probes on Sonnet scored control 33/36 vs pack 36/36, with the pack's
wins exactly in its unique coverage (secret redaction, count reconciliation);
a long-horizon probe on Sonnet + Opus scored 20/20 in all cells (ceiling —
analysis of why, and the confounds, is reported honestly in the results).
Ongoing: bare-model controls, discriminating long-horizon probes, non-Claude runs.

## Türkçe özet

Bu paket, Fable 5'in çalışma disiplinini her modele taşınabilir bir skill'e
döker: kanıt kuralları, doğrulama döngüleri, bağlam ekonomisi, 25 maddelik
kör-nokta atlası ve teslim öncesi 100 puanlık karne. Kurulum yukarıdaki tek
komut; Claude dışı araçlara taşıma tarifi `model-calibration.md` içinde.
Deneyler ve dürüst sonuçları `deney/` klasöründe.

## License

MIT — use it, fork it, ship it.
