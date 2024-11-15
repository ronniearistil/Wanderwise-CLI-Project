# seeds.py

from faker import Faker
from lib.models import CONN, CURSOR
from lib.models.destination import Destination 
from lib.models.activity import Activity 
from lib.models.expense import Expense 
from lib.models.user import User 
import random
from datetime import datetime, timedelta

# Initialize Faker to generate random data
fake = Faker()

def initialize_database():
    """Initialize the database by dropping and recreating all tables."""
    User.drop_table()
    Destination.drop_table()
    Activity.drop_table()
    Expense.drop_table()
    User.create_table()
    Destination.create_table()
    Activity.create_table()
    Expense.create_table()
    print("Database initialized with tables created.")

def seed_users(num=3):
    """Seed the users table with sample data."""
    users = []
    for _ in range(num):
        name = fake.name()
        email = fake.email()
        user = User.create(name=name, email=email)
        CURSOR.execute("SELECT * FROM users WHERE id = (SELECT MAX(id) FROM users)")
        user_record = CURSOR.fetchone()
        users.append(user_record)
    print(f"{num} users seeded.")
    return users

def seed_destinations(users, num=5):
    """Seed the destinations table with sample data linked to users."""
    destinations = []
    for user in users:
        for _ in range(num):
            name = fake.city()
            location = fake.country()
            description = fake.text(max_nb_chars=50)
            destination = Destination.create(name, location, description, user[0])
            CURSOR.execute("SELECT * FROM destinations WHERE id = (SELECT MAX(id) FROM destinations)")
            destination_record = CURSOR.fetchone()
            destinations.append(destination_record)
    print(f"{num * len(users)} destinations seeded.")
    return destinations

def seed_activities(destinations, num_per_destination=3):
    """Seed the activities table with sample data for each destination."""
    activity_ids = []
    activity_names = [
        "City Tour", "Museum Visit", "Hiking", "Beach Day", 
        "Scuba Diving", "Wine Tasting", "Sightseeing", 
        "Shopping", "Cultural Experience", "Boat Ride"
    ]
    for destination in destinations:
        for _ in range(num_per_destination):
            name = random.choice(activity_names)
            description = fake.sentence()
            date = str(fake.date_this_year())
            time = fake.time()
            cost = round(random.uniform(10, 500), 2)
            activity = Activity.create(
                destination_id=destination[0], 
                name=name, 
                date=date, 
                time=time, 
                cost=cost,
                description=description
            )
            activity_ids.append(activity.id)  # Append the ID of the activity
    print(f"{len(activity_ids)} activities seeded.")
    return activity_ids

def seed_expenses(activity_ids, num_per_activity=2):
    """Seed the expenses table with sample data for each activity."""
    expenses = []
    for activity_id in activity_ids:
        for _ in range(num_per_activity):
            amount = round(random.uniform(10, 500), 2)
            date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%m-%d-%Y")
            category = random.choice(["Food", "Transport", "Accommodation", "Entertainment"])
            expense = Expense.create(activity_id=activity_id, amount=amount, date=date, category=category)
            expenses.append(expense)
    print(f"{len(expenses)} expenses seeded.")
    return expenses

def seed_all():
    """Seed the database with sample users, destinations, activities, and expenses."""
    initialize_database()
    users = seed_users()
    destinations = seed_destinations(users)
    activities = seed_activities(destinations)
    seed_expenses(activities)
    print("Database seeding complete.")

if __name__ == "__main__":
    seed_all()





