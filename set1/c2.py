import binascii


def xor(bytes_one: bytes, bytes_two: bytes) -> bytes:
    xord = [ x[0] ^ x[1] for x in  zip(bytes_one, bytes_two)]
    return bytes(xord)

def xor2hex(hs1: str, hs2: str) -> str:
    bytes_one = binascii.unhexlify(hs1)
    bytes_two = binascii.unhexlify(hs2)
    return binascii.hexlify(xor(bytes_one, bytes_two)).decode()


if __name__ == "__main__":
    assert(xor2hex(
        "686974207468652062756c6c277320657965", 
        "1c0111001f010100061a024b53535009181c") == "746865206b696420646f6e277420706c6179")