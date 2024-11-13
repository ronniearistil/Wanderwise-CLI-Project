# Initialize the database connection
import sqlite3 
CONN = sqlite3.connect('wanderwise.db')
CURSOR = CONN.cursor()

# Import each model directly, ensuring they don't reference each other unnecessarily
# from .destination import Destination
# from .activity import Activity
# from .expense import Expense
# from .user import User

# Initialize database schema if needed
# initialize_database()

# Specify the public API of this module
__all__ = ["Destination", "Activity", "Expense", "User", "CONN", "CURSOR"]







