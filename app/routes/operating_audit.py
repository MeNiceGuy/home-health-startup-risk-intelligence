from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
import json

router = APIRouter(prefix="/operating-audit", tags=["Operating Intelligence"])

def risk_score(value, benchmark, higher_is_bad=True):
    value = float(value or 0)
    benchmark = float(benchmark or 1)
    ratio = value / benchmark if higher_is_bad else benchmark / value if value else 2
    if ratio <= 1: return 90
    if ratio <= 1.25: return 75
    if ratio <= 1.5: return 60
    return 35

def field(label, name, value, tip):
    return f"""
    <div class="field">
      <label>{label}</label>
      <input name="{name}" value="{value}">
      <div class="tip">{tip}</div>
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
    label{{font-weight:bold;display:block;margin-bottom:6px;}}
    input{{width:100%;padding:12px;border:1px solid #cbd5e1;border-radius:10px;font-size:15px;}}
    .tip{{margin-top:8px;background:#eff6ff;color:#1e3a8a;padding:12px;border-radius:10px;font-size:14px;line-height:1.4;}}
    button{{background:#2563eb;color:white;padding:15px 22px;border:0;border-radius:10px;font-weight:bold;font-size:16px;}}
    @media(max-width:800px){{.grid{{grid-template-columns:1fr}}}}
    </style>
    </head>
    <body>
    <div class="hero">
      <h1>Operating Intelligence Audit</h1>
      <p>Measure financial, staffing, compliance, and operational bottlenecks against benchmark targets.</p>
    </div>

    <div class="wrap">
    <form method="post" action="/operating-audit/run">

    <div class="card"><h2>Financial Performance</h2><div class="grid">
    {field("Days in A/R", "ar_days", "45", "Average days it takes to collect payment after billing. Lower is better. Benchmark target: 30 days.")}
    {field("Claim Denial Rate (%)", "denial_rate", "15", "Percent of claims denied by payers. High denial rates create revenue leakage. Benchmark target: 10% or lower.")}
    {field("Clean Claim Rate (%)", "clean_rate", "80", "Percent of claims accepted without correction. Higher is better. Benchmark target: 90% or higher.")}
    </div></div>

    <div class="card"><h2>Operational Efficiency</h2><div class="grid">
    {field("Intake Completion Time (days)", "intake_time", "5", "How long it takes from referral/client inquiry to completed intake. Benchmark target: 2 days.")}
    {field("Documentation Lag (days)", "doc_lag", "3", "Average delay between service delivery and completed documentation. Benchmark target: 1 day or less.")}
    {field("Missed Visit Rate (%)", "missed_visits", "8", "Percent of scheduled visits missed or not completed. Benchmark target: 5% or lower.")}
    </div></div>

    <div class="card"><h2>Staffing Capacity</h2><div class="grid">
    {field("Open Roles", "open_roles", "3", "Current unfilled positions affecting service capacity. Benchmark target: 1 or fewer critical openings.")}
    {field("Turnover Rate (%)", "turnover", "40", "Percent of staff leaving over a year. High turnover creates training, scheduling, and quality risk. Benchmark target: 30% or lower.")}
    </div></div>

    <div class="card"><h2>Compliance Readiness</h2><div class="grid">
    {field("QA Audit Score (%)", "qa_score", "75", "Internal audit score for documentation, care records, policy compliance, and quality checks. Benchmark target: 90% or higher.")}
    {field("HIPAA Compliance Score (%)", "hipaa_score", "85", "Estimated readiness for privacy, security, access controls, and records protection. Benchmark target: 95% or higher.")}
    </div></div>

    <button type="submit">Run Predictive Intelligence</button>
    </form>
    </div>
    </body>
    </html>
    """

