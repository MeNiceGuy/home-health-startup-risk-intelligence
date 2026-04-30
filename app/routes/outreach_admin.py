from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.services.outreach_sender import load_queue, process_outreach_queue
from app.services.lead_tracking import get_lead_score, lead_status

router = APIRouter()

def lead_id_for(row):
    return row.get("lead_id") or row.get("email","").replace("@","_").replace(".","_")

@router.get("/admin/outreach", response_class=HTMLResponse)
def outreach_dashboard():
    rows = load_queue()

    enriched = []
    for r in rows:
        lid = lead_id_for(r)
        score = get_lead_score(lid)
        priority = lead_status(score)
        r["_score"] = score
        r["_priority"] = priority
        enriched.append(r)

    pending = len([r for r in enriched if r.get("status") == "pending"])
    sent = len([r for r in enriched if r.get("status") == "sent"])
    failed = len([r for r in enriched if r.get("status") == "failed"])
    hot = len([r for r in enriched if r.get("_priority") == "HOT"])

    top10 = sorted(enriched, key=lambda x: x.get("_score", 0), reverse=True)[:10]

    html = f"""
    <html>
    <body style='font-family:Arial;background:#f8fafc;padding:40px;'>
    <h1>Outreach Intelligence Dashboard</h1>

    <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-bottom:25px;'>
        <div style='background:white;padding:20px;border-radius:14px;'><h3>Pending</h3><h1>{pending}</h1></div>
        <div style='background:white;padding:20px;border-radius:14px;'><h3>Sent</h3><h1>{sent}</h1></div>
        <div style='background:white;padding:20px;border-radius:14px;'><h3>Failed</h3><h1>{failed}</h1></div>
        <div style='background:#fee2e2;padding:20px;border-radius:14px;'><h3>Hot Leads</h3><h1>{hot}</h1></div>
    </div>

    <a href='/admin/outreach/send'
       style='display:inline-block;background:#dc2626;color:white;padding:12px 18px;border-radius:10px;text-decoration:none;font-weight:bold;margin-bottom:20px;'>
       Send Pending Outreach
    </a>

    <a href='/admin/outreach/hot-followup'
       style='display:inline-block;background:#111827;color:white;padding:12px 18px;border-radius:10px;text-decoration:none;font-weight:bold;margin-bottom:20px;margin-left:10px;'>
       Send Hot Lead Follow-Ups
    </a>

    <h2>Top 10 Highest-Scoring Prospects</h2>
    <table border='1' cellpadding='8' style='background:white;border-collapse:collapse;width:100%;margin-bottom:35px;'>
    <tr>
        <th>Rank</th><th>Agency</th><th>Email</th><th>Score</th><th>Priority</th><th>Status</th><th>Preview</th>
    </tr>
    """

    for i, r in enumerate(top10, start=1):
        color = "#dc2626" if r.get("_priority") == "HOT" else "#f59e0b" if r.get("_priority") == "WARM" else "#6b7280"
        html += f"""
        <tr>
            <td>{i}</td>
            <td>{r.get('agency','')}</td>
            <td>{r.get('email','')}</td>
            <td><strong>{r.get('_score',0)}</strong></td>
            <td style='color:{color};font-weight:bold;'>{r.get('_priority')}</td>
            <td>{r.get('status','')}</td>
            <td><a href='{r.get('preview_url','')}'>Open</a></td>
        </tr>
        """

    html += """
    </table>

    <h2>All Outreach Leads</h2>
    <table border='1' cellpadding='8' style='background:white;border-collapse:collapse;width:100%;'>
    <tr>
        <th>Email</th><th>Agency</th><th>State</th><th>Score</th><th>Priority</th><th>Status</th><th>Sent At</th><th>Preview</th><th>Error</th>
    </tr>
    """

    for r in sorted(enriched, key=lambda x: x.get("_score", 0), reverse=True):
        color = "#dc2626" if r.get("_priority") == "HOT" else "#f59e0b" if r.get("_priority") == "WARM" else "#6b7280"
        html += f"""
        <tr>
            <td>{r.get('email','')}</td>
            <td>{r.get('agency','')}</td>
            <td>{r.get('state','')}</td>
            <td>{r.get('_score',0)}</td>
            <td style='color:{color};font-weight:bold;'>{r.get('_priority')}</td>
            <td>{r.get('status','')}</td>
            <td>{r.get('sent_at','')}</td>
            <td><a href='{r.get('preview_url','')}'>Open</a></td>
            <td>{r.get('error','')}</td>
        </tr>
        """

    html += "</table></body></html>"
    return html

@router.get("/admin/outreach/send", response_class=HTMLResponse)
def send_outreach():
    result = process_outreach_queue()

    return f"""
    <html>
    <body style='font-family:Arial;padding:40px;'>
        <h1>Outreach Send Results</h1>
        <p><strong>Sent this run:</strong> {result.get("sent")}</p>
        <p><strong>Total rows:</strong> {result.get("total")}</p>
        <a href="/admin/outreach">Back to Outreach Dashboard</a>
    </body>
    </html>
    """

@router.get("/admin/outreach/hot-followup", response_class=HTMLResponse)
def hot_followup():
    from app.services.hot_followup import send_hot_lead_followups
    result = send_hot_lead_followups()

    return f"""
    <html>
    <body style='font-family:Arial;padding:40px;'>
        <h1>Hot Lead Follow-Up Results</h1>
        <p><strong>Follow-ups sent:</strong> {result.get("sent")}</p>
        <a href="/admin/outreach">Back to Outreach Dashboard</a>
    </body>
    </html>
    """


