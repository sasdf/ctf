import os
import random
import string


# with open('flag.txt', 'rb') as f:
#     FLAG = f.read()
FLAG = b'ACSC{xxxxxxxxxx}'

assert len(FLAG) == 16

p = 251

def random_letters(n):
    return ''.join(random.choices(string.ascii_lowercase, k=n)).encode()

threshold = len(FLAG) + 2

nshares = threshold - (len(FLAG) + 1)

pos = [set(range(p)) for _ in range(p)]
charset = string.ascii_lowercase.encode()

while True:
    padding = random_letters(threshold - len(FLAG))
    coeff = list(FLAG + padding)

    xs = bytes(random.sample(range(1, p), k=nshares))
    ys = bytes(sum(c * pow(x, i, p) for i, c in enumerate(coeff)) % p for x in xs)
    print(f'X: {xs.hex()}')
    print(f'Y: {ys.hex()}')

    x, y = xs[0], ys[0]

    z1 = pow(x, len(FLAG), p)
    z2 = pow(x, len(FLAG)+1, p)
    st = set()
    for c1 in charset:
        for c2 in charset:
            v = (c1 * z1 + c2 * z2) % p
            v = (y - v) % p
            st.add(v)
    pos[x] = pos[x] & st

    print([len(v) for v in pos if len(v) <= 3])
