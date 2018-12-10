import random


p = 0xffffffffeb4f
F = GF(p)
score = 100000000

while True:
    a = random.randrange(p)
    b = random.randrange(p)
    C = EllipticCurve(F, [a,b])
    factors = [f^k for f, k in factor(C.cardinality())]
    s = 2000 * len(factors)
    for f in factors:
        m = int(pow(f, 0.5) + 1)
        s += f / 2 * 24
    if s < score:
        g = C.gen(0)
        print(factors, s, a, b, g, C.cardinality())
        score = s
