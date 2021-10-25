import binascii
from Crypto.Cipher import AES

from set1.c2 import xor
from set2.c9 import pad_bytes


def decrypt_aes_128_cbc(encrypted: bytes, key: bytes, iv: bytes = b"\x00"*16) -> bytes:
    assert len(key) == 16, "AES 128 requires a 16 Byte Key!"
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = b""
    last_block = iv
    output = b""
    while len(encrypted) > 0:
        output += xor(cipher.decrypt(encrypted[:16]), last_block)
        last_block = encrypted[:16]
        encrypted = encrypted[16:]
    block_amount = output[-1]
    return output[:-block_amount]


def encrypt_aes_128_cbc(msg: bytes, key: bytes, iv: bytes = b"\x00" * 16) -> bytes:
    assert len(key) == 16, "AES 128 requires a 16 Byte Key!"

    cipher = AES.new(key, AES.MODE_ECB)
    padded_msg = pad_bytes(msg, 16)
    output = b""
    previous = iv
    while len(padded_msg) > 0:
        inp = xor(padded_msg[:16], previous)
        padded_msg = padded_msg[16:]
        previous = cipher.encrypt(inp)
        output += previous
    return output

    return cipher.decrypt(msg)

if __name__ == "__main__":
    key = "YELLOW SUBMARINE"
    inp =  b"0123456789ABCDEF"
    encrypted = encrypt_aes_128_cbc(inp, key)
    decrypted = decrypt_aes_128_cbc(encrypted, key)
    b = binascii.a2b_base64(open("set2/10.txt").read())
    print(decrypt_aes_128_cbc(b, b"YELLOW SUBMARINE").decode())