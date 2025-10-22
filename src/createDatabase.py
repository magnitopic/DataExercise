import mysql.connector
from mysql.connector import Error
import pandas as pd
import os

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
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
                Name VARCHAR(100) NOT NULL
            )
        """)

        # Product Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(100) NOT NULL
            )
        """)

        # Transaction Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaction (
            id INT AUTO_INCREMENT PRIMARY KEY,
            TotalPrice DECIMAL(10, 2),
            Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Type VARCHAR(50),
            PayMedium VARCHAR(50),
            Observations VARCHAR(255),
            ClientID VARCHAR(20),
            EmployeeID INT,
            FOREIGN KEY (ClientID) REFERENCES clientprovider(NIF),
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

        connection.commit()
        print("Database structure created successfully.")

    except Error as e:
        print(f"Error creating database structure: {e}")

def populate_tables(connection):
    try:
        pd.read_csv('exports/clients.csv').to_sql('clientprovider', con=connection, index=False)

        pd.read_csv('exports/employees.csv').to_sql('employee', con=connection, index=False)

        pd.read_csv('exports/product.csv').to_sql('product', con=connection, index=False)

        pd.read_csv('exports/transaction.csv').to_sql('transaction', con=connection, index=False)

        pd.read_csv('exports/ProductTransaction.csv').to_sql('producttransaction', con=connection, index=False)

    except Error as e:
        print(f"Error populating tables: {e}")

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        create_db_structure(conn)
        populate_tables(conn)
        conn.close()
