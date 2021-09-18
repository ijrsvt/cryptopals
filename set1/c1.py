import binascii

hex2bytes = binascii.unhexlify

def hex2b64(hex_string: str) -> bytes:
    return binascii.b2a_base64(hex2bytes(hex_string), newline=False)



if __name__ == "__main__":
    inp = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    assert(hex2b64(inp) == \
        b"SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t")