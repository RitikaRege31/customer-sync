
import json
import stripe
import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)


stripe.api_key = "sk_test_51QRVPRFNk3oYkWkNiZxiuYeeSRPAi0Rk2EoNzRNw6oztl03us0dlu04cktIuwCbvPgdAVyhNeBouVvLH421H1ZIg00yiY35uGX"

endpoint_secret = "whsec_12791d00b30f0a9afea1ada34cf57a3bed7751fcccbc88b1e7c691eaa3b6ea22"
# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ritika12@",
        database="customer_sync"
    )


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
