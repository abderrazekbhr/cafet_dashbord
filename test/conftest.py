import unittest

class MyTestCase(unittest.TestCase):
    def test_addition(self):
        result = 5 + 10
        self.assertEqual(result, 15, "Addition test failed")

    def test_subtraction(self):
        result = 20 - 5
        self.assertEqual(result, 15, "Subtraction test failed")

if __name__ == '__main__':
    unittest.main()