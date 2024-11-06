# client.py

from lib.models.database import CURSOR, CONN

class Client:
    all = []  # Track all client instances

    def __init__(self, name, contact_info, address):
        self.name = name  # Use the property setter
        self.contact_info = contact_info
        self.address = address
        type(self).all.append(self)  # Add instance to Client.all

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and value:
            self._name = value
        else:
            raise ValueError("Client name must be a non-empty string.")

    @property
    def contact_info(self):
        return self._contact_info

    @contact_info.setter
    def contact_info(self, value):
        if isinstance(value, str) and value:
            self._contact_info = value
        else:
            raise ValueError("Contact info must be a non-empty string.")

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if isinstance(value, str) and value:
            self._address = value
        else:
            raise ValueError("Address must be a non-empty string.")

    @classmethod
    def create(cls, name, contact_info, address):
        """Add a new client to the database and create a Client instance."""
        client = cls(name, contact_info, address)
        CURSOR.execute("INSERT INTO clients (name, contact_info, address) VALUES (?, ?, ?)", 
        (name, contact_info, address))
        CONN.commit()
        return client

    @classmethod
    def get_all(cls):
        """Retrieve all clients from the database."""
        CURSOR.execute("SELECT * FROM clients")
        return CURSOR.fetchall()

    def get_contracts(self):
        """Retrieve all contracts associated with this client."""
        CURSOR.execute("SELECT * FROM contracts WHERE client_id = ?", (self.id,))
        return CURSOR.fetchall()






