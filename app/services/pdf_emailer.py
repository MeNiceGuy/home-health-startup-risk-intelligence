import os
from email.message import EmailMessage

def send_pdf_email(to_email, pdf_path, subject="Your Audit Report"):

    # DEV MODE: Skip sending if SMTP not configured
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    if not smtp_user or not smtp_pass:
        print("⚠️ EMAIL DISABLED: SMTP credentials missing. PDF generated only.")
        return True

    import smtplib

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_email

    msg.set_content("Your audit report is attached.")

    with open(pdf_path, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(pdf_path)

    msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

    return True


