import os
import sys
import jinja2
import requests
import feedparser
import demoji
import hashlib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.models.models import Municipality, UserMunicipality, Bus, BusRoute
from src.models.rabbitmq import RabbitMq

MUNICIPALITY_NAME = 0
TIME = 1
STREETS = 2

class Parser:
    def __init__(self, parser_type):
        self.rabbitmq = RabbitMq(parser_type + '_queue')
        self.parser_type = parser_type
        self.data_for_queue = {}
        self.data = []

    def obtain_data(self):
        if self.parser_type == 'electricity':
            url_template = 'https://www.epsdistribucija.rs/Dan_{{day}}_Iskljucenja.htm'
            for i in range(0, 4):
                url = url_template.replace('{{day}}', str(i))
                self.make_request(url)
                self.parse_data()
        else:
            bus_route_url = os.environ.get('BUS_ROUTE_URL')
            feed = feedparser.parse(bus_route_url)
            tags_to_skip = ['Aktivne izmene na linijama', 'Planirane izmene', 'Informacija']
            current_changes = []

            for post in feed.entries:
                for tag in post.tags:
                    if tag.term not in tags_to_skip:
                        bus_route_number = tag.term.split('a ')[1]
                        bus = Bus.where('bus_route_number' , '=' , bus_route_number).first()
                        content = self.get_data_for_bus(post.link)
                        current_live_route_change = demoji.replace(content)
                        if bus is None:
                            bus = Bus()
                            bus.bus_route_number = bus_route_number
                            bus.save()

                        data = {bus.id: []}
                        data[bus.id].append(current_live_route_change)
                        current_changes.append(data)

                for change in current_changes:
                    for bus_id in change:
                        changes_to_save = change[bus_id]
                        bus = Bus.find(bus_id)
                        saved_routes = bus.bus_route
                        for saved_route in saved_routes:
                            for change_to_save in changes_to_save:
                                if hashlib.blake2b(saved_route.route_change.encode('utf-8')).hexdigest() == hashlib.blake2b(change_to_save.encode('utf-8')).hexdigest():
                                    changes_to_save.remove(change_to_save)

                        for change_to_save in changes_to_save:
                            self.update_bus_route(BusRoute(), bus, change_to_save)

    def update_bus_route(self, bus_route, bus, route_change):
        bus_route.bus_id = bus.id
        bus_route.route_change = route_change
        bus_route.save()
        for user in bus_route.bus.users:
            self.rabbitmq.send_message_to_queue({'bus_id': bus.id, 'user_id': user.user.id})

    def parse_data(self):
        self.streets = []
        all_trs = self.data.find_all('tr')
        title = all_trs[0].td.get_text().split(':')
        real_title = title[0] + 'е' + title[1]
        self.data_for_queue = {real_title: []}
        date = all_trs[0].find_all('td')[0].get_text()
        all_trs = all_trs[2:]
        for tr in all_trs:
            single_row_data = tr.find_all('td')
            municipality_name = single_row_data[MUNICIPALITY_NAME].get_text()
            streets = single_row_data[STREETS].get_text()
            time = single_row_data[TIME].get_text()
            single_day_data = {}
            single_day_data[municipality_name] = {'streets': streets, 'time': time, 'date': date}
            self.data_for_queue[real_title].append(single_day_data)
        self.send_data_to_queue()

    def send_data_to_queue(self):
        for day, municipalities in self.data_for_queue.items():
            for municipality in municipalities:
                self.rabbitmq.send_message_to_queue(municipality)

    def get_data_for_bus(self, url):
        self.make_request(url)
        return str(self.data.find_all('div', {'class': 'post-content'})[0])

    def make_request(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
        response = requests.get(url, headers=headers).content
        self.data = BeautifulSoup(response, 'html.parser')
