# api/app.py
import sys
import os

# Add the project root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify
# from db.db_config import get_db_connection
from queue_service.producer import send_to_queue
# db/db_config.py

import mysql.connector

def get_db_connection():
    """Establish a connection to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="Ritika12@",  
        database="customer_sync"
    )

app = Flask(__name__)

# @app.route('/customers', methods=['POST'])
# def add_customer():
#     """Add a new customer to the database and push it to the queue."""
#     data = request.json
#     name = data.get('name')
#     email = data.get('email')

#     connection = get_db_connection()
#     cursor = connection.cursor()

#     try:
#         cursor.execute("INSERT INTO customers (name, email) VALUES (%s, %s)", (name, email))
#         connection.commit()

#         # Add the customer to RabbitMQ queue
#         send_to_queue(data)

#         return jsonify({"message": "Customer added successfully"}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400
#     finally:
#         connection.close()
@app.route('/customers', methods=['GET', 'POST'])
def manage_customers():
    """Handle both GET and POST requests."""
    if request.method == 'POST':
        # Add a new customer to the database and push to the queue
        data = request.json
        name = data.get('name')
        email = data.get('email')

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO customers (name, email) VALUES (%s, %s)", (name, email))
            connection.commit()

            # Add the customer to RabbitMQ queue
            send_to_queue(data)

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
