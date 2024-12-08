# db/create_db.py

import mysql.connector

def create_database():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",  
        password="Ritika12@"  
    )
    cursor = connection.cursor()

    # Create database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS customer_sync")
    connection.close()

def create_table():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",  
        password="Ritika12@",  
        database="customer_sync"
    )
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE
        )
    """)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_database()
    create_table()
