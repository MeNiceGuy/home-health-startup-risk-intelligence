from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse
from app.services.saas_tracking import get_conn, init_db, USE_POSTGRES

router = APIRouter(prefix="/earnings", tags=["Earnings Dashboard"])

def init_earnings_db():
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    id_type = "SERIAL PRIMARY KEY" if USE_POSTGRES else "INTEGER PRIMARY KEY AUTOINCREMENT"

    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS earnings (
        id {id_type},
        tenant TEXT,
        client_name TEXT,
        product_slug TEXT,
        product_type TEXT,
        gross_amount INTEGER DEFAULT 0,
        platform_fee INTEGER DEFAULT 0,
        consultant_amount INTEGER DEFAULT 0,
        stripe_session TEXT,
        status TEXT DEFAULT 'paid',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def get_earnings(tenant):
    init_earnings_db()
    conn = get_conn()
    cur = conn.cursor()
    p = "%s" if USE_POSTGRES else "?"

    cur.execute(f"""
        SELECT client_name, product_slug, product_type, gross_amount, platform_fee, consultant_amount, created_at
        FROM earnings
        WHERE tenant={p}
        ORDER BY id DESC
    """, (tenant,))
    rows = cur.fetchall()

    gross = sum(int(r[3] or 0) for r in rows)
    platform = sum(int(r[4] or 0) for r in rows)
    consultant = sum(int(r[5] or 0) for r in rows)

    conn.close()
    return rows, gross, platform, consultant

@router.get("/", response_class=HTMLResponse)
def earnings_dashboard(tenant: str = Query("demo")):
    rows, gross, platform, consultant = get_earnings(tenant)

    table_rows = ""
    for r in rows:
        table_rows += f"""
        <tr>
            <td>{r[0]}</td>
            <td>{r[1]}</td>
            <td>{r[2]}</td>
            <td>${int(r[3] or 0)/100:.2f}</td>
            <td>${int(r[5] or 0)/100:.2f}</td>
            <td>${int(r[4] or 0)/100:.2f}</td>
            <td>{str(r[6])[:19]}</td>
        </tr>
        """

    if not table_rows:
        table_rows = "<tr><td colspan='7'>No earnings recorded yet.</td></tr>"

    return f"""
    <html>
    <body style="font-family:Arial;background:#f8fafc;padding:40px;">
    <div style="max-width:1100px;margin:auto;">
        <h1>Consultant Earnings Dashboard</h1>
        <p><strong>Tenant:</strong> {tenant}</p>

        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-bottom:25px;">
            <div style="background:white;padding:24px;border-radius:18px;"><h3>Gross Sales</h3><h1>${gross/100:.2f}</h1></div>
            <div style="background:white;padding:24px;border-radius:18px;"><h3>Consultant Earnings</h3><h1>${consultant/100:.2f}</h1></div>
            <div style="background:white;padding:24px;border-radius:18px;"><h3>Platform Revenue</h3><h1>${platform/100:.2f}</h1></div>
        </div>

        <div style="background:white;padding:24px;border-radius:18px;">
            <h2>Transaction History</h2>
            <table style="width:100%;border-collapse:collapse;">
                <tr>
                    <th>Client</th><th>Product</th><th>Type</th><th>Gross</th><th>Consultant</th><th>Platform</th><th>Date</th>
                </tr>
                {table_rows}
            </table>
        </div>

        <br>
        <a href="/consultant/dashboard?tenant={tenant}">Back to Consultant Dashboard</a>
    </div>
    </body>
    </html>
    """


