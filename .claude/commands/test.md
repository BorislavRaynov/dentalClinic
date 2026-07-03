---
description: Run the Django test suite (all tests, or a specific package/test path).
argument-hint: "[tests.<app> or full test path, optional]"
allowed-tools: Bash(python manage.py test:*)
---

Run the project's Django tests.

- Tests live under the top-level `tests/` package (mirrored as `tests/<app>/<models|views>/test_*.py`), **not** in per-app `tests.py`.
- The suite requires a reachable PostgreSQL and the DB env vars (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`); there is no SQLite fallback.

Target: `$ARGUMENTS`

Steps:

1. If `$ARGUMENTS` is empty, run the full suite:
   ```bash
   python manage.py test
   ```
   Otherwise run the specified target, e.g.:
   ```bash
   python manage.py test $ARGUMENTS
   ```
2. If the run fails because no database is reachable, say so explicitly — do **not** imply tests passed.
3. Summarize results: totals, failures, and the exact failing test names.
4. Never merge or conclude "done" while tests are failing.
