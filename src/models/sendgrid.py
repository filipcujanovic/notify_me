import sendgrid
import os, sys
from sendgrid.helpers.mail import *
from src.models import loader

def create_client():
    api_key = os.environ.get('SENDGRID_API_KEY')
    return sendgrid.SendGridAPIClient(api_key=api_key)

def send_email(**details):
    from_email = Email(details.get('from'))
    to_email = To(details.get('to'))
    subject = details.get('subject')
    content = Content('text/html', details.get('content'))

    mail = Mail(from_email, to_email, subject, content)

    return create_client().client.mail.send.post(request_body=mail.get())