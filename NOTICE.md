# NOTICE — provenance, licensing, modifications

## Summary

All skill content in this pack was **written by Anthropic**. Shin (Vo Sy Dung) packaged and
redistributed it; the packager did not author the skills and does not claim copyright in them.

The three marketplace plugins ship under the **Apache License 2.0** — see [`LICENSE`](LICENSE).
Apache-2.0 permits redistribution, including publicly and in modified form, provided the
license and this notice travel with the work and modifications are stated. Both conditions
are met by this file.

## What came from where

| Component | Source | Version | Captured |
|---|---|---|---|
| `plugins/productivity/` | Anthropic marketplace `knowledge-work-plugins` | 1.3.1 | 2026-09-21 |
| `plugins/product-management/` | Anthropic marketplace `knowledge-work-plugins` | 1.2.0 | 2026-09-21 |
| `plugins/operations/` | Anthropic marketplace `knowledge-work-plugins` | 1.3.0 | 2026-09-21 |
| `plugins/artifact-toolkit/` | Claude Code **bundled** skills (not a marketplace plugin) | runtime contract 0.2.52, Claude Code 2.1.275 | 2026-09-21 |

The three marketplace plugins were copied byte-for-byte from the locally installed plugin
directory. `artifact-toolkit` was assembled from Claude Code's bundled skills, which ship
inside the binary rather than as files; its two `SKILL.md` files are transcriptions of the
skill text as served, and `reference/0.2.52/*.d.ts` are the platform-served type definition
files, copied verbatim.

## Modifications made by the packager

Stated as Apache-2.0 §4(b) requires.

**Skill bodies — unmodified.** Every `SKILL.md` under `plugins/productivity/`,
`plugins/product-management/` and `plugins/operations/` is byte-identical to the installed
original, as are their `CONNECTORS.md`, `README.md`, `.mcp.json`, `.claude-plugin/plugin.json`
and `commands/`.

**Added:**

- `plugins/operations/LICENSE` — the installed `operations` plugin shipped without a LICENSE
  file; the Apache-2.0 text from its sibling plugins was copied in so the license travels with
  every plugin in this pack.
- `.claude-plugin/marketplace.json` — new; makes this repo installable as a marketplace.
- `plugins/artifact-toolkit/` — new packaging of bundled skills, as described above.
- `portable/` — generated flattenings of the skill content. Headings are demoted, relative
  links and `${CLAUDE_PLUGIN_ROOT}` are rewritten to work in a pasted document, and a routing
  header is prepended. The skill prose itself is carried through unchanged.
- `platforms/`, `tools/`, `README.md`, this file.

**Deliberately excluded:** the per-session connector id → display-name map that the live
`artifact-capabilities` skill prints. Those opaque ids are session-scoped and account-specific;
hardcoding them would be both wrong and needlessly identifying. The skill text here explains
how to obtain the mapping live instead.

## Attribution

- Skill content: **Anthropic** — <https://github.com/anthropics/claude-code>
- Packaging: **Shin (Vo Sy Dung)**
- Pack version: 1.0.0 (2026-09-21)

## If you republish this

Keep `LICENSE` and this file. State your own modifications. Do not present the skill content
as your own work, and do not imply Anthropic endorses the repackaging.
