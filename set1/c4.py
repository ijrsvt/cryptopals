import binascii
from itertools import chain
from typing import List

from common import try_all_xor, score


def try_all_inputs(file_name: str) -> List[bytes]:
    inputs = open(file_name).readlines()
    results = list(chain(*[try_all_xor(binascii.unhexlify(f.strip())) for f in inputs]))
    results.sort(key=lambda x: score(x[0]), reverse=True)
    return results

if __name__ == "__main__":
    outputs = try_all_inputs("set1/c4_input.txt")
    print(f"Decoded: {outputs[0][0].decode()}")
    assert outputs[0][1] == 53