from lib.models.database import CURSOR, CONN
from lib.helpers import ValidatorMixin

class User(ValidatorMixin):
    """Model for a user in the Wanderwise application."""

    def __init__(self, name, email):
        # Use mixin validation methods
        self.name = self.validate_text(name)
        self.email = self.validate_email(email)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.validate_text(value)

    @property
    def email(self):
        return self._email

    @name.setter
    def email(self, value):
        self._email = self.validate_email(value)

    @classmethod
    def create_table(cls, cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL CHECK(name <> ''),
                            email TEXT NOT NULL UNIQUE,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')

    @classmethod
    def drop_table(cls, cursor):
        cursor.execute("DROP TABLE IF EXISTS users")

    @classmethod
    def create(cls, cursor, name, email):
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        cursor.connection.commit()
        return cursor.lastrowid

    @classmethod
    def get_all(cls, cursor):
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

    @classmethod
    def find_by_id(cls, cursor, user_id):
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

    @classmethod
    def update(cls, cursor, user_id, name, email):
        cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
        cursor.connection.commit()
        return cursor.rowcount > 0

    @classmethod
    def delete(cls, cursor, user_id):
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        cursor.connection.commit()
        return cursor.rowcount > 0
