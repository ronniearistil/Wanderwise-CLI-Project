# Import classes and database connection for easier access
from .destination import Destination
from .activity import Activity
from .expense import Expense
from .database import CONN, CURSOR, initialize_database

# Initialize the database tables if they haven't been created yet
initialize_database()

# Specify the public API of the module
__all__ = ["Destination", "Activity", "Expense", "CONN", "CURSOR"]


