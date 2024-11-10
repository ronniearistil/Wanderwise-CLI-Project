from lib.models.database import CURSOR, CONN

class Destination:
    
    def __init__(self, name, location, description, id=None):
        self.name = name
        self.location = location
        self.description = description

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

    @classmethod
    def create(cls, name, location, description, user_id):
        """Insert a new destination into the database."""
        CURSOR.execute(
            "INSERT INTO destinations (name, location, description, user_id) VALUES (?, ?, ?, ?)", 
            (name, location, description, user_id)
        )
        CONN.commit()
        return CURSOR.lastrowid  # Return the ID of the newly inserted destination

    @classmethod
    def get_all(cls):
        """Retrieve all destinations from the database."""
        CURSOR.execute("SELECT * FROM destinations")
        return CURSOR.fetchall()
    
    @classmethod
    def filter_by_location(cls, location):
        return [destination for destination in cls.get_all() if destination.location.upper().startswith(location.upper())]




