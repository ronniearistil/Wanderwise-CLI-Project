from lib.models.database import CURSOR, CONN

class Expense:
    """Model for expenses associated with an activity."""

    def __init__(self, activity_id, amount, description=None, date=None, category="General"):
        self.activity_id = activity_id
        self.amount = amount
        self.description = description
        self.date = date
        self.category = category

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if value >= 0:
            self._amount = value
        else:
            raise ValueError("Amount must be non-negative.")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and value.strip():
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string.")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value if value else "No description provided."

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        # Here we assume the date is a valid date string in "YYYY-MM-DD" format
        self._date = value if value else "Today"

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








