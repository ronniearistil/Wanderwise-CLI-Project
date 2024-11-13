from models.__init__ import CURSOR, CONN
import ipdb

class Destination:

    all = {}

    def __init__(self, name, location, description, user_id, id=None):
        self.id = id
        self.user_id = user_id
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


#########ORM CLASS METHODS
        #CRUD
    @classmethod
    def create_table(cls, cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS destinations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL CHECK(name <> ''),
                            location TEXT NOT NULL CHECK(location <> ''),
                            description TEXT,
                            user_id INTEGER,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                        )''')


    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Destination instances """
        sql = """
            DROP TABLE IF EXISTS destinations;
        """
        CURSOR.execute(sql)


    def save(self):
        """ Insert a new row with the name and location values of the current Destination instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO destinations (name, location, description, user_id)
            VALUES (?, ?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.location, self.description, self.user_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self


    @classmethod
    def create(cls, name, location, description, user_id):
        """ Initialize a new Destination instance and save the object to the database """
        destination = cls(name, location, description, user_id)
        destination.save()
        return destination

    def update(self):
        """Update the table row corresponding to the current Destination instance."""
        sql = """
            UPDATE destinations
            SET name = ?, location = ?, description = ?, user_id =?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.description, self.user_id, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Destination instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM destinations
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None


    @classmethod
    def instance_from_db(cls, row):
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


    @classmethod
    def get_all(cls):
        """Return a list containing a Destination object per row in the table"""
        sql = """
            SELECT *
            FROM destinations
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]


######find by and filter
    @classmethod
    def find_by_location(cls, location):
        """Return a Destination object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM destinations
            WHERE location = ?
        """

        row = CURSOR.execute(sql, (location,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def filter_by_location(cls, location):
        return [destination for destination in cls.get_all() if destination.location.upper().startswith(location.upper())]






