from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/operating-audit", tags=["Operating Intelligence"])

def score_section(values):
    score = 0
    for v in values:
        if v == "yes":
            score += 20
    return score

@router.get("/", response_class=HTMLResponse)
def form():
    return """
    <html>
    <body style="font-family:Arial;background:#f8fafc;padding:40px;">
        <h1>Operating Intelligence System</h1>
        <p>Audit your active agency across compliance, staffing, revenue, and operations.</p>

        <form method="post" action="/operating-audit/run">

        <h2>Compliance</h2>
        Policies Updated? <select name="policies"><option>no</option><option>yes</option></select><br>
        Documentation Audits Monthly? <select name="docs"><option>no</option><option>yes</option></select><br>
        HIPAA Training Done? <select name="hipaa"><option>no</option><option>yes</option></select><br>

        <h2>Clinical</h2>
        RN Oversight Active? <select name="rn"><option>no</option><option>yes</option></select><br>
        Background Checks Current? <select name="bg"><option>no</option><option>yes</option></select><br>

        <h2>Revenue</h2>
        Tracking Payers? <select name="payer"><option>no</option><option>yes</option></select><br>
        Tracking Referrals? <select name="referral"><option>no</option><option>yes</option></select><br>

        <h2>Operations</h2>
        Intake System Defined? <select name="intake"><option>no</option><option>yes</option></select><br>
        QA System Active? <select name="qa"><option>no</option><option>yes</option></select><br>

        <br><button type="submit">Run Intelligence Audit</button>
        </form>
    </body>
    </html>
    """

@router.post("/run", response_class=HTMLResponse)
def run(
    policies: str = Form("no"),
    docs: str = Form("no"),
    hipaa: str = Form("no"),
    rn: str = Form("no"),
    bg: str = Form("no"),
    payer: str = Form("no"),
    referral: str = Form("no"),
    intake: str = Form("no"),
    qa: str = Form("no"),
):
    compliance = score_section([policies, docs, hipaa])
    clinical = score_section([rn, bg])
    revenue = score_section([payer, referral])
    operations = score_section([intake, qa])

    total = int((compliance + clinical + revenue + operations) / 4)

    if total >= 80:
        tier = "Strong Operating Position"
    elif total >= 60:
        tier = "Moderate Risk"
    else:
        tier = "High Operational Risk"

    return f"""
    <html>
    <body style="font-family:Arial;background:#f8fafc;padding:40px;">
        <h1>Operating Intelligence Report</h1>

        <h2>Total Score: {total}/100</h2>
        <h3>{tier}</h3>

        <h2>Score Breakdown</h2>
        <ul>
            <li>Compliance: {compliance}%</li>
            <li>Clinical Oversight: {clinical}%</li>
            <li>Revenue Intelligence: {revenue}%</li>
            <li>Operational Systems: {operations}%</li>
        </ul>

        <h2>Business Impact</h2>
        <p>
        Agencies with scores below 60 typically experience revenue leakage,
        increased audit exposure, and scaling limitations.
        </p>

        <h2>Recommended Actions</h2>
<h3>Fix These Now:</h3>
<ul>
<li><a href="/ops-checkout/compliance-system">Fix Compliance System ($149)</a></li>
<li><a href="/ops-checkout/qa-system">Fix QA System ($199)</a></li>
<li><a href="/ops-checkout/revenue-system">Fix Revenue System ($249)</a></li>
<li><a href="/ops-checkout/full-ops">Full Operating System ($799)</a></li>
</ul>

<h2>Upgrade to Monthly Intelligence</h2>
<a href="/subscribe/" style="background:#22c55e;color:#052e16;padding:14px 20px;text-decoration:none;border-radius:8px;">Start Monthly Subscription ($99/mo)</a>

        <ul>
            <li>Implement structured QA audits</li>
            <li>Track payer + referral performance</li>
            <li>Strengthen compliance review cycles</li>
        </ul>

        <br><a href="/operating-audit/">Run Again</a>
    </body>
    </html>
    """
