import sys
import os
import hashlib
import random


version = sys.version.replace('\n', ' ')
print(f'Python {version}')
random.seed(os.urandom(1337))


for i in range(0x1337):
    print(random.randrange(3133731337))


# Encrypt flag
sha512 = hashlib.sha512()
for _ in range(1000):
    rnd = random.getrandbits(32)
    sha512.update(str(rnd).encode('ascii'))

key = sha512.digest()

with open('../flag.txt', 'rb') as f:
    flag = f.read()

enc = bytes(a ^ b for a, b in zip(flag, key))
print('Encrypted:', enc.hex())
