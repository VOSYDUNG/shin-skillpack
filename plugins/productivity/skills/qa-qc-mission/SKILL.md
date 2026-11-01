---
name: qa-qc-mission
description: Run QA/QC sơ bộ — the early verification phase that forms a Mission's common rules before Mission lock. Produces outcome acceptance criteria with required evidence kinds (compatible with the OSER `oser init` acceptance contract), invariants, the QC checks/evaluators to run during delivery and who evaluates, and the unknowns with how to reduce them. Use while forming a Mission to build or solve something, before approving it, or when acceptance is vague.
---

# QA/QC sơ bộ for a Mission

Decide, before the Mission is locked, how anyone will know the result is right. This is
early verification, not testing finished work.

- **QA (quality assurance)** — how quality will be assured: which outcomes count, what
  must never break, who judges, and with what evidence.
- **QC (quality control)** — the concrete checks that will be run during delivery to
  produce that evidence.

The gate itself — when a Mission is ready, direction approval, authority and lock — is
defined in OSER [mission-formation](https://github.com/VOSYDUNG/nnc-claude-plugins/blob/main/plugins/nnc/skills/mission-formation/SKILL.md)
and the [Declaration](https://github.com/VOSYDUNG/nnc-claude-plugins/blob/main/docs/DECLARATION.md).
This skill only supplies the verification part of the Mission draft; it approves nothing.

## When to run it

After the real problem and current state are understood and a direction is chosen or
nearly chosen; before the Mission draft is approved and locked. Re-run only for a Delta
Mission that changes accepted behavior. A one-line task does not need it.

## Method

1. **Read the outcome, not the task list.** Restate who benefits and what observable
   change the Mission must produce. Use the user's language; keep sources and dates.
2. **Write outcome acceptance.** Each criterion is observable and judged on the outcome,
   not on task count. For each, name the evidence kinds it `requires` (for example
   `test_report`, `user_confirmation`, `measurement`, `document_review`, `ledger_record`,
   `screenshot`, `log_excerpt`). Different evidence kinds are not interchangeable; a test
   pass does not prove real use. Missing baseline or target stays UNKNOWN with a step to
   measure it — never an invented number.
3. **State invariants.** What must stay true throughout delivery: data that must not be
   altered or leaked, behavior that must not regress, authority limits, budget or time
   envelope, safety constraints. Each invariant names how a breach would be detected.
4. **Plan QC.** For each acceptance criterion and invariant, the check that produces its
   evidence: what is checked, method (automated test, review, measurement, user trial),
   when (per change, per milestone, before release), who or what evaluates, and pass
   condition. The evaluator is independent of the producer where the claim is material;
   routine items may use self-report.
5. **List unknowns and how to reduce them.** For each: why it matters, the cheapest safe
   way to reduce it (read a source, ask the owner, small experiment, measurement), and
   what decision changes once known. Unknowns that block acceptance go to the gate as
   open items, not as assumed facts.
6. **Hand to the gate.** Return the block below to the Mission draft. The person with
   authority approves; a recommendation is not approval.

## Template

```yaml
# QA/QC sơ bộ — [Mission/work ID] — as of [date]
outcome: "[beneficiary + observable change]"
acceptance:            # maps to oser init: [{id, description, requires: [...]}]
  - id: A1
    description: "[observable outcome condition]"
    requires: [measurement, user_confirmation]
  - id: A2
    description: "[...]"
    requires: [test_report]
invariants:
  - id: I1
    rule: "[must stay true]"
    detect: "[how a breach is noticed]"
qc:
  - covers: [A1]
    check: "[what is checked and how]"
    when: "[per change | milestone | before release]"
    evaluator: "[role/agent/person; independent of producer?]"
    pass: "[pass condition]"
unknowns:
  - item: "[what is not known]"
    impact: "[which criterion/decision it affects]"
    reduce_by: "[source/question/experiment]"
    blocks_acceptance: true
```

Keep only `acceptance` entries in `{id, description, requires}` form when passing them to
`oser init`; invariants, QC and unknowns stay in the Mission draft or project brief.

## Rules

- Acceptance judges outcomes; QC produces evidence; neither grants authority.
- UNKNOWN stays UNKNOWN. Requested is not done; a receipt is not an outcome.
- Do not copy business data (ledgers, customer lists) into the criteria; reference the
  source system and the evidence kind.
- After lock, changing accepted behavior or acceptance is a Delta Mission, handled by
  OSER [adaptive-delivery](https://github.com/VOSYDUNG/nnc-claude-plugins/blob/main/plugins/nnc/skills/adaptive-delivery/SKILL.md).
- Once the Mission exists, plans, checklists and reviews continue in
  [outcome-work-management](../outcome-work-management/SKILL.md).
