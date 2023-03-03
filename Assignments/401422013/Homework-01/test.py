import unittest
import random
import multiply


class TestCase(unittest.TestCase):

    def test_multiply(self):
        for i in range(20):
            a = random.randint(0, 1000)
            b = random.randint(0, 1000)
            result = multiply.multiply(a, b)
            self.assertEqual(result, a * b)

if __name__ == '__main__':
    unittest.main()