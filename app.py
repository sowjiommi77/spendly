import os
import sqlite3
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    error = None
    name = ""
    email = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not name:
            error = "Name is required."
        elif "@" not in email:
            error = "Please enter a valid email address."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        else:
            conn = get_db()
            try:
                conn.execute(
                    "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                    (name, email, generate_password_hash(password)),
                )
                conn.commit()
                conn.close()
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                conn.close()
                error = "An account with that email already exists."

    return render_template("register.html", error=error, name=name, email=email)


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    error = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            error = "Please enter your email and password."
        else:
            conn = get_db()
            user = conn.execute(
                "SELECT id, password_hash FROM users WHERE email = ?", (email,)
            ).fetchone()
            conn.close()

            if user is None or not check_password_hash(user["password_hash"], password):
                error = "Invalid email or password."
            else:
                session["user_id"] = user["id"]
                return redirect(url_for("profile"))

    return render_template("login.html", error=error)


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    conn = get_db()
    row = conn.execute(
        "SELECT * FROM users WHERE id = ?", (session["user_id"],)
    ).fetchone()
    expense_rows = conn.execute(
        "SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC",
        (session["user_id"],),
    ).fetchall()
    conn.close()

    initials = "".join(w[0] for w in row["name"].split())[:2].upper()
    member_since = datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%B %Y")

    total_spent = sum(r["amount"] for r in expense_rows)
    transaction_count = len(expense_rows)

    cat_totals = {}
    for r in expense_rows:
        cat_totals[r["category"]] = cat_totals.get(r["category"], 0) + r["amount"]

    top_category = max(cat_totals, key=cat_totals.get) if cat_totals else "—"

    user = {
        "name": row["name"],
        "email": row["email"],
        "member_since": member_since,
        "initials": initials,
    }
    stats = {
        "total_spent": total_spent,
        "transaction_count": transaction_count,
        "top_category": top_category,
    }
    transactions = [
        {
            "date": r["date"],
            "description": r["description"] or "",
            "category": r["category"],
            "amount": r["amount"],
        }
        for r in expense_rows[:5]
    ]
    categories = sorted(
        [
            {
                "name": k,
                "total": v,
                "pct": round(v / total_spent * 100) if total_spent else 0,
            }
            for k, v in cat_totals.items()
        ],
        key=lambda c: c["total"],
        reverse=True,
    )

    return render_template("profile.html", user=user, stats=stats,
                           transactions=transactions, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
