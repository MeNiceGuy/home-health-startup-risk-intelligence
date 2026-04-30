import csv, os
from datetime import datetime
from app.services.smtp_sender import send_email

QUEUE_FILE = "data/outreach_queue.csv"

def load_queue():
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        clean = []
        for r in rows:
            row = {str(k).replace("\ufeff",""): v for k, v in r.items()}
            if not row.get("lead_id"):
                row["lead_id"] = row.get("email","").replace("@","_").replace(".","_")
            clean.append(row)
        return clean

def save_queue(rows):
    os.makedirs("data", exist_ok=True)
    fields = ["created_at","lead_id","email","agency","state","preview_url","status","sent_at","error"]
    with open(QUEUE_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def build_outreach_email(agency, preview_url):
    subject = f"Benchmark insight for {agency}"
    body = f"""
Hello,

We identified public CMS performance signals suggesting {agency} may have operational or revenue-cycle improvement opportunities.

A limited benchmark preview is available here:
{preview_url}

The preview shows only high-level signals. A full audit can estimate impact, prioritize issues, and recommend corrective systems.

Best,
Home Health Performance Intelligence
"""
    return subject, body

def process_outreach_queue(limit=25):
    rows = load_queue()
    sent = 0

    for row in rows:
        if sent >= limit:
            break

        if row.get("status") != "pending":
            continue

        try:
            subject, body = build_outreach_email(row.get("agency","Agency"), tracked_url)
            send_email(row.get("email"), subject, body)

            row["status"] = "sent"
            row["sent_at"] = datetime.now().isoformat(timespec="seconds")
            row["error"] = ""
            sent += 1

        except Exception as e:
            row["status"] = "failed"
            row["error"] = str(e)

    save_queue(rows)
    return {"sent": sent, "total": len(rows)}





