from set1.c1 import *
from set1.c2 import *
from set1.c3 import *
from set1.c4 import *
from set1.c5 import *

# Set C2
# print(xor("686974207468652062756c6c277320657965", "1c0111001f010100061a024b53535009181c"))
# print(xor2hex("686974207468652062756c6c277320657965", "1c0111001f010100061a024b53535009181c"))

# Set C3
# print(try_all_xor("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"))

# Set C4
# print(try_all_inputs("set1/c4_input.txt"))

# Set C5
print(bytes2hex(repeated_xor_encrypt_strings("Burning 'em, if you ain't quick and nimble\n" + "I go crazy when I hear a cymbal", "ICE")))

