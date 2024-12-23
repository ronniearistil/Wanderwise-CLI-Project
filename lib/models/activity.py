from lib.models.__init__ import CURSOR, CONN  # Only import the database connection
# from __init__ import CURSOR, CONN  # Only import the database connection
# import ipdb

class Activity:
    """Model for an activity associated with a destination."""
    all = {}

    def __init__(self, name, date, time, cost, description, destination_id, id=None):
        # Instance attributes
        self.id = id
        self.name = name
        self.date = date
        self.time = time
        self.cost = cost
        self.destination_id = destination_id
        self.description = description

    # ********
    # Class Methods
    # ********

    @classmethod
    def create_table(cls):
        try:
            CURSOR.execute('''CREATE TABLE IF NOT EXISTS activities (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL CHECK(name <> ''),
                            date INTEGER NOT NULL CHECK(date <> ''),
                            time TEXT,
                            cost INTEGER,
                            description TEXT,
                            destination_id INTEGER,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY(destination_id) REFERENCES destinations(id)
                        )''')
        except Exception as e:
            print("There was an error creating your table:", e)
            return e


    @classmethod
    def drop_table(cls):
        try:
            """ Drop the table that persists Activity instances """
            sql = """
                DROP TABLE IF EXISTS activities;
            """
            CURSOR.execute(sql)
        except Exception as e:
            print("there was an error dropping the table")

    def save(self):
        """ Insert a new row with the name, date, time, cost, description, created_at and destination id values of the current Activty object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        try:
            sql = """
            INSERT INTO activities (name, date, time, cost, description, destination_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            # ipdb.set_trace()
            CURSOR.execute(sql, (self.name, self.date, self.time, self.cost, self.description, self.destination_id))
            CONN.commit()

            self.id = CURSOR.lastrowid
            type(self).all[self.id] = self
        except Exception as e:
            CONN.rollback()
            print("Error saving activity", e)
            return e

    @classmethod
    def create(cls, name, date, time, cost, description, destination_id):
        try:
            """ Initialize a new Activity instance and save the object to the database """
            activity = cls(name, date, time, cost, description, destination_id)
            
            activity.save()
            return activity
        except Exception as e:
            print("you have an error initializing a Activity and saving the object to the database", e)
            return None

    @classmethod
    def update(cls, activity_id, name, date, time, cost, description, destination_id):
        """Update the table row corresponding to the current Activity instance."""
        try:
            sql = """
                UPDATE activities
                SET name = ?, date = ?, time = ?, cost = ?, description = ?, destination_id = ?
                WHERE id = ?
            """
            CURSOR.execute(
                sql, (name, date, time, cost, description, activity_id, destination_id)
            )
            CONN.commit()
            return CURSOR.rowcount > 0
        except Exception as e:
            print(f"Error updating activity: {e}")
            return e


    @classmethod
    def delete(cls, activity_id):
        """Delete the table row corresponding to the current Activity instance and update local dictionary."""
        try:
            sql = """
                DELETE FROM activities
                WHERE id = ?
                """
            CURSOR.execute(sql, (activity_id,))
            CONN.commit()
            activity_id = None
        except Exception as e:
            print(f"Error deleting activity: {e}")
            return e


    
    @classmethod
    def instance_from_db(cls, row):
        try:
            """Return an Activity object having the attribute values from the table row."""

            activity = cls.all.get(row[0])
            if activity:
                activity.name = row [1]
                activity.date = row [2]
                activity.time = row [3]
                activity.cost = row [4]
                activity.description = row [5]
                activity.destination_id = row [6]
            else:
                activity = cls(row[1], row[2], row[3], row[4], row[5], row[6], row[0])
                cls.all[activity.id] = activity
            return activity
        except Exception as e:
            print("there was an issue returning your Activity obj from the database", e)
            return e
    
    @classmethod
    def get_all(cls):
        """Return a list containing an Activity object for each row in the table."""
        try:
            sql = "SELECT * FROM activities"
            rows = CURSOR.execute(sql).fetchall()
            return [cls.instance_from_db(row) for row in rows]
        except Exception as e:
            print(f"Error retrieving activities", e)
        return None
        
    @classmethod
    def find_by_id(cls, activity_id):
        """Retrieve an activity by its ID and return an Activity object."""
        CURSOR.execute("SELECT * FROM activities WHERE id = ?", (activity_id,))
        row = CURSOR.fetchone()
        if row:
            return cls(row[1], row[2], row[3], row[4], row[5], row[6], row[0])
        return None


    # *******
    # PROPERTIES
    # *******
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value_to_validate):
        if not isinstance(value_to_validate, str):
            raise TypeError("name must be a string")
        elif len(value_to_validate) not in range(2, 50):
            raise ValueError("name must be in between 2 and 50 characters")
        # elif not hasattr(self, "_name"):
        #     raise AttributeError("name cannot be initialized")
        self._name = value_to_validate  #Set the validated name


    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date_validate):
        self._date = date_validate

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time_validate):
        self._time = time_validate
        

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value_cost):
        self._cost = value_cost  # Set the validated cost

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description_value):
        self._description = description_value

if __name__ == "__main__":
    activity1 = Activity(destination_id=1, name="Hiking", date="2024-12-01", time="08:00", cost=50, description="A morning hiking trip.", id = 1)
    activity2 = Activity(destination_id=2, name="Bicycle", date="2024-11-01", time="09:00", cost=100, description="A morning hiking.", id = 2)
# import ipdb; ipdb.set_trace()
