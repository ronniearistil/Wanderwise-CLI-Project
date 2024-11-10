from lib.models.database import CURSOR, CONN

class Expense:
    """Model for expenses associated with an activity."""

    def __init__(self, activity_id, amount, description=None, date=None, category="General"):
        self.activity_id = activity_id
        self.amount = amount
        self.description = description or "No description provided."
        self.date = date or "Today"
        self.category = category

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
        """Retrieve all expenses associated with a specific activity as a list of dictionaries."""
        CURSOR.execute("SELECT * FROM expenses WHERE activity_id = ?", (activity_id,))
        rows = CURSOR.fetchall()
        return [
            {
                "id": row[0],
                "activity_id": row[1],
                "amount": row[2],
                "description": row[3],
                "date": row[4],
                "category": row[5],
                "created_at": row[6]
            } for row in rows
        ]

    @classmethod
    def find_by_id(cls, expense_id):
        """Retrieve a specific expense by its ID as a dictionary."""
        CURSOR.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        row = CURSOR.fetchone()
        if row:
            return {
                "id": row[0],
                "activity_id": row[1],
                "amount": row[2],
                "description": row[3],
                "date": row[4],
                "category": row[5],
                "created_at": row[6]
            }
        return None

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









