import click
from rich.console import Console
from rich.table import Table
from lib.models.destination import Destination
from lib.models.activity import Activity
from lib.models.expense import Expense
from lib.models.user import User
from lib.helpers import ValidatorMixin

# Initialize Rich console for enhanced CLI output
console = Console()

def prompt_input(prompt_text, input_type=str, validator=None):
    """
    Prompt the user for input with validation and options to quit ('q') or go back ('b').
    :param prompt_text: The text to display in the prompt.
    :param input_type: Expected type of input (e.g., str, int).
    :param validator: Optional validation function to apply on input.
    :return: User input if not 'q' or 'b'.
    """
    while True:
        response = click.prompt(f"{prompt_text} (or 'q' to quit, 'b' to go back)", type=input_type)
        
        # Exit or go back if 'q' or 'b' entered
        if str(response).lower() == 'q':
            console.print("[bold red]Exiting...[/bold red]")
            raise SystemExit
        elif str(response).lower() == 'b':
            console.print("[yellow]Going back to the main menu.[/yellow]")
            raise click.exceptions.Exit()

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
def add_user():
    """Add a new user."""
    try:
        name = prompt_input("Enter user name", validator=ValidatorMixin.validate_text)
        email = prompt_input("Enter user email", validator=ValidatorMixin.validate_text)
        User.create(name, email)
        console.print(f"[green]User '{name}' added successfully.[/green]")
    except click.exceptions.Exit:
        console.print("[yellow]Returned to main menu.[/yellow]")

@cli.command()
def add_destination():
    """Add a new destination for a user."""
    try:
        user_id = prompt_input("Enter user ID", int)
        name = prompt_input("Enter destination name", validator=ValidatorMixin.validate_text)
        location = prompt_input("Enter location", validator=ValidatorMixin.validate_text)
        description = prompt_input("Enter a short description", validator=ValidatorMixin.validate_text)
        
        Destination.create(name, location, description, user_id)
        console.print(f"[green]Destination '{name}' added successfully.[/green]")
    except click.exceptions.Exit:
        console.print("[yellow]Returned to main menu.[/yellow]")

@cli.command()
def add_activity():
    """Add a new activity for a destination."""
    try:
        destination_id = prompt_input("Enter destination ID", int)
        name = prompt_input("Enter activity name", validator=ValidatorMixin.validate_text)
        date = prompt_input("Enter date (YYYY-MM-DD)", validator=ValidatorMixin.validate_date)
        time = prompt_input("Enter time")
        cost = prompt_input("Enter activity cost", float, validator=ValidatorMixin.validate_positive_number)
        description = prompt_input("Enter a short description", validator=ValidatorMixin.validate_text)
        
        Activity.create(destination_id, name, date, time, cost, description)
        console.print(f"[green]Activity '{name}' added successfully.[/green]")
    except click.exceptions.Exit:
        console.print("[yellow]Returned to main menu.[/yellow]")

@cli.command()
def add_expense():
    """Add an expense for an activity."""
    try:
        activity_id = prompt_input("Enter activity ID", int)
        amount = prompt_input("Enter amount", float, validator=ValidatorMixin.validate_positive_number)
        category = prompt_input("Enter category", validator=ValidatorMixin.validate_text)
        description = prompt_input("Enter a short description", validator=ValidatorMixin.validate_text)
        date = prompt_input("Enter date (YYYY-MM-DD)", validator=ValidatorMixin.validate_date)

        Expense.create(activity_id, amount, date, category, description)
        console.print("[green]Expense added successfully.[/green]")
    except click.exceptions.Exit:
        console.print("[yellow]Returned to main menu.[/yellow]")

if __name__ == "__main__":
    cli()

