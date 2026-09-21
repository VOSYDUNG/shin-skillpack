# Load into claude.ai (Projects) and Claude Desktop chat

Distinct from Claude Code: claude.ai Projects take **project instructions** plus **project
knowledge**, not plugins.

## Projects

1. claude.ai → *Projects* → *Create project*.
2. **Set project instructions** — paste one `portable/*.bundle.md`. Claude's instruction
   budget is generous; a single domain bundle (24–111 KB) fits comfortably and behaves better
   than retrieval because it is always in context.
3. **Project knowledge** — add the other bundles as files if that project needs more than one
   domain, or add `portable/SHIN-ALL-IN-ONE.bundle.md` and keep instructions short with
   `ROUTER-ONLY.md`.

One project per domain beats one project holding everything: `Operations`,
`Product`, `Productivity`. The model routes better with less to route through.

## Claude Skills (claude.ai capability, where enabled)

If your claude.ai account has custom Skills enabled, upload each skill folder directly rather
than pasting bundles — you get the same progressive disclosure Claude Code has. A skill folder
is `SKILL.md` plus whatever it references:

```
plugins/operations/skills/status-report/
plugins/product-management/skills/write-spec/
plugins/artifact-toolkit/skills/artifact-diagramming/
```

Zip the individual skill folder and upload it. Skills that reference `../../CONNECTORS.md`
need that file alongside, or paste the connector table into the project instructions once.

## Connectors

claude.ai connectors (Gmail, Google Drive, Google Calendar, Slack, Notion, …) are authorized in
**Settings → Connectors**, not in this pack. The `~~` placeholders resolve to whatever you have
connected. Nothing in this repo grants access to anything.

## Org context note

These four plugins are generic — Anthropic wrote them for a generic knowledge worker. They do
**not** know your org's channels, its reporting-scope rules, or its language requirements.
Keep your own org-context skill or instructions loaded **alongside** the bundle, not instead
of it: the bundle supplies the procedure, your org
context supplies the facts and the tone.
