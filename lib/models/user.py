from lib.models.database import CURSOR, CONN

class User:
    """Model for a user in the Wanderwise application."""
    
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @classmethod
    def create(cls, name, email):
        CURSOR.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        CONN.commit()
        return CURSOR.lastrowid

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM users")
        return CURSOR.fetchall()

