from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/audit-checkout", response_class=HTMLResponse)
def audit_checkout(lead_id: str = "", email: str = "", agency: str = "Your Agency"):

    if lead_id:
        from app.services.lead_tracking import log_lead_event
        log_lead_event(lead_id, agency, email, "checkout_started")

    return """
    <html>
    <body style="font-family:Arial;background:#f8fafc;margin:0;color:#111827;">

        <h1>Full Audit Checkout</h1>
        <p>Unlock your full revenue performance audit.</p>

        <a href="/create-checkout-session">Proceed to Payment</a>

    </body>
    </html>
    """

