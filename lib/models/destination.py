from lib.base_model import BaseModel

class Destination(BaseModel):
    """Model for a travel destination."""

    CREATE_TABLE_SQL = '''CREATE TABLE IF NOT EXISTS destinations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL CHECK(name <> ''),
                            location TEXT NOT NULL CHECK(location <> ''),
                            description TEXT,
                            user_id INTEGER,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                        )'''

    @classmethod
    def create_table(cls):
        cls.execute_create_table(cls.CREATE_TABLE_SQL)

    @classmethod
    def drop_table(cls):
        super().drop_table("destinations")

    @classmethod
    def create(cls, name, location, description, user_id):
        return super().create(
            "INSERT INTO destinations (name, location, description, user_id) VALUES (?, ?, ?, ?)",
            (name, location, description, user_id)
        )

    @classmethod
    def get_all(cls):
        return super().get_all("SELECT * FROM destinations")

    @classmethod
    def find_by_id(cls, destination_id):
        return super().find_by_id("SELECT * FROM destinations WHERE id = ?", destination_id)

    @classmethod
    def update(cls, destination_id, **kwargs):
        """Update a destination with specified fields."""
        columns = ', '.join([f"{k} = ?" for k in kwargs.keys()])
        params = tuple(kwargs.values()) + (destination_id,)
        return super().update(f"UPDATE destinations SET {columns} WHERE id = ?", params)

    @classmethod
    def delete(cls, destination_id):
        return super().delete("DELETE FROM destinations WHERE id = ?", destination_id)


'''Purpose: Manages destination-related data with CRUD operations.
Connections: Extends base_model for shared database methods, and includes 
a foreign key relationship with User.'''



