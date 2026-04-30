import csv, os
from datetime import datetime
from app.services.lead_tracking import get_lead_score, lead_status
from app.services.smtp_sender import send_email

QUEUE_FILE = "data/outreach_queue.csv"

def send_hot_lead_followups():
    if not os.path.exists(QUEUE_FILE):
        return {"sent": 0}

    sent = 0

    with open(QUEUE_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for r in rows:
        lead_id = r.get("lead_id") or r.get("email","").replace("@","_").replace(".","_")
        score = get_lead_score(lead_id)

        if lead_status(score) == "HOT":
            subject = f"Next step for {r.get('agency','your agency')}"
            body = f"""
Hello,

Your benchmark activity indicates interest in the full performance audit.

Based on the preview and audit path, the next best step is reviewing the recommended implementation system.

Open your preview again:
{r.get("preview_url","")}

Best,
Home Health Performance Intelligence
"""
            send_email(r.get("email"), subject, body)
            sent += 1

    return {"sent": sent}


