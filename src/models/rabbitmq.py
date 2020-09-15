from src.models import loader 
import pika
import json
import os

class RabbitMq:
    def __init__(self, queue_name):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get('RABBITMQ_HOST')))
        self.queue_name = queue_name
        self.routing_key = queue_name
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def __del__(self):
        self.connection.close()
    
    def send_message_to_queue(self, message):
        message = json.dumps(message)
        self.channel.basic_publish(exchange='', routing_key=self.routing_key, body=message)
    
    def start_consuming(self, callback):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback)
        self.channel.start_consuming()
