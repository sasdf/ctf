import numpy as np
from math import factorial
import telnetlib

from matrix import matrix # import from the task's code

n = 385
rounds = 5
offset = 2432902008176639000

r = telnetlib.Telnet('arcade.fluxfingers.net', 1820)


def matinv(m):
    """ Run Gauss-Jordan elimination """
    res = []
    e = np.eye(m.shape[0], dtype=m.dtype)
    m = np.concatenate([m, e], 1)
    m = list(m)
    for col in range(len(m)):
        i = np.argmax([r[col] for r in m])
        cur = m.pop(i)
        if not cur[col]:
            raise ValueError('Singular matrix')
        res = [r ^ (cur & r[col]) for r in res] + [cur]
        m = [r ^ (cur & r[col]) for r in m]
    res = np.stack([np.split(r, 2)[1] for r in res])
    return res


def matrix_mul(state, matrix, n=None):
    """ Matrix multiplication under GF2 """
    result = []
    assert (len(state) == len(matrix) == len(matrix[0]))
    for i in range(len(state)):
        bit = (matrix[i] & state).sum() & 1
        result.append(bit)
    return np.array(result)


def compress(lst, n):
    """ Compress array to integer """
    return sum(c * factorial(n - k - 1) for k, c in enumerate(lst))


def inv_s_layer(state, n):
    """ Inverse of chi transformation """
    # Guess first two bits
    for z in range(4):
        res = [z // 2, z % 2] + [None] * (n - 2)
        correct = True
        # Reconstruct all bits
        for i in reversed(range(n)):
            a = state[i] ^ ((1 - res[(i + 1) % n]) & res[(i + 2) % n])
            if res[i] is None:
                res[i] = a
            else:
                # Check consistency of first two bits
                if res[i] != a:
                    correct = False
        if correct:
            res = np.array(res)
            return res


list_to_num = lambda l: int(''.join(map(str, l)), 2)
num_to_list = lambda num, n: ([0] * n + [int(c) for c in bin(num)[2:]])[-n:]


def generate_keystream_block(i):
    r.write(f'{i}\n'.encode('ascii'))
    r.read_until(b'> ')
    block = r.read_until(b'\n')[:-1]
    block = int(block, 16)
    return num_to_list(block, n)


print(f'[*] Receiving challenge')
r.read_until(b'Challenge: ')
chal = int(r.read_until(b'\n')[:-1], 16)
chal = num_to_list(chal, n)
print(f'[+] Got:')
print(chal)
print()


print(f'[*] Calculate inverses')
N = factorial(n)
M = np.array(matrix)
inv = matinv(M)
invPerm = [np.array([0] * r + [1] * (n - r - 1) + [0]) for r in range(n)]


print(f'[*] Reading keystreams')
cnt = compress([1] * (n - 1), n)
i1 = N - offset + N**rounds * cnt
i2 = N - offset
s1 = np.array(generate_keystream_block(i1))
s2 = np.array(generate_keystream_block(i2))
print(f'[+] Got:')
print(s1)
print(s2)
print()


print(f'[*] Reconstruct keys')
s = s1 ^ s2
s = matrix_mul(s, inv)
s = matrix_mul(s, invPerm)
s = [s, 1 - s] # We have two possibilities when undo permutation
for _ in range(rounds):
    s = [inv_s_layer(x, n) for x in s]
    s = [matrix_mul(x, inv) for x in s]


print(f'[*] Recovering flag')
print(f'[+] Found:')
for x in s:
    x = list_to_num((x ^ chal).tolist())
    x = x.to_bytes(n // 8 + 1, 'big').strip(b'\0')
    try:
        print(x.decode('ascii'))
    except UnicodeDecodeError:
        pass
