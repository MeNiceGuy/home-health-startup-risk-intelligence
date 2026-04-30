from fastapi_mail import FastMail, MessageSchema
from app.services.email_config import conf

async def send_kit_email(email: str, subject: str, body: str, file_path: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype="html",
        attachments=[file_path]
    )

    fm = FastMail(conf)
    await fm.send_message(message)


