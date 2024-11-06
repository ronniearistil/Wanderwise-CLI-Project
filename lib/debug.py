# debug.py

from lib.models.destination import Destination
from lib.models.activity import Activity
from lib.models.expense import Expense

# Example usage for debugging

# Add a test destination
destination_id = Destination.create("Paris", "France", "The city of lights")
print(f"Destination added: {Destination.get_all()}")

# Add a test activity for the above destination
activity_id = Activity.create(destination_id=destination_id, name="Eiffel Tower Visit", date="2023-11-07", time="10:00", cost=25.0, description="Visit the Eiffel Tower")
print(f"Activity added: {Activity.get_by_destination(destination_id)}")

# Add a test expense for the above activity
expense_id = Expense.create(activity_id=activity_id, amount=15.5, date="2023-11-07", category="Transport", description="Taxi to Eiffel Tower")
print(f"Expense added: {Expense.get_by_activity(activity_id)}")

