from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.services.suppression import suppress_email

router = APIRouter()

@router.get("/admin/suppress", response_class=HTMLResponse)
def suppress_form():
    return """
    <html><body style='font-family:Arial;background:#f8fafc;padding:40px;'>
    <div style='max-width:700px;margin:auto;background:white;padding:30px;border-radius:18px;'>
        <h1>Suppress Email / STOP Opt-Out</h1>
        <form action="/admin/suppress/add" method="get">
            <input name="email" placeholder="email@example.com" style="padding:12px;width:80%;">
            <button style="padding:12px;background:#dc2626;color:white;border:0;border-radius:8px;">Suppress</button>
        </form>
    </div>
    </body></html>
    """

@router.get("/admin/suppress/add", response_class=HTMLResponse)
def suppress_add(email: str):
    suppress_email(email, "STOP")
    return f"""
    <html><body style='font-family:Arial;padding:40px;'>
        <h1>Suppressed</h1>
        <p>{email} will no longer receive outreach or follow-up emails.</p>
        <a href="/admin/suppress">Back</a>
    </body></html>
    """

