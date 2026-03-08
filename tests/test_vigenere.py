import unittest
from src.lab2.vigenere import encrypt_vigenere, decrypt_vigenere

class TestVigenere(unittest.TestCase):
    
    def test_encrypt_basic(self):
        # Тесты из условия задачи
        self.assertEqual(encrypt_vigenere("PYTHON", "A"), "PYTHON")
        self.assertEqual(encrypt_vigenere("python", "a"), "python")
        self.assertEqual(encrypt_vigenere("ATTACKATDAWN", "LEMON"), "LXFOPVEFRNHR")
    
    def test_decrypt_basic(self):
        # Тесты из условия задачи
        self.assertEqual(decrypt_vigenere("PYTHON", "A"), "PYTHON")
        self.assertEqual(decrypt_vigenere("python", "a"), "python")
        self.assertEqual(decrypt_vigenere("LXFOPVEFRNHR", "LEMON"), "ATTACKATDAWN")
    
    def test_with_spaces_and_punctuation(self):
        plaintext = "Hello, World!"
        keyword = "KEY"
        encrypted = encrypt_vigenere(plaintext, keyword)
        self.assertEqual(decrypt_vigenere(encrypted, keyword), plaintext)
    
    def test_empty_string(self):
        self.assertEqual(encrypt_vigenere("", "KEY"), "")
        self.assertEqual(decrypt_vigenere("", "KEY"), "")
    
    def test_keyword_longer_than_text(self):
        self.assertEqual(encrypt_vigenere("ABC", "LONGKEY"), "LON")
        self.assertEqual(decrypt_vigenere("LON", "LONGKEY"), "ABC")

if __name__ == '__main__':
    unittest.main()
