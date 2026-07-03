---
description: Run a full pre-merge review — code review, security, and QA — in parallel.
argument-hint: "[optional focus area or file paths]"
---

Coordinate a pre-merge review of the current changes.

Focus (optional): `$ARGUMENTS`

Steps:

1. Determine the scope with `git status` and `git diff` (staged + unstaged). If `$ARGUMENTS` names files or an area, narrow to that.
2. Delegate the following reviews **in parallel** (they are independent):
   - `reviewer` — correctness, readability, maintainability, convention conformance (`CLAUDE.md`).
   - `security` — auth/authorization coverage, input validation, secrets, CSRF/XSS/SQL injection, `DEBUG` password-validator behavior.
   - `qa` — missing tests and uncovered edge cases under the top-level `tests/` package.
3. Consolidate findings into one report, grouped by severity: Critical, High, Medium, Low, Suggestions.
4. Explicitly call out any `CLAUDE.md` "Never" violations (auth model changes, edited migrations, committed secrets/env files, enabled commented-out CI steps).
5. Do not mark the change ready to merge while Critical or High findings remain, or while tests fail.
