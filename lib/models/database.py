import sqlite3

# Connect to SQLite database
CONN = sqlite3.connect('wanderwise.db')
CURSOR = CONN.cursor()

def initialize_database():
    """Initialize the database with required tables if they don't exist."""
    
    # Create users table
    CURSOR.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

    # Create destinations table
    CURSOR.execute('''CREATE TABLE IF NOT EXISTS destinations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        name TEXT NOT NULL,
                        location TEXT NOT NULL,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )''')

    # Create activities table
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

    # Create expenses table
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
    CONN.commit()
    print("Database initialized.")

















