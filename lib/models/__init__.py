# Import database connection first
from .database import CONN, CURSOR, initialize_database

# Import models
from .destination import Destination
from .activity import Activity
from .expense import Expense
from .user import User

# Initialize the database tables if they haven't been created yet
initialize_database()

# Specify the public API of the module
__all__ = ["Destination", "Activity", "Expense", "User", "CONN", "CURSOR"]





