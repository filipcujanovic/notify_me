import os
import sys
import base64
import jinja2
from src.models import loader
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .models import Bus, BusRoute, User
from .gmail import Gmail
from googleapiclient.discovery import build

class Notification:
    def __init__(self, notification_channel, notification_type, model_id, user_id):
        self.notification_channel = notification_channel
        self.notification_type = notification_type
        self.model_id = model_id
        self.user_id = user_id
        self.receiver_email = ''
        self.email_title = ''
        self.html = []
        self.email_template = []

        self.message = MIMEMultipart('alternative')
        self.creds = Gmail.get_gmail_creds()
        self.service = build('gmail', 'v1', credentials=Gmail.get_gmail_creds())

    def create_email(self, data = None):
        if self.notification_channel == 'email':
            self.receiver_email = User.find(self.user_id).email
            if self.notification_type == 'bus':
                bus = Bus().find(self.model_id)
                bus_routes = bus.bus_route
                self.email_title = 'Izmena na liniji ' + bus.bus_route_number
                for bus_route in bus_routes:
                    self.email_template.append(bus_route.route_change)
            elif self.notification_type == 'electricity':
                template = os.environ.get('TEMPLATE_DIR') + 'email_template.html'
                if not os.path.exists(template):
                    print('No template file present: %s' % template)
                    sys.exit()
                template_loader = jinja2.FileSystemLoader(searchpath='')
                template_env = jinja2.Environment(loader=template_loader)
                template_html = template_env.get_template(template)
                self.email_title = data['date'] + ' у општини ' + data['municipality']
                self.email_template.append(template_html.render(data=data))

    def send_email(self, data = None):
        self.create_email(data)
        html_text = ''.join(self.email_template)
        self.message['Subject'] = self.email_title
        self.message['From'] = 'me'
        self.message['To'] = self.receiver_email
        self.message.attach(MIMEText(html_text, 'html'))
        raw = base64.urlsafe_b64encode(self.message.as_bytes())
        raw = raw.decode()
        body = {'raw': raw}
        self.service.users().messages().send(userId='me', body=body).execute()
        print('Email sent - ' + self.receiver_email)