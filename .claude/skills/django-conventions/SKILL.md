---
name: django-conventions
description: Conventions and guardrails for the dental-clinic Django repo. Use when writing or changing models, views, URLs, templates, validators, or tests, or when unsure how a new piece of code should be structured to match the codebase.
---

# Django Conventions (dental-clinic)

Authoritative reference is `CLAUDE.md` at the repo root. This skill is a quick-access summary.

## App layout

- All app code lives under the `dental_clinic/` package: seven apps (`auth_app`, `dentist_profile`, `patient`, `treatment`, `appointment`, `invoice`, `common`).
- Apps are registered in `INSTALLED_APPS` by full dotted path: `dental_clinic.<app>`.
- Import siblings by full package path (`from dental_clinic.patient.models import Patient`) or relative imports (`from ..treatment.models import Treatment`).

## Views

- Use **class-based generic views** from `django.views.generic` (imported as `views`).
- Guard every view with `LoginRequiredMixin`. There are **no function-based views**.
- Cross-app redirects use `reverse_lazy` on `success_url` (e.g. patient create → appointment create).

## URLs & templates

- URL names are **kebab-case** (`create-patient`, `appointment-create`, `patients-catalogue`).
- Templates live in top-level `templates/dental_clinic/<app>/` with **kebab-case** filenames (`create-patient.html`), extending `templates/base.html`.
- Static assets go in top-level `static/` (`style/`, `images/`).

## Models & validation

- Model constants are UPPER_CASE class attributes (e.g. `UIN_NUMBER_MAX_LENGTH = 10`).
- Field validators live in per-app `validators.py`, named `validate_<what>` (e.g. `validate_phone_number_only_nums`).
- Keep functions under ~40 lines. Follow SOLID; prefer dependency injection; avoid duplication.

## Auth (do not change)

- `AUTH_USER_MODEL = 'auth_app.DentistUser'`; login is by 10-digit **UIN number** (`USERNAME_FIELD = 'uin_number'`).
- Do not switch the DB engine, replace `DentistUser`, or change `USERNAME_FIELD`.

## Migrations

- After model changes: `python manage.py makemigrations` and include the new migration.
- **Never edit or delete existing migrations** — add new ones instead.

## Tests

- Tests live under the top-level `tests/` package: `tests/<app>/<models|views>/test_*.py` — **not** in per-app `tests.py`.
- Use `django.test.TestCase`, `reverse()` for URLs, `assertTemplateUsed`/`assertRedirects` for views.
- Descriptive method names encode scenario + expectation (`test_patient_create_view_unauthenticated_redirects`).
- Requires a reachable PostgreSQL (no SQLite fallback). Run: `python manage.py test` or `python manage.py test tests.<app>`.

## Don't (drive-by) change

- `Invoice.amount` / `invoice_number` CharFields or `Treatment.cost` FloatField — money representation is a maintainer decision.
- The commented-out CI test/deploy steps or the AWS ECS scaffolding.
