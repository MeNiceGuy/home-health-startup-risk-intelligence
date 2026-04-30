import csv, os
from datetime import datetime

EVENT_FILE = "data/lead_events.csv"

def log_lead_event(lead_id, agency, email, event):
    os.makedirs("data", exist_ok=True)
    exists = os.path.exists(EVENT_FILE)

    with open(EVENT_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["time","lead_id","agency","email","event"])
        w.writerow([datetime.now().isoformat(timespec="seconds"), lead_id, agency, email, event])

def get_lead_score(lead_id):
    if not os.path.exists(EVENT_FILE):
        return 0

    score = 0
    with open(EVENT_FILE, newline="", encoding="utf-8") as f:
        rows = csv.DictReader(f)
        for r in rows:
            if r.get("lead_id") == lead_id:
                if r.get("event") == "preview_clicked":
                    score += 30
                if r.get("event") == "full_audit_clicked":
                    score += 50
                if r.get("event") == "pdf_requested":
                    score += 40

    return score

def lead_status(score):
    if score >= 80:
        return "HOT"
    if score >= 40:
        return "WARM"
    return "COLD"


