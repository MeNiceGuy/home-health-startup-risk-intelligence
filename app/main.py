from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.routes.launch import router as launch_router
from app.routes.audit import router as audit_router
from app.routes.kits import router as kits_router
from app.routes.checkout import router as checkout_router
from app.routes.delivery import router as delivery_router
from app.routes.admin import router as admin_router`nfrom app.routes.auth import router as auth_router`nfrom app.routes.dashboard import router as dashboard_router`nfrom app.routes.operating_audit import router as operating_audit_router`nfrom app.routes.operating_audit import router as operating_audit_router

app = FastAPI(title="Boswell Consulting Group")

# correct static mount (no backticks)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(launch_router)
app.include_router(audit_router)
app.include_router(kits_router)
app.include_router(checkout_router)`nfrom app.routes.delivery import router as delivery_router`nfrom app.routes.download import router as download_router`napp.include_router(delivery_router)`napp.include_router(download_router)
app.include_router(delivery_router)
app.include_router(admin_router)`napp.include_router(auth_router)`napp.include_router(dashboard_router)`napp.include_router(operating_audit_router)`napp.include_router(operating_audit_router)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <body style="font-family:Arial;background:#0f172a;color:white;padding:50px;">
        <div style="max-width:900px;margin:auto;text-align:center;">
            <img src="/static/logo.png" style="width:280px;margin-bottom:20px;background:white;padding:10px;border-radius:12px;">
            <h1 style="font-size:44px;">Boswell Consulting Group</h1>
            <p style="font-size:20px;color:#cbd5e1;">
                Home Health Startup Risk Intelligence by Boswell Consulting Group. Diagnose licensing, staffing, compliance, and operational risks before launch.
            </p>

            <br>

            <a href="/audit/" style="background:#22c55e;color:#052e16;padding:14px 20px;text-decoration:none;border-radius:8px;">Run Risk Audit</a>
            <a href="/operating-audit/" style="background:#2563eb;color:white;padding:14px 20px;text-decoration:none;border-radius:8px;margin-left:10px;">Operating Agency Audit</a><a href="/kits/" style="background:white;color:#0f172a;padding:14px 20px;text-decoration:none;border-radius:8px;margin-left:10px;">View Kits</a>
        </div>
    </body>
    </html>
    """
