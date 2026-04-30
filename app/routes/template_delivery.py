from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import os
import stripe

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")

def add_timeline_event(*args, **kwargs):
    return None

TEMPLATES = {
    "operations": {
        "title": "Operations Workflow System",
        "items": [
            "Intake checklist",
            "Scheduling control process",
            "Missed visit tracking log",
            "Daily operations review cadence"
        ]
    },
    "compliance": {
        "title": "Compliance Readiness Pack",
        "items": [
            "Compliance audit checklist",
            "Incident reporting workflow",
            "Policy review schedule",
            "Internal QA monitoring process"
        ]
    },
    "hiring": {
        "title": "Hiring & Onboarding Kit",
        "items": [
            "Hiring pipeline tracker",
            "New hire onboarding checklist",
            "Retention risk review",
            "Backup staffing plan"
        ]
    },
    "revenue": {
        "title": "Revenue Cycle Policy Pack",
        "items": [
            "Denial prevention checklist",
            "Pre-billing QA review",
            "A/R follow-up workflow",
            "Revenue leakage tracker"
        ]
    }
}

def verify_payment(session_id: str):
    dev_key = os.getenv("DEV_BYPASS_KEY", "")

    if dev_key and session_id == dev_key:
        return True
    if not session_id or not session_id.startswith("cs_"):
        return False

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session.payment_status == "paid"
    except Exception:
        return False

@router.get("/templates/{slug}", response_class=HTMLResponse)
def generate_template(slug: str, session_id: str = ""):
    paid = verify_payment(session_id)

    if not paid:
        return """
        <html>
        <body style='font-family:Arial;padding:40px;background:#f8fafc;'>
            <div style='max-width:720px;margin:auto;background:white;padding:35px;border-radius:18px;box-shadow:0 8px 24px rgba(0,0,0,.08);'>
                <h1>Payment Verification Required</h1>
                <p>This template is locked until Stripe confirms payment.</p>
                <a href='/template-checkout/operations' style='display:inline-block;background:#dc2626;color:white;padding:14px 20px;border-radius:10px;text-decoration:none;font-weight:bold;'>
                    Return to Checkout
                </a>
            </div>
        </body>
        </html>
        """

    template = TEMPLATES.get(slug, TEMPLATES["operations"])

    add_timeline_event("demo", "client", "Template Purchased", "Client purchased template", f"Template: {slug}", "")

    items_html = ""
    for item in template["items"]:
        items_html += f"<li>{item}</li>"

    return f"""
    <html>
    <body style='font-family:Arial;padding:40px;background:#f8fafc;'>
        <div style='max-width:820px;margin:auto;background:white;padding:35px;border-radius:18px;box-shadow:0 8px 24px rgba(0,0,0,.08);'>
            <h1>{template["title"]}</h1>
            <p>This paid template pack is designed to help home health agencies reduce operational risk and improve execution.</p>
            <h2>Included Tools</h2>
            <ul>{items_html}</ul>
            <hr>
            <p><strong>Next Step:</strong> Implement these tools inside your agency workflow and track weekly improvement.</p>
            <a href='/consultant/dashboard?tenant=demo'><hr>
<h2>Recover Your Lost Revenue Faster</h2>
<p>Most agencies struggle to implement these systems correctly. We help you fix it in 14 days.</p>

<a href="/upsell/consulting"
   style="display:inline-block;background:#16a34a;color:white;padding:16px 24px;border-radius:12px;font-weight:bold;text-decoration:none;margin-top:20px;">
   Book Strategy Call ($2,999 Implementation Plan)
</a>

<br><br>
<a href='/consultant/dashboard?tenant=demo'>Return to Dashboard</a></a>
        </div>
    </body>
    </html>
    """




