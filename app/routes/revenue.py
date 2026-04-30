from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import csv, os

router = APIRouter()

def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

@router.get("/admin/revenue", response_class=HTMLResponse)
def revenue_dashboard():
    leads = read_csv("data/leads.csv")
    bookings = read_csv("data/bookings.csv")
    emails = read_csv("data/email_queue.csv")

    total_leads = len(leads)
    total_bookings = len(bookings)
    pending_emails = len([e for e in emails if e.get("status") == "pending"])
    sent_emails = len([e for e in emails if e.get("status") == "sent"])

    pipeline_value = (total_leads * 129) + (total_bookings * 2999)

    html = f"""
    <html>
    <body style='font-family:Arial;background:#f8fafc;padding:40px;'>
        <h1>Revenue Command Center</h1>

        <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-bottom:30px;'>
            <div style='background:white;padding:22px;border-radius:16px;box-shadow:0 6px 18px rgba(0,0,0,.06);'>
                <h3>Total Leads</h3><h1>{total_leads}</h1>
            </div>
            <div style='background:white;padding:22px;border-radius:16px;box-shadow:0 6px 18px rgba(0,0,0,.06);'>
                <h3>Bookings</h3><h1>{total_bookings}</h1>
            </div>
            <div style='background:white;padding:22px;border-radius:16px;box-shadow:0 6px 18px rgba(0,0,0,.06);'>
                <h3>Pipeline Value</h3><h1>${pipeline_value:,}</h1>
            </div>
            <div style='background:white;padding:22px;border-radius:16px;box-shadow:0 6px 18px rgba(0,0,0,.06);'>
                <h3>Email Status</h3><p>Sent: {sent_emails}</p><p>Pending: {pending_emails}</p>
            </div>
        </div>

        <a href='/admin/pipeline'>View Lead Pipeline</a> |
        <a href='/admin/bookings'>View Bookings</a> |
        <a href='/admin/email-queue'>View Email Queue</a> |
        <a href='/operating-audit/?intake_time=5&missed_visits=9&denial_rate=18&ar_days=48'>Run Demo Audit</a>
    </body>
    </html>
    """
    return html


