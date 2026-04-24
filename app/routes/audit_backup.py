from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, FileResponse
from app.services.risk_engine import calculate_risk_score
from app.services.fix_engine import get_fix_instructions
from app.services.pdf_engine import generate_audit_pdf
from app.services.kit_mapper import KIT_MAP

router = APIRouter(prefix="/audit", tags=["Audit"])

def q(label, name, options, tip):
    opts = "".join([f'<option value="{v}">{t}</option>' for v, t in options])
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
        body {{ margin:0; font-family:Arial, sans-serif; background:#f8fafc; color:#0f172a; }}
        .wrap {{ max-width:1050px; margin:40px auto; padding:20px; }}
        .hero {{ background:#0f172a; color:white; padding:35px; border-radius:18px; margin-bottom:25px; }}
        .section {{ background:white; padding:28px; border-radius:16px; margin-bottom:22px; box-shadow:0 8px 24px rgba(15,23,42,.08); }}
        .grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:20px; }}
        .field label {{ display:block; font-weight:700; margin-bottom:8px; }}
        input, select {{ width:100%; padding:12px; border:1px solid #cbd5e1; border-radius:10px; font-size:15px; }}
        .tip {{ position:relative; display:inline-flex; align-items:center; justify-content:center; background:#2563eb; color:white; border-radius:50%; width:18px; height:18px; font-size:12px; cursor:help; }}
        .tip:hover::after {{ content:attr(data-tip); position:absolute; left:24px; top:-8px; width:300px; background:#0f172a; color:white; padding:12px; border-radius:10px; z-index:999; line-height:1.4; box-shadow:0 12px 30px rgba(0,0,0,.25); }}
        button {{ background:#2563eb; color:white; padding:14px 22px; border:0; border-radius:10px; font-weight:bold; cursor:pointer; }}
    </style>
    </head>
    <body>
    <div class="wrap">
        <div class="hero">
            <h1>Boswell Consulting Group Startup Intelligence Audit</h1>
            <p>Assess launch readiness across licensing, staffing, revenue, operations, compliance, and execution capacity.</p>
        </div>

        <form method="post" action="/audit/run">
            <div class="section">
                <h2>Client Information</h2>
                <div class="grid">
                    <div class="field"><label>Agency Name</label><input name="agency_name"></div>
                    <div class="field"><label>Owner Name</label><input name="owner_name"></div>
                    <div class="field"><label>City / County</label><input name="location"></div>
                    <div class="field"><label>Target Start Date</label><input type="date" name="start_date"></div>
                </div>
            </div>

            <div class="section"><h2>Licensing Readiness</h2><div class="grid">
                {q("Business Entity Formed?", "business_registered", ypn, "Has the company been legally created with the state?")}
                {q("EIN Obtained?", "ein_obtained", yn, "Federal tax ID used for banking, hiring, and tax filings.")}
                {q("Specific License Type Identified?", "license_type_identified", ypn, "Do you know which license applies to your care model?")}
                {q("Licensing Documents Prepared?", "license_docs_ready", ypn, "Have required application documents been gathered and reviewed?")}
                {q("State Inspection / Survey Requirements Reviewed?", "inspection_ready", ypn, "Have you reviewed what the state may inspect?")}
            </div></div>

            <div class="section"><h2>Clinical & Staffing Risk</h2><div class="grid">
                {q("RN Clinical Supervisor Secured?", "rn_secured", [("no","No"),("contracted","Contracted"),("yes","Yes")], "Do you have an RN available to supervise care if required?")}
                {q("Clinical Leadership Meets State Requirements?", "clinical_qualified", [("no","No"),("unknown","Unknown"),("yes","Yes")], "Does leadership meet required license, education, or experience standards?")}
                {q("Staffing Plan Created?", "staffing_plan", ypn, "Have you identified roles, timing, and supervision structure?")}
                {q("Background Check Workflow Defined?", "background_check_process", ypn, "Do you have a staff screening process?")}
            </div></div>

            <div class="section"><h2>Revenue & Market Strategy</h2><div class="grid">
                {q("Primary Payer Strategy Defined?", "revenue_model", [("no","No"),("private_pay","Private Pay"),("medicaid","Medicaid"),("medicare","Medicare"),("hybrid","Hybrid")], "How will the agency get paid?")}
                {q("Reimbursement Timeline Understood?", "revenue_timeline", ypn, "Do you know when payment is expected after services?")}
                {q("Referral Strategy Defined?", "referral_strategy", ypn, "Do you know where clients will come from?")}
            </div></div>

            <div class="section"><h2>Operational Infrastructure</h2><div class="grid">
                {q("Intake / Admission Workflow Documented?", "intake_process", ypn, "Written process for referrals, assessments, and starting care.")}
                {q("EMR / Documentation System Selected?", "documentation_system", [("no","No"),("evaluating","Evaluating"),("yes","Yes")], "Software/system for records, notes, billing, and compliance.")}
                {q("Service Area Defined?", "service_area", ypn, "Cities, counties, or regions your agency will serve.")}
            </div></div>

            <div class="section"><h2>Compliance & Legal Exposure</h2><div class="grid">
                {q("Policies & Procedures Ready?", "policies_ready", ypn, "Written rules for care, documentation, patient rights, and operations.")}
                {q("HIPAA Records Process in Place?", "hipaa_system", ypn, "Secure process for storing and protecting patient information.")}
                {q("QA / Audit Process Established?", "qa_process", ypn, "Process to review documentation, care quality, and compliance risks.")}
                {q("Incident Reporting Procedure Created?", "incident_reporting", ypn, "Process for incidents, complaints, or safety concerns.")}
            </div></div>

            <div class="section"><h2>Execution Capacity</h2><div class="grid">
                {q("Weekly Launch Time Available?", "execution_time", [("low","Less than 5 hours/week"),("medium","5-10 hours/week"),("high","10+ hours/week")], "How much time can you dedicate weekly?")}
                {q("Working Alone or With Support?", "support_level", [("alone","Alone"),("some_support","Some support"),("professional_support","Professional support")], "Support may include consultants, attorneys, or advisors.")}
            </div></div>

            <button type="submit">Run Intelligence Audit</button>
        </form>
    </div>
    </body>
    </html>
    """

# keep your existing POST/download routes below if they already exist
