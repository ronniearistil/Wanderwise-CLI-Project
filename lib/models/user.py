from lib.models.__init__ import CURSOR, CONN
from datetime import datetime


class User:
    """Model for a user in the Wanderwise application."""

    def __init__(self, name, email, created_at=None, id=None):
        self.name = name  # Automatically validated by the setter
        self.email = email  # Automatically validated by the setter
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        """Validate and set the name."""
        if isinstance(value, str) and value.strip():
            self._name = value.strip()
        else:
            raise ValueError("Name must be a non-empty string.")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        """Validate and set the email."""
        if isinstance(value, str) and "@" in value and "." in value:
            self._email = value.strip()
        else:
            raise ValueError("Invalid email format.")

    def destinations(self):
        """Select all destinations associated with this user."""
        from lib.models.destination import Destination
        try:
            query = CURSOR.execute('SELECT * FROM destinations WHERE user_id = ?', (self.id,))
            data = query.fetchall()
            return [Destination.instance_from_db(row) for row in data]
        except Exception as e:
            CONN.rollback()  # Rollback if any error occurs
            print(f"Error retrieving destinations for user {self.id}: {e}")
            return []

    @classmethod
    def create_table(cls):
        try:
            CURSOR.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL CHECK(name <> ''),
                                email TEXT NOT NULL UNIQUE,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )''')
        except Exception as e:
            CONN.rollback()
            print(f"Error creating users table: {e}")

    @classmethod
    def drop_table(cls):
        try:
            CURSOR.execute("DROP TABLE IF EXISTS users")
        except Exception as e:
            CONN.rollback()
            print(f"Error dropping users table: {e}")

    @classmethod
    def create(cls, name, email):
        """Create a new user entry in the database and return the User object."""
        try:
            sql = "INSERT INTO users (name, email) VALUES (?, ?)"
            CURSOR.execute(sql, (name, email))
            CONN.commit()
            user_id = CURSOR.lastrowid
            return cls(name, email, id=user_id)
        except Exception as e:
            CONN.rollback()
            print("Error creating user:", e)
            return None

    @classmethod
    def get_all(cls):
        try:
            CURSOR.execute("SELECT * FROM users")
            data = CURSOR.fetchall()
            return [cls(row[1], row[2], row[3], row[0]) for row in data]
        except Exception as e:
            print(f"Error retrieving users: {e}")
            return []

    @classmethod
    def find_by_id(cls, user_id):
        try:
            CURSOR.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            data = CURSOR.fetchone()
            return cls(data[1], data[2], data[3], data[0]) if data else None
        except Exception as e:
            print(f"Error finding user by ID: {e}")
            return None

    @classmethod
    def update(cls, user_id, name, email):
        try:
            CURSOR.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
            CONN.commit()
            return CURSOR.rowcount > 0
        except Exception as e:
            CONN.rollback()
            print(f"Error updating user {user_id}: {e}")
            return False

    @classmethod
    def delete(cls, user_id):
        try:
            CURSOR.execute("DELETE FROM users WHERE id = ?", (user_id,))
            CONN.commit()
            return CURSOR.rowcount > 0
        except Exception as e:
            CONN.rollback()
            print(f"Error deleting user {user_id}: {e}")
            return False



# Sample instance of Expense for testing
if __name__ == "__main__":
    user1 = User(name="Test User", email="testuser@example.com")
    ipdb.set_trace()
