import random
import multiprocessing as mp
from tqdm import tqdm, trange
from collections import defaultdict

from untamper import untamper, tamper
from pr import getindices
from posRange import PosRange
from mt import MT19937, tobin

from IPython import embed


# r = random.Random(31337)
# obs = [r.randrange(1<<31) for _ in range(624 * 45)]
# states = [untamper(o) for o in obs]

def init():
    global realpos, states, dbg
    r = random.Random()
    r.randint(0, 10)
    dbg = list(r.getstate()[1][:-1])
    for _ in range(90):
        _ = [r.getrandbits(32) for _ in range(624)]
        dbg += list(r.getstate()[1][:-1])
    dbg = dbg[2:]
    realpos = list(range(len(dbg)))
    realpos = [i for i, s in zip(realpos, dbg) if tamper(s) < (1<<31)]
    states = [s for s in dbg if tamper(s) < (1<<31)]


def check(a, b, c):
    a = a & 0x7fffffff
    x = b ^ (a >> 1)
    if a & 1:
        x ^= 0x9908b0df
    x = x | (1 << 30)
    y = c | (1 << 30)
    return x == y


indices = getindices(1e-8)


def search(ai):
    a = states[ai]
    for bi, ci in indices:
        bi, ci = bi + ai, ci + ai
        if ci >= len(states):
            continue
        b, c = states[bi], states[ci]
        if check(a, b, c):
            return ai, bi, ci


def getChains(eps=1e-8):
    pool = mp.Pool(30)
    size = len(states) - 312
    bar = tqdm(pool.imap(search, range(size)), total=size)
    ret = []
    try:
        for res in bar:
            if res is not None:
                bar.desc = f'[o] Chains - {len(ret)} found'
                a, b, c = res
                assert(realpos[a] + 396 == realpos[b])
                assert(realpos[a] + 623 == realpos[c])
                ret.append(res)
    finally:
        bar.close()
        pool.close()
    return ret


failed = 0
for n in range(10000):
    init()
    try:
        chains = getChains(1e-8)
    except AssertionError:
        failed += 1
    print(f'Rate: {failed * 100 / (n + 1): 0.4f}')
