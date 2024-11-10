from lib.models.database import CURSOR, CONN

class Destination:
    """Model for a travel destination."""

    def __init__(self, name, location, description=None):
        self.name = name
        self.location = location
        self.description = description or ""

    @classmethod
    def create_table(cls, cursor):
        """Create the destinations table if it doesn't exist."""
        cursor.execute('''CREATE TABLE IF NOT EXISTS destinations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL CHECK(name <> ''),
                            location TEXT NOT NULL CHECK(location <> ''),
                            description TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            UNIQUE(name, location)
                        )''')

    @classmethod
    def drop_table(cls, cursor):
        """Drop the destinations table if it exists."""
        cursor.execute("DROP TABLE IF EXISTS destinations")

    @classmethod
    def create(cls, cursor, name, location, description):
        """Insert a new destination into the database."""
        cursor.execute("INSERT INTO destinations (name, location, description) VALUES (?, ?, ?)", 
                    (name, location, description))
        cursor.connection.commit()
        return cursor.lastrowid

    @classmethod
    def get_all(cls, cursor):
        """Retrieve all destinations from the database."""
        cursor.execute("SELECT * FROM destinations")
        return cursor.fetchall()





