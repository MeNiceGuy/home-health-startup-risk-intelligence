from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.services.benchmark_audit import audit_from_inputs

router = APIRouter()

def build_timeline(findings):
    ordered = sorted(
        [f for f in findings if isinstance(f, dict)],
        key=lambda x: x.get("estimated_impact", 0),
        reverse=True
    )

    weeks = [
        ("Week 1", "Stabilize the highest revenue leakage area."),
        ("Week 2", "Implement workflow controls and accountability checks."),
        ("Week 3", "Strengthen staffing, compliance, and documentation processes."),
        ("Week 4", "Review results, monitor KPIs, and adjust operating cadence.")
    ]

    html = ""
    for i, item in enumerate(weeks):
        focus = ordered[i]["label"] if i < len(ordered) else "Performance Monitoring"
        html += f"<li><strong>{item[0]}:</strong> {focus} — {item[1]}</li>"

    return html

def build_expected_outcomes(findings):
    outcomes = []

    keys = [f.get("key") for f in findings if isinstance(f, dict)]

    if "denial_rate" in keys or "ar_days" in keys:
        outcomes.append("Improved revenue-cycle discipline and reduced preventable cash-flow leakage.")
    if "intake_time" in keys or "missed_visits" in keys:
        outcomes.append("Faster intake execution, fewer missed visits, and stronger operational control.")
    if "staff_turnover" in keys:
        outcomes.append("Better staffing stability, coverage reliability, and reduced continuity risk.")
    if "compliance_findings" in keys:
        outcomes.append("Improved compliance readiness and stronger internal audit discipline.")

    if not outcomes:
        outcomes.append("Maintain benchmark performance through ongoing monitoring.")

    return "".join([f"<li>{o}</li>" for o in outcomes])

