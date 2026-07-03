---
description: Generate and apply Django migrations following repo guardrails.
argument-hint: "[app label, optional]"
allowed-tools: Bash(python manage.py makemigrations:*), Bash(python manage.py migrate:*), Bash(python manage.py showmigrations:*)
---

Create and apply database migrations for this Django project.

App scope (optional): `$ARGUMENTS`

Guardrails (from `CLAUDE.md`):

- **Never edit or delete existing migrations** — they may already be applied. Only add new ones.
- Do not switch the database engine or alter the `DentistUser` / `USERNAME_FIELD` auth model.
- Requires the DB env vars and a reachable PostgreSQL.

Steps:

1. Generate migrations:
   ```bash
   python manage.py makemigrations $ARGUMENTS
   ```
2. Show what will be applied:
   ```bash
   python manage.py showmigrations
   ```
3. Apply them:
   ```bash
   python manage.py migrate $ARGUMENTS
   ```
4. Report the new migration files created and confirm they are included in the change set.
5. If no database is reachable, stop after `makemigrations`, and say the migration was generated but not applied.
