# testing/test_expense.py

import unittest
from lib.models.user import User
from lib.models.destination import Destination
from lib.models.activity import Activity
from lib.models.expense import Expense
from lib.models.database import CURSOR, CONN

class TestExpense(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the database schema before running any tests."""
        # Clear tables and recreate them to ensure a clean state
        Expense.drop_table(CURSOR)
        Activity.drop_table(CURSOR)
        Destination.drop_table(CURSOR)
        User.drop_table(CURSOR)
        
        User.create_table(CURSOR)
        Destination.create_table(CURSOR)
        Activity.create_table(CURSOR)
        Expense.create_table(CURSOR)
    
    def setUp(self):
        """Set up required entries in the database for expense tests."""
        # Clear all records to ensure no unique constraint issues
        CURSOR.execute("DELETE FROM expenses")
        CURSOR.execute("DELETE FROM activities")
        CURSOR.execute("DELETE FROM destinations")
        CURSOR.execute("DELETE FROM users")
        CONN.commit()
        
        # Create a user, destination, and activity to link expenses to
        self.user_id = User.create(CURSOR, "Alice Smith", "alice.smith@example.com")
        self.destination_id = Destination.create(CURSOR, "Paris", "France", "City of Light", self.user_id)
        self.activity_id = Activity.create(CURSOR, self.destination_id, "Eiffel Tower Visit", "11-10-2024", "10:00", 50.0, "Guided tour")

    def test_create_expense(self):
        """Test creating an expense linked to an activity."""
        expense_id = Expense.create(CURSOR, self.activity_id, 100.0, "Ticket fee", "11-10-2024", "Entertainment")
        self.assertIsNotNone(expense_id, "Failed to create a new expense")

    def test_get_by_activity(self):
        """Test retrieving expenses associated with an activity."""
        Expense.create(CURSOR, self.activity_id, 50.0, "Metro fare", "11-10-2024", "Transport")
        Expense.create(CURSOR, self.activity_id, 30.0, "Lunch", "11-11-2024", "Food")
        expenses = Expense.get_by_activity(CURSOR, self.activity_id)
        self.assertEqual(len(expenses), 2, "Failed to retrieve all expenses for activity")

    def tearDown(self):
        """Clear data after each test to avoid conflicts."""
        CURSOR.execute("DELETE FROM expenses")
        CURSOR.execute("DELETE FROM activities")
        CURSOR.execute("DELETE FROM destinations")
        CURSOR.execute("DELETE FROM users")
        CONN.commit()

    @classmethod
    def tearDownClass(cls):
        """Tear down the database schema after all tests have completed."""
        Expense.drop_table(CURSOR)
        Activity.drop_table(CURSOR)
        Destination.drop_table(CURSOR)
        User.drop_table(CURSOR)
        CONN.commit()

if __name__ == "__main__":
    unittest.main()

