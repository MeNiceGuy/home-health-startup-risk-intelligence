from app.routes.audit_success import router as audit_success_router
from app.routes.checkout_page import router as checkout_page_router
from app.routes.audit_unlock import router as audit_unlock_router
from app.routes.pricing import router as pricing_router
import os
from dotenv import load_dotenv

# FORCE LOAD .env FROM ROOT
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"), override=True)


from dotenv import load_dotenv
load_dotenv()
from app.routes.outreach_admin import router as outreach_admin_router
from app.routes.mini_audit import router as mini_audit_router
from app.routes.cms_targets import router as cms_targets_router
from app.routes.cms_admin import router as cms_admin_router
from app.routes.cart import router as cart_router
from app.routes.kit_checkout import router as kit_checkout_router
from app.routes.tracking import router as tracking_router
from app.routes.revenue import router as revenue_router
from app.routes.booking import router as booking_router
from app.routes.upsell import router as upsell_router
from app.routes.leads import router as leads_router
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
from app.routes.bundle_checkout import router as bundle_checkout_router
from app.routes.client_timeline import router as client_timeline_router
from app.routes.stripe_connect import router as stripe_connect_router
from app.routes.earnings import router as earnings_router
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
app.include_router(bundle_checkout_router)
app.include_router(client_timeline_router)
app.include_router(stripe_connect_router)
app.include_router(earnings_router)
app.include_router(onboarding_success_router)
app.include_router(consultant_dashboard_router)
app.include_router(preview_router)
app.include_router(preview_router)











app.include_router(leads_router)



app.include_router(upsell_router)


app.include_router(booking_router)


app.include_router(revenue_router)


app.include_router(tracking_router)


app.include_router(kit_checkout_router)



app.include_router(cart_router)


app.include_router(cms_admin_router)



app.include_router(cms_targets_router)

app.include_router(mini_audit_router)


app.include_router(outreach_admin_router)







app.include_router(pricing_router)


app.include_router(audit_unlock_router)




from fastapi.responses import HTMLResponse




app.include_router(audit_success_router)



