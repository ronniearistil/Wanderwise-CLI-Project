import click
from rich.console import Console
from rich.table import Table
from lib.models.destination import Destination
from lib.models.activity import Activity
from lib.models.expense import Expense
from lib.models.user import User
from lib.helpers import ValidatorMixin, format_date
from lib.models.database import CURSOR, CONN

console = Console()

def prompt_input(prompt_text, input_type=str, optional=False):
    """Prompt for input with validation and error handling."""
    while True:
        response = click.prompt(f"{prompt_text} (or 'e' to exit, 'b' to go back)", default='', show_default=False)
        if response.lower() == 'e':
            console.print("[bold red]Exiting...[/bold red]")
            raise SystemExit
        elif response.lower() == 'b':
            console.print("[yellow]Returning to the previous menu.[/yellow]")
            return 'b'
        if optional and not response:
            return None

        try:
            return input_type(response)
        except ValueError:
            console.print(f"[red]Invalid input. Please enter a valid {input_type.__name__}.[/red]")

def display_menu(options, menu_name="Main", show_welcome=True):
    """Display a menu with the provided options, with an optional welcome message."""
    if show_welcome:
        console.print(f"\n[cyan bold]Welcome to Wanderwise! Select an option from the {menu_name} menu.[/cyan bold]")
    else:
        console.print(f"\n[cyan bold]Select an option from the {menu_name} menu.[/cyan bold]")
    
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
    """Main menu for navigating management menus."""
    while True:
        choice = display_menu({
            "1": "User Management",
            "2": "Destination Management",
            "3": "Activity Management",
            "4": "Expense Management"
        }, "Main", show_welcome=True)  # Show welcome only for the main menu
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

def management_menu(name, model, fields):
    """Display CRUD options for each model."""
    while True:
        choice = display_menu({
            "1": f"Add {name}",
            "2": f"View {name}s",
            "3": f"Edit {name}",
            "4": f"Delete {name}"
        }, f"{name} Management", show_welcome=False)  # No welcome message for submenus
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

# Define management menus for each model
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
        "user_id": "Enter user ID,"
    })

def activity_management_menu():
    management_menu("Activity", Activity, {
        "destination_id": "Enter destination ID",
        "name": "Enter activity name",
        "date": "Enter date (MM-DD-YYYY)",
        # "time": "Enter time",
        "time": "Enter time (optional)",
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
def add_entry(model, fields):
    """Add a new entry with proper validation."""
    data = {}
    for key, label in fields.items():
        value = prompt_input(label, optional=(key == "time"))  # Make 'time' optional

        if key == "cost":  # Explicit handling for cost
            try:
                value = float(value)  # Convert cost to float
                if value < 0:
                    console.print("[red]Cost must be a non-negative number.[/red]")
                    return
            except ValueError:
                console.print("[red]Invalid Cost: Must be a number.[/red]")
                return
        # Handle optional 'time' field
        if key == "time" and not value:
            value = None
        # Handle required fields
        if not value:
            console.print(f"[red]Invalid {key.capitalize()}: This field is required.[/red]")
            return
        data[key] = value
    try:
        entry = model.create(**data)
        if entry:
            console.print(f"[green]{model.__name__} added successfully with ID {entry.id}.[/green]")
        else:
            console.print(f"[red]Failed to add {model.__name__}: Unknown error.[/red]")
    except Exception as e:
        console.print(f"[red]Error creating {model.__name__}: {str(e)}[/red]")
def view_entries(model, name):
    """Display all entries in a table format."""
    try:
        entries = model.get_all()
        if not entries:
            console.print(f"[yellow]No {name.lower()}s found.[/yellow]")
            return

        table = Table(title=f"{name}s")
        # Add columns dynamically based on the model attributes
        attributes = vars(entries[0]).keys()
        for attr in attributes:
            table.add_column(attr.capitalize())

        # Add rows dynamically
        for entry in entries:
            row = [str(getattr(entry, attr)) for attr in attributes]
            table.add_row(*row)

        console.print(table)
    except Exception as e:
        console.print(f"[red]Error displaying {name}s: {e}[/red]")

def edit_entry(model, name, fields):
    """Edit an existing entry."""
    entry_id = prompt_input(f"Enter {name.lower()} ID to edit", int)
    existing_entry = model.find_by_id(entry_id)
    if not existing_entry:
        console.print(f"[red]{name} ID '{entry_id}' not found.[/red]")
        return
    console.print("[yellow]Leave field empty to keep current value.[/yellow]")
    updated_data = {
        key: prompt_input(f"{label} [Current: {getattr(existing_entry, key)}]", optional=True) or getattr(existing_entry, key)
        for key, label in fields.items()
    }
    try:
        model.update(entry_id, **updated_data)
        console.print(f"[green]{name} ID '{entry_id}' updated successfully.[/green]")
    except Exception as e:
        console.print(f"[red]Error updating {name}: {e}[/red]")

def delete_entry(model, name):
    """Delete an entry by ID."""
    entry_id = prompt_input(f"Enter {name.lower()} ID to delete", int)
    if click.confirm(f"Are you sure you want to delete this {name.lower()}?"):
        try:
            model.delete(entry_id)
            console.print(f"[green]{name} ID '{entry_id}' deleted successfully.[/green]")
        except Exception as e:
            console.print(f"[red]Error deleting {name}: {e}[/red]")

if __name__ == "__main__":
    main_menu()
