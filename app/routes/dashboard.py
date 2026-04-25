from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.services.saas_tracking import get_dashboard_data
from app.services.trend_ai import generate_trend_insights
import json

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def get_recommendations(compliance, clinical, revenue, operations):
    recs = []

    if clinical < 60:
        recs.append({
            "name": "Clinical Oversight System",
            "price": "$499",
            "link": "/ops-checkout/clinical",
            "desc": "Fix RN supervision, care delivery structure, and compliance risk."
        })

    if revenue < 60:
        recs.append({
            "name": "Revenue Intelligence System",
            "price": "$399",
            "link": "/ops-checkout/revenue",
            "desc": "Fix payer strategy, billing flow, and cash cycle delays."
        })

    if compliance < 60:
        recs.append({
            "name": "Compliance Optimization System",
            "price": "$299",
            "link": "/ops-checkout/compliance",
            "desc": "Fix policies, HIPAA exposure, and audit readiness."
        })

    if operations < 60:
        recs.append({
            "name": "Operations System Kit",
            "price": "$349",
            "link": "/ops-checkout/operations",
            "desc": "Fix intake workflow, documentation system, and execution gaps."
        })

    if not recs:
        recs.append({
            "name": "Scale Optimization System",
            "price": "$599",
            "link": "/ops-checkout/scale",
            "desc": "Optimize scaling, hiring, and performance systems."
        })

    return recs

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

    recs = get_recommendations(compliance, clinical, revenue, operations)

    labels = [str(row[7])[:10] for row in reversed(scores)]
    total_scores = [row[2] for row in reversed(scores)]

    rec_html = "".join([
        f"""
        <div class="rec">
            <h3>{r['name']} ({r['price']})</h3>
            <p>{r['desc']}</p>
            <a href="{r['link']}">Fix This</a>
        </div>
        """ for r in recs
    ])

    return f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{margin:0;font-family:Arial;background:#f8fafc;padding:20px;}}
            .card {{background:white;padding:20px;border-radius:14px;margin-bottom:20px;}}
            .grid {{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;}}
            .rec {{background:#f1f5f9;padding:16px;border-radius:12px;margin-bottom:12px;}}
            .rec a {{display:inline-block;margin-top:10px;background:#2563eb;color:white;padding:10px;border-radius:8px;text-decoration:none;}}
            @media(max-width:800px){{.grid{{grid-template-columns:1fr;}}}}
        </style>
    </head>

    <body>

        <h1>Intelligence Dashboard</h1>

        <div class="grid">
            <div class="card">Total: {total}</div>
            <div class="card">Compliance: {compliance}</div>
            <div class="card">Clinical: {clinical}</div>
            <div class="card">Revenue: {revenue}</div>
            <div class="card">Operations: {operations}</div>
        </div>

        <div class="card">
            <h2>AI Insight</h2>
            <p style="white-space:pre-line;">{ai_insight}</p>
        </div>

        <div class="card">
            <h2>Recommended Fixes</h2>
            {rec_html}
        </div>

        <div class="card">
            <h2>Trend</h2>
            <canvas id="chart"></canvas>
        </div>

        <script>
        new Chart(document.getElementById("chart"), {{
            type: "line",
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: "Score",
                    data: {json.dumps(total_scores)},
                    borderWidth: 2
                }}]
            }}
        }});
        </script>

    </body>
    </html>
    """
