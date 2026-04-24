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
    <body style="font-family:Arial;background:#f8fafc;padding:40px;"><style>.tip{display:inline-block;background:#2563eb;color:white;border-radius:50%;width:18px;height:18px;text-align:center;font-size:12px;line-height:18px;cursor:pointer;margin-left:6px}.tip:hover::after{content:attr(data-tip);position:absolute;background:#0f172a;color:white;padding:10px;border-radius:8px;width:280px;margin-left:10px;z-index:99;font-size:13px;line-height:1.4}</style>
        <h1>Boswell Consulting Group Startup Intelligence Audit</h1>
        <p>Assess launch readiness across licensing, clinical staffing, revenue, operations, compliance, and execution capacity.</p>

        <form method="post" action="/audit/run">

            <h2>Client Information</h2>
            Agency Name:<br><input name="agency_name"><br><br>
            Owner Name:<br><input name="owner_name"><br><br>
            City / County:<br><input name="location"><br><br>
            Target Start Date:<br><input type="date" name="start_date"><br><br>

            <h2>Licensing Readiness</h2>
            Business Entity Formed? <span class="tip" data-tip="This means your company is legally registered. Example: LLC filed with the Virginia SCC.">?</span><br><small>What this means: Your company is legally registered.<br>Why it matters: Required before licensing.<br>Example: LLC filed with Virginia SCC.</small><br><select name="business_registered"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>
            EIN Obtained? <span class="tip" data-tip="An EIN is your federal business tax ID. Example: IRS-issued EIN used for banking, hiring, and tax filings.">?</span><br><select name="ein_obtained"><option value="no">No</option><option value="yes">Yes</option></select><br><br>
            Specific License Type Identified? <span class="tip" data-tip="This means you know whether you need a home care, home health, skilled, or non-medical license.">?</span><br><select name="license_type_identified"><option value="no">No</option><option value="partial">Somewhat</option><option value="yes">Yes</option></select><br><br>
            Licensing Documents Prepared? <span class="tip" data-tip="This means your required application documents are gathered and ready for submission.">?</span><br><select name="license_docs_ready"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>
            State Inspection / Survey Requirements Reviewed? <span class="tip" data-tip="This means you understand what the state may review before approval or operation.">?</span><br><select name="inspection_ready"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>

            <h2>Clinical & Staffing Risk</h2>
            RN Clinical Supervisor Secured? <span class="tip" data-tip="This means you have an RN available to oversee clinical care if required for your model.">?</span><br><small>What this means: A registered nurse oversees care delivery.<br>Why it matters: Required for compliance and operations.<br>Example: Contracted RN supervising patient care.</small><br><select name="rn_secured"><option value="no">No</option><option value="contracted">Contracted</option><option value="yes">Yes</option></select><br><br>
            Clinical Leadership Meets State Requirements? <span class="tip" data-tip="This means the administrator or clinical leader meets required education, license, and experience standards.">?</span><br><select name="clinical_qualified"><option value="no">No</option><option value="unknown">Unknown</option><option value="yes">Yes</option></select><br><br>
            Staffing Plan Created?<br><select name="staffing_plan"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>
            Background Check Workflow Defined?<br><select name="background_check_process"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>

            <h2>Revenue & Market Strategy</h2>
            Primary Payer Strategy Defined? <span class="tip" data-tip="This means you know how the agency will get paid. Example: private pay, Medicaid, Medicare, VA, or hybrid model.">?</span><br><small>What this means: How you will get paid.<br>Why it matters: Determines cash flow and survival.<br>Example: Private pay vs Medicaid vs Medicare.</small><br><select name="revenue_model"><option value="no">No</option><option value="private_pay">Private Pay</option><option value="medicaid">Medicaid</option><option value="medicare">Medicare</option><option value="hybrid">Hybrid</option></select><br><br>
            Reimbursement Timeline Understood? <span class="tip" data-tip="This means you understand when cash will actually come in after services are provided.">?</span><br><select name="revenue_timeline"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>
            Referral Strategy Defined?<br><select name="referral_strategy"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>

            <h2>Operational Infrastructure</h2>
            Intake / Admission Workflow Documented?<br><select name="intake_process"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>
            EMR / Documentation System Selected? <span class="tip" data-tip="This means you selected software or a system for patient records, notes, compliance, and billing support.">?</span><br><select name="documentation_system"><option value="no">No</option><option value="evaluating">Evaluating</option><option value="yes">Yes</option></select><br><br>
            Service Area Defined?<br><select name="service_area"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>

            <h2>Compliance & Legal Exposure</h2>
            Policies & Procedures Ready? <span class="tip" data-tip="These are written rules for care, documentation, patient rights, infection control, emergency planning, and operations.">?</span><br><small>What this means: Written operational and compliance guidelines.<br>Why it matters: Required for licensing and audits.<br>Example: Infection control, patient rights policies.</small><br><select name="policies_ready"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>
            HIPAA Records Process in Place? <span class="tip" data-tip="This means patient information is stored, accessed, and protected securely under HIPAA expectations.">?</span><br><small>What this means: Secure handling of patient data.<br>Why it matters: Legal requirement with penalties.<br>Example: Encrypted EMR system.</small><br><select name="hipaa_system"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>
            QA / Audit Process Established? <span class="tip" data-tip="This means you regularly review documentation, care quality, incidents, and compliance risks.">?</span><br><select name="qa_process"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br><br>
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
