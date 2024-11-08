import sqlite3

# Connect to SQLite database
CONN = sqlite3.connect('wanderwise.db')
CURSOR = CONN.cursor()

def initialize_database():
    """Initialize the database with required tables and constraints if they don't exist."""
    
    # Create users table with UNIQUE email constraint
    CURSOR.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL CHECK(name <> ''),  -- Ensures name is not empty
                        email TEXT NOT NULL UNIQUE,            -- Email must be unique across users
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

    # Create destinations table with a NOT NULL foreign key and CHECK constraints
    CURSOR.execute('''CREATE TABLE IF NOT EXISTS destinations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,              -- Ensures a user is linked
                        name TEXT NOT NULL CHECK(name <> ''),   -- Destination name cannot be empty
                        location TEXT NOT NULL CHECK(location <> ''), -- Location cannot be empty
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE -- Deletes destination if the user is deleted
                    )''')

    # Create activities table with NOT NULL constraints, default values, and a CHECK on cost
    CURSOR.execute('''CREATE TABLE IF NOT EXISTS activities (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        destination_id INTEGER NOT NULL,       -- Ensures a destination is linked
                        name TEXT NOT NULL CHECK(name <> ''),   -- Activity name cannot be empty
                        date TEXT DEFAULT (date('now')),       -- Defaults to today's date if not provided
                        time TEXT,
                        cost REAL DEFAULT 0 CHECK(cost >= 0),  -- Cost must be non-negative
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(destination_id) REFERENCES destinations(id) ON DELETE CASCADE -- Deletes activity if the destination is deleted
                    )''')

    # Create expenses table with NOT NULL constraints, default values, and a CHECK on amount
    CURSOR.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        activity_id INTEGER NOT NULL,          -- Ensures an activity is linked
                        amount REAL NOT NULL CHECK(amount >= 0), -- Expense amount must be non-negative
                        description TEXT,
                        date TEXT DEFAULT (date('now')),       -- Defaults to today's date if not provided
                        category TEXT NOT NULL CHECK(category <> ''), -- Category cannot be empty
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(activity_id) REFERENCES activities(id) ON DELETE CASCADE -- Deletes expense if the activity is deleted
                    )''')

    # Commit all table creations to the database
    CONN.commit()
    print("Database initialized with constraints.")


















