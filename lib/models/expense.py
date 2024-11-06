# lib/models/expense.py

from lib.models.database import CURSOR, CONN

class Expense:
    """Model for expenses associated with an activity."""

    @classmethod
    def create(cls, activity_id, amount, date, category, description=None):
        """Add a new expense to the database and return an instance of Expense."""
        CURSOR.execute(
            "INSERT INTO expenses (activity_id, amount, date, category, description) VALUES (?, ?, ?, ?, ?)",
            (activity_id, amount, date, category, description)
        )
        CONN.commit()
        return CURSOR.lastrowid  # Return the ID of the new expense

    @classmethod
    def get_by_activity(cls, activity_id):
        """Retrieve all expenses associated with a specific activity."""
        CURSOR.execute("SELECT * FROM expenses WHERE activity_id = ?", (activity_id,))
        return CURSOR.fetchall()






