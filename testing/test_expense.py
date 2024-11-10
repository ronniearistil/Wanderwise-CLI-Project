import unittest
from lib.models.expense import Expense
from lib.models.activity import Activity
from lib.models.destination import Destination
from lib.models.user import User
from lib.models.database import CURSOR, CONN

class TestExpense(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the tables for all models before any tests run
        User.create_table(CURSOR)
        Destination.create_table(CURSOR)
        Activity.create_table(CURSOR)
        Expense.create_table(CURSOR)

    @classmethod
    def tearDownClass(cls):
        # Drop tables after all tests in this class have run
        Expense.drop_table(CURSOR)
        Activity.drop_table(CURSOR)
        Destination.drop_table(CURSOR)
        User.drop_table(CURSOR)

    def tearDown(self):
        """Clear all relevant tables after each test to ensure no leftover data."""
        CURSOR.execute("DELETE FROM expenses")
        CURSOR.execute("DELETE FROM activities")
        CURSOR.execute("DELETE FROM destinations")
        CURSOR.execute("DELETE FROM users")
        CONN.commit()

    def setUp(self):
        """Set up required entries in the database for expense tests."""
        # Create user, destination, and activity for use in expense tests
        self.user_id = User.create(CURSOR, "Alice Smith", "alice.smith@example.com")
        self.destination_id = Destination.create(CURSOR, "Paris", "France", "City of Light")
        self.activity_id = Activity.create(CURSOR, self.destination_id, "Eiffel Tower Visit", "2023-11-10", "10:00", 50.0)

    def test_create_expense(self):
        """Test creating an expense linked to an activity."""
        expense_id = Expense.create(CURSOR, self.activity_id, 100.0, "Ticket fee")
        self.assertIsNotNone(expense_id, "Failed to create a new expense")

    def test_get_by_activity(self):
        """Test retrieving expenses associated with an activity."""
        Expense.create(CURSOR, self.activity_id, 50.0, "Metro fare")
        Expense.create(CURSOR, self.activity_id, 30.0, "Lunch")
        expenses = Expense.get_by_activity(CURSOR, self.activity_id)
        self.assertEqual(len(expenses), 2, "Failed to retrieve all expenses for activity")
