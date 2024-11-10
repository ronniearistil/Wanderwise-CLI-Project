import unittest
from lib.models.user import User
from lib.models.database import CURSOR, CONN

class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        User.create_table(CURSOR)

    @classmethod
    def tearDownClass(cls):
        User.drop_table(CURSOR)

    def tearDown(self):
        """Clean up test data after each test."""
        CURSOR.execute("DELETE FROM users")
        CONN.commit()

    def test_create_user(self):
        user_id = User.create(CURSOR, "Alice Smith", "alice.smith@example.com")
        self.assertIsNotNone(user_id, "Failed to create a new user")

    def test_get_all_users(self):
        User.create(CURSOR, "Alice Smith", "alice.smith@example.com")
        User.create(CURSOR, "Bob Johnson", "bob.johnson@example.com")
        users = User.get_all(CURSOR)
        self.assertEqual(len(users), 2, "Failed to retrieve all users")
