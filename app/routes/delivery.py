from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse, FileResponse
from app.services.ai_writer import generate_custom_kit
from app.services.ai_pdf import generate_ai_kit_pdf
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

    kit_name = slug.replace("-", " ").title()

    client_data = {
        "agency_name": "Client Agency",
        "owner_name": customer_email,
        "location": "N/A",
        "state": "N/A"
    }

    kit_content = generate_custom_kit(client_data, kit_name, slug)
    pdf_path = generate_ai_kit_pdf(client_data, kit_name, kit_content)

    return f"""
    <html>
    <body style="font-family:Arial;padding:40px;">
        <h1>Your Custom Kit Is Ready</h1>
        <p><strong>Kit:</strong> {kit_name}</p>
        <p><strong>Email:</strong> {customer_email}</p>
        <a href="/deliver/download?file={pdf_path}">Download Your AI-Generated Kit</a>
        <br><br>
        <a href="/dashboard/">Go to Dashboard</a>
    </body>
    </html>
    """

@router.get("/download")
def download_generated_kit(file: str):
    return FileResponse(file, filename=file.split("/")[-1])
