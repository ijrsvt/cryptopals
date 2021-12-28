from binascii import a2b_base64
from typing import Optional

from Crypto.Cipher import AES

from set1.c2 import xor



def keystream(key: bytes, nonce: Optional[bytes] = None) -> bytes:
    cipher = AES.new(key)
    i = 0
    if nonce is None:
        nonce = i.to_bytes(8, byteorder="little")
    while True:
        yield cipher.encrypt(nonce + i.to_bytes(8, byteorder="little"))
        i+=1

def encrypt(key: bytes, msg: bytes) -> bytes:
    stream = keystream(key)
    ptr = 0
    output = b""
    while ptr < len(msg):
        output += xor(next(stream), msg[ptr: ptr + 16])
        ptr += 16
    assert len(output) == len(msg)
    return output

def decrypt(key: bytes, encrypted: bytes) -> str:
    raw = encrypt(key, encrypted)
    return raw.decode()

if __name__ == "__main__":
    output = decrypt(b"YELLOW SUBMARINE", a2b_base64("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="))
    print(output)

