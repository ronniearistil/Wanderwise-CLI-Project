import unittest
import random
from lib.models.user import User
from lib.database_setup import reset_and_seed_database, CONN, CURSOR

class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Reset and seed the database at the start of tests
        reset_and_seed_database()

    def tearDown(self):
        """Clean up test data after each test."""
        # Clear tables with dependencies in the correct order
        CURSOR.execute("DELETE FROM expenses")
        CURSOR.execute("DELETE FROM activities")
        CURSOR.execute("DELETE FROM destinations")
        CURSOR.execute("DELETE FROM users")
        CONN.commit()

    def test_create_user(self):
        unique_email = f"alice.smith{random.randint(1, 1000)}@example.com"
        user_id = User.create("Alice Smith", unique_email)
        self.assertIsNotNone(user_id, "Failed to create a new user")

    def test_get_all_users(self):
        email1 = f"user1{random.randint(1, 1000)}@example.com"
        email2 = f"user2{random.randint(1, 1000)}@example.com"
        
        User.create("Alice Smith", email1)
        User.create("Bob Johnson", email2)
        
        users = User.get_all()
        self.assertGreaterEqual(len(users), 2, "Failed to retrieve all users")

if __name__ == "__main__":
    unittest.main()


