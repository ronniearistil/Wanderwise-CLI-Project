from models.__init__ import CURSOR, CONN  # Only import the database connection

class Activity:
    """Model for an activity associated with a destination."""

    def __init__(self, destination_id, name, date=None, time=None, cost=0, description=""):
        self.destination_id = destination_id
        self.name = name
        self.date = date or "Today"
        self.time = time or "00:00"
        self.cost = cost
        self.description = description

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
    @property
    def cost(self):
        return self._cost         

    @cost.setter
    def cost(self, value_cost):
        if not isinstance(value_cost, int):
            raise TypeError("cost must be an integer")
        elif not value_cost :
            raise ValueError("cost cannot be negative")
        self._cost = value_cost    # Set the validated cost
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value_to_validate):
        if not isinstance(value_to_validate, str):
            raise TypeError("name must be a string")
        elif len(value_to_validate) not in range(2, 50):
            raise ValueError("name must be in between 2 and 50 characters")
        elif hasattr(self, "_name"):
            raise AttributeError("name cannot be initialized")
        self._name = value_to_validate  #Set the validated name

    @classmethod
    def drop_table(cls, cursor):
        """Drop the activities table if it exists."""
        cursor.execute("DROP TABLE IF EXISTS activities")

    @classmethod
    def delete(cls, activity_id):
        """Delete an activity from the database by its ID."""
        # Check if the activity exists before attempting to delete
        CURSOR.execute("SELECT id FROM activity WHERE id = ?", (activity_id,))
        result = CURSOR.fetchone()
        if result is None:
            raise ValueError(f"Activity with ID {activity_id} does not exist")

        CURSOR.execute("DELETE FROM activity WHERE id = ?", (activity_id,))
        CURSOR.connection.commit()  # Commit the deletion to the database

        # Optionally, remove the instance from the class's `all` list if it exists
        cls.all = [activity for activity in cls.all if activity.id != activity_id]

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