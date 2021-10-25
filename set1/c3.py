import binascii
from typing import List, Optional, Tuple, Union

from set1.c2 import xor


HEURISTIC_VALID = 0.7


MOST_COMMON = [" ", "e", "t", "a", "o", "i"]

def is_valid(inp_bytes: bytes) -> bool:
    if not inp_bytes.isascii():
        return False

    num_valid = sum(1.0 for x in inp_bytes if bytes([x]).isalnum() or b" " == bytes([x]))

    return num_valid/len(inp_bytes) >  HEURISTIC_VALID

def try_xor(b_list: str, k: int) -> Optional[bytes]:
    xord = xor(b_list, bytes([k]*len(b_list)))
    if is_valid(xord):
        
        return xord
    return None

def score(inp_bytes: bytes) -> int:
    score = 0
    for char in inp_bytes.decode():
        if char in MOST_COMMON:
            score += 1
        elif not char.isalnum():
            score -= 1
    return sum(inp_bytes.decode().count(y) for y in MOST_COMMON)

def try_all_xor(inp_bytes: bytes, include_keys=True) -> List[Union[bytes, Tuple[bytes, int]]]:
    all_options = [try_xor(inp_bytes, i) for i in range(255)]
    valid_options = [(a,i) for i, a in enumerate(all_options) if a is not None]
    valid_options.sort(key=lambda x: score(x[0]), reverse=True)
    if include_keys:
        return valid_options
    else:
        return [x[0] for x in valid_options]


if __name__ == "__main__":
    inp = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    text, key = try_all_xor(binascii.unhexlify(inp), include_keys=True)[0]
    print(f"Decrypted: {text.decode()}")
    assert key == 88