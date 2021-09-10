import base64


def hex2bytes(hex_string: str) -> bytes:
    return bytes.fromhex(hex_string)

def hex2b64(hex_string: str) -> bytes:
    return base64.b64encode(hex2bytes(hex_string))
