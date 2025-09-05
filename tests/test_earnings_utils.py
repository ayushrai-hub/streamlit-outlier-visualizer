"""
Unit tests for earnings_utils.py
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.earnings_utils import parse_duration, format_seconds

class TestEarningsUtils(unittest.TestCase):
    def test_parse_duration(self):
        self.assertEqual(parse_duration('1h 30m 20s'), 5420)
        self.assertEqual(parse_duration('2h'), 7200)
        self.assertEqual(parse_duration('45m'), 2700)
        self.assertEqual(parse_duration('10s'), 10)
        self.assertEqual(parse_duration('-'), 0)
        self.assertEqual(parse_duration(''), 0)
        self.assertEqual(parse_duration('1h 0m 0s'), 3600)

    def test_format_seconds(self):
        self.assertEqual(format_seconds(5420), '01h 30m 20s')
        self.assertEqual(format_seconds(7200), '02h 00m 00s')
        self.assertEqual(format_seconds(10), '00h 00m 10s')
        self.assertEqual(format_seconds(0), '00h 00m 00s')

if __name__ == '__main__':
    unittest.main(verbosity=2)
