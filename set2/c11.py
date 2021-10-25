import secrets
from typing import Optional, Tuple

from Crypto.Cipher import AES

from set2.c9 import pad_bytes
from set2.c10 import encrypt_aes_128_cbc


def encrypt_aes_128_ecb(msg: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    padded = pad_bytes(msg, 16)
    output = b""
    for i in range(0,len(padded), 16):
        output += cipher.encrypt(padded[i:i+16])
    return output



def choose_encrypt(msg: bytes, key: Optional[bytes] = None) -> Tuple[bytes, str]:
    if key is None:
        key = secrets.token_bytes(16)

    modded_bytes = secrets.token_bytes(5 + secrets.randbelow(6)) + msg + secrets.token_bytes(5 + secrets.randbelow(6))
    if secrets.randbelow(2) == 1:
        return encrypt_aes_128_cbc(msg=modded_bytes, key=key, iv=secrets.token_bytes(16)), "CBC"
    else:
        return encrypt_aes_128_ecb(msg=modded_bytes, key=key), "ECB"


def detect_oracle():
    msg = b"X"* 128
    encrypted, mode = choose_encrypt(msg)
    b1 = encrypted[64:80]
    b2 = encrypted[80:96]
    if b1 == b2:
        assert mode == "ECB", encrypted
    else:
        assert mode == "CBC", encrypted

if __name__ == "__main__":
    for _ in range(10000):
        detect_oracle()
