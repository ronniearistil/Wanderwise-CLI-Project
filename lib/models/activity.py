from lib.models.database import CURSOR, CONN  # Only import the database connection

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

    @classmethod
    def drop_table(cls, cursor):
        """Drop the activities table if it exists."""
        cursor.execute("DROP TABLE IF EXISTS activities")

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


