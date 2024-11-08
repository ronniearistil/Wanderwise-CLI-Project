from lib.models.database import CURSOR, CONN

class Activity:
    """Model for an activity associated with a destination."""

    @classmethod
    def create(cls, destination_id, name, date=None, time=None, cost=0, description=""):
        """Insert a new activity into the database."""
        CURSOR.execute(
            "INSERT INTO activities (destination_id, name, date, time, cost, description) VALUES (?, ?, ?, ?, ?, ?)",
            (destination_id, name, date, time, cost, description)
        )
        CONN.commit()
        return CURSOR.lastrowid  # Return the ID of the newly inserted activity

    @classmethod
    def get_by_destination(cls, destination_id):
        """Retrieve all activities associated with a specific destination."""
        CURSOR.execute("SELECT * FROM activities WHERE destination_id = ?", (destination_id,))
        return CURSOR.fetchall()
