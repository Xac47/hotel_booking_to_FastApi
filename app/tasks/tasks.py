import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.tasks.celery import celery_app
from app.tasks.email_templates import create_booking_confirmation_template


@celery_app.task
def process_pic(path: str):
    image_path = Path(path)
    image = Image.open(image_path)
    image_resized_1000_500 = image.resize((1000, 500))
    image_resized_400_200 = image.resize((400, 200))
    image_resized_1000_500.save(f"app/static/images/resized_1000_500_{image_path.name}")
    image_resized_400_200.save(f"app/static/images/resized_400_200_{image_path.name}")


@celery_app.task
def send_booking_confirmation_email(booking: dict, email_to: EmailStr):

    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
