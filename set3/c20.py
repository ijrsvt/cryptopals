import base64
from set1.common import try_all_xor, repeated_xor_encrypt
from set3.c18 import encrypt, keystream
from secrets import token_bytes


def get_vecs():
    fname = __file__.replace(".py", ".txt")
    key = token_bytes(16)
    return [
        encrypt(key, base64.b64decode(line.strip()))
        for line in
        open(fname).readlines()]
vectors = get_vecs()

trunc = max(len(v) for v in vectors)
print("Minimum length of vectors:", min(len(v) for v in vectors))
out = [b"" for _ in range(len(vectors))]
for i in range(trunc):
    col = [v[i] if i < len(v) else None for v in vectors]
    col_b = bytes([b for b in col if b is not None])

    result = try_all_xor(col_b, include_keys=True)
    if not result:
        print("FAKE NEWS")
        decoded_col = bytes([35]*len(vectors))
    else:
        decoded_col, _ = result[0]
    j = 0
    i = 0
    while i < len(vectors):
        if col[j] is not None:
            out[j] += bytes([decoded_col[j]])
            j += 1
        i += 1

print("#" * min(len(v) for v in vectors))
for o in out:
    print(o.decode(), end="|\n")