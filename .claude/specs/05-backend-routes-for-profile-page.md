# Spec: Backend Routes for Profile Page

## Overview

The profile page template already exists and is fully designed (Step 04), but it
currently renders hardcoded mock data. This step wires the `/profile` route to the
real database: fetching the logged-in user's record from `users`, querying their
expenses from `expenses`, and computing summary stats (total spent, transaction
count, top category, per-category breakdown) before passing live data to the
template. No new routes or tables are needed — this is purely a backend
implementation step.

## Depends on

- Step 01 — Database setup (`get_db`, `init_db`, `seed_db`, both tables exist)
- Step 03 — Login / logout (`session["user_id"]` is set on login)
- Step 04 — Profile page template (`profile.html` exists and accepts the four
  template variables: `user`, `stats`, `transactions`, `categories`)

## Routes

- `GET /profile` — replace hardcoded mock data with real DB queries — logged-in only

No new routes.

## Database changes

No database changes. Both `users` and `expenses` tables already exist with all
required columns.

## Templates

- **Create:** none
- **Modify:** none — `profile.html` already consumes `user`, `stats`,
  `transactions`, and `categories` in the exact shape produced by this
  implementation

## Files to change

- `app.py` — rewrite the `/profile` route body to query the database instead of
  returning hardcoded dicts

## Files to create

None.

## New dependencies

No new dependencies.

## Rules for implementation

- No SQLAlchemy or ORMs — raw `sqlite3` via `get_db()` only
- Parameterised queries only — never use string formatting in SQL
- Passwords hashed with werkzeug (not relevant here, but maintain the rule)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Close every DB connection after use
- Redirect to `/login` if `session["user_id"]` is absent (auth guard already
  present — keep it)
- Derive `member_since` from the user's `created_at` field, formatted as
  "Month YYYY" (e.g. "June 2026")
- Derive `initials` from the user's `name` field (first letter of each word,
  up to 2 letters, uppercased)
- `transactions` list must be sorted by `date` descending, limited to the 5
  most recent expenses
- `categories` list must be sorted by `total` descending
- Each category entry needs `name`, `total` (sum of amounts), and `pct`
  (integer percentage of overall total, rounded)
- `stats.top_category` is the category with the highest total spend

## Definition of done

- [ ] Log in as `demo@spendly.com` / `demo123` and visit `/profile` — the name
      "Demo User" appears in the profile header (not hardcoded, fetched from DB)
- [ ] The email shown is `demo@spendly.com` (from DB)
- [ ] "Member since" shows the correct formatted date derived from `created_at`
- [ ] "Total spent" stat matches the sum of all 8 seeded expenses (392.49)
- [ ] "Transactions" stat shows 8
- [ ] "Top category" stat shows "Bills" (highest seeded total at 120.00)
- [ ] The recent transactions table shows the 5 most recent expenses sorted
      newest-first (Jun 15 → Jun 13 → Jun 11 → Jun 09 → Jun 07)
- [ ] The category breakdown lists all 7 categories with correct totals and
      percentages that add up to 100 (±1 due to rounding)
- [ ] Registering a new account and visiting `/profile` shows that user's real
      name, email, and zero-expense stats (total 0.00, count 0, top category "—")
- [ ] Visiting `/profile` while logged out redirects to `/login`
