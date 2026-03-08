import unittest
from src.lab2.vigenere import encrypt_vigenere, decrypt_vigenere

class TestVigenere(unittest.TestCase):
    def test_encrypt(self):
        self.assertEqual(encrypt_vigenere("PYTHON", "A"), "PYTHON")
        self.assertEqual(encrypt_vigenere("python", "a"), "python")
        self.assertEqual(encrypt_vigenere("ATTACKATDAWN", "LEMON"), "LXFOPVEFRNHR")
    
    def test_decrypt(self):
        self.assertEqual(decrypt_vigenere("PYTHON", "A"), "PYTHON")
        self.assertEqual(decrypt_vigenere("python", "a"), "python")
        self.assertEqual(decrypt_vigenere("LXFOPVEFRNHR", "LEMON"), "ATTACKATDAWN")
    
    def test_empty(self):
        self.assertEqual(encrypt_vigenere("", "KEY"), "")
        self.assertEqual(decrypt_vigenere("", "KEY"), "")

if __name__ == '__main__':
    unittest.main()
