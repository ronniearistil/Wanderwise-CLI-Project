# debug.py

from lib.models.client import Client
from lib.models.contract import Contract
from lib.models.payment import Payment

# Example usage for debugging
Client.create("John Doe", "123-456-7890", "123 Main St")
print(Client.get_all())
