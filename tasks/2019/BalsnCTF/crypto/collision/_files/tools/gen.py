import hashlib
import subprocess
import json
import os
from Crypto.Cipher import AES, DES
from Crypto.Util.number import bytes_to_long, long_to_bytes


p = int("""\
6816b2bba5ad70478c1beadb176b9ab17cb172841b10277f538f9d837f2\
2bdd807b970605c63859c739571cc535fd0c6879149b2d2eb676a182fd7\
5ff343e75a22ce75c36a775157c34f17\
""", 16)


def omnihash(x):
    ret = subprocess.check_output(['omnihash', '-jcs'], input=x)
    return json.loads(ret)[0][0]


def gen(x):
    # Destroy the value
    x = bytes_to_long(x)
    x = pow(x, 31337, p)
    x = long_to_bytes(x)
    
    # Destroy again
    for _ in range(10):
        k = x[:16]
        aes = AES.new(k, AES.MODE_CFB, k)
        x = aes.encrypt(x[16:]) + k

    # Destroy one more time
    x = b'QAQQAQQQ' + x
    for _ in range(10):
        k = hashlib.sha256(x[:8]).digest()[:8]
        des = DES.new(k, DES.MODE_CFB, k)
        x = k + des.encrypt(x[8:])

    # Check
    x = x + b'OAOOAOOO'
    hash = omnihash(x)
    return hash


if __name__ == '__main__':
    x = os.urandom(64)
    print(f'md5: {hashlib.md5(x).hexdigest()}')
    print(f'sha1: {hashlib.sha1(x).hexdigest()}')
    print(f'sha3_224: {hashlib.sha3_224(x).hexdigest()}')
    with open('hash.json', 'w') as f:
        json.dump(gen(x), f, indent=4)
