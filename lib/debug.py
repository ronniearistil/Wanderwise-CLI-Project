from models.destination import Destination
from models.activity import Activity
from models.expense import Expense
from models.user import User
from models.__init__ import CONN, CURSOR
import ipdb

# Example usage for debugging
if __name__ == "__main__":
    # Create a new user
    user= User.find_by_id(CURSOR,3)
    ipdb.set_trace()
    user.destinations()
