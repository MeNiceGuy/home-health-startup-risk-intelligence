from fastapi import APIRouter
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
import os
import stripe
from app.services.pdf_engine import generate_paid_audit_pdf

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "os.getenv("STRIPE_SECRET_KEY")")

def create_checkout(name: str, amount: int):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": name},
                "unit_amount": amount,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://127.0.0.1:8000/success",
        cancel_url="http://127.0.0.1:8000/cancel",
    )
    return RedirectResponse(session.url)

@router.get("/checkout/audit")
def audit_checkout():
    return create_checkout("Home Health Audit Report", 4900)

@router.get("/checkout/fix-plan")
def fix_plan_checkout():
    return create_checkout("Custom Fix Plan", 9900)

@router.get("/checkout/full-system")
def full_system_checkout():
    return create_checkout("Full Agency Optimization System", 299900)

@router.get("/success", response_class=HTMLResponse)
def success():
    return """
    <html>
    <body style='font-family:Arial;padding:40px;background:#f8fafc;'>
        <div style='max-width:760px;margin:auto;background:white;padding:35px;border-radius:18px;box-shadow:0 8px 24px rgba(0,0,0,.08);'>
            <h1 style='color:#16a34a;'>Payment Successful</h1>
            <p>Your paid audit report is ready.</p>
            <a href='/download/paid-audit-report' style='display:inline-block;background:#dc2626;color:white;padding:14px 20px;border-radius:10px;text-decoration:none;font-weight:bold;'>
                Download Paid Audit Report
            </a>
            <br><br>
            <a href='/checkout/full-system' style='display:inline-block;background:#111827;color:white;padding:14px 20px;border-radius:10px;text-decoration:none;font-weight:bold;'>
                Upgrade to Full Agency Optimization System
            </a>
        </div>
    </body>
    </html>
    """

@router.get("/cancel", response_class=HTMLResponse)
def cancel():
    return """
    <h1>Payment Cancelled</h1>
    <p>You can return to your audit report anytime.</p>
    <a href='/'>Return Home</a>
    """

@router.get("/download/paid-audit-report")
def download_paid_audit_report():
    from fastapi.responses import FileResponse
    from app.services.pdf_engine import generate_audit_pdf

    path = generate_audit_pdf(
        {"score": 56},
        ["Fix intake delays", "Reduce denials", "Improve staffing"]
    )

    return FileResponse(path, media_type="application/pdf", filename="audit_report.pdf")




@router.get("/consulting-checkout")
def consulting_checkout():
    return create_checkout("14-Day Home Health Implementation Plan", 299900)


