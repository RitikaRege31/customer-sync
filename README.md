
 
# Customer Sync Application

This project is a customer management system that integrates with the Stripe API for handling customer data. It includes features to create, retrieve, and synchronize customer data between a MySQL database and Stripe.

## Features

- Add new customers to a MySQL database and synchronize with Stripe.
- Retrieve all customer details from the database.
- Stripe webhook integration to handle real-time customer updates.
- MySQL database schema setup and management.
- Flask-based RESTful API for customer management.

---




## Prerequisites

- Python 3.8 or higher
- MySQL server installed and running
- Stripe API keys (Test and Webhook Secret)
- RabbitMQ (if planning for advanced queuing)
- Flask and required dependencies

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>


2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt



3. Configure MySQL
   Open the MySQL CLI or your preferred database management tool.
   Create the database:
   ```bash
   CREATE DATABASE customer_sync;
 Modify the MySQL connection settings in api/app.py and db/db_config.py as necessary:
   ```bash
   host="localhost"
   user="your_mysql_user"
   password="your_mysql_password"

4. Run Database Initialization
   Execute the database creation script:
   ```bash
   python db/create_db.py

5. Configure Stripe
   Replace the placeholder keys in the code with your Stripe API keys:
   In api/app.py, api/config.py, and integrations/stripe_webhook.py:
   ```python
   stripe.api_key = "your_stripe_secret_key"
   STRIPE_WEBHOOK_SECRET = "your_stripe_webhook_secret"


6. Start the Flask Application
   Run the API:
   ```bash
   python api/app.py
 The API will be accessible at http://127.0.0.1:5001

7. Verify Webhooks (Optional)
   To test Stripe webhooks locally, use the Stripe CLI:
   ```bash
   stripe listen --forward-to localhost:5001/webhook
 Update the webhook endpoint in Stripe's dashboard to match your live deployment URL.

API Endpoints
1. Add Customer
URL: /customers
Method: POST
Body:
{
  "name": "Customer Name",
  "email": "customer@example.com"
}
Response:
{
  "message": "Customer added successfully"
}

2. Retrieve Customers
URL: /customers
Method: GET
Response:
[
  {
    "id": 1,
    "name": "Customer Name",
    "email": "customer@example.com"
  }
]

3. Stripe Webhook
URL: /webhook
Method: POST
Body: Stripe webhook payload

Deployment Instructions
Local Deployment
Follow the installation steps to run the app locally.
Use a tool like Postman to interact with the API.

