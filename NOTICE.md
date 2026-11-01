# NOTICE — provenance, licensing, modifications

## Summary

The original skill content in this pack was **written by Anthropic**. Shin (Vo Sy Dung)
packaged and redistributed it and does not claim authorship of those originals.
The 2026-09-22 working draft adds a method developed for Shin's requirements and makes
the specific adaptations listed below. It is not an Anthropic-authored or endorsed method.

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

**Original snapshot:** at commit `c17ae1d6bb6e195a597129964f611c5297e32ccf`, the marketplace
skill bodies and supporting files were copied without modification as described above.

**Working draft 2026-09-22:**

- Added `plugins/productivity/skills/outcome-work-management/SKILL.md`, a draft method
  authored with Codex from Shin's requirements, and `WORK-MANAGEMENT.md` with rationale,
  illustrative examples and its unvalidated operational status.
- Extended that draft with goal formation, selective method routing and explicit
  input/output/decision conditions, including the distinction between ideation and commitment.
- Added the `shin-agentic-work` skills-only Codex/portable package and a bundled copy
  of Shin's existing `nnc-ai-oser` method (its MIT license travels with that skill).
  On 2026-11-01 that copy was replaced by a thin bridge to the current NNC OSER R2
  method; the fixed-team generator (`team.py`), role catalogue and team schema were
  removed in favour of the host's native delegation.
- Codex packaging normalizes copied skill frontmatter by removing Claude-only keys
  and rewrites connector-document links to resources inside the package. It includes
  no configured MCP servers, account connectors or private project records.
- Reworked the outcome method and its design document around agentic execution and
  one current ROOT brief, without manually versioned management documents.
- Adapted Productivity's `task-management`, `start`, and `update` skills to route linked
  planning to the new method, preserve history, reconcile stable IDs and respect acceptance.
- Updated Productivity documentation and package metadata to identify the addition.
- Changed the generated bundle policy and retrieval instructions from verbatim compliance
  to contextual adaptation, evidence and explicit separation of plans from actuals.
- Updated package documentation, generated portable bundles and checksums accordingly.
- Other upstream skill bodies, connector declarations and runtime types remain unchanged.

**Added:**

- `plugins/operations/LICENSE` — the installed `operations` plugin shipped without a LICENSE
  file; the Apache-2.0 text from its sibling plugins was copied in so the license travels with
  every plugin in this pack.
- `.claude-plugin/marketplace.json` — new; makes this repo installable as a marketplace.
- `plugins/artifact-toolkit/` — new packaging of bundled skills, as described above.
- `portable/` — generated flattenings of the skill content. Headings are demoted, relative
  links and `${CLAUDE_PLUGIN_ROOT}` are rewritten to work in a pasted document, and a routing
  header is prepended. The current source skill prose is carried through into each bundle.
- `platforms/`, `tools/`, `README.md`, this file.

**Deliberately excluded:** the per-session connector id → display-name map that the live
`artifact-capabilities` skill prints. Those opaque ids are session-scoped and account-specific;
hardcoding them would be both wrong and needlessly identifying. The skill text here explains
how to obtain the mapping live instead.

## Attribution

- Original skill content: **Anthropic** — <https://github.com/anthropics/claude-code>
- Outcome-work-management method and adaptations: **Shin, with Codex assistance**
- Packaging: **Shin (Vo Sy Dung)**
- Original pack: 1.0.0 (2026-09-21); current local draft: 1.1.0-draft.1 (2026-09-22)

## If you republish this

Keep `LICENSE` and this file. State your own modifications. Do not present the skill content
as your own work, and do not imply Anthropic endorses the repackaging.
