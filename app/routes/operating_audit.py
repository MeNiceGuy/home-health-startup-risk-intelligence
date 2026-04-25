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
        else:
            return 35
    except:
        return 40

@router.get("/", response_class=HTMLResponse)
def form():
    return """
    <html>
    <body style="font-family:Arial;padding:40px;background:#f8fafc;">
    <h1>Operating Intelligence Audit</h1>
    <p>Enter current performance numbers to compare against operating benchmarks.</p>

    <form method="post" action="/operating-audit/run">
    <h2>Financial</h2>
    Days in A/R: <input name="ar_days" value="45"><br><br>
    Denial Rate (%): <input name="denial_rate" value="15"><br><br>
    Clean Claim Rate (%): <input name="clean_rate" value="80"><br><br>

    <h2>Operations</h2>
    Intake Time (days): <input name="intake_time" value="5"><br><br>
    Documentation Lag (days): <input name="doc_lag" value="3"><br><br>
    Missed Visits (%): <input name="missed_visits" value="8"><br><br>

    <h2>Staffing</h2>
    Open Positions: <input name="open_roles" value="3"><br><br>
    Turnover Rate (%): <input name="turnover" value="40"><br><br>

    <h2>Compliance</h2>
    QA Audit Score (%): <input name="qa_score" value="75"><br><br>
    HIPAA Score (%): <input name="hipaa_score" value="85"><br><br>

    <button type="submit">Run Predictive Intelligence</button>
    </form>
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
    benchmarks = {
        "A/R Days": 30,
        "Denial Rate": 10,
        "Clean Claim Rate": 90,
        "Intake Time": 2,
        "Documentation Lag": 1,
        "Missed Visits": 5,
        "Open Roles": 1,
        "Turnover": 30,
        "QA Score": 90,
        "HIPAA Score": 95
    }

    current = {
        "A/R Days": ar_days,
        "Denial Rate": denial_rate,
        "Clean Claim Rate": clean_rate,
        "Intake Time": intake_time,
        "Documentation Lag": doc_lag,
        "Missed Visits": missed_visits,
        "Open Roles": open_roles,
        "Turnover": turnover,
        "QA Score": qa_score,
        "HIPAA Score": hipaa_score
    }

    financial = int((risk_score(ar_days,30) + risk_score(denial_rate,10) + risk_score(clean_rate,90,False)) / 3)
    operations = int((risk_score(intake_time,2) + risk_score(doc_lag,1) + risk_score(missed_visits,5)) / 3)
    staffing = int((risk_score(open_roles,1) + risk_score(turnover,30)) / 2)
    compliance = int((risk_score(qa_score,90,False) + risk_score(hipaa_score,95,False)) / 2)

    total = int((financial + operations + staffing + compliance) / 4)

# FINANCIAL IMPACT CALCULATIONS
lost_revenue = int((denial_rate - 10) * 1000) if denial_rate > 10 else 0
delay_cost = int((ar_days - 30) * 500) if ar_days > 30 else 0
total_impact = lost_revenue + delay_cost

    if total >= 80:
        tier = "Low Risk"
        message = "Agency appears stable, but should continue monitoring performance."
    elif total >= 60:
        tier = "Moderate Risk"
        message = "Agency shows measurable bottlenecks that may limit profitability or scale."
    else:
        tier = "High Risk"
        message = "Agency shows serious operational, financial, or compliance exposure requiring immediate correction."

    labels = list(current.keys())
    current_values = list(current.values())
    benchmark_values = list(benchmarks.values())
    score_labels = ["Financial", "Operations", "Staffing", "Compliance"]
    score_values = [financial, operations, staffing, compliance]

    return f"""
    <html>
    <head>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    body{{font-family:Arial;background:#f8fafc;margin:0;padding:24px;color:#0f172a;}}
    .grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;}}
    .card{{background:white;padding:22px;border-radius:16px;margin-bottom:20px;box-shadow:0 8px 24px rgba(15,23,42,.08);}}
    .metric{{font-size:34px;font-weight:bold;}}
    .danger{{background:#fee2e2;color:#7f1d1d;border-left:6px solid #dc2626;}}
    @media(max-width:900px){{.grid{{grid-template-columns:1fr;}}}}
    </style>
    </head>
    <body>

    <h1>Predictive Operating Intelligence Report</h1>

    <div class="grid">
        <div class="card"><h3>Total Risk Score</h3><div class="metric">{total}/100</div></div>
        <div class="card"><h3>Financial</h3><div class="metric">{financial}%</div></div>
        <div class="card"><h3>Operations</h3><div class="metric">{operations}%</div></div>
        <div class="card"><h3>Compliance</h3><div class="metric">{compliance}%</div></div>
    </div>

    <div class="card danger">
        <h2>Predictive Risk Tier: {tier}</h2>

<div class="card danger">
<h2>Estimated Financial Impact</h2>
<p><strong>Revenue Loss from Denials:</strong> ${lost_revenue}</p>
<p><strong>Cash Flow Delay Impact:</strong> ${delay_cost}</p>
<p><strong>Total Estimated Impact:</strong> ${total_impact}</p>
<p style="color:#7f1d1d;">
These inefficiencies are directly reducing available cash flow, slowing growth,
and increasing operational risk.
</p>
</div>
        <p>{message}</p>
    </div>

    <div class="card">
        <h2>Current Performance vs Benchmark</h2>
<p style="color:#475569;">
This chart compares your current performance against industry targets.
Gaps indicate operational inefficiencies, revenue leakage, or compliance exposure.
For example, higher A/R days directly delay cash flow, while high denial rates reduce revenue collected.
</p>
<p style="color:#475569;">
This chart compares your current performance against industry targets.
Gaps indicate operational inefficiencies, revenue leakage, or compliance exposure.
For example, higher A/R days directly delay cash flow, while high denial rates reduce revenue collected.
</p>
        <canvas id="benchmarkChart"></canvas>
    </div>

    <div class="card">
        <h2>Score Breakdown</h2>
        <canvas id="scoreChart"></canvas>
    </div>

    <div class="card">
        <h2>Risk Radar</h2>
        <canvas id="radarChart"></canvas>
    </div>

    <div class="card">
        <h2>Recommended Fixes</h2>
        <ul>
            <li>Financial below 80: Revenue Intelligence System</li>
            <li>Operations below 80: Operations System Kit</li>
            <li>Staffing below 80: Staffing Capacity System</li>
            <li>Compliance below 80: Compliance Optimization System</li>
        </ul>
        <a href="/dashboard/">View Dashboard</a>
    </div>

    <script>
    const labels = {json.dumps(labels)};
    const currentValues = {json.dumps(current_values)};
    const benchmarkValues = {json.dumps(benchmark_values)};
    const scoreLabels = {json.dumps(score_labels)};
    const scoreValues = {json.dumps(score_values)};

    new Chart(document.getElementById("benchmarkChart"), {{
        type: "bar",
        data: {{
            labels: labels,
            datasets: [
                {{label: "Client Current Performance", data: currentValues}},
                {{label: "Benchmark Target", data: benchmarkValues}}
            ]
        }}
    }});

    new Chart(document.getElementById("scoreChart"), {{
        type: "bar",
        data: {{
            labels: scoreLabels,
            datasets: [{{label: "Score", data: scoreValues}}]
        }},
        options: {{scales: {{y: {{min:0,max:100}}}}}}
    }});

    new Chart(document.getElementById("radarChart"), {{
        type: "radar",
        data: {{
            labels: scoreLabels,
            datasets: [{{label: "Operating Health", data: scoreValues}}]
        }},
        options: {{scales: {{r: {{min:0,max:100}}}}}}
    }});
    </script>

    </body>
    </html>
    """
