from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routes.launch import router as launch_router
from app.routes.audit import router as audit_router

app = FastAPI(title="Home Health Launch Compliance Tool")

app.include_router(launch_router)
app.include_router(audit_router)
from app.routes.kits import router as kits_router
app.include_router(kits_router)
from app.routes.checkout import router as checkout_router
app.include_router(checkout_router)
from app.routes.delivery import router as delivery_router
app.include_router(delivery_router)
from app.routes.admin import router as admin_router
app.include_router(admin_router)
from app.routes.payment import router as payment_router
app.include_router(payment_router)
from app.routes.success import router as success_router
app.include_router(success_router)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Home Health Launch Compliance Tool</title>
        <style>
            body { font-family: Arial; background:#f4f6f8; padding:40px; }
            .card { background:white; padding:30px; border-radius:12px; max-width:900px; margin:auto; box-shadow:0 4px 14px rgba(0,0,0,.08); }
            a { display:inline-block; margin:10px 10px 0 0; padding:12px 18px; background:#2563eb; color:white; text-decoration:none; border-radius:8px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Home Health Launch Compliance Tool</h1>
            <p>Virginia MVP: launch roadmap, compliance categories, risk flags, and startup readiness audit.</p>
            <a href="/launch/virginia">View Virginia Compliance Data</a>
            <a href="/audit/">Run Startup Compliance Audit</a><a href="/kits/">Startup Completion Kits</a>
        </div>
    </body>
    </html>
    """
