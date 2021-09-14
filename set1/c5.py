


def repeated_xor_encrypt(input_b: bytes, key_b: bytes) -> bytes:
    return bytes([b ^ key_b[indx % len(key_b)] for indx, b in enumerate(input_b)])

def repeated_xor_encrypt_strings(input_str: str, key: str) -> bytes:
    return repeated_xor_encrypt(input_str.encode(), key.encode())

