from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/operating-audit", tags=["Operating Agency Audit"])

@router.get("/", response_class=HTMLResponse)
def operating_audit_form():
    return """
    <html>
    <body style="font-family:Arial;background:#f8fafc;padding:40px;">
        <h1>Boswell Consulting Group Operating Agency Intelligence Audit</h1>
        <p>For home health agencies already operating and wanting to identify compliance, performance, staffing, documentation, and scaling risks.</p>

        <form method="post" action="/operating-audit/run">

            <h2>Agency Information</h2>
            Agency Name:<br><input name="agency_name"><br><br>
            Owner / Administrator:<br><input name="owner_name"><br><br>
            Location:<br><input name="location"><br><br>
            Years Operating:<br><input name="years_operating"><br><br>

            <h2>Compliance Operations</h2>
            Policies Updated Within Last 12 Months?<br>
            <select name="policies_updated"><option value="no">No</option><option value="yes">Yes</option></select><br><br>

            Documentation Audits Performed Monthly?<br>
            <select name="documentation_audits"><option value="no">No</option><option value="yes">Yes</option></select><br><br>

            HIPAA Training Completed Annually?<br>
            <select name="hipaa_training"><option value="no">No</option><option value="yes">Yes</option></select><br><br>

            Incident Reporting Process Active?<br>
            <select name="incident_reporting"><option value="no">No</option><option value="yes">Yes</option></select><br><br>

            <h2>Staffing & Clinical Oversight</h2>
            RN / Clinical Supervisor Actively Reviewing Care?<br>
            <select name="clinical_review"><option value="no">No</option><option value="yes">Yes</option></select><br><br>

            Staff Turnover Is Under Control?<br>
            <select name="turnover_control"><option value="no">No</option><option value="yes">Yes</option></select><br><br>

            Background Checks Current?<br>
            <select name="background_checks"><option value="no">No</option><option value="yes">Yes</option></select><br><br>

            <h2>Performance & Scaling</h2>
            Tracking Referral Sources?<br>
            <select name="referral_tracking"><option value="no">No</option><option value="yes">Yes</option></select><br><br>

            Tracking Revenue by Payer Source?<br>
            <select name="payer_tracking"><option value="no">No</option><option value="yes">Yes</option></select><br><br>

            Quality Improvement Plan Active?<br>
            <select name="quality_plan"><option value="no">No</option><option value="yes">Yes</option></select><br><br>

            Ready to Scale Caseload or Service Area?<br>
            <select name="scale_ready"><option value="no">No</option><option value="yes">Yes</option></select><br><br>

            <button type="submit">Run Operating Agency Audit</button>
        </form>
    </body>
    </html>
    """

@router.post("/run", response_class=HTMLResponse)
def run_operating_audit(
    agency_name: str = Form("N/A"),
    owner_name: str = Form("N/A"),
    location: str = Form("N/A"),
    years_operating: str = Form("N/A"),
    policies_updated: str = Form("no"),
    documentation_audits: str = Form("no"),
    hipaa_training: str = Form("no"),
    incident_reporting: str = Form("no"),
    clinical_review: str = Form("no"),
    turnover_control: str = Form("no"),
    background_checks: str = Form("no"),
    referral_tracking: str = Form("no"),
    payer_tracking: str = Form("no"),
    quality_plan: str = Form("no"),
    scale_ready: str = Form("no")
):
    answers = locals()

    risk_points = 0
    gaps = []

    for key, value in answers.items():
        if key not in ["agency_name", "owner_name", "location", "years_operating"] and value != "yes":
            risk_points += 8
            gaps.append(key.replace("_", " ").title())

    score = max(100 - risk_points, 20)

    if score >= 80:
        tier = "Low Operating Risk"
    elif score >= 60:
        tier = "Moderate Operating Risk"
    else:
        tier = "High Operating Risk"

    gaps_html = "".join([f"<li>{g}</li>" for g in gaps])

    return f"""
    <html>
    <body style="font-family:Arial;padding:40px;">
        <h1>Operating Agency Audit Complete</h1>
        <p><strong>{agency_name}</strong> | {location}</p>
        <h2>Score: {score}/100</h2>
        <h3>{tier}</h3>

        <h2>Identified Operating Gaps</h2>
        <ul>{gaps_html}</ul>

        <h2>Business Interpretation</h2>
        <p>This agency may have operational, compliance, staffing, or scaling gaps that should be corrected before expanding patient volume, payer contracts, or service area.</p>

        <a href="/operating-audit/">Run Again</a>
    </body>
    </html>
    """
