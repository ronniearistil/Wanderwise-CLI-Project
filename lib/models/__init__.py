# Import only database connection and initialization, not specific models
from .database import CONN, CURSOR, initialize_database

# Initialize the database tables if they haven't been created yet
initialize_database()

__all__ = ["CONN", "CURSOR", "initialize_database"]






