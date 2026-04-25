from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from app.services.saas_tracking import save_intelligence_score

router = APIRouter(prefix="/operating-audit", tags=["Operating Intelligence"])

def score(vals):
    return sum([20 for v in vals if v == "yes"])

@router.get("/", response_class=HTMLResponse)
def form():
    return """
    <html>
    <body style="font-family:Arial;padding:40px;">
    <h1>Operating Intelligence System</h1>

    <form method="post" action="/operating-audit/run">

    <h2>Compliance</h2>
    Policies Updated? <select name="policies"><option>no</option><option>yes</option></select><br>
    HIPAA System Active? <select name="hipaa"><option>no</option><option>yes</option></select><br>
    QA Audits Monthly? <select name="qa"><option>no</option><option>yes</option></select><br>

    <h2>Clinical</h2>
    RN Oversight Active? <select name="rn"><option>no</option><option>yes</option></select><br>
    Background Checks Current? <select name="bg"><option>no</option><option>yes</option></select><br>

    <h2>Financial Intelligence</h2>
    Claims Submitted Weekly? <select name="claims"><option>no</option><option>yes</option></select><br>
    Denials Tracked? <select name="denials"><option>no</option><option>yes</option></select><br>
    Reimbursement Timeline Known? <select name="reimbursement"><option>no</option><option>yes</option></select><br>

    <h2>Revenue & Growth</h2>
    Payer Strategy Defined? <select name="payer"><option>no</option><option>yes</option></select><br>
    Referral System Active? <select name="referral"><option>no</option><option>yes</option></select><br>
    Marketing Strategy Active? <select name="marketing"><option>no</option><option>yes</option></select><br>

    <h2>Staffing Capacity</h2>
    Staffing Plan Defined? <select name="staffing"><option>no</option><option>yes</option></select><br>
    Hiring Pipeline Active? <select name="hiring"><option>no</option><option>yes</option></select><br>
    Visits Fully Covered? <select name="coverage"><option>no</option><option>yes</option></select><br>

    <h2>Operations</h2>
    Intake System Defined? <select name="intake"><option>no</option><option>yes</option></select><br>
    Documentation System Active? <select name="docs"><option>no</option><option>yes</option></select><br>

    <br><button type="submit">Run Intelligence Audit</button>
    </form>
    </body>
    </html>
    """

@router.post("/run", response_class=HTMLResponse)
def run(
    policies:str=Form("no"), hipaa:str=Form("no"), qa:str=Form("no"),
    rn:str=Form("no"), bg:str=Form("no"),
    claims:str=Form("no"), denials:str=Form("no"), reimbursement:str=Form("no"),
    payer:str=Form("no"), referral:str=Form("no"), marketing:str=Form("no"),
    staffing:str=Form("no"), hiring:str=Form("no"), coverage:str=Form("no"),
    intake:str=Form("no"), docs:str=Form("no")
):
    compliance = score([policies, hipaa, qa])
    clinical = score([rn, bg])
    financial = score([claims, denials, reimbursement])
    revenue = score([payer, referral, marketing])
    staffing_score = score([staffing, hiring, coverage])
    operations = score([intake, docs])

    total = int((compliance+clinical+financial+revenue+staffing_score+operations)/6)

    save_intelligence_score(
        "Operating Agency","Full Audit",
        total,compliance,clinical,revenue,operations
    )

    return f"""
    <html>
    <body style="font-family:Arial;padding:40px;">
    <h1>Operating Intelligence Report</h1>

    <h2>Total Score: {total}/100</h2>

    <ul>
    <li>Compliance: {compliance}%</li>
    <li>Clinical: {clinical}%</li>
    <li>Financial: {financial}%</li>
    <li>Revenue: {revenue}%</li>
    <li>Staffing: {staffing_score}%</li>
    <li>Operations: {operations}%</li>
    </ul>

    <h2>Business Impact</h2>
    <p>
    Weak financial or staffing systems create the highest failure risk,
    even if compliance is strong.
    </p>

    <h2>Next Moves</h2>
    <ul>
    <li>Fix financial tracking immediately</li>
    <li>Strengthen staffing pipeline</li>
    <li>Implement QA + documentation audits</li>
    </ul>

    <br><a href="/dashboard/">View Dashboard</a>
    </body>
    </html>
    """
