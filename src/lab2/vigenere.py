def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = []
    keyword = keyword.upper()
    key_len = len(keyword)
    for i, char in enumerate(plaintext):
        if char.isalpha():
            shift = ord(keyword[i % key_len]) - ord('A')
            if char.isupper():
                ciphertext.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            else:
                ciphertext.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
        else:
            ciphertext.append(char)
    return ''.join(ciphertext)

def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = []
    keyword = keyword.upper()
    key_len = len(keyword)
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            shift = ord(keyword[i % key_len]) - ord('A')
            if char.isupper():
                plaintext.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:
                plaintext.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
        else:
            plaintext.append(char)
    return ''.join(plaintext)
