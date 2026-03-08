def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    keyword = keyword.upper()
    key_index = 0
    
    for char in plaintext:
        if char.isalpha():
            shift = ord(keyword[key_index % len(keyword)]) - ord('A')
            
            if char.isupper():
                shifted = (ord(char) - ord('A') + shift) % 26 + ord('A')
            else:
                shifted = (ord(char) - ord('a') + shift) % 26 + ord('a')
            
            ciphertext += chr(shifted)
            key_index += 1
        else:
            ciphertext += char
    
    return ciphertext

def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""
    keyword = keyword.upper()
    key_index = 0
    
    for char in ciphertext:
        if char.isalpha():
            shift = ord(keyword[key_index % len(keyword)]) - ord('A')
            
            if char.isupper():
                shifted = (ord(char) - ord('A') - shift) % 26 + ord('A')
            else:
                shifted = (ord(char) - ord('a') - shift) % 26 + ord('a')
            
            plaintext += chr(shifted)
            key_index += 1
        else:
            plaintext += char
    
    return plaintext
