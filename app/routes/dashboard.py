from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.services.saas_tracking import get_dashboard_data
from app.services.trend_ai import generate_trend_insights
import json

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/", response_class=HTMLResponse)
def dashboard():
    subs, scores = get_dashboard_data()

    ai_insight = generate_trend_insights(scores)

    labels = [row[7][:10] for row in reversed(scores)]
    total_scores = [row[2] for row in reversed(scores)]
    compliance_scores = [row[3] for row in reversed(scores)]
    clinical_scores = [row[4] for row in reversed(scores)]
    revenue_scores = [row[5] for row in reversed(scores)]
    operations_scores = [row[6] for row in reversed(scores)]

    sub_rows = "".join([
        f"<tr><td>{email}</td><td>{status}</td><td>{date}</td></tr>"
        for email, status, date in subs
    ])

    score_rows = "".join([
        f"<tr><td>{agency}</td><td>{audit}</td><td>{total}/100</td><td>{comp}%</td><td>{clinical}%</td><td>{rev}%</td><td>{ops}%</td><td>{date}</td></tr>"
        for agency, audit, total, comp, clinical, rev, ops, date in scores
    ])

    return f"""
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body style="font-family:Arial;background:#f8fafc;padding:40px;">
        <h1>Boswell Consulting Group Intelligence Dashboard</h1>

        <div style="background:white;padding:25px;border-radius:14px;margin-bottom:25px;">
            <h2>AI Trend Analysis</h2>
            <p style="white-space:pre-line;">{ai_insight}</p>
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:25px;">
            <div style="background:white;padding:25px;border-radius:14px;">
                <h2>Total Score Trend</h2>
                <canvas id="totalChart"></canvas>
            </div>

            <div style="background:white;padding:25px;border-radius:14px;">
                <h2>Category Score Breakdown</h2>
                <canvas id="categoryChart"></canvas>
            </div>
        </div>

        <div style="background:white;padding:25px;border-radius:14px;margin-top:25px;">
            <h2>Subscription Tracking</h2>
            <table border="1" cellpadding="10" style="border-collapse:collapse;width:100%;">
                <tr><th>Email</th><th>Status</th><th>Created</th></tr>
                {sub_rows}
            </table>
        </div>

        <div style="background:white;padding:25px;border-radius:14px;margin-top:25px;">
            <h2>Intelligence Score History</h2>
            <table border="1" cellpadding="10" style="border-collapse:collapse;width:100%;">
                <tr>
                    <th>Agency</th><th>Audit Type</th><th>Total</th><th>Compliance</th>
                    <th>Clinical</th><th>Revenue</th><th>Operations</th><th>Date</th>
                </tr>
                {score_rows}
            </table>
        </div>

        <br>
        <a href="/operating-audit/">Run Operating Audit</a><br><br>
        <a href="/audit/">Run Startup Audit</a><br><br>
        <a href="/kits/">View Kits</a>

        <script>
            const labels = {json.dumps(labels)};
            const totalScores = {json.dumps(total_scores)};
            const complianceScores = {json.dumps(compliance_scores)};
            const clinicalScores = {json.dumps(clinical_scores)};
            const revenueScores = {json.dumps(revenue_scores)};
            const operationsScores = {json.dumps(operations_scores)};

            new Chart(document.getElementById("totalChart"), {{
                type: "line",
                data: {{
                    labels: labels,
                    datasets: [{{
                        label: "Total Score",
                        data: totalScores,
                        borderWidth: 3,
                        tension: 0.3
                    }}]
                }},
                options: {{
                    scales: {{
                        y: {{
                            min: 0,
                            max: 100
                        }}
                    }}
                }}
            }});

            new Chart(document.getElementById("categoryChart"), {{
                type: "bar",
                data: {{
                    labels: labels,
                    datasets: [
                        {{ label: "Compliance", data: complianceScores }},
                        {{ label: "Clinical", data: clinicalScores }},
                        {{ label: "Revenue", data: revenueScores }},
                        {{ label: "Operations", data: operationsScores }}
                    ]
                }},
                options: {{
                    scales: {{
                        y: {{
                            min: 0,
                            max: 100
                        }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """
