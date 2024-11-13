# lib/models/__init__.py
from ..database_setup import CONN, CURSOR, reset_and_seed_database

# Import each model directly, ensuring they don't reference each other unnecessarily
from .destination import Destination
from .activity import Activity
from .expense import Expense
from .user import User

''' Initialize database schema if needed'''
reset_and_seed_database()

'''Define the accessible interface of the models module'''

__all__ = ["Destination", "Activity", "Expense", "User", "CONN", "CURSOR"]


''' Purpose: This file serves as the entry point for the models package, importing all the necessary models and initializing the database schema.
# Connections: References database_setup for setting up the database and uses imported models for ORM purposes.
# Comment: Ensure that the __all__ statement reflects only the models and database connections needed for external access.'''



