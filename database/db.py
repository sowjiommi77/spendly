import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "spendly.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    if conn.execute("SELECT 1 FROM users LIMIT 1").fetchone():
        conn.close()
        return

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    user_id = cursor.lastrowid

    expenses = [
        (user_id, 42.50,  "Food",          "2026-06-01", "Grocery run"),
        (user_id, 15.00,  "Transport",     "2026-06-03", "Bus pass top-up"),
        (user_id, 120.00, "Bills",         "2026-06-05", "Electricity bill"),
        (user_id, 35.00,  "Health",        "2026-06-07", "Pharmacy"),
        (user_id, 25.00,  "Entertainment", "2026-06-09", "Cinema tickets"),
        (user_id, 89.99,  "Shopping",      "2026-06-11", "New shoes"),
        (user_id, 10.00,  "Other",         "2026-06-13", "Miscellaneous"),
        (user_id, 55.00,  "Food",          "2026-06-15", "Restaurant dinner"),
    ]
    cursor.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?,?,?,?,?)",
        expenses,
    )
    conn.commit()
    conn.close()
