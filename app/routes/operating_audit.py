from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
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

def yes_no_bad(value):
    return str(value or "").strip().lower() in ["no", "none", "manual", "unknown", "not sure", ""]

def root_cause_diagnosis(data):
    diagnoses = []

    if float(data["denial_rate"]) > 10:
        diagnoses.append(("Revenue Cycle", "High denial rate", "Likely caused by weak billing review, incomplete documentation, payer rule errors, or no denial tracking process."))

    if yes_no_bad(data["billing_process"]):
        diagnoses.append(("Revenue Cycle", "No defined billing workflow", "Billing is likely dependent on memory or individual effort instead of a repeatable process."))

    if data["billing_owner"].lower() in ["owner", "none", "unknown"]:
        diagnoses.append(("Administration", "Billing ownership risk", "The owner or unclear ownership may create bottlenecks, delayed follow-up, and weak accountability."))

    if float(data["intake_time"]) > 2:
        diagnoses.append(("Operations", "Slow intake process", "Client onboarding is likely delayed by unclear referral handling, missing intake checklist, or manual coordination."))

    if data["schedule_system"].lower() in ["none", "manual", "paper"]:
        diagnoses.append(("Operations", "Scheduling system weakness", "Manual scheduling increases missed visits, communication gaps, and scaling limitations."))

    if float(data["missed_visits"]) > 5:
        diagnoses.append(("Operations", "Missed visit risk", "Likely caused by staffing shortages, weak backup coverage, poor scheduling controls, or lack of real-time monitoring."))

    if yes_no_bad(data["doc_same_day"]):
        diagnoses.append(("Documentation", "Documentation lag risk", "Delayed documentation can slow billing, weaken compliance, and reduce audit readiness."))

    if float(data["open_roles"]) > 1:
        diagnoses.append(("Staffing", "Capacity gap", "Open roles may limit growth, increase missed visits, and place pressure on current staff."))

    if float(data["turnover"]) > 30:
        diagnoses.append(("Staffing", "High turnover risk", "Turnover may indicate weak onboarding, poor retention systems, compensation pressure, or scheduling strain."))

    if yes_no_bad(data["hiring_process"]):
        diagnoses.append(("Staffing", "No repeatable hiring pipeline", "Growth will be limited because recruiting, screening, onboarding, and training are not systemized."))

    if yes_no_bad(data["backup_staff"]):
        diagnoses.append(("Staffing", "No backup coverage", "Call-outs can immediately become missed visits, client dissatisfaction, and compliance exposure."))

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
        html += f"""
        <div class="diag">
            <h3>{area}: {issue}</h3>
            <p>{cause}</p>
        </div>
        """
    return html

def field(label, name, value, tip):
    return f"""
    <div class="field">
      <label>{label} <span class="info">ⓘ</span></label>
      <input name="{name}" value="{value}">
      <div class="tooltip">{tip}</div>
    </div>
    """

