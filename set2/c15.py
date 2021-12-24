import pytest

from set2.c9 import pad_bytes


def validate_padding(inp: str) -> str:
    inp = inp.encode()
    num_pads = inp[-1]
    padded_bytes = inp[-1*num_pads:]
    if not (all(i == num_pads for i in padded_bytes) and len(padded_bytes) == num_pads):
        raise Exception("Invalid Padding!!")
    return inp[:-1*num_pads].decode()


if __name__ == "__main__":
    assert validate_padding(pad_bytes(b"abcacadf", 13).decode()) == "abcacadf"
    assert validate_padding(pad_bytes(b"abcd", 4).decode()) == "abcd"
    with pytest.raises(Exception):
        validate_padding("1234\01\02")
    with pytest.raises(Exception):
        validate_padding("1234\05\05\05")

    assert validate_padding("1234\01") == "1234"
    print("SUCCESS!")