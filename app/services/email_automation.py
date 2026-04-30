from datetime import datetime, timedelta
import csv, os

QUEUE_FILE = "data/email_queue.csv"

FOLLOWUPS = [
    (0, "Your Home Health Audit Was Saved", "Your audit was saved. The next step is unlocking the full report and correction plan."),
    (1, "Revenue Loss Compounds Fast", "Operational delays, denials, and staffing gaps can quietly reduce agency performance every month."),
    (3, "Your Fix Plan Is the Next Step", "A structured fix plan helps prioritize revenue cycle, intake workflow, staffing, and compliance corrections."),
    (5, "Ready to Recover Lost Revenue?", "Your agency does not need more guesswork. The full optimization system converts audit findings into action.")
]

def queue_followups(email, name="", agency=""):
    os.makedirs("data", exist_ok=True)
    exists = os.path.exists(QUEUE_FILE)

    with open(QUEUE_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow(["send_at", "email", "name", "agency", "subject", "body", "status"])

        for days, subject, body in FOLLOWUPS:
            send_at = (datetime.now() + timedelta(days=days)).isoformat(timespec="seconds")
            writer.writerow([send_at, email, name, agency, subject, body, "pending"])

def get_queue():
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


