import os
import sqlite3

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

    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "member_since": "June 2026",
        "initials": "DU",
    }
    stats = {
        "total_spent": 392.49,
        "transaction_count": 8,
        "top_category": "Bills",
    }
    transactions = [
        {"date": "Jun 15", "description": "Restaurant dinner", "category": "Food",          "amount": 55.00},
        {"date": "Jun 11", "description": "New shoes",         "category": "Shopping",      "amount": 89.99},
        {"date": "Jun 09", "description": "Cinema tickets",    "category": "Entertainment", "amount": 25.00},
        {"date": "Jun 07", "description": "Pharmacy",          "category": "Health",        "amount": 35.00},
        {"date": "Jun 05", "description": "Electricity bill",  "category": "Bills",         "amount": 120.00},
    ]
    categories = [
        {"name": "Bills",         "total": 120.00, "pct": 31},
        {"name": "Food",          "total": 97.50,  "pct": 25},
        {"name": "Shopping",      "total": 89.99,  "pct": 23},
        {"name": "Health",        "total": 35.00,  "pct": 9},
        {"name": "Entertainment", "total": 25.00,  "pct": 6},
        {"name": "Transport",     "total": 15.00,  "pct": 4},
        {"name": "Other",         "total": 10.00,  "pct": 3},
    ]
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
