from django.test import TestCase
from payments.services import MockChapa
from unittest.mock import patch
import time


class MockChapaTest(TestCase):
    @patch('time.sleep', return_value=None)  # Skip real delays
    def test_payment_success(self, mock_sleep):
        # Test successful payment (mock random to always return True)
        with patch('random.random', return_value=0.7):  # < 0.8 = success
            result = MockChapa.process_payment(1000)
            self.assertTrue(result['success'])

    def test_payment_failure(self):
        with patch('random.random', return_value=0.9):  # > 0.8 = failure
            result = MockChapa.process_payment(1000)
            self.assertFalse(result['success'])