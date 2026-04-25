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

    labels = [str(row[7])[:10] for row in reversed(scores)]
    total_scores = [row[2] for row in reversed(scores)]

    return f"""
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body style="font-family:Arial;background:#f8fafc;padding:16px;margin:0;">
        <style>
.card{background:white;padding:20px;border-radius:14px;margin-bottom:20px;box-shadow:0 6px 18px rgba(0,0,0,.06);}
.nav a{display:inline-block;margin:6px 6px 6px 0;padding:12px 14px;background:#2563eb;color:white;text-decoration:none;border-radius:10px;}
canvas{max-width:100%;}
@media(max-width:700px){
h1{font-size:26px;line-height:1.2;}
h2{font-size:21px;}
.card{padding:16px;}
.nav a{display:block;width:100%;box-sizing:border-box;text-align:center;}
}
</style><h1>Boswell Consulting Group Intelligence Dashboard</h1>

        <div class="card">
            <h2>AI Trend Analysis</h2>
            <p style="white-space:pre-line;">{ai_insight}</p>
        </div>

        <div class="card">
            <h2>Total Score Trend</h2>
            <canvas id="chart"></canvas>
        </div>

        <a href="/operating-audit/">Run Operating Audit</a><br><br>
        <a href="/audit/">Run Startup Audit</a><br><br>
        <a href="/kits/">View Kits</a>

        <script>
        new Chart(document.getElementById("chart"), {{
            type: "line",
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: "Total Score",
                    data: {json.dumps(total_scores)},
                    borderWidth: 3
                }}]
            }},
            options: {{
                scales: {{
                    y: {{ min: 0, max: 100 }}
                }}
            }}
        }});
        </script>
    </body>
    </html>
    """
