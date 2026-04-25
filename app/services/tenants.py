from app.services.saas_tracking import get_conn, init_db, USE_POSTGRES

def init_tenants():
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    id_type = "SERIAL PRIMARY KEY" if USE_POSTGRES else "INTEGER PRIMARY KEY AUTOINCREMENT"

    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS tenants (
        id {id_type},
        name TEXT,
        subdomain TEXT UNIQUE,
        logo_url TEXT,
        primary_color TEXT,
        stripe_account TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def get_tenant(request):
    init_tenants()
    tenant_param = request.query_params.get("tenant")
    host = request.headers.get("host","")
    sub = tenant_param or host.split(".")[0]

    conn = get_conn()
    cur = conn.cursor()

    if USE_POSTGRES:
        cur.execute("SELECT name, logo_url, primary_color FROM tenants WHERE subdomain=%s", (sub,))
    else:
        cur.execute("SELECT name, logo_url, primary_color FROM tenants WHERE subdomain=?", (sub,))

    row = cur.fetchone()
    conn.close()

    if row:
        return {"name": row[0], "logo": row[1] or "", "color": row[2] or "#2563eb", "subdomain": sub}

    return {"name": "Default Intelligence System", "logo": "", "color": "#2563eb", "subdomain": sub}
