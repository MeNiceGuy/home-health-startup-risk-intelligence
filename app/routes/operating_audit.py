from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from app.services.saas_tracking import save_intelligence_score

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
    <body style="font-family:Arial;padding:40px;">
        <h1>Operating Intelligence System</h1>
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

    save_intelligence_score(
        "Operating Agency",
        "Operating Audit",
        total,
        compliance,
        clinical,
        revenue,
        operations
    )

    return f"""
    <html>
    <body style="font-family:Arial;padding:40px;">
        <h1>Operating Intelligence Report</h1>
        <h2>Total Score: {total}/100</h2>

        <ul>
            <li>Compliance: {compliance}%</li>
            <li>Clinical: {clinical}%</li>
            <li>Revenue: {revenue}%</li>
            <li>Operations: {operations}%</li>
        </ul>

        <a href="/dashboard/">View Dashboard</a>
    </body>
    </html>
    """
