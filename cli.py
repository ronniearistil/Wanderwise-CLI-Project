import click
from rich.console import Console
from rich.table import Table
from lib.models.destination import Destination
from lib.models.activity import Activity
from lib.models.expense import Expense
from lib.models.user import User
from lib.helpers import ValidatorMixin, format_date  # Import format_date function

# Initialize Rich console for enhanced CLI output
console = Console()

def prompt_input(prompt_text, input_type=str, validator=None):
    """
    Prompt the user for input with validation.
    """
    while True:
        response = click.prompt(f"{prompt_text} (or 'e' to exit, 'b' to go back)", type=input_type)
        
        if str(response).lower() == 'e':
            console.print("[bold red]Exiting...[/bold red]")
            raise SystemExit
        elif str(response).lower() == 'b':
            console.print("[yellow]Returning to the main menu.[/yellow]")
            return 'b'

        # Validate input if a validator function is provided
        if validator and not validator(response):
            console.print("[red]Invalid input. Please try again.[/red]")
        else:
            return response

@click.group()
def cli():
    """Wanderwise CLI for managing users, destinations, activities, and expenses."""
    pass

@cli.command()
def main_menu():
    """Main menu for Wanderwise CLI."""
    while True:
        console.print("\n[cyan bold]Welcome to Wanderwise CLI[/cyan bold]")
        console.print("Select an option:")
        console.print("1. Add User")
        console.print("2. Add Destination")
        console.print("3. Add Activity")
        console.print("4. Add Expense")
        console.print("e. Exit")

        choice = click.prompt("Enter choice", type=str).lower()

        if choice == '1':
            add_user()
        elif choice == '2':
            add_destination()
        elif choice == '3':
            add_activity()
        elif choice == '4':
            add_expense()
        elif choice == 'e':
            console.print("[bold red]Exiting...[/bold red]")
            break
        else:
            console.print("[red]Invalid choice. Please select a valid option.[/red]")

def select_destination():
    """Allow user to select an existing destination."""
    destinations = Destination.get_all()  # Fetch all destinations
    if not destinations:
        console.print("[yellow]No destinations available. Add a destination first.[/yellow]")
        return None

    console.print("\nAvailable Destinations:")
    for idx, dest in enumerate(destinations, start=1):
        console.print(f"{idx}. {dest[1]} in {dest[2]}")  # Assuming dest[1] is name, dest[2] is location

    choice = prompt_input("Select a destination by number", int)
    if 1 <= choice <= len(destinations):
        return destinations[choice - 1][0]  # Return the selected destination ID
    else:
        console.print("[red]Invalid choice. Please select a valid destination number.[/red]")
        return select_destination()

def add_user():
    """Add a new user."""
    console.print("\n[cyan bold]Add User[/cyan bold]")
    try:
        name = prompt_input("Enter user name", validator=ValidatorMixin.validate_text)
        if name == 'b':
            return
        email = prompt_input("Enter user email", validator=ValidatorMixin.validate_text)
        if email == 'b':
            return
        User.create(CURSOR, name, email)
        console.print(f"[green]User '{name}' added successfully.[/green]")
    except click.exceptions.Exit:
        console.print("[yellow]Returned to main menu.[/yellow]")

def add_destination():
    """Add a new destination for a user."""
    console.print("\n[cyan bold]Add Destination[/cyan bold]")
    try:
        name = prompt_input("Enter destination name", validator=ValidatorMixin.validate_text)
        if name == 'b':
            return
        location = prompt_input("Enter location", validator=ValidatorMixin.validate_text)
        if location == 'b':
            return
        description = prompt_input("Enter a short description", validator=ValidatorMixin.validate_text)
        if description == 'b':
            return

        existing_destination = Destination.find_by_name_and_location(name, location)
        if existing_destination:
            console.print(f"[yellow]Destination '{name}' in '{location}' already exists.[/yellow]")
        else:
            Destination.create(CURSOR, name, location, description)
            console.print(f"[green]Destination '{name}' added successfully.[/green]")
    except click.exceptions.Exit:
        console.print("[yellow]Returned to main menu.[/yellow]")

def add_activity():
    """Add a new activity for a destination."""
    console.print("\n[cyan bold]Add Activity[/cyan bold]")
    try:
        destination_id = select_destination()
        if not destination_id:
            return  # No destination selected

        name = prompt_input("Enter activity name", validator=ValidatorMixin.validate_text)
        if name == 'b':
            return
        date = prompt_input("Enter date (MM-DD-YYYY)", validator=ValidatorMixin.validate_date)
        if date == 'b':
            return
        time = prompt_input("Enter time")
        if time == 'b':
            return
        cost = prompt_input("Enter activity cost", float, validator=ValidatorMixin.validate_positive_number)
        if cost == 'b':
            return
        description = prompt_input("Enter a short description", validator=ValidatorMixin.validate_text)
        if description == 'b':
            return

        Activity.create(CURSOR, destination_id, name, date, time, cost, description)
        console.print(f"[green]Activity '{name}' added successfully.[/green]")
    except click.exceptions.Exit:
        console.print("[yellow]Returned to main menu.[/yellow]")

def add_expense():
    """Add an expense for an activity."""
    console.print("\n[cyan bold]Add Expense[/cyan bold]")
    try:
        activity_id = prompt_input("Enter activity ID", int)
        if activity_id == 'b':
            return
        amount = prompt_input("Enter amount", float, validator=ValidatorMixin.validate_positive_number)
        if amount == 'b':
            return
        category = prompt_input("Enter category", validator=ValidatorMixin.validate_text)
        if category == 'b':
            return
        description = prompt_input("Enter a short description", validator=ValidatorMixin.validate_text)
        if description == 'b':
            return
        date = prompt_input("Enter date (MM-DD-YYYY)", validator=ValidatorMixin.validate_date)
        if date == 'b':
            return
        Expense.create(CURSOR, activity_id, amount, date, category, description)
        console.print("[green]Expense added successfully.[/green]")
    except click.exceptions.Exit:
        console.print("[yellow]Returned to main menu.[/yellow]")

if __name__ == "__main__":
    main_menu()






