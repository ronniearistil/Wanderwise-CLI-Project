from lib.base_model import BaseModel

class Activity(BaseModel):
    """Model for an activity associated with a destination."""

    CREATE_TABLE_SQL = '''CREATE TABLE IF NOT EXISTS activities (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            destination_id INTEGER NOT NULL,
                            name TEXT NOT NULL CHECK(name <> ''),
                            date TEXT DEFAULT (date('now')),
                            time TEXT,
                            cost REAL DEFAULT 0 CHECK(cost >= 0),
                            description TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY(destination_id) REFERENCES destinations(id) ON DELETE CASCADE
                        )'''

    @classmethod
    def create_table(cls):
        cls.execute_create_table(cls.CREATE_TABLE_SQL)

    @classmethod
    def drop_table(cls):
        super().drop_table("activities")

    @classmethod
    def create(cls, destination_id, name, date=None, time=None, cost=0, description=""):
        return super().create(
            "INSERT INTO activities (destination_id, name, date, time, cost, description) VALUES (?, ?, ?, ?, ?, ?)",
            (destination_id, name, date, time, cost, description)
        )

    @classmethod
    def get_all(cls):
        # Provide default SQL query for retrieving all activities
        return super().get_all("SELECT * FROM activities")

    @classmethod
    def get_by_destination(cls, destination_id):
        return cls.get_by_column("SELECT * FROM activities WHERE destination_id = ?", destination_id)

    @classmethod
    def find_by_id(cls, activity_id):
        return super().find_by_id("SELECT * FROM activities WHERE id = ?", activity_id)

    @classmethod
    def update(cls, activity_id, **kwargs):
        columns = ', '.join([f"{k} = ?" for k in kwargs.keys()])
        params = tuple(kwargs.values()) + (activity_id,)
        return super().update(f"UPDATE activities SET {columns} WHERE id = ?", params)

    @classmethod
    def delete(cls, activity_id):
        return super().delete("DELETE FROM activities WHERE id = ?", activity_id)





