import random
import math
from typing import Tuple

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return abs(a)

def multiplicative_inverse(e: int, phi: int) -> int:
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        else:
            g, x, y = extended_gcd(b % a, a)
            return g, y - (b // a) * x, x
    g, x, _ = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("Модульное обратное не существует")
    else:
        return x % phi

def generate_keypair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    
    d = multiplicative_inverse(e, phi)
    
    return ((e, n), (d, n))
