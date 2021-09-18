import binascii
from collections import Counter
from typing import Tuple



def matching_ecb_128_blocks(msg: bytes) -> Tuple[bool, int]:
    split = [msg[i:i+16] for i in  range(0,len(msg),16)]
    counts = Counter(split).values()
    non_unique = sum(c-1 for c in counts if c > 1)
    return non_unique > 0, non_unique 

def find_ecb_128(hex_lines: str) -> bytes:
    max_overlap = 0
    likely_line = b''
    for line in hex_lines.split("\n"):
        if not line:
            continue
        good, counts = matching_ecb_128_blocks(binascii.unhexlify(line))
        if good and counts > max_overlap:
            max_overlap = counts
            likely_line = binascii.unhexlify(line)
    return likely_line

if __name__ == "__main__":
    line = find_ecb_128(open("8.txt").read())
    print(matching_ecb_128_blocks(line))
    assert matching_ecb_128_blocks(line)[1] > 1
