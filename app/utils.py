"""Helper utility functions for Energy Tracker."""
from datetime import datetime


def calculate_energy_kwh(power_watts, hours_used):
    """Calculate energy consumption in kWh.

    Args:
        power_watts: Power rating of appliance in watts
        hours_used: Number of hours appliance was used

    Returns:
        Energy consumption in kilowatt-hours (kWh)
    """
    return (power_watts * hours_used) / 1000


def calculate_monthly_bill(entries, rate_per_kwh):
    """Calculate total monthly electricity bill.

    Args:
        entries: List of energy entry dictionaries
        rate_per_kwh: Billing rate per kilowatt-hour

    Returns:
        Total bill amount
    """
    total_kwh = sum(entry["energy_kwh"] for entry in entries)
    return total_kwh * rate_per_kwh


def format_currency(amount):
    """Format amount as currency.

    Args:
        amount: Numeric amount

    Returns:
        Formatted currency string
    """
    return f"₹{amount:.2f}"


def validate_date(date_string):
    """Validate date string format.

    Args:
        date_string: Date in YYYY-MM-DD format

    Returns:
        True if valid, False otherwise
    """
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_positive_number(value, field_name="Value"):
    """Validate that a value is a positive number.

    Args:
        value: Value to validate
        field_name: Name of field for error message

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        num = float(value)
        if num <= 0:
            return False, f"{field_name} must be greater than 0"
        return True, None
    except (ValueError, TypeError):
        return False, f"{field_name} must be a valid number"


def get_month_name(month_number):
    """Convert month number to name.

    Args:
        month_number: Month as integer (1-12)

    Returns:
        Month name as string
    """
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    return (
        months[month_number - 1]
        if 1 <= month_number <= 12
        else "Unknown"
    )
