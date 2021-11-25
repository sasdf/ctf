import random
import numpy as np
import itertools
import subprocess
import os


def _int32(x):
    return int(0xFFFFFFFF & x)


_zero = set()
_one = set((624 * 32,))


def frombin(s):
    return int(''.join(map(str, reversed(s))), 2)


def tobin(s):
    s = bin(s)[2:].rjust(32, '0')
    s = list(map(int, s))[::-1]
    return s


def SHL(x, n):
    return [_zero for _ in range(n)] + x[:-n]


def SHR(x, n):
    return x[n:] + [_zero for _ in range(n)]


def _xor(x, y):
    if x is _zero:
        return y
    if y is _zero:
        return x
    return x ^ y


def XOR(x, y):
    return [_xor(a, b) for a, b in zip(x, y)]


def ANDi(x, y):
    y = tobin(y)
    return [a if b else _zero for a, b in zip(x, y)]


class MT19937:
    def __init__(self):
        self.mt = [[set((b,)) for b in range(i*32, (i+1)*32)] for i in range(624)]
        self.i = 624
        self.off = 0
        self._gen = self.geniter()
        self._sol = None
        path = os.path.join(os.path.dirname(__file__), 'mt-solve')
        self._solver = subprocess.Popen([path], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        self.remain = 19937

    def geniter(self):
        while True:
            if self.i == 624:
                self.twist()
                self.i = 0

            y = self.mt[self.i]
        
            y = XOR(y, SHR(y, 11))
            y = XOR(y, ANDi(SHL(y, 7), 0x9d2c5680))
            y = XOR(y, ANDi(SHL(y, 15), 0xefc60000))
            y = XOR(y, SHR(y, 18))
            
            self.i += 1
            self.off += 1

            yield from y

    def __iter__(self):
        return self._gen

    def add(self, n):
        expr = next(self._gen)
        if self._sol is not None:
            return 0
        if n is None:
            return self.remain
        if n:
            expr = expr ^ _one
        expr = ' '.join(map(str, list(expr))) + '\n'
        self._solver.stdin.write(expr.encode('ascii'))
        self._solver.stdin.flush()
        res = int(self._solver.stdout.readline())
        if res == 0:
            self._sol = self._solver.stdout.readline().strip()
        self.remain = res
        return self.remain
        
    def reconstruct(self, prng='python'):
        state = list(map(int, self._sol.decode('ascii')))
        state = [state[i:i+32] for i in range(0, 624*32, 32)]

        if prng == 'python':
            state = tuple([frombin(s) for s in state] + [624])
            state = (3, state, None)
            r = random.Random(0)
            r.setstate(state)
            for _ in range(self.off):
                r.getrandbits(32)
        elif prng == 'numpy':
            state = tuple([frombin(s) for s in state])
            state = ('MT19937', np.array(state, dtype=np.uint32), 624, 0, 0.0)
            r = np.random.RandomState(1)
            r.set_state(state)
            for _ in range(self.off):
                r.randint(256)
        else:
            raise KeyError('Unknown PRNG')
        return r

    def twist(self):
        for i in range(0, 624):
            y = ANDi(self.mt[i], 0x80000000)
            y = XOR(y, ANDi(self.mt[(i + 1) % 624], 0x7fffffff))
            r = XOR(self.mt[(i + 397) % 624], SHR(y, 1))
            m = [y[0] if b else _zero for b in tobin(0x9908b0df)]
            r = XOR(r, m)
            self.mt[i] = r


if __name__ == '__main__':
    m = MT19937()

    res, i = 19937, 0
    while res:
        i += 1
        if i % 128 == 0:
            for _ in range(16):
                np.random.randint(0, 256)
            for _ in range(16 * 32):
                m.add(None)
        a = np.random.randint(0, 128)
        a = tobin(a)[:7]
        for b in a:
            res = m.add(b)
        for _ in range(32-7):
            m.add(None)
        if i % 28 == 0:
            print(i, res)
    print(res, m.remain)
    s = m.reconstruct('numpy')
    for i in range(624*10):
        a, b = np.random.randint(0, 1<<32), s.randint(0, 1<<32)
        assert(a == b)
        if i % 62 == 0:
            print(i)
    print('OK')
