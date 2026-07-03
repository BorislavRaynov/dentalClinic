# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A dental clinic management web app built with **Django 4.2** and **PostgreSQL**. A dentist (the only user type) registers patients, books appointments, assigns treatments, and generates invoices for the provided services. Server-rendered Django templates; no REST API, no JavaScript framework.

## Architecture

All application code lives in the `dental_clinic/` package, split into seven Django apps registered in `INSTALLED_APPS` with their full dotted path (`dental_clinic.<app>`):

- `auth_app` — custom authentication. `AUTH_USER_MODEL = 'auth_app.DentistUser'`; users log in with a 10-digit **UIN number** (`USERNAME_FIELD = 'uin_number'`), not a username/email. `DentalUserManager.create_superuser` also auto-creates a `DentistUserProfile`.
- `dentist_profile` — profile data (names) for the dentist user, linked to `DentistUser`.
- `patient` — `Patient` model with a `ManyToManyField` to `Treatment`. `Patient.delete()` is overridden to clear treatments first.
- `treatment` — `Treatment` with a 3-digit `clinical_code`, name, cost, description, and optional notes; create/edit views under `/treatment/`.
- `appointment` — `Appointment` = FK to `Patient` + FK to the dentist user + date/time.
- `invoice` — `Invoice` per patient; `invoice_number` (CharField) is the primary key; `amount` is also a CharField.
- `common` — home page / shared views.

Cross-app flow to know: creating a patient redirects to appointment creation (`PatientCreateView.success_url = reverse_lazy('appointment-create')`), and adding treatments to a patient redirects back to the appointments catalogue. Root URL wiring is in `dental_clinic/urls.py` (`/authentication/`, `/profile/`, `/appointment/`, `/patient/`, `/treatment/`, `/invoice/`, `/admin/`).

Configuration is entirely environment-driven (`dental_clinic/settings.py`): `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` (space-separated), `DB_NAME`/`DB_USER`/`DB_PASSWORD`/`DB_HOST`/`DB_PORT`, `STATIC_ROOT`. Env files are expected at `envs/.env` (dev, used by `docker-compose.yml`) and `envs/.env.prod` (prod, used by `docker-compose.prod.yml`) — both are git-ignored and not in the repo. Note: when `DEBUG` is truthy, `AUTH_PASSWORD_VALIDATORS` is emptied.

Deployment: `docker-compose.yml` (dev: web via `runserver`, Postgres, pgAdmin) and `docker-compose.prod.yml` (Gunicorn + Postgres + nginx with certbot volumes; nginx config in `nginx/conf.d/web.conf`). CI (`.github/workflows/pipeline.yml`) only installs dependencies on push/PR to `main`; the test step and an AWS ECS deploy job exist but are commented out.

## Commands

There is no package manager script layer — everything goes through `manage.py` or Docker Compose. Running `manage.py` locally requires the DB env vars above and a reachable PostgreSQL.

```bash
pip install -r requirements.txt          # install deps (Python 3.8 in CI)

python manage.py runserver               # dev server (needs env vars + Postgres)
docker compose up                        # dev stack: web + Postgres + pgAdmin (needs envs/.env)

python manage.py makemigrations          # after model changes
python manage.py migrate

python manage.py test                    # run all tests
python manage.py test tests.patient      # run one test package
python manage.py test tests.patient.views.test_create_view.PatientCreateViewTestCase.test_patient_create_view_unauthenticated_redirects   # single test
```

- **Lint/format:** TODO — no linter or formatter is configured in this repo (no flake8/ruff/black/isort config found).
- Caution: `requirements.txt` is UTF-16 encoded; if you edit it, preserve an encoding pip accepts rather than rewriting it blindly.
- The dev compose `web` service runs `runserver localhost:8000` (binds localhost inside the container), so the published port may not be reachable from the host — a known quirk, not something to silently "fix" while doing unrelated work.

## Coding Conventions (as observed)

