import mysql.connector
from mysql.connector import Error
import pandas as pd
import os

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'mag',
    'password': 'pass123',
    'database': 'testdb'
}

def create_connection():
    """Create a database connection to MySQL server."""
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        if connection.is_connected():
            print(f"Successfully connected to MySQL database: {DATABASE_CONFIG['database']}")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    

def create_db_structure(connection):
    try:
        cursor = connection.cursor()
        
        # Transaction Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaction (
            id INT AUTO_INCREMENT PRIMARY KEY,
            TotalPrice DECIMAL(10, 2),
            Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Type VARCHAR(50),
            PayMedium VARCHAR(50),
            Observations VARCHAR(255),
            ClientID INT,
            EmployeeID INT,
            FOREIGN KEY (ClientID) REFERENCES client(id),
            FOREIGN KEY (EmployeeID) REFERENCES employee(id)
        )
        """)

        # ProductTransaction Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS producttransaction (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ProductID INT,
                TransactionID INT,
                Quantity INT,
                Price DECIMAL(10, 2),
                FOREIGN KEY (ProductID) REFERENCES product(id),
                FOREIGN KEY (TransactionID) REFERENCES transaction(id)
            )
        """)

        # Product Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(100) NOT NULL
            )
        """)

        # ClientProvider Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientprovider (
                NIF VARCHAR(20) PRIMARY KEY,
                Name VARCHAR(100) NOT NULL,
                Address VARCHAR(255)
            )
        """)

        # Employee Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employee (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(100) NOT NULL,
            )
        """)

        connection.commit()
        print("Database structure created successfully.")

    except Error as e:
        print(f"Error creating database structure: {e}")



if __name__ == "__main__":
    conn = create_connection()
    if conn:
        create_db_structure(conn)
        conn.close()
