from tqdm import tqdm, trange
from firstblood.all import uio
import libnum
import functools


# r = uio.spawn('python3 -u vuln.py')
r = uio.tcp('78.46.149.10', 13373)

one = r.until(' ')
y = r.line()

print(f'[*] 1: {one}')
print(f'[*] y: {y}')

p = 0xfffffed83c17
O = p - 1


def add(x, y):
    return r.line(f'mul {x} {y}').line()


def mul(x, y):
    return r.line(f'dhp {x} {y}').line()


def genexps(y):
    exps = [y]
    for i in trange(48 - 1, desc='genexps'):
        exps.append(mul(exps[-1], exps[-1]))
    return exps


two = add(one, one)
four = add(two, two)
five = add(one, four)
g = five
print(f'g = {g}')
gexps = genexps(g)
yexps = genexps(y)


def exp(n, exps):
    bs = (n).bin.rev
    s = [e for e, b in zip(exps, bs) if b == '1']
    if len(s) == 0:
        return one
    else:
        return functools.reduce(mul, s)


M = [2, 3, 7, 13, 47, 103, 107, 151]
gencs = [exp(O // e, gexps) for e in tqdm(M, desc='genencs')]
yencs = [exp(O // e, yexps) for e in tqdm(M, desc='genencs')]


def findord(t, b, m, o):
    assert(t != one)
    if b == one:
        print(f'o = 0')
        return 0
    assert(m != one)
    for n in range(1, o):
        if b == t:
            print(f'o = {n}')
            return n
        b = mul(b, m)
    raise ValueError('WTF' + str(o))


yords = []
for gi, yi, oi in zip(gencs, yencs, M):
    n = findord(gi, yi, yi, oi)
    yords.append(n)

print(yords)

assert(yords[1] != 0)
assert(yords[3] != 0)


def bexp(x, n):
    r = one
    for _ in range(n):
        r = mul(r, x)
    return r


def findexp(i, k):
    M1 = M[i]
    Mc = M1
    Mn = Mc * M1
    oi = yords[i]
    ym = yencs[i]
    for _ in range(k - 1):
        gb = exp(O // Mn, gexps)
        yb = exp(O // Mn * oi, yexps)
        oi = (findord(gb, yb, ym, M1) - 1) * Mc + oi
        print(f'o = {oi}')
        Mc = Mn
        Mn = Mc * M1
    M[i] = Mc
    yords[i] = oi


findexp(1, 2)
findexp(3, 4)

yords = [0 if a == 0 else libnum.invmod(a, b) for a, b in zip(yords, M)]
yo = libnum.solve_crt(yords, M)
print(yo)
sol = pow(5, yo, p)

r.line(f'sol {sol}')

r.interact()
