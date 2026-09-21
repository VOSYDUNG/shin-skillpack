# Artifact Toolkit

Two skills for authoring Claude Artifacts well.

| Skill | Use it when |
|---|---|
| **artifact-capabilities** | Before writing a page that needs runtime behavior static HTML can't provide — remembering what people do on it, shared state across viewers, reading connected data, knowing who is viewing, asking Claude a question, storing or handing over files. |
| **artifact-diagramming** | Before drawing any diagram in an artifact — deciding whether a picture earns its place, and the inline-SVG mechanics that keep it legible in light and dark. |

## Provenance and status

These are **snapshots of Claude's built-in (bundled) skills**, captured 2026-09-21 from
Claude Code **2.1.275**, runtime contract **0.2.52**. They are not marketplace plugins —
they ship inside the Claude Code binary — so they were extracted rather than copied from a
plugin directory. They are packaged here so the knowledge travels with the rest of the pack.

**Inside Claude, prefer the built-in skills.** They carry the live capability roster and the
live per-session connector map; this copy cannot. Use this one when you are outside Claude,
when you want a stable reference to diff against, or when the built-ins are unavailable.

## Portability

`artifact-diagramming` is **fully portable** — the "what to draw" rules and the inline-SVG
mechanics apply to any assistant that can emit SVG. Load it anywhere.

`artifact-capabilities` is **reference-only outside Claude**. The `window.claude` runtime it
describes exists only in claude.ai Artifacts. See
[`skills/artifact-capabilities/PORTABILITY.md`](skills/artifact-capabilities/PORTABILITY.md)
for the capability → ordinary-web mapping to use when porting the ideas elsewhere.

## Contents

```
skills/
├── artifact-capabilities/
│   ├── SKILL.md
│   ├── PORTABILITY.md
│   └── reference/0.2.52/     ← 12 platform-served .d.ts files, verbatim
└── artifact-diagramming/
    └── SKILL.md
```

The `.d.ts` files under `reference/0.2.52/` are the authoritative call contract for that
runtime version — read `claude.d.ts` and `mcp.d.ts` before writing capability code.