@router.get("/", response_class=HTMLResponse)
def form():
    return f"""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    body{{margin:0;font-family:Arial;background:#f8fafc;color:#0f172a;}}
    .hero{{background:linear-gradient(135deg,#0f172a,#1e3a8a);color:white;padding:55px 24px;text-align:center;}}
    .wrap{{max-width:1100px;margin:-30px auto 40px;padding:20px;}}
    .card{{background:white;padding:26px;border-radius:18px;box-shadow:0 12px 32px rgba(15,23,42,.12);margin-bottom:20px;}}
    .grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px;}}
    .field{{position:relative;}}
    label{{font-weight:bold;display:block;margin-bottom:6px;}}
    input{{width:100%;padding:12px;border:1px solid #cbd5e1;border-radius:10px;font-size:15px;}}
    .info{{color:#2563eb;cursor:pointer;}}
    .tooltip{{display:none;position:absolute;background:#0f172a;color:white;padding:12px;border-radius:10px;font-size:13px;top:64px;z-index:99;width:290px;line-height:1.4;box-shadow:0 10px 25px rgba(0,0,0,.25);}}
    .field:hover .tooltip{{display:block;}}
    button{{background:#2563eb;color:white;padding:15px 22px;border:0;border-radius:10px;font-weight:bold;font-size:16px;}}
    @media(max-width:800px){{.grid{{grid-template-columns:1fr}}.tooltip{{position:static;display:block;margin-top:8px;width:auto;}}}}
    </style>
    </head>
    <body>
    <div class="hero">
      <h1>Operating Intelligence Audit</h1>
      <p>Find root causes behind revenue leakage, compliance risk, staffing gaps, and scaling bottlenecks.</p>
    </div>

    <div class="wrap">
    <form method="post" action="/operating-audit/run">

    <div class="card"><h2>Revenue Cycle Intelligence</h2><div class="grid">
    {field("Days in A/R", "ar_days", "45", "Average days to collect payment after billing. Target: under 30 days.")}
    {field("Denial Rate (%)", "denial_rate", "15", "Percent of claims denied. Target: 10% or lower.")}
    {field("Billing Process Defined?", "billing_process", "No", "Example: written process for coding, claim submission, denial follow-up, and payment posting.")}
    {field("Who Handles Billing?", "billing_owner", "Owner", "Example: owner, biller, outsourced billing company, office manager.")}
    </div></div>

    <div class="card"><h2>Operations Intelligence</h2><div class="grid">
    {field("Intake Time (days)", "intake_time", "5", "Time from referral/client inquiry to completed intake. Target: 1–2 days.")}
    {field("Scheduling System Used?", "schedule_system", "Manual", "Example: EMR scheduling, spreadsheet, paper calendar, or no system.")}
    {field("Missed Visits (%)", "missed_visits", "8", "Percent of scheduled visits missed or not completed. Target: 5% or lower.")}
    {field("Documentation Completed Same Day?", "doc_same_day", "No", "Same-day notes reduce billing delays and audit exposure.")}
    </div></div>

    <div class="card"><h2>Staffing Intelligence</h2><div class="grid">
    {field("Open Roles", "open_roles", "3", "Current unfilled positions affecting operations or growth.")}
    {field("Turnover Rate (%)", "turnover", "40", "Percent of staff leaving annually. Target: 30% or lower.")}
    {field("Hiring Process Defined?", "hiring_process", "No", "Example: recruiting source, screening, background checks, onboarding, training.")}
    {field("Backup Coverage Available?", "backup_staff", "No", "Do you have backup staff for call-outs, emergencies, or schedule gaps?")}
    </div></div>

    <div class="card"><h2>Compliance Intelligence</h2><div class="grid">
    {field("QA Audit Score (%)", "qa_score", "75", "Internal audit score for documentation, care records, policy compliance, and quality checks. Target: 90%+.")}
    {field("Policies Updated?", "policies_updated", "No", "Are policies current for HIPAA, patient rights, infection control, incident reporting, and operations?")}
    {field("Incident Tracking System?", "incident_tracking", "No", "Do you formally track complaints, incidents, missed visits, errors, and corrective actions?")}
    {field("HIPAA Compliance Score (%)", "hipaa_score", "85", "Readiness for privacy, security, access control, breach response, and record protection. Target: 95%+.")}
    </div></div>

    <button type="submit">Run Root-Cause Intelligence Audit</button>
    </form>
    </div>
    </body>
    </html>
    """

