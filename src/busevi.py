import re
import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

bus_route_url = 'https://www.busevi.com/feed/'

gmail_user = 'cujanovic.test.mail@gmail.com'
gmail_password = 'xCeo%t3^@!*djVi27M^fj!p7Ql72O%Z22fx'
receiver_emails = ['milosb793@gmail.com', 'cujanovic.filip@gmail.com']

feed = feedparser.parse(bus_route_url)
tag_to_skip = 'Aktivne izmene na linijama'

bus_numbers_to_find = ['706', '73', '703', '706E']

posts = []
added_posts = []

for post in feed.entries:
    for tag in post.tags:
        if tag_to_skip != tag.term:
            bus_number = tag.term.split('a ')[1]
            if bus_number in bus_numbers_to_find:
                if post.title not in added_posts:
                    posts.append(post)
                    added_posts.append(post.title)
html = ''


for post in posts:
    html += re.sub('(?=<p>The post ).+', '', post.content[0].value)


for receiver_email in receiver_emails:
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Radovi na ' + ('liniji ' if len(bus_numbers_to_find) == 1 else 'linijama ') + ' '.join(bus_numbers_to_find)
    message['From'] = gmail_user
    message['To'] = receiver_email
    message.attach(MIMEText(html, 'html'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, receiver_email, message.as_string())
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')
