import csv
import datetime
import pytz
import requests
import urllib
import uuid

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    def get_status_text(status_code):
        status_dict = {
            100: "Continue",
            101: "Switching Protocols",
            200: "OK",
            201: "Created",
            202: "Accepted",
            204: "No Content",
            300: "Multiple Choices",
            301: "Moved Permanently",
            302: "Found",
            304: "Not Modified",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            500: "Internal Server Error",
            501: "Not Implemented",
            502: "Bad Gateway",
            503: "Service Unavailable",
            # Add more status codes as needed
        }

        return status_dict.get(status_code, "Unknown Status")
    return render_template("apology.html", code=code, message=escape(message), error=get_status_text(code)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def fetch_currency_rates():
    try:
        OPEN_EXCHANGE_APP_ID = '4df10bc3546eed55ff8e64bb'
        OPEN_EXCHANGE_API_URL = 'https://open.er-api.com/v6/latest/EGP'
        response = requests.get(OPEN_EXCHANGE_API_URL)
        response.raise_for_status()
        data = response.json()
        return data.get('rates', {})
    except requests.RequestException as e:
        apology("Error fetching currency rates: {e}",400)
        return {}

def lookup(currency,amount):
    """Look up rate for currency."""
    # Query API
    try:
        # Fetch the latest currency rates
        currency_rates_to_egp = fetch_currency_rates()
        if currency not in currency_rates_to_egp:
            return  apology("Invalid currency",400)
        egp_amount = amount * currency_rates_to_egp[currency]
        return egp_amount
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
