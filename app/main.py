from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.routes.launch import router as launch_router
from app.routes.audit import router as audit_router
from app.routes.kits import router as kits_router
from app.routes.checkout import router as checkout_router
from app.routes.delivery import router as delivery_router
from app.routes.download import router as download_router
from app.routes.admin import router as admin_router
from app.routes.auth import router as auth_router
from app.routes.dashboard import router as dashboard_router
from app.routes.operating_audit import router as operating_audit_router
from app.routes.ops_checkout import router as ops_checkout_router
from app.routes.subscription import router as subscription_router

app = FastAPI(title="Boswell Consulting Group")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(launch_router)
app.include_router(audit_router)
app.include_router(kits_router)
app.include_router(checkout_router)
app.include_router(delivery_router)
app.include_router(download_router)
app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(operating_audit_router)
app.include_router(ops_checkout_router)
app.include_router(subscription_router)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <body style="font-family:Arial;background:#0f172a;color:white;padding:50px;">
        <div style="max-width:900px;margin:auto;text-align:center;">
            <h1>Boswell Consulting Group</h1>
            <p style="font-size:20px;color:#cbd5e1;">
                Home Health Intelligence Platform — Startup + Operating Systems
            </p>

            <a href="/audit/" style="background:#22c55e;padding:14px 20px;border-radius:8px;color:black;">Startup Audit</a>
            <a href="/operating-audit/" style="background:#2563eb;padding:14px 20px;border-radius:8px;color:white;margin-left:10px;">Operating Audit</a>
            
        </div>
    </body>
    </html>
    """
