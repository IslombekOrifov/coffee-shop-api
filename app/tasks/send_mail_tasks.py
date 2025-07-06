import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config.settings import settings

from .celery import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(name="app.tasks.send_mail_tasks.send_email_task")
def send_email_task(to_email: str, subject: str, body: str):
    logger.info(f"Starting send_email_task to {to_email}")
    msg = MIMEMultipart()
    msg["From"] = settings.EMAIL_HOST_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))
    try:
        logger.info(f"Coooodeeeee {body}")
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, to_email, msg.as_string())

        logger.info(f"Email successfully sent to {to_email} {body}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}. Error: {e}")
        raise
