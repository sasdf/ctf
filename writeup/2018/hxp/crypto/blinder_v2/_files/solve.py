"""
Partial solution for blinder from hxpctf2018.
Idea: Reduce to solving discrete log on an elliptic curve of smooth order
Currently fails pretty often, so run multiple it times

author: tjbecker (PPP) sasdf(Balsn)

function/variable start with i means that it operates on/is number.
"""

from firstblood.all import uio
from Crypto.Cipher import AES
from functools import lru_cache
from collections import Counter
import libnum

p = 0xffffffffeb4f          # |G| = p

r = uio.spawn('python3 vuln.py')
# r = uio.tcp('116.203.21.6', 13377)

# debug
key = r.line().hexd
# aes = AES.new(key, AES.MODE_ECB)
# enc = lambda x: aes.encrypt(x.to_bytes(16, 'big')).hex()
# dec = lambda y: int.from_bytes(aes.decrypt(bytes.fromhex(y)), 'big')

one, T = r.line().split(" ")

zero = None

# Operation count
cnt = 0


# NAF representation
def NAF(k):
    z = []
    while k > 0:
        if k & 1:
            z.append(2 - k % 4)
        else:
            z.append(0)
        k = (k - z[-1]) // 2
    return tuple(z[::-1])


def BIN(k):
    return bin(k)[2:].map(int).list
    

@lru_cache(None)
def add(x, y):
    if zero is not None:
        if x == zero:
            return y
        if y == zero:
            return x
    global cnt
    cnt += 1
    print(f'cnt: {cnt}')
    return r.line(f"mul {x} {y}").line()


def iadd(x, y):
    return (x + y) % p

    
@lru_cache(None)
def mul(x, y):
    if x == one:
        return y
    if y == one:
        return x
    if zero is not None:
        if x == zero or y == zero:
            return zero
    global cnt
    cnt += 1
    print(f'cnt: {cnt}')
    return r.line(f"dhp {x} {y}").line()


def imul(x, y):
    return (x * y) % p


@lru_cache(None)
def neg(x):
    global cnt
    cnt += 1
    print(f'cnt: {cnt}')
    return r.line(f"inv {x}").line()


def ineg(x):
    return (-x) % p


def merge(points, op, identity):
    # combine neighbors first for better cache
    # example: a, b, c, d -> (a*b), (c*d)
    while len(points) > 1:
        nxt = []
        if len(points) & 1:
            nxt.append(points[-1])
            points = points[:-1]
        for a, b in points.chunk(2):
            nxt.append(op(a, b))
        points = nxt

    if len(points) == 0:
        return identity

    return points[0]


def fastMul(zero, one, add, neg, REPR):
    def _fastMul(k):
        points = []
        A = one
        for b in REPR(k).rev:
            if b == 1:
                points.append(A)
            elif b == -1:
                points.append(neg(A))
            A = add(A, A)

        return merge(points, add, zero)
    return _fastMul


def exp(x, e):
    return fastMul(one, x, mul, None, BIN)(e)


def inv(x):
    # return exp(x, p-2)
    e1, e2 = 3 * 41, 2288414444759
    r = exp(x, e1)
    return exp(r, e2)


def iinv(x):
    return pow(x, p-2, p)


def sqrt(x):
    # return exp(x, (p + 1) // 4)
    e1, e2 = 4 * 3 * 5 * 59 * 3037, 281 * 23293
    r = exp(x, e1)
    return exp(r, e2)


zero = add(one, neg(one))


embedInt = fastMul(zero, one, add, neg, NAF)


def embedPoint(p):
    x, y = p
    return (embedInt(x), embedInt(y))


fords = [2**5, 3, 5, 59, 281, 3037, 23293] # 2^5

iG = (31719700816391, 198118965997565)

order = p ** 2 - 1

O = (zero, one)
iO = (0, 1)


def _Padd(add):
    def Padd(p1, p2):
        (a, b), (c, d) = p1, p2
        return (add(a, c), add(b, d))
    return Padd


Padd = _Padd(add)
iPadd = _Padd(iadd)


def _Pneg(neg):
    def Pneg(p1):
        return tuple(map(neg, p1))
    return Pneg


Pneg = _Pneg(neg)
iPneg = _Pneg(ineg)


def _Pmul(add, mul, neg):
    def Pmul(p1, p2):
        (a, b), (c, d) = p1, p2
        # ad + bc, bd - ac
        return (add(mul(a, d), mul(c, b)), add(mul(b, d), neg(mul(a, c))))
    return Pmul


Pmul = _Pmul(add, mul, neg)
iPmul = _Pmul(iadd, imul, ineg)


def iPexp(x, e):
    return fastMul((0, 1), x, iPmul, None, BIN)(e)


def EDlogNaive(X, P, o):
    cur = iO
    for i in range(o):
        if embedInt(cur[0]) == P[0]:
            return i
        cur = iPmul(X, cur)
    assert False, f"Couldn't solve dlog {o}"


# Baby-step Giant-step
def EDlog_bsgs(iX, P, o):
    #
    #return EDlogNaive(X,P,o)
    m = int(pow(o, 0.5) + 1)
    table = {}
    cur = O
    gam = P
    X = embedPoint(iX)
    for j in range(m):
        table[cur[0]] = j
        if gam[0] in table:
            return table[gam[0]]
        cur = Pmul(cur, X)
    M = iPexp(iX, o-m)
    M = embedPoint(M)
    for i in range(m):
        if gam[0] in table:
            return i*m + table[gam[0]]
        gam = Pmul(gam, M)
    assert False, "Couldn't solve dlog" + str(o)


# Pohlig-Hellman
def EDlog(X, P):
    xs = []
    fs = []

    # calculate Pexp(P, order//f) together
    Pfs = []
    Ps = [P]
    for _ in range(94):
        Ps.append(Pmul(Ps[-1], Ps[-1]))

    for f in fords:
        z = []
        for i, b in enumerate(BIN(order // f).rev):
            if b == 1:
                z.append(Ps[i])
        Pfs.append(z)

    # Merge most common pair first
    while any(len(z) > 1 for z in Pfs):
        cnt = Counter()
        for z in Pfs:
            for p in z.combinations(2):
                p = tuple(sorted(p))
                cnt.update([p])
        (A, B), _ = cnt.most_common(1)[0]
        C = Pmul(A, B)
        for z in Pfs:
            if A in z and B in z:
                z.remove(A)
                z.remove(B)
                z.append(C)

    assert all(len(z) == 1 for z in Pfs)
    Pfs = [z[0] for z in Pfs]

    for Pf, f in zip(Pfs, fords):
        fs.append(f)
        Xf = iPexp(X, order // f)
        print("Doing dlog on factor", f)
        xs.append(EDlog_bsgs(Xf, Pf, f))
    return libnum.solve_crt(xs, fs)


P = (T, one)

dlog = EDlog(iG, P)
print(f'Done: {dlog}')
Y = iPexp(iG, dlog)
m = libnum.invmod(Y[1], p)
Y = (Y[0] * m) % p
print("GOT Y:", Y)

r.line("sol {}".format(Y))

r.interact()
