from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.routes.launch import router as launch_router
from app.routes.audit import router as audit_router
from app.routes.kits import router as kits_router
from app.routes.checkout import router as checkout_router
from app.routes.delivery import router as delivery_router
from app.routes.admin import router as admin_router

app = FastAPI(title="Home Health Startup Risk Intelligence")`napp.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(launch_router)
app.include_router(audit_router)
app.include_router(kits_router)
app.include_router(checkout_router)
app.include_router(delivery_router)
app.include_router(admin_router)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <body style="font-family:Arial;background:#0f172a;color:white;padding:50px;">
        <div style="max-width:950px;margin:auto;">
            <img src="/static/logo.png" style="width:300px;margin-bottom:20px;background:white;padding:10px;border-radius:12px;"><h1 style="font-size:44px;">Home Health Startup Risk Intelligence</h1>
            <p style="font-size:20px;color:#cbd5e1;">
                Diagnose licensing, compliance, staffing, and operational risks before your agency launches.
            </p>

            <div style="background:white;color:#111827;padding:30px;border-radius:16px;margin-top:30px;">
                <h2>Know what could delay your launch before it costs you time and money.</h2>
                <p>Our system analyzes startup readiness and generates a structured risk report with recommended next actions.</p>

                <a href="/audit/" style="background:#2563eb;color:white;padding:14px 20px;text-decoration:none;border-radius:8px;">Run Startup Risk Audit</a>
                <a href="/kits/" style="background:#111827;color:white;padding:14px 20px;text-decoration:none;border-radius:8px;margin-left:10px;">View Completion Kits</a>
            </div>
        </div>
    </body>
    </html>
    """
