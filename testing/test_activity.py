import unittest
from lib.models.activity import Activity
from lib.models.destination import Destination
from lib.models.expense import Expense
from lib.models.user import User
from lib.database_setup import reset_and_seed_database, CONN, CURSOR

class TestActivity(unittest.TestCase):
    pass