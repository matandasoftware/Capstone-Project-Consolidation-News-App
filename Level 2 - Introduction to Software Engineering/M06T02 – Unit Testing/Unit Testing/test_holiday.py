# test_holiday.py
import unittest
from holiday import hotel_cost, plane_cost, car_rental, holiday_cost


class TestHolidayCostCalculator(unittest.TestCase):
    """Test cases for the Holiday Cost Calculator functions."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.price_per_night = 1200.50
        self.daily_car_rate = 400.80
    
    # ========== Hotel Cost Tests ==========
    
    def test_hotel_cost_one_night(self):
        """Test hotel cost for 1 night."""
        result = hotel_cost(1)
        expected = 1200.50
        self.assertEqual(result, expected)
    
    def test_hotel_cost_multiple_nights(self):
        """Test hotel cost for multiple nights."""
        result = hotel_cost(5)
        expected = 5 * 1200.50  # 6002.50
        self.assertEqual(result, expected)
    
    def test_hotel_cost_zero_nights(self):
        """Test hotel cost for 0 nights (edge case)."""
        result = hotel_cost(0)
        expected = 0.0
        self.assertEqual(result, expected)
    
    def test_hotel_cost_large_number(self):
        """Test hotel cost for a large number of nights."""
        result = hotel_cost(100)
        expected = 100 * 1200.50  # 120050.0
        self.assertEqual(result, expected)
    
    # ========== Plane Cost Tests ==========
    
    def test_plane_cost_cape_town(self):
        """Test flight cost to Cape Town."""
        result = plane_cost("Cape Town")
        expected = 2500.75
        self.assertEqual(result, expected)
    
    def test_plane_cost_durban(self):
        """Test flight cost to Durban."""
        result = plane_cost("durban")
        expected = 1800.40
        self.assertEqual(result, expected)
    
    def test_plane_cost_johannesburg(self):
        """Test flight cost to Johannesburg."""
        result = plane_cost("JOHANNESBURG")
        expected = 2200.99
        self.assertEqual(result, expected)
    
    def test_plane_cost_port_elizabeth(self):
        """Test flight cost to Port Elizabeth."""
        result = plane_cost("port elizabeth")
        expected = 2000.25
        self.assertEqual(result, expected)
    
    def test_plane_cost_case_insensitive(self):
        """Test that city names are case-insensitive."""
        result1 = plane_cost("Cape Town")
        result2 = plane_cost("cape town")
        result3 = plane_cost("CAPE TOWN")
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)
    
    def test_plane_cost_with_whitespace(self):
        """Test city name with extra whitespace."""
        result = plane_cost("  cape town  ")
        expected = 2500.75
        self.assertEqual(result, expected)
    
    def test_plane_cost_unknown_city(self):
        """Test flight cost for an unknown city (returns default)."""
        result = plane_cost("Pretoria")
        expected = 2100.00  # Default price
        self.assertEqual(result, expected)
    
    # ========== Car Rental Tests ==========
    
    def test_car_rental_one_day(self):
        """Test car rental cost for 1 day."""
        result = car_rental(1)
        expected = 400.80
        self.assertEqual(result, expected)
    
    def test_car_rental_multiple_days(self):
        """Test car rental cost for multiple days."""
        result = car_rental(7)
        expected = 7 * 400.80  # 2805.60
        self.assertEqual(result, expected)
    
    def test_car_rental_zero_days(self):
        """Test car rental cost for 0 days (edge case)."""
        result = car_rental(0)
        expected = 0.0
        self.assertEqual(result, expected)
    
    def test_car_rental_large_number(self):
        """Test car rental cost for many days."""
        result = car_rental(30)
        expected = 30 * 400.80  # 12024.0
        self.assertEqual(result, expected)
    
    # ========== Total Holiday Cost Tests ==========
    
    def test_holiday_cost_cape_town_basic(self):
        """Test total cost: 3 nights, Cape Town, 2 days car rental."""
        result = holiday_cost(3, "Cape Town", 2)
        expected = (3 * 1200.50) + 2500.75 + (2 * 400.80)
        # 3601.50 + 2500.75 + 801.60 = 6903.85
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_holiday_cost_durban_week(self):
        """Test total cost: 7 nights in Durban, 7 days car rental."""
        result = holiday_cost(7, "Durban", 7)
        expected = (7 * 1200.50) + 1800.40 + (7 * 400.80)
        # 8403.50 + 1800.40 + 2805.60 = 13009.50
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_holiday_cost_johannesburg(self):
        """Test total cost for Johannesburg trip."""
        result = holiday_cost(5, "johannesburg", 5)
        expected = (5 * 1200.50) + 2200.99 + (5 * 400.80)
        # 6002.50 + 2200.99 + 2004.00 = 10207.49
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_holiday_cost_all_zeros(self):
        """Test total cost when all values are zero."""
        result = holiday_cost(0, "Cape Town", 0)
        expected = 0.0 + 2500.75 + 0.0  # Only flight cost
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_holiday_cost_unknown_city(self):
        """Test total cost with unknown city (uses default flight price)."""
        result = holiday_cost(2, "Pretoria", 3)
        expected = (2 * 1200.50) + 2100.00 + (3 * 400.80)
        # 2401.00 + 2100.00 + 1202.40 = 5703.40
        self.assertAlmostEqual(result, expected, places=2)
    
    # ========== Data Type Tests ==========
    
    def test_hotel_cost_returns_float(self):
        """Test that hotel_cost returns a float."""
        result = hotel_cost(3)
        self.assertIsInstance(result, float)
    
    def test_plane_cost_returns_float(self):
        """Test that plane_cost returns a float."""
        result = plane_cost("Cape Town")
        self.assertIsInstance(result, float)
    
    def test_car_rental_returns_float(self):
        """Test that car_rental returns a float."""
        result = car_rental(5)
        self.assertIsInstance(result, float)
    
    def test_holiday_cost_returns_float(self):
        """Test that holiday_cost returns a float."""
        result = holiday_cost(3, "Durban", 2)
        self.assertIsInstance(result, float)


if __name__ == '__main__':
    unittest.main()
