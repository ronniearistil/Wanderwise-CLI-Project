from lib.database_setup import CONN, CURSOR

class BaseModel:
    """Base class to handle common database operations."""

    @classmethod
    def execute_create_table(cls, sql):
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def get_by_column(cls, sql, value):
        CURSOR.execute(sql, (value,))
        return CURSOR.fetchall()

    @classmethod
    def drop_table(cls, table_name):
        CURSOR.execute(f"DROP TABLE IF EXISTS {table_name}")
        CONN.commit()

    @classmethod
    def _execute_sql(cls, sql, params=()):
        CURSOR.execute(sql, params)
        CONN.commit()  # Ensure the changes are saved to the database
        return CURSOR

    @classmethod
    def create(cls, sql, params):
        CURSOR.execute(sql, params)
        CONN.commit()  # Commit after insert
        return CURSOR.lastrowid

    @classmethod
    def get_all(cls, sql):
        CURSOR.execute(sql)
        return CURSOR.fetchall()

    @classmethod
    def find_by_id(cls, sql, item_id):
        CURSOR.execute(sql, (item_id,))
        return CURSOR.fetchone()

    @classmethod
    def update(cls, sql, params):
        CURSOR.execute(sql, params)
        CONN.commit()  # Commit after update
        return CURSOR.rowcount

    @classmethod
    def delete(cls, sql, item_id):
        CURSOR.execute(sql, (item_id,))
        CONN.commit()  # Commit after delete
        return CURSOR.rowcount