@router.post("/run", response_class=HTMLResponse)
def run(
    ar_days: float = Form(0), denial_rate: float = Form(0), clean_rate: float = Form(0),
    intake_time: float = Form(0), doc_lag: float = Form(0), missed_visits: float = Form(0),
    open_roles: float = Form(0), turnover: float = Form(0),
    qa_score: float = Form(0), hipaa_score: float = Form(0)
):
    financial = int((risk_score(ar_days,30) + risk_score(denial_rate,10) + risk_score(clean_rate,90,False)) / 3)
    operations = int((risk_score(intake_time,2) + risk_score(doc_lag,1) + risk_score(missed_visits,5)) / 3)
    staffing = int((risk_score(open_roles,1) + risk_score(turnover,30)) / 2)
    compliance = int((risk_score(qa_score,90,False) + risk_score(hipaa_score,95,False)) / 2)
    total = int((financial + operations + staffing + compliance) / 4)

    lost_revenue = int((denial_rate - 10) * 1000) if denial_rate > 10 else 0
    delay_cost = int((ar_days - 30) * 500) if ar_days > 30 else 0
    total_impact = lost_revenue + delay_cost

    labels = ["A/R Days","Denial Rate","Clean Claim Rate","Intake Time","Doc Lag","Missed Visits","Open Roles","Turnover","QA Score","HIPAA Score"]
    current = [ar_days,denial_rate,clean_rate,intake_time,doc_lag,missed_visits,open_roles,turnover,qa_score,hipaa_score]
    benchmark = [30,10,90,2,1,5,1,30,90,95]
    score_labels = ["Financial","Operations","Staffing","Compliance"]
    score_values = [financial,operations,staffing,compliance]

    actions = sorted([
      ("Financial", financial, lost_revenue, "Reduce denials, improve clean claims, and shorten A/R."),
      ("Operations", operations, delay_cost, "Improve intake speed, documentation turnaround, and missed visit control."),
      ("Staffing", staffing, 1500 if staffing < 80 else 0, "Strengthen hiring pipeline, coverage, and retention."),
      ("Compliance", compliance, 2000 if compliance < 80 else 0, "Improve QA audits, HIPAA readiness, and survey preparedness.")
    ], key=lambda x: x[1])

    roadmap = "".join([f"<div class='road'><h3>Week {i+1}: {a[0]}</h3><p>{a[3]}</p><p><strong>Estimated impact:</strong> ${a[2]}</p></div>" for i,a in enumerate(actions)])

    return f"""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
    body{{margin:0;font-family:Arial;background:#f8fafc;color:#0f172a;}}
    .hero{{background:linear-gradient(135deg,#0f172a,#1e3a8a);color:white;padding:50px 24px;}}
    .wrap{{max-width:1150px;margin:-30px auto 40px;padding:20px;}}
    .card{{background:white;padding:24px;border-radius:18px;margin-bottom:20px;box-shadow:0 12px 32px rgba(15,23,42,.12);}}
    .metrics{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;}}
    .metric{{font-size:34px;font-weight:bold;}}
    .grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px;}}
    .danger{{border-left:6px solid #dc2626;background:#fee2e2;color:#7f1d1d;}}
    .road{{background:#f1f5f9;padding:16px;border-radius:14px;margin-bottom:12px;}}
    canvas{{max-width:100%;min-height:300px;}}
    @media(max-width:900px){{.metrics,.grid{{grid-template-columns:1fr;}}}}
    </style>
    </head>
    <body>
    <div class="hero"><h1>Predictive Operating Intelligence Report</h1><p>Score: {total}/100</p></div>
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

    <div class="grid">
      <div class="card"><h2>Client Performance vs Benchmark</h2><p>Shows where the agency is above or below target operating standards.</p><canvas id="benchmarkChart"></canvas></div>
      <div class="card"><h2>Score Breakdown</h2><p>Shows which business area is creating the biggest bottleneck.</p><canvas id="scoreChart"></canvas></div>
    </div>

    <div class="card"><h2>Risk Radar</h2><p>Shows whether risk is balanced or concentrated in one business function.</p><canvas id="radarChart"></canvas></div>

    <div class="card"><h2>30-Day Dynamic Execution Roadmap</h2>{roadmap}</div>

    </div>

    <script>
    const labels = {json.dumps(labels)};
    const current = {json.dumps(current)};
    const benchmark = {json.dumps(benchmark)};
    const scoreLabels = {json.dumps(score_labels)};
    const scoreValues = {json.dumps(score_values)};

    new Chart(document.getElementById("benchmarkChart"), {{
      type:"bar",
      data:{{labels:labels,datasets:[{{label:"Client Current",data:current}},{{label:"Benchmark Target",data:benchmark}}]}},
      options:{{responsive:true, maintainAspectRatio:false}}
    }});

    new Chart(document.getElementById("scoreChart"), {{
      type:"bar",
      data:{{labels:scoreLabels,datasets:[{{label:"Score",data:scoreValues}}]}},
      options:{{responsive:true, maintainAspectRatio:false, scales:{{y:{{min:0,max:100}}}}}}
    }});

    new Chart(document.getElementById("radarChart"), {{
      type:"radar",
      data:{{labels:scoreLabels,datasets:[{{label:"Operating Health",data:scoreValues}}]}},
      options:{{responsive:true, maintainAspectRatio:false, scales:{{r:{{min:0,max:100}}}}}}
    }});
    </script>
    </body>
    </html>
    """
