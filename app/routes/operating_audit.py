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
        if ratio <= 1:
            return 90
        if ratio <= 1.25:
            return 75
        if ratio <= 1.5:
            return 60
        return 35
    except Exception:
        return 40

def yes_no_bad(value):
    return str(value or "").strip().lower() in ["no", "none", "manual", "unknown", "not sure", ""]

def field(label, name, value, tip):
    return f"""
    <div class="field">
      <label>{label} <span class="info">ⓘ</span></label>
      <input name="{name}" value="{value}">
      <div class="tooltip">{tip}</div>
    </div>
    """

def root_cause_diagnosis(data):
    diagnoses = []

    if float(data["denial_rate"]) > 10:
        diagnoses.append(("Revenue Cycle", "High denial rate", "Likely caused by weak billing review, incomplete documentation, payer rule errors, or no denial tracking process."))

    if yes_no_bad(data["billing_process"]):
        diagnoses.append(("Revenue Cycle", "No defined billing workflow", "Billing is likely dependent on memory instead of a repeatable process."))

    if str(data["billing_owner"]).lower() in ["owner", "none", "unknown"]:
        diagnoses.append(("Administration", "Billing ownership risk", "Owner-handled or unclear billing ownership may create bottlenecks and delayed follow-up."))

    if float(data["intake_time"]) > 2:
        diagnoses.append(("Operations", "Slow intake process", "Likely caused by unclear referral handling, missing intake checklist, or manual coordination."))

    if str(data["schedule_system"]).lower() in ["none", "manual", "paper"]:
        diagnoses.append(("Operations", "Scheduling system weakness", "Manual scheduling increases missed visits, communication gaps, and scaling limits."))

    if float(data["missed_visits"]) > 5:
        diagnoses.append(("Operations", "Missed visit risk", "Likely caused by staffing shortages, weak backup coverage, or poor scheduling controls."))

    if yes_no_bad(data["doc_same_day"]):
        diagnoses.append(("Documentation", "Documentation lag risk", "Delayed documentation can slow billing, weaken compliance, and reduce audit readiness."))

    if float(data["open_roles"]) > 1:
        diagnoses.append(("Staffing", "Capacity gap", "Open roles may limit growth and increase missed visits."))

    if float(data["turnover"]) > 30:
        diagnoses.append(("Staffing", "High turnover risk", "Turnover may indicate weak onboarding, poor retention, compensation pressure, or scheduling strain."))

    if yes_no_bad(data["hiring_process"]):
        diagnoses.append(("Staffing", "No repeatable hiring pipeline", "Growth will be limited because recruiting, screening, onboarding, and training are not systemized."))

    if yes_no_bad(data["backup_staff"]):
        diagnoses.append(("Staffing", "No backup coverage", "Call-outs can become missed visits, client dissatisfaction, and compliance exposure."))

    if float(data["qa_score"]) < 90:
        diagnoses.append(("Compliance", "QA audit weakness", "The agency may have documentation defects, policy gaps, or inconsistent internal review processes."))

    if yes_no_bad(data["policies_updated"]):
        diagnoses.append(("Compliance", "Policy maintenance gap", "Policies may not reflect current operations, payer requirements, or regulatory expectations."))

    if yes_no_bad(data["incident_tracking"]):
        diagnoses.append(("Compliance", "Incident reporting gap", "Events may not be documented, trended, escalated, or used for quality improvement."))

    if float(data["hipaa_score"]) < 95:
        diagnoses.append(("Compliance", "HIPAA exposure", "Patient information controls may be incomplete, increasing privacy, security, and audit risk."))

    return diagnoses

def diagnosis_html(diagnoses):
    if not diagnoses:
        return "<p>No major root-cause gaps detected based on current inputs.</p>"

    html = ""
    for area, issue, cause in diagnoses:
        templates = template_recommendations(issue)
        html += f"<div class='diag'><h3>{area}: {issue}</h3><p>{cause}</p></div>"
    return html

