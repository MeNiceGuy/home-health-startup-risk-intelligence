from app.services.suppression import is_suppressed
import csv, os
from datetime import datetime
from app.services.smtp_sender import send_email

TARGET_FILE = "data/cms_target_leads.csv"
SENT_FILE = "data/auto_outreach_sent.csv"

def already_sent(lead_id):
    if not os.path.exists(SENT_FILE):
        return False
    with open(SENT_FILE, newline="", encoding="utf-8") as f:
        return any(r.get("lead_id") == lead_id for r in csv.DictReader(f))

def log_sent(lead_id, email, agency):
    exists = os.path.exists(SENT_FILE)
    with open(SENT_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["sent_at","lead_id","email","agency"])
        w.writerow([datetime.now().isoformat(timespec="seconds"), lead_id, email, agency])

def send_enriched_outreach():
    if not os.path.exists(TARGET_FILE):
        return {"sent": 0, "error": "No target file found."}

    with open(TARGET_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    sent = 0

    for r in rows:
        lead_id = r.get("lead_id","")
        email = r.get("email","")
        agency = r.get("agency","your agency")
        preview = r.get("preview_url","http://127.0.0.1:8000/pricing")

        if not email or is_suppressed(email) or r.get("email_verified") != "true" or already_sent(lead_id):
            continue

        subject = f"{agency}: revenue risk signals detected"

        body = f"""
Hello,

Boswell Consulting Group identified public performance signals suggesting {agency} may have operational or revenue-cycle improvement opportunities.

Your free preview is available here:
{preview}

The preview shows limited indicators. The full audit can estimate revenue exposure, prioritize issues, and recommend corrective systems.

Best,
Boswell Consulting Group

Operational benchmarking only. Not legal, clinical, billing, or regulatory advice.
Reply STOP to opt out.
"""

        if send_email(email, subject, body):
            log_sent(lead_id, email, agency)
            sent += 1

    return {"sent": sent}


