import binascii
import math
import secrets
from typing import Callable


from set2.c11 import encrypt_aes_128_ecb

UNKOWN_STRING = """Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK"""


class Oracle:
    def __init__(self):
        self.key = secrets.token_bytes(16)

    def run(self, inp: bytes):
        return encrypt_aes_128_ecb(inp + binascii.a2b_base64(UNKOWN_STRING), self.key)


def determine_block_size(enc_fn: Callable[[bytes], bytes]):
    i = 0
    original_size = len(enc_fn(b"A" * i))
    while True:
        i += 1 
        new_size = len(enc_fn(b"A" * i))
        if original_size != new_size:
            return new_size - original_size


def ensure_ecb(o: Oracle):
    output = o.run(b"X" * 128)
    assert output[64:80] == output[80:96]


def decode_sixteen_bytes_at_atime(o: Oracle):
    block_size = determine_block_size(o.run)
    ensure_ecb(o)
    reverse_discovered = b""
    for i in range(1, block_size+1):
        one_short = b"A" * (block_size -i)
        encrypted_one_short = o.run(one_short)
        options = {
            o.run(one_short + reverse_discovered + bytes([j]))[:16]: j
            for j in range(256)
        }
        reverse_discovered += bytes([options[encrypted_one_short[:16]]])

    return reverse_discovered



def decode_unknown_string(o: Oracle):
    block_size = determine_block_size(o.run)
    ensure_ecb(o)
    num_blocks = math.ceil(len(o.run(b""))/16)
    reverse_discovered = b"" 
    for b in range(num_blocks):
        for i in range(1, block_size+1):
            one_short = b"A" * (block_size -i)
            encrypted_one_short = o.run(one_short)[:16*(b+1)]
            options = {
                o.run(one_short + reverse_discovered + bytes([j]))[:16*(b+1)]: j
                for j in range(256)
            }
            try:
                last_byte = bytes([options[encrypted_one_short]])
                if not last_byte.isascii():
                    return reverse_discovered
                reverse_discovered += last_byte
            except Exception as e:
                print(f"Caught Exception: {e}")
                return reverse_discovered
    return reverse_discovered


if __name__ == "__main__":
    o = Oracle()
    decoded = decode_unknown_string(o)
    print(decoded)

