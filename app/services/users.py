import sqlite3
from passlib.hash import bcrypt

DB = "app_data.db"

def init_users_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password_hash TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def create_user(email, password):
    init_users_db()
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        (email, bcrypt.hash(password))
    )
    conn.commit()
    conn.close()

def verify_user(email, password):
    init_users_db()
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash FROM users WHERE email=?", (email,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    user_id, password_hash = row
    if bcrypt.verify(password, password_hash):
        return {"id": user_id, "email": email}

    return None
