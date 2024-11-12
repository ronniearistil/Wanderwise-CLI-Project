# lib/models/__init__.py
from ..database_setup import CONN, CURSOR, reset_and_seed_database

# Import each model directly, ensuring they don't reference each other unnecessarily
from .destination import Destination
from .activity import Activity
from .expense import Expense
from .user import User

# Initialize database schema if needed
reset_and_seed_database()

# Specify the public API of this module
__all__ = ["Destination", "Activity", "Expense", "User", "CONN", "CURSOR"]








