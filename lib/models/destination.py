from lib.models.database import CURSOR, CONN

class Destination:
    """Model for a travel destination."""

    @classmethod
    def create(cls, name, location, description, user_id):
        """Insert a new destination into the database."""
        CURSOR.execute(
            "INSERT INTO destinations (name, location, description, user_id) VALUES (?, ?, ?, ?)", 
            (name, location, description, user_id)
        )
        CONN.commit()
        return CURSOR.lastrowid  # Return the ID of the newly inserted destination

    @classmethod
    def get_all(cls):
        """Retrieve all destinations from the database."""
        CURSOR.execute("SELECT * FROM destinations")
        return CURSOR.fetchall()




