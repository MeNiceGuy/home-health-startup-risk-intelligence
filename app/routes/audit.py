from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, FileResponse
from app.services.risk_engine import calculate_risk_score
from app.services.fix_engine import get_fix_instructions
from app.services.pdf_engine import generate_audit_pdf
from app.services.kit_mapper import KIT_MAP
from app.services.state_regulatory_engine import generate_regulatory_intelligence

router = APIRouter(prefix="/audit", tags=["Audit"])

def text_field(label, name, tip, field_type="text"):
    return f"""
    <div class="field">
        <label>{label} <span class="tip" data-tip="{tip}">?</span></label>
        <input type="{field_type}" name="{name}">
    </div>
    """

def select_field(label, name, options, tip):
    opts = "".join([f'<option value="{v}">{t}</option>' for v,t in options])
    return f"""
    <div class="field">
        <label>{label} <span class="tip" data-tip="{tip}">?</span></label>
        <select name="{name}">{opts}</select>
    </div>
    """

@router.get("/", response_class=HTMLResponse)
def audit_form():
    yn = [("no","No"),("yes","Yes")]
    ypn = [("no","No"),("partial","Partial"),("yes","Yes")]

    return f"""
    <html>
    <head>
    <style>
        body {{ font-family:Arial; background:#f8fafc; margin:0; padding:0; color:#0f172a; }}
        .container {{ max-width:1100px; margin:40px auto; padding:20px; }}
        .card {{ background:white; padding:25px; border-radius:14px; margin-bottom:20px; box-shadow:0 6px 18px rgba(0,0,0,.08); }}
        .grid {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
        .field label {{ font-weight:bold; display:block; margin-bottom:6px; }}
        select, input {{ width:100%; padding:11px; border-radius:8px; border:1px solid #cbd5e1; font-size:15px; }}
        .tip {{ position:relative; display:inline-flex; align-items:center; justify-content:center; background:#2563eb; color:white; border-radius:50%; width:18px; height:18px; font-size:12px; margin-left:6px; cursor:help; }}
        .tip::after {{ content:attr(data-tip); position:absolute; left:26px; top:50%; transform:translateY(-50%) translateX(-6px); width:300px; background:#0f172a; color:white; padding:12px; border-radius:10px; font-size:13px; line-height:1.4; opacity:0; visibility:hidden; transition:all .18s ease; z-index:999; box-shadow:0 12px 30px rgba(0,0,0,.25); }}
        .tip:hover::after {{ opacity:1; visibility:visible; transform:translateY(-50%) translateX(0); }}
        button {{ background:#2563eb; color:white; padding:14px 20px; border:none; border-radius:10px; font-weight:bold; cursor:pointer; }}
    </style>
    </head>
    <body>
    <div class="container">
        <div class="card">
            <h1>Boswell Consulting Group Startup Intelligence Audit</h1>
            <p>Diagnose licensing, staffing, compliance, and revenue risks before launch.</p>
        </div>

        <form method="post" action="/audit/run">

            <div class="card"><h2>Client Information</h2><div class="grid">
                {text_field("Agency Name", "agency_name", "Enter the legal or planned name of the agency. Example: Boswell Home Care LLC.")}
                {text_field("Owner Name", "owner_name", "Enter the owner, founder, or person responsible for launch execution.")}
                {text_field("City / County", "location", "Enter the primary city, county, or region where the agency will operate.")}
                {text_field("Target Start Date", "start_date", "Enter the date you want to begin accepting clients.", "date")}
            </div></div>

            <div class="card"><h2>Licensing Readiness</h2><div class="grid">
                {select_field("Business Entity Formed?", "business_registered", ypn, "Has the company been legally created with the state? Example: LLC registered with Virginia SCC.")}
                {select_field("EIN Obtained?", "ein_obtained", yn, "Has the agency received a federal Employer Identification Number from the IRS?")}
                {select_field("Specific License Type Identified?", "license_type_identified", ypn, "Do you know whether your model requires home care, home health, skilled, or non-medical licensing?")}
                {select_field("Licensing Documents Prepared?", "license_docs_ready", ypn, "Have required application documents been gathered, completed, and reviewed?")}
                {select_field("State Inspection / Survey Requirements Reviewed?", "inspection_ready", ypn, "Have you reviewed what the state may inspect before approval or operation?")}
            </div></div>

            <div class="card"><h2>Clinical & Staffing Risk</h2><div class="grid">
                {select_field("RN Clinical Supervisor Secured?", "rn_secured", [("no","No"),("contracted","Contracted"),("yes","Yes")], "Do you have an RN available to supervise clinical care if required by your service model?")}
                {select_field("Clinical Leadership Meets State Requirements?", "clinical_qualified", [("no","No"),("unknown","Unknown"),("yes","Yes")], "Does leadership meet required license, education, or experience standards?")}
                {select_field("Staffing Plan Created?", "staffing_plan", ypn, "Have you identified required roles, hiring timing, supervision structure, and staffing gaps?")}
                {select_field("Background Check Workflow Defined?", "background_check_process", ypn, "Do you have a process for screening staff before they begin work?")}
            </div></div>

            <div class="card"><h2>Revenue & Market Strategy</h2><div class="grid">
                {select_field("Primary Payer Strategy Defined?", "revenue_model", [("no","No"),("private_pay","Private Pay"),("medicaid","Medicaid"),("medicare","Medicare"),("hybrid","Hybrid")], "Do you know how the agency will get paid? Example: private pay, Medicaid, Medicare, VA, or hybrid.")}
                {select_field("Reimbursement Timeline Understood?", "revenue_timeline", ypn, "Do you understand when payment is expected after services are delivered?")}
                {select_field("Referral Strategy Defined?", "referral_strategy", ypn, "Do you know where clients will come from? Example: hospitals, physicians, community partners, online leads.")}
            </div></div>

            <div class="card"><h2>Operational Infrastructure</h2><div class="grid">
                {select_field("Intake / Admission Workflow Documented?", "intake_process", ypn, "Do you have a written process for receiving referrals, assessing clients, and starting care?")}
                {select_field("EMR / Documentation System Selected?", "documentation_system", [("no","No"),("evaluating","Evaluating"),("yes","Yes")], "Have you selected software or a system for patient records, care notes, billing, and compliance tracking?")}
                {select_field("Service Area Defined?", "service_area", ypn, "Have you identified the cities, counties, or regions your agency will serve?")}
            </div></div>

            <div class="card"><h2>Compliance & Legal Exposure</h2><div class="grid">
                {select_field("Policies & Procedures Ready?", "policies_ready", ypn, "Do you have written rules for care, documentation, patient rights, infection control, emergency planning, and operations?")}
                {select_field("HIPAA Records Process in Place?", "hipaa_system", ypn, "Do you have a secure process for storing, accessing, and protecting patient information?")}
                {select_field("QA / Audit Process Established?", "qa_process", ypn, "Do you have a process to review documentation, care quality, incidents, and compliance trends?")}
                {select_field("Incident Reporting Procedure Created?", "incident_reporting", ypn, "Do staff know how to document and escalate incidents, complaints, or safety concerns?")}
            </div></div>

            <div class="card"><h2>Execution Capacity</h2><div class="grid">
                {select_field("Weekly Launch Time Available?", "execution_time", [("low","Less than 5 hours/week"),("medium","5-10 hours/week"),("high","10+ hours/week")], "How much focused time can you dedicate each week to completing launch tasks?")}
                {select_field("Working Alone or With Support?", "support_level", [("alone","Alone"),("some_support","Some support"),("professional_support","Professional support")], "Are you launching alone or with help from partners, consultants, attorneys, or compliance advisors?")}
            </div></div>

            <button type="submit">Run Intelligence Audit</button>
        </form>
    </div>
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
    inspection_ready: str = Form("no"),
    rn_secured: str = Form(...),
    clinical_qualified: str = Form(...),
    staffing_plan: str = Form("no"),
    background_check_process: str = Form("no"),
    revenue_model: str = Form(...),
    revenue_timeline: str = Form(...),
    referral_strategy: str = Form("no"),
    intake_process: str = Form("no"),
    documentation_system: str = Form("no"),
    service_area: str = Form("no"),
    policies_ready: str = Form(...),
    hipaa_system: str = Form(...),
    qa_process: str = Form("no"),
    incident_reporting: str = Form("no"),
    execution_time: str = Form("low"),
    support_level: str = Form("alone")
):
    answers = locals()
    result = calculate_risk_score(answers)
    fixes = get_fix_instructions(result["missing_items"])
    regulatory = generate_regulatory_intelligence(state, agency_type, revenue_model, answers)
    pdf_path = generate_audit_pdf(result, fixes, agency_name, owner_name, location, start_date)
    regulatory_findings_html = "".join([f"<li>{x}</li>" for x in regulatory.get("findings", [])])
    regulatory_blockers_html = "".join([f"<li>{x}</li>" for x in regulatory.get("blockers", [])])
    regulatory_kits_html = "".join([f"<li>{x}</li>" for x in regulatory.get("recommended_kits", [])])

    kits_html = ""
    for item in result["missing_items"]:
        for key in KIT_MAP:
            if key in item:
                kits_html += f'<li><a href="/kits/{KIT_MAP[key]}">Fix this: <a href="/checkout/{item}</a>">Purchase Solution</a></li>'

    return f"""
    <html><body style="font-family:Arial;padding:40px;">
        <h1>Startup Risk Assessment Complete</h1>
        <p><strong>{agency_name}</strong> | {location}</p>
        <p>Score: {result["risk_score"]}/100 ({result["risk_tier"]})</p>
        <h2>Download Your Report</h2>
        <a href="/audit/download?file={pdf_path}">Download Report</a>
        <h2>Regulatory Intelligence</h2>
        <p><strong>Authority:</strong> {regulatory.get("authority")}</p>
        <p><strong>Regulatory Risk:</strong> {regulatory.get("risk_level")}</p>
        <h3>Regulatory Findings</h3>
        <ul>{regulatory_findings_html}</ul>
        <h3>Regulatory Blockers</h3>
        <ul>{regulatory_blockers_html}</ul>
        <h3>Recommended Regulatory Kits</h3>
        <ul>{regulatory_kits_html}</ul>

        <h2>Recommended Solutions</h2>
        <ul>{kits_html}</ul>
        <br><a href="/audit/">Run Again</a>
    </body></html>
    """

@router.get("/download")
def download_pdf(file: str):
    return FileResponse(file, filename=file.split("\\")[-1])
