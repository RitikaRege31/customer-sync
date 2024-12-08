# queue/consumer.py

# import pika
# import json

# def callback(ch, method, properties, body):
#     customer_data = json.loads(body)
#     print(f"Received customer data: {customer_data}")

#     # Sync to Stripe (as in stripe_sync.py) or save to DB here

# def consume_from_queue():
#     connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
#     channel = connection.channel()

#     channel.queue_declare(queue='customer_queue')

#     channel.basic_consume(
#         queue='customer_queue', on_message_callback=callback, auto_ack=True
#     )

#     print('Waiting for messages. To exit press CTRL+C')
#     channel.start_consuming()

# if __name__ == "__main__":
#     consume_from_queue()
# import pika
# import json
# # from db.db_config import get_db_connection
# import mysql.connector

# def get_db_connection():
#     """Establish a connection to the MySQL database."""
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",  
#         password="Ritika12@",  
#         database="customer_sync"
#     )

# def callback(ch, method, properties, body):
#     print("Received customer data:", body)

#     try:
#         # Parse the received message
#         customer_data = json.loads(body)
#         name = customer_data.get('name')
#         email = customer_data.get('email')

#         if not name or not email:
#             print("Invalid data. Name or email is missing.")
#             return

#         # Insert data into the database
#         connection = get_db_connection()
#         cursor = connection.cursor()

#         sql = "INSERT INTO customers (name, email) VALUES (%s, %s)"
#         cursor.execute(sql, (name, email))
#         connection.commit()

#         print("Customer added to the database:", name, email)

#         cursor.close()
#         connection.close()

#     except Exception as e:
#         print(f"Error processing message: {e}")

# connection_params = pika.ConnectionParameters('localhost')
# connection = pika.BlockingConnection(connection_params)
# channel = connection.channel()

# channel.queue_declare(queue='customer_queue')

# channel.basic_consume(queue='customer_queue', on_message_callback=callback, auto_ack=True)

# print('Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()
# import pika
# import json
# import mysql.connector
# import stripe

# # Set your Stripe secret key
# stripe.api_key = 'sk_test_51QRVPRFNk3oYkWkNiZxiuYeeSRPAi0Rk2EoNzRNw6oztl03us0dlu04cktIuwCbvPgdAVyhNeBouVvLH421H1ZIg00yiY35uGX'

# def get_db_connection():
#     """Establish a connection to the MySQL database."""
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",  
#         password="Ritika12@",  
#         database="customer_sync"
#     )

# def callback(ch, method, properties, body):
#     print("Received customer data:", body)

#     try:
#         # Parse the received message
#         customer_data = json.loads(body)
#         name = customer_data.get('name')
#         email = customer_data.get('email')

#         if not name or not email:
#             print("Invalid data. Name or email is missing.")
#             return

#         # Insert data into the database
#         connection = get_db_connection()
#         cursor = connection.cursor()

#         sql = "INSERT INTO customers (name, email) VALUES (%s, %s)"
#         cursor.execute(sql, (name, email))
#         connection.commit()

#         print("Customer added to the database:", name, email)

#         # Create the customer on Stripe
#         stripe_customer = stripe.Customer.create(
#             name=name,
#             email=email
#         )

#         print(f"Customer created on Stripe with ID: {stripe_customer['id']}")

#         cursor.close()
#         connection.close()

#     except Exception as e:
#         print(f"Error processing message: {e}")

# # Set up RabbitMQ connection
# connection_params = pika.ConnectionParameters('localhost')
# connection = pika.BlockingConnection(connection_params)
# channel = connection.channel()

# # Declare the queue
# channel.queue_declare(queue='customer_queue')

# # Consume the message from the queue
# channel.basic_consume(queue='customer_queue', on_message_callback=callback, auto_ack=True)

# print('Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()

import pika
import json
import mysql.connector
import stripe

# Set your Stripe secret key
# stripe.api_key = ''
stripe.api_key = 'sk_test_51QRVPRFNk3oYkWkNiZxiuYeeSRPAi0Rk2EoNzRNw6oztl03us0dlu04cktIuwCbvPgdAVyhNeBouVvLH421H1ZIg00yiY35uGX'

def get_db_connection():
    """Establish a connection to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="Ritika12@",  
        database="customer_sync"
    )

def callback(ch, method, properties, body):
    print("Received customer data:", body)

    try:
        # Parse the received message
        customer_data = json.loads(body)
        name = customer_data.get('name')
        email = customer_data.get('email')

        if not name or not email:
            print("Invalid data. Name or email is missing.")
            return

        # Check if the customer already exists in the database
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
        existing_customer = cursor.fetchone()

        if existing_customer:
            print(f"Customer with email {email} already exists. Skipping insertion.")
        else:
            # Insert new customer into the database if not already present
            sql = "INSERT INTO customers (name, email) VALUES (%s, %s)"
            cursor.execute(sql, (name, email))
            connection.commit()
            print("Customer added to the database:", name, email)

            # Create the customer on Stripe
            stripe_customer = stripe.Customer.create(
                name=name,
                email=email
            )

            print(f"Customer created on Stripe with ID: {stripe_customer['id']}")

        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Error processing message: {e}")

# Set up RabbitMQ connection
connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='customer_queue')

# Consume the message from the queue
channel.basic_consume(queue='customer_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
