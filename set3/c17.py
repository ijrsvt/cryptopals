import binascii
import secrets

from set2.c10 import _decrypt_aes_128_cbc_raw, encrypt_aes_128_cbc
from set2.c15 import validate_padding_bytes

OPTIONS = [
    "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
    "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
    "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
    "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
    "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
    "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
    "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
    "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
    "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
    "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93",
]


class Oracle:
    def __init__(self):
        self.key = secrets.token_bytes(16)

    def encrypt(self):
        opt = binascii.a2b_base64(OPTIONS[secrets.randbelow(len(OPTIONS))])
        iv = secrets.token_bytes(16)
        return iv, encrypt_aes_128_cbc(opt, self.key, iv)
        
    def decrypt(self, iv: bytes, cipher_text: bytes):
        decrypted = _decrypt_aes_128_cbc_raw(cipher_text, self.key, iv)
        try:
            validate_padding_bytes(decrypted)
            return True
        except Exception:
            return False  



if __name__ == "__main__":
    o = Oracle()
    iv, ct = o.encrypt()
    assert o.decrypt(iv, ct)
