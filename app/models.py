"""Database models and initialization for Energy Tracker."""

import sqlite3
from contextlib import closing
from datetime import datetime


def get_db_connection(db_path):
    """Create a database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path):
    """Initialize the database schema."""
    with closing(get_db_connection(db_path)) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS energy_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                appliance TEXT NOT NULL,
                power_watts INTEGER NOT NULL,
                hours_used REAL NOT NULL,
                energy_kwh REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS billing_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rate_per_kwh REAL NOT NULL,
                effective_date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX IF NOT EXISTS idx_entry_date ON energy_entries(date);
        """)

        # Insert default billing rate if not exists
        cursor = conn.execute("SELECT COUNT(*) FROM billing_rates")
        if cursor.fetchone()[0] == 0:
            conn.execute(
                "INSERT INTO billing_rates (rate_per_kwh, effective_date) VALUES (?, ?)",
                (7.5, datetime.now().strftime("%Y-%m-%d")),
            )

        conn.commit()


def add_energy_entry(db_path, date, appliance, power_watts, hours_used):
    """Add a new energy entry to the database."""
    energy_kwh = (power_watts * hours_used) / 1000

    with closing(get_db_connection(db_path)) as conn:
        conn.execute(
            """INSERT INTO energy_entries 
               (date, appliance, power_watts, hours_used, energy_kwh) 
               VALUES (?, ?, ?, ?, ?)""",
            (date, appliance, power_watts, hours_used, energy_kwh),
        )
        conn.commit()

    return energy_kwh


def get_monthly_entries(db_path, month, year):
    """Get all energy entries for a specific month."""
    with closing(get_db_connection(db_path)) as conn:
        entries = conn.execute(
            """SELECT * FROM energy_entries 
               WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
               ORDER BY date DESC""",
            (f"{month:02d}", str(year)),
        ).fetchall()

    return [dict(entry) for entry in entries]


def get_current_rate(db_path):
    """Get the current billing rate."""
    with closing(get_db_connection(db_path)) as conn:
        rate = conn.execute(
            "SELECT rate_per_kwh FROM billing_rates ORDER BY effective_date DESC LIMIT 1"
        ).fetchone()

    return rate["rate_per_kwh"] if rate else 7.5


def update_billing_rate(db_path, new_rate):
    """Update the billing rate."""
    with closing(get_db_connection(db_path)) as conn:
        conn.execute(
            "INSERT INTO billing_rates (rate_per_kwh, effective_date) VALUES (?, ?)",
            (new_rate, datetime.now().strftime("%Y-%m-%d")),
        )
        conn.commit()
