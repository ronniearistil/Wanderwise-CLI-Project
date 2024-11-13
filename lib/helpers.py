# helpers.py
import re
from datetime import datetime

class ValidatorMixin:
    """Mixin class providing reusable validation methods."""

    @staticmethod
    def validate_text(text):
        """Ensure the text is a non-empty string."""
        if isinstance(text, str) and len(text.strip()) > 0:
            return text
        print("Text must be a non-empty string.")

    @staticmethod
    def validate_positive_number(value):
        """Ensure the value is a positive number."""
        if isinstance(value, (int, float)) and value >= 0:
            return value
        raise ValueError("Value must be a positive number.")

    @staticmethod
    def validate_date(date_str):
        """Ensure the date string is in a valid MM-DD-YYYY format."""
        if re.match(r"\d{2}-\d{2}-\d{4}", date_str):
            return date_str
        raise ValueError("Date must be in MM-DD-YYYY format.")

    @staticmethod
    def validate_email(email):
        """Basic email validation."""
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return email
        print ("Invalid email format.")

# Function to reformat date strings
def format_date(date_str):
    """Convert a date string from 'YYYY-MM-DD' to 'MM-DD-YYYY'."""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%m-%d-%Y")