# cli.py

import click
from lib.models.database import initialize_database
from lib.models.client import Client
from lib.models.contract import Contract
from lib.models.payment import Payment

# Initialize database at startup
initialize_database()

@click.group()
def cli():
    """CLI for managing clients, contracts, and payments."""
    pass

@cli.command()
def add_client():
    """Add a new client with validated input."""
    try:
        name = click.prompt("Enter client name (or type 'q' to quit)")
        if name.lower() in ["q", "quit"]:
            click.echo("Exiting...")
            return

        contact_info = click.prompt("Enter contact info (or type 'q' to quit)")
        if contact_info.lower() in ["q", "quit"]:
            click.echo("Exiting...")
            return

        address = click.prompt("Enter address (or type 'q' to quit)")
        if address.lower() in ["q", "quit"]:
            click.echo("Exiting...")
            return

        Client.create(name, contact_info, address)
        click.echo(f"Client '{name}' added successfully.")
    except ValueError as ve:
        click.echo(f"Error: {ve}")
    except Exception as e:
        click.echo(f"An error occurred: {e}")

@cli.command()
def add_contract():
    """Add a new contract for a client, with validation."""
    try:
        client_id = click.prompt("Enter client ID (or type 'q' to quit)", type=int)
        if client_id == 'q':
            return

        description = click.prompt("Enter contract description (or type 'q' to quit)")
        start_date = click.prompt("Enter start date (YYYY-MM-DD) (or type 'q' to quit)")
        end_date = click.prompt("Enter end date (YYYY-MM-DD) (or type 'q' to quit)")
        amount = click.prompt("Enter contract amount (or type 'q' to quit)", type=float)

        Contract.create(client_id, description, start_date, end_date, amount)
        click.echo("Contract added successfully.")
    except ValueError as ve:
        click.echo(f"Error: {ve}")
    except Exception as e:
        click.echo(f"An error occurred: {e}")

@cli.command()
def add_payment():
    """Add a new payment for a contract, with validation."""
    try:
        contract_id = click.prompt("Enter contract ID (or type 'q' to quit)", type=int)
        amount = click.prompt("Enter payment amount (or type 'q' to quit)", type=float)
        payment_date = click.prompt("Enter payment date (YYYY-MM-DD) (or type 'q' to quit)")
        status = click.prompt("Enter payment status (default 'pending')", default="pending")

        Payment.create(contract_id, amount, payment_date, status)
        click.echo("Payment added successfully.")
    except ValueError as ve:
        click.echo(f"Error: {ve}")
    except Exception as e:
        click.echo(f"An error occurred: {e}")

# List commands and other functionalities would remain similar to previous versions.

@cli.command()
def exit():
    """Exit the CLI."""
    click.echo("Goodbye!")
    raise SystemExit

if __name__ == "__main__":
    cli()




