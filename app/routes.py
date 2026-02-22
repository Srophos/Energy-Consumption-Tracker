"""Application routes for Energy Tracker."""

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from datetime import datetime
from .models import add_energy_entry, get_monthly_entries, get_current_rate, update_billing_rate
from .utils import (
    calculate_monthly_bill,
    format_currency,
    validate_date,
    validate_positive_number,
    get_month_name,
)

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET", "POST"])
def daily_entry():
    """Display daily entry form and handle submissions."""
    if request.method == "POST":
        # Get form data
        date = request.form.get("date")
        appliance = request.form.get("appliance")
        power_watts = request.form.get("power_watts")
        hours_used = request.form.get("hours_used")

        # Validation
        errors = []

        if not date or not validate_date(date):
            errors.append("Please provide a valid date")

        if not appliance or not appliance.strip():
            errors.append("Please provide an appliance name")

        is_valid_power, power_error = validate_positive_number(power_watts, "Power rating")
        if not is_valid_power:
            errors.append(power_error)

        is_valid_hours, hours_error = validate_positive_number(hours_used, "Hours used")
        if not is_valid_hours:
            errors.append(hours_error)

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "daily_entry.html",
                date=date,
                appliance=appliance,
                power_watts=power_watts,
                hours_used=hours_used,
            )

        # Add entry to database
        try:
            energy_kwh = add_energy_entry(
                current_app.config["DATABASE"],
                date,
                appliance.strip(),
                int(float(power_watts)),
                float(hours_used),
            )
            flash(f"Entry added successfully! Energy consumed: {energy_kwh:.2f} kWh", "success")

            # Redirect to dashboard for the month of the entry
            entry_date = datetime.strptime(date, "%Y-%m-%d")
            return redirect(url_for("main.dashboard", month=entry_date.month, year=entry_date.year))
        except Exception as e:
            flash(f"Error adding entry: {str(e)}", "error")
            return render_template("daily_entry.html")

    # GET request - show form with today's date as default
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template("daily_entry.html", date=today)


@bp.route("/dashboard")
def dashboard():
    """Display monthly consumption and bill."""
    # Get month and year from query params, default to current month
    now = datetime.now()
    month = request.args.get("month", now.month, type=int)
    year = request.args.get("year", now.year, type=int)

    # Validate month and year
    if not (1 <= month <= 12):
        month = now.month
    if not (2000 <= year <= 2100):
        year = now.year

    # Get entries for the month
    entries = get_monthly_entries(current_app.config["DATABASE"], month, year)

    # Get current billing rate
    rate = get_current_rate(current_app.config["DATABASE"])

    # Calculate total bill
    total_bill = calculate_monthly_bill(entries, rate) if entries else 0
    total_kwh = sum(entry["energy_kwh"] for entry in entries) if entries else 0

    # Format data for display
    month_name = get_month_name(month)

    return render_template(
        "dashboard.html",
        entries=entries,
        month=month,
        year=year,
        month_name=month_name,
        total_kwh=total_kwh,
        rate_per_kwh=rate,
        total_bill=total_bill,
        format_currency=format_currency,
    )


@bp.route("/health")
def health():
    """Health check endpoint for deployment verification."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}, 200
