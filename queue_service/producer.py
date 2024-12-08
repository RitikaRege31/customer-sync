# queue/producer.py

import pika
import json

def send_to_queue(customer_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='customer_queue')

    channel.basic_publish(
        exchange='',
        routing_key='customer_queue',
        body=json.dumps(customer_data)
    )

    connection.close()

if __name__ == "__main__":
    customer_data = {"name": "John Doe", "email": "john@example.com"}
    send_to_queue(customer_data)
