from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
import json

router = APIRouter(prefix="/operating-audit", tags=["Operating Intelligence"])

def risk_score(value, benchmark, higher_is_bad=True):
    try:
        value = float(value)
        benchmark = float(benchmark)

        if higher_is_bad:
            ratio = value / benchmark if benchmark else 1
        else:
            ratio = benchmark / value if value else 2

        if ratio <= 1:
            return 90
        elif ratio <= 1.25:
            return 75
        elif ratio <= 1.5:
            return 60
        return 35
    except:
        return 40

@router.get("/", response_class=HTMLResponse)
def form():
    return """
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    body{margin:0;font-family:Arial;background:#f8fafc;color:#0f172a;}
    .hero{background:linear-gradient(135deg,#0f172a,#1e3a8a);color:white;padding:55px 24px;text-align:center;}
    .wrap{max-width:1050px;margin:-30px auto 40px;padding:20px;}
    .card{background:white;padding:26px;border-radius:18px;box-shadow:0 12px 32px rgba(15,23,42,.12);margin-bottom:20px;}
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
    label{font-weight:bold;display:block;margin-bottom:6px;}
    input{width:100%;padding:12px;border:1px solid #cbd5e1;border-radius:10px;}
    button{background:#2563eb;color:white;padding:15px 22px;border:0;border-radius:10px;font-weight:bold;}
    @media(max-width:800px){.grid{grid-template-columns:1fr}.hero h1{font-size:30px}}
    </style>
    </head>
    <body>
    <div class="hero">
      <h1>Operating Intelligence Audit</h1>
      <p>Quantify financial, staffing, compliance, and operational bottlenecks.</p>
    </div>

    <div class="wrap">
    <form method="post" action="/operating-audit/run">

    <div class="card">
    <h2>Financial Performance</h2>
    <div class="grid">
      <div><label>Days in A/R</label><input name="ar_days" value="45"></div>
      <div><label>Denial Rate (%)</label><input name="denial_rate" value="15"></div>
      <div><label>Clean Claim Rate (%)</label><input name="clean_rate" value="80"></div>
    </div>
    </div>

    <div class="card">
    <h2>Operations</h2>
    <div class="grid">
      <div><label>Intake Time (days)</label><input name="intake_time" value="5"></div>
      <div><label>Documentation Lag (days)</label><input name="doc_lag" value="3"></div>
      <div><label>Missed Visits (%)</label><input name="missed_visits" value="8"></div>
    </div>
    </div>

    <div class="card">
    <h2>Staffing</h2>
    <div class="grid">
      <div><label>Open Roles</label><input name="open_roles" value="3"></div>
      <div><label>Turnover Rate (%)</label><input name="turnover" value="40"></div>
    </div>
    </div>

    <div class="card">
    <h2>Compliance</h2>
    <div class="grid">
      <div><label>QA Audit Score (%)</label><input name="qa_score" value="75"></div>
      <div><label>HIPAA Score (%)</label><input name="hipaa_score" value="85"></div>
    </div>
    </div>

    <button type="submit">Run Predictive Intelligence</button>
    </form>
    </div>
    </body>
    </html>
    """

