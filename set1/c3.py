from typing import List, Optional

from .c1 import hex2bytes
from .c2 import bytes2hex, xor


HEURISTIC_VALID = 0.9

def is_valid(inp_bytes: bytes) -> bool:
    if not inp_bytes.isascii():
        return False

    num_valid = sum(1.0 for x in inp_bytes if bytes([x]).isalnum() or b" " == bytes([x]))

    return num_valid/len(inp_bytes) >  HEURISTIC_VALID

def try_xor(inp_hex: str, k: int) -> Optional[bytes]:
    b_list = hex2bytes(inp_hex)
    xord = xor(b_list, bytes([k]*len(b_list)))
    if is_valid(xord):
        
        return xord
    return None

def try_all_xor(inp_hex: str) -> List[bytes]:
    all_options = [try_xor(inp_hex, i) for i in range(255)]
    return [a for a in all_options if a is not None]

