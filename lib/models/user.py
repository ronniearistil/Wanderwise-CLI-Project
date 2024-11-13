from models.__init__ import CURSOR, CONN
from helpers import ValidatorMixin
import ipdb

class User(ValidatorMixin):
    """Model for a user in the Wanderwise application."""

    def __init__(self, name, email, created_at, id =None):
        # Use mixin validation methods
        self.name = name
        self.email = email
        self.created_at = created_at
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
        data = cursor.fetchall()
        return [cls(row[1], row[2], row[3], row[0] ) for row in data]

    @classmethod
    def find_by_id(cls, cursor, user_id):
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        data = cursor.fetchone()
        return  cls(data[1], data[2], data[3], data[0] )
    

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
    
    def destinations(self):
        '''Select all destinations by user'''
        from models.destination import Destination
        query = CURSOR.execute('SELECT * FROM destinations WHERE user_id =?', (self.id,))
        data =query.fetchall()
        return[Destination.instance_from_db(row) for row in data]
        

# def destinations(self):
        # from destination import Destination
#         return[destination for destination in Destination.get_all() if destination.user is self] 