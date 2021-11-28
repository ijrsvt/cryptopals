import secrets
from typing import Callable

from urllib.parse import quote

from set2.c10 import decrypt_aes_128_cbc, encrypt_aes_128_cbc


PREPEND = "comment1=cooking%20MCs;userdata="
APPEND = ";comment2=%20like%20a%20pound%20of%20bacon"


def generate_string(userdata: str, aes_key: bytes, iv: bytes) -> str:
    userdata = userdata.replace("=", quote("="))
    userdata = userdata.replace(";", quote(";"))
    string = PREPEND + userdata + APPEND
    return encrypt_aes_128_cbc(string.encode(), aes_key, iv)

def decrypt_blob(blob: bytes, aes_key: bytes, iv: bytes) -> bool:
    decrypted = decrypt_aes_128_cbc(blob, aes_key, iv)
    # print(decrypted)
    dct = {
        tpl.split(b"=")[0] : tpl.split(b"=")[1]
        for tpl in decrypted.split(b";")
    }
    # print(dct)
    return dct.get(b"admin") == b"true"
    

def hackthis_shit(enc: Callable[[str], bytes], decrypt: Callable[[bytes], bool]):
    bit_flipped_semi_colon = bytes([";".encode()[0] ^ 1]).decode()
    bit_flipped_eq = bytes(["=".encode()[0] ^ 1]).decode()
    devious_input = "A" * 16  + bit_flipped_semi_colon + "admin" + bit_flipped_eq + "true"

    encrypted = enc(devious_input)
    one_swap =  encrypted[:32] + bytes([encrypted[32] ^ 1]) + encrypted[33:]
    offset = 32 + len(";admin")
    two_swap = one_swap[:offset] + bytes([one_swap[offset] ^ 1]) + one_swap[offset + 1:]
    assert decrypt(two_swap)


if __name__ == "__main__":
    key = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)

    blob = generate_string("data;;admin=true;;", key, iv)
    assert not decrypt_blob(blob, key, iv), "Bad Padding"
    hackthis_shit(
        lambda x: generate_string(x, key, iv),
        lambda y: decrypt_blob(y, key, iv)
    )

    