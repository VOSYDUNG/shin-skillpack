---
name: shin-agentic-work
description: Run a project through goal formation, outcome planning, bounded execution with the host's native delegation, and evidence review. Use when the user wants an agentic workflow with a clean ROOT context and one current project brief.
---

# Shin Agentic Work

Combine [outcome-work-management](../outcome-work-management/SKILL.md) for deciding
what useful result to pursue with [nnc-ai-oser](../nnc-ai-oser/SKILL.md), the bridge to
the NNC OSER R2 method (Mission formation, adaptive delivery, kernel state and evidence).
Read the first when shaping work; read the second when a durable Mission, authority or
evidence trail matters. Both are bundled in this plugin.
Use the user's language. Agentic execution is the preferred method for substantial
independent work; keep trivial or tightly dependent work local.

## Start from the current source

Read the project's instructions and its designated current ROOT brief (default
`docs/ROOT.md`). Use that document as the single coordination entry point. It links
to the small set of authoritative goal/acceptance/architecture documents; read only
the source slice necessary for the decision. Do not reload all agent logs, historical
reports or whole repositories. Existing source-of-truth files retain their authority.

If there is no ROOT brief, synthesize a current one from existing sources. If a goal
is unresolved, choose a suitable discovery method with outcome-work-management.
If the goal is already settled, proceed to the next unresolved decision rather than
reopening it. Do not manufacture a new quarterly OKR merely to set up this workflow.

## Allocate execution

Choose direct work, tools or delegation per task. Use the host's native subagent
mechanism as its own documentation and the current session actually provide it. There
is no fixed roster, role list, model profile or global concurrency cap to set up first;
any existing project agent configuration is the project's own choice, not a requirement
of this workflow. Read available models, slots and permissions from the session; do not
guess model IDs or change global model settings. The user's selected model remains ROOT.
Missing capability/usage data stays unknown.

Coordinate by events. Dispatch a ready package when its inputs are available, continue
independent local work, and consume the agent's completion/blocker message when delivered.
Do not poll agent status, loop over read/list/status calls, or sleep-and-retry to wait.
If nothing independent remains, use a single supported event wait/yield; resume only
on a completion, blocker or user event. A timeout is not a completion and is not a reason
to start a waiting loop. New dependent assignments are triggered by the received result.

A bounded assignment states: useful output, reason, method, source/commit, owned
files or graph nodes, dependencies, exclusions, acceptance, actual model/effort,
minimal context, decision rights, side-effect limits, attempt/effort boundary, and
handoff destination. Use fresh self-contained context (`fork_turns="none"` when
supported). Do not create sidebar tasks to simulate internal workers.

Use subagents only for useful independent work, within the slots the host actually
offers. Read-only reviewers inspect and report; they do not write files even if their
runtime allows it. ROOT stores their returned
report when a durable file is useful. Writers own disjoint scopes. A reviewer checks
material implementation independently after its relevant changes settle. Routine
edits do not require a ceremonial second approval.

## Keep ROOT and worker records separate

Use the existing workspace layout or this small default:

```text
AGENTS.md                         # concise entry and boundaries
docs/ROOT.md                      # one current coordination/verification brief
docs/<key-source>.md              # goal, acceptance, architecture when already needed
workspace/agents/<package>/      # briefs, working notes, outputs, handoff
workspace/evidence/               # raw tests/observations, as required by the project
```

Do not create duplicate GOAL/STATUS/PLAN summaries when ROOT already conveys them.
Existing historical or runtime evidence is not deleted as a side effect of adopting
this structure. Operational working files do not belong in the repository top level.

Each agent returns a short handoff (normally <=40 lines): package ID and source,
result and scope, outputs/changed files, checks actually run and evidence paths,
limitations/blockers, recommendation or next decision. Do not send the whole
transcript or fill ROOT with daily agent notes. Surface material blockers promptly.

## One current document, not a stack of revisions

ROOT alone maintains the current brief. It contains the intended outcome and
acceptance; authoritative source links; current facts with observation dates;
current plan versus actual result; packages/ownership/dependencies; evidence index;
blockers; decisions still required; and the next action.

Rewrite its affected sections coherently. If the structure changes substantially,
recompose the whole document, remove obsolete instructions and reconcile links.
Keep the stable filename. Do not append a diary, changelog or v1/v2/final documents.
No manual document-version ledger or archival copy is required. A technical package
version or source hash can exist for install/verification mechanics without creating
multiple working documents. A current brief must not convert an unknown result to a
fact or misrepresent prior measured evidence while being rewritten.

## Verify through the ROOT brief

ROOT uses the brief as the index to acceptance and evidence, not as proof by itself.
Check the relevant source output, scope, date and code identity; rerun a focused check
when needed. Distinguish agent-reported, ROOT-verified, and not-yet-verified claims.
Update the brief to the strongest evidenced state and next decision. Avoid copying
the raw evidence into it. Claimed completion must match the project's acceptance.

The workflow grants no live input, payments, messages, deployment or autonomous future
runs. Use authorization already present and ask only for a genuinely missing decision.
On a host without delegation or filesystem access, state that limit and perform the
available planning/review steps; never imply workers ran or files were saved.
