from lib.models.database import CURSOR, CONN

class Payment:
    all = []  # Track all payment instances

    def __init__(self, contract_id, amount, payment_date, status='pending'):
        self.contract_id = contract_id
        self.amount = amount
        self.payment_date = payment_date
        self.status = status
        type(self).all.append(self)  # Add instance to Payment.all

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if isinstance(value, (int, float)) and value > 0:
            self._amount = value
        else:
            raise ValueError("Amount must be a positive number.")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, str) and value in ["pending", "completed"]:
            self._status = value
        else:
            raise ValueError("Status must be 'pending' or 'completed'.")

    @classmethod
    def create(cls, contract_id, amount, payment_date, status='pending'):
        """Add a new payment to the database and create a Payment instance."""
        payment = cls(contract_id, amount, payment_date, status)
        CURSOR.execute("INSERT INTO payments (contract_id, amount, payment_date, status) VALUES (?, ?, ?, ?)", 
        (contract_id, amount, payment_date, status))
        CONN.commit()
        return payment

    @classmethod
    def get_all(cls):
        """Retrieve all payments from the database."""
        CURSOR.execute("SELECT * FROM payments")
        return CURSOR.fetchall()

