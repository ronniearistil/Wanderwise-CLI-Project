from models.__init__ import CURSOR, CONN  # Only import the database connection

def initialize_database(reset=False):
    """
    Initialize the database. This function will be called at the start of the application
    to set up tables or reset them if needed.
    """
    # Import models within the function to avoid circular imports
    from models.user import User
    from models.destination import Destination
    from models.activity import Activity
    from models.expense import Expense

    if reset:
        # Drop tables if reset is requested
        User.drop_table(CURSOR)
        Destination.drop_table(CURSOR)
        Activity.drop_table(CURSOR)
        Expense.drop_table(CURSOR)

    # Create tables for each model/Class
    User.create_table(CURSOR)
    Destination.create_table(CURSOR)
    Activity.create_table(CURSOR)
    Expense.create_table(CURSOR)

    # Commit changes to the database
    CONN.commit()
    print("Database initialized with tables created.")


if __name__=='__main__': 
    initialize_database()
















