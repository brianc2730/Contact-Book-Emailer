
import smtplib
import os
from email.message import EmailMessage

def emailer(recipient, subject, message):

    my_message = EmailMessage()

    my_message["Subject"] = subject
    my_message["From"] = os.environ.get("TEST_EMAIL")
    my_message["To"] = recipient
    my_message.set_content(message)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as emailer:

        emailer.login(os.environ.get("TEST_EMAIL"), os.environ.get("TEST_PASSWORD"))

        emailer.send_message(my_message)

