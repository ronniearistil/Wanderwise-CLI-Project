# lib/models/database.py

import sqlite3

# Connect to SQLite database
CONN = sqlite3.connect('travel_tracker.db')
CURSOR = CONN.cursor()

def initialize_database():
    """Initialize the database with required tables if they don't exist."""
    
    # Create destinations table with description column
    CURSOR.execute('''CREATE TABLE IF NOT EXISTS destinations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        location TEXT NOT NULL,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

    # Create activities table with description column
    CURSOR.execute('''CREATE TABLE IF NOT EXISTS activities (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        destination_id INTEGER,
                        name TEXT NOT NULL,
                        date TEXT,
                        time TEXT,
                        cost REAL,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(destination_id) REFERENCES destinations(id)
                    )''')

    # Create expenses table with description column
    CURSOR.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        activity_id INTEGER,
                        amount REAL,
                        description TEXT,
                        date TEXT,
                        category TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(activity_id) REFERENCES activities(id)
                    )''')

    # Commit the changes to save the tables
    CONN.commit()
    print("Database initialized.")

# Call to initialize the database when the file is loaded
initialize_database()











