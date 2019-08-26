import os
import re
import smtplib
import sys

import jinja2
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class HtmlParser:
    def __init__(self, parser_type):
        # self.receiver_emails = ['cujanovic.filip@gmail.com', 'milosb793@gmail.com']
        self.receiver_emails = ['cujanovic.filip@gmail.com']
        self.email_title = ''
        self.sender_email = 'cujanovic.test.mail@gmail.com'
        self.sender_password = 'xCeo%t3^@!*djVi27M^fj!p7Ql72O%Z22fx'
        self.html = []
        self.email_template = []

        if parser_type == 'electricity':
            url_template = 'https://www.epsdistribucija.rs/Dan_{{day}}_Iskljucenja.htm'
            for i in range(0, 4):
                url = url_template.replace('{{day}}', str(i))
                headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
                response = requests.get(url, headers=headers).content
                self.html.append(BeautifulSoup(response, 'html.parser'))
            self.streets_to_find = ['БУЛЕВАР ОСЛОБОЂЕЊА', 'КРАГУЈЕВАЧКИХ ЂАКА', 'ТРЕШЊА']
            self.dates = []
            self.streets = []

        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(self.sender_email, self.sender_password)
        self.message = MIMEMultipart('alternative')

    def parse_data(self):
        for row in self.html:
            self.streets = []
            all_trs = row.find_all('tr')
            title = all_trs[0].td.get_text().split(':')
            self.dates.append(title[1])
            self.email_title = title[0] + 'е'
            all_trs = all_trs[2:]
            for tr in all_trs:
                single_row_data = tr.find_all('td')
                data_row = single_row_data[2]
                for street_to_find in self.streets_to_find:
                    result = re.search('(?<=' + street_to_find + ': ).*?, ', data_row.get_text())
                    if result is not None:
                        self.streets.append(
                            {'name': street_to_find, 'time': single_row_data[1].get_text(),
                             'numbers': result.group().strip()})
            data = {'title': self.email_title, 'streets': self.streets}
            self.create_email(data)
        self.send_email()

    def create_email(self, data):
        template = 'email_template.html'
        if not os.path.exists(template):
            print('No template file present: %s' % template)
            sys.exit()

        template_loader = jinja2.FileSystemLoader(searchpath='')
        template_env = jinja2.Environment(loader=template_loader)
        template_html = template_env.get_template(template)

        self.email_template.append(template_html.render(data=data))

    def send_email(self):
        for receiver_email in self.receiver_emails:
            html_text = ''.join(self.email_template)
            self.message['Subject'] = self.email_title + ','.join(self.dates)
            self.message['From'] = self.sender_email
            self.message['To'] = receiver_email
            self.message.attach(MIMEText(html_text, 'html'))
            self.server.send_message(self.message, self.sender_email, receiver_email)
