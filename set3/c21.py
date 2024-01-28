

def not_value(v: int, w:int = 32):
    return v ^ ((1<<w) - 1)


def bottom_bits(v: int, w: int = 32):
    return v & ((1 <<w) - 1)

class MersenneTwister: 
    W = 32 # bits
    N = 624 # iterations
    M = 397 # middle word
    R = 31 # separation point

    # Coefficients
    A = int("9908B0DF", 16)
    B = int("9D2C5680", 16)
    C = int("EFC60000", 16)
    D = int("FFFFFFFF", 16)

    def __init__(self):
        self.s = 7
        self.t = 15

        self.u = 11
        self.l = 18

        self.MT = [0] * MersenneTwister.N
        self.index = MersenneTwister.N+1
        self.lower_mask = (1 << MersenneTwister.R) - 1 # 0x7fffffff
        self.upper_mask = bottom_bits(not_value(self.lower_mask)) #0x80000000
        self.f = 1812433253


    def seed_mt(self, seed: int):
        self.index = MersenneTwister.N
        self.MT[0] = seed
        for i in range(1, MersenneTwister.N):
            val = self.f * (self.MT[i-1] ^ (self.MT[i-1] >> (MersenneTwister.W - 2))) + i 
            self.MT[i] = bottom_bits(val)

    def extract_numbers(self):
        if self.index > MersenneTwister.N:
            raise RuntimeError("Not seeded!")
        if self.index == MersenneTwister.N:
            self.twist()
        
        y = self.MT[self.index]
        y = y ^ ((y >> self.u) & MersenneTwister.D)
        y = y ^ ((y << self.s) & MersenneTwister.B)
        y = y ^ ((y << self.t) & MersenneTwister.C)
        y = y ^ (y >> self.l)

        self.index += 1
        return bottom_bits(y)

    def twist(self):
        self.index = 0
        for i in range(MersenneTwister.N):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i+1) % MersenneTwister.N] & self.lower_mask)
            xA = x >> 1
            if x % 2 != 0:
                xA = xA ^ MersenneTwister.A
            self.MT[i] = self.MT[(i + MersenneTwister.M) % MersenneTwister.N] ^ xA


m = MersenneTwister()
m.seed_mt(5489)

# from random import Random
# r = Random(5489)
# print(bin(r.getrandbits(32)))
# It appears that this is not actually the raw MT
# outputs :(

# REF_OUTPUT came from https://asecuritysite.com/primes/twister
REF_OUTPUT = [3499211612, 581869302, 3890346734, 3586334585, 545404204, 4161255391, 3922919429, 949333985, 2715962298, 1323567403, 418932835, 2350294565, 1196140740, 809094426, 2348838239, 4264392720, 4112460519, 4279768804, 4144164697, 4156218106]

for correct_output in REF_OUTPUT:
    real_output = m.extract_numbers()
    assert real_output == correct_output
print("Success!")

