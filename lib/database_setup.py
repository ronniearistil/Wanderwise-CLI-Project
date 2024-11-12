import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker for generating random data
fake = Faker()

# Determine which database to use based on environment
CONN = sqlite3.connect(':memory:')  # Use ':memory:' for tests to run in an in-memory database
CURSOR = CONN.cursor()

# Enable foreign key constraints
def initialize_database():
    CONN.execute("PRAGMA foreign_keys = ON;")
    CONN.commit()

initialize_database()  # Call to ensure foreign key constraints are enabled

# Rest of your functions...
def reset_database():
    """Resets the database by dropping all tables and recreating them."""
    with CONN:
        CURSOR.execute("PRAGMA foreign_keys = OFF;")
        CURSOR.execute("DROP TABLE IF EXISTS users")
        CURSOR.execute("DROP TABLE IF EXISTS destinations")
        CURSOR.execute("DROP TABLE IF EXISTS activities")
        CURSOR.execute("DROP TABLE IF EXISTS expenses")
        CURSOR.execute("PRAGMA foreign_keys = ON;")
        CONN.commit()

def create_tables():
    """
    Creates tables for users, destinations, activities, and expenses.
    """
    from lib.models.user import User
    from lib.models.destination import Destination
    from lib.models.activity import Activity
    from lib.models.expense import Expense

    # Create tables through model class methods
    User.create_table()
    Destination.create_table()
    Activity.create_table()
    Expense.create_table()

    print("Database tables created successfully.")

def seed_data():
    """
    Seeds the database with sample data using Faker.
    """
    from lib.models.user import User
    from lib.models.destination import Destination
    from lib.models.activity import Activity
    from lib.models.expense import Expense

    # Seed users
    user_ids = []
    for _ in range(3):
        name = fake.name()
        email = fake.email()
        user_id = User.create(name=name, email=email)
        user_ids.append(user_id)
    
    # Seed destinations and related activities
    destination_ids = []
    for user_id in user_ids:
        for _ in range(5):
            name = fake.city()
            location = fake.country()
            description = fake.text(max_nb_chars=50)
            destination_id = Destination.create(name, location, description, user_id)
            destination_ids.append(destination_id)

    # Seed activities
    activity_ids = []
    for destination_id in destination_ids:
        for _ in range(3):
            name = random.choice(["City Tour", "Museum Visit", "Hiking", "Beach Day"])
            description = fake.sentence()
            date = fake.date_this_year()
            time = fake.time()
            cost = round(random.uniform(10, 500), 2)
            activity_id = Activity.create(destination_id, name, date, time, cost, description)
            activity_ids.append(activity_id)

    # Seed expenses
    for activity_id in activity_ids:
        for _ in range(2):
            amount = round(random.uniform(10, 500), 2)
            date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%m-%d-%Y")
            category = random.choice(["Food", "Transport", "Accommodation", "Entertainment"])
            Expense.create(activity_id, amount, date, category)

    print("Database seeded with sample data.")

def reset_and_seed_database():
    """
    Resets, creates tables, and seeds the database with sample data.
    """
    reset_database()
    create_tables()
    seed_data()
    print("Database reset, tables created, and data seeded.")

# Run seeding if executed directly
if __name__ == "__main__":
    reset_and_seed_database()
























