from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse
from app.services.ai_writer import generate_custom_kit
from app.services.ai_pdf import generate_ai_kit_pdf
from app.services.tracking import save_purchase
import stripe

router = APIRouter(prefix="/deliver", tags=["Delivery"])

@router.get("/{slug}", response_class=HTMLResponse)
def deliver_kit(slug: str, session_id: str = Query(None)):
    customer_email = "unknown"

    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            customer_email = session.get("customer_details", {}).get("email", "unknown")
        except Exception:
            customer_email = "unknown"

    client_data = {
        "agency_name": "Client Agency",
        "owner_name": customer_email,
        "location": "N/A",
        "start_date": "N/A"
    }

    kit_name = slug.replace("-", " ").title()

    content = generate_custom_kit(client_data, kit_name, slug)
    pdf_path = generate_ai_kit_pdf(client_data, kit_name, content)

    save_purchase(customer_email, slug, session_id or "N/A", pdf_path)

    return f"""
    <html>
    <body style="font-family:Arial;padding:40px;">
        <h1>Your Custom Kit Is Ready</h1>
        <p><strong>Kit:</strong> {kit_name}</p>
        <p><strong>Email:</strong> {customer_email}</p>
        <a href="/download-kit?file={pdf_path}">Download Your Custom Kit</a><br><br>
        <a href="/dashboard/">Go to Dashboard</a>
    </body>
    </html>
    """
