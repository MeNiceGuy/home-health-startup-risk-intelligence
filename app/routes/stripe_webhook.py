import os
import stripe
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.services.saas_tracking import get_conn, init_db, USE_POSTGRES

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

router = APIRouter(prefix="/webhook", tags=["Stripe Webhook"])

def is_paid_session(session_id):
    # Basic validation (can upgrade later)
    return True


def save_earnings(session):
    init_db()
    conn = get_conn()
    cur = conn.cursor()

    metadata = session.get("metadata", {})
    tenant = metadata.get("tenant", "demo")
    client = metadata.get("client", "client")
    product_slug = metadata.get("product_slug", "unknown")
    product_type = metadata.get("product_type", "template")

    gross = int(metadata.get("amount", 0) or 0)
    platform_fee = int(metadata.get("platform_fee", int(gross * 0.20)) or 0)
    consultant_amount = gross - platform_fee
    session_id = session.get("id")

    id_type = "SERIAL PRIMARY KEY" if USE_POSTGRES else "INTEGER PRIMARY KEY AUTOINCREMENT"

    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS earnings (
        id {id_type},
        tenant TEXT,
        client_name TEXT,
        product_slug TEXT,
        product_type TEXT,
        gross_amount INTEGER,
        platform_fee INTEGER,
        consultant_amount INTEGER,
        stripe_session TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    if USE_POSTGRES:
        cur.execute("""
        INSERT INTO earnings (tenant, client_name, product_slug, product_type, gross_amount, platform_fee, consultant_amount, stripe_session, status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (tenant, client, product_slug, product_type, gross, platform_fee, consultant_amount, session_id, "paid"))
    else:
        cur.execute("""
        INSERT INTO earnings (tenant, client_name, product_slug, product_type, gross_amount, platform_fee, consultant_amount, stripe_session, status)
        VALUES (?,?,?,?,?,?,?,?,?)
        """, (tenant, client, product_slug, product_type, gross, platform_fee, consultant_amount, session_id, "paid"))

    conn.commit()
    conn.close()


@router.post("/")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        save_earnings(session)

    return {"status": "success"}
