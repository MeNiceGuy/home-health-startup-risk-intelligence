from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from app.services.templates import templates
import json

router = APIRouter(prefix="/operating-audit", tags=["Operating Intelligence"])

def risk_score(value, benchmark, higher_is_bad=True):
    try:
        value = float(value or 0)
        benchmark = float(benchmark or 1)
        ratio = value / benchmark if higher_is_bad else benchmark / value if value else 2
        if ratio <= 1: return 90
        if ratio <= 1.25: return 75
        if ratio <= 1.5: return 60
        return 35
    except:
        return 40

def kit_for(area):
    kits = {
        "Revenue Cycle": ("Revenue Cycle Starter Kit", "$199", "/templates/revenue"),
        "Operations": ("Operations Workflow Kit", "$199", "/templates/operations"),
        "Staffing": ("Hiring & Retention Kit", "$179", "/templates/hiring"),
        "Compliance": ("Compliance Policy Pack", "$199", "/templates/compliance")
    }
    return kits.get(area, ("Business Optimization Kit", "$199", "/templates/operations"))

def diagnose(data):
    issues = []
    if data["denial_rate"] > 10:
        issues.append(("Revenue Cycle","High Claim Denial Risk","Claims may be submitted without strong pre-billing review, documentation validation, or denial tracking."))
    if data["ar_days"] > 30:
        issues.append(("Revenue Cycle","Slow Cash Collection","Payment collection is slower than target and may weaken payroll, reinvestment, and growth capacity."))
    if data["intake_time"] > 2:
        issues.append(("Operations","Slow Intake Conversion","The agency may lack a clear intake checklist, referral workflow, or owner assignment."))
    if data["missed_visits"] > 5:
        issues.append(("Operations","Missed Visit Exposure","Missed visits often indicate scheduling weakness, staffing shortages, or poor backup coverage."))
    if data["turnover"] > 30:
        issues.append(("Staffing","Retention Breakdown","High turnover suggests onboarding, pay, scheduling, culture, or workload problems."))
    if data["open_roles"] > 1:
        issues.append(("Staffing","Capacity Constraint","Open roles limit census growth and increase strain on current staff."))
    if data["qa_score"] < 90:
        issues.append(("Compliance","QA Audit Weakness","Low QA scores suggest documentation defects or weak internal review."))
    if data["hipaa_score"] < 95:
        issues.append(("Compliance","HIPAA Exposure","Privacy and security controls may be incomplete."))
    return issues

def diagnosis_html(issues):
    html = ""
    for area, issue, explanation in issues:
        kit, price, link = kit_for(area)
        html += f"""
        <div class='diag'>
            <h3>{area}: {issue}</h3>
            <p><strong>Root Cause:</strong> {explanation}</p>
            <p><strong>Business Impact:</strong> This can create revenue leakage, compliance exposure, operational delays, and scaling limits.</p>
            <p><strong>Recommended Fix:</strong> Install a repeatable system with ownership, checklist controls, documentation standards, and weekly review.</p>
            <div class='offer'>
                <strong>Recommended Template Kit:</strong> {kit}<br>
                <strong>Startup-Friendly Price:</strong> {price}<br><br>
                <a href='{link}'>Buy Separate Kit</a>
            </div>
        </div>
        """
    return html or "<p>No major root-cause gaps detected from current inputs.</p>"

