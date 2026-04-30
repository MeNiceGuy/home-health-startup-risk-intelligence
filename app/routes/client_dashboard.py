from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/client", tags=["Client Dashboard"])

@router.get("/dashboard", response_class=HTMLResponse)
def client_dashboard(email: str = Query("client@example.com")):
    return f"""
    <html>
    <body style="font-family:Arial;background:#f8fafc;padding:40px;">
    <div style="max-width:950px;margin:auto;background:white;padding:35px;border-radius:18px;">
        <h1>Client Improvement Dashboard</h1>
        <p><strong>Client:</strong> {email}</p>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;">
            <div style="padding:20px;background:#eff6ff;border-radius:14px;">
                <h2>Run Audit</h2>
                <a href="/operating-audit/" style="background:#2563eb;color:white;padding:12px 16px;border-radius:10px;text-decoration:none;">Start Audit</a>
            </div>

            <div style="padding:20px;background:#f0fdf4;border-radius:14px;">
                <h2>Track Progress</h2>
                <a href="/progress/?email={email}" style="background:#16a34a;color:white;padding:12px 16px;border-radius:10px;text-decoration:none;">Open Tracker</a>
            </div>
        </div>

        <h2>Recommended Next Step</h2>
        <p>Review your latest audit, purchase the recommended kit, and track implementation over 30 days.</p>
    </div>
    </body>
    </html>
    """


