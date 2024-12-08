
import pika
import json
import stripe
import mysql.connector
from flask import Flask, request, jsonify

# Set your Stripe secret key
stripe.api_key = "sk_test_51QRVPRFNk3oYkWkNiZxiuYeeSRPAi0Rk2EoNzRNw6oztl03us0dlu04cktIuwCbvPgdAVyhNeBouVvLH421H1ZIg00yiY35uGX"  # Replace with your Stripe test key

# Initialize Flask app
app = Flask(__name__)

def get_db_connection():
    """Establish a connection to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="Ritika12@",  
        database="customer_sync"
    )

def create_stripe_customer(name, email):
    """Create a customer in Stripe."""
    try:
        # Sync the customer to Stripe
        stripe_customer = stripe.Customer.create(
            name=name,
            email=email
        )
        print(f"Customer created on Stripe with ID: {stripe_customer['id']}")
        return stripe_customer
    except Exception as e:
        print(f"Error creating Stripe customer: {e}")
        return None

@app.route('/customers', methods=['GET', 'POST'])
def manage_customers():
    """Handle both GET and POST requests."""
    if request.method == 'POST':
        # Add a new customer to the database and sync to Stripe
        data = request.json
        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return jsonify({"error": "Name and email are required"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO customers (name, email) VALUES (%s, %s)", (name, email))
            connection.commit()

            # Now, create the customer on Stripe
            create_stripe_customer(name, email)

            return jsonify({"message": "Customer added successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        finally:
            connection.close()

    elif request.method == 'GET':
        # Retrieve all customers from the database
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM customers")
            customers = cursor.fetchall()

            # Convert the result to a list of dictionaries
            customer_list = [{"id": row[0], "name": row[1], "email": row[2]} for row in customers]

            return jsonify(customer_list), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        finally:
            connection.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
