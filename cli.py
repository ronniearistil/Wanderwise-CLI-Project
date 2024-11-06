import click
from lib.models.database import initialize_database
from lib.models.destination import Destination
from lib.models.activity import Activity
from lib.models.expense import Expense
from lib.helpers import ValidatorMixin

class TravelCLI(ValidatorMixin):
    def __init__(self):
        initialize_database()

    def prompt_input(self, prompt_text, input_type=str):
        """Prompt user for input and exit if 'q' is entered."""
        response = click.prompt(f"{prompt_text} (or 'q' to quit)", type=input_type)
        if str(response).lower() == 'q':
            click.echo("Exiting...")
            raise SystemExit
        return response

    @click.group()
    def cli():
        """Travel Tracker CLI for managing destinations, activities, and expenses."""
        pass

    @cli.command()
    def add_destination():
        """Add a new destination."""
        name = TravelCLI().prompt_input("Enter destination name")
        country = TravelCLI().prompt_input("Enter country")
        description = TravelCLI().prompt_input("Enter a short description")

        if not TravelCLI.validate_text(name) or not TravelCLI.validate_text(country):
            click.echo("Invalid input for name or country.")
            return
        
        Destination.create(name, country, description)
        click.echo(f"Destination '{name}' added successfully.")

    @cli.command()
    def list_destinations():
        """List all destinations."""
        destinations = Destination.get_all()
        for destination in destinations:
            click.echo(destination)

    @cli.command()
    def add_activity():
        """Add a new activity for a destination."""
        destination_id = TravelCLI().prompt_input("Enter destination ID", int)
        name = TravelCLI().prompt_input("Enter activity name")
        date = TravelCLI().prompt_input("Enter date (YYYY-MM-DD)")
        time = TravelCLI().prompt_input("Enter time")
        cost = TravelCLI().prompt_input("Enter activity cost", float)

        if not TravelCLI.validate_positive_number(cost):
            click.echo("Cost must be a positive number.")
            return

        Activity.create(destination_id, name, date, time, cost)
        click.echo(f"Activity '{name}' added successfully.")

    @cli.command()
    def list_activities():
        """List all activities for a specific destination."""
        destination_id = TravelCLI().prompt_input("Enter destination ID", int)
        activities = Activity.get_by_destination(destination_id)
        for activity in activities:
            click.echo(activity)

    @cli.command()
    def add_expense():
        """Add an expense for an activity."""
        activity_id = TravelCLI().prompt_input("Enter activity ID", int)
        amount = TravelCLI().prompt_input("Enter amount", float)
        description = TravelCLI().prompt_input("Enter expense description")

        if not TravelCLI.validate_positive_number(amount):
            click.echo("Amount must be a positive number.")
            return

        Expense.create(activity_id, amount, description)
        click.echo("Expense added successfully.")

if __name__ == "__main__":
    TravelCLI().cli()


