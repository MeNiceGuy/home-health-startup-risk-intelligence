from app.services.suppression import is_suppressed
import csv, os
from datetime import datetime
from app.services.smtp_sender import send_email

EVENT_FILE = "data/lead_events.csv"
FOLLOWUP_FILE = "data/followup_log.csv"

SEQUENCE = [
    {
        "stage": "day1_incomplete_preview",
        "subject": "{agency}: your revenue risk preview is incomplete",
        "body": """Hello,

Your free preview showed potential revenue-risk signals for {agency}.

The preview only shows limited indicators. The full audit unlocks:
- estimated monthly revenue exposure
- top leakage drivers
- CMS benchmark positioning
- corrective roadmap
- executive PDF report

Unlock the full audit here:
http://127.0.0.1:8000/audit-checkout?lead_id={lead_id}&email={email}&agency={agency}

Best,
Boswell Consulting Group"""
    },
    {
        "stage": "day2_revenue_risk",
        "subject": "{agency}: unresolved gaps may keep costing you",
        "body": """Hello,

Operational gaps can quietly compound through denial risk, delayed A/R, slow intake, missed visits, and staffing instability.

Agencies with similar patterns may experience preventable revenue leakage each month.

The full audit is designed to estimate exposure and identify what to fix first:
http://127.0.0.1:8000/audit-checkout?lead_id={lead_id}&email={email}&agency={agency}

Best,
Boswell Consulting Group"""
    },
    {
        "stage": "day3_final_action",
        "subject": "Final reminder: review {agency}'s performance risk",
        "body": """Hello,

This is the final reminder for {agency}'s revenue-risk preview.

The free preview identified possible performance signals. The full audit provides the actual roadmap:
- revenue opportunity score
- estimated monthly impact
- priority corrective actions
- executive PDF report

Complete the full audit here:
http://127.0.0.1:8000/audit-checkout?lead_id={lead_id}&email={email}&agency={agency}

Best,
Boswell Consulting Group

Operational benchmarking only. Not legal, clinical, billing, or regulatory advice."""
    }
]

def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def read_events():
    return read_csv(EVENT_FILE)

def already_sent(lead_id, stage):
    rows = read_csv(FOLLOWUP_FILE)
    return any(r.get("lead_id") == lead_id and r.get("stage") == stage for r in rows)

def log_followup(lead_id, email, agency, stage):
    os.makedirs("data", exist_ok=True)
    exists = os.path.exists(FOLLOWUP_FILE)
    with open(FOLLOWUP_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["time","lead_id","email","agency","stage"])
        w.writerow([datetime.now().isoformat(timespec="seconds"), lead_id, email, agency, stage])

def next_stage_for(lead_id):
    for step in SEQUENCE:
        if not already_sent(lead_id, step["stage"]):
            return step
    return None

def send_multi_stage_followups():
    events = read_events()
    grouped = {}

    for e in events:
        lead_id = e.get("lead_id", "")
        if lead_id:
            grouped.setdefault(lead_id, []).append(e)

    sent = 0
    skipped = 0

    for lead_id, rows in grouped.items():
        latest = rows[-1]
        email = latest.get("email", "")
        agency = latest.get("agency", "your agency")
        event_types = [r.get("event") for r in rows]

        if not email or is_suppressed(email):
            skipped += 1
            continue

        if "audit_paid" in event_types:
            skipped += 1
            continue

        if "preview_clicked" not in event_types and "checkout_started" not in event_types:
            skipped += 1
            continue

        step = next_stage_for(lead_id)
        if not step:
            skipped += 1
            continue

        subject = step["subject"].format(agency=agency, lead_id=lead_id, email=email)
        body = step["body"].format(agency=agency, lead_id=lead_id, email=email)

        if send_email(email, subject, body):
            log_followup(lead_id, email, agency, step["stage"])
            sent += 1
        else:
            skipped += 1

    return {"sent": sent, "skipped": skipped}


