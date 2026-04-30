from app.services.saas_tracking import get_conn, init_db, USE_POSTGRES
from app.services.tenants import init_tenants

def get_tenant_stripe_account(tenant):
    init_tenants()
    conn = get_conn()
    cur = conn.cursor()

    if USE_POSTGRES:
        cur.execute("SELECT stripe_account FROM tenants WHERE subdomain=%s", (tenant,))
    else:
        cur.execute("SELECT stripe_account FROM tenants WHERE subdomain=?", (tenant,))

    row = cur.fetchone()
    conn.close()

    if row and row[0]:
        return row[0]

    return ""


