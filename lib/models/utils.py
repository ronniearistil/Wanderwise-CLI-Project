from datetime import datetime
import re


# The utils.py file in the Travel Tracker CLI project serves as a collection of helper functions designed to streamline and simplify common tasks across the application. It includes utility functions for:
# 
# Formatting: Functions like format_currency and capitalize_words help standardize the display of monetary values and names, ensuring outputs look professional and consistent.
# 
# Validation: Functions like validate_date, validate_positive_number, and validate_email check user inputs for accuracy, reducing the risk of errors by validating dates, positive numbers, and email formats.
# 
# User Interaction: prompt_exit_option provides a convenient way for users to exit the program from any prompt, and print_divider adds visual separation in CLI output to improve readability.
# 
# Input Sanitization: sanitize_input ensures that user responses are cleaned and standardized, making the application more robust and user-friendly.