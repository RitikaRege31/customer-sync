# queue/rabbitmq.py

import pika

def get_rabbitmq_connection():
    """Establish a connection to RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='customer_queue')
    return connection, channel
