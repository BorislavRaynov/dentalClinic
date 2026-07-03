---
description: Produce an implementation plan for a feature via the architect agent.
argument-hint: "<feature description>"
---

Plan a feature before any code is written.

Feature: `$ARGUMENTS`

Preconditions:

- If `$ARGUMENTS` is empty, ask what should be planned and stop.

Steps:

1. Delegate to the `architect` agent to analyze the request against the existing architecture (seven Django apps under `dental_clinic/`, CBVs + `LoginRequiredMixin`, UIN-based auth, server-rendered templates).
2. The architect must read `CLAUDE.md` and existing code before proposing anything, and must respect its "Never" guardrails.
3. Return a plan containing:
   - Goal
   - Current state
   - Proposed solution (which apps/files change, where new code belongs)
   - Risks
   - Task breakdown (independent tasks flagged for parallel work)
   - Estimated complexity
   - Validation strategy (tests to add under top-level `tests/`)
4. Do **not** implement yet — stop after presenting the plan for approval.
