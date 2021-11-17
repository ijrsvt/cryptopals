import math
import secrets  
from typing import Callable, Dict

from set2.c9 import pad_bytes
from set2.c10 import decrypt_aes_128_ecb
from set2.c11 import encrypt_aes_128_ecb
from set2.c12 import determine_block_size

def parse_url(url: str) ->Dict[str, str]:
    split = url.split("&")
    return {
        v.split("=")[0] : v.split("=")[1]
        for v in split 
    }


def profile_for(email: str, uid:str= "10", role:str = "user"):
    obj = {
        "email" : email,
        "uid" : uid,
        "role" : role 
    }
    for k,v in obj.items():
        vp = v.replace("=","<eq>")
        vpp = vp.replace("&", "<and>")
        obj[k] = vpp
    return "&".join([
        f"{k}={v}" for k,v in obj.items()       
    ])


class Oracle:
    def __init__(self):
        self.key = secrets.token_bytes(16)

    def _inner_encrypt(self, b: bytes) -> bytes:
        return encrypt_aes_128_ecb(b, self.key)

    def encrypt(self, email: str) -> bytes:
        return self._inner_encrypt(profile_for(email).encode())


    def _inner_decrypt(self, b: bytes) -> bytes:
        return decrypt_aes_128_ecb(b, self.key)

    def decode(self, encrypted_bytes: bytes) -> Dict[str,str]:
        return parse_url(self._inner_decrypt(encrypted_bytes).decode())



def generate_encrypted_bytes_for_admin(encrypt_fn: Callable[[str], bytes]):
    desired_string = "admin"
    pad_size = determine_block_size(lambda x: encrypt_fn(x.decode()))
    padded = pad_bytes(desired_string.encode(), pad_size).decode()

    initial_offset = pad_size - len("email=")
    initial_block = "X" * initial_offset

    return encrypt_fn(initial_block + padded)[pad_size:2*pad_size]

def determine_empty_len_size(o: Callable[[str], bytes]):
    original_size = len(o(""))
    i = 1
    while True:
        new_size = len(o("X" * i))
        if new_size > original_size:
            return original_size - i
        i += 1

def test_determine_empty_len_size():
    def fn(desired_size: int):
        def inner_fn(s: str):
            og = "X" * desired_size
            (og + s).encode()
            return encrypt_aes_128_ecb((og + s).encode(), secrets.token_bytes(16))
        return inner_fn
    for i in range(16):
        size =  determine_empty_len_size(fn(i))
        assert size == i, f"Got {size}, not {i}"



def solve(oracle: Callable[[str], bytes]) -> bytes:
    """
    1. Modify the input to get a single AES Encrypted 16B block that begins with `admin` & properly padded
    2. Generate an input that sets `user` onto its own block
    3. Swap the last block with the block that you created in part 1
    4. Decrypt & Profit
    """
    admin_block = generate_encrypted_bytes_for_admin(oracle)
    original_size = determine_empty_len_size(oracle)
    pad_size = determine_block_size(lambda x: oracle(x.decode()))
    email_bytes = (math.ceil(original_size * 1.0 / pad_size))
    bs_bytes = oracle("A" * (email_bytes * pad_size - original_size + + len("user")))
    return bs_bytes, bs_bytes[:-16] + admin_block
    

if __name__ == "__main__":
    o =Oracle()
    ENCRYPTED_USER = o.encrypt("ian.rodney@gmail.com") 
    DECODED = o.decode(ENCRYPTED_USER)
    print("Encrypted", ENCRYPTED_USER, "\n", "Decrypted", DECODED)
    test_determine_empty_len_size()
    potential = generate_encrypted_bytes_for_admin(o.encrypt)

    normal, hacked = solve(o.encrypt)
    assert o.decode(hacked)["role"] == "admin", o.decode(hacked)
    print(f"\nWe now have this role: {o.decode(hacked)}")