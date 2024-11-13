import click
from rich.console import Console
from rich.table import Table
from lib.models.destination import Destination
from lib.models.activity import Activity
from lib.models.expense import Expense
from lib.models.user import User
from lib.helpers import ValidatorMixin
from lib.models.database import CURSOR

console = Console()

def prompt_input(prompt_text, input_type=str, validator=None, optional=False):
    """Prompt for input with validation, allowing 'b' to go back and 'e' to exit."""
    while True:
        response = click.prompt(f"{prompt_text} (or 'e' to exit, 'b' to go back)", default='', show_default=False)
        if response.lower() == 'e':
            console.print("[bold red]Exiting...[/bold red]")
            raise SystemExit
        elif response.lower() == 'b':
            console.print("[yellow]Returning to the previous menu.[/yellow]")
            return 'b'

        if optional and not response:
            return None  # Allow empty input if marked optional

        try:
            response = input_type(response)
        except ValueError:
            console.print(f"[red]Invalid input. Please enter a valid {input_type.__name__} or 'b' to go back.[/red]")
            continue

        if validator and not validator(response):
            console.print("[red]Invalid input. Please try again.[/red]")
        else:
            return response

def display_menu(options, menu_name="Main"):
    """Display menu options with a dynamic headline."""
    console.print(f"\n[cyan bold]Welcome to Wanderwise! Please select an option from the {menu_name} menu to proceed.[/cyan bold]")
    for key, description in options.items():
        console.print(f"{key}. {description}")
    console.print("e. Exit")
    return click.prompt("Enter choice", type=str).lower()

@click.group()
def cli():
    """Wanderwise CLI for managing users, destinations, activities, and expenses."""
    pass

@cli.command()
def main_menu():
    while True:
        choice = display_menu({
            "1": "User Management",
            "2": "Destination Management",
            "3": "Activity Management",
            "4": "Expense Management"
        })

        if choice == '1':
            user_management_menu()
        elif choice == '2':
            destination_management_menu()
        elif choice == '3':
            activity_management_menu()
        elif choice == '4':
            expense_management_menu()
        elif choice == 'e':
            console.print("[bold red]Exiting...[/bold red]")
            break

### Core Management Menus

def user_management_menu():
    management_menu("User", User, {
        "name": "Enter user name",
        "email": "Enter user email"
    })

def destination_management_menu():
    management_menu("Destination", Destination, {
        "name": "Enter destination name",
        "location": "Enter location",
        "description": "Enter description",
        "user_id": "Enter user ID"
    })

def activity_management_menu():
    management_menu("Activity", Activity, {
        "destination_id": "Enter destination ID",
        "name": "Enter activity name",
        "date": "Enter date (MM-DD-YYYY)",
        "time": "Enter time",
        "cost": "Enter activity cost",
        "description": "Enter description"
    })

def expense_management_menu():
    management_menu("Expense", Expense, {
        "activity_id": "Enter activity ID",
        "amount": "Enter amount",
        "date": "Enter date (MM-DD-YYYY)",
        "category": "Enter category",
        "description": "Enter description"
    })

### Generalized Management Menu

def management_menu(name, model, fields):
    while True:
        choice = display_menu({
            "1": f"Add {name}",
            "2": f"View {name}s",
            "3": f"Edit {name}",
            "4": f"Delete {name}"
        }, f"{name} Management")

        if choice == '1':
            add_entry(model, fields)
        elif choice == '2':
            view_entries(model, name)
        elif choice == '3':
            edit_entry(model, name, fields)
        elif choice == '4':
            delete_entry(model, name)
        elif choice == 'e':
            break

def add_entry(model, fields):
    """Add a new entry based on provided fields."""
    data = {key: prompt_input(label, validator=ValidatorMixin.validate_text) for key, label in fields.items()}
    model.create(CURSOR, **data)
    console.print(f"[green]{model.__name__} added successfully.[/green]")

def view_entries(model, name):
    """View entries in a table format."""
    entries = model.get_all(CURSOR)
    if entries:
        table = Table(title=f"{name}s")
        column_names = [desc[0] for desc in CURSOR.description]  # Fetch column names
        for col_name in column_names:
            table.add_column(col_name.capitalize(), justify="left")
        for entry in entries:
            table.add_row(*map(str, entry))
        console.print(table)
    else:
        console.print(f"[yellow]No {name.lower()}s found.[/yellow]")

def edit_entry(model, name, fields):
    """Edit an existing entry with optional fields."""
    entry_id = prompt_input(f"Enter {name.lower()} ID to edit", int)
    existing_entry = model.find_by_id(CURSOR, entry_id)
    if not existing_entry:
        console.print(f"[red]{name} ID '{entry_id}' not found.[/red]")
        return

    console.print("[yellow]Leave field empty to keep current value.[/yellow]")
    updated_data = handle_edit_fields(fields, dict(zip(CURSOR.description, existing_entry)))
    model.update(CURSOR, entry_id, **updated_data)
    console.print(f"[green]{name} ID '{entry_id}' updated successfully.[/green]")

def delete_entry(model, name):
    """Delete an entry by ID with confirmation."""
    entry_id = prompt_input(f"Enter {name.lower()} ID to delete", int)
    if click.confirm(f"Are you sure you want to delete this {name.lower()}?"):
        model.delete(CURSOR, entry_id)
        console.print(f"[green]{name} ID '{entry_id}' deleted successfully.[/green]")

if __name__ == "__main__":
    main_menu()














