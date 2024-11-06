# lib/models/destination.py
from lib.models.database import CURSOR, CONN

class Destination:
    """Model for a travel destination."""

    @classmethod
    def create(cls, name, country, description):
        CURSOR.execute("INSERT INTO destinations (name, country, description) VALUES (?, ?, ?)", 
        (name, country, description))
        CONN.commit()
        # Return the ID of the newly inserted destination
        return CURSOR.lastrowid

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM destinations")
        return CURSOR.fetchall()








