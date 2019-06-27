from tqdm import tqdm
from telnetlib import Telnet
import multiprocessing as mp


def worker(_):
    xs = []
    ys = []
    r = Telnet('reality.ctfcompetition.com', 1337)
    r.read_until(b'coefficients')
    for _ in range(3):
        r.read_until(b': ')
        c = r.read_until(b'\n').decode()
        x, y = c.split(', ')
        xs.append(x)
        ys.append(y)
    r.close()
    return xs, ys


xs = []
ys = []
pool = mp.Pool(16)
bar = tqdm(pool.imap_unordered(worker, range(100)), total=100, smoothing=0)
try:
    for x, y in bar:
        xs.extend(x)
        ys.extend(y)
finally:
    bar.close()
    pool.terminate()
    pool.join()
