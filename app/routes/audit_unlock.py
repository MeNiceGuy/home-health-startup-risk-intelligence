from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/audit-unlock", response_class=HTMLResponse)
def audit_unlock():
    return """
    <html>
    <body style='font-family:Arial;padding:40px;background:#f8fafc;'>
    <div style='max-width:700px;margin:auto;background:white;padding:30px;border-radius:18px;'>
        <h1>Audit Unlocked</h1>
        <p>Your full performance audit is now available.</p>

        <a href="/operating-audit/?agency=Your%20Agency&state=VA&access=paid-audit"
           style='display:inline-block;background:#dc2626;color:white;padding:14px 22px;border-radius:12px;text-decoration:none;font-weight:bold;'>
           View Full Audit
        </a>
    </div>
    </body>
    </html>
    """



