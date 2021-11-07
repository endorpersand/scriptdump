"""
creation: unknown

Encoding & decoding Vigenere

there's also vigenereencrypt idk what that does
"""

from itertools import cycle

def vigenere_cipher(msg, key):
    CHARS = "abcdefghijklmnopqrstuvwxyz"

    # sanitize key
    key = key.lower()
    key = ''.join(c for c in key if c in CHARS)
    keygen = cycle(key)

    # shift msg across alphabet
    ciphermsg = []
    for c in msg:
        lc = c.lower()
        if lc not in CHARS:
            ciphermsg.append(c)
            continue
        shifted_index = CHARS.index(lc) + CHARS.index(next(keygen))
        shifted_index %= len(CHARS)
        nc = CHARS[shifted_index].lower() if c.islower() else CHARS[shifted_index].upper()
        ciphermsg.append(nc)

    return ''.join(ciphermsg)

def vigenere_decipher(cipher, key):
    # sanitize key
    CHARS = "abcdefghijklmnopqrstuvwxyz"
    key = key.lower()
    key = ''.join(c for c in key if c in CHARS)

    # invert key
    key = ''.join(CHARS[(-CHARS.index(c)) % len(CHARS)] for c in key)

    return vigenere_cipher(cipher, key)

print(vigenere_cipher("hello", "howdy"))
print(vigenere_cipher("helLo how are ya", "howdy"))
print(vigenere_decipher("oshOm ocs dpl mw", "howdy"))

vigenereencrypt = lambda message, keyword, alphabet = "abcdefghijklmnopqrstuvwxyz": ''.join(alphabet[(alphabet.index(x) + alphabet.index(y)) % 26] for x, y in zip(message.lower(), __import__('itertools').cycle(keyword.lower())))