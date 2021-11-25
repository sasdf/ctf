import numpy as np
import random
import os
import string

from tqdm import tqdm, trange
from collections import Counter


p = 251
mlen = 16 # message size
plen = 16 # padding size
rlen = 15 # input size
clen = mlen + plen # threshold
off = (ord('a') + ord('z')) // 2 # padding offset

ninst = 26 # solve with `ninst` instances

R = Zmod(p)
P.<x> = PolynomialRing(R)

print('[*] Reading inputs')
Xs, Ys, Os = [], [], []
with open('dump') as f:
    for line in f:
        if line.startswith('X: '):
            Xs.append(bytes.fromhex(line[-31:]))
        if line.startswith('Y: '):
            Ys.append(bytes.fromhex(line[-31:]))
        if line.startswith('O: '):
            Os.append(line[-plen-1:].strip().encode())

print('[*] Building lattices')
Ls = []
for x, y in list(zip(Xs, Ys))[:ninst]:
    x = (list(x) + [0] * clen)[:clen]
    x, y = vector(R, list(x)), vector(R, list(y))
    Y = matrix.column(R, [-y])
    V = matrix.vandermonde(x)
    Y, V = Y[:rlen], V[:rlen]
    V = Y.augment(V)
    B = V.right_kernel().basis_matrix()
    B = B.change_ring(ZZ)
    # print(B)

    assert B[:mlen, :mlen] == identity_matrix(mlen)

    # Remove the bias
    L = B[:, -plen:]
    L[0] = [e - off for e in L[0]]
    Ls.append(L)

print('[*] Merging lattices')
M = [[]]
for i, L in enumerate(Ls):
    M[0].append(L[:mlen+1])
    left, right = plen * i, plen * (len(Ls) - i - 1)
    L = L[mlen+1:]
    M.append([zero_matrix(L.nrows(), left), L, zero_matrix(L.nrows(), right)])
L = block_matrix(M, subdivide=False)

m = identity_matrix(L.ncols()) * p
ML = L.stack(m)

print(f'[+] Solving lattice of size {ML.ncols()} x {ML.nrows()}')
BL = ML.BKZ()

print(f'[+] Searching for solution')
for _pad in BL:
    for pad in [_pad, -_pad]:
        # Checking padding distribution
        if all(e == 0 for e in pad):
            continue
        pad = [e + off for e in pad]
        if any(e < ord('a') or e > ord('z') for e in pad):
            continue
        Ps = [bytes(pad[i:i+plen]) for i in range(0, len(pad), plen)]
        print('[+] Testing padding:')
        print(Ps)
        XX, YY = [], []
        for xs, ys, ps in list(zip(Xs, Ys, Ps)):
            zz = [(yi - sum(c * pow(xi, i+mlen, p) for i, c in enumerate(ps))) % p for xi, yi in zip(xs, ys)]
            XX.extend(xs)
            YY.extend(zz)
        XX = vector(R, XX)
        XX = matrix.vandermonde(XX)
        YY = vector(R, YY)
        try:
            print('[+] Flag:', bytes(XX.solve_right(YY).list()).rstrip(b'\0'))
        except ValueError:
            pass

if len(Os):
    c = b''.join(Os[:ninst])
    c = vector(ZZ, [e - off for e in c])

    print('[+] Debugging oracle')
    print(BL.solve_left(c))
