#!/usr/bin/python2
# -*- coding: utf-8 -*-


from pwn import remote
from hashlib import sha256
from Crypto.Util.number import long_to_bytes, getRandomInteger
from Crypto.Cipher import AES
import sys


def hex2int(s):
    return int(s.replace('\n', '').replace(' ', ''), 16)


def encrypt(data, key):
    aes = AES.new(key, AES.MODE_CBC, '\0' * 16)
    data += sha256(data).digest()
    pad = 16 - len(data) % 16
    data = data + chr(pad) * pad
    data = aes.encrypt(data).encode('base64')
    return data.replace('\n', '')


def decrypt(data, key):
    aes = AES.new(key, AES.MODE_CBC, '\0' * 16)
    data = aes.decrypt(data.decode('base64'))
    data = data[:-ord(data[-1])]
    data, mac = data[:-32], data[-32:]
    if sha256(data).digest() != mac:
        raise ValueError('Invalid MAC')
    return data


p = hex2int("""
a9ec265bac549eb26a36b1ddafaba4189e4506593cd37c97c3cff7ad06ab51ee
1708a59748ab06a46baea7d33f8499092db63baafd7d6f60e4718e366c705ee6
d0876db4f17a987e6b0cb1795c78f969d8b4ee446b729b7e8bbfe6472bc80157
6374ee87b1a0948408700bc39517236cb681562eec6b9a8d00d9dc9791dbca1b
""")

#-- There's a small subgroup with order 49391 --#
b = 49391
assert((p - 1) % b == 0)

#-- Generate an element in that group --#
g = 1
while g == 1 or g == p - 1:
    g = pow(getRandomInteger(1024), (p - 1) // b, p)

#-- Login --#
r = remote('localhost', 1234)
r.sendline('parconal')
sys.stdout.write(r.recvuntil('>>> '))
print('parconal')

#-- Salt, which we don't need --#
sys.stdout.write(r.recvuntil('[=] '))

#-- DHKE: remote's public key --#
sys.stdout.write(r.recvuntil('[=] '))
TER = r.recvline()
sys.stdout.write(TER)
TER = int(TER.strip(), 16)

#-- DHKE: our public key --#
r.sendline('%x' % g)
sys.stdout.write(r.recvuntil('>>> '))
print('%x' % g)

#-- Authentication challenge --#
sys.stdout.write(r.recvuntil('[=] '))
encChal = r.recvline()
sys.stdout.write(encChal)

#-- Brute force 49391 possible keys --#
chal = None
shared = g
for i in range(b):
    try:
        key = sha256(long_to_bytes(shared)).digest()
        chal = decrypt(encChal, key)
    except ValueError:
        pass
    else:
        break
    shared = (shared * g) % p
assert(chal is not None)

#-- Reply our answer --#
resp = sha256(chal).digest()
r.sendline(encrypt(resp, key))
sys.stdout.write(r.recvuntil('>>> '))
print(encrypt(resp, key))

#-- Receive secret flag --#
sys.stdout.write(r.recvuntil('[=] '))
secret = r.recvline()
sys.stdout.write(secret)
secret = decrypt(secret, key)
print(secret)
