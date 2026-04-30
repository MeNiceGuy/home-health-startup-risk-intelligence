import os
import stripe
from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse, HTMLResponse
from app.services.saas_tracking import get_conn, init_db, USE_POSTGRES
from app.services.settings import BASE_URL

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter(prefix="/stripe-connect", tags=["Stripe Connect"])

def get_tenant_account(tenant):
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    p = "%s" if USE_POSTGRES else "?"

    cur.execute(f"SELECT stripe_account FROM tenants WHERE subdomain={p}", (tenant,))
    row = cur.fetchone()
    conn.close()

    return row[0] if row and row[0] else ""

def save_tenant_account(tenant, account_id):
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    p = "%s" if USE_POSTGRES else "?"

    cur.execute(
        f"UPDATE tenants SET stripe_account={p} WHERE subdomain={p}",
        (account_id, tenant)
    )

    conn.commit()
    conn.close()

@router.get("/start")
def start_connect(tenant: str = Query("demo"), email: str = Query("")):
    account_id = get_tenant_account(tenant)

    if not account_id:
        account = stripe.Account.create(
            type="express",
            email=email if email else None,
            capabilities={
                "card_payments": {"requested": True},
                "transfers": {"requested": True}
            },
            business_type="individual"
        )

        account_id = account["id"]
        save_tenant_account(tenant, account_id)

    account_link = stripe.AccountLink.create(
        account=account_id,
        refresh_url=f"{BASE_URL}/stripe-connect/refresh?tenant={tenant}",
        return_url=f"{BASE_URL}/stripe-connect/return?tenant={tenant}",
        type="account_onboarding"
    )

    return RedirectResponse(account_link["url"])

@router.get("/refresh")
def refresh_connect(tenant: str = Query("demo")):
    return RedirectResponse(f"/stripe-connect/start?tenant={tenant}")

@router.get("/return", response_class=HTMLResponse)
def connect_return(tenant: str = Query("demo")):
    return f"""
    <html>
    <body style="font-family:Arial;background:#f8fafc;padding:40px;">
    <div style="max-width:750px;margin:auto;background:white;padding:35px;border-radius:18px;">
        <h1>Stripe Connect Setup Started</h1>
        <p>Your consultant payout account has been connected or onboarding has started.</p>
        <p>Stripe may require identity and banking verification before payouts activate.</p>
        <a href="/consultant/dashboard?tenant={tenant}"
        style="background:#2563eb;color:white;padding:14px 20px;border-radius:10px;text-decoration:none;">
        Back to Consultant Dashboard
        </a>
    </div>
    </body>
    </html>
    """


