# helpers.py

from datetime import datetime
import re

class ValidatorMixin:
    """Mixin class for validation methods."""

    @staticmethod
    def validate_text(text):
        """Ensure the text is a non-empty string."""
        return isinstance(text, str) and len(text.strip()) > 0

    @staticmethod
    def validate_positive_number(value):
        """Ensure the value is a positive number."""
        return isinstance(value, (int, float)) and value > 0

    @staticmethod
    def validate_date(date_str):
        """Basic validation for date format YYYY-MM-DD."""
        return bool(re.match(r"\d{4}-\d{2}-\d{2}", date_str))
