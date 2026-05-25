# Students will write this file in Step 1 — Database Setup
# This file should contain:
#   get_db()   — returns a SQLite connection with row_factory and foreign keys enabled
#   init_db()  — creates all tables using CREATE TABLE IF NOT EXISTS
#   seed_db()  — inserts sample data for development
import os
import sqlite3
from werkzeug.security import generate_password_hash

# Path to the SQLite database file (placed in project root)
_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "expense_tracker.db")

def get_db():
    """Return a SQLite connection with dict‑style rows and foreign keys enabled."""
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Create the users and expenses tables if they do not exist."""
    schema_users = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );
    """
    schema_expenses = """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """
    conn = get_db()
    conn.executescript(schema_users + schema_expenses)
    conn.commit()
    conn.close()

def seed_db():
    """Insert a demo user and sample expenses if the database is empty."""
    conn = get_db()
    cur = conn.cursor()
    # Check if a user already exists
    cur.execute("SELECT 1 FROM users LIMIT 1")
    if cur.fetchone():
        conn.close()
        return
    # Insert demo user
    password_hash = generate_password_hash('demo123')
    cur.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash)
    )
    user_id = cur.lastrowid
    # Sample expenses data
    expenses = [
        (user_id, 12.5, 'Food', '2026-05-01', 'Lunch'),
        (user_id, 45.0, 'Transport', '2026-05-02', 'Taxi'),
        (user_id, 80.0, 'Bills', '2026-05-03', 'Electricity'),
        (user_id, 30.0, 'Health', '2026-05-04', 'Medicine'),
        (user_id, 60.0, 'Entertainment', '2026-05-05', 'Movie'),
        (user_id, 150.0, 'Shopping', '2026-05-06', 'Clothes'),
        (user_id, 20.0, 'Other', '2026-05-07', 'Gift'),
        (user_id, 25.0, 'Food', '2026-05-08', 'Dinner')
    ]
    cur.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses
    )
    conn.commit()
    conn.close()

# This file should contain:
#   get_db()   — returns a SQLite connection with row_factory and foreign keys enabled
#   init_db()  — creates all tables using CREATE TABLE IF NOT EXISTS
#   seed_db()  — inserts sample data for development

