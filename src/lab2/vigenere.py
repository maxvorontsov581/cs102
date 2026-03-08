def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = []
    keyword = keyword.upper()
    key_len = len(keyword)
    key_index = 0
    for ch in plaintext:
        if ch.isalpha():
            shift = ord(keyword[key_index % key_len]) - ord('A')
            if ch.isupper():
                ciphertext.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
            else:
                ciphertext.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
            key_index += 1
        else:
            ciphertext.append(ch)
    return ''.join(ciphertext)

def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = []
    keyword = keyword.upper()
    key_len = len(keyword)
    key_index = 0
    for ch in ciphertext:
        if ch.isalpha():
            shift = ord(keyword[key_index % key_len]) - ord('A')
            if ch.isupper():
                plaintext.append(chr((ord(ch) - ord('A') - shift) % 26 + ord('A')))
            else:
                plaintext.append(chr((ord(ch) - ord('a') - shift) % 26 + ord('a')))
            key_index += 1
        else:
            plaintext.append(ch)
    return ''.join(plaintext)
