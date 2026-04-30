from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse, HTMLResponse
from app.services.subscription import create_subscription_checkout
from app.services.saas_tracking import save_subscription
import stripe

router = APIRouter(prefix="/subscribe", tags=["Subscription"])

@router.get("/")
def subscribe():
    url = create_subscription_checkout()
    return RedirectResponse(url)

@router.get("/success", response_class=HTMLResponse)
def subscription_success(session_id: str = Query(None)):
    email = "unknown"

    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            email = session.get("customer_details", {}).get("email", "unknown")
        except Exception:
            email = "unknown"

    save_subscription(email, session_id or "N/A", "active")

    return """
    <html>
    <body style="font-family:Arial;padding:40px;">
        <h1>Subscription Activated</h1>
        <p>Your Operating Intelligence subscription is active.</p>
        <a href="/dashboard/">Go to Dashboard</a>
    </body>
    </html>
    """


