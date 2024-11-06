# seeds.py

from faker import Faker
from lib.models.client import Client
from lib.models.contract import Contract
from lib.models.payment import Payment
import random

fake = Faker()

def seed_clients(num=5):
    for _ in range(num):
        Client.create(fake.name(), fake.phone_number(), fake.address())
    print(f"{num} clients seeded.")

def seed_contracts(num=5):
    for _ in range(num):
        client_id = random.randint(1, 5)
        Contract.create(client_id, fake.catch_phrase(), fake.date(), fake.date(), random.uniform(500, 5000))
    print(f"{num} contracts seeded.")

def seed_payments(num=5):
    for _ in range(num):
        contract_id = random.randint(1, 5)
        Payment.create(contract_id, random.uniform(100, 1000), fake.date())
    print(f"{num} payments seeded.")

if __name__ == "__main__":
    seed_clients()
    seed_contracts()
    seed_payments()
    print("Database seeding complete.")


