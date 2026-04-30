import csv, os
from datetime import datetime

OUTREACH_FILE = "data/outreach_queue.csv"

def queue_outreach(email, agency, state, preview_url):
    os.makedirs("data", exist_ok=True)
    exists = os.path.exists(OUTREACH_FILE)

    with open(OUTREACH_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["created_at","email","agency","state","preview_url","status"])
        writer.writerow([datetime.now().isoformat(timespec="seconds"), email, agency, state, preview_url, "pending"])


