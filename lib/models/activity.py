# lib/models/activity.py
from lib.models.database import CURSOR, CONN

class Activity:
    """Model for an activity associated with a destination."""

    @classmethod
    def create(cls, destination_id, name, date=None, time=None, cost=0, description=""):
        CURSOR.execute(
            "INSERT INTO activities (destination_id, name, date, time, cost, description) VALUES (?, ?, ?, ?, ?, ?)",
            (destination_id, name, date, time, cost, description)
        )
        CONN.commit()
        return CURSOR.lastrowid

    @classmethod
    def get_by_destination(cls, destination_id):
        CURSOR.execute("SELECT * FROM activities WHERE destination_id = ?", (destination_id,))
        return CURSOR.fetchall()




