#!/usr/bin/env python3

import math
from telnetlib import Telnet
from phe import paillier
import gmpy2

print('[*] Generating Key')
p = gmpy2.next_prime(1 << 512)
while not gmpy2.is_prime(p*2 + 1):
    p = gmpy2.next_prime(p)
p = int(p)
q = p * 2 + 1
print('[*] Generating Key...done')

n = p * q
pk = paillier.PaillierPublicKey(n)
sk = paillier.PaillierPrivateKey(pk, p, q)

c = pk.raw_encrypt(sk.q)

print('[*] Connect to Server')
t = Telnet('ot.ctf.hackover.de', 1337)
t.write('{}\n'.format(pk.n).encode())
c = pk.raw_encrypt(sk.q)
t.write('{}\n'.format(c).encode())

print('[+] Response')
c0 = int(t.read_until(b'\n').decode().strip())
c1 = int(t.read_until(b'\n').decode().strip())
print("c0 = {}".format(c0))
print("c1 = {}".format(c1))

# z0, z1 = rand(), rand()
# c = (n+1) ^ q mod n^2
# c0 = (n+1)^x0 * z0^(n*x0) * c^(x0(n-1) + r0)
# c1 = (n+1)^r1 * z1^(n*r1) * c^(r1(n-1) + x1)
# 
# d0 = x0 - q * x0 + q * r0 mod n
# d1 = r1 - q * r1 + q * x1 mod n
#
# d0 = x0 mod q
# 
# d1 = r1 - (2p+1) * r1 + (2p+1) * x1 mod n
# let r1 = p * a + (r1 mod p)
# d1 = r1 - (2p+1) * (p * a + (r1 mod p)) + (2p+1) * x1 mod n
# d1 = r1 - (2p+1) * (r1 mod p) + (2p+1) * x1 mod n
# d1 = r1 - (r1 mod p) + x1 mod p
# d1 = x1 mod p

d0 = sk.raw_decrypt(c0)
d1 = sk.raw_decrypt(c1)
x0 = d0 % sk.q
x1 = d1 % sk.p
x = x0 ^ x1
m = x.to_bytes(math.ceil(x.bit_length() / 8), 'big').decode('ascii')
print(f'[+] Flag: {m}')
