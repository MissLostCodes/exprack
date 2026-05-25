# Spec: Registration

## Overview
Add user registration functionality allowing new users to create an account with email and password. This is the second step in the Spendly roadmap, enabling onboarding of new users.

## Depends on
Step 01 – database setup must be complete.

## Routes
- `GET /register` — render registration form — public
- `POST /register` — process registration data, create user, login — public

## Database changes
- Add `users` table with columns `id INTEGER PRIMARY KEY AUTOINCREMENT`, `email TEXT UNIQUE NOT NULL`, `password_hash TEXT NOT NULL`.
- Ensure `init_db()` creates this table.

## Templates
- **Create:** `templates/register.html` (registration form extending `base.html`).
- **Modify:** `templates/base.html` — add navigation link to Register page.

## Files to change
- `app.py` — add routes for GET and POST `/register` handling form display and submission.
- `database/db.py` — add function to insert a new user with password hashing using Werkzeug's `generate_password_hash`.
- `templates/base.html` — insert link to registration page.

## Files to create
- `templates/register.html`

## New dependencies
- `werkzeug` for password hashing (already a Flask dependency, but ensure it is imported).

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`

## Definition of done
- [ ] Registration page renders correctly.
- [ ] Submitting valid email/password creates a new user in the `users` table.
- [ ] Passwords are stored as a hash, not plain text.
- [ ] Duplicate email registration shows an error message.
- [ ] After successful registration, user is redirected to the landing page and is logged in.
- [ ] Tests cover rendering, successful registration, duplicate email handling, and password hashing.
