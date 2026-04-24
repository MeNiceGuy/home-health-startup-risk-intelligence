import sqlite3
from datetime import datetime

DB_PATH = "app_data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_email TEXT,
        kit_slug TEXT,
        stripe_session_id TEXT,
        purchase_date TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_purchase(customer_email, kit_slug, stripe_session_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO purchases (customer_email, kit_slug, stripe_session_id, purchase_date)
    VALUES (?, ?, ?, ?)
    """, (customer_email, kit_slug, stripe_session_id, datetime.now().isoformat()))

    conn.commit()
    conn.close()

def get_purchases():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT customer_email, kit_slug, stripe_session_id, purchase_date FROM purchases ORDER BY id DESC")
    rows = cur.fetchall()

    conn.close()
    return rows
