import unittest
from lib.models.user import User
from lib.models.destination import Destination
from lib.models.activity import Activity
from lib.models.expense import Expense
from lib.database_setup import reset_and_seed_database, CONN, CURSOR

class TestExpense(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        reset_and_seed_database()

    def setUp(self):
        # Clear all records for a clean test environment
        CURSOR.execute("DELETE FROM expenses")
        CURSOR.execute("DELETE FROM activities")
        CURSOR.execute("DELETE FROM destinations")
        CURSOR.execute("DELETE FROM users")
        CONN.commit()

        # Create a user, destination, and activity to link expenses to
        self.user_id = User.create("Alice Smith", "alice.smith@example.com")
        self.destination_id = Destination.create("Paris", "France", "City of Light", self.user_id)
        self.activity_id = Activity.create(self.destination_id, "Eiffel Tower Visit", "11-10-2024", "10:00", 50.0, "Guided tour")

    def test_create_expense(self):
        """Test creating an expense linked to an activity."""
        expense_id = Expense.create(self.activity_id, 100.0, "Ticket fee", "11-10-2024", "Entertainment")
        self.assertIsNotNone(expense_id, "Failed to create a new expense")

    def test_get_by_activity(self):
        """Test retrieving expenses associated with an activity."""
        Expense.create(self.activity_id, 50.0, "Metro fare", "11-10-2024", "Transport")
        Expense.create(self.activity_id, 30.0, "Lunch", "11-11-2024", "Food")
        expenses = Expense.get_by_activity(self.activity_id)
        self.assertEqual(len(expenses), 2, "Failed to retrieve all expenses for activity")

    def tearDown(self):
        """Clear data after each test to avoid conflicts."""
        CURSOR.execute("DELETE FROM expenses")
        CURSOR.execute("DELETE FROM activities")
        CURSOR.execute("DELETE FROM destinations")
        CURSOR.execute("DELETE FROM users")
        CONN.commit()

if __name__ == "__main__":
    unittest.main()

