import csv
import os
import smtplib
from datetime import datetime
from email.message import EmailMessage

QUEUE_FILE = "data/email_queue.csv"

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)

def send_email(to_email, subject, body):
    if not SMTP_USER or not SMTP_PASS:
        raise RuntimeError("SMTP_USER or SMTP_PASS is missing.")

    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

def process_email_queue():
    if not os.path.exists(QUEUE_FILE):
        return {"sent": 0, "message": "No queue file found."}

    with open(QUEUE_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    sent = 0
    now = datetime.now()

    for row in rows:
        if row.get("status") != "pending":
            continue

        send_at = datetime.fromisoformat(row["send_at"])

        if send_at <= now:
            send_email(row["email"], row["subject"], row["body"])
            row["status"] = "sent"
            sent += 1

    with open(QUEUE_FILE, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["send_at","email","name","agency","subject","body","status"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return {"sent": sent, "message": f"{sent} emails sent."}
