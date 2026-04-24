from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.routes.auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    user = get_current_user(request)

    if not user:
        return RedirectResponse("/auth/login", status_code=302)

    email = user.get("email")

    return f"""
    <html>
    <body style="font-family:Arial;background:#f8fafc;padding:40px;">
        <div style="max-width:1000px;margin:auto;">
            <h1>Boswell Consulting Group Dashboard</h1>
            <p>Logged in as: <strong>{email}</strong></p>

            <div style="background:white;padding:25px;border-radius:14px;margin-top:20px;">
                <h2>Startup Risk Intelligence</h2>
                <p>Run a new audit, review recommended kits, and download reports.</p>
                <a href="/audit/">Run New Audit</a>
            </div>

            <div style="background:white;padding:25px;border-radius:14px;margin-top:20px;">
                <h2>Completion Kits</h2>
                <p>Purchase targeted implementation kits based on your audit results.</p>
                <a href="/kits/">View Kits</a>
            </div>

            <br>
            <a href="/auth/logout">Logout</a>
        </div>
    </body>
    </html>
    """
