# db_connection.py
import sqlite3

def get_connection():
    """Create and return a new SQLite database connection."""
    return sqlite3.connect('wanderwise.db')

