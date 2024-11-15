from lib.models.__init__ import CURSOR, CONN
from lib.helpers import ValidatorMixin
from datetime import datetime


class Expense(ValidatorMixin):
    """Model for expenses associated with an activity."""

    def __init__(self, activity_id, amount, description=None, date=None, category="General", id=None):
        self.id = id
        self.activity_id = activity_id
        self.amount = amount  # Using property for validation
        self.description = self.validate_text(description or "No description provided.")
        self.date = self.validate_date(date or datetime.now().strftime("%m-%d-%Y"))
        self.category = category  # Using property for validation

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

    def activity(self):
        """Retrieve the activity linked to this expense from the database."""
        from lib.models.activity import Activity
        try:
            query = CURSOR.execute('SELECT * FROM activities WHERE id = ?', (self.activity_id,))
            data = query.fetchone()
            return Activity.instance_from_db(data) if data else None
        except Exception as e:
            CONN.rollback()
            print(f"Error retrieving activity for expense {self.id}: {e}")
            return None

    CREATE_TABLE_SQL = '''CREATE TABLE IF NOT EXISTS expenses (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            activity_id INTEGER NOT NULL,
                            amount REAL NOT NULL,
                            date TEXT NOT NULL,
                            category TEXT NOT NULL,
                            description TEXT,
                            FOREIGN KEY(activity_id) REFERENCES activities(id)
                        )'''

    @classmethod
    def create_table(cls):
        """Create the expenses table."""
        try:
            CURSOR.execute(cls.CREATE_TABLE_SQL)
            CONN.commit()
        except Exception as e:
            print(f"Error creating expenses table: {e}")

    @classmethod
    def drop_table(cls):
        """Drop the expenses table."""
        try:
            CURSOR.execute("DROP TABLE IF EXISTS expenses")
            CONN.commit()
        except Exception as e:
            print(f"Error dropping expenses table: {e}")

    @classmethod
    def create(cls, activity_id, amount, description=None, date=None, category="General"):
        """Create a new expense record and return an Expense object."""
        date = cls.validate_date(date or datetime.now().strftime("%m-%d-%Y"))
        try:
            amount = cls.validate_positive_number(float(amount))  # Ensure numeric type
            CURSOR.execute(
                "INSERT INTO expenses (activity_id, amount, description, date, category) VALUES (?, ?, ?, ?, ?)",
                (activity_id, amount, description, date, category)
            )
            CONN.commit()
            return cls(activity_id, amount, description, date, category, id=CURSOR.lastrowid)
        except Exception as e:
            CONN.rollback()
            print(f"Error creating expense: {e}")
            return None

    @classmethod
    def get_all(cls):
        """Retrieve all expenses as Expense objects."""
        try:
            CURSOR.execute("SELECT * FROM expenses")
            rows = CURSOR.fetchall()
            return [cls(row[1], row[2], row[3], row[4], row[5], row[0]) for row in rows]
        except Exception as e:
            print(f"Error retrieving all expenses: {e}")
            return []

    @classmethod
    def find_by_id(cls, expense_id):
        """Retrieve an expense by its ID and return an Expense object."""
        try:
            CURSOR.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
            row = CURSOR.fetchone()
            if row:
                return cls(row[1], row[2], row[3], row[4], row[5], row[0])
            return None
        except Exception as e:
            print(f"Error finding expense by ID: {e}")
            return None

    @classmethod
    def update(cls, expense_id, activity_id, amount, date, category, description):
        """Update an existing expense and return success status."""
        date = cls.validate_date(date)
        try:
            amount = cls.validate_positive_number(float(amount))  # Ensure numeric type
            CURSOR.execute(
                "UPDATE expenses SET activity_id = ?, amount = ?, date = ?, category = ?, description = ? WHERE id = ?",
                (activity_id, amount, date, category, description, expense_id)
            )
            CONN.commit()
            return CURSOR.rowcount > 0
        except Exception as e:
            CONN.rollback()
            print(f"Error updating expense: {e}")
            return False

    @classmethod
    def delete(cls, expense_id):
        """Delete an expense by ID and return success status."""
        try:
            CURSOR.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            CONN.commit()
            return CURSOR.rowcount > 0
        except Exception as e:
            CONN.rollback()
            print(f"Error deleting expense: {e}")
            return False

if __name__ == "__main__":
    # Example for testing
    expense = Expense(activity_id=1, amount=200, description="Test expense", date="01-01-2025", category="Travel")
    print(expense)



# Simple instance of Expense for testing
if __name__ == "__main__":
    expense1 = Expense(activity_id=1, amount=200, description="Lunch expense", date="12-01-2024", category="Food")
    ipdb.set_trace() 




