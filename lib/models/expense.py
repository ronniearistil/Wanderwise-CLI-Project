from lib.models.__init__ import CURSOR, CONN
from lib.helpers import ValidatorMixin
from datetime import datetime

class Expense(ValidatorMixin):
    """Model for expenses associated with an activity."""

    def __init__(self, activity_id, amount, description=None, date=None, category="General", id=None):
        self.id = id
        self.activity_id = activity_id
        self.amount = amount
        self.description = self.validate_text(description or "No description provided.")
        self.date = self.validate_date(date or datetime.now().strftime("%m-%d-%Y"))
        self.category = category

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = self.validate_positive_number(value)

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = self.validate_text(value)

    @classmethod
    def create_table(cls, cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            activity_id INTEGER NOT NULL,
                            amount REAL NOT NULL CHECK(amount >= 0),
                            description TEXT,
                            date TEXT DEFAULT (date('now')),
                            category TEXT NOT NULL CHECK(category <> ''),
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY(activity_id) REFERENCES activities(id) ON DELETE CASCADE
                        )''')

    @classmethod
    def drop_table(cls, cursor):
        cursor.execute("DROP TABLE IF EXISTS expenses")

    @classmethod
    def create(cls, cursor, activity_id, amount, description=None, date=None, category="General"):
        """Create a new expense record and return an Expense object."""
        date = cls.validate_date(date or datetime.now().strftime("%m-%d-%Y"))
        try:
            cursor.execute(
                "INSERT INTO expenses (activity_id, amount, description, date, category) VALUES (?, ?, ?, ?, ?)",
                (activity_id, amount, description, date, category)
            )
            cursor.connection.commit()
            return cls(activity_id, amount, description, date, category, id=cursor.lastrowid)
        except Exception as e:
            cursor.connection.rollback()
            print(f"Error creating expense: {e}")
            return None

    @classmethod
    def get_all(cls, cursor):
        """Retrieve all expenses as Expense objects."""
        cursor.execute("SELECT * FROM expenses")
        rows = cursor.fetchall()
        return [cls(row[1], row[2], row[3], row[4], row[5], row[0]) for row in rows]

    @classmethod
    def get_by_activity(cls, cursor, activity_id):
        """Retrieve all expenses associated with a specific activity ID as Expense objects."""
        cursor.execute("SELECT * FROM expenses WHERE activity_id = ?", (activity_id,))
        rows = cursor.fetchall()
        return [cls(row[1], row[2], row[3], row[4], row[5], row[0]) for row in rows]

    @classmethod
    def find_by_id(cls, cursor, expense_id):
        """Retrieve an expense by its ID and return an Expense object."""
        cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        row = cursor.fetchone()
        if row:
            return cls(row[1], row[2], row[3], row[4], row[5], row[0])
        return None

    @classmethod
    def update(cls, cursor, expense_id, activity_id, amount, date, category, description):
        """Update an existing expense and return success status."""
        date = cls.validate_date(date)
        try:
            cursor.execute(
                "UPDATE expenses SET activity_id = ?, amount = ?, date = ?, category = ?, description = ? WHERE id = ?",
                (activity_id, amount, date, category, description, expense_id)
            )
            cursor.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            cursor.connection.rollback()
            print(f"Error updating expense: {e}")
            return False

    @classmethod
    def delete(cls, cursor, expense_id):
        """Delete an expense by ID and return success status."""
        try:
            cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            cursor.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            cursor.connection.rollback()
            print(f"Error deleting expense: {e}")
            return False