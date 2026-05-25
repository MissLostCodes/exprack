from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = "dev-secret-key"

# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    from database.db import get_db
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        if not (name and email and password):
            error = "All fields are required."
            return render_template("register.html", error=error)
        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, generate_password_hash(password)),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            error = "Email already registered."
            return render_template("register.html", error=error)
        # Log the user in (simple session)
        user_row = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        session["user_id"] = user_row["id"]
        return redirect(url_for("landing"))
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/logout")
def logout():
    return "Logout — coming in Step 3"

@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"

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
