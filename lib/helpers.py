from datetime import datetime


class ValidatorMixin:
    """Mixin class providing basic validation methods."""

    @staticmethod
    def validate_positive_number(value):
        """Ensure the value is a positive number."""
        if isinstance(value, (int, float)) and value >= 0:
            return value
        raise ValueError("Value must be a positive number.")

    @staticmethod
    def validate_date(date_str):
        """Ensure the date string is in a valid MM-DD-YYYY format."""
        try:
            datetime.strptime(date_str, "%m-%d-%Y")
            return date_str
        except ValueError:
            raise ValueError("Date must be in MM-DD-YYYY format.")

    @staticmethod
    def validate_text(value):
        """Ensure the value is a non-empty string."""
        if isinstance(value, str) and value.strip():
            return value
        raise ValueError("Text must be a non-empty string.")


# Function to reformat date strings
def format_date(date_str):
    """Convert a date string from 'YYYY-MM-DD' to 'MM-DD-YYYY'."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%m-%d-%Y")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")










