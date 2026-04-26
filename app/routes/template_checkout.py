import os
import stripe
from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse
from app.services.settings import FREE_MODE, BASE_URL
from app.services.saas_tracking import get_conn, init_db, USE_POSTGRES

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter(prefix="/template-checkout", tags=["Template Checkout"])

PRODUCTS = {
    "revenue": {"name": "Revenue Cycle Starter Kit", "price": 19900},
    "operations": {"name": "Operations Workflow Kit", "price": 19900},
    "hiring": {"name": "Hiring & Retention Kit", "price": 17900},
    "compliance": {"name": "Compliance Policy Pack", "price": 19900}
}

def get_stripe_account(tenant):
    if not tenant:
        return ""

    init_db()
    conn = get_conn()
    cur = conn.cursor()
    p = "%s" if USE_POSTGRES else "?"

    cur.execute(f"SELECT stripe_account FROM tenants WHERE subdomain={p}", (tenant,))
    row = cur.fetchone()
    conn.close()

    return row[0] if row and row[0] else ""

@router.get("/{slug}")
def template_checkout(slug: str, tenant: str = Query(""), client: str = Query("")):
    product = PRODUCTS.get(slug)

    if not product:
        return {"error": "Template not found"}

    if FREE_MODE:
        return RedirectResponse(f"/templates/{slug}?session_id=free-demo-{slug}", status_code=303)

    stripe_account = get_stripe_account(tenant)
    platform_fee = int(product["price"] * 0.20)

    session_args = {
        "mode": "payment",
        "payment_method_types": ["card"],
        "line_items": [{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": product["name"]},
                "unit_amount": product["price"]
            },
            "quantity": 1
        }],
        "success_url": f"{BASE_URL}/templates/{slug}?session_id={{CHECKOUT_SESSION_ID}}",
        "cancel_url": f"{BASE_URL}/consultant/dashboard?tenant={tenant}",
        "metadata": {
            "product_slug": slug,
            "product_type": "template",
            "tenant": tenant,
            "client": client,
            "amount": str(product["price"]),
            "platform_fee": str(platform_fee)
        }
    }

    if stripe_account:
        session_args["payment_intent_data"] = {
            "application_fee_amount": platform_fee,
            "transfer_data": {
                "destination": stripe_account
            }
        }

    session = stripe.checkout.Session.create(**session_args)
    return RedirectResponse(session.url)
