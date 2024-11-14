from lib.models.__init__ import CURSOR, CONN
from lib.helpers import ValidatorMixin
import ipdb
from datetime import datetime

class User(ValidatorMixin):
    """Model for a user in the Wanderwise application."""

    def __init__(self, name, email, created_at=None, id=None):
        self.name = name
        self.email = email
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.validate_text(value)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = self.validate_email(value)

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
    def create_table(cls, cursor):
        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL CHECK(name <> ''),
                                email TEXT NOT NULL UNIQUE,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )''')
        except Exception as e:
            CONN.rollback()
            print(f"Error creating users table: {e}")

    @classmethod
    def drop_table(cls, cursor):
        try:
            cursor.execute("DROP TABLE IF EXISTS users")
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
    def get_all(cls, cursor):
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        return [cls(row[1], row[2], row[3], row[0]) for row in data]

    @classmethod
    def find_by_id(cls, cursor, user_id):
        try:
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            data = cursor.fetchone()
            return cls(data[1], data[2], data[3], data[0]) if data else None
        except Exception as e:
            print(f"Error finding user by ID: {e}")
            return None

    @classmethod
    def update(cls, cursor, user_id, name, email):
        try:
            cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
            cursor.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            CONN.rollback()
            print(f"Error updating user {user_id}: {e}")
            return False

    @classmethod
    def delete(cls, cursor, user_id):
        try:
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            cursor.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            CONN.rollback()
            print(f"Error deleting user {user_id}: {e}")
            return False

# def destinations(self):
        # from destination import Destination
#         return[destination for destination in Destination.get_all() if destination.user is self] 