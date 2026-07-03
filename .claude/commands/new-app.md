---
description: Scaffold a new Django app following this repo's conventions.
argument-hint: "<app_name>"
allowed-tools: Bash(python manage.py startapp:*)
---

Create a new Django app named `$ARGUMENTS`, wired to match this repository's conventions.

Preconditions:

- If `$ARGUMENTS` is empty, ask for the app name and stop.

Conventions to follow (see `CLAUDE.md`):

- Apps live under the `dental_clinic/` package and are registered in `INSTALLED_APPS` by full dotted path: `dental_clinic.$ARGUMENTS`.
- Views are **class-based generic views** guarded with `LoginRequiredMixin`.
- URL names and template filenames are **kebab-case**.
- Templates go in top-level `templates/dental_clinic/$ARGUMENTS/`.
- Field validators go in a per-app `validators.py`, named `validate_<what>`.
- Model constants are UPPER_CASE class attributes.
- Tests go under the top-level `tests/$ARGUMENTS/<models|views>/test_*.py`, not the per-app `tests.py`.

Steps:

1. Create the app in the package directory:
   ```bash
   python manage.py startapp $ARGUMENTS dental_clinic/$ARGUMENTS
   ```
2. Set the app's `AppConfig.name` to `dental_clinic.$ARGUMENTS` in `apps.py`.
3. Register `dental_clinic.$ARGUMENTS` in `INSTALLED_APPS` (`dental_clinic/settings.py`).
4. Add a `urls.py` with an `app_name`/kebab-case URL names and include it from `dental_clinic/urls.py`.
5. Create the `tests/$ARGUMENTS/` package (with `__init__.py`) and `templates/dental_clinic/$ARGUMENTS/` directory.
6. Add a `validators.py` stub if the models will need custom validation.
7. Report the files created and the wiring changes made.

Delegate implementation of models/views to the `backend` agent if the app needs real functionality beyond scaffolding.
