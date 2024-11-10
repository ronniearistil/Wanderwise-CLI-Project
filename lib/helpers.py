# helpers.py

import re

class ValidatorMixin:
    """Mixin class providing reusable validation methods."""

    @staticmethod
    def validate_text(text):
        """Ensure the text is a non-empty string."""
        if isinstance(text, str) and len(text.strip()) > 0:
            return text
        raise ValueError("Text must be a non-empty string.")

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
        raise ValueError("Invalid email format.")


