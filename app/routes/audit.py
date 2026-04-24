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
    <body style="font-family:Arial;padding:40px;">
        <h1>Home Health Startup Intelligence Audit</h1>

        <form method="post" action="/audit/run">
            <h2>Client Information</h2>
            Agency Name:<br><input name="agency_name"><br><br>
            Owner Name:<br><input name="owner_name"><br><br>
            Location:<br><input name="location"><br><br>
            Target Start Date:<br><input type="date" name="start_date"><br><br>

            <h2>Licensing Readiness</h2>
            Business Registered?<br><select name="business_registered"><option value="no">No</option><option value="yes">Yes</option></select><br><br>
            EIN Obtained?<br><select name="ein_obtained"><option value="no">No</option><option value="yes">Yes</option></select><br><br>
            Licensing Documentation Completed?<br><select name="license_docs_ready"><option value="no">No</option><option value="yes">Yes</option></select><br><br>
            Reviewed State Inspection Requirements?<br><select name="inspection_ready"><option value="no">No</option><option value="yes">Yes</option></select><br><br>

            <h2>Clinical & Staffing</h2>
            RN Clinical Supervisor Secured?<br><select name="rn_secured"><option value="no">No</option><option value="yes">Yes</option></select><br><br>
            Clinical Leadership Meets State Requirements?<br><select name="clinical_qualified"><option value="no">No</option><option value="yes">Yes</option></select><br><br>

            <h2>Operations</h2>
            Patient Intake Process Defined?<br><select name="intake_process"><option value="no">No</option><option value="yes">Yes</option></select><br><br>
            Documentation System Selected?<br><select name="documentation_system"><option value="no">No</option><option value="yes">Yes</option></select><br><br>

            <h2>Revenue Model</h2>
            Payer Strategy Defined?<br><select name="revenue_model"><option value="no">No</option><option value="yes">Yes</option></select><br><br>
            Understand Reimbursement Timeline?<br><select name="revenue_timeline"><option value="no">No</option><option value="yes">Yes</option></select><br><br>

            <h2>Compliance Systems</h2>
            Policies & Procedures Ready?<br><select name="policies_ready"><option value="no">No</option><option value="yes">Yes</option></select><br><br>
            HIPAA System in Place?<br><select name="hipaa_system"><option value="no">No</option><option value="yes">Yes</option></select><br><br>
            QA / Audit Process Established?<br><select name="qa_process"><option value="no">No</option><option value="yes">Yes</option></select><br><br>

            <button type="submit">Run Intelligence Audit</button>
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
    license_docs_ready: str = Form(...),
    inspection_ready: str = Form(...),
    rn_secured: str = Form(...),
    clinical_qualified: str = Form(...),
    intake_process: str = Form(...),
    documentation_system: str = Form(...),
    revenue_model: str = Form(...),
    revenue_timeline: str = Form(...),
    policies_ready: str = Form(...),
    hipaa_system: str = Form(...),
    qa_process: str = Form(...)
):
    answers = {
        "business_registered": business_registered,
        "ein_obtained": ein_obtained,
        "license_docs_ready": license_docs_ready,
        "inspection_ready": inspection_ready,
        "rn_secured": rn_secured,
        "clinical_qualified": clinical_qualified,
        "intake_process": intake_process,
        "documentation_system": documentation_system,
        "revenue_model": revenue_model,
        "revenue_timeline": revenue_timeline,
        "policies_ready": policies_ready,
        "hipaa_system": hipaa_system,
        "qa_process": qa_process
    }

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
