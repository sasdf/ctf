import subprocess
import struct
import multiprocessing as mp


def run(s):
    """ Get encrypted result """
    prog = subprocess.run(
        ['./ld-linux-x86-64.so.2', '--library-path', '.', './chains'],
        input=s, check=True, stdout=subprocess.PIPE)
    return struct.unpack('<32H', prog.stdout[-64:])

# Input permutation table
idx = range(0, 32, 8)
idx = [i + k for i in range(8) for k in idx]

# Target extracted from `target.py`
target = [
    0x46ca, 0x4187, 0x5582, 0x5e51, 0x56e1, 0x56e1, 0x56e1, 0x6666,
    0x3674, 0x367a, 0x3668, 0x3670, 0x3670, 0x366e, 0x3645, 0x29c1,
    0x15aa, 0x158b, 0x1599, 0x15b9, 0x15b4, 0x15b8, 0x15cd, 0x15cd,
    0x410d, 0x4114, 0x4109, 0x4135, 0x4136, 0x4109, 0x409b, 0x409b,
]

def handle(args):
    """ Bruteforce the target byte """
    i, k = args
    for c in range(32, 128):
        print(f'Try {i} = {c}')
        r = run(b'a' * i + bytes([c]) + b'a' * (31 - i))
        if r[k] == target[k]:
            return c

# Distribute each byte to different worker
flag = ''
pool = mp.Pool(32)
for c in pool.imap(handle, enumerate(idx)):
    if c is not None:
        flag += chr(c)
        print(flag)
