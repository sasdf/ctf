#!/usr/bin/python2
# -*- coding: utf-8 -*-


from pwn import remote
from hashlib import sha256
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES


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


r = remote('localhost', 1234)

r.sendline('enforle')
r.recvuntil('[=] ')
salt = r.recvline().strip().decode('base64')
pwd = "farvil{Ers vynut. Pa, deliu parconal'd farvil'i movenf.}"
g = bytes_to_long(PBKDF2(pwd, salt, 1024 // 8))
g = pow(g, 2, p)

r.recvuntil('[=] ')
TER = int(r.recvline().strip(), 16)

r.sendline('%x' % g)
key = sha256(long_to_bytes(TER)).digest()

r.recvuntil('[=] ')
chal = decrypt(r.recvline(), key)
resp = sha256(chal).digest()
r.sendline(encrypt(resp, key))

r.recvuntil('[=] ')
secret = decrypt(r.recvline(), key)

print(secret)
