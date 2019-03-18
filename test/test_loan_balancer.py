import unittest
from loan_balancer import LoadBalancer

class TestStringMethods(unittest.TestCase):

    def test_assign_loan_normal(self):
        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()
