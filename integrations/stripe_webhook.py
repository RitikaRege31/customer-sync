# import sys
# import os

# # Add the project root directory to PYTHONPATH
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# # import sys
# # import os
# import json
# from flask import Flask, request, jsonify
# import stripe
# from db.db_config import get_db_connection
# import logging

# # Initialize logging
# logging.basicConfig(level=logging.DEBUG)

# app = Flask(__name__)

# # Set your Stripe secret keys
# stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_51QRVPRFNk3oYkWkNiZxiuYeeSRPAi0Rk2EoNzRNw6oztl03us0dlu04cktIuwCbvPgdAVyhNeBouVvLH421H1ZIg00yiY35uGX")
# STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_12791d00b30f0a9afea1ada34cf57a3bed7751fcccbc88b1e7c691eaa3b6ea22")

# @app.route('/webhook', methods=['POST'])
# def stripe_webhook():
#     """Handle incoming webhook events from Stripe."""
#     payload = request.get_data(as_text=True)
#     sig_header = request.headers.get('Stripe-Signature')

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, STRIPE_WEBHOOK_SECRET
#         )
#     except ValueError as e:
#         logging.error(f"Invalid payload: {e}")
#         return jsonify({'error': 'Invalid payload'}), 400
#     except stripe.error.SignatureVerificationError as e:
#         logging.error(f"Invalid signature: {e}")
#         return jsonify({'error': 'Invalid signature'}), 400

#     # Handle the event
#     logging.info(f"Received event: {event['type']}")
#     if event['type'] == 'customer.created':
#         customer_data = event['data']['object']
#         sync_customer_to_db(customer_data)

#     elif event['type'] == 'customer.updated':
#         customer_data = event['data']['object']
#         update_customer_in_db(customer_data)

#     elif event['type'] == 'customer.deleted':
#         customer_data = event['data']['object']
#         delete_customer_from_db(customer_data['id'])

#     return jsonify({'status': 'success'}), 200

# def sync_customer_to_db(customer_data):
#     """Insert a new customer into the database."""
#     connection = get_db_connection()
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "INSERT INTO customers (stripe_id, name, email) VALUES (%s, %s, %s)",
#                 (customer_data['id'], customer_data.get('name'), customer_data.get('email'))
#             )
#         connection.commit()
#     except Exception as e:
#         logging.error(f"Error inserting customer: {e}")
#     finally:
#         connection.close()

# def update_customer_in_db(customer_data):
#     """Update an existing customer in the database."""
#     connection = get_db_connection()
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "UPDATE customers SET name = %s, email = %s WHERE stripe_id = %s",
#                 (customer_data.get('name'), customer_data.get('email'), customer_data['id'])
#             )
#         connection.commit()
#     except Exception as e:
#         logging.error(f"Error updating customer: {e}")
#     finally:
#         connection.close()

# def delete_customer_from_db(stripe_id):
#     """Delete a customer from the database."""
#     connection = get_db_connection()
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("DELETE FROM customers WHERE stripe_id = %s", (stripe_id,))
#         connection.commit()
#     except Exception as e:
#         logging.error(f"Error deleting customer: {e}")
#     finally:
#         connection.close()

# if __name__ == "__main__":
#     app.run(port=5000)
import json
import stripe
import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace with your actual Stripe secret key
stripe.api_key = "sk_test_51QRVPRFNk3oYkWkNiZxiuYeeSRPAi0Rk2EoNzRNw6oztl03us0dlu04cktIuwCbvPgdAVyhNeBouVvLH421H1ZIg00yiY35uGX"

# Your webhook signing secret from the Stripe CLI output
endpoint_secret = "whsec_12791d00b30f0a9afea1ada34cf57a3bed7751fcccbc88b1e7c691eaa3b6ea22"
# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ritika12@",
        database="customer_sync"
    )

# @app.route('/webhook', methods=['GET','POST'])
# def stripe_webhook():
#     if request.method == 'GET':
#         return jsonify({"message": "Webhook is running!"}), 200
#     elif request.method == 'POST':
#         # Handle the Stripe webhook event
#         try:
#             payload = request.get_data(as_text=True)
#             event = json.loads(payload)
#             # Add your webhook handling logic here
#             event_type = event.get('type')
#             data_object = event.get('data', {}).get('object', {})
            
#             if event_type == 'customer.created':
#                 # Example: Log the created customer ID and email
#                 customer_id = data_object.get('id')
#                 email = data_object.get('email')
#                 name = data_object.get('name')

#                 connection = get_db_connection()
#                 cursor = connection.cursor()

#                 sql = "INSERT INTO customers (name, email) VALUES (%s, %s)"
#                 cursor.execute(sql, (name, email))
#                 connection.commit()

#                 cursor.close()
#                 connection.close()

#                 print(f"Customer created: {customer_id}, email: {email}")
            
#             return jsonify({"status": "success"}), 200
#         except Exception as e:
#             print(f"Error processing webhook: {e}")
#             return jsonify({"error": "Webhook handling failed"}), 400
@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    print("Received payload:")
    print(payload)  # Log the raw payload

    try:
        event = json.loads(payload)
        print("Parsed event:")
        print(json.dumps(event, indent=4))  # Log parsed event

        event_type = event.get('type')
        data_object = event.get('data', {}).get('object', {})

        print(f"Event type: {event_type}")
        print(f"Data object: {json.dumps(data_object, indent=4)}")

        if event_type == 'customer.created':
            # Extract customer details
            customer_id = data_object.get('id')
            email = data_object.get('email')
            name = data_object.get('name')

            print(f"Customer created: ID={customer_id}, Name={name}, Email={email}")

            # Insert into the database
            connection = get_db_connection()
            cursor = connection.cursor()
            sql = "INSERT INTO customers (name, email) VALUES (%s, %s)"
            cursor.execute(sql, (name, email))
            connection.commit()
            cursor.close()
            connection.close()

            print("Customer added to the database!")

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(port=5000)
