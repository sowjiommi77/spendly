# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the dev server
python app.py          # http://localhost:5001

# Run tests
pytest                 # all tests
pytest tests/test_foo.py::test_bar   # single test
```

Install dependencies: `pip install -r requirements.txt`

## Architecture

**Spendly** is a Flask expense-tracker app built as a step-by-step teaching project. Backend is Python/Flask + SQLite; frontend is Jinja2 templates with vanilla CSS/JS — no build step.

### Backend (`app.py`, `database/db.py`)

`app.py` is the single entry point — all Flask routes live there. Routes beyond the public landing/auth pages are stubs ("coming in Step N") that students fill in.

`database/db.py` is intentionally left empty for students to implement three functions:
- `get_db()` — SQLite connection with `row_factory` and foreign keys enabled
- `init_db()` — `CREATE TABLE IF NOT EXISTS` for all tables
- `seed_db()` — sample data for development

### Templates

All pages extend `templates/base.html` via Jinja2 block inheritance. Blocks available: `title`, `head` (extra `<link>`/`<meta>`), `content`, `scripts`.

`base.html` renders the shared navbar and footer and loads `static/css/style.css` + `static/js/main.js` on every page.

### CSS design system

`static/css/style.css` defines all CSS custom properties (design tokens) at `:root`. Use these variables — don't hardcode colors or fonts:
- Colors: `--ink`, `--ink-soft`, `--ink-muted`, `--paper`, `--accent` (dark green `#1a472a`), `--accent-2` (gold), `--danger`
- Fonts: `--font-display` (DM Serif Display) / `--font-body` (DM Sans)
- Layout: `--max-width: 1200px`, `--auth-width: 440px`

The landing page has its own supplemental stylesheet at `static/css/landing.css`. Page-specific overrides follow the same pattern — add a new CSS file and load it in the page's `{% block head %}`.

### Routes

| URL | Template | Notes |
|-----|----------|-------|
| `/` | `landing.html` | Marketing page with video modal |
| `/register` | `register.html` | POST to `/register` (not yet wired) |
| `/login` | `login.html` | POST to `/login` (not yet wired) |
| `/terms` | `terms.html` | Static legal page |
| `/privacy` | `privacy.html` | Static legal page |
| `/logout`, `/profile`, `/expenses/*` | — | Placeholder strings, to be implemented |

### Testing

pytest-flask is configured; add tests under a `tests/` directory. The `app` fixture from `pytest-flask` expects a Flask app exported from `app.py`.
