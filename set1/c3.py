from typing import List, Optional, Tuple, Union

from .c1 import hex2bytes
from .c2 import bytes2hex, xor


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

def try_all_xor(inp_bytes: bytes, include_keys=True) -> List[Union[bytes, Tuple[bytes, int]]]:
    all_options = [try_xor(inp_bytes, i) for i in range(255)]
    valid_options = [(a,i) for i, a in enumerate(all_options) if a is not None]
    valid_options.sort(key=lambda x: sum(x[0].decode().count(y) for y in MOST_COMMON), reverse=True)
    if include_keys:
        return valid_options
    else:
        return [x[0] for x in valid_options]

def try_all_xor_hex(inp_hex: str) -> List[bytes]:
    return try_all_xor(hex2bytes(inp_hex), include_keys=False)