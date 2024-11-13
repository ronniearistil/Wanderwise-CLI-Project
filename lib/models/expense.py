from lib.base_model import BaseModel

class Expense(BaseModel):
    """Model for an expense in the Wanderwise application."""

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
        cls.execute_create_table(cls.CREATE_TABLE_SQL)

    @classmethod
    def drop_table(cls):
        super().drop_table("expenses")

    @classmethod
    def create(cls, activity_id, amount, date, category, description=None):
        return super().create(
            "INSERT INTO expenses (activity_id, amount, date, category, description) VALUES (?, ?, ?, ?, ?)",
            (activity_id, amount, date, category, description)
        )

    @classmethod
    def get_all(cls):
        return super().get_all("SELECT * FROM expenses")

    @classmethod
    def get_by_activity(cls, activity_id):
        return cls.get_by_column("SELECT * FROM expenses WHERE activity_id = ?", activity_id)

    @classmethod
    def find_by_id(cls, expense_id):
        """Retrieve a specific expense by its ID."""
        return super().find_by_id("SELECT * FROM expenses WHERE id = ?", expense_id)

    @classmethod
    def update(cls, expense_id, **kwargs):
        columns = ', '.join([f"{k} = ?" for k in kwargs.keys()])
        params = tuple(kwargs.values()) + (expense_id,)
        return super().update(f"UPDATE expenses SET {columns} WHERE id = ?", params)

    @classmethod
    def delete(cls, expense_id):
        return super().delete("DELETE FROM expenses WHERE id = ?", expense_id)



'''Purpose: Manages expense-related data with CRUD functionality.
Connections: Extends base_model, with a foreign key link to Activity.'''



