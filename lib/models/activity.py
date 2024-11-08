from lib.models.database import CURSOR, CONN  # Only import the database connection

class Activity:
    """Model for an activity associated with a destination."""

    @classmethod
    def create(cls, destination_id, name, date=None, time=None, cost=0, description=""):
        """
        Insert a new activity into the database.
        
        :param destination_id: ID of the destination associated with this activity.
        :param name: Name of the activity.
        :param date: Optional date of the activity.
        :param time: Optional time of the activity.
        :param cost: Cost of the activity (default is 0).
        :param description: Description of the activity.
        :return: ID of the newly inserted activity.
        """
        CURSOR.execute(
            "INSERT INTO activities (destination_id, name, date, time, cost, description) VALUES (?, ?, ?, ?, ?, ?)",
            (destination_id, name, date, time, cost, description)
        )
        CONN.commit()
        return CURSOR.lastrowid  # Return the ID of the newly inserted activity

    @classmethod
    def get_by_destination(cls, destination_id):
        """
        Retrieve all activities associated with a specific destination.
        
        :param destination_id: ID of the destination.
        :return: List of all activities for the given destination.
        """
        CURSOR.execute("SELECT * FROM activities WHERE destination_id = ?", (destination_id,))
        return CURSOR.fetchall()

