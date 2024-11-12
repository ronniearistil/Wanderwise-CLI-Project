import sqlite3
from lib.models.database import CURSOR, CONN

class Destination:

    all = []
   
    def __init__(self, name, location, description, id=None):
        self.name = name
        self.location = location
        self.description = description
        type(self).all.append(self)

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("your name must be a string")
        elif not len(name) in range(1, 26):
            raise ValueError("your name must be between 1 and 25 characters")
        else:
            self._name = name

    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, location):
        if not isinstance(location, str):
            raise TypeError("your location must be a string")
        else:
            self._location = location


    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description):
        if not isinstance(description, str):
            raise TypeError("your description must be a string")
        elif not len(description) in range(1, 141):
            raise ValueError("your name must be between 1 and 140 characters")
        else:
            self._description = description


    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, user_id):
        if not isinstance(user_id, int):
            raise TypeError("your user_id must be a number")
        else:
            self._user_id = user_id


    """Model for a travel destination."""

    # Inserts a new row into the destinations table using values for name, location, description, and user_id.
    # Commits the transaction to save changes.
    # Returns the ID of the newly inserted row for reference.
    @classmethod
    def create(cls, name, location, description, user_id):
        """Insert a new destination/row into the database."""
        CURSOR.execute(
            "INSERT INTO destinations (name, location, description, user_id) VALUES (?, ?, ?, ?)", 
            (name, location, description, user_id)
        )
        CONN.commit()
        return CURSOR.lastrowid  # Return the ID of the newly inserted destination


    # Executes a SQL command to select all rows from the destinations table.
    # Fetches and returns all rows as a list of tuples, where each tuple corresponds to a row. 
    # This allows access to all records in the table.
    @classmethod
    def get_all(cls):
        """Retrieve all destinations from the database."""
        CURSOR.execute("SELECT * FROM destinations")
        return CURSOR.fetchall()
    

    # Calls cls.get_all() to retrieve all destinations.
    # Filters the list to include only destinations where the location attribute starts with the specified location string.
    # Returns a new list containing only the destinations that match this condition.
    @classmethod
    def filter_by_location(cls, location):
        return [destination for destination in cls.get_all() if destination.location.upper().startswith(location.upper())]