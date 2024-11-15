from lib.models.__init__ import CURSOR, CONN
from lib.models import user
import ipdb


class Destination:

    all = {}

    def __init__(self, name, location, description, user_id, id=None):
        self.id = id
        self.user_id = int(user_id)
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
            raise TypeError("your user_id must be an integer")
        from lib.models.user import User
        if User.find_by_id(user_id) is None:
            raise ValueError("this user doesn't exist")
        else:
            self._user_id = user_id

    #########ORM CLASS METHODS
    # CRUD
    @classmethod
    def create_table(cls):
        try:
            CURSOR.execute(
                """CREATE TABLE IF NOT EXISTS destinations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL CHECK(name <> ''),
                            location TEXT NOT NULL CHECK(location <> ''),
                            description TEXT,
                            user_id INTEGER,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                        )"""
            )
        except Exception as e:
            print("there was an error creating your table")
            return e

    @classmethod
    def drop_table(cls):
        try:
            """Drop the table that persists Destination instances"""
            sql = """
                DROP TABLE IF EXISTS destinations;
            """
            CURSOR.execute(sql)
        except Exception as e:
            print("there was an error dropping your table")
            return e

    def save(self):
        """Insert a new row with the name and location values of the current Destination instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        try:
            sql = """
                INSERT INTO destinations (name, location, description, user_id)
                VALUES (?, ?, ?, ?)
            """

            CURSOR.execute(
                sql, (self.name, self.location, self.description, self.user_id)
            )
            CONN.commit()

            self.id = CURSOR.lastrowid
            type(self).all[self.id] = self
        except Exception as e:
            CONN.rollback()
            print("you have an error saving your destination", e)
            return e

    @classmethod
    def create(cls, name, location, description, user_id):
        """Initialize a new Destination instance and save the object to the database"""
        try:
            user_id = int(user_id)
            destination = cls(name, location, description, user_id)
            destination.save()
            return destination
        except Exception as e:
            print(
                "you have an error initializing a Destination and saving the object to the database",
                e,
            )
            return None

    @classmethod
    def update(cls, destination_id, name, location, description, user_id):
        """Update the table row corresponding to the current Destination instance."""
        try:
            sql = """
                UPDATE destinations
                SET name = ?, location = ?, description = ?, user_id =?
                WHERE id = ?
            """
            CURSOR.execute(
                sql, (name, location, description, user_id, destination_id)
            )
            CONN.commit()
            return CURSOR.rowcount > 0
        except Exception as e:
            print("there was an issue updating your table row", e)
            return e
        
    @classmethod
    def delete(cls, destination_id):
        """Delete the table row corresponding to the current Destination instance,
        delete the dictionary entry, and reassign id attribute"""
        try:
            sql = """
                DELETE FROM destinations
                WHERE id = ?
            """
            CURSOR.execute(sql, (destination_id,))
            CONN.commit()
            destination_id = None
        except Exception as e:
            print("there was an issue deleting the row from the database")
            return e

    @classmethod
    def instance_from_db(cls, row):
        try:
            """Return a Destination object having the attribute values from the table row."""

            # Check the dictionary for an existing instance using the row's primary key
            destination = cls.all.get(row[0])
            if destination:
                # ensure attributes match row values in case local instance was modified
                destination.name = row[1]
                destination.location = row[2]
                destination.description = row[3]
                destination.user_id = row[4]
            else:
                # not in dictionary, create new instance and add to dictionary
                destination = cls(row[1], row[2], row[3], row[4], row[0])
                cls.all[destination.id] = destination
            return destination
        except Exception as e:
            print(
                "there was an issue returning your Destination obj from the database", e
            )
            return e

    @classmethod
    def get_all(cls):
        """Return a list containing a Destination object per row in the table"""
        try:
            sql = """
                SELECT *
                FROM destinations
            """
            rows = CURSOR.execute(sql).fetchall()
            return [cls.instance_from_db(row) for row in rows]
        except Exception as e:
            print("there is an error returning your list with a Destination obj", e)
        return None

    ######find by and filter
    @classmethod
    def find_by_id(cls, destination_id):
        try:
            CURSOR.execute("SELECT * FROM destinations WHERE id = ?", (destination_id,))
            data = CURSOR.fetchone()
            return cls(data[1], data[2], data[3], data[4], data[0]) if data else None
        except Exception as e:
            print(f"Error finding destination by ID: {e}")
            return None

    @classmethod
    def find_by_location(cls, location):
        """Return a Destination object corresponding to the table row matching the specified primary key"""
        try:
            sql = """
                SELECT *
                FROM destinations
                WHERE location = ?
            """
            row = CURSOR.execute(sql, (location,)).fetchone()
            return cls.instance_from_db(row) if row else None
        except Exception as e:
            print("there is no Destination that corresponds to the table", e)
            return None

    @classmethod
    def filter_by_location(cls, location):
        try:
            return [
                destination
                for destination in cls.get_all()
                if destination.location.upper().startswith(location.upper())
            ] or ValueError(f"No destinations found matching location: {location}")
        except Exception as e:
            print("Error filtering destinations by location:", e)
        return None