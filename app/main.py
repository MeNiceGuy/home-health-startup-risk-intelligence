import os
import importlib
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"), override=True)

app = FastAPI(title="Boswell Consulting Group")

if os.path.isdir("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

def include_router_safe(module_path: str, router_name: str = "router"):
    try:
        module = importlib.import_module(module_path)
        router = getattr(module, router_name, None)
        if router:
            app.include_router(router)
    except Exception as e:
        print(f"Router skipped: {module_path} -> {e}")

ROUTERS = [
    "app.routes.suppression_admin",
    "app.routes.enrichment",
    "app.routes.followups",
    "app.routes.cms_leads",
    "app.routes.mini_audit",
    "app.routes.checkout_page",
    "app.routes.audit_success"
]

for r in ROUTERS:
    include_router_safe(r)

@app.get("/", response_class=HTMLResponse)
def homepage():
    return """
    <html>
    <body style="font-family:Arial;background:#f8fafc;margin:0;color:#111827;">
        <section style="background:linear-gradient(135deg,#111827,#7f1d1d,#dc2626);color:white;padding:80px 40px;text-align:center;">
            <p style="font-weight:bold;letter-spacing:1px;">BOSWELL CONSULTING GROUP</p>
            <h1 style="font-size:50px;max-width:1050px;margin:0 auto 18px;">
                Home Health Intelligence That Finds Revenue Leakage Before It Keeps Costing You
            </h1>
            <p style="font-size:21px;max-width:860px;margin:auto;line-height:1.6;">
                An automated intelligence tool for home health agencies that uses CMS-backed signals, benchmark scoring, and audit logic to identify risk, estimate revenue impact, and recommend corrective systems.
            </p>
            <a href="/mini-audit?agency=Your%20Agency&state=VA"
               style="display:inline-block;background:white;color:#991b1b;padding:17px 30px;border-radius:12px;text-decoration:none;font-weight:bold;margin-top:32px;font-size:17px;">
               See My Revenue Risk
            </a>
        </section>
    </body>
    </html>
    """







