from fastapi import APIRouter, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from app.services.tenants import init_tenants, get_conn, USE_POSTGRES
import re

router = APIRouter(prefix="/onboard", tags=["Consultant Onboarding"])

def clean_subdomain(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())[:20]

@router.get("/", response_class=HTMLResponse)
def onboard_form():
    return """
    <html><body style="font-family:Arial;padding:40px;background:#f8fafc;">
    <div style="max-width:600px;margin:auto;background:white;padding:30px;border-radius:16px;">
    <h1>Start Your Consulting Platform</h1>
    <form method="post" action="/consultant-subscribe/checkout" enctype="multipart/form-data">
        <label>Consulting Brand Name</label><br>
        <input name="name" required style="width:100%;padding:12px;margin-bottom:15px;"><br>

        <label>Email</label><br>
        <input name="email" required style="width:100%;padding:12px;margin-bottom:15px;"><br>

        <label>Logo Upload Optional</label><br>
        <input type="file" name="logo" accept="image/*" style="width:100%;padding:12px;margin-bottom:15px;"><br>

        <label>Stripe Connected Account ID Optional</label><br>
        <input name="stripe_account" placeholder="acct_..." style="width:100%;padding:12px;margin-bottom:15px;"><br>

        <label>Primary Brand Color</label><br>
<input type="color" name="color_custom" value="#2563eb" style="width:100%;height:50px;margin-bottom:20px;"><br>

        <button style="background:#2563eb;color:white;padding:14px 20px;border:0;border-radius:10px;">
        Create My Platform
        </button>
    </form>
    </div>
    </body></html>
    """

@router.post("/create")
def create_tenant(name: str = Form(...), email: str = Form(...), color_select: str = Form(""), color_custom: str = Form(""), stripe_account: str = Form(""), logo: UploadFile = File(None)):
    init_tenants()
    subdomain = clean_subdomain(name)

    color = color_custom if color_custom else color_select

    logo_url = ""
    if logo and logo.filename:
        import os
        ext = os.path.splitext(logo.filename)[1] or ".png"
        logo_path = f"app/static/tenant_logos/{subdomain}{ext}"
        with open(logo_path, "wb") as f:
            f.write(logo.file.read())
        logo_url = f"/static/tenant_logos/{subdomain}{ext}"

    conn = get_conn()
    cur = conn.cursor()

    if USE_POSTGRES:
        cur.execute("""
        INSERT INTO tenants (name, subdomain, primary_color, stripe_account, logo_url) VALUES (%s, %s, %s, %s, %s)
        RETURNING subdomain
        """, (name, subdomain, color, stripe_account, logo_url))
        result = cur.fetchone()
        subdomain = result[0]
    else:
        cur.execute("""
        INSERT OR IGNORE INTO tenants (name, subdomain, primary_color, stripe_account, logo_url) VALUES (?, ?, ?, ?, ?)
        """, (name, subdomain, color, stripe_account, logo_url))

    conn.commit()
    conn.close()

    return RedirectResponse(f"http://127.0.0.1:8000/consultant/dashboard?tenant={subdomain}", status_code=303)










