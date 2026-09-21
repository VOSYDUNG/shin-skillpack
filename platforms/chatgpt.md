# Load into ChatGPT

ChatGPT has no skill loader, so the pack goes in as instructions + knowledge files. Two
routes, depending on whether you want a reusable GPT or a one-off project.

## Route A — a Custom GPT (reusable, shareable with your team)

1. **Create** → ChatGPT → *Explore GPTs* → *Create* → *Configure*.
2. **Name / Description** — e.g. `Shin Ops Copilot`.
3. **Instructions** — paste `portable/ROUTER-ONLY.md`, then append the retrieval rule below.
   The Instructions field caps at **8,000 characters**; `ROUTER-ONLY.md` is ~6 KB, so it fits
   with room for house rules. A full bundle does **not** fit here — that is what Knowledge is for.
4. **Knowledge** — upload the bundles you want that GPT to have:
   - `portable/operations.bundle.md`
   - `portable/product-management.bundle.md`
   - `portable/productivity.bundle.md`
   - `portable/artifact-toolkit.bundle.md`

   Upload only what that GPT is for. A focused GPT retrieves more reliably than one holding
   all four.
5. **Capabilities** — keep *Code Interpreter* on if you want the skills to produce real
   `.xlsx` / `.docx` deliverables.

Append this to the Instructions so retrieval actually fires:

```
When a request matches a skill in the routing table above, open the matching
*.bundle.md knowledge file, locate that skill's "## Skill: /<name>" section, and
follow it verbatim — including its output template — before answering. Do not
paraphrase the template away. If the skill needs a figure, an owner or a date you
do not have, ask for it instead of inventing one.
```

## Route B — a Project (faster, per-workspace)

ChatGPT Projects take project instructions plus files. Paste one `*.bundle.md` **directly
into the project instructions** if it fits the field; otherwise paste `ROUTER-ONLY.md` there
and attach the bundles as project files. Same retrieval rule applies.

Route B is the better fit when only you use it. Route A is better when several teammates should
get the same behavior.

## What to expect

**Works well.** Every skill's procedure, framework, and output template. `/write-spec`,
`/status-report`, `/risk-assessment`, `/vendor-review`, `/synthesize-research` and the rest
produce the same documents they do in Claude — the value is in the prose, and the prose ports.

**Needs you to paste data.** The `~~` placeholders (`~~project tracker`, `~~chat`, `~~email`)
assume connected systems. ChatGPT's own connectors may cover some of it; otherwise the skill
will ask you to paste the ticket list, the metrics, the interview notes. The bundle header
already instructs the model to ask rather than invent.

**Won't work.** `artifact-capabilities` describes the `window.claude` runtime inside claude.ai
Artifacts — it does not exist in ChatGPT Canvas. Treat that one section as design reference.
`artifact-diagramming` works fine; ChatGPT emits SVG.

**Degrades.** `productivity` assumes files on disk (`TASKS.md`, `CLAUDE.md`, `memory/`).
In ChatGPT, keep those as project files you update, and tell the GPT they are the source of
truth. It cannot write them for you.

## Re-upload after edits

Knowledge files are snapshots. After editing any `SKILL.md`, re-run
`python tools/build_portable.py` and re-upload the changed bundle.
