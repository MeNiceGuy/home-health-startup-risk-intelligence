from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.services.saas_tracking import get_conn, init_db, USE_POSTGRES
import os
import stripe

router = APIRouter(prefix="/stripe", tags=["Stripe Webhooks"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

def init_purchase_db():
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    id_type = "SERIAL PRIMARY KEY" if USE_POSTGRES else "INTEGER PRIMARY KEY AUTOINCREMENT"

    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS purchases (
        id {id_type},
        session_id TEXT UNIQUE,
        customer_email TEXT,
        product_slug TEXT,
        product_type TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def save_paid_purchase(session):
    init_purchase_db()
    conn = get_conn()
    cur = conn.cursor()

    session_id = session.get("id")
    customer_email = session.get("customer_details", {}).get("email", "unknown")
    product_slug = session.get("metadata", {}).get("product_slug", "unknown")
    product_type = session.get("metadata", {}).get("product_type", "template")
    status = "paid"

    if USE_POSTGRES:
        cur.execute("""
        INSERT INTO purchases (session_id, customer_email, product_slug, product_type, status)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (session_id) DO NOTHING
        """, (session_id, customer_email, product_slug, product_type, status))
    else:
        cur.execute("""
        INSERT OR IGNORE INTO purchases (session_id, customer_email, product_slug, product_type, status)
        VALUES (?, ?, ?, ?, ?)
        """, (session_id, customer_email, product_slug, product_type, status))

    conn.commit()
    conn.close()

def is_paid_session(session_id, slug):
    init_purchase_db()
    conn = get_conn()
    cur = conn.cursor()

    if USE_POSTGRES:
        cur.execute(
            "SELECT status FROM purchases WHERE session_id=%s AND product_slug=%s",
            (session_id, slug)
        )
    else:
        cur.execute(
            "SELECT status FROM purchases WHERE session_id=? AND product_slug=?",
            (session_id, slug)
        )

    row = cur.fetchone()
    conn.close()
    return row and row[0] == "paid"

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        if WEBHOOK_SECRET:
            event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
        else:
            event = stripe.Event.construct_from(await request.json(), stripe.api_key)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        if session.get("payment_status") == "paid":
            save_paid_purchase(session)

    return {"received": True}
