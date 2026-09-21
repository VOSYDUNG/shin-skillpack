# Portable bundles

Generated files — **do not edit them by hand.** Edit `plugins/<name>/skills/<skill>/SKILL.md`
and re-run:

```bash
python tools/build_portable.py
```

## What's here

| File | Size | Paste it where |
|---|---|---|
| `ROUTER-ONLY.md` | ~6 KB | A standing instruction field with a tight budget (ChatGPT Custom GPT "Instructions", Grok custom instructions, a system prompt). Lists every skill and when to use it, but not the procedures. |
| `productivity.bundle.md` | ~24 KB | One domain at a time — a Project, a Custom GPT knowledge file, or straight into a chat. |
| `product-management.bundle.md` | ~111 KB | ” |
| `operations.bundle.md` | ~27 KB | ” |
| `artifact-toolkit.bundle.md` | ~22 KB | ” (see the portability caveat below) |
| `NNC-ALL-IN-ONE.bundle.md` | ~184 KB | A knowledge file or Project doc where the whole pack should be available at once. Too large for most "instructions" fields. |

## The two patterns

**Pattern A — everything in the instruction field.** Works where the budget allows (Claude
Projects, a long system prompt). Paste one `*.bundle.md`. The model then has the full procedure
and output templates in context for every turn.

**Pattern B — router in instructions, bundles as knowledge.** Works where the instruction field
is small (ChatGPT Custom GPTs cap Instructions at 8,000 characters). Paste `ROUTER-ONLY.md` as
the instructions and upload the `*.bundle.md` files as knowledge/retrieval files. Add this line
to the instructions so retrieval actually fires:

> When a request matches a skill in the routing table, open the matching `*.bundle.md`
> knowledge file, find that skill's `## Skill:` section, and follow it verbatim — including
> its output template — before answering.

Pattern B is more fragile (retrieval can miss), so prefer Pattern A when the budget allows.

## What survives the port, and what doesn't

**Survives everywhere.** The procedures, the frameworks, the output templates, the questions
each skill asks before producing a document. This is the bulk of the value and it is plain
prose — any competent model follows it.

**Needs a substitute.** The `~~category` placeholders (`~~project tracker`, `~~chat`,
`~~email`, …) mean "whatever tool the user has connected in that category." On a platform with
no connectors, the skill should ask the user to paste the data instead. Each bundle's header
rule 4 already instructs the model to do that.

**Does not port.** `artifact-toolkit`'s `artifact-capabilities` skill describes the
`window.claude` runtime, which exists only in claude.ai Artifacts. Outside Claude it is design
reference, not runnable API. `artifact-diagramming` in the same bundle *is* fully portable.
See `plugins/artifact-toolkit/skills/artifact-capabilities/PORTABILITY.md`.

`productivity` assumes a working directory with `TASKS.md`, `CLAUDE.md` and a `memory/`
folder. On a chat-only platform there is no filesystem: the model should keep those documents
in the conversation or in a Project doc the user maintains, and say so rather than pretending
to write files.
