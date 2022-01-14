import os
import json
import base64
from dotenv import load_dotenv, find_dotenv
import sendgrid
from sendgrid.helpers.mail import *

def mail_sender(subject,msg,email):
    load_dotenv(verbose=True)
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    print("API KEY : " + SENDGRID_API_KEY)
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    from_email = Email("Solidarity.purchase@gmail.com")
    to_email = To(email)
    content = Content("text/plain", msg)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return response