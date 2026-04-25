import os
import sqlite3
import psycopg

DATABASE_URL = os.getenv("DATABASE_URL")
USE_POSTGRES = bool(DATABASE_URL)

def get_conn():
    if USE_POSTGRES:
        return psycopg.connect(DATABASE_URL)
    return sqlite3.connect("fallback.db")

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    id_type = "SERIAL PRIMARY KEY" if USE_POSTGRES else "INTEGER PRIMARY KEY AUTOINCREMENT"

    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS users (
        id {id_type},
        email TEXT UNIQUE,
        password_hash TEXT
    )
    """)

    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id {id_type},
        customer_email TEXT,
        stripe_session_id TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS intelligence_scores (
        id {id_type},
        agency_name TEXT,
        audit_type TEXT,
        total_score INTEGER,
        compliance_score INTEGER,
        clinical_score INTEGER,
        revenue_score INTEGER,
        operations_score INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def save_subscription(email, session_id, status="active"):
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    sql = "INSERT INTO subscriptions (customer_email, stripe_session_id, status) VALUES ({}, {}, {})"

    if USE_POSTGRES:
        cur.execute(sql.format("%s", "%s", "%s"), (email, session_id, status))
    else:
        cur.execute(sql.format("?", "?", "?"), (email, session_id, status))

    conn.commit()
    conn.close()

def save_intelligence_score(agency, audit_type, total, compliance, clinical, revenue, operations):
    init_db()
    conn = get_conn()
    cur = conn.cursor()

    if USE_POSTGRES:
        cur.execute("""
        INSERT INTO intelligence_scores
        (agency_name, audit_type, total_score, compliance_score, clinical_score, revenue_score, operations_score)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (agency, audit_type, total, compliance, clinical, revenue, operations))
    else:
        cur.execute("""
        INSERT INTO intelligence_scores
        (agency_name, audit_type, total_score, compliance_score, clinical_score, revenue_score, operations_score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (agency, audit_type, total, compliance, clinical, revenue, operations))

    conn.commit()
    conn.close()

def get_dashboard_data():
    init_db()
    conn = get_conn()
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
