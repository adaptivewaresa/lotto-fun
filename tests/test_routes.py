import unittest
from unittest.mock import patch
from app.services import generate_pen_lotto_numbers, fetch_draw_frequencies


class TestServices(unittest.TestCase):
    @patch('app.services.fetch_draw_frequencies')
    def test_generate_pen_lotto_numbers(self, mock_fetch):
        # Mock draw frequencies
        mock_fetch.return_value = {1: 100, 2: 80, 3: 60, 4: 40, 5: 20}

        # Call the function
        result = generate_pen_lotto_numbers()
        self.assertIn('numbers', result)
        self.assertIn('reasons', result)
        self.assertEqual(len(result['numbers']), 6)
