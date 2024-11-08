import sqlite3

# Connect to SQLite database
CONN = sqlite3.connect('wanderwise.db')
CURSOR = CONN.cursor()

def initialize_database():
    """Initialize the database with required tables and constraints if they don't exist."""
    
    # Create users table with UNIQUE email constraint
    CURSOR.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL CHECK(name <> ''),
                        email TEXT NOT NULL UNIQUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

    # Create destinations table with UNIQUE name-location constraint
    CURSOR.execute('''CREATE TABLE IF NOT EXISTS destinations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL CHECK(name <> ''),
                        location TEXT NOT NULL CHECK(location <> ''),
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(name, location)  -- Ensure each name-location pair is unique
                    )''')

    # Create activities table with NOT NULL constraints and a CHECK on cost
    CURSOR.execute('''CREATE TABLE IF NOT EXISTS activities (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        destination_id INTEGER NOT NULL,
                        name TEXT NOT NULL CHECK(name <> ''),
                        date TEXT DEFAULT (date('now')),
                        time TEXT,
                        cost REAL DEFAULT 0 CHECK(cost >= 0),
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(destination_id) REFERENCES destinations(id) ON DELETE CASCADE
                    )''')

    # Create expenses table with NOT NULL constraints and a CHECK on amount
    CURSOR.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        activity_id INTEGER NOT NULL,
                        amount REAL NOT NULL CHECK(amount >= 0),
                        description TEXT,
                        date TEXT DEFAULT (date('now')),
                        category TEXT NOT NULL CHECK(category <> ''),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(activity_id) REFERENCES activities(id) ON DELETE CASCADE
                    )''')

    # Commit all table creations to the database
    CONN.commit()
    print("Database initialized with constraints.")



















