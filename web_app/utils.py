import smtplib
import secrets
import string
from email.message import EmailMessage


def get_unique_hash():
    letters_and_digits = string.ascii_letters + string.digits
    return "".join(secrets.choice(letters_and_digits) for _ in range(20))
