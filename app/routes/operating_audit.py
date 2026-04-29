from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.services.benchmark_audit import audit_from_inputs

router = APIRouter()

@router.get("/operating-audit/", response_class=HTMLResponse)
async def operating_audit(request: Request):
    params = request.query_params

    inputs = {
        "denial_rate": params.get("denial_rate", 18),
        "ar_days": params.get("ar_days", 48),
        "intake_time": params.get("intake_time", 5),
        "missed_visits": params.get("missed_visits", 9),
        "staff_turnover": params.get("staff_turnover", 32),
        "compliance_findings": params.get("compliance_findings", 4),
        "agency_name": params.get("agency") or "",
        "state": params.get("state") or ""
    }

    audit = audit_from_inputs(inputs)

    cards = ""
    bars = ""
    for category, score in audit["categories"].items():
        color = "#16a34a" if score >= 85 else "#f59e0b" if score >= 70 else "#dc2626"
        cards += f"<div class='card'><p>{category}</p><h2 style='color:{color};'>{score}%</h2></div>"
        bars += f"<div class='bar-row'><span>{category}</span><div class='bar-bg'><div class='bar-fill' style='width:{score}%;background:{color};'></div></div><strong>{score}%</strong></div>"

    findings = ""
    for f in audit["findings"]:
        color = "#16a34a" if f["score"] >= 85 else "#f59e0b" if f["score"] >= 70 else "#dc2626"
        gap = "At or below benchmark" if f["gap"] <= 0 else f"+{f['gap']} {f['unit']} above benchmark"
        findings += f"""
        <div class='finding'>
            <h3>{f['label']} <span style='color:{color};'>({f['risk']})</span></h3>
            <p><strong>Your Input:</strong> {f['value']} {f['unit']} | <strong>Benchmark:</strong> {f['benchmark']} {f['unit']}</p>
            <p><strong>Gap:</strong> {gap}</p>
            <p><strong>Estimated Monthly Impact:</strong> <span class="loss">${audit.get("total_estimated_impact", audit.get("estimated_loss",0)):,}</span>{f.get("estimated_impact", 0):,}</p>
            <p><strong>Why this matters:</strong> {f['why']}</p>
        </div>
        """

    cms = audit.get("cms_data", {})
    agency_profile = audit.get("agency_cms_profile", {})
    rankings = audit.get("percentile_rankings", {})

    agency_html = ""
    if agency_profile.get("matched"):
        rows = ""
        for k, v in list(agency_profile.get("profile", {}).items())[:10]:
            rows += f"<tr><td><strong>{k}</strong></td><td>{v}</td></tr>"
        agency_html = f"<table>{rows}</table>"
    else:
        agency_html = f"<p>{agency_profile.get('message', 'No agency-level CMS match found.')}</p>"

    percentile_html = ""
    if rankings:
        for metric, data in list(rankings.items())[:6]:
            percentile_html += f"<p><strong>{metric}:</strong> {data.get('percentile')} percentile | Value: {data.get('value')}</p>"
    else:
        percentile_html = "<p>Percentile ranking unavailable for this match because usable numeric CMS performance fields were not found.</p>"

    return f"""
    <html>
    <head>
    <title>Home Health Performance Audit</title>
    <style>
        body{{margin:0;font-family:Arial;background:#f3f4f6;color:#111827;}}
        .wrap{{max-width:1150px;margin:auto;padding:40px 24px;}}
        .hero,.panel,.card,.finding{{background:white;border-radius:18px;box-shadow:0 8px 24px rgba(0,0,0,.06);}}
        .hero{{padding:34px;border-left:8px solid #dc2626;}}
        .grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:28px 0;}}
        .card{{padding:22px;}}
        .panel{{padding:28px;margin-bottom:24px;}}
        .finding{{padding:22px;border-left:6px solid #dc2626;margin-bottom:16px;}}
        .loss{{font-size:34px;font-weight:900;color:#dc2626;}}
        .bar-row{{display:grid;grid-template-columns:160px 1fr 60px;gap:12px;align-items:center;margin:14px 0;}}
        .bar-bg{{background:#e5e7eb;height:16px;border-radius:999px;overflow:hidden;}}
        .bar-fill{{height:16px;}}
        .cta{{display:inline-block;background:#dc2626;color:white;padding:15px 24px;border-radius:12px;text-decoration:none;font-weight:bold;}}
        table{{width:100%;border-collapse:collapse;}} td{{padding:8px;border-bottom:1px solid #e5e7eb;}}
    </style>
    </head>
    <body>
    <div class="wrap">

        <div class="hero">
            <h1>Home Health Performance Audit</h1>
            <p>Benchmark-driven operational, staffing, compliance, and revenue cycle analysis.</p>
            <p><strong>Total Score:</strong> <span class="loss">{audit["total_score"]}%</span></p>
            <p><strong>Confidence / Data Quality:</strong> {audit["confidence"]} ({audit.get("data_quality", "N/A")}% data quality)</p>
            <p><strong>Estimated Monthly Impact:</strong> <span class="loss">${audit.get("total_estimated_impact", audit.get("estimated_loss",0)):,}</span>{audit["estimated_loss"]:,}</span></p>
            <a class="cta" href="/kits?recommended={",".join(audit.get("recommended_kits", []))}">View Recommended Fix Systems</a>
        </div>

        <div class="grid">{cards}</div>

        <div class="panel">
            <h2>Performance Visualization</h2>
            {bars}
        </div>

        <div class="panel">
            <h2>CMS Benchmark Comparison</h2>
            <p><strong>CMS Denial Rate Avg:</strong> {(cms.get("cms_denial_avg") or "N/A")}</p>
            <p><strong>CMS A/R Days Avg:</strong> {cms.get("cms_ar_avg", "N/A")}</p>
        </div>

        <div class="panel">
            <h2>Agency-Level CMS Match</h2>
            {agency_html}
        </div>

        <div class="panel">
            <h2>CMS Percentile Ranking</h2>
            {percentile_html}
        </div>

        <div class="panel">
            <h2>Top Revenue Leakage Drivers</h2>
<p>Largest sources of financial loss identified in this audit.</p></h2>
            <p>Each finding shows the input, benchmark, gap, risk signal, and business meaning.</p>
        </div>

        {
    "".join(
        sorted(
            [
                f"<div class='finding'><strong>{x.get('label','Unknown')}</strong>: ${x.get('estimated_impact',0):,}/month</div>"
                for x in audit["findings"] if isinstance(x, dict)
            ],
            key=lambda z: int(z.split("$")[1].replace(",","").split("/")[0]),
            reverse=True
        )[:3]
    )
}

<h2>Operational & Financial Risk Analysis</h2>
{findings}

        <div class="panel">
            <h2>Source Notes</h2>
            <p>This audit uses benchmark-based decision logic and can reference CMS Provider Data Catalog Home Health datasets when available.</p>

            <h2>Important Disclaimer</h2>
            <p>This audit is a decision-support tool, not a regulatory determination, legal opinion, financial guarantee, or official CMS assessment.</p>
            <p>Estimated financial impact is directional and should be validated against billing, census, claims, payroll, and compliance records before business decisions are made.</p>
        </div>

    </div>
    </body>
    </html>
    """







