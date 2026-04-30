from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/pricing", response_class=HTMLResponse)
def pricing():
    return """
    <html>
    <head>
        <title>Pricing | Home Health Revenue Intelligence</title>
    </head>
    <body style="font-family:Arial;background:#f8fafc;margin:0;color:#111827;">

        <!-- HERO -->
        <section style="background:linear-gradient(135deg,#7f1d1d,#dc2626);color:white;padding:70px 40px;text-align:center;">
            <h1 style="font-size:46px;max-width:950px;margin:0 auto 18px;">
                Identify and Recover Hidden Revenue Loss in Your Agency
            </h1>
            <p style="font-size:20px;max-width:850px;margin:auto;line-height:1.6;">
                Start with a free signal preview, then unlock a full performance audit to estimate monthly impact and prioritize corrective action.
            </p>
            <a href="/mini-audit?agency=Your%20Agency&state=VA"
               style="display:inline-block;background:white;color:#991b1b;padding:16px 26px;border-radius:12px;text-decoration:none;font-weight:bold;margin-top:30px;">
               Start Free Preview
            </a>
        </section>

        <!-- VALUE SECTION -->
        <section style="max-width:1100px;margin:45px auto;padding:0 24px;">
            <div style="background:white;padding:30px;border-radius:20px;box-shadow:0 10px 30px rgba(0,0,0,.08);">
                <h2>What This Platform Identifies</h2>
                <ul style="font-size:17px;line-height:1.9;">
                    <li>Revenue leakage from denials and delayed billing</li>
                    <li>Intake inefficiencies limiting growth</li>
                    <li>A/R drag impacting cash flow</li>
                    <li>Staffing instability affecting performance</li>
                    <li>Operational and compliance-related risk signals</li>
                </ul>
            </div>

            <!-- PRICING TIERS -->
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:35px;">

                <!-- FREE -->
                <div style="background:white;padding:30px;border-radius:20px;box-shadow:0 10px 28px rgba(0,0,0,.08);">
                    <h2>Free Preview</h2>
                    <h1 style="font-size:38px;">$0</h1>
                    <p>Quickly see if your agency shows risk signals.</p>
                    <ul style="line-height:1.9;">
                        <li>CMS-based signal detection</li>
                        <li>High-level performance indicators</li>
                        <li>Limited insight preview</li>
                    </ul>
                    <a href="/mini-audit?agency=Your%20Agency&state=VA"
                       style="display:block;background:#111827;color:white;text-align:center;padding:14px;border-radius:12px;text-decoration:none;font-weight:bold;">
                       Start Free
                    </a>
                </div>

                <!-- AUDIT -->
                <div style="background:white;padding:30px;border-radius:20px;box-shadow:0 10px 28px rgba(0,0,0,.08);border:3px solid #dc2626;">
                    <div style="background:#fee2e2;color:#991b1b;padding:8px 12px;border-radius:999px;display:inline-block;font-weight:bold;">
                        Most Popular
                    </div>
                    <h2>Full Performance Audit</h2>
                    <h1 style="font-size:38px;">$199</h1>
                    <p>Understand how much revenue may be at risk.</p>
                    <ul style="line-height:1.9;">
                        <li>Estimated monthly revenue impact</li>
                        <li>Top leakage drivers</li>
                        <li>Executive PDF report</li>
                        <li>Priority roadmap</li>
                        <li>Recommended corrective systems</li>
                    </ul>
                    <a href="/audit-checkout"
                       style="display:block;background:#dc2626;color:white;text-align:center;padding:14px;border-radius:12px;text-decoration:none;font-weight:bold;">
                       Unlock Full Audit
                    </a>
                </div>

                <!-- SYSTEM -->
                <div style="background:#111827;color:white;padding:30px;border-radius:20px;box-shadow:0 10px 28px rgba(0,0,0,.12);">
                    <h2>Full Agency Optimization System</h2>
                    <h1 style="font-size:38px;">$1,999</h1>
                    <p>Implement solutions to correct revenue loss drivers.</p>
                    <ul style="line-height:1.9;">
                        <li>Revenue cycle workflow system</li>
                        <li>Intake and operations optimization</li>
                        <li>Staffing and execution templates</li>
                        <li>Compliance readiness framework</li>
                        <li>Operational control systems</li>
                    </ul>
                    <a href="/cart/add/full-optimization"
                       style="display:block;background:#f59e0b;color:#111827;text-align:center;padding:14px;border-radius:12px;text-decoration:none;font-weight:bold;">
                       Recover Lost Revenue
                    </a>
                </div>
            </div>

            <!-- ROI SECTION -->
            <div style="background:#fff7ed;border-left:7px solid #f59e0b;padding:28px;border-radius:18px;margin-top:35px;">
                <h2>ROI Perspective</h2>
                <p style="font-size:18px;line-height:1.7;">
                    If your agency is losing even $10,000 per month from preventable operational inefficiencies,
                    that represents $120,000+ annually. The audit helps identify where losses may be occurring
                    before investing in solutions.
                </p>
            </div>

            <!-- DISCLAIMER -->
            <div style="background:#f3f4f6;padding:24px;border-radius:18px;margin-top:25px;">
                <h2>Important Note</h2>
                <p style="line-height:1.6;">
                    This platform provides operational benchmarking and business decision support. It does not provide legal,
                    clinical, billing, or regulatory advice. Agencies should validate findings against internal records,
                    payer requirements, and applicable regulations.
                </p>
            </div>

        </section>

    </body>
    </html>
    """


