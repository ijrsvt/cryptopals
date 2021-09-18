import binascii
from Crypto.Cipher import AES


def decrypt_aes_128(msg: bytes, key: bytes) -> bytes:
    assert len(key) == 16, "AES 128 requires a 16 Byte Key!"
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(msg)

if __name__ == "__main__":
    b = binascii.a2b_base64(open("7.txt").read())
    print(decrypt_aes_128(b, b"YELLOW SUBMARINE").decode())