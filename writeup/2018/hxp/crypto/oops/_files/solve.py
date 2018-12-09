from firstblood.all import uio
from Crypto.Cipher import AES


cnt = 10000
def conn():
    global r, rawenc, flagenc, off1, off2, cnt, key
    # r = uio.spawn('python3 -u vuln.py')
    r = uio.tcp('195.201.131.58', 3250)
    flagenc = r.line().hexd
    # key = r.line().hexd


def half_times(n):
    src = list(n)
    dst = src[:]
    carry = src[-1] & 1
    src[-1] ^= (carry * 0x87)
    for i in range(len(src) - 1, 0, -1):
        dst[i] = ((src[i] >> 1) | ((src[i-1] & 1) << 7)) & 0xff
    dst[0] = ((dst[0] >> 1) | (carry << 7)) & 0xff
    return bytes(dst)


def two_times(n):
    src = list(n)
    dst = src[:]
    carry = src[0] >> 7
    assert(carry <= 1)
    for i in range(len(src) - 1):
        dst[i] = ((src[i] << 1) | (src[i+1] >> 7)) & 0xff
    dst[-1] = ((src[-1] << 1) ^ (carry * 0x87)) & 0xff
    return bytes(dst)


def three_times(n):
    t = two_times(n)
    return t.xor(n)


def renc(nonce, plain):
    global cnt
    cnt += 1
    res = r.line(f'enc {nonce.hexe} {plain.hexe}').line()
    cipher, tag = res[2:].split(' ')
    return cipher.hexd, tag.hexd


def rdec(nonce, cipher, tag):
    global cnt
    cnt += 1
    res = r.line(f'dec {nonce.hexe} {cipher.hexe} {tag.hexe}').line()
    plain = res[2:]
    return plain.hexd


def dbgenc(p):
    return AES.new(key, AES.MODE_ECB).encrypt(p)


conn()

N = b'\0' * 16
M1 = b'\0' * 15 + b'\x80'
M2 = b'\0' * 16

C, T = renc(N, M1+M2)
C1, C2 = C.chunk(16)
Cp = C1.xor(M1)
Tp = M2.xor(C2)

Mp = rdec(N, Cp, Tp)
L2 = Mp.xor(M1)

print(f'[*] Got First CP pair')

N = L2.xor(M1)
L = L2.xor(C1)
M = b'\0' * 64
C, T = renc(N, M)
C1, C2, C3, _ = C.chunk(16)
P1 = two_times(L)
P2 = two_times(P1)
P3 = two_times(P2)
C1 = C1.xor(P1)
C2 = C2.xor(P2)
C3 = C3.xor(P3)

print(f'[*] Got More CP pairs')

# assert(dbgenc(P1) == C1)
# assert(dbgenc(P2) == C2)
# assert(dbgenc(P3) == C3)

flagenc = flagenc.chunk(16).list
nblocks = len(flagenc) * 2
L = C2
csum = b'\0' * 16
for _ in range(nblocks):
    L = two_times(L)
    csum = csum.xor(L)
L = two_times(L)
last = L.xor(M1)

L = three_times(L)
csum = csum.xor(L)

L = C1
M = b''
L = two_times(L)
M += L.xor(last)
L = two_times(L)
M += L.xor(csum)
M += b'\0' * 16
C, T = renc(P1, M)
Clast, Ccsum, _ = C.chunk(16)
L = C1
L = two_times(L)
Clast = L.xor(Clast)
L = two_times(L)
Ccsum = L.xor(Ccsum)

print(f'[*] Got last and checksum')
# assert(dbgenc(last) == Clast)
# assert(dbgenc(csum) == Ccsum)

L = C2
C = b''
for e in flagenc:
    L = two_times(L)
    C += e.xor(L)
    L = two_times(L)
    C += e.xor(L)

C += Clast
Ps = rdec(P2, C, Ccsum).chunk(16).list

L = C2
P = b''
for e, _ in Ps[:-1].chunk(2):
    L = two_times(L)
    P += e.xor(L)
    L = two_times(L)

print(P)
