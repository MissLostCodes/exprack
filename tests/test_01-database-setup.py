import os
import sqlite3
import pytest

from expense_tracker.database.db import get_db, init_db, seed_db

# Use a temporary database file for isolation
TEST_DB = "test_expense_tracker.db"

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Point the DB helper to a temporary file
    original_db_path = os.getenv("EXPENSE_DB_PATH", "expense_tracker.db")
    os.environ["EXPENSE_DB_PATH"] = TEST_DB
    # Ensure a clean start
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    # Initialize and seed
    init_db()
    seed_db()
    yield
    # Cleanup after test suite
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    os.environ["EXPENSE_DB_PATH"] = original_db_path

def get_connection():
    conn = sqlite3.connect(TEST_DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def test_db_initialization():
    conn = get_connection()
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    assert cur.fetchone() is not None
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expenses'")
    assert cur.fetchone() is not None
    conn.close()

def test_insert_expense():
    conn = get_connection()
    # Get demo user id
    user_id = conn.execute("SELECT id FROM users WHERE email='demo@spendly.com'").fetchone()["id"]
    conn.execute(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?,?,?,?,?)",
        (user_id, 12.34, 'Food', '2024-01-01', 'Lunch')
    )
    conn.commit()
    row = conn.execute("SELECT * FROM expenses WHERE user_id=?", (user_id,)).fetchone()
    assert row is not None
    assert row["amount"] == 12.34
    conn.close()

def test_query_expenses():
    conn = get_connection()
    user_id = conn.execute("SELECT id FROM users WHERE email='demo@spendly.com'").fetchone()["id"]
    # Insert two expenses
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?,?,?,?,?)",
        [
            (user_id, 5.0, 'Transport', '2024-01-02', 'Bus'),
            (user_id, 20.0, 'Bills', '2024-01-03', 'Electricity')
        ]
    )
    conn.commit()
    rows = conn.execute("SELECT * FROM expenses WHERE user_id=?", (user_id,)).fetchall()
    assert len(rows) == 2
    conn.close()

def test_db_cleanup():
    conn = get_connection()
    conn.close()
