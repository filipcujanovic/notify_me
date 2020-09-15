import sys
sys.path.append('.')
from src.models.rabbitmq import RabbitMq
from src.models.notification import Notification
import json

def handle_message_from_queue(ch, method, properties, body):
    body = json.loads(body)
    print(body)
    notification = Notification('email', 'bus', body['bus_id'], body['user_id'])
    notification.send_email()
    ch.basic_ack(delivery_tag = method.delivery_tag)

rabbitmq = RabbitMq('bus_queue')
rabbitmq.start_consuming(handle_message_from_queue)