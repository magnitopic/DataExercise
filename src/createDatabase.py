import mysql.connector
from mysql.connector import Error
import csv

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
            Document VARCHAR(100),
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
    finally:
        cursor.close()


def populate_tables(connection):
    try:
        cursor = connection.cursor()
        
        # Populate ClientProvider
        with open('exports/clients.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                cursor.execute(
                    "INSERT INTO clientprovider (NIF, Name, Address) VALUES (%s, %s, %s)",
                    (row['NIF'], row['Name'], row['Address'])
                )
        connection.commit()
        print("ClientProvider data loaded.")
        
        # Populate Employee
        with open('exports/employees.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                cursor.execute(
                    "INSERT INTO employee (id, Name) VALUES (%s, %s)",
                    (row['id'], row['Name'])
                )
        connection.commit()
        print("Employee data loaded.")
        
        # Populate Product
        with open('exports/product.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                cursor.execute(
                    "INSERT INTO product (id, Name) VALUES (%s, %s)",
                    (row['id'], row['Name'])
                )
        connection.commit()
        print("Product data loaded.")
        
        # Populate Transaction
        with open('exports/transaction.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                cursor.execute(
                    """INSERT INTO transaction 
                    (id, TotalPrice, Date, Type, PayMedium, Observations, Document, ClientID, EmployeeID) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (row['id'], row['TotalPrice'], row['Date'], row['Type'], row['PayMedium'],
                     row['Observations'], row['Document'], row['ClientID'], row['EmployeeID'])
                )
        connection.commit()
        print("Transaction data loaded.")

        # Populate ProductTransaction
        with open('exports/ProductTransaction.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                cursor.execute(
                    """INSERT INTO producttransaction 
                    (TransactionID, Quantity, Price, ProductID, id) 
                    VALUES (%s, %s, %s, %s, %s)""",
                    (row['TransactionID'], row['Quantity'], row['Price'], row['ProductID'], row['id'])
                )
        print("ProductTransaction data loaded.")
        
        connection.commit()
        print("All data committed successfully.")
        
    except Error as e:
        connection.rollback()
        print(f"Error populating tables: {e}")
    finally:
        cursor.close()

def drop_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("DROP DATABASE IF EXISTS testdb")
        connection.commit()
        print("Database dropped successfully.")
        # Recreate the database
        cursor.execute("CREATE DATABASE testdb")
        cursor.execute("USE testdb")
        connection.commit()
        print("Database recreated successfully.")
    except Error as e:
        print(f"Error dropping database: {e}")
    finally:
        cursor.close()

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        drop_database(conn)
        create_db_structure(conn)
        populate_tables(conn)
        conn.close()
