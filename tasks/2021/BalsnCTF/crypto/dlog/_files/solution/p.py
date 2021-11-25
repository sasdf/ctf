import gmpy2
import requests
import random
import time
import sys
import numpy as np
import re
from tqdm import tqdm, trange
from telnetlib import Telnet


sess = requests.Session()

ip = '34.237.222.98'
ip = 'dlog2.balsnctf.com'

def get_oracle(x):
    res = sess.get(f'http://{ip}:27492/oracle', params={'x': x})
    return int(res.text)

def get_metrics():
    res = sess.get(f'http://{ip}:27492/metrics')
    res = res.text
    count = int(float(re.search(r'flag_processing_seconds_count (.*)', res).group(1)))
    value = float(re.search(r'flag_processing_seconds_sum (.*)', res).group(1))
    return count, value

def get_flag(x):
    res = sess.get(f'http://{ip}:27492/flag', params={'x': x})
    return res.text

"""
# Using requests
def get_time(x):
    sn, en = 0, 10000
    while en - sn > 3:
        sn, sv = get_metrics()
        get_flag(x)
        en, ev = get_metrics()
    assert en > sn
    return int((ev - sv) / (en - sn) * 1e9)


"""

conn = Telnet(ip, 27492)
"""
# Using socket
def _get_time(x):
    conn.write(f'''\
GET /metrics HTTP/1.1

GET /flag?x={x} HTTP/1.1

GET /metrics HTTP/1.1

'''.replace('\n', '\r\n').encode())
    conn.read_until(b'flag_processing_seconds_count ')
    sn = int(float(conn.read_until(b'\n').decode()))
    conn.read_until(b'flag_processing_seconds_sum ')
    sv = float(conn.read_until(b'\n').decode())
    conn.read_until(b'flag_processing_seconds_count ')
    en = int(float(conn.read_until(b'\n').decode()))
    conn.read_until(b'flag_processing_seconds_sum ')
    ev = float(conn.read_until(b'\n').decode())
    return sn, sv, en, ev

def get_time(x):
    sn, sv, en, ev = _get_time(x)
    while en - sn > 1:
        sn, sv, en, ev = _get_time(x)
    assert en > sn
    return int((ev - sv) / (en - sn) * 1e9)
"""

# Using pipelined socket
def _get_time(xs):
    msg = [f'''\
GET /metrics HTTP/1.1

''']
    for x in xs:
        msg.append(f'''\
GET /flag?x={x} HTTP/1.1

GET /metrics HTTP/1.1

''')
    conn.write(''.join(msg).replace('\n', '\r\n').encode())
    ys = []
    for _ in range(len(xs)+1):
        conn.read_until(b'flag_processing_seconds_count ')
        sn = int(float(conn.read_until(b'\n').decode()))
        conn.read_until(b'flag_processing_seconds_sum ')
        sv = float(conn.read_until(b'\n').decode())
        ys.append((sn, sv))
    return ys

def get_time(xs):
    ret, ys = [], _get_time(xs)
    for (sn, sv), (en, ev) in zip(ys, ys[1:]):
        assert en > sn
        ret.append(int((ev - sv) / (en - sn) * 1e9))
    return ret


# Recover p
p = None
two = get_oracle(2)
a, b = get_oracle(2), 2
for i in range(6):
    b *= 2
    c = get_oracle(b)
    d = a * two - c
    if p is None: p = d
    else: p = gmpy2.gcd(d, p)
    a = c
p = int(p)
assert gmpy2.is_prime(p)
print('p =', p)


# Recover s
def gen_pair(s):
    while m := random.randrange(1 << 20):
        if pow(m, (p-1) // 2, p) == 1:
            break
    ss, mm = s, m
    while (ss & 1) == 0:
        mm = pow(mm, (p + 1) // 4, p)
        ss = ss // 2
    m0 = pow(mm, pow(ss, -1, p-1), p)
    assert pow(m0, s, p) == m
    m1 = pow(m, pow(s+1, -1, p-1), p)
    return m0, m1


def leak(s):
    res = [[], []]

    s = s << 1
    ms = [e for p in range(4) for e in gen_pair(s)]

    # Collect measurements
    chunk_size = 3
    chunk_num = 20
    xs = []
    for i in range(int(2 * chunk_size * chunk_num * 3)):
        m = ms[i % len(ms)]
        xs.append(m)
    ys = get_time(xs[:len(xs)//2]) + get_time(xs[len(xs)//2:])
    for i, t in enumerate(ys):
        res[i % 2].append(t)
    res = np.array(res).reshape(2, -1)

    # Filter extreme values
    mask = np.sum([
        *(res < np.percentile(res, 25, axis=-1, keepdims=True)),
        *(res > np.percentile(res, 75, axis=-1, keepdims=True)),
    ], 0) == 0

    # Filter in time domain
    _res = []
    for row in res:
        row = row[mask]
        out = []
        for i in range(0, len(row), chunk_size):
            out.append(np.median(row[i:i+chunk_size]))
        _res.append(out)

    res = np.array(_res)
    obs = (res[0] > res[1]).astype(int)
    print(f'[+] t0: mid={np.median(res[0]):.2f}, std={res[0].std():.2f}')
    print(f'[+] t1: mid={np.median(res[1]):.2f}, std={res[1].std():.2f}')
    print(f'[+] bit: {obs.mean():.2f} ({len(obs):2d}) - {"".join(map(str, obs))}')
    return obs.mean()


s = 0b1
s = 0b101
s = 0b10111000101001100100011010011010110111111001011101101111000110010000001001010000111010
s = 0b101110001010011
# s = 0b10111000010001
o = 0b1011100010100110010001101001101011011111100101110110111100011001000000100101000011101011101101001111
# o = 912443792780746885007752625963

# ans = o
# print(get_flag(pow(1337, pow(ans, -1, p-1), p)))

bad = ' ' * (s.bit_length() + 2)
for idx in range(100):
    score = 0.5
    scores = []
    print('='*10, idx, '='*10)
    while not (score <= 0.25 or score >= 0.75):
        score = leak(s)
        scores.append(score)
    bit = int(score > 0.5)
    s = (s << 1) | bit
    overall = np.mean(scores)

    if (len(scores) >= 8) or (score > 0.5 and overall < 0.6) or (score < 0.5 and overall > 0.4):
        print('[!] Looks bad, you may need to modify the result manually')
        bad += 'X'
    else:
        bad += '.'

    print(f'[+] Overall: {overall:.2f}')
    print(f'[+] Bad:     {bad}')
    print(f'[+] Current: {bin(s)}')
    print(f'[+] Debug  : {bin(o)}')

    bf = 10
    for guess in range(1<<bf):
        if pow(2, (s<<bf)+guess, p) == two:
            ans = (s<<bf)+guess
            print('!! Found !!')
            print(ans)
            print(ans == o)
            print(get_flag(pow(1337, pow(ans, -1, p-1), p)))

            exit(0)
