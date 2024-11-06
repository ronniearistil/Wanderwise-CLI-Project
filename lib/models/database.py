# database.py

import sqlite3

# Connect to SQLite database
CONN = sqlite3.connect('contracts.db')
CURSOR = CONN.cursor()

def initialize_database():
    """Create necessary tables in the database if they do not exist."""
    print("Initializing database...")

    # Create clients table
    CURSOR.execute('''CREATE TABLE IF NOT EXISTS clients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        contact_info TEXT,
                        address TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')
    print("Created clients table.")

    # Create contracts table
    CURSOR.execute('''CREATE TABLE IF NOT EXISTS contracts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_id INTEGER,
                        description TEXT,
                        start_date DATE,
                        end_date DATE,
                        amount REAL,
                        status TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(client_id) REFERENCES clients(id)
                    )''')
    print("Created contracts table.")

    # Create payments table
    CURSOR.execute('''CREATE TABLE IF NOT EXISTS payments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        contract_id INTEGER,
                        amount REAL,
                        payment_date DATE,
                        status TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(contract_id) REFERENCES contracts(id)
                    )''')
    print("Created payments table.")

    # Commit the changes to save the tables
    CONN.commit()
    print("Database initialized.")