@router.get("/", response_class=HTMLResponse)
def form(request: Request):
    form_sections = f"""
    <div class="card"><h2>Revenue Cycle Intelligence</h2><div class="grid">
    {field("Days in A/R", "ar_days", "45", "Average days to collect payment after billing. Target: under 30 days.")}
    {field("Denial Rate (%)", "denial_rate", "15", "Percent of claims denied. Target: 10% or lower.")}
    {field("Clean Claim Rate (%)", "clean_rate", "80", "Percent of claims accepted without correction. Target: 90% or higher.")}
    {field("Billing Process Defined?", "billing_process", "No", "Example: coding, claim submission, denial follow-up, and payment posting.")}
    {field("Who Handles Billing?", "billing_owner", "Owner", "Example: owner, biller, outsourced billing company, or office manager.")}
    </div></div>

    <div class="card"><h2>Operations Intelligence</h2><div class="grid">
    {field("Intake Time (days)", "intake_time", "5", "Time from referral/client inquiry to completed intake. Target: 1-2 days.")}
    {field("Scheduling System Used?", "schedule_system", "Manual", "Example: EMR scheduling, spreadsheet, paper calendar, or no system.")}
    {field("Missed Visits (%)", "missed_visits", "8", "Percent of scheduled visits missed or not completed. Target: 5% or lower.")}
    {field("Documentation Completed Same Day?", "doc_same_day", "No", "Same-day notes reduce billing delays and audit exposure.")}
    </div></div>

    <div class="card"><h2>Staffing Intelligence</h2><div class="grid">
    {field("Open Roles", "open_roles", "3", "Current unfilled positions affecting operations or growth.")}
    {field("Turnover Rate (%)", "turnover", "40", "Percent of staff leaving annually. Target: 30% or lower.")}
    {field("Hiring Process Defined?", "hiring_process", "No", "Example: recruiting source, screening, background checks, onboarding, training.")}
    {field("Backup Coverage Available?", "backup_staff", "No", "Backup staff for call-outs, emergencies, or schedule gaps.")}
    </div></div>

    <div class="card"><h2>Compliance Intelligence</h2><div class="grid">
    {field("QA Audit Score (%)", "qa_score", "75", "Internal audit score for documentation, care records, policy compliance, and quality checks. Target: 90%+.")}
    {field("Policies Updated?", "policies_updated", "No", "Current policies for HIPAA, patient rights, infection control, incident reporting, and operations.")}
    {field("Incident Tracking System?", "incident_tracking", "No", "Formal tracking for complaints, incidents, missed visits, errors, and corrective actions.")}
    {field("HIPAA Compliance Score (%)", "hipaa_score", "85", "Privacy, security, access control, breach response, and record protection readiness. Target: 95%+.")}
    </div></div>
    """

    return templates.TemplateResponse("operating_intake.html", {
        "request": request,
        "form_sections": form_sections
    })

@router.post("/run", response_class=HTMLResponse)
def run(
    request: Request,
    ar_days: float = Form(0),
    denial_rate: float = Form(0),
    clean_rate: float = Form(80),
    billing_process: str = Form("No"),
    billing_owner: str = Form("Owner"),
    intake_time: float = Form(0),
    schedule_system: str = Form("Manual"),
    missed_visits: float = Form(0),
    doc_same_day: str = Form("No"),
    open_roles: float = Form(0),
    turnover: float = Form(0),
    hiring_process: str = Form("No"),
    backup_staff: str = Form("No"),
    qa_score: float = Form(0),
    policies_updated: str = Form("No"),
    incident_tracking: str = Form("No"),
    hipaa_score: float = Form(0)
):
    data = {
        "ar_days": ar_days,
        "denial_rate": denial_rate,
        "clean_rate": clean_rate,
        "billing_process": billing_process,
        "billing_owner": billing_owner,
        "intake_time": intake_time,
        "schedule_system": schedule_system,
        "missed_visits": missed_visits,
        "doc_same_day": doc_same_day,
        "open_roles": open_roles,
        "turnover": turnover,
        "hiring_process": hiring_process,
        "backup_staff": backup_staff,
        "qa_score": qa_score,
        "policies_updated": policies_updated,
        "incident_tracking": incident_tracking,
        "hipaa_score": hipaa_score
    }

    diagnoses = root_cause_diagnosis(data)

    financial = int((risk_score(ar_days, 30) + risk_score(denial_rate, 10) + risk_score(clean_rate, 90, False)) / 3)
    operations = int((risk_score(intake_time, 2) + risk_score(missed_visits, 5)) / 2)
    staffing = int((risk_score(open_roles, 1) + risk_score(turnover, 30)) / 2)
    compliance = int((risk_score(qa_score, 90, False) + risk_score(hipaa_score, 95, False)) / 2)
    total = int((financial + operations + staffing + compliance) / 4)

    lost_revenue = int((denial_rate - 10) * 1000) if denial_rate > 10 else 0
    delay_cost = int((ar_days - 30) * 500) if ar_days > 30 else 0
    total_impact = lost_revenue + delay_cost

    labels = ["Financial", "Operations", "Staffing", "Compliance"]
    scores = [financial, operations, staffing, compliance]

    bundle = generate_bundle(diagnoses)

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
        "root_html": diagnosis_html(diagnoses),
        "labels": json.dumps(labels),
        "scores": json.dumps(scores),
        "bundle": bundle
    }

    return templates.TemplateResponse("operating_report.html", context)
