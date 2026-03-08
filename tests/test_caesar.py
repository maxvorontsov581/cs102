import unittest
from src.lab2.caesar import encrypt_caesar, decrypt_caesar

class TestCaesar(unittest.TestCase):
    def test_encrypt(self):
        self.assertEqual(encrypt_caesar("PYTHON"), "SBWKRQ")
        self.assertEqual(encrypt_caesar("python"), "sbwkrq")
        self.assertEqual(encrypt_caesar("Python3.6"), "Sbwkrq3.6")
        self.assertEqual(encrypt_caesar(""), "")
    
    def test_decrypt(self):
        self.assertEqual(decrypt_caesar("SBWKRQ"), "PYTHON")
        self.assertEqual(decrypt_caesar("sbwkrq"), "python")
        self.assertEqual(decrypt_caesar("Sbwkrq3.6"), "Python3.6")
        self.assertEqual(decrypt_caesar(""), "")
    
    def test_custom_shift(self):
        self.assertEqual(encrypt_caesar("ABC", 1), "BCD")
        self.assertEqual(decrypt_caesar("BCD", 1), "ABC")

if __name__ == '__main__':
    unittest.main()