- Follow SOLID
- Use dependency injection
- Keep functions under 40 lines where practical
- Avoid duplication
- Use meaningful names
- Views are **class-based generic views** (`django.views.generic`, imported as `views`) guarded with `LoginRequiredMixin`. Follow this pattern; no function-based views are used.
- Templates live in the top-level `templates/dental_clinic/<app>/` directory with **kebab-case** filenames (`create-patient.html`); URL names are also kebab-case (`create-patient`, `appointment-create`, `patients-catalogue`).
- Field validators live in a per-app `validators.py`, named `validate_<what>` (e.g. `validate_phone_number_only_nums`).
- Model constants are UPPER_CASE class attributes (e.g. `UIN_NUMBER_MAX_LENGTH = 10`).
- Imports of sibling apps use the full package path (`from dental_clinic.patient.models import Patient`) or relative imports (`from ..treatment.models import Treatment`).
- Static assets go in top-level `static/` (`style/`, `images/`).

## Testing Expectations

- Tests live in the top-level `tests/` package, mirrored as `tests/<app>/<models|views>/test_*.py` — **not** in the per-app `tests.py` files (those are empty scaffolding).
- Style: `django.test.TestCase`, descriptive method names encoding the scenario and expectation (`test_patient_create_view_unauthenticated_redirects`), `reverse()` for URLs, `assertTemplateUsed`/`assertRedirects` for views.
- Only `appointment`, `auth_app`, `patient`, and `treatment` currently have tests; there is no coverage tooling or enforced threshold. CI does **not** run tests (the step is commented out).
- Tests need a PostgreSQL database available (settings have no SQLite fallback).
Always:

- update tests
- run tests
- do not merge failing tests

## Repository Workflow & Git Conventions

- Single branch: `main`; CI triggers on push and PR to `main`.
- Observed commit messages are short, imperative, ending with a period (e.g. "Set up environments.").
- TODO: no PR template, branch-naming scheme, review process, or CONTRIBUTING file exists — ask the maintainer before assuming one.
- The repo root doubles as a Python virtualenv (`pyvenv.cfg` is checked in); `.gitignore` excludes the venv internals, env files, `postgresql/` data, and `staticfiles/`.

## Git

- Never force push.
- Always create a feature branch.
- Commit after each logical change.
- Use Conventional Commits.

Examples:

feat:
fix:
refactor:
docs:
test:

## Before finishing

Always:

1. lint
2. run tests
3. explain what changed
4. update documentation if needed

## For AI Assistants

Always, before finishing work:

- Run `python manage.py test` (or at minimum the test packages touching your change) if a database is available; if you cannot run them, say so explicitly rather than implying they passed.
- After any model change, generate the migration (`makemigrations`) and include it in the change.
- Keep new code consistent with the observed conventions above (CBVs + `LoginRequiredMixin`, kebab-case templates/URL names, validators in `validators.py`, tests under top-level `tests/`).
- Check `git status` to ensure no env files, venv artifacts, or `postgresql/` data are being committed.

Never:

- Commit or hardcode secrets — settings must keep reading from environment variables; don't invent an `envs/.env` with real-looking credentials.
- Enable the commented-out CI test/deploy steps, or change the AWS deploy scaffolding, without being asked.
- Switch the database engine, replace the custom `DentistUser` model, or change `USERNAME_FIELD` — auth and data are built around UIN-based login.
- Edit or delete existing migrations that may already be applied; add new ones instead.
- "Fix" the `Invoice.amount`/`invoice_number` CharFields or `Treatment.cost` FloatField as a drive-by; changing money representation is a schema decision for the maintainer.

## Open Questions (context from the maintainer would improve accuracy)

- TODO: What are the expected contents of `envs/.env` / `envs/.env.prod` (a committed `.env.example` would help)?
- TODO: Which Python version is authoritative — CI pins 3.8, but the Dockerfile uses `python:3` (latest)?
- TODO: Is there a preferred linter/formatter (black, ruff, flake8) even though none is configured?
- TODO: Should CI run the test suite (the step exists but is commented out) — intentional or unfinished?
- TODO: Branching/PR conventions — is direct push to `main` acceptable, or are PRs required?
- TODO: Deployment reality — is the AWS ECS pipeline (commented out) planned, or is `docker-compose.prod.yml` on a VM the actual target?
- TODO: Are the per-app empty `tests.py` files meant to be removed, or kept as placeholders?
- TODO: Invoice `amount` as CharField — intentional (formatted strings) or tech debt slated for a migration?
