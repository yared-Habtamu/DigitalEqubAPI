import random
import time


class MockChapa:
    @staticmethod
    def process_payment(amount):
        time.sleep(2)  # Simulate network delay for 2 sec
        return {
            'success': random.random() < 0.7,  # assuming 70%sucess
            'message': 'Payment processed' if random.random() < 0.7 else 'Insufficient funds'
        }
