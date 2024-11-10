# destination.py

from lib.models.database import CURSOR, CONN

class Destination:
    """Model for a travel destination."""

    @classmethod
    def create_table(cls, cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS destinations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL CHECK(name <> ''),
                            location TEXT NOT NULL CHECK(location <> ''),
                            description TEXT,
                            user_id INTEGER,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                        )''')

    @classmethod
    def drop_table(cls, cursor):
        cursor.execute("DROP TABLE IF EXISTS destinations")

    @classmethod
    def create(cls, cursor, name, location, description, user_id):
        """Insert a new destination into the database."""
        cursor.execute(
            "INSERT INTO destinations (name, location, description, user_id) VALUES (?, ?, ?, ?)",
            (name, location, description, user_id)
        )
        cursor.connection.commit()
        return cursor.lastrowid

    @classmethod
    def get_all(cls, cursor):
        """Retrieve all destinations from the database."""
        cursor.execute("SELECT * FROM destinations")
        return cursor.fetchall()






