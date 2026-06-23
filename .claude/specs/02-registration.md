# Spec: Registration

## Overview

Implement the `POST /register` route so new users can create a Spendly account. The GET route and template already exist; this step wires up the form submission — validating input, hashing the password, inserting the user into the database, and redirecting appropriately. It also sets `app.secret_key` (required for Flask sessions and flash messages used in later steps).

## Depends on

- Step 01 — Database Setup (`database/db.py` with working `get_db()`, `init_db()`, `users` table)

## Routes

- `POST /register` — accept form submission, create user, redirect — public

## Database changes

No new tables or columns. The `users` table already has all required columns:
`id`, `name`, `email`, `password_hash`, `created_at`.

## Templates

- **Modify:** `templates/register.html` — already renders `{{ error }}`; no structural changes needed. Optionally re-populate `name` and `email` fields on validation failure using `{{ value }}` variables passed from the route.

## Files to change

- `app.py` — add `secret_key`, add imports (`request`, `redirect`, `url_for`, `flash`), implement `POST /register` route, convert existing `GET /register` to accept `["GET", "POST"]` on the same route function

## Files to create

None.

## New dependencies

No new pip packages.

## Rules for implementation

- No SQLAlchemy or ORMs
- Parameterised queries only — never format SQL strings with user input
- Hash passwords with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Set `app.secret_key` using `os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")`
- Validate server-side: name non-empty, valid email format (basic check), password ≥ 8 characters
- On duplicate email, catch the `sqlite3.IntegrityError` and show a friendly error — do not expose the raw exception
- On success, redirect to `/login` (login is implemented in Step 3)
- Re-render the form with `error` message and the submitted `name`/`email` values on any validation failure so the user does not have to retype everything

## Definition of done

- [ ] Submitting the form with valid data creates a new row in `users` with a hashed password
- [ ] Submitting a duplicate email shows "An account with that email already exists" on the form (not a 500 error)
- [ ] Submitting with an empty name shows a validation error on the form
- [ ] Submitting with a password shorter than 8 characters shows a validation error on the form
- [ ] After successful registration, the browser is redirected to `/login`
- [ ] The `name` and `email` fields are repopulated when the form is re-shown after an error
- [ ] App starts without errors and `secret_key` is set
