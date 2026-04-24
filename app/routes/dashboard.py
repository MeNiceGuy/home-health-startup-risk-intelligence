from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.services.saas_tracking import get_dashboard_data

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/", response_class=HTMLResponse)
def dashboard():
    subs, scores = get_dashboard_data()

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
    <body style="font-family:Arial;background:#f8fafc;padding:40px;">
        <h1>Boswell Consulting Group SaaS Dashboard</h1>

        <h2>Subscription Tracking</h2>
        <table border="1" cellpadding="10" style="background:white;border-collapse:collapse;">
            <tr><th>Email</th><th>Status</th><th>Created</th></tr>
            {sub_rows}
        </table>

        <h2>Intelligence Score History</h2>
        <table border="1" cellpadding="10" style="background:white;border-collapse:collapse;">
            <tr>
                <th>Agency</th><th>Audit Type</th><th>Total</th><th>Compliance</th>
                <th>Clinical</th><th>Revenue</th><th>Operations</th><th>Date</th>
            </tr>
            {score_rows}
        </table>

        <br>
        <a href="/operating-audit/">Run Operating Audit</a><br><br>
        <a href="/audit/">Run Startup Audit</a><br><br>
        <a href="/kits/">View Kits</a>
    </body>
    </html>
    """
