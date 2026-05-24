# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

| Task | Command | Notes |
|------|---------|-------|
| **Create a virtual environment / install dependencies** | `uv venv && source .venv/bin/activate && uv pip install -r requirements.txt` | `uv` is already vendored in this repo (`uv.lock`). |
| **Run the development server** | `python -m expense_tracker.main` <br>or `flask --app expense_tracker.app run --debug --port 5001` | The app listens on **port 5001** by default. |
| **Run the full test suite** | `pytest` | Tests are placed under `tests/` (if added later). |
| **Run a single test** | `pytest path/to/test_file.py::test_name` | Replace with the desired file and test function. |
| **Lint / static analysis** | `ruff check .` | `ruff` is a fast linter/formatter; install with `uv pip install ruff` if not present. |
| **Format code** | `ruff format .` | Keeps codebase consistently styled. |
| **Database migrations (future)** | `alembic upgrade head` | Placeholder – the project currently uses a simple SQLite helper (`expense_tracker/database/db.py`). |
| **Open a REPL with app context** | `python -c "import expense_tracker.app as app; import flask; ctx = app.app.test_request_context(); ctx.push()"` | Useful for quick exploration of routes or models. |

---

## High‑Level Architecture

```
expense-tracker/
├── expense_tracker/
│   ├── app.py          ← Core Flask app, defines routes & template rendering
│   ├── main.py         ← Entry point (`python -m expense_tracker.main`)
│   ├── database/
│   │   ├── __init__.py ← Exposes the DB helper
│   │   └── db.py       ← Simple SQLite wrapper (create_connection, init_db)
│   ├── static/         ← CSS & JS assets served by Flask
│   └── templates/      ← Jinja2 HTML templates (base, landing, login, register, terms)
├── pyproject.toml      ← Build metadata, Python version, dependencies
├── requirements.txt    ← Pin‑precise package versions for reproducible installs
└── README.md           ← High‑level project description
```

### Core Concepts

* **Flask Application (`app.py`)** – Declares routes for landing, registration, login, terms, and placeholder routes for future features (profile, expense CRUD). Each view returns a rendered Jinja2 template or a placeholder string.
* **Templates** – All HTML files extend `base.html`. Navigation is built with `url_for` calls, ensuring routes stay in sync with the Python code.
* **Static Assets** – `static/css/style.css` provides layout/branding; `static/js/main.js` is a stub for future interactivity.
* **Database Layer** – A minimal SQLite helper (`database/db.py`) supplies a `get_connection()` function and an `init_db()` routine that creates a basic `expenses` table. The layer is deliberately thin to keep the learning curve low.
* **Entry Point (`main.py`)** – Executes `app.run()` with debug mode enabled on port 5001. Running the module (`python -m expense_tracker.main`) is the canonical way to start the dev server.
* **Testing** – The project uses **pytest** with **pytest‑flask** for request‑level testing. Tests are expected under a top‑level `tests/` directory (currently empty but scaffolded by the dependency list).

### Extensibility Points

* **Add new pages** – Create a Jinja2 template in `templates/`, add a corresponding route in `app.py`, and link to it via `url_for`.
* **Expand the DB schema** – Modify `database/db.py` and run `init_db()` (or a migration tool) to evolve the schema; expose new helper functions as needed.
* **Front‑end enhancements** – Update `static/css/style.css` or `static/js/main.js`; the base template already pulls these assets into every page.

---

## Quick Reference for Future Claude Code Instances

* When adding a new Flask route, **always** use `url_for` in templates to avoid hard‑coded URLs.
* For any UI change, edit the relevant template under `templates/` and verify the update by restarting the dev server (or using Flask’s auto‑reload in debug mode).
* Stick to the existing project structure: keep backend logic in `app.py` or the `database/` package, and UI assets under `static/` & `templates/`.
* Run `ruff` before committing to catch style or import issues early. Use `ruff format` to auto‑format.
* Use the provided virtual‑env workflow (`uv venv && source .venv/bin/activate`) for an isolated, reproducible environment. The lock file (`uv.lock`) guarantees deterministic installs.
