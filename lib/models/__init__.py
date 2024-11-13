# Initialize the database connection
import sqlite3 
CONN = sqlite3.connect('wanderwise.db')
CURSOR = CONN.cursor()

# Specify the public API of this module
__all__ = ["Destination", "Activity", "Expense", "User", "CONN", "CURSOR"]







