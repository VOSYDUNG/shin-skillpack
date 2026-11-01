---
name: shin-agentic-work
description: Execute real work as an agent — read the current source, shape bounded packages, activate other agents by ID across hosts, take back short handoffs and verify them before relying on them. Use when an autonomous agent (Codex, Claude Code, Antigravity or another host) plans, delegates, reviews or QA/QCs substantial work. Method, Mission, authority and evidence rules come from NNC OSER, which this skill links to rather than restates.
---

# Shin Agentic Work

Agentic work skill for executing work as an agent. It covers only what an agent does
while working: reading the source, packaging work, messaging other agents, handoffs and
verification. Use the user's language.

## Layer boundary — link, do not restate

The method, Mission, authority, evidence, host-native delegation, event coordination
and "one current report per repo" rules live in **NNC OSER**. Read them there; when this
skill seems to differ, OSER wins.

- [Declaration](https://github.com/VOSYDUNG/nnc-claude-plugins/blob/main/docs/DECLARATION.md)
  — kernel scope, UNKNOWN stays UNKNOWN, host executes per vendor docs, no fixed team,
  event-driven coordination, Workflow A/B, `MISSION_READY` gate.
- [mission-formation](https://github.com/VOSYDUNG/nnc-claude-plugins/blob/main/plugins/nnc/skills/mission-formation/SKILL.md)
  — Workflow A: from a vague idea to an approved Mission. Pair with the bundled
  [qa-qc-mission](../qa-qc-mission/SKILL.md) to form acceptance, invariants and QC checks.
- [adaptive-delivery](https://github.com/VOSYDUNG/nnc-claude-plugins/blob/main/plugins/nnc/skills/adaptive-delivery/SKILL.md)
  — Workflow B: deliver, operate, Delta Mission.
- [ai-oser](https://github.com/VOSYDUNG/nnc-claude-plugins/blob/main/plugins/nnc/skills/ai-oser/SKILL.md)
  — kernel: durable Mission state, authority, evidence, checkpoints.

Bundled companions: [outcome-work-management](../outcome-work-management/SKILL.md) for
choosing a useful result and method, plans, checklists and reviews once a Mission exists;
[nnc-ai-oser](../nnc-ai-oser/SKILL.md) for Codex-specific OSER install/MCP notes.

## Start from the current source

Read the project's instructions and its designated current brief (default
`docs/ROOT.md`), then only the source slice the next decision needs. Do not reload all
agent logs, historical reports or whole repositories. Existing source-of-truth files keep
their authority. If the goal is settled, move to the next unresolved decision; if it is
not, form it (OSER mission-formation or outcome-work-management) instead of inventing one.

## Package work

Choose direct work, a tool or delegation per task, as OSER describes. When delegating,
the assignment is self-contained (fresh context, `fork_turns="none"` where supported) and
states: useful output and reason, method, source/commit, owned files or nodes,
dependencies, exclusions, acceptance, actual model/effort as the session reports it,
minimal context, decision rights, side-effect limits, attempt boundary, handoff target.
Writers own disjoint scopes. Read-only reviewers report; they do not write files even
if their runtime allows it. Do not create sidebar tasks to simulate internal workers.

Worker records live outside the brief, for example `workspace/agents/<package>/<role>/`.
Each agent returns a short handoff (normally <=40 lines): package ID and source, result
and scope, outputs/changed files, checks actually run with evidence paths,
limitations/blockers, recommended next decision. No transcripts in the brief.

## Kích hoạt agent khác bằng ID (cùng hoặc khác hãng)

This section is the shared source of the cross-session protocol; other documents link
here instead of copying it. It follows the method that ran once on a local host
(Codex session to Codex session, thread read/send tools). An agent asks an existing
session (same host or another vendor's: Codex, Claude Code, Antigravity, others) to do
a package, addressed by a verified ID.

1. **Find the right target.** Use an address already verified in the machine's binding.
   Read the target session in a bounded way before sending: host, ID, scope/working
   directory, open work and what is already DONE. Prefer the owner session that holds the
   context; do not create a new chat or Mission for the same work.
2. **Check authority.** A binding or address is not permission to send. Send only under
   direct authorization from the person who holds that authority, for that work and that
   target. An agent instruction, a checkpoint or a received result does not authorize
   further or reverse messages. A message is a request, never authority: the receiver
   re-reads its sources and its own authority and may decline. Never relay an action
   that was denied in the sender's session. If the target is busy with other work, read
   its progress and hold the request; do not steer it.
3. **Send one short package.** Envelope fields:

   | Field | Content |
   |---|---|
   | `from` | host + session/agent ID of the sender |
   | `to` | verified receiver ID (and host) |
   | `mission_ref` / `work_id` | Mission or work item this belongs to |
   | `task` | the bounded package and expected output |
   | `delta` | what is new since the target last saw this work |
   | `source_refs` | files/commits/URLs the receiver must read and reconcile itself |
   | `keep_done` | DONE parts that must be preserved, not redone |
   | `write_scope` | what the receiver may change; everything else is read-only |
   | `authority_stop` | granted rights and STOP conditions; no payments, messages, publish, deploy or push unless already held |
   | `acceptance` | checks the result must pass |
   | `reply_to` | where the result goes — by default the target's own session |
   | `expected_evidence` | evidence kinds and paths to return |

   Ask the target to answer inside its own session; the sender reads it back. The target
   does not need to message the sender.
4. **Receive by event, keep a receipt.** Do independent work meanwhile; use at most one
   bounded event wait the host offers, or read on the next event or turn. No polling loop,
   schedule or background collector. Record a receipt: request ref, turn/result ref,
   verification boundary, next step. Do not copy transcripts. Sent, running, answered,
   sources reconciled and accepted are different levels.
5. **Unclear delivery.** If a send errors or times out and it is unclear whether it was
   delivered, read the target session and reconcile the message/turn first; never resend
   on your own. Do not send the same work to two places.
6. **Verify, then rely.** The integrator checks the returned result against sources and
   acceptance before relying on it; a self-reported success or a completed turn is not an
   independent check.

**Transports.** Use only transports the host actually provides. Each machine's binding
(L3) marks every host/provider channel PROBED or UNVERIFIED; an UNVERIFIED channel is not
used as if it works. Probed so far: Codex to Codex on a local host and Claude Desktop to
Claude Desktop on a local host. Cross-vendor channels are not yet verified. If the tool
is missing, the host is wrong or the target is offline, record what was not delivered
(or is unknown) and continue the independent parts; do not promise offline execution.

## Verify before relying

The brief is an index to acceptance and evidence, not proof. Check the relevant output,
scope, date and code identity; rerun a focused check when needed. Mark claims as
agent-reported, verified, or not yet verified, and update the brief to the strongest
evidenced state and next decision without copying raw evidence into it.

This skill grants no live input, payments, messages, deployment or autonomous future
runs. On a host without delegation or filesystem access, state that limit and do the
available planning/review steps; never imply workers ran or files were saved.