@router.post("/run", response_class=HTMLResponse)
def run(
    ar_days: float = Form(0),
    denial_rate: float = Form(0),
    clean_rate: float = Form(0),
    intake_time: float = Form(0),
    doc_lag: float = Form(0),
    missed_visits: float = Form(0),
    open_roles: float = Form(0),
    turnover: float = Form(0),
    qa_score: float = Form(0),
    hipaa_score: float = Form(0)
):
    financial = int((risk_score(ar_days,30) + risk_score(denial_rate,10) + risk_score(clean_rate,90,False)) / 3)
    operations = int((risk_score(intake_time,2) + risk_score(doc_lag,1) + risk_score(missed_visits,5)) / 3)
    staffing = int((risk_score(open_roles,1) + risk_score(turnover,30)) / 2)
    compliance = int((risk_score(qa_score,90,False) + risk_score(hipaa_score,95,False)) / 2)
    total = int((financial + operations + staffing + compliance) / 4)

    lost_revenue = int((denial_rate - 10) * 1000) if denial_rate > 10 else 0
    delay_cost = int((ar_days - 30) * 500) if ar_days > 30 else 0
    total_impact = lost_revenue + delay_cost

    tier = "Strong" if total >= 80 else "Watchlist" if total >= 60 else "Critical"
    tier_color = "#16a34a" if total >= 80 else "#f59e0b" if total >= 60 else "#dc2626"

    labels = ["A/R Days","Denial Rate","Clean Claim Rate","Intake Time","Doc Lag","Missed Visits","Open Roles","Turnover","QA Score","HIPAA Score"]
    current = [ar_days, denial_rate, clean_rate, intake_time, doc_lag, missed_visits, open_roles, turnover, qa_score, hipaa_score]
    benchmark = [30,10,90,2,1,5,1,30,90,95]
    score_labels = ["Financial","Operations","Staffing","Compliance"]
    score_values = [financial, operations, staffing, compliance]

    actions = [
        ("Financial", financial, lost_revenue, "Revenue Intelligence System"),
        ("Operations", operations, delay_cost, "Operations System Kit"),
        ("Staffing", staffing, 1500 if staffing < 80 else 0, "Staffing Capacity System"),
        ("Compliance", compliance, 2000 if compliance < 80 else 0, "Compliance Optimization System")
    ]
    actions = sorted(actions, key=lambda x: x[1])

    roadmap_html = ""
    for i, (name, score, impact, system) in enumerate(actions):
        roadmap_html += f"""
        <div class="road">
            <h3>Week {i+1}: {name}</h3>
            <p><strong>Score:</strong> {score}%</p>
            <p><strong>Recommended System:</strong> {system}</p>
            <p><strong>Estimated Impact:</strong> ${impact}</p>
        </div>
        """

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
    .badge{{display:inline-block;background:{tier_color};color:white;padding:9px 14px;border-radius:999px;font-weight:bold;}}
    .grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px;}}
    .danger{{border-left:6px solid #dc2626;background:#fee2e2;color:#7f1d1d;}}
    .road{{background:#f1f5f9;padding:16px;border-radius:14px;margin-bottom:12px;}}
    .btn{{display:inline-block;background:#2563eb;color:white;text-decoration:none;padding:13px 16px;border-radius:10px;font-weight:bold;}}
    canvas{{max-width:100%;}}
    @media(max-width:900px){{.metrics,.grid{{grid-template-columns:1fr;}}.hero h1{{font-size:30px;}}}}
    </style>
    </head>

    <body>
    <div class="hero">
      <h1>Predictive Operating Intelligence Report</h1>
      <p>Status: <span class="badge">{tier}</span></p>
    </div>

    <div class="wrap">
      <div class="metrics">
        <div class="card"><h3>Total</h3><div class="metric">{total}/100</div></div>
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
        <div class="card">
          <h2>Client Performance vs Benchmark</h2>
          <p>This chart compares the client’s current performance against target benchmarks. Large gaps reveal revenue leakage, delays, or compliance exposure.</p>
          <canvas id="benchmarkChart"></canvas>
        </div>

        <div class="card">
          <h2>Score Breakdown</h2>
          <p>This shows which business function is creating the biggest bottleneck.</p>
          <canvas id="scoreChart"></canvas>
        </div>
      </div>

      <div class="card">
        <h2>Risk Radar</h2>
        <p>The radar chart gives a quick view of balance across financial, operations, staffing, and compliance performance.</p>
        <canvas id="radarChart"></canvas>
      </div>

      <div class="card">
        <h2>30-Day Dynamic Execution Roadmap</h2>
        <p>The lowest-scoring categories are prioritized first so the agency can stabilize the highest-risk areas before scaling.</p>
        {roadmap_html}
      </div>

      <div class="card">
        <h2>Recommended Next Step</h2>
        <p>Use the roadmap to correct bottlenecks, then rerun the audit to measure improvement.</p>
        <a class="btn" href="/operating-audit/">Run Another Audit</a>
      </div>
    </div>

    <script>
    new Chart(document.getElementById("benchmarkChart"), {{
        type: "bar",
        data: {{
            labels: {json.dumps(labels)},
            datasets: [
                {{label: "Client Current", data: {json.dumps(current)}}},
                {{label: "Benchmark Target", data: {json.dumps(benchmark)}}}
            ]
        }}
    }});

    new Chart(document.getElementById("scoreChart"), {{
        type: "bar",
        data: {{
            labels: {json.dumps(score_labels)},
            datasets: [{{label: "Score", data: {json.dumps(score_values)}}}]
        }},
        options: {{scales: {{y: {{min:0,max:100}}}}}}
    }});

    new Chart(document.getElementById("radarChart"), {{
        type: "radar",
        data: {{
            labels: {json.dumps(score_labels)},
            datasets: [{{label: "Operating Health", data: {json.dumps(score_values)}}}]
        }},
        options: {{scales: {{r: {{min:0,max:100}}}}}}
    }});
    </script>
    </body>
    </html>
    """
