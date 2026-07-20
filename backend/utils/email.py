import smtplib
import os

from email.mime.text import MIMEText


def send_email(receiver, otp):

    sender = os.getenv("MAIL_USER")
    password = os.getenv("MAIL_PASSWORD")

    message = MIMEText(
        f"""
Welcome to ChatVerse!

Your email verification OTP is:

{otp}

This OTP is valid for 10 minutes.

Thank you,
ChatVerse Team
"""
    )

    message["Subject"] = "ChatVerse OTP Verification"
    message["From"] = sender
    message["To"] = receiver


    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()

    server.login(
        sender,
        password
    )

    server.send_message(message)

    server.quit()
    