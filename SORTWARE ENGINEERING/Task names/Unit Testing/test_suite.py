# test_suite.py
import unittest
from test_holiday import TestHolidayCostCalculator


# Create and run test suite
suite = unittest.TestLoader().loadTestsFromTestCase(TestHolidayCostCalculator)
unittest.TextTestRunner(verbosity=2).run(suite)
