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

    @classmethod
    def find_by_id(cls, expense_id):
        """Retrieve a specific expense by its ID."""
        CURSOR.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        return CURSOR.fetchone()

    @classmethod
    def update(cls, expense_id, activity_id, amount, date, category, description):
        """Update an existing expense in the database."""
        CURSOR.execute(
            """
            UPDATE expenses 
            SET activity_id = ?, amount = ?, date = ?, category = ?, description = ?
            WHERE id = ?
            """,
            (activity_id, amount, date, category, description, expense_id)
        )
        CONN.commit()
        return CURSOR.rowcount > 0  # Returns True if the update was successful

    @classmethod
    def delete(cls, expense_id):
        """Delete an expense from the database by its ID."""
        CURSOR.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        CONN.commit()
        return CURSOR.rowcount > 0  # Returns True if the deletion was successful








