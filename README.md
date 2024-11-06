# Freelancer Contract Management Tool

## Overview

The **Freelancer Contract Management Tool** is a command-line interface (CLI) application designed to help freelancers manage client information, track contract details, and log payments efficiently. Built using Python and SQLite, this application provides an organized way to maintain records for clients, contracts, and payments in a single database.

## Features

- **Add Clients**: Add a new client with validated input fields (name, contact info, and address).
- **Manage Contracts**: Add contracts linked to specific clients, specifying details such as contract description, start and end dates, and amount.
- **Record Payments**: Track payments for each contract, specifying payment amount, date, and status.
- **List All Entries**: Display lists of clients, contracts, and payments.
- **View Client-Specific Contracts**: Retrieve all contracts associated with a particular client.
- **Graceful Exit**: Quit any command or the CLI itself at any time without errors.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url>
   cd Freelancer-Contract-Management-Tool

## Install Dependencies: 
The project uses pipenv for dependency management. Install pipenv if you don’t have it: pip install pipenv

## Then, install the project dependencies: 
pipenv install

## Activate the Virtual Environment:
pipenv shell

## Initialize the Database: 
The database is automatically initialized when you start the CLI for the first time. This will create the necessary tables for clients, contracts, and payments.

## Usage
Running the CLI
Start the CLI by executing:
python cli.py

## Available Commands
- add-client: Add a new client.
- list-clients: Display all clients.
- add-contract: Add a contract for a specific client.
- list-contracts: Display all contracts.
- add-payment: Record a payment for a contract.
- list-payments: Display all payments.
- list-client-contracts: Show contracts associated with a specific client.
- exit: Exit the CLI application.

## Example Usage
- python cli.py add-client
<!-- Follow prompts to enter client name, contact info, and address -->

python cli.py list-clients
# Display all stored clients

## Project Structure
Freelancer-Contract-Management-Tool/
│
├── cli.py                 # Main CLI file containing command definitions
├── lib/
│   └── models/
│       ├── client.py      # Client model class
│       ├── contract.py    # Contract model class
│       ├── payment.py     # Payment model class
│       └── database.py    # Database setup and initialization
├── Pipfile                # Pipenv dependency file
├── Pipfile.lock           # Dependency lock file
└── README.md              # Project documentation

## Data Validation and Requirements
- **Client Name**: Must be a non-empty string.
- **Contract Amount**: Must be a positive number.
- **Payment Status**: Acceptable values are "pending" or "completed".

Testing and Error Handling
The application includes basic error handling and input validation for each command. You can test each command by intentionally providing invalid inputs (e.g., non-integer values for client_id or invalid date formats). Error messages will display when inputs are invalid.