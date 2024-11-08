from lib.models.database import CURSOR, CONN

class Expense:
    """Model for expenses associated with an activity."""

    @classmethod
    def create(cls, activity_id, amount, description=None, date=None, category="General"):
        """
        Add a new expense to the database.
        
        :param activity_id: The ID of the activity associated with this expense.
        :param amount: The amount of the expense.
        :param description: Optional description of the expense.
        :param date: Optional date of the expense.
        :param category: Category of the expense (default is "General").
        :return: The ID of the newly created expense.
        """
        CURSOR.execute(
            "INSERT INTO expenses (activity_id, amount, description, date, category) VALUES (?, ?, ?, ?, ?)",
            (activity_id, amount, description, date, category)
        )
        CONN.commit()
        return CURSOR.lastrowid

    @classmethod
    def get_by_activity(cls, activity_id):
        """
        Retrieve all expenses associated with a specific activity.
        
        :param activity_id: The ID of the activity.
        :return: A list of expenses as tuples.
        """
        CURSOR.execute("SELECT * FROM expenses WHERE activity_id = ?", (activity_id,))
        return CURSOR.fetchall()

    @classmethod
    def find_by_id(cls, expense_id):
        """
        Find an expense by its ID.
        
        :param expense_id: The ID of the expense to retrieve.
        :return: The expense record as a tuple if found, otherwise None.
        """
        CURSOR.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        return CURSOR.fetchone()

    @classmethod
    def update(cls, expense_id, activity_id, amount, date, category, description=None):
        """
        Update an existing expense in the database.
        
        :param expense_id: The ID of the expense to update.
        :param activity_id: The ID of the associated activity.
        :param amount: The updated amount of the expense.
        :param date: The updated date of the expense.
        :param category: The updated category of the expense.
        :param description: The updated description of the expense.
        :return: True if the expense was updated, False otherwise.
        """
        CURSOR.execute(
            "UPDATE expenses SET activity_id = ?, amount = ?, date = ?, category = ?, description = ? WHERE id = ?",
            (activity_id, amount, date, category, description, expense_id)
        )
        CONN.commit()
        return CURSOR.rowcount > 0

    @classmethod
    def delete(cls, expense_id):
        """
        Delete an expense from the database by its ID.
        
        :param expense_id: The ID of the expense to delete.
        :return: True if the expense was deleted, False otherwise.
        """
        CURSOR.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        CONN.commit()
        return CURSOR.rowcount > 0







