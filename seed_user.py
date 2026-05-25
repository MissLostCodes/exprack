import os, random, string, datetime
from werkzeug.security import generate_password_hash
from database.db import get_db, init_db

# Ensure DB and tables exist
init_db()

first_names = [
    "Aarav", "Vihaan", "Rohan", "Arjun", "Kabir", "Lakshya", "Aditya", "Ishaan", "Karan", "Manav",
    "Priya", "Ananya", "Isha", "Kavya", "Mira", "Nisha", "Pooja", "Riya", "Sana", "Tara"
]
last_names = [
    "Sharma", "Patel", "Singh", "Kumar", "Gupta", "Mehta", "Joshi", "Reddy", "Mishra", "Verma",
    "Chopra", "Desai", "Bhatia", "Nair", "Goyal", "Kapoor", "Agarwal", "Saxena", "Bhat", "Rathod"
]

def generate_user():
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    # email derived from name lowercased, replace spaces with dot, add random 2-3 digits
    base = name.lower().replace(' ', '.')
    suffix = str(random.randint(10, 999))
    email = f"{base}{suffix}@gmail.com"
    password_hash = generate_password_hash('password123')
    created_at = datetime.datetime.utcnow().isoformat()
    return name, email, password_hash, created_at

conn = get_db()
cur = conn.cursor()

while True:
    name, email, password_hash, created_at = generate_user()
    cur.execute('SELECT 1 FROM users WHERE email = ?', (email,))
    if not cur.fetchone():
        cur.execute(
            'INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)',
            (name, email, password_hash, created_at)
        )
        user_id = cur.lastrowid
        conn.commit()
        print(f"Inserted user:\n  id: {user_id}\n  name: {name}\n  email: {email}")
        break

conn.close()
