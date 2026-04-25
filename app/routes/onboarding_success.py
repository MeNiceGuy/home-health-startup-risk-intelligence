from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse
from app.services.tenants import init_tenants, get_conn, USE_POSTGRES
import stripe
import re

router = APIRouter(prefix="/onboard", tags=["Onboarding Success"])

def clean_subdomain(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())[:20]

@router.get("/success", response_class=HTMLResponse)
def onboard_success(session_id: str = Query(...)):
    session = stripe.checkout.Session.retrieve(session_id)

    if session.get("payment_status") != "paid":
        return "<h1>Payment not confirmed yet. Please refresh.</h1>"

    data = session.get("metadata", {})
    name = data.get("name", "Consultant Platform")
    email = data.get("email", "")
    color = data.get("color", "#2563eb")
    stripe_account = data.get("stripe_account", "")
    subdomain = clean_subdomain(name)

    init_tenants()
    conn = get_conn()
    cur = conn.cursor()

    if USE_POSTGRES:
        cur.execute("""
        INSERT INTO tenants (name, subdomain, primary_color, stripe_account)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (subdomain) DO NOTHING
        """, (name, subdomain, color, stripe_account))
    else:
        cur.execute("""
        INSERT OR IGNORE INTO tenants (name, subdomain, primary_color, stripe_account)
        VALUES (?, ?, ?, ?)
        """, (name, subdomain, color, stripe_account))

    conn.commit()
    conn.close()

    return f"""
    <html>
    <body style="font-family:Arial;background:#f8fafc;padding:40px;">
    <div style="max-width:800px;margin:auto;background:white;padding:35px;border-radius:18px;">
        <h1>Your White-Label Platform Is Active</h1>
        <p><strong>Brand:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Monthly Plan:</strong> $199/month</p>
        <a href="/consultant/dashboard?tenant={subdomain}"
        style="background:{color};color:white;padding:14px 20px;border-radius:10px;text-decoration:none;">
        Open Consultant Dashboard
        </a>
    </div>
    </body>
    </html>
    """
