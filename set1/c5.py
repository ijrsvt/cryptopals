import binascii


def repeated_xor_encrypt(input_b: bytes, key_b: bytes) -> bytes:
    return bytes([b ^ key_b[indx % len(key_b)] for indx, b in enumerate(input_b)])



if __name__ == "__main__":
    input_str = "Burning 'em, if you ain't quick and nimble\n" + "I go crazy when I hear a cymbal"
    output = repeated_xor_encrypt(input_str.encode(), "ICE".encode())
    assert binascii.hexlify(output).decode() == (
        "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272"
        "a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
    )