from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException, status
import smtplib
from config import config
from db.base import Users
from db.scripts.museums import select_with_id
from db.scripts.users import get_email, get_subs_email


def set_msg_up():
    msg = MIMEMultipart("alternative")
    msg["From"] = config.EMAIL_USERNAME
    return msg


def send_ver_mail(user_id, url, message):
    msg = set_msg_up()
    msg["Subject"] = "Verification Link"
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


def send_notif_mail(museum_id, message):
    msg = set_msg_up()
    museum = select_with_id(id=museum_id).title
    header = f"""<pre> 
    Добрый день.
    {museum} опубликовал новое сообщение:
    {message}
    </pre>"""
    header = MIMEText(header, "html")
    msg.attach(header)
    msg["To"] = ", ".join(get_subs_email(museum_id))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(config.EMAIL_USERNAME, config.EMAIL_PASSWORD)
            smtp.send_message(msg)
    except:
        print("Unable to send")
