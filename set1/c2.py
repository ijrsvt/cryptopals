from .c1 import hex2bytes


def bytes2hex(b: bytes) -> str:
    return b.hex()

def xor(bytes_one: bytes, bytes_two: bytes) -> bytes:
    xord = [ x[0] ^ x[1] for x in  zip(bytes_one, bytes_two)]
    return bytes(xord)

def xor2hex(hs1: str, hs2: str) -> str:
    bytes_one = hex2bytes(hs1)
    bytes_two = hex2bytes(hs2)
    return bytes2hex(xor(bytes_one, bytes_two))