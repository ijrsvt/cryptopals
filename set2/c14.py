from collections import Counter
import binascii
import random
import secrets
from typing import Callable


from set2.c11 import encrypt_aes_128_ecb
from set2.c12 import UNKOWN_STRING


class Oracle:
    def __init__(self):
        self.key = secrets.token_bytes(16)

    def run(self, inp: bytes):
        prefix = secrets.token_bytes(random.randint(0, 128))
        return encrypt_aes_128_ecb(prefix + inp + binascii.a2b_base64(UNKOWN_STRING), self.key)



def determine_ecb_block_size(enc_fn: Callable[[bytes], bytes]):
    candidate = 2
    NUM_CHARS = 100_000
    encrypted = enc_fn(b"A" * NUM_CHARS)
    while True:
        # Try to count how many matching blocks given the candidate block size
        cnt = Counter(encrypted[candidate * i:candidate * (i + 1)] for i in range(0,len(encrypted)//candidate))

        freq = Counter(cnt.values())

        most_common_count = max(freq.keys())
        if most_common_count > (NUM_CHARS / candidate) * .9 and freq[most_common_count] == 1:
            # We have found a key if >90% of blocks match & there is only one match block!
            return candidate
        candidate += 1


def decode_sixteen_bytes_at_atime(o: Oracle):
    block_size = determine_ecb_block_size(o.run)
    reverse_discovered = b""
    for i in range(1, block_size+1):
        one_short = b"A" * (block_size -i)
        encrypted_one_short = o.run(one_short * 4)
        
        options = {
            o.run(
                one_short + reverse_discovered + bytes([j])
                )[:16]: j
            for j in range(256)
        }
        reverse_discovered += bytes([options[encrypted_one_short[:16]]])

    return reverse_discovered


if __name__ == "__main__":
    o = Oracle()
    print(determine_ecb_block_size(o.run))
    