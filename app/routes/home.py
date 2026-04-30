from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Home Health Intelligence | Boswell Consulting Group</title>
    </head>
    <body style="font-family:Arial;background:#f8fafc;margin:0;color:#111827;">

        <section style="background:linear-gradient(135deg,#111827,#7f1d1d,#dc2626);color:white;padding:78px 40px;text-align:center;">
            <p style="font-weight:bold;letter-spacing:1px;">BOSWELL CONSULTING GROUP</p>
            <h1 style="font-size:50px;max-width:1050px;margin:0 auto 18px;">
                Home Health Intelligence That Finds Revenue Leakage Before It Keeps Costing You
            </h1>
            <p style="font-size:21px;max-width:860px;margin:auto;line-height:1.6;">
                An automated intelligence tool for operating home health agencies. Use CMS-backed signals, benchmark scoring, and agency-specific inputs to identify risk, estimate revenue impact, and unlock corrective systems.
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
                    This platform automates the path from risk detection to recommended action. It is designed to help agency owners and operators quickly understand where operational issues may be creating revenue loss, workflow drag, staffing instability, or compliance-related pressure.
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
                    <p>High-level signal detection for cold agency prospects.</p>
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

