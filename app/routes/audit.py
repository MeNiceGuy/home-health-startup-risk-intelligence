from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, FileResponse
from app.services.risk_engine import calculate_risk_score
from app.services.fix_engine import get_fix_instructions
from app.services.pdf_engine import generate_audit_pdf
from app.services.kit_mapper import KIT_MAP

router = APIRouter(prefix="/audit", tags=["Audit"])

@router.get("/", response_class=HTMLResponse)
def audit_form():
    return """
    <html>
    <body style="font-family:Arial;background:#f8fafc;padding:40px;">
        <h1>Boswell Consulting Group Startup Intelligence Audit</h1>
        <p>Assess launch readiness across licensing, clinical staffing, revenue, operations, compliance, and execution capacity.</p>

        <form method="post" action="/audit/run">

            <h2>Client Information</h2>
            Agency Name:<br><input name="agency_name"><br><br>
            Owner Name:<br><input name="owner_name"><br><br>
            City / County:<br><input name="location"><br><br>
            Target Start Date:<br><input type="date" name="start_date"><br><br>

            <h2>Licensing Readiness</h2>
            Business Entity Formed?<br><select name="business_registered"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>
            EIN Obtained?<br><select name="ein_obtained"><option value="no">No</option><option value="yes">Yes</option></select><br><br>
            Specific License Type Identified?<br><select name="license_type_identified"><option value="no">No</option><option value="partial">Somewhat</option><option value="yes">Yes</option></select><br><br>
            Licensing Documents Prepared?<br><select name="license_docs_ready"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>
            State Inspection / Survey Requirements Reviewed?<br><select name="inspection_ready"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>

            <h2>Clinical & Staffing Risk</h2>
            RN Clinical Supervisor Secured?<br><select name="rn_secured"><option value="no">No</option><option value="contracted">Contracted</option><option value="yes">Yes</option></select><br><br>
            Clinical Leadership Meets State Requirements?<br><select name="clinical_qualified"><option value="no">No</option><option value="unknown">Unknown</option><option value="yes">Yes</option></select><br><br>
            Staffing Plan Created?<br><select name="staffing_plan"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>
            Background Check Workflow Defined?<br><select name="background_check_process"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>

            <h2>Revenue & Market Strategy</h2>
            Primary Payer Strategy Defined?<br><select name="revenue_model"><option value="no">No</option><option value="private_pay">Private Pay</option><option value="medicaid">Medicaid</option><option value="medicare">Medicare</option><option value="hybrid">Hybrid</option></select><br><br>
            Reimbursement Timeline Understood?<br><select name="revenue_timeline"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>
            Referral Strategy Defined?<br><select name="referral_strategy"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>

            <h2>Operational Infrastructure</h2>
            Intake / Admission Workflow Documented?<br><select name="intake_process"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>
            EMR / Documentation System Selected?<br><select name="documentation_system"><option value="no">No</option><option value="evaluating">Evaluating</option><option value="yes">Yes</option></select><br><br>
            Service Area Defined?<br><select name="service_area"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>

            <h2>Compliance & Legal Exposure</h2>
            Policies & Procedures Ready?<br><select name="policies_ready"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>
            HIPAA Records Process in Place?<br><select name="hipaa_system"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>
            QA / Audit Process Established?<br><select name="qa_process"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>
            Incident Reporting Procedure Created?<br><select name="incident_reporting"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>

            <h2>Execution Capacity</h2>
            Weekly Launch Time Available?<br><select name="execution_time"><option value="low">Less than 5 hours/week</option><option value="medium">5-10 hours/week</option><option value="high">10+ hours/week</option></select><br><br>
            Are You Working Alone or With Support?<br><select name="support_level"><option value="alone">Alone</option><option value="some_support">Some support</option><option value="professional_support">Professional support</option></select><br><br>

            <button type="submit" style="padding:12px 18px;background:#2563eb;color:white;border:0;border-radius:8px;">Run Intelligence Audit</button>
        </form>
    </body>
    </html>
    """

@router.post("/run", response_class=HTMLResponse)
def run_audit(
    agency_name: str = Form("N/A"),
    owner_name: str = Form("N/A"),
    location: str = Form("N/A"),
    start_date: str = Form("N/A"),

    business_registered: str = Form(...),
    ein_obtained: str = Form(...),
    license_type_identified: str = Form(...),
    license_docs_ready: str = Form(...),
    inspection_ready: str = Form(...),

    rn_secured: str = Form(...),
    clinical_qualified: str = Form(...),
    staffing_plan: str = Form(...),
    background_check_process: str = Form(...),

    revenue_model: str = Form(...),
    revenue_timeline: str = Form(...),
    referral_strategy: str = Form(...),

    intake_process: str = Form(...),
    documentation_system: str = Form(...),
    service_area: str = Form(...),

    policies_ready: str = Form(...),
    hipaa_system: str = Form(...),
    qa_process: str = Form(...),
    incident_reporting: str = Form(...),

    execution_time: str = Form(...),
    support_level: str = Form(...)
):
    answers = locals()

    result = calculate_risk_score(answers)
    fixes = get_fix_instructions(result["missing_items"])
    pdf_path = generate_audit_pdf(result, fixes, agency_name, owner_name, location, start_date)

    kits_html = ""
    for item in result["missing_items"]:
        for key in KIT_MAP:
            if key in item:
                kits_html += f'<li><a href="/kits/{KIT_MAP[key]}">Fix this: {item}</a></li>'

    return f"""
    <html>
    <body style="font-family:Arial;padding:40px;">
        <h1>Startup Risk Assessment Complete</h1>
        <p><strong>{agency_name}</strong> | {location}</p>
        <p>Score: {result["risk_score"]}/100 ({result["risk_tier"]})</p>

        <h2>Download Your Report</h2>
        <a href="/audit/download?file={pdf_path}">Download Report</a>

        <h2>Recommended Solutions</h2>
        <ul>{kits_html}</ul>

        <br>
        <a href="/audit/">Run Again</a>
    </body>
    </html>
    """

@router.get("/download")
def download_pdf(file: str):
    return FileResponse(file, filename=file.split("\\")[-1])
