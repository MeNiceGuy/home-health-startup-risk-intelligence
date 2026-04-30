from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime, timedelta
import csv
import os

router = APIRouter()

LEADS_FILE = "data/leads.csv"
QUEUE_FILE = "data/email_queue.csv"

# -----------------------
# SAVE LEAD
# -----------------------
def save_lead(name, email, agency, phone, source):
    os.makedirs("data", exist_ok=True)
    file_exists = os.path.exists(LEADS_FILE)

    with open(LEADS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["created_at", "name", "email", "agency", "phone", "source", "status"])

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            name, email, agency, phone, source, "new"
        ])

# -----------------------
# EMAIL QUEUE
# -----------------------
FOLLOWUPS = [
    (0, "Your Audit Is Ready", "Your audit was saved. Next step: unlock full report."),
    (1, "Revenue Loss Compounds", "Small inefficiencies reduce revenue every month."),
    (3, "Fix Plan Recommended", "A structured fix plan improves performance."),
    (5, "Ready to Recover Revenue?", "Upgrade to full optimization system.")
]

def queue_followups(email, name, agency):
    os.makedirs("data", exist_ok=True)
    exists = os.path.exists(QUEUE_FILE)

    # Prevent duplicate email sequences
    existing = []
    if exists:
        with open(QUEUE_FILE, newline="", encoding="utf-8") as f:
            existing = list(csv.DictReader(f))

    if any(r["email"] == email for r in existing):
        return

    with open(QUEUE_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow(["send_at","email","name","agency","subject","body","status"])

        for days, subject, body in FOLLOWUPS:
            send_at = (datetime.now() + timedelta(days=days)).isoformat(timespec="seconds")
            writer.writerow([send_at, email, name, agency, subject, body, "pending"])

# -----------------------
# CAPTURE ROUTE
# -----------------------
@router.post("/lead/capture")
def capture_lead(
    name: str = Form(...),
    email: str = Form(...),
    agency: str = Form(""),
    phone: str = Form(""),
    source: str = Form("operating_audit")
):
    save_lead(name, email, agency, phone, source)
    queue_followups(email, name, agency)
    return RedirectResponse("/lead/thank-you", status_code=303)

# -----------------------
# THANK YOU PAGE
# -----------------------
@router.get("/lead/thank-you", response_class=HTMLResponse)
def thank_you():
    return """
    <h1>Audit Saved</h1>
    <p>Your results are ready. Next step: unlock full report.</p>
    <a href='/checkout/audit'>Unlock Full Audit</a>
    """

# -----------------------
# PIPELINE DASHBOARD
# -----------------------
@router.get("/admin/pipeline", response_class=HTMLResponse)
def pipeline():
    if not os.path.exists(LEADS_FILE):
        return "<h1>No leads yet.</h1>"

    with open(LEADS_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    total = len(rows)
    pipeline_value = total * 2999

    html = f"<h1>Pipeline</h1><h2>{total} Leads</h2><h2>${pipeline_value}</h2><table border='1'>"

    for r in rows:
        html += f"<tr><td>{r['name']}</td><td>{r['email']}</td></tr>"

    html += "</table>"
    return html

# -----------------------
# EMAIL QUEUE VIEW
# -----------------------
@router.get("/admin/email-queue", response_class=HTMLResponse)
def email_queue():
    if not os.path.exists(QUEUE_FILE):
        return "<h1>No emails queued.</h1>"

    with open(QUEUE_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    html = """
    <h1>Email Queue</h1>

    <a href="/admin/process-email-queue"
       style="display:inline-block;background:#dc2626;color:white;padding:12px 18px;border-radius:10px;text-decoration:none;font-weight:bold;margin-bottom:20px;">
       Send Pending Follow-Up Emails
    </a>

    <table border='1' cellpadding='10'>
    """

    for r in rows:
        html += f"<tr><td>{r['email']}</td><td>{r['subject']}</td><td>{r['status']}</td></tr>"

    html += "</table>"
    return html


@router.get("/admin/process-email-queue", response_class=HTMLResponse)
def process_email_queue_route():
    from app.services.smtp_sender import process_email_queue

    try:
        result = process_email_queue()
        return f"<h1>Email Queue Processed</h1><p>{result['message']}</p><a href='/admin/email-queue'>Back to Email Queue</a>"
    except Exception as e:
        return f"<h1>Email Send Error</h1><p>{str(e)}</p><a href='/admin/email-queue'>Back</a>"




