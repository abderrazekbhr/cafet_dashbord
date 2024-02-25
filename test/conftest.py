import unittest

class MyTest(unittest.TestCase):
    def test_something(self):
        # Write test cases here
        pass

    def test_another_thing(self):
        # Test the / endpoint
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()