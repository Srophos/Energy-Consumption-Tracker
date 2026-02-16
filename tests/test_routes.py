"""Unit tests for application routes."""
import unittest
import os
import tempfile
from datetime import datetime
from app import create_app
from app.models import init_db, add_energy_entry


class RoutesTestCase(unittest.TestCase):
    """Test cases for application routes."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = create_app({'DATABASE': self.db_path, 'TESTING': True})
        self.client = self.app.test_client()
        
        with self.app.app_context():
            init_db(self.db_path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def test_daily_entry_get(self):
        """Test GET request to daily entry page."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Daily Energy Entry', response.data)
    
    def test_daily_entry_post_success(self):
        """Test successful POST to daily entry."""
        data = {
            'date': '2024-01-15',
            'appliance': 'Air Conditioner',
            'power_watts': '1500',
            'hours_used': '8'
        }
        response = self.client.post('/', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Entry added successfully', response.data)
    
    def test_daily_entry_post_invalid_date(self):
        """Test POST with invalid date."""
        data = {
            'date': 'invalid-date',
            'appliance': 'AC',
            'power_watts': '1500',
            'hours_used': '8'
        }
        response = self.client.post('/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'valid date', response.data)
    
    def test_daily_entry_post_negative_power(self):
        """Test POST with negative power value."""
        data = {
            'date': '2024-01-15',
            'appliance': 'AC',
            'power_watts': '-100',
            'hours_used': '8'
        }
        response = self.client.post('/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'greater than 0', response.data)
    
    def test_daily_entry_post_empty_appliance(self):
        """Test POST with empty appliance name."""
        data = {
            'date': '2024-01-15',
            'appliance': '   ',
            'power_watts': '1500',
            'hours_used': '8'
        }
        response = self.client.post('/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'appliance name', response.data)
    
    def test_dashboard_get(self):
        """Test GET request to dashboard."""
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Energy Dashboard', response.data)
    
    def test_dashboard_with_entries(self):
        """Test dashboard displays entries correctly."""
        with self.app.app_context():
            add_energy_entry(self.db_path, '2024-01-15', 'AC', 1500, 8)
            add_energy_entry(self.db_path, '2024-01-16', 'Fridge', 200, 24)
        
        response = self.client.get('/dashboard?month=1&year=2024')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AC', response.data)
        self.assertIn(b'Fridge', response.data)
    
    def test_dashboard_empty_month(self):
        """Test dashboard with no entries for selected month."""
        response = self.client.get('/dashboard?month=6&year=2024')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No entries found', response.data)
    
    def test_dashboard_invalid_month(self):
        """Test dashboard with invalid month parameter."""
        response = self.client.get('/dashboard?month=13&year=2024')
        self.assertEqual(response.status_code, 200)
        # Should default to current month
        self.assertIn(b'Energy Dashboard', response.data)
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['status'], 'healthy')
        self.assertIn('timestamp', json_data)


if __name__ == '__main__':
    unittest.main()
