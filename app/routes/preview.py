from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/preview", tags=["White Label Preview"])

@router.get("/", response_class=HTMLResponse)
def preview(
    brand: str = Query("Your Consulting Brand"),
    color: str = Query("#2563eb"),
    logo: str = Query("")
):
    logo_html = f'<img src="{logo}" style="max-height:80px;margin-bottom:15px;">' if logo else ""

    return f"""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin:0;font-family:Arial;background:#f8fafc;color:#0f172a;">
        <div style="background:linear-gradient(135deg,#0f172a,{color});color:white;padding:60px 24px;text-align:center;">
            {logo_html}
            <h1>{brand}</h1>
            <p>White-Label Home Health Intelligence Platform</p>
        </div>

        <div style="max-width:1050px;margin:-35px auto 40px;padding:20px;">
            <div style="background:white;padding:30px;border-radius:18px;box-shadow:0 14px 35px rgba(15,23,42,.14);">
                <h2>Operating Intelligence Audit</h2>
                <p>Your clients can run audits, receive root-cause analysis, view charts, buy tailored kits, and track execution progress.</p>

                <a href="/consultant/dashboard?tenant=preview" style="display:inline-block;background:{color};color:white;padding:14px 20px;border-radius:10px;text-decoration:none;font-weight:bold;">
                Preview Consultant Command Center
                </a>
            </div>
        </div>
    </body>
    </html>
    """


