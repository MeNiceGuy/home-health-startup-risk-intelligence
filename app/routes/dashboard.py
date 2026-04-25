from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.services.saas_tracking import get_dashboard_data
from app.services.trend_ai import generate_trend_insights
from app.routes.auth import get_current_user
import json

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    user = get_current_user(request)

    if not user:
        return RedirectResponse("/auth/login")

    subs, scores = get_dashboard_data()

    ai_insight = generate_trend_insights(scores)

    labels = [str(row[7])[:10] for row in reversed(scores)]
    total_scores = [row[2] for row in reversed(scores)]

    return f"""
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body style="font-family:Arial;background:#f8fafc;padding:40px;">

        <h1>Boswell Intelligence Dashboard</h1>

        <div style="background:#fee2e2;padding:20px;border-radius:12px;margin-bottom:20px;">
            <strong>CRITICAL ALERT:</strong> Monitor clinical and compliance systems closely.
        </div>

        <div style="background:white;padding:25px;border-radius:14px;margin-bottom:25px;">
            <h2>AI Trend Analysis</h2>
            <p style="white-space:pre-line;">{ai_insight}</p>

            <h2>Recommended System Upgrade</h2>

            <a href="/ops-checkout/full-ops"
            style="background:#ef4444;color:white;padding:14px 20px;border-radius:8px;display:inline-block;margin-top:10px;">
            Fix Your Operational Gaps ($799)
            </a>

            <br><br>

            <a href="/subscribe/"
            style="background:#22c55e;color:black;padding:14px 20px;border-radius:8px;">
            Activate Monthly Intelligence Monitoring ($99/mo)
            </a>
        </div>

        <div style="background:white;padding:25px;border-radius:14px;">
            <h2>Total Score Trend</h2>
            <canvas id="chart"></canvas>
        </div>

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
