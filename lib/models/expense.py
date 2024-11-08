from lib.models.database import CURSOR, CONN

class Expense:
    """Model for expenses associated with an activity."""

    @classmethod
    def create(cls, activity_id, amount, description=None, date=None, category="General"):
        """Add a new expense to the database and return the new expense ID."""
        CURSOR.execute(
            "INSERT INTO expenses (activity_id, amount, description, date, category) VALUES (?, ?, ?, ?, ?)",
            (activity_id, amount, description, date, category)
        )
        CONN.commit()
        return CURSOR.lastrowid

    @classmethod
    def get_by_activity(cls, activity_id):
        """Retrieve all expenses associated with a specific activity."""
        CURSOR.execute("SELECT * FROM expenses WHERE activity_id = ?", (activity_id,))
        return CURSOR.fetchall()




