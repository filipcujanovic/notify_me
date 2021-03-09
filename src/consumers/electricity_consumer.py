import sys

sys.path.append('.')

from src.models.rabbitmq import RabbitMq
from src.models.notification import Notification
from src.models.models import Municipality
from src.models.models import UserMunicipality
import json

MUNICIPALITY = 0

def handle_message_from_queue(ch, method, properties, body):
    body = json.loads(body)
    for date in body:
        municipality = list(body[date].keys())[MUNICIPALITY]
        municipality_id = Municipality.where('name', '=', municipality).first().id
        for user in UserMunicipality.where('municipality_id' , '=', municipality_id).get():
            notification = Notification('email', 'electricity', municipality_id, user.user_id)
            notification.send_email(body)
            ch.basic_ack(delivery_tag = method.delivery_tag)

rabbitmq = RabbitMq('electricity_queue')
rabbitmq.start_consuming(handle_message_from_queue)