@router.post("/run", response_class=HTMLResponse)
def run(
    ar_days: float = Form(0), denial_rate: float = Form(0), clean_rate: float = Form(80),
    billing_process: str = Form("No"), billing_owner: str = Form("Owner"),
    intake_time: float = Form(0), schedule_system: str = Form("Manual"),
    missed_visits: float = Form(0), doc_same_day: str = Form("No"),
    open_roles: float = Form(0), turnover: float = Form(0),
    hiring_process: str = Form("No"), backup_staff: str = Form("No"),
    qa_score: float = Form(0), policies_updated: str = Form("No"),
    incident_tracking: str = Form("No"), hipaa_score: float = Form(0)
):
    data = locals()
    diagnoses = root_cause_diagnosis(data)

    financial = int((risk_score(ar_days,30) + risk_score(denial_rate,10) + risk_score(clean_rate,90,False)) / 3)
    operations = int((risk_score(intake_time,2) + risk_score(missed_visits,5)) / 2)
    staffing = int((risk_score(open_roles,1) + risk_score(turnover,30)) / 2)
    compliance = int((risk_score(qa_score,90,False) + risk_score(hipaa_score,95,False)) / 2)
    total = int((financial + operations + staffing + compliance) / 4)

    lost_revenue = int((denial_rate - 10) * 1000) if denial_rate > 10 else 0
    delay_cost = int((ar_days - 30) * 500) if ar_days > 30 else 0
    total_impact = lost_revenue + delay_cost

    labels = ["Financial","Operations","Staffing","Compliance"]
    scores = [financial, operations, staffing, compliance]

    root_html = diagnosis_html(diagnoses)

    return f"""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
    body{{margin:0;font-family:Arial;background:#f8fafc;color:#0f172a;}}
    .hero{{background:linear-gradient(135deg,#0f172a,#1e3a8a);color:white;padding:50px 24px;}}
    .wrap{{max-width:1150px;margin:-30px auto 40px;padding:20px;}}
    .card,.diag{{background:white;padding:24px;border-radius:18px;margin-bottom:20px;box-shadow:0 12px 32px rgba(15,23,42,.12);}}
    .metrics{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;}}
    .metric{{font-size:34px;font-weight:bold;}}
    .danger{{border-left:6px solid #dc2626;background:#fee2e2;color:#7f1d1d;}}
    .diag{{background:#f1f5f9;}}
    .chart-container{
    position:relative;
    width:100%;
    height:320px;
    max-height:320px;
}
canvas{
    width:100% !important;
    height:100% !important;
}
    @media(max-width:900px){{.metrics{{grid-template-columns:1fr;}}}}
    </style>
    </head>
    <body>
    <div class="hero"><h1>Root-Cause Operating Intelligence Report</h1><p>Total Score: {total}/100</p></div>

    <div class="wrap">
      <div class="metrics">
        <div class="card"><h3>Total</h3><div class="metric">{total}</div></div>
        <div class="card"><h3>Financial</h3><div class="metric">{financial}%</div></div>
        <div class="card"><h3>Operations</h3><div class="metric">{operations}%</div></div>
        <div class="card"><h3>Staffing</h3><div class="metric">{staffing}%</div></div>
        <div class="card"><h3>Compliance</h3><div class="metric">{compliance}%</div></div>
      </div>

      <div class="card danger">
        <h2>Estimated Financial Impact</h2>
        <p><strong>Revenue Loss from Denials:</strong> ${lost_revenue}</p>
        <p><strong>Cash Flow Delay Impact:</strong> ${delay_cost}</p>
        <p><strong>Total Estimated Impact:</strong> ${total_impact}</p>
      </div>

      <div class="card">
        <h2>Root-Cause Diagnoses</h2>
        <p>These findings explain why the bottlenecks are likely happening, not just what the score says.</p>
        {root_html}
      </div>

      <div class="card">
        <h2>Score Breakdown</h2>
        <p>This chart shows which business function is weakest and should be addressed first.</p>
        <div class="chart-container"><canvas id="scoreChart"></canvas></div>
      </div>

      <div class="card">
        <h2>Risk Radar</h2>
        <p>The radar chart shows whether risk is isolated or spread across the business.</p>
        <div class="chart-container"><canvas id="radarChart"></canvas></div>
      </div>

      <a href="/operating-audit/">Run Another Audit</a>
    </div>

    <script>
    const labels = {json.dumps(labels)};
    const scores = {json.dumps(scores)};

    new Chart(document.getElementById("scoreChart"), {{
      type:"bar",
      data:{{labels:labels,datasets:[{{label:"Operating Score",data:scores}}]}},
      options:{{responsive:true,maintainAspectRatio:true,scales:{{y:{{min:0,max:100}}}}}}
    }});

    new Chart(document.getElementById("radarChart"), {{
      type:"radar",
      data:{{labels:labels,datasets:[{{label:"Risk Profile",data:scores}}]}},
      options:{{responsive:true,maintainAspectRatio:true,scales:{{r:{{min:0,max:100}}}}}}
    }});
    </script>
    </body>
    </html>
    """
