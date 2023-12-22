import pika
from django.conf import settings

class RabbitMQSender:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                virtual_host=settings.RABBITMQ_VIRTUAL_HOST,
                credentials=pika.PlainCredentials(
                    username=settings.RABBITMQ_USER,
                    password=settings.RABBITMQ_PASSWORD,
                ),
            )
        )
        self.channel = self.connection.channel()

    def send_message(self, queue_name, message):
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_publish(exchange='', routing_key=queue_name, body=message)

    def close_connection(self):
        self.connection.close()
