import random
import json
import itertools
import functools
import heapq
import textwrap
import sys

from scipy.stats import hypergeom, binom
from Crypto.Util.number import isPrime
from sympy import mod_inverse


prime_len = 1024
bits_len = 180


def generate_prime(prime_len, check_prime=True):
    while True:
        bits = random.getrandbits(bits_len)
        idxs = random.sample(range(1, prime_len-2), bits_len)
        p = 1 | 2**(prime_len - 1) | 2**(prime_len - 2)
        for i in range(bits_len):
            p += (bits >> i & 1)*2**idxs[i]
        if not check_prime or isPrime(p):
            return p



local = True
if local:
    p = generate_prime(prime_len)
    q = generate_prime(prime_len)
    n = p * q
else:
    with open('pair.json') as f:
        data = json.load(f)
    q = p
    n = data[int(sys.argv[1])][0]



# Probability about numbers of bits in the prime
tol = 1e-6
rv = binom(bits_len, 0.5)
binom_left = int(rv.ppf(tol))
binom_right = int(rv.ppf(1 - tol))
binom_values = {i: rv.pmf(i) for i in range(binom_left, binom_right+1)}

@functools.lru_cache(maxsize=100000)
def get_proba(nbits, size):
    """Get the probability of given number is sampled from our prime distribution"""
    p = 0
    for i, b in binom_values.items():
        p += b * hypergeom.pmf(nbits, prime_len-3, i, size)
    return p


@functools.lru_cache(maxsize=100000)
def get_nbits(a):
    return sum(map(int, bin(a)[2:]))


def fitness(pn, qn, size):
    """Get the probability of given number is lower bits of n's factor"""
    qprob = get_proba(qn, size-1)
    pprob = get_proba(pn, size-1)
    prob = qprob * pprob
    # prob = prob ** (1 / (size-1))
    prob = prob * (size - 1)
    return prob


def debug_diff(u, size):
    """debug log"""
    if local:
        # show difference
        M = 1 << size
        MM = M - 1
        v = p if get_nbits((p&MM) ^ u) < get_nbits((q&MM) ^ u) else q
        return bin(u ^ v)[2:].rjust(prime_len, '0')
    else:
        # show current number
        return bin(u)[2:].rjust(prime_len, '0')


# (score, size, p, q, n, pn, qn)
queue = [(0, 1, 1, 1, 1, 0, 0)]

def main():
    cnt = 0
    while len(queue):
        score, size, pp, qq, nn, pn, qn = queue[0]

        # Logging
        if cnt & 0xffff == 0:
            print(f'{score:.4f} {size:4d} {len(queue)}')
            dbg = debug_diff(pp, size)
            dbg = '\n'.join(textwrap.wrap(dbg))
            dbg = textwrap.indent(dbg, ' ' * 4)
            print(dbg)
        cnt += 1

        # Checking
        if pp != 1 and pp != n and n % pp == 0:
            print(f'Found {pp}')
            break

        # Expand
        if size < 1024:
            mask = (1 << (size + 1)) - 1
            if (n & mask) == (nn & mask):
            # if ((n >> size) & 1) == ((nn >> size) & 1):
                score = -fitness(pn, qn, size + 1)
                heapq.heapreplace(queue, (score, size + 1, pp, qq, nn, pn, qn))
                # assert ((pp * qq) & mask) == (nn & mask) == (n & mask)
                score = -fitness(pn + 1, qn + 1, size + 1)
                qqq = qq | (1 << size)
                ppp = pp | (1 << size)
                nnn = nn + (pp << size) + (qqq << size)
                # assert ((ppp * qqq) & mask) == (nnn & mask) == (n & mask)
                heapq.heappush(queue, (score, size + 1, ppp, qqq, nnn, pn+1, qn+1))
            else:
                score = -fitness(pn, qn + 1, size + 1)
                qqq = qq | (1 << size)
                nnn = nn + (pp << size)
                # assert ((pp * qqq) & mask) == (nnn & mask) == (n & mask)
                heapq.heapreplace(queue, (score, size + 1, pp, qqq, nnn, pn, qn + 1))
                score = -fitness(pn + 1, qn, size + 1)
                ppp = pp | (1 << size)
                nnn = nn + (qq << size)
                # assert ((ppp * qq) & mask) == (nnn & mask) == (n & mask)
                heapq.heappush(queue, (score, size + 1, ppp, qq, nnn, pn + 1, qn))
        else:
            # Failed
            heapq.heappop(queue)

main()
