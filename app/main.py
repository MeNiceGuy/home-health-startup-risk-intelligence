from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.staticfiles import StaticFiles
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
from app.routes.template_delivery import router as template_delivery_router
from app.routes.template_checkout import router as template_checkout_router
from app.routes.progress import router as progress_router
from app.routes.stripe_webhook import router as stripe_webhook_router
from app.routes.onboarding import router as onboarding_router
from app.routes.consultant_subscription import router as consultant_subscription_router
from app.routes.free_onboarding import router as free_onboarding_router
from app.routes.client_dashboard import router as client_dashboard_router
from app.routes.onboarding_success import router as onboarding_success_router
from app.routes.consultant_dashboard import router as consultant_dashboard_router
from app.routes.preview import router as preview_router
from app.routes.preview import router as preview_router

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
app.include_router(template_delivery_router)
app.include_router(template_checkout_router)
app.include_router(progress_router)
app.include_router(stripe_webhook_router)
app.include_router(onboarding_router)
app.include_router(consultant_subscription_router)
app.include_router(free_onboarding_router)
app.include_router(client_dashboard_router)
app.include_router(onboarding_success_router)
app.include_router(consultant_dashboard_router)
app.include_router(preview_router)
app.include_router(preview_router)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    body{margin:0;font-family:Arial;background:#f8fafc;color:#0f172a;}
    .hero{background:linear-gradient(135deg,#0f172a,#1e3a8a);color:white;padding:70px 24px;text-align:center;}
    .hero p{color:#dbeafe;font-size:20px;}
    .wrap{max-width:1050px;margin:-35px auto 40px;padding:20px;}
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:22px;}
    .card{background:white;padding:30px;border-radius:18px;box-shadow:0 14px 35px rgba(15,23,42,.14);}
    .tag{display:inline-block;background:#dbeafe;color:#1e3a8a;padding:7px 12px;border-radius:999px;font-weight:bold;}
    .btn{display:inline-block;margin-top:18px;background:#2563eb;color:white;padding:14px 18px;border-radius:10px;text-decoration:none;font-weight:bold;}
    .green{background:#22c55e;color:#052e16;}
    ul{line-height:1.7;}
    @media(max-width:800px){.grid{grid-template-columns:1fr}.hero h1{font-size:30px}}
    </style>
    </head>
    <body>
      <div class="hero">
        <h1>Boswell Consulting Group</h1>
        <p>Home Health Intelligence Platform for startups and operating agencies.</p>
      </div>

      <div class="wrap">
        <div class="grid">
          <div class="card">
            <span class="tag">For New Agencies</span>
            <h2>Startup Intelligence Audit</h2>
            <p>Choose this if you are planning to start a home care or home health agency and need to understand licensing, staffing, compliance, payer, and launch-readiness risks before opening.</p>
            <ul>
              <li>Best for pre-launch founders</li>
              <li>Identifies missing startup requirements</li>
              <li>Helps prioritize licensing and compliance steps</li>
            </ul>
            <a class="btn green" href="/audit/">Start Startup Audit</a>
          </div>

          <div class="card">
            <span class="tag">For Existing Agencies</span>
            <h2>Operating Intelligence Audit</h2>
            <p>Choose this if your agency is already serving clients and you want to diagnose bottlenecks in compliance, revenue cycle, staffing, operations, documentation, and growth capacity.</p>
            <ul>
              <li>Best for active businesses</li>
              <li>Compares performance against benchmarks</li>
              <li>Helps identify scaling and revenue leaks</li>
            </ul>
            <a class="btn" href="/operating-audit/">Start Operating Audit</a>
          </div>
          <div class="card" style="margin-top:22px;border:3px solid #16a34a;">
    <span class="tag">For Consultants</span>
    <h2>White-Label Consultant Platform</h2>
    <p>Use this system under your consulting brand to run audits, sell templates, generate AI-tailored client documents, and track client execution progress.</p>
    <ul>
      <li>Launch your own branded audit platform</li>
      <li>Sell startup and operating improvement kits</li>
      <li>Use AI delivery after checkout</li>
      <li>Keep clients engaged with progress tracking</li>
    </ul>
    <a class="btn green" href="/onboard/">Start White-Label Setup</a>
  </div>
</div>
</body>
    </html>
    """

