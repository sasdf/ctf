import multiprocessing as mp
from tqdm import tqdm, trange
from collections import defaultdict

from untamper import untamper, tamper
from pr import getindices
from posRange import PosRange
from mt import MT19937, tobin

import hashlib


obs = []
with open('../task/output.1.txt') as f:
    f.readline()
    for _ in range(0x1337):
        obs.append(int(f.readline()))
    enc = f.readline().strip().split(' ')[1]
    enc = bytes.fromhex(enc)
states = [untamper(o) for o in obs]


def check(a, b, c):
    a = a & 0x7fffffff
    x = b ^ (a >> 1)
    if a & 1:
        x ^= 0x9908b0df
    x = x | (1 << 30)
    y = c | (1 << 30)
    return x == y


indices = getindices(p=3133731337/(1 << 32), eps=1e-5)
print(len(indices))


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
    pool = mp.Pool(16)
    size = len(states) - 312
    bar = tqdm(pool.imap(search, range(size)), total=size)
    ret = []
    try:
        for res in bar:
            if res is not None:
                bar.desc = f'[o] Chains - {len(ret)} found'
                a, b, c = res
                ret.append(res)
    finally:
        bar.close()
        pool.close()
    return ret


chains = getChains(1e-8)

edges = defaultdict(list)
for a, b, c in chains:
    edges[a].append((b, 396))
    edges[a].append((c, 623))
    edges[b].append((a, -396))
    edges[b].append((c, 227))
    edges[c].append((a, -623))
    edges[c].append((b, -227))

visited = {}
def dfs(e, component, pos):
    p = visited.get(e)
    if p is not None:
        assert(p == pos)
        return
    visited[e] = pos
    component.append((e, pos))
    for n, d in edges[e]:
        dfs(n, component, pos + d)


components = []
for i in range(len(states)):
    if i not in visited:
        component = []
        dfs(i, component, 0)
        component = tuple(sorted(component))
        components.append(component)
components = sorted(components, key=lambda x: len(x))[::-1]
node2comp = {}
for c in components:
    for e, p in c:
        node2comp[e] = c


def propagateComponent(alignments, comp):
    alter = False

    # Find most strict position range
    pos = alignments[comp[0][0]].copy()
    for e, p in comp[1:]:
        pos = pos & (alignments[e] - p)

    # Propagate the range to component's elements
    for e, p in comp:
        old = alignments[e].copy()
        alignments[e] &= pos + p
        if alignments[e] < old:
            alter = True

    return alter


def propagateNeighbors(alignments):
    alter = 0

    # Forward propagation of left side
    for i in range(1, len(alignments)):
        start = alignments[i-1].start + 1
        if alignments[i].start < start:
            alter += 1
            alignments[i].start = start

    # Backward propagation of right side
    for i in range(0, len(alignments)-1):
        stop = alignments[i+1].stop - 1
        if alignments[i].stop > stop:
            alter += 1
            alignments[i].stop = stop

    return alter


alignments = [PosRange(-1000000000 + i, 1000000000 - i) for i in range(len(states))]

alignments[components[0][0][0]] = PosRange(0)
alter = 1
cs = [c for c in components if len(c) > 1]
bar = tqdm()
while alter:
    alter = 0
    for c in cs:
        alter += propagateComponent(alignments, c)
    alter += propagateNeighbors(alignments)
    bar.desc = f'[o] Shrinking - {alter} changed'
    bar.update()
bar.close()


recover = [(s, i, a.start) for i, (s, a) in enumerate(zip(states, alignments)) if a.det]
print(f'[+] {len(recover)} points recovered')

mt = MT19937()
left = recover[0][2]
right = recover[-1][2]
alignedStates = [None] * (right - left + 1)
for s, i, p in recover:
    alignedStates[p - left] = s

prng = remain = None
bar = tqdm(alignedStates)
for s in bar:
    if prng is not None:
        prng.getrandbits(32)
        continue
    if s is None:
        for _ in range(32):
            remain = mt.add(None)
    else:
        for b in tobin(tamper(s)):
            remain = mt.add(b)
    bar.desc = f'[o] Reconstruct - {remain} remain'
    if remain == 0:
        prng = mt.reconstruct('python')
bar.close()

for _ in range(len(states) - recover[-1][1] - 1):
    prng.randrange(3133731337)


sha512 = hashlib.sha512()
for _ in range(1000):
    rnd = prng.getrandbits(32)
    sha512.update(str(rnd).encode('ascii'))

key = sha512.digest()

flag = bytes(a ^ b for a, b in zip(enc, key))
print(flag)
