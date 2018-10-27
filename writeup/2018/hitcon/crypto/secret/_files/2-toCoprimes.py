import pickle
import codecs
import gmpy2
import random
import itertools as it



tohex = lambda x: codecs.encode(x, 'hex')
fromhex = lambda x: codecs.decode(x, 'hex')
xor = lambda a, b: bytes(ai ^ bi for ai, bi in zip(a, b))

def pairGCD(nums):
    factors = set()
    for a, b in it.combinations(nums, r=2):
        g = gmpy2.gcd(a, b)
        if g != 1:
            factors.add(int(g))
    return factors


def factorize(nums, include=False):
    factors = pairGCD(nums)
    if len(factors) == 0:
        return nums
    factors = factorize(factors, include=True)
    if include:
        nums = list(nums)
        for f in factors:
            for i, e in enumerate(nums):
                while e % f == 0:
                    e //= f
                nums[i] = e
        nums = set(nums)
    else:
        nums = set()
    if 1 in nums:
        nums.remove(1)
    nums.update(factors)
    return nums


def toCoprime(nums):
    nums = nums[:]
    factors = factorize(nums)
    for i, e in enumerate(nums):
        for f in factors:
            while e % f == 0:
                e //= f
            nums[i] = e
    return nums

with open('N.txt') as f:
    data = int(f.read()).to_bytes(128, 'little')

with open('o.pkl', 'rb') as f:
    overflow = pickle.load(f)

with open('c.pkl', 'rb') as f:
    cs = pickle.load(f)

# p = int.from_bytes(b'key:' + b'1' * 16, 'big')

# print(data)
nums = []
for o, c in zip(overflow, cs):
    o = codecs.decode(o, 'hex')
    n = o + data[4:]
    n = int.from_bytes(n, 'little')
    c = int.from_bytes(codecs.decode(c, 'hex'), 'big')
    # assert(c < n)
    # assert (c == pow(p, 217, n))
    nums.append(n)

Ns = toCoprime(nums)
Cs = [int.from_bytes(codecs.decode(c, 'hex'), 'big') % n for c, n in zip(cs, nums)]
pairs = []
for c, n in zip(Cs, Ns):
    pairs.append((c, n))
with open('pair.pkl', 'wb') as f:
    pickle.dump(pairs, f, protocol=2)
