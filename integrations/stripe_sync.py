# integrations/stripe_sync.py

import stripe
import mysql.connector

# Set your Stripe secret key
stripe.api_key = "sk_test_51QRVPRFNk3oYkWkNiZxiuYeeSRPAi0Rk2EoNzRNw6oztl03us0dlu04cktIuwCbvPgdAVyhNeBouVvLH421H1ZIg00yiY35uGX"  # Replace with your Stripe test key

# Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ritika12@",
        database="customer_sync"
    )

def sync_customers_to_stripe():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    for customer in customers:
        # Sync customer data to Stripe
        stripe.Customer.create(
            name=customer[1],
            email=customer[2]
        )

    connection.close()

if __name__ == "__main__":
    sync_customers_to_stripe()
