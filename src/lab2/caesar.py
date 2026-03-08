def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """Encrypts plaintext using a Caesar cipher."""
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            if char.isupper():
                shifted = (ord(char) - ord('A') + shift) % 26 + ord('A')
            else:
                shifted = (ord(char) - ord('a') + shift) % 26 + ord('a')
            ciphertext += chr(shifted)
        else:
            ciphertext += char
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """Decrypts a ciphertext using a Caesar cipher."""
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                shifted = (ord(char) - ord('A') - shift) % 26 + ord('A')
            else:
                shifted = (ord(char) - ord('a') - shift) % 26 + ord('a')
            plaintext += chr(shifted)
        else:
            plaintext += char
    return plaintext
