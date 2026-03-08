import unittest
from src.lab2.rsa import is_prime, gcd, multiplicative_inverse, generate_keypair

class TestRSA(unittest.TestCase):
    
    def test_is_prime(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(5))
        self.assertTrue(is_prime(7))
        self.assertTrue(is_prime(11))
        self.assertTrue(is_prime(13))
        self.assertTrue(is_prime(17))
        self.assertTrue(is_prime(19))
        self.assertTrue(is_prime(23))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(6))
        self.assertFalse(is_prime(8))
        self.assertFalse(is_prime(9))
        self.assertFalse(is_prime(10))
        self.assertFalse(is_prime(15))
        self.assertFalse(is_prime(21))
        self.assertFalse(is_prime(25))
    
    def test_gcd(self):
        self.assertEqual(gcd(12, 15), 3)
        self.assertEqual(gcd(3, 7), 1)
        self.assertEqual(gcd(10, 25), 5)
        self.assertEqual(gcd(14, 21), 7)
        self.assertEqual(gcd(17, 19), 1)
        self.assertEqual(gcd(100, 125), 25)
        self.assertEqual(gcd(0, 5), 5)
        self.assertEqual(gcd(5, 0), 5)
    
    def test_multiplicative_inverse(self):
        self.assertEqual(multiplicative_inverse(7, 40), 23)
        self.assertEqual(multiplicative_inverse(3, 10), 7)
        self.assertEqual(multiplicative_inverse(17, 3120), 2753)
        self.assertEqual(multiplicative_inverse(5, 12), 5)
        self.assertEqual(multiplicative_inverse(9, 26), 3)
    
    def test_generate_keypair(self):
        public, private = generate_keypair(61, 53)
        e, n = public
        d, _ = private
        self.assertEqual(n, 61 * 53)
        self.assertTrue(1 < e < (61-1)*(53-1))
        self.assertTrue((e * d) % ((61-1)*(53-1)) == 1)
        
        public, private = generate_keypair(17, 19)
        e, n = public
        d, _ = private
        self.assertEqual(n, 17 * 19)
        self.assertTrue(1 < e < (17-1)*(19-1))
        self.assertTrue((e * d) % ((17-1)*(19-1)) == 1)
    
    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            generate_keypair(4, 7)
        with self.assertRaises(ValueError):
            generate_keypair(7, 9)
        with self.assertRaises(ValueError):
            generate_keypair(5, 5)

if __name__ == '__main__':
    unittest.main()
