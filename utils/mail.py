from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException, status
import smtplib
from config import config
from db.base import Users
from db.scripts.users import get_email


def send_ver_mail(user_id, url, message):

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Verification Link"
    msg["From"] = config.EMAIL_USERNAME
    msg["To"] = get_email(user_id)
    ver_text = f"""<pre> 
    Добрый день.
    Для подтверждения электронной почты перейдите по ссылке: <a href="{url}/{message}">Нажмите на меня</a>
    С уважением,
    Local Museum.
    </pre>"""
    email_body = MIMEText(ver_text, "html")
    msg.attach(email_body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(config.EMAIL_USERNAME, config.EMAIL_PASSWORD)
            smtp.send_message(msg)
    except:
        print("Unable to send")
