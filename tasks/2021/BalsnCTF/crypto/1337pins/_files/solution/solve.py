import random
from tqdm import tqdm, trange
from telnetlib import Telnet

from mt import MT19937, tobin, untamper, tamper


# conn = Telnet('127.0.0.1', 27491)
conn = Telnet('3.239.213.227', 27491)

mt = MT19937()

remain = None
bar = trange(40)
for i in bar:
    conn.write(b'10\n'*500)
    for _ in range(500):
        s = int(conn.read_until(b'\n').decode())
        s = s & 1
        for b in tobin(s)[:1] + [None] * 31:
            remain = mt.add(b)
        bar.desc = f'[o] Reconstruct - {remain} remain'
    if remain == 0:
        rec = mt.reconstruct('python')
        break
bar.close()

bar = trange(1337)
for i in range(0, 1337, 100):
    n = min(1337 - i, 100)
    m = ''.join(f'{rec.getrandbits(32) % 10}\n' for _ in range(n))
    conn.write(m.encode())
    for _ in range(n):
        res = conn.read_until(b'\n').decode().strip()
        assert res == '.', res
    bar.update(n)

conn.interact()
