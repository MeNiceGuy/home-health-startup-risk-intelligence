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
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f8fafc;
            color: #0f172a;
            padding: 40px;
        }

        .tip {
            position: relative;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: #2563eb;
            color: white;
            border-radius: 50%;
            width: 18px;
            height: 18px;
            font-size: 12px;
            font-weight: bold;
            cursor: help;
            margin-left: 6px;
        }

        .tip::after {
            content: attr(data-tip);
            position: absolute;
            left: 28px;
            top: 50%;
            transform: translateY(-50%) translateX(-6px);
            width: 320px;
            background: #0f172a;
            color: white;
            padding: 12px 14px;
            border-radius: 10px;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.25);
            font-size: 13px;
            line-height: 1.45;
            opacity: 0;
            visibility: hidden;
            pointer-events: none;
            transition: all 0.18s ease;
            z-index: 999;
        }

        .tip:hover::after {
            opacity: 1;
            visibility: visible;
            transform: translateY(-50%) translateX(0);
        }

        input, select {
            padding: 9px;
            margin-top: 6px;
            min-width: 260px;
        }

        h2 {
            margin-top: 30px;
        }
    </style>
    
        <h1>Boswell Consulting Group Startup Intelligence Audit</h1>
        <p>Assess launch readiness across licensing, clinical staffing, revenue, operations, compliance, and execution capacity.</p>

        <form method="post" action="/audit/run">

            <h2>Client Information</h2>
            Agency Name: <span class="tip" data-tip="Enter the legal or planned name of the agency. Example: Boswell Home Care LLC.">?</span><br><input name="agency_name"><br>
            Owner Name: <span class="tip" data-tip="Enter the person responsible for ownership or launch execution.">?</span><br><input name="owner_name"><br>
            City / County: <span class="tip" data-tip="Enter the primary city or county where the agency will operate.">?</span><br><input name="location"><br>
            Target Start Date: <span class="tip" data-tip="Enter the date you want the agency to begin accepting clients.">?</span><span class="tip" data-tip="Your expected launch date. <br><input type="date" name="start_date"><br>

            <h2>Licensing Readiness</h2>
            Business Entity Formed? <span class="tip" data-tip="Has the company been legally created with the state? Example: LLC registered with Virginia SCC.">?</span><span class="tip" data-tip="This means your company is legally registered. <br><select name="business_registered"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br>
            EIN Obtained? <span class="tip" data-tip="Has the agency received a federal Employer Identification Number from the IRS?">?</span><span class="tip" data-tip="An EIN is your federal business tax ID. <br><select name="ein_obtained"><option value="no">No</option><option value="yes">Yes</option></select><br>
            Specific License Type Identified? <span class="tip" data-tip="Do you know which license applies to your model: home care, home health, skilled, or non-medical?">?</span><br><select name="license_type_identified"><option value="no">No</option><option value="partial">Somewhat</option><option value="yes">Yes</option></select><br>
            Licensing Documents Prepared? <span class="tip" data-tip="Have the documents needed for the state application been gathered and reviewed?">?</span><br><select name="license_docs_ready"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br>
            State Inspection / Survey Requirements Reviewed? <span class="tip" data-tip="Have you reviewed what the state may inspect before approval or operation?">?</span><br><select name="inspection_ready"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br>

            <h2>Clinical & Staffing Risk</h2>
            RN Clinical Supervisor Secured? <span class="tip" data-tip="Do you have an RN available to supervise clinical care if required by your service model?">?</span><br><select name="rn_secured"><option value="no">No</option><option value="contracted">Contracted</option><option value="yes">Yes</option></select><br>
            Clinical Leadership Meets State Requirements? <span class="tip" data-tip="Does your administrator or clinical leader meet required license, education, or experience standards?">?</span><br><select name="clinical_qualified"><option value="no">No</option><option value="unknown">Unknown</option><option value="yes">Yes</option></select><br>
            Staffing Plan Created? <span class="tip" data-tip="Have you identified required roles, hiring timing, supervision structure, and staffing gaps?">?</span><br><select name="staffing_plan"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br>
            Background Check Workflow Defined? <span class="tip" data-tip="Do you have a process for screening staff before they begin work?">?</span><br><select name="background_check_process"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br>

            <h2>Revenue & Market Strategy</h2>
            Primary Payer Strategy Defined? <span class="tip" data-tip="Do you know how the agency will get paid? Example: private pay, Medicaid, Medicare, VA, or hybrid.">?</span><span class="tip" data-tip="This means you know how the agency will get paid. <br><select name="revenue_model"><option value="no">No</option><option value="private_pay">Private Pay</option><option value="medicaid">Medicaid</option><option value="medicare">Medicare</option><option value="hybrid">Hybrid</option></select><br>
            Reimbursement Timeline Understood? <span class="tip" data-tip="Do you understand when payment is expected after services are delivered?">?</span><br><select name="revenue_timeline"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br>
            Referral Strategy Defined? <span class="tip" data-tip="Do you know where clients will come from? Example: hospitals, physicians, community partners, online leads.">?</span><span class="tip" data-tip="This means you know where clients will come from. <br><select name="referral_strategy"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br>

            <h2>Operational Infrastructure</h2>
            Intake / Admission Workflow Documented? <span class="tip" data-tip="Do you have a written process for receiving referrals, assessing clients, and starting care?">?</span><br><select name="intake_process"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br>
            EMR / Documentation System Selected? <span class="tip" data-tip="Have you selected software or a system for patient records, notes, billing, and compliance tracking?">?</span><br><select name="documentation_system"><option value="no">No</option><option value="evaluating">Evaluating</option><option value="yes">Yes</option></select><br>
            Service Area Defined? <span class="tip" data-tip="Have you identified the cities, counties, or regions your agency will serve?">?</span><br><select name="service_area"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br>

            <h2>Compliance & Legal Exposure</h2>
            Policies & Procedures Ready? <span class="tip" data-tip="Do you have written rules for care, documentation, patient rights, infection control, emergency planning, and operations?">?</span><br><select name="policies_ready"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br>
            HIPAA Records Process in Place? <span class="tip" data-tip="Do you have a secure process for storing, accessing, and protecting patient information?">?</span><br><select name="hipaa_system"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br>
            QA / Audit Process Established? <span class="tip" data-tip="Do you have a process to review documentation, care quality, incidents, and compliance trends?">?</span><br><select name="qa_process"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br>
            Incident Reporting Procedure Created? <span class="tip" data-tip="Do staff know how to document and escalate incidents, complaints, or safety concerns?">?</span><br><select name="incident_reporting"><option value="no">No</option><option value="partial">Partial</option><option value="yes">Yes</option></select><br>

            <h2>Execution Capacity</h2>
            Weekly Launch Time Available? <span class="tip" data-tip="How much focused time can you dedicate each week to completing launch tasks?">?</span><br><select name="execution_time"><option value="low">Less than 5 hours/week</option><option value="medium">5-10 hours/week</option><option value="high">10+ hours/week</option></select><br>
            Are You Working Alone or With Support? <span class="tip" data-tip="Are you launching alone or with help from partners, consultants, attorneys, or compliance advisors?">?</span><br><select name="support_level"><option value="alone">Alone</option><option value="some_support">Some support</option><option value="professional_support">Professional support</option></select><br>

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
