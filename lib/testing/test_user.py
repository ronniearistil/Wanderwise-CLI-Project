import unittest
from lib.models.user import User
from lib.models.database import CONN, CURSOR

class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Clear the users table before starting tests
        CURSOR.execute("DELETE FROM users")
        CONN.commit()

    def tearDown(self):
        # Clear data after each test to avoid conflicts
        CURSOR.execute("DELETE FROM users")
        CONN.commit()

    def test_create_user(self):
        user_id = User.create("Alice Smith", "alice.smith@example.com")
        self.assertIsNotNone(user_id, "Failed to create a new user")

    def test_get_all_users(self):
        User.create("Alice Smith", "alice.smith@example.com")
        User.create("Bob Johnson", "bob.johnson@example.com")
        users = User.get_all()
        self.assertEqual(len(users), 2, "Failed to retrieve all users")

    def test_update_user(self):
        user_id = User.create("Alice Smith", "alice.smith@example.com")
        updated = User.update(user_id, "Alice Johnson", "alice.johnson@example.com")
        self.assertTrue(updated, "Failed to update user")

        user = User.find_by_id(user_id)
        self.assertEqual(user[1], "Alice Johnson", "User name did not update correctly")

    def test_delete_user(self):
        user_id = User.create("Alice Smith", "alice.smith@example.com")
        deleted = User.delete(user_id)
        self.assertTrue(deleted, "Failed to delete user")

        user = User.find_by_id(user_id)
        self.assertIsNone(user, "User was not deleted properly")

if __name__ == "__main__":
    unittest.main()
