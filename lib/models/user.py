from lib.models.database import CURSOR, CONN
import re

class User:
    """Model for a user in the Wanderwise application."""

    def __init__(self, name, email):
        """Initialize a new User instance with name and email."""
        self.name = name
        self.email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and value.strip():
            self._name = value
        else:
            raise ValueError("Name must be a non-empty string.")

    @property
    def email(self):
        return self._email

    @staticmethod
    def _is_valid_email(value):
        """Basic email validation."""
        return re.match(r"[^@]+@[^@]+\.[^@]+", value)

    @name.setter
    def email(self, value):
        if self._is_valid_email(value):
            self._email = value
        else:
            raise ValueError("Invalid email format.")

    @classmethod
    def create(cls, name, email):
        """
        Create a new user in the database.
        
        :param name: The name of the user.
        :param email: The email of the user.
        :return: The ID of the newly created user.
        """
        CURSOR.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        CONN.commit()
        return CURSOR.lastrowid

    @classmethod
    def get_all(cls):
        """
        Retrieve all users from the database.
        
        :return: A list of all users as tuples.
        """
        CURSOR.execute("SELECT * FROM users")
        return CURSOR.fetchall()

    @classmethod
    def find_by_id(cls, user_id):
        """
        Find a user by their ID.
        
        :param user_id: The ID of the user to retrieve.
        :return: The user record as a tuple if found, otherwise None.
        """
        CURSOR.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return CURSOR.fetchone()

    @classmethod
    def update(cls, user_id, name, email):
        """
        Update an existing user's name and email in the database.
        
        :param user_id: The ID of the user to update.
        :param name: The new name of the user.
        :param email: The new email of the user.
        :return: True if the user was updated, False otherwise.
        """
        CURSOR.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
        CONN.commit()
        return CURSOR.rowcount > 0

    @classmethod
    def delete(cls, user_id):
        """
        Delete a user from the database by their ID.
        
        :param user_id: The ID of the user to delete.
        :return: True if the user was deleted, False otherwise.
        """
        CURSOR.execute("DELETE FROM users WHERE id = ?", (user_id,))
        CONN.commit()
        return CURSOR.rowcount > 0



