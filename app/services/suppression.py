import csv, os
from datetime import datetime

SUPPRESSION_FILE = "data/suppression_list.csv"

def normalize_email(email):
    return str(email or "").strip().lower()

def is_suppressed(email):
    email = normalize_email(email)
    if not email or not os.path.exists(SUPPRESSION_FILE):
        return False

    with open(SUPPRESSION_FILE, newline="", encoding="utf-8") as f:
        return any(normalize_email(r.get("email")) == email for r in csv.DictReader(f))

def suppress_email(email, reason="STOP"):
    email = normalize_email(email)
    if not email:
        return False

    os.makedirs("data", exist_ok=True)

    if is_suppressed(email):
        return True

    exists = os.path.exists(SUPPRESSION_FILE)

    with open(SUPPRESSION_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["email","reason","suppressed_at"])
        w.writerow([email, reason, datetime.now().isoformat(timespec="seconds")])

    return True

