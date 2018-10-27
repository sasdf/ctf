import telnetlib
import gmpy2
from tqdm import tqdm, trange

r = telnetlib.Telnet('13.112.92.9', 21701)
# r = telnetlib.Telnet('127.0.0.1', 20974)
rline = lambda: r.read_until(b'\n')[:-1]


local = rline() == b'Local'
if local:
    realn = int(rline().decode('ascii'))
    rline()
encflag = rline()
print(f'[+] encrypted flag: {encflag}')

def hex(m):
    m = f'{m:x}'
    if len(m) & 1:
        m = '0' + m
    return m

def enc(m):
    r.write(b'A\n')
    r.write(f'{hex(m)}\n'.encode('ascii'))
    r.read_until(b'input: ')
    return int(rline().decode('ascii'), 16)

def dec(m):
    r.write(b'B\n')
    r.write(f'{hex(m)}\n'.encode('ascii'))
    r.read_until(b'input: ')
    return int(rline().decode('ascii'), 16)

def get_m_mod_n(m):
    return dec(enc(m))

# Recover N
last = None
n = 0
for i in trange(1023, 7, -1):
    res = get_m_mod_n((1 << i) + n)
    if res == 0:
        n |= (1 << i)
    else:
        last = res
    tqdm.write(f'res: {res}')
    tqdm.write(f'n: {n}')
    if local:
        tqdm.write(f'diff: {realn - n}')
n += 0x100 - last
tqdm.write(f'res: {res}')
tqdm.write(f'n: {n}')
if local:
    tqdm.write(f'diff: {realn - n}')
# n = realn

# Decrypt the flag
flag = int(input("Recovered flag: "), 16)
g = n + 1
nsquare = n * n
div = int(gmpy2.invert(256, n))
cur = int(encflag.decode('ascii'), 16)
if flag:
    cur *= pow(g, n - flag, nsquare)
    l = len(bin(flag)[2:])
    l += (8 - l % 8)
    cur = pow(cur, gmpy2.invert((1 << l), n), nsquare)
else:
    l = 0
for i in range(l // 8, l // 8 + 16):
    d = dec(cur)
    flag += d << (i*8)
    cur *= pow(g, n - d, nsquare)
    cur = pow(cur, div, nsquare)
    print(f'd: {hex(d)}')
    print(f'flag: {hex(flag)}')

