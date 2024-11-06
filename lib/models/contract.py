# contract.py

class Contract:
    all = []  # Track all contract instances

    def __init__(self, client_id, description, start_date, end_date, amount, status='active'):
        self.client_id = client_id
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.amount = amount
        self.status = status
        type(self).all.append(self)  # Add instance to Contract.all

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if isinstance(value, str) and value:
            self._description = value
        else:
            raise ValueError("Contract description must be a non-empty string.")

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if isinstance(value, (int, float)) and value > 0:
            self._amount = value
        else:
            raise ValueError("Amount must be a positive number.")

    @classmethod
    def create(cls, client_id, description, start_date, end_date, amount, status='active'):
        """Add a new contract to the database and create a Contract instance."""
        contract = cls(client_id, description, start_date, end_date, amount, status)
        CURSOR.execute('''INSERT INTO contracts (client_id, description, start_date, end_date, amount, status) 
                        VALUES (?, ?, ?, ?, ?, ?)''', 
        (client_id, description, start_date, end_date, amount, status))
        CONN.commit()
        return contract

    @classmethod
    def get_all(cls):
        """Retrieve all contracts from the database."""
        CURSOR.execute("SELECT * FROM contracts")
        return CURSOR.fetchall()

    def get_payments(self):
        """Retrieve all payments associated with this contract."""
        CURSOR.execute("SELECT * FROM payments WHERE contract_id = ?", (self.id,))
        return CURSOR.fetchall()




