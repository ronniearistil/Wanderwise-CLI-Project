from lib.models.database import CURSOR, CONN
from lib.helpers import ValidatorMixin
from datetime import datetime

class Expense(ValidatorMixin):
    """Model for expenses associated with an activity."""

    def __init__(self, activity_id, amount, description=None, date=None, category="General"):
        self.activity_id = activity_id
        self.amount = self.validate_positive_number(amount)
        self.description = self.validate_text(description or "No description provided.")
        self.date = self.validate_date(date or datetime.now().strftime("%m-%d-%Y"))
        self.category = self.validate_text(category)

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
        date = cls.validate_date(date or datetime.now().strftime("%m-%d-%Y"))
        cursor.execute(
            "INSERT INTO expenses (activity_id, amount, description, date, category) VALUES (?, ?, ?, ?, ?)",
            (activity_id, amount, description, date, category)
        )
        cursor.connection.commit()
        return cursor.lastrowid

    @classmethod
    def get_all(cls, cursor):
        cursor.execute("SELECT * FROM expenses")
        return cursor.fetchall()

    @classmethod
    def get_by_activity(cls, cursor, activity_id):
        """Retrieve all expenses associated with a specific activity ID."""
        cursor.execute("SELECT * FROM expenses WHERE activity_id = ?", (activity_id,))
        return cursor.fetchall()

    @classmethod
    def update(cls, cursor, expense_id, activity_id, amount, date, category, description):
        date = cls.validate_date(date)
        cursor.execute(
            "UPDATE expenses SET activity_id = ?, amount = ?, date = ?, category = ?, description = ? WHERE id = ?",
            (activity_id, amount, date, category, description, expense_id)
        )
        cursor.connection.commit()
        return cursor.rowcount > 0

    @classmethod
    def delete(cls, cursor, expense_id):
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        cursor.connection.commit()
        return cursor.rowcount > 0




