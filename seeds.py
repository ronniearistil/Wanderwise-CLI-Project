# seeds.py

from faker import Faker
from lib.models import Destination, Activity, Expense, CONN, CURSOR
import random
from datetime import datetime, timedelta

# Initialize Faker to generate random data
fake = Faker()

# Function to seed destinations
def seed_destinations(num=5):
    """Seed the destinations table with sample data."""
    destinations = []
    for _ in range(num):
        name = fake.city()
        country = fake.country()
        description = fake.text(max_nb_chars=50)  # Generate a description with Faker
        destination = Destination.create(name=name, country=country, description=description)  # Pass description
        # Fetch the last inserted row to get the ID
        CURSOR.execute("SELECT * FROM destinations WHERE id = (SELECT MAX(id) FROM destinations)")
        destination_record = CURSOR.fetchone()  # Fetch the full record with the ID
        destinations.append(destination_record)
    print(f"{num} destinations seeded.")
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
            name = random.choice(activity_names)  # Choose a relevant activity name
            description = fake.sentence()  # A brief description of the activity
            date = fake.date_this_year()   # A random date for the activity
            time = fake.time()             # A random time for the activity
            cost = round(random.uniform(10, 500), 2)  # Random cost
            activity = Activity.create(
                destination_id=destination[0], 
                name=name, 
                date=date, 
                time=time, 
                cost=cost,
                description=description
            )
            activities.append(activity)
    print(f"{len(activities)} activities seeded.")
    return activities

# Function to seed expenses for each activity
def seed_expenses(activity_ids, num_per_activity=2):
    """Seed the expenses table with sample data for each activity."""
    expenses = []
    for activity_id in activity_ids:
        for _ in range(num_per_activity):
            amount = round(random.uniform(10, 500), 2)  # Random expense amount
            date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")  # Random recent date
            category = random.choice(["Food", "Transport", "Accommodation", "Entertainment"])
            expense = Expense.create(activity_id=activity_id, amount=amount, date=date, category=category)
            expenses.append(expense)
    print(f"{len(expenses)} expenses seeded.")
    return expenses

# Main seeding function to populate the database
def seed_all():
    """Seed the database with sample destinations, activities, and expenses."""
    # Clear the tables to avoid duplicates during repeated seeding
    clear_tables()
    destinations = seed_destinations()
    activities = seed_activities(destinations)
    seed_expenses(activities)
    print("Database seeding complete.")

def clear_tables():
    """Clear all tables before seeding to avoid duplicate data."""
    CURSOR.execute("DELETE FROM expenses")
    CURSOR.execute("DELETE FROM activities")
    CURSOR.execute("DELETE FROM destinations")
    CONN.commit()
    print("Cleared all tables.")

# Run seeding if executed directly
if __name__ == "__main__":
    seed_all()



