from lib.base_model import BaseModel

class User(BaseModel):
    """Model for a user in the Wanderwise application."""
    
    CREATE_TABLE_SQL = '''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL CHECK(name <> ''),
                                email TEXT NOT NULL UNIQUE,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )'''

    @classmethod
    def create_table(cls):
        cls.execute_create_table(cls.CREATE_TABLE_SQL)

    @classmethod
    def drop_table(cls):
        super().drop_table("users")

    @classmethod
    def create(cls, name, email):
        return super().create(
            "INSERT INTO users (name, email) VALUES (?, ?)", (name, email)
        )

    @classmethod
    def get_all(cls):
        return super().get_all("SELECT * FROM users")

    @classmethod
    def find_by_id(cls, user_id):
        return super().find_by_id("SELECT * FROM users WHERE id = ?", user_id)

    @classmethod
    def update(cls, user_id, **kwargs):
        columns = ', '.join([f"{k} = ?" for k in kwargs.keys()])
        params = tuple(kwargs.values()) + (user_id,)
        return super().update(f"UPDATE users SET {columns} WHERE id = ?", params)

    @classmethod
    def delete(cls, user_id):
        return super().delete("DELETE FROM users WHERE id = ?", user_id)


'''Purpose: Manages user-related data with CRUD functionality.
Connections: Extends BaseModel and is linked to Destination.'''






