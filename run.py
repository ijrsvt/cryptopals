import base64
from set1.c1 import *
from set1.c2 import *
from set1.c3 import *
from set1.c4 import *
from set1.c5 import *
from set1.c6 import *
from set1.c7 import *

# Set C2
# print(xor("686974207468652062756c6c277320657965", "1c0111001f010100061a024b53535009181c"))
# print(xor2hex("686974207468652062756c6c277320657965", "1c0111001f010100061a024b53535009181c"))

# Set C3
# print(try_all_xor_hex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"))

# Set C4
# print(try_all_inputs("set1/c4_input.txt"))

# Set C5
#print(bytes2hex(repeated_xor_encrypt_strings("Burning 'em, if you ain't quick and nimble\n" + "I go crazy when I hear a cymbal", "ICE")))

# Set C6
# # assert hamming_distance("this is a test".encode(), "wokka wokka!!!".encode()) == 37
# b = base64.b64decode(open("set1/6.txt").read())
# print(find_key_size(b, top_n=10))
# # test_find_key_size()
# out = brute_force_repeated_xort(b, 29)
# print("The Key is:\n", bytes(out[1]))
# print("The Message is:\n", repeated_xor_encrypt(b, out[1]).decode())


# Set C7
b = base64.b64decode(open("set1/7.txt").read())
print(decrypt_aes_128(b, b"YELLOW SUBMARINE").decode())