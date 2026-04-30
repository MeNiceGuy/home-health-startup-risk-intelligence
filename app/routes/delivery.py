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
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                margin:0;
                font-family:Arial, sans-serif;
                background:#f8fafc;
                color:#0f172a;
            }}
            .hero {{
                background:linear-gradient(135deg,#0f172a,#1e3a8a);
                color:white;
                padding:60px 24px;
                text-align:center;
            }}
            .hero h1 {{
                font-size:42px;
                margin-bottom:12px;
            }}
            .hero p {{
                color:#dbeafe;
                font-size:18px;
            }}
            .wrap {{
                max-width:900px;
                margin:-40px auto 40px;
                padding:20px;
            }}
            .card {{
                background:white;
                padding:32px;
                border-radius:18px;
                box-shadow:0 14px 40px rgba(15,23,42,.15);
                margin-bottom:20px;
            }}
            .badge {{
                display:inline-block;
                background:#dcfce7;
                color:#166534;
                padding:8px 14px;
                border-radius:999px;
                font-weight:bold;
                margin-bottom:15px;
            }}
            .btn {{
                display:inline-block;
                background:#2563eb;
                color:white;
                padding:14px 20px;
                border-radius:10px;
                text-decoration:none;
                font-weight:bold;
                margin-top:10px;
            }}
            .secondary {{
                background:#0f172a;
            }}
            .info {{
                background:#f1f5f9;
                padding:18px;
                border-radius:12px;
                margin-top:18px;
            }}
            @media(max-width:700px){{
                .hero h1 {{font-size:30px;}}
                .card {{padding:22px;}}
                .btn {{display:block;text-align:center;margin-bottom:10px;}}
            }}
        </style>
    </head>
    <body>
        <div class="hero">
            <h1>Boswell Consulting Group</h1>
            <p>Your AI-generated implementation kit is ready.</p>
        </div>

        <div class="wrap">
            <div class="card">
                <div class="badge">Purchase Confirmed</div>
                <h2>{kit_name}</h2>
                <p>Your customized kit has been generated based on the selected solution area.</p>

                <div class="info">
                    <p><strong>Email:</strong> {customer_email}</p>
                    <p><strong>Document Type:</strong> AI-Generated Implementation Kit</p>
                    <p><strong>Status:</strong> Ready for download</p>
                </div>

                <a class="btn" href="/deliver/download?file={pdf_path}">Download Your Kit</a>
                <a class="btn secondary" href="/dashboard/">Go to Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    """

@router.get("/download")
def download_generated_kit(file: str):
    return FileResponse(file, filename=file.split("/")[-1])


