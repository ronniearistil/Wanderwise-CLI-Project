import unittest
from lib.models.activity import Activity
from lib.models.destination import Destination
from lib.models.user import User
from lib.models.expense import Expense
from lib.models.database import CONN, CURSOR

class TestExpense(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Clear tables before starting tests
        CURSOR.execute("DELETE FROM expenses")
        CURSOR.execute("DELETE FROM activities")
        CURSOR.execute("DELETE FROM destinations")
        CURSOR.execute("DELETE FROM users")
        CONN.commit()

    def setUp(self):
        # Add a user, destination, and activity to link expenses to
        self.user_id = User.create("Alice Smith", "alice.smith@example.com")
        self.destination_id = Destination.create("Paris", "France", "City of Light", self.user_id)
        self.activity_id = Activity.create(self.destination_id, "Eiffel Tower Visit", "2023-11-10", "10:00", 50.0, "Guided tour")

    def tearDown(self):
        # Clear data after each test
        CURSOR.execute("DELETE FROM expenses")
        CURSOR.execute("DELETE FROM activities")
        CURSOR.execute("DELETE FROM destinations")
        CURSOR.execute("DELETE FROM users")
        CONN.commit()

    def test_create_expense(self):
        expense_id = Expense.create(self.activity_id, 100.0, "2023-11-10", "Travel", "Ticket fee")
        self.assertIsNotNone(expense_id, "Failed to create a new expense")

    def test_get_by_activity(self):
        Expense.create(self.activity_id, 50.0, "2023-11-10", "Travel", "Metro fare")
        Expense.create(self.activity_id, 30.0, "2023-11-11", "Food", "Lunch")
        expenses = Expense.get_by_activity(self.activity_id)
        self.assertEqual(len(expenses), 2, "Failed to retrieve all expenses for activity")

    def test_update_expense(self):
        expense_id = Expense.create(self.activity_id, 100.0, "2023-11-10", "Travel", "Ticket fee")
        updated = Expense.update(expense_id, self.activity_id, 120.0, "2023-11-12", "Entertainment", "Evening event")
        self.assertTrue(updated, "Failed to update expense")

        expense = Expense.find_by_id(expense_id)
        self.assertEqual(expense[4], "Evening event", "Expense description did not update correctly")

    def test_delete_expense(self):
        expense_id = Expense.create(self.activity_id, 100.0, "2023-11-10", "Travel", "Ticket fee")
        deleted = Expense.delete(expense_id)
        self.assertTrue(deleted, "Failed to delete expense")

        expense = Expense.find_by_id(expense_id)
        self.assertIsNone(expense, "Expense was not deleted properly")

if __name__ == "__main__":
    unittest.main()
