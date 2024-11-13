from models.database import CURSOR, CONN  # Only import the database connection


class Activity:
    """Model for an activity associated with a destination."""


    def __init__(self, destination_id, name, date=None, time=None, cost=0, description=""):
        # Instance attributes
        self.destination_id = destination_id
        self.name = name
        self.date = date or "Today"
        self.time = time or "00:00"
        self.cost = cost
        self.description = description

    # ********
    # Class Methods
    # ********

    @classmethod
    def create_table(cls, cursor):
        """Create the activities table if it doesn't exist."""
        cursor.execute('''CREATE TABLE IF NOT EXISTS activities (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            destination_id INTEGER NOT NULL,
                            name TEXT NOT NULL CHECK(name <> ''),
                            date TEXT DEFAULT (date('now')),
                            time TEXT,
                            cost REAL DEFAULT 0 CHECK(cost >= 0),
                            description TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY(destination_id) REFERENCES destinations(id) ON DELETE CASCADE
                        )''')

    @classmethod
    def drop_table(cls, cursor):
        """Drop the activities table if it exists."""
        cursor.execute("DROP TABLE IF EXISTS activities")

    
    def delete(cls, cursor, activity_id):
        cursor.execute("DELETE FROM activities WHERE id = ?", (activity_id,))
        cursor.connection.commit()
        return cursor.rowcount > 0 
        # This checks if the number of affected rows is greater than zero.

    @classmethod
    def get_all(cls, cursor):
        cursor.execute("SELECT * FROM activity")
        return cursor.fetchall()

    @classmethod
    def update(cls, name, date, time, cost, description):
        try:
            with CONN:
                CURSOR.execute(f""""
                    UPDATE SET name=?, species=?, breed=?, temperament=?
                    WHERE id = ?;       
                """,)
                
        except Exception as e:
            return e
    
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
