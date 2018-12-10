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


two = embedInt(2)
three = embedInt(3)

ia, ib = 66451624201262, 159479737227219

fords = [64, 17, 23, 31, 79, 139, 173, 191]

iG = (177142211969678, 203618895879441)

order = 281474973641152

O = (zero, one)
iO = (0, 1)
a, b = map(embedInt, [ia, ib])


def _Padd(O, a, zero, two, three, add, mul, inv, neg):
    def Padd(p1, p2):
        (x1, y1), (x2, y2) = p1, p2
        if (x2, y2) == O:
            return (x1, y1)
        if (x1, y1) == O:
            return (x2, y2)
        if (x1, y1) == (x2, y2):
            if y1 == zero:
                return O
            m = add(mul(three, mul(x1, x1)), a)
            m = mul(m, inv(mul(two, y1)))
        elif x1 == x2:
            return O
        else:
            m = mul(add(y2, neg(y1)), inv(add(x2, neg(x1))))
        x = add(add(mul(m, m), neg(x1)), neg(x2))
        y = add(mul(m, add(x1, neg(x))), neg(y1))
        return (x, y)
    return Padd


Padd = _Padd(O, a, zero, two, three, add, mul, inv, neg)
iPadd = _Padd(iO, ia, 0, 2, 3, iadd, imul, iinv, ineg)


def _Pneg(neg):
    def Pneg(A):
        x, y = A
        return (x, neg(y))
    return Pneg


Pneg = _Pneg(neg)
iPneg = _Pneg(ineg)


def _Pmul(O, Padd, Pneg):
    def Pmul(A, t):
        return fastMul(O, A, Padd, Pneg, NAF)(t)
    return Pmul


Pmul = _Pmul(O, Padd, Pneg)
iPmul = _Pmul(iO, iPadd, iPneg)


def EDlogNaive(X, P, o):
    cur = iO
    for i in range(o):
        if embedInt(cur[1]) == P[1]:
            return i
        cur = iPadd(X, cur)
    assert False, f"Couldn't solve dlog {o}"


# Pohlig-Hellman
def EDlog(X, P):
    xs = []
    fs = []

    # calculate Pmul(P, order//f) together
    Pfs = []
    Ps = [P]
    for _ in range(47):
        Ps.append(Padd(Ps[-1], Ps[-1]))
    for f in fords:
        z = []
        for i, b in enumerate(NAF(order // f).rev):
            if b == 1:
                z.append(Ps[i])
            elif b == -1:
                z.append(Pneg(Ps[i]))
        Pfs.append(z)

    # Merge most common pair first
    while any(len(z) > 1 for z in Pfs):
        cnt = Counter()
        for z in Pfs:
            for p in z.combinations(2):
                p = tuple(sorted(p))
                cnt.update([p])
        (A, B), _ = cnt.most_common(1)[0]
        C = Padd(A, B)
        for z in Pfs:
            if A in z and B in z:
                z.remove(A)
                z.remove(B)
                z.append(C)

    assert all(len(z) == 1 for z in Pfs)
    Pfs = [z[0] for z in Pfs]

    for Pf, f in zip(Pfs, fords):
        fs.append(f)
        Xf = iPmul(X, order//f)
        print("Doing dlog on factor", f)
        xs.append(EDlogNaive(Xf, Pf, f))
    return libnum.solve_crt(xs, fs)


RHS = add(add(exp(T, 3), mul(a, T)), b)
P = (T, sqrt(RHS))

dlog = EDlog(iG, P)
print(f'Done: {dlog}')
Y = iPmul(iG, dlog)[0]
print("GOT Y:", Y)

r.line("sol {}".format(Y))

r.interact()