@router.get("/", response_class=HTMLResponse)
def form(request: Request):
    form_sections = """
    <div class='card'><h2>Revenue Cycle</h2><div class='grid'>
      <div><label>Days in A/R</label><input name='ar_days' value='45'><div class='tooltip'>Average days to collect payment. Target: under 30.</div></div>
      <div><label>Denial Rate (%)</label><input name='denial_rate' value='15'><div class='tooltip'>Percent of claims denied. Target: 10% or lower.</div></div>
    </div></div>

    <div class='card'><h2>Operations</h2><div class='grid'>
      <div><label>Intake Time (days)</label><input name='intake_time' value='5'><div class='tooltip'>Referral to completed intake. Target: 1-2 days.</div></div>
      <div><label>Missed Visits (%)</label><input name='missed_visits' value='8'><div class='tooltip'>Missed or incomplete visits. Target: 5% or lower.</div></div>
    </div></div>

    <div class='card'><h2>Staffing</h2><div class='grid'>
      <div><label>Open Roles</label><input name='open_roles' value='3'><div class='tooltip'>Unfilled roles limiting growth or coverage.</div></div>
      <div><label>Turnover Rate (%)</label><input name='turnover' value='40'><div class='tooltip'>Annual staff turnover. Target: 30% or lower.</div></div>
    </div></div>

    <div class='card'><h2>Compliance</h2><div class='grid'>
      <div><label>QA Audit Score (%)</label><input name='qa_score' value='75'><div class='tooltip'>Internal quality/documentation audit score. Target: 90%+.</div></div>
      <div><label>HIPAA Score (%)</label><input name='hipaa_score' value='85'><div class='tooltip'>Privacy, security, access control, and records protection readiness. Target: 95%+.</div></div>
    </div></div>
    """
    return templates.TemplateResponse("operating_intake.html", {"request": request, "form_sections": form_sections})

@router.post("/run", response_class=HTMLResponse)
def run(
    request: Request,
    ar_days: float = Form(0),
    denial_rate: float = Form(0),
    intake_time: float = Form(0),
    missed_visits: float = Form(0),
    open_roles: float = Form(0),
    turnover: float = Form(0),
    qa_score: float = Form(0),
    hipaa_score: float = Form(0)
):
    data = {
        "ar_days": ar_days,
        "denial_rate": denial_rate,
        "intake_time": intake_time,
        "missed_visits": missed_visits,
        "open_roles": open_roles,
        "turnover": turnover,
        "qa_score": qa_score,
        "hipaa_score": hipaa_score
    }

    issues = diagnose(data)

    financial = int((risk_score(ar_days, 30) + risk_score(denial_rate, 10)) / 2)
    operations = int((risk_score(intake_time, 2) + risk_score(missed_visits, 5)) / 2)
    staffing = int((risk_score(open_roles, 1) + risk_score(turnover, 30)) / 2)
    compliance = int((risk_score(qa_score, 90, False) + risk_score(hipaa_score, 95, False)) / 2)
    total = int((financial + operations + staffing + compliance) / 4)

    lost_revenue = int((denial_rate - 10) * 1000) if denial_rate > 10 else 0
    delay_cost = int((ar_days - 30) * 500) if ar_days > 30 else 0
    total_impact = lost_revenue + delay_cost

    categories = list(set([i[0] for i in issues]))
    bundle = None
    if len(categories) >= 3:
        bundle = {
            "name": "Startup Operations Stabilization Bundle",
            "price": "$799",
            "desc": "A bundled system to fix revenue cycle, operations, staffing, and compliance gaps together.",
            "link": "/bundle/startup-stabilization"
        }
    elif len(categories) == 2:
        bundle = {
            "name": "Targeted Growth Repair Bundle",
            "price": "$499",
            "desc": "A focused bundle to fix the two highest-risk areas limiting growth.",
            "link": "/bundle/targeted-growth"
        }

    context = {
        "request": request,
        "total": total,
        "financial": financial,
        "operations": operations,
        "staffing": staffing,
        "compliance": compliance,
        "lost_revenue": lost_revenue,
        "delay_cost": delay_cost,
        "total_impact": total_impact,
        "root_html": diagnosis_html(issues),
        "bundle": bundle,
        "labels": json.dumps(["Financial","Operations","Staffing","Compliance"]),
        "scores": json.dumps([financial, operations, staffing, compliance])
    }

    return templates.TemplateResponse("operating_report.html", context)
