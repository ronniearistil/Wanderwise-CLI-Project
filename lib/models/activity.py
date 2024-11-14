from models.database import CURSOR, CONN  # Only import the database connection


class Activity:
    """Model for an activity associated with a destination."""
    all = {}

    def __init__(self, name, date, time, cost, description, destination_id, id=None):
        # Instance attributes
        self.id = id
        self.name = name
        self.destination_id = destination_id
        self.date = date
        self.time = time
        self.cost = cost
        self.description = description

    # ********
    # Class Methods
    # ********

    @classmethod
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of activities instances """
        sql = """
            CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL CHECK(name <> ''),
            date TEXT,
            time TEXT,
            cost TEXT,
            description TEXT,
            destination_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            FOREIGN KEY (destination_id) REFERENCES destination(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Activity instances """
        sql = """
            DROP TABLE IF EXISTS activities;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name, date, time, cost, description, created_at and destination id values of the current Activty object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        try:
            sql = """
            INSERT INTO activities (name, date, time, cost, description, destination_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            CURSOR.execute(sql, (self.name, self.date, self.time, self.cost, self.description, self.destination_id))
            CONN.commit()
        
            self.id = CURSOR.lastrowid
            type(self).all[self.id] = self
        except Exception as e:
            print(f"Error saving activity: {e}")

    @classmethod
    def create(cls, name, date, cost, description, destination_id):
        """ Initialize a new Activity instance and save the object to the database"""
        activity = cls(name, date, cost, description, destination_id)
        activity.save()
        return activity
    
    def update(self):
        """Update the table row corresponding to the current Activity instance."""
        try:
            sql = """
            UPDATE activities
            SET name = ?, date = ?, time = ?, cost = ?, description = ?, destination_id = ?
            WHERE id = ?
            """
            CURSOR.execute(sql, (self.name, self.date, self.time, self.cost, self.description, self.destination_id, self.id))
            CONN.commit()
        except Exception as e:
            print(f"Error updating activity: {e}")

    
    def delete(self):
        """Delete the table row corresponding to the current Activity instance and update local dictionary."""
        try:
            sql = "DELETE FROM activities WHERE id = ?"
            CURSOR.execute(sql, (self.id,))
            CONN.commit()
            del type(self).all[self.id]
            self.id = None
        except Exception as e:
            print(f"Error deleting activity: {e}")


    
    @classmethod
    def instance_from_db(cls, row):
        """Return an Activity object having the attribute values from the table row."""

        activity = cls.all.get(row[0])
        if activity:
            activity.name = row [1]
            activity.date = row [2]
            activity.cost = row [3]
            activity.description = row [4]
            activity.destination_id = row [5]
        else:
            activity = cls(row[1], row[2], row[3], row[4], row[5], row[0])
            cls.all[activity.id] = activity
        return activity
    
    @classmethod
    def get_all(cls):
        """Return a list containing an Activity object for each row in the table."""
        try:
            sql = "SELECT * FROM activities"
            rows = CURSOR.execute(sql).fetchall()
            return [cls.instance_from_db(row) for row in rows]
        except Exception as e:
            print(f"Error retrieving activities: {e}")
            return []

    



        
    def expenses(self):
        from expense import Expense
        return [expenses for expenses in Expense.get_all() if  is self]

    # *******
    # PROPERTIES
    # *******
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value_to_validate):
        if not isinstance(value_to_validate, str):
            return ("name must be a string")
        elif len(value_to_validate) not in range(2, 50):
            return ("name must be in between 2 and 50 characters")
        elif hasattr(self, "_name"):
            return ("name cannot be initialized")
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
        if not isinstance(value_cost, (int, float)):
            return ("cost must be an integer or float")
        elif value_cost < 0:
            return ("cost cannot be negative")
        self._cost = value_cost  # Set the validated cost

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description_value):
        self._description = description_value


    @classmethod
    def create(cls, cursor, destination_id, name, date=None, time=None, cost=0, description=""):
        """Insert a new activity into the database."""
        cursor.execute(
            "INSERT INTO activities (destination_id, name, date, time, cost, description) VALUES (?, ?, ?, ?, ?, ?)",
            (destination_id, name, date, time, cost, description)
        )
        cursor.connection.commit()
        return cursor.lastrowid

    @classmethod
    def get_by_destination(cls, cursor, destination_id):
        """Retrieve all activities associated with a specific destination."""
        cursor.execute("SELECT * FROM activities WHERE destination_id = ?", (destination_id,))
        return cursor.fetchall()




# activity1 = Activity(destination_id=1, name="Hiking", date="2024-12-01", time="08:00", cost=50, description="A morning hiking trip.")
