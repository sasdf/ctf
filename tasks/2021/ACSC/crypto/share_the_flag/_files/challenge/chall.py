#!/usr/bin/env python3
import os
import random
import string


with open('flag.txt', 'rb') as f:
    FLAG = f.read().strip()
assert FLAG.startswith(b'ACSC{')
assert FLAG.endswith(b'}')
SECRET = FLAG[5:-1]
assert len(SECRET) == 16

p = 251

def random_letters(n):
    return ''.join(random.choices(string.ascii_lowercase, k=n)).encode()

print("""\
.----------------.
| Share the flag |
'----------------'

Welcome to our flag-sharing service.
We understand some of you couldn't resist sharing flags with others,
but it is STRICTLY PROHIBITED by the rules.
In order to satisfy your desire...
We made the official flag sharing service for you,
with a new algorithm inspired by Shamir Secret Sharing.

""")

# You'll need at least `threshold` shares to unlock the flag
threshold = 32

# Admin holds `len(SECRET) + 1` shares.
nshares = threshold - (len(SECRET) + 1)

# Splitting the flag
padding = random_letters(threshold - len(SECRET))
coeff = list(SECRET + padding)

xs = bytes(random.sample(range(1, p), k=nshares))
ys = bytes(sum(c * pow(x, i, p) for i, c in enumerate(coeff)) % p for x in xs)
print(f'X: {xs.hex()}')
print(f'Y: {ys.hex()}')
