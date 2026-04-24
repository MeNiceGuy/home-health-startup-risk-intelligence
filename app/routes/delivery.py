from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.services.ai_writer import generate_custom_kit
from app.services.ai_pdf import generate_ai_kit_pdf

router = APIRouter(prefix="/deliver", tags=["Delivery"])

@router.get("/{slug}", response_class=HTMLResponse)
def deliver_kit(slug: str, request: Request):

    # You can later pull real user data from DB/session
    client_data = {
        "agency_name": request.query_params.get("agency", "Client Agency"),
        "owner_name": request.query_params.get("owner", "Owner"),
        "location": request.query_params.get("location", "Unknown"),
        "start_date": request.query_params.get("start", "N/A")
    }

    kit_name = slug.replace("-", " ").title()

    content = generate_custom_kit(client_data, kit_name, slug)
    pdf_path = generate_ai_kit_pdf(client_data, kit_name, content)

    return f"""
    <html>
    <body style="font-family:Arial;padding:40px;">
        <h1>Your Kit Is Ready</h1>
        <p>{kit_name}</p>
        <a href="/download-kit?file={pdf_path}">Download Your Custom Kit</a>
    </body>
    </html>
    """
