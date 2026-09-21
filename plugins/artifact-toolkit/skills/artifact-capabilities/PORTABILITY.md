# Portability note — artifact-capabilities

This skill is **not portable in the way the other three plugins are.** Read this before
pasting it into ChatGPT, Grok, or any non-Claude assistant.

## Why

`artifact-capabilities` describes a **runtime that only exists inside claude.ai Artifacts**:
the `window.claude.use(name)` bridge, the `capabilities: {...}` declaration passed to Claude's
own `Artifact` tool, and the consent shell that grants them per viewer. None of that exists in
ChatGPT Canvas, Grok, Gemini Canvas, or a plain browser. Code written against it there will
throw or silently no-op.

Two further limits:

1. **The capability roster is per-account and served live.** The list in `SKILL.md`
   (`artifact`, `assets`, `comments`, `db`, `downloads`, `mcp`, `room`, `sample`, `self`,
   `user`) is what this account was served on 2026-09-21 at contract **0.2.52**. Another
   account may be served fewer. Never treat the snapshot as an entitlement.
2. **The connector id → display-name map is per session.** The live skill prints it fresh each
   session. It is deliberately **not** copied into this pack; hardcoding last session's opaque
   ids into a page breaks it for every viewer.

## What to do instead, per platform

| Platform | Use this skill as |
|---|---|
| **Claude Code / Claude Desktop / claude.ai** | Prefer the **built-in** `artifact-capabilities` skill — it carries the live roster and the live connector map. This copy is a fallback and a diff reference. |
| **ChatGPT / Grok / Gemini / local models** | **Design reference only.** Useful for the *patterns* (when state belongs in the page vs. a store vs. an ephemeral room; degrade-on-`null`; never block first paint on consent). Do not ask the model to emit `claude.use(...)` code. |
| **Any platform, building a real web app** | Map each capability to its ordinary equivalent — see the table below. |

## Capability → ordinary-web equivalent

Use this when porting an Artifact concept to a normal app on another platform.

| Capability | What it does | Ordinary equivalent |
|---|---|---|
| `artifact` | Page republishes itself as the record | Server-rendered page + a save endpoint, or a static site rebuilt on write |
| `db` | JSON doc store outside the page | Firestore / Supabase / any document DB |
| `room` | Ephemeral presence + events among live viewers | WebSocket / WebRTC datachannel / Liveblocks |
| `user` | Who is viewing, within the org | Your auth provider's session + directory lookup |
| `assets` | Per-artifact blob store | S3 / R2 / Supabase Storage |
| `downloads` | Hand the viewer a generated file | `Blob` + `URL.createObjectURL` + `<a download>` |
| `sample` | Page asks the model a question | Your own API route calling a model API, with your key server-side |
| `mcp` | Page calls the *viewer's* connectors | Per-user OAuth to each SaaS, tokens held server-side |
| `comments` | Page writes into the shell's comment store | Your own comment table + UI |
| `permissions` | Lazy per-capability consent | Browser Permissions API / your own consent gate |

The design rules in `SKILL.md` survive the port even when the API does not: declare the
minimum, branch on absence, never block first paint on a permission prompt, treat anything
other viewers wrote as untrusted input, and never put secrets in shared state.
