import os
import smtplib
from email.message import EmailMessage

def send_pdf_email(to_email, pdf_path, subject="Your Home Health Performance Audit"):
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_pass = os.getenv("SMTP_PASS", "")
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    if not smtp_user or not smtp_pass:
        raise Exception("SMTP credentials are missing.")

    msg = EmailMessage()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.set_content("""
Your Home Health Performance Audit is attached.

This report includes:
- Executive summary
- Priority roadmap
- Implementation timeline
- Expected outcomes
- Revenue leakage breakdown

This audit is a decision-support tool and should be validated against agency records.
""")

    with open(pdf_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename="home_health_performance_audit.pdf"
        )

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

    return True
