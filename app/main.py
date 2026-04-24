from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.routes.launch import router as launch_router
from app.routes.audit import router as audit_router
from app.routes.kits import router as kits_router
from app.routes.checkout import router as checkout_router
from app.routes.delivery import router as delivery_router
from app.routes.admin import router as admin_router

app = FastAPI(title="Home Health Startup Risk Intelligence")

# correct static mount (no backticks)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

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
        <div style="max-width:900px;margin:auto;text-align:center;">
            <img src="/static/logo.png" style="width:280px;margin-bottom:20px;background:white;padding:10px;border-radius:12px;">
            <h1 style="font-size:44px;">Home Health Startup Risk Intelligence</h1>
            <p style="font-size:20px;color:#cbd5e1;">
                Diagnose and de-risk your agency before it costs you time, money, and compliance failures.
            </p>

            <br>

            <a href="/audit/" style="background:#22c55e;color:#052e16;padding:14px 20px;text-decoration:none;border-radius:8px;">Run Risk Audit</a>
            <a href="/kits/" style="background:white;color:#0f172a;padding:14px 20px;text-decoration:none;border-radius:8px;margin-left:10px;">View Kits</a>
        </div>
    </body>
    </html>
    """
