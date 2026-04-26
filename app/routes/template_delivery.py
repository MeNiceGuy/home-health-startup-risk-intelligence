from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse, FileResponse
from app.services.template_ai import generate_tailored_template, TEMPLATE_PRODUCTS
from app.services.template_pdf import generate_template_pdf
import stripe
from app.routes.stripe_webhook import is_paid_session
from app.services.settings import FREE_MODE

router = APIRouter(prefix="/templates", tags=["Templates"])

@router.get("/{slug}", response_class=HTMLResponse)
def generate_template(slug: str, session_id: str = Query(None)):
    if not FREE_MODE and (not session_id or not is_paid_session(session_id, slug)):
        from app.services.client_timeline import add_timeline_event

    add_timeline_event(
        "demo",
        "client",
        "Template Purchased",
        "Client purchased template",
        f"Template: {slug}",
        ""
    )

    return HTMLResponse("""
        <html><body style="font-family:Arial;padding:40px;">
        <h1>Payment Verification Required</h1>
        <p>Your payment has not been confirmed yet. If you just paid, refresh in a few seconds.</p>
        <a href="/template-checkout/""" + slug + """">from app.services.client_timeline import add_timeline_event

    add_timeline_event(
        "demo",
        "client",
        "Template Purchased",
        "Client purchased template",
        f"Template: {slug}",
        ""
    )

    return to Checkout</a>
        </body></html>
        """, status_code=403)
    email = "unknown"

    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            email = session.get("customer_details", {}).get("email", "unknown")
        except Exception:
            email = "unknown"

    client_data = {
        "agency_name": "Client Agency",
        "state": "Virginia / North Carolina",
        "agency_type": "Home Health / Home Care",
        "email": email
    }

    template_name, content = generate_tailored_template(slug, client_data)
    pdf_path = generate_template_pdf(template_name, content, client_data)

    from app.services.client_timeline import add_timeline_event

    add_timeline_event(
        "demo",
        "client",
        "Template Purchased",
        "Client purchased template",
        f"Template: {slug}",
        ""
    )

    return f"""
    <html>
    <body style="font-family:Arial;background:#f8fafc;padding:40px;">
        <div style="max-width:850px;margin:auto;background:white;padding:35px;border-radius:18px;">
            <h1>{template_name}</h1>
            <p>Your AI-tailored document is ready.</p>
            <p><strong>Email:</strong> {email}</p>

            <a href="/templates/download?file={pdf_path}"
            style="background:#2563eb;color:white;padding:14px 20px;border-radius:10px;text-decoration:none;">
            Download Template
            </a>
        </div>
    </body>
    </html>
    """

@router.get("/download")
def download_template(file: str):
    from app.services.client_timeline import add_timeline_event

    add_timeline_event(
        "demo",
        "client",
        "Template Purchased",
        "Client purchased template",
        f"Template: {slug}",
        ""
    )

    return FileResponse(file, filename=file.split("/")[-1])

