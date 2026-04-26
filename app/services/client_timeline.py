from app.services.saas_tracking import get_conn, init_db, USE_POSTGRES
from datetime import datetime

def init_timeline_db():
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    id_type = "SERIAL PRIMARY KEY" if USE_POSTGRES else "INTEGER PRIMARY KEY AUTOINCREMENT"

    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS client_timeline (
        id {id_type},
        tenant TEXT,
        client_name TEXT,
        event_type TEXT,
        title TEXT,
        detail TEXT,
        link TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def add_timeline_event(tenant, client_name, event_type, title, detail="", link=""):
    init_timeline_db()
    conn = get_conn()
    cur = conn.cursor()
    p = "%s" if USE_POSTGRES else "?"

    cur.execute(
        f"INSERT INTO client_timeline (tenant, client_name, event_type, title, detail, link) VALUES ({p}, {p}, {p}, {p}, {p}, {p})",
        (tenant, client_name, event_type, title, detail, link)
    )

    conn.commit()
    conn.close()

def get_client_timeline(tenant, client_name):
    init_timeline_db()
    conn = get_conn()
    cur = conn.cursor()
    p = "%s" if USE_POSTGRES else "?"

    cur.execute(
        f"""
        SELECT event_type, title, detail, link, created_at
        FROM client_timeline
        WHERE tenant={p} AND client_name={p}
        ORDER BY created_at DESC
        """,
        (tenant, client_name)
    )

    rows = cur.fetchall()
    conn.close()
    return rows
