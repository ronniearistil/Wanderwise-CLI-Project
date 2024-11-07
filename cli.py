import click
from lib.models.database import initialize_database
from lib.models.destination import Destination
from lib.models.activity import Activity
from lib.models.expense import Expense
from lib.helpers import ValidatorMixin