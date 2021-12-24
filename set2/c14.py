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

def find_n_target_block(encrypted: bytes, block_size: int, n: int = 1, num_sequential:int = 3):
    prev = b""
    num_repeat = 1
    for i in range(0, len(encrypted), block_size):
        chunk = encrypted[i:i+block_size]
        if prev == chunk:
            num_repeat += 1
        elif num_repeat == num_sequential:
            return encrypted[i: i + (n)*block_size]
        else:
            num_repeat = 1
        prev = chunk
    return None

def process_encrypted_short(inp: Counter) -> bytes:
    output = inp.copy()
    output.pop(None, None)
    return sorted(output.items(), key=lambda x: x[1], reverse=True)[0][0]

def decode_one_byte(o: Oracle):
    block_size = determine_ecb_block_size(o.run)
    one_short = b"A" * ((block_size * 3)) + b"\x01" * (block_size -1)    
    encrypted_one_short = Counter(find_n_target_block(o.run(one_short), block_size) for _ in range(1000))
    expected = process_encrypted_short(encrypted_one_short)
    while True:
        for j in range(256):
            attempt = find_n_target_block(o.run(one_short + bytes([j])), block_size)
            if attempt is not None and  attempt == expected:
                return j

def decode_sixteen_bytes(o: Oracle):
    block_size = determine_ecb_block_size(o.run)
    prefix = b"A" * ((block_size * 3)) 
    reverse_discovered = b""
    for i in range(1, block_size+1):
        one_short = prefix + b"\x01" * (block_size -i)
        encrypted_i_short = Counter(find_n_target_block(o.run(one_short), block_size) for _ in range(1000))
        expected = process_encrypted_short(encrypted_i_short)
        flag = True
        while flag:
            for j in range(256):
                one_short = prefix + b"\x01" * (block_size -i) + reverse_discovered + bytes([j])
                attempt = find_n_target_block(o.run(one_short), block_size)
                if attempt is not None and attempt == expected:
                    reverse_discovered += bytes([j])
                    flag = False
                    break
    return reverse_discovered

def decode_all(o: Oracle):
    block_size = determine_ecb_block_size(o.run)
    prefix = b"\x00" * (block_size * 3)    
    reverse_discovered = b""
    b = 1
    while True:
        for i in range(1, block_size+1):
            test_input = prefix + b"\x01" * (block_size - i)
            encrypted_one_short = Counter(find_n_target_block(o.run(test_input), block_size, b) for _ in range(1000))
            expected = process_encrypted_short(encrypted_one_short)
            flag = True
            iters = 0 
            while flag:
                for j in range(1,256):
                    one_short = prefix + b"\x01" * (block_size - i ) + reverse_discovered + bytes([j])
                    attempt = find_n_target_block(o.run(one_short), block_size, b)
                    if attempt == expected:
                        reverse_discovered += bytes([j])
                        flag = False
                        break
                iters += 1
                if iters == 100:
                    return reverse_discovered
        b += 1



if __name__ == "__main__":
    o = Oracle()
    print(bytes([decode_one_byte(o)]))
    print(decode_sixteen_bytes(o).decode("UTF-8"))
    print("FINAL ITEM")
    print(decode_all(o).decode("UTF-8"))