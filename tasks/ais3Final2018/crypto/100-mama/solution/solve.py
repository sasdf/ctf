#!/usr/bin/python2

from pwn import remote
import gmpy2


def mul(x, y):
    x, y = toMulGroup(x), toMulGroup(y)
    r = (x * y) % (n + 1)
    return toAddGroup(r)


def add(x, y):
    return (x + y) % n


def toMulGroup(x):
    return x if x else n


def toAddGroup(x):
    return x if x != n else 0


r = remote('localhost', 1234)
n = int(r.readline().strip()[4:], 16)
p = n + 1
r.recvline()
r.recvline()

last = 1
for i in range(128):
    x, y = [int(i, 16) for i in r.recvline().strip().split(' => ')]
    delta = (toMulGroup(x) - toMulGroup(y)) % p
    m = gmpy2.invert(delta, p)
    mx = mul(m, x)

    #-- x, y = 0, -1 --#
    r.sendline('0')
    r.sendline(hex(mul(last, m)))
    r.sendline('1')
    r.sendline(hex(-mx % n))

    #-- swap 0, -1 --#
    r.sendline('0')
    r.sendline(hex(gmpy2.invert(2, p)))
    r.sendline('1')
    r.sendline(hex(1))
    r.sendline('0')
    r.sendline(hex(2))
    r.sendline('1')
    r.sendline(hex((mx - 2) % n))

    last = delta

r.sendline('0')
r.sendline(hex(last))

r.sendline('2')

r.recvuntil('flag:')
r.recvline()
print(r.recvline())
