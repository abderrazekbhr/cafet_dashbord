# tests/test_app.py
import unittest
from app import app

class FlaskTest(unittest.TestCase):

    def setUp(self):
        # Set up a test client
        self.app = app.test_client()

    def test_hello_endpoint(self):
        # Test the / endpoint
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
