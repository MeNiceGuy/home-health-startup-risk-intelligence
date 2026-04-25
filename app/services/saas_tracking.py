import os
import psycopg
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")
    return psycopg.connect(DATABASE_URL)

def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id SERIAL PRIMARY KEY,
                customer_email TEXT,
                stripe_session_id TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS purchases (
                id SERIAL PRIMARY KEY,
                customer_email TEXT,
                kit_slug TEXT,
                stripe_session_id TEXT,
                file_path TEXT,
                purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS intelligence_scores (
                id SERIAL PRIMARY KEY,
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

def save_subscription(email, session_id, status="active"):
    init_db()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO subscriptions (customer_email, stripe_session_id, status)
            VALUES (%s, %s, %s)
            """, (email, session_id, status))
            conn.commit()

def save_purchase(customer_email, kit_slug, stripe_session_id, file_path):
    init_db()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO purchases (customer_email, kit_slug, stripe_session_id, file_path)
            VALUES (%s, %s, %s, %s)
            """, (customer_email, kit_slug, stripe_session_id, file_path))
            conn.commit()

def save_intelligence_score(agency, audit_type, total, compliance, clinical, revenue, operations):
    init_db()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO intelligence_scores
            (agency_name, audit_type, total_score, compliance_score, clinical_score, revenue_score, operations_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (agency, audit_type, total, compliance, clinical, revenue, operations))
            conn.commit()

def get_dashboard_data():
    init_db()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT customer_email, status, created_at FROM subscriptions ORDER BY id DESC")
            subs = cur.fetchall()

            cur.execute("""
            SELECT agency_name, audit_type, total_score, compliance_score, clinical_score, revenue_score, operations_score, created_at
            FROM intelligence_scores
            ORDER BY id DESC
            """)
            scores = cur.fetchall()

    return subs, scores