from fastapi.responses import HTMLResponse


    <html>
    """
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

        <section style="max-width:1120px;margin:45px auto;padding:0 24px;">

            <div style="background:white;padding:34px;border-radius:22px;box-shadow:0 10px 30px rgba(0,0,0,.08);">
                <h2>Built for Agencies That Want Answers Without a Sales Call</h2>
                <p style="font-size:18px;line-height:1.7;">
                    This system automates the path from risk detection to recommended action. It helps agency owners quickly understand where operational issues may create revenue loss, workflow drag, staffing instability, or compliance-related pressure.
                </p>
            </div>

            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:30px;">
                <div style="background:white;padding:24px;border-radius:18px;box-shadow:0 8px 24px rgba(0,0,0,.06);">
                    <h3>1. Detect</h3>
                    <p>Identify public CMS and benchmark signals that may indicate performance gaps.</p>
                </div>
                <div style="background:white;padding:24px;border-radius:18px;box-shadow:0 8px 24px rgba(0,0,0,.06);">
                    <h3>2. Diagnose</h3>
                    <p>Unlock a full audit with revenue impact, leakage drivers, and priority roadmap.</p>
                </div>
                <div style="background:white;padding:24px;border-radius:18px;box-shadow:0 8px 24px rgba(0,0,0,.06);">
                    <h3>3. Recommend</h3>
                    <p>Receive corrective systems matched to the issues found in the audit.</p>
                </div>
                <div style="background:white;padding:24px;border-radius:18px;box-shadow:0 8px 24px rgba(0,0,0,.06);">
                    <h3>4. Implement</h3>
                    <p>Purchase the recommended optimization system and begin fixing the gaps.</p>
                </div>
            </div>

            <div style="background:#fff7ed;border-left:7px solid #f59e0b;padding:30px;border-radius:18px;margin-top:35px;">
                <h2>Even a $10,000 Monthly Gap Becomes $120,000+ Annually</h2>
                <p style="font-size:18px;line-height:1.7;">
                    Denials, delayed A/R, missed visits, slow intake, staffing instability, and weak operating controls can quietly compound every month. The free preview shows limited risk signals. The full audit estimates impact and identifies what to fix first.
                </p>
                <a href="/pricing"
                   style="display:inline-block;background:#dc2626;color:white;padding:15px 24px;border-radius:12px;text-decoration:none;font-weight:bold;">
                   View Audit Options
                </a>
            </div>

            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:35px;">
                <div style="background:white;padding:28px;border-radius:20px;box-shadow:0 10px 28px rgba(0,0,0,.08);">
                    <h2>Free Preview</h2>
                    <p>High-level signal detection for agency risk awareness.</p>
                    <a href="/mini-audit?agency=Your%20Agency&state=VA"
                       style="display:block;background:#111827;color:white;text-align:center;padding:14px;border-radius:12px;text-decoration:none;font-weight:bold;">
                       Start Free Preview
                    </a>
                </div>

                <div style="background:white;padding:28px;border-radius:20px;box-shadow:0 10px 28px rgba(0,0,0,.08);border:3px solid #dc2626;">
                    <h2>Full Performance Audit</h2>
                    <p>Paid audit with revenue impact, executive PDF, roadmap, and recommendations.</p>
                    <a href="/audit-checkout"
                       style="display:block;background:#dc2626;color:white;text-align:center;padding:14px;border-radius:12px;text-decoration:none;font-weight:bold;">
                       Unlock Full Audit
                    </a>
                </div>

                <div style="background:#111827;color:white;padding:28px;border-radius:20px;box-shadow:0 10px 28px rgba(0,0,0,.12);">
                    <h2>Optimization System</h2>
                    <p>Corrective workflows, templates, and controls matched to audit findings.</p>
                    <a href="/cart/add/full-optimization"
                       style="display:block;background:#f59e0b;color:#111827;text-align:center;padding:14px;border-radius:12px;text-decoration:none;font-weight:bold;">
                       Fix the Gaps
                    </a>
                </div>
            </div>

            <div style="background:#f3f4f6;padding:24px;border-radius:18px;margin-top:30px;">
                <h2>Important Note</h2>
                <p style="line-height:1.6;">
                    Home Health Intelligence by Boswell Consulting Group provides operational benchmarking and business decision support. It does not provide legal, clinical, billing, or regulatory advice. Agencies should validate findings against internal records, payer requirements, and applicable regulations.
                </p>
            </div>

        </section>
    </body>
    </html>
    """
    <html>
    <body style="font-family:Arial;background:#f8fafc;margin:0;color:#111827;">

        <section style="background:linear-gradient(135deg,#111827,#dc2626);color:white;padding:80px;text-align:center;">
            <h1>Home Health Intelligence</h1>
            <p>by Boswell Consulting Group</p>
            <p>We identified signals your agency may be losing revenue.</p>

            <a href="/mini-audit?agency=Your%20Agency&state=VA"
               style="display:inline-block;background:white;color:#dc2626;padding:16px 28px;border-radius:10px;text-decoration:none;font-weight:bold;margin-top:20px;">
               See My Revenue Risk
            </a>
        </section>

    </body>
    </html>
    """





from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def homepage():
    return """
    <html>
    <body style="font-family:Arial;background:#f8fafc;margin:0;color:#111827;">

        <section style="background:linear-gradient(135deg,#111827,#dc2626);color:white;padding:80px;text-align:center;">
            <h1>Home Health Intelligence</h1>
            <p>by Boswell Consulting Group</p>
            <p>We identified signals your agency may be losing revenue.</p>

            <a href="/mini-audit?agency=Your%20Agency&state=VA"
               style="display:inline-block;background:white;color:#dc2626;padding:16px 28px;border-radius:10px;text-decoration:none;font-weight:bold;margin-top:20px;">
               See My Revenue Risk
            </a>
        </section>

    </body>
    </html>
    """

