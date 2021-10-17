import binascii
from collections import defaultdict
from typing import List

from set1.common import try_all_xor, repeated_xor_encrypt

def hamming_byte_distance(b1: int, b2: int) -> int:
    differing = b1 ^ b2
    return sum(
        (differing >> i) & 1
        for i in range(8)
    )


def hamming_distance(s1_b: bytes, s2_b: bytes) -> int:
    return sum(hamming_byte_distance(b1, b2) for b1, b2 in zip(s1_b, s2_b))


def find_key_size(input_bytes: bytes, 
                  min_key_size: int = 2, 
                  max_key_size: int = 40, 
                  top_n: int = 5,
                  debug: bool = False
            ) -> List[int]:
    results = defaultdict(list)
    for key_size in range(min_key_size, min(max_key_size + 1, int(len(input_bytes) / 2))):
        num_iters = int(len(input_bytes) / (key_size * 2))
        dist = sum(
            hamming_distance(input_bytes[key_size*i:key_size*(i+1)],
                            input_bytes[key_size*(i+1):(i+2)*key_size])
                    for i in range(num_iters)
        )
        dist /= (key_size * num_iters )
        # dist = hamming_distance(input_bytes[:key_size], input_bytes[key_size:2*key_size]) / key_size

        results[dist].append(key_size)
    output = [
        (key, edit_distance) 
        for edit_distance in sorted(results.keys())
        for key in results[edit_distance]
    ]
    if debug:
        for key_size, edit_distance in output[:top_n]:
            print(f"KEY_SIZE: {key_size}; EDIT_DISTANCE: {edit_distance}")

    return [i[0] for i in output[:top_n]]

def test_find_key_size():
    varying = "123456789zxcvbnm,.asdfghjkl;qwertyu"
    inp = varying * 3
    assert find_key_size(inp.encode(), top_n=1)[0] == len(varying)
    inp2 = "2" + inp[1:]
    assert find_key_size(inp2.encode(), top_n=1)[0] == len(varying)
    inp3 = varying[:10] + varying
    assert find_key_size(inp3.encode(), top_n=1)[0] == 10


def brute_force_repeated_xort(input_bytes: bytes, key_size: int):
    chunks = defaultdict(list)
    for i, b in enumerate(input_bytes):
        chunks[i%key_size].append(b)
    assert sum(len(chunks[i]) for i in range(len(chunks))) == len(input_bytes)
    possible_keys = {
        k : try_all_xor(v, include_keys=True) for k, v in chunks.items()
    }
    return possible_keys, bytes([possible_keys[i][0][1] for i in range(key_size)])

if __name__ == "__main__":
    assert hamming_distance("this is a test".encode(), "wokka wokka!!!".encode()) == 37
    b = binascii.a2b_base64(open("6.txt").read())
    print(find_key_size(b, top_n=10))
    test_find_key_size()
    out = brute_force_repeated_xort(b, 29)
    print("The Key is:\n", bytes(out[1]))
    print("The Message is:\n", repeated_xor_encrypt(b, out[1]).decode())
    assert out[1].decode() == "Terminator X: Bring the noise"