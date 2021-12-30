import binascii
import secrets
from typing import Callable

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



def brute_force_second_block(enc: bytes, decrypt: Callable[[bytes], bool] ) -> bytes:
    assert len(enc) == 32
    d_k_1 = [None]  * 16
    p_k_1 = [None]  * 16
    for padding_amount in range(1, 17, 1):
        indx = 16 - padding_amount
        suffix = bytes([
            b ^ padding_amount for b in d_k_1
            if b is not None
        ])+ enc[16:]
        options = [
            k for k,v in 
            {i : decrypt(enc[:indx] + bytes([i]) + suffix ) for i in range(255) if i != enc[indx]}.items()
            if v
        ]
        if len(options) == 0:
            options = [enc[indx]]
        d_k_1[indx] = options[0] ^ padding_amount
        p_k_1[indx] = d_k_1[indx] ^ enc[16 - padding_amount]
    return bytes(p_k_1)


def brute_force_all(o: Oracle):
    found = set()
    strings = []
    while len(found) < len(OPTIONS):
        iv, ct = o.encrypt()
        output = [
            brute_force_second_block(ct[i:i+32], lambda x : o.decrypt(iv, x))
            for i in range(0, len(ct) - 16, 16)
            ]
        output.insert(0,
            brute_force_second_block(iv + ct[:16], lambda x : o.decrypt(x[:16], x[16:]))
        )
        sol = b"".join(output)
        try:
            digit = int(sol[:6])
            assert sol.isascii()
            if digit not in found:
                found.add(digit)
                strings.append(sol)
        except Exception as e:
            print("OOF\n", sol)
    found = list(found)
    strings.sort(key=lambda x: int(x[:6]))
    print("Found All!!\n\n")
    [print(s) for s in strings]

if __name__ == "__main__":
    o = Oracle()
    iv, ct = o.encrypt()
    assert o.decrypt(iv, ct)
    brute_force_all(o)


