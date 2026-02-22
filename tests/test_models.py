"""Unit tests for database models."""

import os
import tempfile
import unittest

from app.models import (add_energy_entry, get_current_rate,
                        get_monthly_entries, init_db, update_billing_rate)


class ModelsTestCase(unittest.TestCase):
    """Test cases for database models."""

    def setUp(self):
        """Set up test fixtures."""
        self.db_fd, self.db_path = tempfile.mkstemp()
        init_db(self.db_path)

    def tearDown(self):
        """Clean up test fixtures."""
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_init_db_creates_tables(self):
        """Test that database initialization creates required tables."""
        import sqlite3

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check energy_entries table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='energy_entries'"
        )
        self.assertIsNotNone(cursor.fetchone())

        # Check billing_rates table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='billing_rates'")
        self.assertIsNotNone(cursor.fetchone())

        conn.close()

    def test_init_db_creates_default_rate(self):
        """Test that database initialization creates a default billing rate."""
        rate = get_current_rate(self.db_path)
        self.assertIsNotNone(rate)
        self.assertGreater(rate, 0)

    def test_add_energy_entry(self):
        """Test adding an energy entry."""
        energy_kwh = add_energy_entry(self.db_path, "2024-01-15", "Air Conditioner", 1500, 8.0)

        # Energy should be (1500W * 8h) / 1000 = 12 kWh
        self.assertEqual(energy_kwh, 12.0)

        # Verify entry was added
        entries = get_monthly_entries(self.db_path, 1, 2024)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["appliance"], "Air Conditioner")

    def test_add_multiple_entries(self):
        """Test adding multiple energy entries."""
        add_energy_entry(self.db_path, "2024-01-15", "AC", 1500, 8)
        add_energy_entry(self.db_path, "2024-01-16", "Fridge", 200, 24)
        add_energy_entry(self.db_path, "2024-01-17", "TV", 100, 5)

        entries = get_monthly_entries(self.db_path, 1, 2024)
        self.assertEqual(len(entries), 3)

    def test_get_monthly_entries_empty(self):
        """Test getting entries for a month with no data."""
        entries = get_monthly_entries(self.db_path, 6, 2024)
        self.assertEqual(len(entries), 0)

    def test_get_monthly_entries_filters_correctly(self):
        """Test that monthly entries are filtered by month/year."""
        add_energy_entry(self.db_path, "2024-01-15", "AC", 1500, 8)
        add_energy_entry(self.db_path, "2024-02-15", "AC", 1500, 8)
        add_energy_entry(self.db_path, "2024-01-20", "Fridge", 200, 24)

        # January should have 2 entries
        jan_entries = get_monthly_entries(self.db_path, 1, 2024)
        self.assertEqual(len(jan_entries), 2)

        # February should have 1 entry
        feb_entries = get_monthly_entries(self.db_path, 2, 2024)
        self.assertEqual(len(feb_entries), 1)

    def test_get_current_rate(self):
        """Test getting the current billing rate."""
        rate = get_current_rate(self.db_path)
        self.assertIsInstance(rate, float)
        self.assertGreater(rate, 0)

    def test_update_billing_rate(self):
        """Test updating the billing rate."""
        old_rate = get_current_rate(self.db_path)
        new_rate = 10.5

        update_billing_rate(self.db_path, new_rate)

        current_rate = get_current_rate(self.db_path)
        self.assertEqual(current_rate, new_rate)
        self.assertNotEqual(current_rate, old_rate)

    def test_energy_calculation_accuracy(self):
        """Test that energy calculations are accurate."""
        # 2000W for 5 hours = 10 kWh
        energy = add_energy_entry(self.db_path, "2024-01-15", "Heater", 2000, 5)
        self.assertEqual(energy, 10.0)

        # 500W for 0.5 hours = 0.25 kWh
        energy = add_energy_entry(self.db_path, "2024-01-16", "Microwave", 500, 0.5)
        self.assertEqual(energy, 0.25)

        # 100W for 24 hours = 2.4 kWh
        energy = add_energy_entry(self.db_path, "2024-01-17", "Light", 100, 24)
        self.assertEqual(energy, 2.4)


if __name__ == "__main__":
    unittest.main()
