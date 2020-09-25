import numpy as np
from tqdm import trange, tqdm


a, b, c = 3, 13, 37
m = (1<<64)-1
"""

s0 = s[p]
p = (p + 1) % 64
s1 = s[p]
res = (s0 + s1) & m

s1 = s1 ^ (s1 << a) & m
s[p] = (s1 ^ s0 ^ (s1 >> b) ^ (s0 >> c)) & m
"""

def init():
    state = np.arange(64, dtype=np.uint64)
    state = np.frombuffer(state.tobytes(), dtype=np.uint8)
    state = np.unpackbits(state, bitorder='little')
    return state

def shift_mat(n, s):
    return np.diag(np.ones(n - abs(s), dtype=np.uint8), k=s)

def identity(*args):
    if len(args) == 1: args = args[0]
    return np.eye(args, dtype=np.uint8)

def zeros(*args):
    if len(args) == 1: args = args[0]
    return np.zeros(args, dtype=np.uint8)

O = zeros(64)
I = identity(64)
A = shift_mat(64, -a)
B = shift_mat(64, b)
C = shift_mat(64, c)
S1 = ((B+I) @ (A+I)) & 1
S0 = (C+I) & 1

M = np.block([
    [S0, S1, zeros(64, 4096-128)],
    [zeros(4096-128, 128), identity(4096-128)],
    [I, zeros(64, 4096-64)],
])


def matmul(A, B):
    A = (A & 1).astype(np.double)
    B = (B & 1).astype(np.double)
    C = (A @ B).astype(np.uint64) & 1
    return C


if True:
    E = np.load('cache.npy')
else:
    E = [M]
    for _ in trange(64):
        E.append(matmul(E[-1], E[-1]))
    E = np.stack(E)
    np.save('cache.npy', E)
    

def jump(n, state):
    R = identity(4096)
    for s in range(64):
        if (n >> s) & 1:
            state = matmul(E[s], state)
    return state


def randgen(state):
    s = np.packbits(state, bitorder='little').tobytes()
    s = np.frombuffer(s, dtype=np.uint64).tolist()
    res = (s[0] + s[1]) & m
    state = matmul(M, state)
    return state, res
    

state = init()
state = jump(31337, state)

enc = open("enc.dat", 'rb').read()
assert len(enc) == 256

flag = b""

bar = trange(len(enc))
for x in bar:
    state, buf = randgen(state)
    sh = x//2
    if sh > 64:sh = 64
    mask = (1 << sh) - 1
    buf &= mask
    state = jump(buf, state)
    state, r = randgen(state)
    flag += bytes([ enc[x] ^ (r & 0xff) ])
    tqdm.write(repr(flag))
bar.close()
print(flag)
