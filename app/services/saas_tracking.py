import sqlite3
from datetime import datetime

DB_PATH = "app_data.db"

def init_saas_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_email TEXT,
        stripe_session_id TEXT,
        status TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS intelligence_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agency_name TEXT,
        audit_type TEXT,
        total_score INTEGER,
        compliance_score INTEGER,
        clinical_score INTEGER,
        revenue_score INTEGER,
        operations_score INTEGER,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_subscription(email, session_id, status="active"):
    init_saas_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO subscriptions (customer_email, stripe_session_id, status, created_at)
    VALUES (?, ?, ?, ?)
    """, (email, session_id, status, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def save_intelligence_score(agency, audit_type, total, compliance, clinical, revenue, operations):
    init_saas_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO intelligence_scores
    (agency_name, audit_type, total_score, compliance_score, clinical_score, revenue_score, operations_score, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (agency, audit_type, total, compliance, clinical, revenue, operations, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_dashboard_data():
    init_saas_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT customer_email, status, created_at FROM subscriptions ORDER BY id DESC")
    subs = cur.fetchall()

    cur.execute("""
    SELECT agency_name, audit_type, total_score, compliance_score, clinical_score, revenue_score, operations_score, created_at
    FROM intelligence_scores
    ORDER BY id DESC
    """)
    scores = cur.fetchall()

    conn.close()
    return subs, scores
