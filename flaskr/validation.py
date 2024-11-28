# validation.py contains functions that validate user input. These functions are used in the routes to validate the input before processing it. The functions are as follows:   
import re
from datetime import datetime

def is_not_empty(value):
    """
    Check if a value is not empty.

    Parameters:
        value (str): The value to check.

    Returns:
        bool: True if the value is not empty, False otherwise.
    """
    return bool(value and value.strip())

def is_valid_email(email):
    """
    Validate an email address.

    Parameters:
        email (str): The email address to validate.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_date(date_str):
    """
    Validate a date string.

    Parameters:
        date_str (str): The date string to validate.

    Returns:
        bool: True if the date string is valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def is_valid_integer(value):
    """
    Validate if a value is an integer.

    Parameters:
        value (str): The value to validate.

    Returns:
        bool: True if the value is an integer, False otherwise.
    """
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_valid_float(value):
    """
    Validate if a value is a float.

    Parameters:
        value (str): The value to validate.

    Returns:
        bool: True if the value is a float, False otherwise.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

def is_within_range(value, min_value, max_value):
    """
    Check if a value is within a specified range.

    Parameters:
        value (str): The value to check.
        min_value (float): The minimum value of the range.
        max_value (float): The maximum value of the range.

    Returns:
        bool: True if the value is within the range, False otherwise.
    """
    try:
        num = float(value)
        return min_value <= num <= max_value
    except ValueError:
        return False

def is_within_length(value, max_length):
    """
    Check if a value is within a specified length.

    Parameters:
        value (str): The value to check.
        max_length (int): The maximum length.

    Returns:
        bool: True if the value is within the length, False otherwise.
    """
    return len(value) <= max_length

def is_secure_password(password):
    """
    Validate if a password is secure.

    Parameters:
        password (str): The password to validate.

    Returns:
        bool: True if the password is secure, False otherwise.
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[\W_]', password):
        return False
    return True