@router.get("/operating-audit/", response_class=HTMLResponse)
async def operating_audit(request: Request):
    token = request.query_params.get("access", "")
    dev = request.query_params.get("dev", "")

    if token != "paid-audit" and dev != "1":
        return HTMLResponse("""
        <html>
        <body style='font-family:Arial;background:#f8fafc;padding:40px;'>
        <div style='max-width:700px;margin:auto;background:white;padding:35px;border-radius:18px;box-shadow:0 10px 30px rgba(0,0,0,.08);'>
            <h1>Full Audit Locked</h1>
            <p>The full performance audit requires payment to access.</p>
            <a href='/pricing' style='display:inline-block;background:#dc2626;color:white;padding:14px 22px;border-radius:12px;text-decoration:none;font-weight:bold;'>
                View Pricing
            </a>
        </div>
        </body>
        </html>
        """)
    params = request.query_params

    inputs = {
        "denial_rate": params.get("denial_rate", 18),
        "ar_days": params.get("ar_days", 48),
        "intake_time": params.get("intake_time", 5),
        "missed_visits": params.get("missed_visits", 9),
        "staff_turnover": params.get("staff_turnover", 32),
        "compliance_findings": params.get("compliance_findings", 4),
        "agency_name": params.get("agency") or "",
        "state": params.get("state") or "",
        "lead_id": params.get("lead_id") or "",
        "email": params.get("email") or ""
    }

    audit = audit_from_inputs(inputs)

    if inputs.get("lead_id"):
        from app.services.lead_tracking import log_lead_event
        log_lead_event(inputs.get("lead_id"), inputs.get("agency_name"), inputs.get("email"), "full_audit_clicked")
    findings = [f for f in audit.get("findings", []) if isinstance(f, dict)]

    recommended = ",".join(audit.get("recommended_kits", []))
    timeline_html = build_timeline(findings)
    outcomes_html = build_expected_outcomes(findings)

    category_cards = ""
    bars = ""
    for category, score in audit.get("categories", {}).items():
        color = "#16a34a" if score >= 85 else "#f59e0b" if score >= 70 else "#dc2626"
        category_cards += f"<div class='card'><p>{category}</p><h2 style='color:{color};'>{score}%</h2></div>"
        bars += f"<div class='bar-row'><span>{category}</span><div class='bar-bg'><div class='bar-fill' style='width:{score}%;background:{color};'></div></div><strong>{score}%</strong></div>"

    top_leaks = ""
    for f in sorted(findings, key=lambda x: x.get("estimated_impact", 0), reverse=True)[:3]:
        top_leaks += f"<div class='finding'><strong>{f['label']}</strong>: ${f.get('estimated_impact',0):,}/month</div>"

    findings_html = ""
    for f in findings:
        color = "#16a34a" if f["score"] >= 85 else "#f59e0b" if f["score"] >= 70 else "#dc2626"
        gap = "At or below benchmark" if f["gap"] <= 0 else f"+{f['gap']} {f['unit']} above benchmark"

        findings_html += f"""
        <div class='finding'>
            <h3>{f['label']} <span style='color:{color};'>({f['risk']})</span></h3>
            <p><strong>Your Input:</strong> {f['value']} {f['unit']} | <strong>Benchmark:</strong> {f['benchmark']} {f['unit']}</p>
            <p><strong>Gap:</strong> {gap}</p>
            <p><strong>Estimated Monthly Impact:</strong> ${f.get('estimated_impact',0):,}</p>
            <p><strong>Why this matters:</strong> {f['why']}</p>
        </div>
        """

    cms = audit.get("cms_data", {})
    agency_profile = audit.get("agency_cms_profile", {})
    agency_html = f"<p>{agency_profile.get('message', 'No CMS agency match found.')}</p>"

    if agency_profile.get("matched"):
        rows = ""
        for k, v in list(agency_profile.get("profile", {}).items())[:10]:
            rows += f"<tr><td><strong>{k}</strong></td><td>{v}</td></tr>"
        agency_html = f"<table>{rows}</table>"

    return f"""
    <html>
    <head>
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
        li{{margin-bottom:10px;line-height:1.5;}}
    </style>
    </head>
    <body>
    <div class='wrap'>

        <div class='hero'>
{("<div style='background:#dcfce7;color:#166534;padding:14px;border-radius:12px;margin-bottom:18px;font-weight:bold;'>Executive PDF emailed successfully.</div>" if params.get("sent") == "1" else "")}
            <h1>Home Health Performance Audit</h1>
            <p>Benchmark-driven operational, staffing, compliance, and revenue cycle analysis.</p>
            <p><strong>Total Score:</strong> <span class='loss'>{audit.get("total_score")}%</span></p>
            <p><strong>Performance Tier:</strong> {audit.get("tier","N/A")}</p>
            <p><strong>Confidence / Data Quality:</strong> {audit.get("confidence")} ({audit.get("data_quality")}% data quality)</p>
            <p><strong>Estimated Monthly Impact:</strong> <span class='loss'>${audit.get("total_estimated_impact",0):,}</span></p>
            <a class='cta' href='/kits?recommended={recommended}'>View Recommended Fix Systems</a>

<form method='get' action='/send/audit-pdf' style='margin-top:18px;display:flex;gap:10px;flex-wrap:wrap;'>
    <input name='email' type='email' placeholder='Email this audit PDF' required style='padding:13px;border-radius:10px;border:1px solid #d1d5db;min-width:260px;'>

    <input type='hidden' name='agency' value='{inputs["agency_name"]}'>
    <input type='hidden' name='state' value='{inputs["state"]}'>
    <input type='hidden' name='denial_rate' value='{inputs["denial_rate"]}'>
    <input type='hidden' name='ar_days' value='{inputs["ar_days"]}'>
    <input type='hidden' name='intake_time' value='{inputs["intake_time"]}'>
    <input type='hidden' name='missed_visits' value='{inputs["missed_visits"]}'>
    <input type='hidden' name='staff_turnover' value='{inputs["staff_turnover"]}'>
    <input type='hidden' name='compliance_findings' value='{inputs["compliance_findings"]}'>

    <button class='cta' style='border:none;background:#111827;cursor:pointer;'>Email Executive PDF</button>
</form>
<a class='cta' style='background:#111827;margin-left:10px;' href='/download/audit-pdf?agency={inputs["agency_name"]}&state={inputs["state"]}&denial_rate={inputs["denial_rate"]}&ar_days={inputs["ar_days"]}&intake_time={inputs["intake_time"]}&missed_visits={inputs["missed_visits"]}&staff_turnover={inputs["staff_turnover"]}&compliance_findings={inputs["compliance_findings"]}&email={inputs.get("email","")}'>Download PDF + Save Report</a>
        </div>

        <div class='grid'>{category_cards}</div>

        <div class='panel'>
            <h2>Executive Summary</h2>
            <p>{audit.get("executive_summary",{}).get("narrative","This audit identifies operational and financial risks requiring structured corrective action.")}</p>
        </div>

        <div class='panel'>
            <h2>Priority Roadmap</h2>
            <ul>
                {''.join([f"<li><strong>Priority {r['priority']}:</strong> {r['focus']} — {r['action']}</li>" for r in audit.get("roadmap",[])])}
            </ul>
        </div>

        <div class='panel'>
            <h2>Implementation Timeline</h2>
            <ul>{timeline_html}</ul>
        </div>

        <div class='panel'>
            <h2>Expected Outcomes</h2>
            <p>If implemented effectively, the agency can reasonably target the following operational improvements:</p>
            <ul>{outcomes_html}</ul>
        </div>

        <div class='panel'>
            <h2>Performance Visualization</h2>
            {bars}
        </div>

        <div class='panel'>
            <h2>CMS Benchmark Comparison</h2>
            <p><strong>CMS Denial Rate Avg:</strong> {cms.get("cms_denial_avg") or "N/A"}</p>
            <p><strong>CMS A/R Days Avg:</strong> {cms.get("cms_ar_avg") or "N/A"}</p>
        </div>

        <div class='panel'>
    <h2>CMS Percentile Benchmarking</h2>
    <p>This section compares matched CMS performance fields against other CMS agencies when usable numeric fields are available.</p>
    {
        "".join([
            f"<p><strong>{k}:</strong> {v.get('value')} | Percentile: {v.get('percentile')}% | Sample: {v.get('sample_size')}</p>"
            for k, v in audit.get("cms_percentiles", {}).items()
        ]) or "<p>Percentile benchmarking unavailable for this agency match.</p>"
    }
</div>

<div class='panel'>
    <h2>Agency-Level CMS Match</h2>
            {agency_html}
        </div>

        <div class='panel' style='border:3px solid #f59e0b;background:#fff7ed;'>
    <h2>Recommended Corrective System</h2>
    <p><strong>Based on this audit, your agency should prioritize the Full Agency Optimization System.</strong></p>
    <p>
        This system is designed to address the revenue-cycle, intake, staffing, operational,
        and compliance gaps identified in this report.
    </p>
    <p><strong>Estimated Monthly Revenue at Risk:</strong> <span class='loss'>${audit.get("total_estimated_impact",0):,}</span></p>
    <p>
        If even a portion of this leakage is reduced, the implementation system can pay for itself quickly.
    </p>
    <a class='cta' style='background:#f59e0b;color:#111827;' href='/cart/add/full-optimization'>
        Get Full Agency Optimization System
    </a>
</div>

<div class='panel'>
    <h2>Top Revenue Leakage Drivers</h2>
            {top_leaks}
        </div>

        <div class='panel'>
            <h2>Operational & Financial Risk Analysis</h2>
            <p>Each finding shows the input, benchmark, gap, risk signal, and business meaning.</p>
        </div>

        {findings_html}

        <div class='panel'>
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

@router.get("/download/audit-pdf")
def download_audit_pdf(
    agency: str = "",
    state: str = "",
    denial_rate: float = 18,
    ar_days: float = 48,
    intake_time: float = 5,
    missed_visits: float = 9,
    staff_turnover: float = 32,
    compliance_findings: float = 4
):
    from fastapi.responses import FileResponse
    from app.services.pdf_engine import generate_consulting_audit_pdf

    inputs = {
        "agency_name": agency,
        "state": state,
        "denial_rate": denial_rate,
        "ar_days": ar_days,
        "intake_time": intake_time,
        "missed_visits": missed_visits,
        "staff_turnover": staff_turnover,
        "compliance_findings": compliance_findings
    }

    path = generate_consulting_audit_pdf(inputs, "audit_report.pdf")

    if email:
        from app.services.lead_tracking import log_lead_event
        lead_id = email.replace("@","_").replace(".","_")
        log_lead_event(lead_id, agency, email, "pdf_downloaded")
    return FileResponse(path, media_type="application/pdf", filename="home_health_performance_audit.pdf")


@router.get("/send/audit-pdf")
def send_audit_pdf(
    email: str,
    agency: str = "",
    state: str = "",
    denial_rate: float = 18,
    ar_days: float = 48,
    intake_time: float = 5,
    missed_visits: float = 9,
    staff_turnover: float = 32,
    compliance_findings: float = 4
):
    from fastapi.responses import RedirectResponse
    from app.services.pdf_engine import generate_consulting_audit_pdf
    from app.services.pdf_emailer import send_pdf_email

    inputs = {
        "agency_name": agency,
        "state": state,
        "denial_rate": denial_rate,
        "ar_days": ar_days,
        "intake_time": intake_time,
        "missed_visits": missed_visits,
        "staff_turnover": staff_turnover,
        "compliance_findings": compliance_findings
    }

    path = generate_consulting_audit_pdf(inputs, "audit_report.pdf")

    if email:
        from app.services.lead_tracking import log_lead_event
        lead_id = email.replace("@","_").replace(".","_")
        log_lead_event(lead_id, agency, email, "pdf_downloaded")
    send_pdf_email(email, path)

    from app.services.lead_tracking import log_lead_event
    log_lead_event(email.replace("@","_").replace(".","_"), agency, email, "pdf_requested")

    return RedirectResponse(
        f"/operating-audit/?agency={agency}&state={state}&denial_rate={denial_rate}&ar_days={ar_days}&intake_time={intake_time}&missed_visits={missed_visits}&staff_turnover={staff_turnover}&compliance_findings={compliance_findings}&sent=1",
        status_code=303
    )












