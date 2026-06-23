# Spec: Login and Logout

## Overview

Implement `POST /login` and `GET /logout` so users can authenticate into Spendly and end their session. The `GET /login` route and template already exist as stubs; this step wires up form submission — querying the database, verifying the hashed password, writing the user id into a Flask session cookie, and redirecting to the dashboard (or back to the form on failure). Logout clears the session and redirects to the landing page. Together these two routes are the gate that all future protected pages will rely on.

## Depends on

- Step 01 — Database Setup (`database/db.py` with `get_db()`, `users` table)
- Step 02 — Registration (users exist in the database with hashed passwords)

## Routes

- `GET  /login`  — show login form — public
- `POST /login`  — validate credentials, set session, redirect to `/` — public
- `GET  /logout` — clear session, redirect to `/` — public (safe to call when not logged in)

## Database changes

No database changes. The `users` table already has `id`, `email`, and `password_hash`.

## Templates

- **Modify:** `templates/login.html` — change the `<form>` to `method="POST" action="/login"`, add `{{ error }}` display block above the form fields (matching the style used in `register.html`)

## Files to change

- `app.py` — convert `GET /login` to `["GET", "POST"]`, implement POST logic with session; implement `/logout` to clear session and redirect
- `templates/login.html` — add POST action and error display

## Files to create

None.

## New dependencies

No new pip packages. `flask.session` is part of Flask.

## Rules for implementation

- No SQLAlchemy or ORMs
- Parameterised queries only — never format SQL strings with user input
- Passwords hashed with werkzeug — verify with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Store only `user_id` (integer) in `session` — never store the password or full user dict
- On failed login show a generic message: "Invalid email or password." — do not reveal which field is wrong
- On success redirect to `/` (dashboard placeholder) — a later step will change this to `/dashboard`
- Use `session.clear()` in `/logout`, then redirect to `/`
- Import `session` from `flask` (already available via the Flask install)

## Definition of done

- [ ] Visiting `GET /login` renders the login form without errors
- [ ] Submitting valid credentials sets `session["user_id"]` and redirects away from `/login`
- [ ] Submitting a wrong password shows "Invalid email or password." on the form — no 500 error
- [ ] Submitting an email that does not exist shows "Invalid email or password." — same message, no information leak
- [ ] Submitting with empty fields shows a validation error before hitting the database
- [ ] Visiting `/logout` clears the session and redirects to `/`
- [ ] After logout, `session["user_id"]` is no longer set
- [ ] The demo user (`demo@spendly.com` / `demo123`) can log in successfully
