---
name: local-dev-setup
description: How to run the dental-clinic Django app locally or via Docker, including required environment variables and Postgres. Use when setting up the project, running the server, or diagnosing "can't connect to database" / missing-env-var errors.
---

# Local Dev Setup (dental-clinic)

## Requirements

- Python (CI pins **3.8**; the Dockerfile uses `python:3`).
- A reachable **PostgreSQL** — there is no SQLite fallback.
- Environment variables (see below). Env files are expected at `envs/.env` (dev) and `envs/.env.prod` (prod); both are **git-ignored and not in the repo**.

## Required environment variables

`settings.py` is entirely env-driven:

- `SECRET_KEY`
- `DEBUG` — when truthy, `AUTH_PASSWORD_VALIDATORS` is emptied (dev only).
- `ALLOWED_HOSTS` — space-separated.
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- `STATIC_ROOT`

Never hardcode these or commit real credentials.

## Install & run (local)

```bash
pip install -r requirements.txt   # NOTE: requirements.txt is UTF-16 encoded — preserve an encoding pip accepts
python manage.py migrate
python manage.py runserver         # needs env vars + reachable Postgres
```

## Run via Docker

```bash
docker compose up                  # dev: web + Postgres + pgAdmin (needs envs/.env)
```

Known quirk: the dev `web` service runs `runserver localhost:8000` (binds localhost **inside** the container), so the published port may not be reachable from the host. This is a known issue — don't silently "fix" it during unrelated work.

## Common issues

- `django.db.utils.OperationalError` / connection refused → Postgres not running or `DB_*` vars unset.
- `ImproperlyConfigured: SECRET_KEY` → env file missing or not loaded.
- pip fails reading `requirements.txt` → encoding was rewritten; restore a UTF-16 (or pip-accepted) encoding.

## Before finishing work

1. No linter/formatter is configured (TODO in repo) — match existing style manually.
2. `python manage.py test` (needs a database).
3. `git status` — ensure no env files, venv artifacts, or `postgresql/` data are staged.
