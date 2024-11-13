from faker import Faker
from lib.models import Destination, Activity, Expense, User, CONN, CURSOR
import random
from datetime import datetime, timedelta

# Initialize Faker to generate random data
fake = Faker()

# Function to initialize the database
def initialize_database():
    """Initialize the database by dropping and recreating all tables."""
    # Drop tables to reset schema
    User.drop_table(CURSOR)
    Destination.drop_table(CURSOR)
    Activity.drop_table(CURSOR)
    Expense.drop_table(CURSOR)
    
    # Recreate tables with updated schema
    User.create_table(CURSOR)
    Destination.create_table(CURSOR)
    Activity.create_table(CURSOR)
    Expense.create_table(CURSOR)
    
    CONN.commit()
    print("Database initialized with tables created.")

# Function to seed users
def seed_users(num=3):
    """Seed the users table with sample data."""
    users = []
    for _ in range(num):
        name = fake.name()
        email = fake.email()
        user = User.create(CURSOR, name=name, email=email)  # Pass CURSOR as the first argument
        # Fetch the last inserted row to get the ID
        CURSOR.execute("SELECT * FROM users WHERE id = (SELECT MAX(id) FROM users)")
        user_record = CURSOR.fetchone()  # Fetch the full record with the ID
        users.append(user_record)
    print(f"{num} users seeded.")
    return users  # Returns full records for each user

# Function to seed destinations
def seed_destinations(users, num=5):
    """Seed the destinations table with sample data linked to users."""
    destinations = []
    for user in users:
        for _ in range(num):
            name = fake.city()
            location = fake.country()
            description = fake.text(max_nb_chars=50)
            destination = Destination.create(CURSOR, name, location, description, user[0])  # Match argument order
            CURSOR.execute("SELECT * FROM destinations WHERE id = (SELECT MAX(id) FROM destinations)")
            destination_record = CURSOR.fetchone()  # Fetch the full record with the ID
            destinations.append(destination_record)
    print(f"{num * len(users)} destinations seeded.")
    return destinations  # Returns full records for each destination

# Function to seed activities for each destination
def seed_activities(destinations, num_per_destination=3):
    """Seed the activities table with sample data for each destination."""
    activities = []
    activity_names = [
        "City Tour", "Museum Visit", "Hiking", "Beach Day", 
        "Scuba Diving", "Wine Tasting", "Sightseeing", 
        "Shopping", "Cultural Experience", "Boat Ride"
    ]
    for destination in destinations:
        for _ in range(num_per_destination):
            name = random.choice(activity_names)
            description = fake.sentence()
            date = fake.date_this_year()
            time = fake.time()
            cost = round(random.uniform(10, 500), 2)
            activity_id = Activity.create(
                CURSOR,
                destination_id=destination[0], 
                name=name, 
                date=date, 
                time=time, 
                cost=cost,
                description=description
            )
            activities.append(activity_id)
    print(f"{len(activities)} activities seeded.")
    return activities

# Function to seed expenses for each activity
def seed_expenses(activity_ids, num_per_activity=2):
    """Seed the expenses table with sample data for each activity."""
    expenses = []
    for activity_id in activity_ids:
        for _ in range(num_per_activity):
            amount = round(random.uniform(10, 500), 2)
            date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%m-%d-%Y")
            category = random.choice(["Food", "Transport", "Accommodation", "Entertainment"])
            expense = Expense.create(CURSOR, activity_id=activity_id, amount=amount, date=date, category=category)
            expenses.append(expense)
    print(f"{len(expenses)} expenses seeded.")
    return expenses

# Main seeding function to populate the database
def seed_all():
    """Seed the database with sample users, destinations, activities, and expenses."""
    # Initialize database with updated schema
    initialize_database()
    
    # Seed tables
    users = seed_users()  # Seed users first
    destinations = seed_destinations(users)  # Seed destinations with linked user_ids
    activities = seed_activities(destinations)  # Seed activities linked to destinations
    seed_expenses(activities)  # Seed expenses linked to activities by passing activity IDs directly
    print("Database seeding complete.")

# Run seeding if executed directly
if __name__ == "__main__":
    seed_all()





