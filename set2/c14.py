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



def determine_ecb_block_size(enc_fn: Callable[[bytes], bytes]) -> int:
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


def find_n_target_block(encrypted: bytes, block_size: int, n: int = 1):
    prev = b""
    in_repeated = False
    for i in range(0, len(encrypted), block_size):
        chunk = encrypted[i:i+block_size]
        if prev == chunk:
            in_repeated = True
        elif in_repeated:
            return encrypted[i: i + (n)*block_size]
        prev = chunk


def decode_one_byte(o: Oracle):
    block_size = determine_ecb_block_size(o.run)
    one_short = b"A" * ((block_size * 10) - 1)    
    encrypted_one_short = {find_n_target_block(o.run(one_short), block_size) for _ in range(1000)}
    while True:
        for j in range(256):
            attempt = find_n_target_block(o.run(one_short + bytes([j])), block_size)
            if attempt in encrypted_one_short:
                return j

def decode_sixteen_bytes(o: Oracle):
    block_size = determine_ecb_block_size(o.run)
    one_short = b"A" * ((block_size * 10) - 1)    
    reverse_discovered = b""
    for i in range(1, block_size+1):
        encrypted_one_short = {find_n_target_block(o.run(one_short), block_size) for _ in range(1000)}
        flag = True
        while flag:
            for j in range(256):
                attempt = find_n_target_block(o.run(one_short + reverse_discovered + bytes([j])), block_size)
                if attempt in encrypted_one_short:
                    reverse_discovered += bytes([j])
                    flag = False
    return reverse_discovered

def decode_all(o: Oracle):
    block_size = determine_ecb_block_size(o.run)
    one_short = b"\x00" * ((block_size * 10) - 1)    
    reverse_discovered = b""
    b = 1
    while True:
        for i in range(1, block_size+1):
            encrypted_one_short = {find_n_target_block(o.run(one_short), block_size, b) for _ in range(1000)}
            flag = True
            iters = 0
            while flag:
                for j in range(1,256):
                    attempt = find_n_target_block(o.run(one_short + reverse_discovered + bytes([j])), block_size, b)
                    if attempt in encrypted_one_short:
                        reverse_discovered += bytes([j])
                        flag = False
                        break
                        # print(b"Found " + (bytes([j])))
                if iters > 1000:
                    return reverse_discovered
                iters += 1
        b += 1
        print("FOUNDER", reverse_discovered, len(reverse_discovered))



if __name__ == "__main__":
    o = Oracle()
    # print(determine_ecb_block_size(o.run))
    z = decode_one_byte(o)
    y = decode_all(o)