import requests

from flask import redirect, session, flash
from functools import wraps

def usd(value):
    """Format value as USD."""
    # Handle None values
    if value is None:
        return "$0.00"
    
    # Convert to float if it's a string
    try:
        if isinstance(value, str):
            # Remove any existing dollar signs and commas
            value = value.replace('$', '').replace(',', '')
        value = float(value)
    except (ValueError, TypeError):
        return "$0.00"
    
    return f"${value:,.2f}"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# helper function to validate the inputs and check they are numbers
def validate_input(data):
    try:
        if data is None:
            value = 0.0
        else:
            value = float(data)
    except (TypeError, ValueError):
        return None
    return value
