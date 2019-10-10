import subprocess
import json
import pickle
import crcmod.predefined as crcmod
import os
import hashlib
import libnum
from tqdm import trange
from Crypto.Cipher import AES, DES
from Crypto.Util.number import bytes_to_long, long_to_bytes


SZ = 75
prefix = b'QAQQAQQQ'
suffix = b'OAOOAOOO'
round = 10


def crcs(x):
    ret = {}
    for name in sorted(crcmod._crc_definitions_by_name):
        crc_name = crcmod._crc_definitions_by_name[name]['name']
        aname = crc_name.upper()
        crc = crcmod.PredefinedCrc(crc_name)
        crc.update(x)
        ret[aname] = crc.crcValue
    return ret


def xor(a, b):
    return {k: a[k] ^ b[k] for k in a.keys()}


print(f'[*] Generate bias')
zeros = crcs(b'\0' * (SZ + len(suffix)))

data = []
for i in trange(SZ * 8):
    x = (1 << i).to_bytes(SZ, 'little') + b'\0' * len(suffix)
    row = xor(crcs(x), zeros)
    data.append(row)


print(f'[*] Generate constants')
for _ in range(round):
    prefix = hashlib.sha256(prefix).digest()[:8]
zeros = crcs(prefix + b'\0' * SZ + suffix)


print(f'[*] Sanity check')
x = os.urandom(SZ)
target = crcs(prefix + x + suffix)
cur = zeros
x = int.from_bytes(x, 'little')
for i in range(SZ * 8):
    if (x >> i) & 1:
        cur = xor(cur, data[i])
assert cur == target


print(f'[*] Preprocess target hash')
with open('../task/hash.json') as f:
    target = json.load(f)
md5 = target['MD5']
target = {k: int(v.rstrip('L'), 16) for k, v in target.items() if v.startswith('0x')}

target = xor(target, zeros)
data.append(target)


print(f'[*] Build matrix')
keys = sorted(data[0].keys())
bits = [{k: bin(v)[2:] for k, v in d.items()} for d in data]
size = {k: max(len(d[k]) for d in bits) for k in keys}
bits = [list(map(int, ''.join(b[k].rjust(size[k], '0') for k in keys))) for b in bits]


print(f'[*] Output')
with open('data.pkl', 'wb') as f:
    data = {
        'md5': md5,
        'prefix': prefix,
        'suffix': suffix,
        'bits': bits,
    }
    pickle.dump(data, f, protocol=2)


print('[*] Solve CRC')
subprocess.check_call(['sage', 'solvecrc.sage'])


print('[*] Decrypt password')
p = int("""\
6816b2bba5ad70478c1beadb176b9ab17cb172841b10277f538f9d837f2\
2bdd807b970605c63859c739571cc535fd0c6879149b2d2eb676a182fd7\
5ff343e75a22ce75c36a775157c34f17\
""", 16)


with open('ctx', 'rb') as f:
    x = f.read()
x = x[8:-8]

keys = []
k = b'QAQQAQQQ'
for _ in range(10):
    k = hashlib.sha256(k).digest()[:8]
    keys.append(k)

for k in keys[::-1]:
    des = DES.new(k, DES.MODE_CFB, k)
    x = des.decrypt(x)

for _ in range(10):
    k = x[-16:]
    aes = AES.new(k, AES.MODE_CFB, k)
    x = k + aes.decrypt(x[:-16])

x = bytes_to_long(x)
x = pow(x, libnum.invmod(31337, p-1), p)
x = long_to_bytes(x)

assert hashlib.md5(x).hexdigest() == 'cd86c62d1c8d808a96e49511e0b79158'

print(x.hex())
