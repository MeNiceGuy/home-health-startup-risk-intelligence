from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/audit-success", response_class=HTMLResponse)
def audit_success(lead_id: str = "", email: str = "", agency: str = "Your Agency"):

    if lead_id:
        from app.services.lead_tracking import log_lead_event
        log_lead_event(lead_id, agency, email, "audit_paid")

    return """
    <html>
    <body style="font-family:Arial;background:#f8fafc;margin:0;color:#111827;">

        <h1>Audit Purchased</h1>
        <p>Your audit is ready.</p>

        <a href="/operating-audit">View Audit</a>

        <h2>Next Step</h2>
        <p>Your audit identifies problems. It does not fix them.</p>

        <a href="/cart/add/full-optimization">Fix the Gaps ($1,999)</a>

    </body>
    </html>
    """

