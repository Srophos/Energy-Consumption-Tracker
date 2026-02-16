"""Unit tests for utility calculations."""
import unittest
from app.utils import (
    calculate_energy_kwh, calculate_monthly_bill, format_currency,
    validate_date, validate_positive_number, get_month_name
)


class CalculationsTestCase(unittest.TestCase):
    """Test cases for utility calculations."""
    
    def test_calculate_energy_kwh(self):
        """Test energy calculation in kWh."""
        # 1000W for 1 hour = 1 kWh
        self.assertEqual(calculate_energy_kwh(1000, 1), 1.0)
        
        # 1500W for 8 hours = 12 kWh
        self.assertEqual(calculate_energy_kwh(1500, 8), 12.0)
        
        # 500W for 0.5 hours = 0.25 kWh
        self.assertEqual(calculate_energy_kwh(500, 0.5), 0.25)
        
        # 2000W for 5 hours = 10 kWh
        self.assertEqual(calculate_energy_kwh(2000, 5), 10.0)
    
    def test_calculate_monthly_bill(self):
        """Test monthly bill calculation."""
        entries = [
            {'energy_kwh': 10.0},
            {'energy_kwh': 5.0},
            {'energy_kwh': 3.5}
        ]
        rate = 7.5
        
        # Total: 18.5 kWh * 7.5 = 138.75
        bill = calculate_monthly_bill(entries, rate)
        self.assertEqual(bill, 138.75)
    
    def test_calculate_monthly_bill_empty(self):
        """Test monthly bill calculation with no entries."""
        entries = []
        rate = 7.5
        
        bill = calculate_monthly_bill(entries, rate)
        self.assertEqual(bill, 0)
    
    def test_calculate_monthly_bill_different_rates(self):
        """Test monthly bill calculation with different rates."""
        entries = [{'energy_kwh': 100.0}]
        
        # Rate 5.0
        bill = calculate_monthly_bill(entries, 5.0)
        self.assertEqual(bill, 500.0)
        
        # Rate 10.0
        bill = calculate_monthly_bill(entries, 10.0)
        self.assertEqual(bill, 1000.0)
    
    def test_format_currency(self):
        """Test currency formatting."""
        self.assertEqual(format_currency(100), '₹100.00')
        self.assertEqual(format_currency(123.45), '₹123.45')
        self.assertEqual(format_currency(0.99), '₹0.99')
        self.assertEqual(format_currency(1234.567), '₹1234.57')
    
    def test_validate_date_valid(self):
        """Test date validation with valid dates."""
        self.assertTrue(validate_date('2024-01-15'))
        self.assertTrue(validate_date('2023-12-31'))
        self.assertTrue(validate_date('2024-02-29'))  # Leap year
    
    def test_validate_date_invalid(self):
        """Test date validation with invalid dates."""
        self.assertFalse(validate_date('2024-13-01'))  # Invalid month
        self.assertFalse(validate_date('2024-01-32'))  # Invalid day
        self.assertFalse(validate_date('not-a-date'))
        self.assertFalse(validate_date('2024/01/15'))  # Wrong format
        self.assertFalse(validate_date(''))
    
    def test_validate_positive_number_valid(self):
        """Test positive number validation with valid inputs."""
        is_valid, error = validate_positive_number(10, 'Test')
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        
        is_valid, error = validate_positive_number(0.1, 'Test')
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        
        is_valid, error = validate_positive_number('123.45', 'Test')
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_positive_number_invalid(self):
        """Test positive number validation with invalid inputs."""
        # Zero
        is_valid, error = validate_positive_number(0, 'Test')
        self.assertFalse(is_valid)
        self.assertIn('greater than 0', error)
        
        # Negative
        is_valid, error = validate_positive_number(-10, 'Test')
        self.assertFalse(is_valid)
        self.assertIn('greater than 0', error)
        
        # Non-numeric
        is_valid, error = validate_positive_number('abc', 'Test')
        self.assertFalse(is_valid)
        self.assertIn('valid number', error)
        
        # None
        is_valid, error = validate_positive_number(None, 'Test')
        self.assertFalse(is_valid)
        self.assertIn('valid number', error)
    
    def test_get_month_name(self):
        """Test month name conversion."""
        self.assertEqual(get_month_name(1), 'January')
        self.assertEqual(get_month_name(6), 'June')
        self.assertEqual(get_month_name(12), 'December')
    
    def test_get_month_name_invalid(self):
        """Test month name conversion with invalid input."""
        self.assertEqual(get_month_name(0), 'Unknown')
        self.assertEqual(get_month_name(13), 'Unknown')
        self.assertEqual(get_month_name(-1), 'Unknown')
    
    def test_energy_calculation_edge_cases(self):
        """Test energy calculation edge cases."""
        # Very small values
        energy = calculate_energy_kwh(1, 0.001)
        self.assertAlmostEqual(energy, 0.000001, places=6)
        
        # Very large values
        energy = calculate_energy_kwh(5000, 100)
        self.assertEqual(energy, 500.0)
        
        # Fractional hours
        energy = calculate_energy_kwh(1200, 2.5)
        self.assertEqual(energy, 3.0)


if __name__ == '__main__':
    unittest.main()
