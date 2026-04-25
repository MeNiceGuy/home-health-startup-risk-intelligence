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

    latest = scores[0] if scores else None
    total = latest[2] if latest else 0
    compliance = latest[3] if latest else 0
    clinical = latest[4] if latest else 0
    revenue = latest[5] if latest else 0
    operations = latest[6] if latest else 0

    if total >= 80:
        badge = "Strong"
        badge_color = "#16a34a"
    elif total >= 60:
        badge = "Watchlist"
        badge_color = "#f59e0b"
    else:
        badge = "Critical"
        badge_color = "#dc2626"

    labels = [str(row[7])[:10] for row in reversed(scores)]
    total_scores = [row[2] for row in reversed(scores)]

    return f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{margin:0;font-family:Arial;background:#f8fafc;color:#0f172a;}}
            .sidebar {{position:fixed;left:0;top:0;width:230px;height:100vh;background:#0f172a;color:white;padding:24px;}}
            .sidebar a {{display:block;color:#cbd5e1;text-decoration:none;margin:18px 0;}}
            .main {{margin-left:280px;padding:32px;}}
            .top {{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;}}
            .badge {{background:{badge_color};color:white;padding:10px 16px;border-radius:999px;font-weight:bold;}}
            .grid {{display:grid;grid-template-columns:repeat(5,1fr);gap:16px;margin-bottom:24px;}}
            .card {{background:white;padding:22px;border-radius:18px;box-shadow:0 8px 24px rgba(15,23,42,.08);}}
            .metric {{font-size:34px;font-weight:bold;margin-top:10px;}}
            .risk {{background:#fee2e2;color:#7f1d1d;border-left:6px solid #dc2626;}}
            .cta a {{display:inline-block;margin:8px 8px 0 0;padding:13px 16px;border-radius:10px;text-decoration:none;font-weight:bold;}}
            .red {{background:#dc2626;color:white;}}
            .green {{background:#22c55e;color:#052e16;}}
            .blue {{background:#2563eb;color:white;}}
            canvas {{max-width:100%;}}
            @media(max-width:900px) {{
                .sidebar {{position:relative;width:auto;height:auto;}}
                .main {{margin-left:0;padding:16px;}}
                .grid {{grid-template-columns:1fr;}}
                .top {{display:block;}}
            }}
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h2>Boswell Consulting Group</h2>
            <a href="/dashboard/">Dashboard</a>
            <a href="/operating-audit/">Operating Audit</a>
            <a href="/audit/">Startup Audit</a>
            <a href="/kits/">Kits</a>
        </div>

        <div class="main">
            <div class="top">
                <div>
                    <h1>Intelligence Dashboard</h1>
                    <p>Operational risk, compliance health, and business intelligence tracking.</p>
                </div>
                <div class="badge">{badge}</div>
            </div>

            <div class="grid">
                <div class="card"><h3>Total</h3><div class="metric">{total}/100</div></div>
                <div class="card"><h3>Compliance</h3><div class="metric">{compliance}%</div></div>
                <div class="card"><h3>Clinical</h3><div class="metric">{clinical}%</div></div>
                <div class="card"><h3>Revenue</h3><div class="metric">{revenue}%</div></div>
                <div class="card"><h3>Operations</h3><div class="metric">{operations}%</div></div>
            </div>

            <div class="card risk">
                <h2>Risk Indicator</h2>
                <p><strong>Status:</strong> {badge}</p>
                <p>If scores fall below 60, prioritize clinical oversight, documentation QA, revenue tracking, and compliance review immediately.</p>
            </div>

            <div class="card">
                <h2>AI Executive Insight</h2>
                <p style="white-space:pre-line;">{ai_insight}</p>
            </div>

            <div class="card">
                <h2>Total Score Trend</h2>
                <canvas id="chart"></canvas>
            </div>

            <div class="card cta">
                <h2>Recommended Next Actions</h2>
                <a class="red" href="/ops-checkout/full-ops">Fix Operational Gaps ($799)</a>
                <a class="green" href="/subscribe/">Activate Monitoring ($99/mo)</a>
                <a class="blue" href="/operating-audit/">Run New Audit</a>
            </div>
        </div>

        <script>
        new Chart(document.getElementById("chart"), {{
            type: "line",
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: "Total Score",
                    data: {json.dumps(total_scores)},
                    borderWidth: 3,
                    tension: .35
                }}]
            }},
            options: {{
                scales: {{ y: {{ min:0, max:100 }} }}
            }}
        }});
        </script>
    </body>
    </html>
    """
