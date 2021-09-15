

def pad_bytes(inp: bytes, block_size: int) -> bytes:
    num_to_pad = block_size - (len(inp) % block_size)
    result = inp + bytes([num_to_pad]) * num_to_pad
    assert len(result) % block_size == 0, "Padding Failed!!"
    return result

if __name__ == "__main__":  
    print(pad_bytes(b"Yellow Submarine", 20))
    print(pad_bytes(b"Yellow Submarine", 14))
    print(pad_bytes(b"Yellow Submarine", 14)[-1] == 12)