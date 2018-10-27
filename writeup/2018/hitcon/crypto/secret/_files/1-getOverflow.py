import telnetlib
import codecs
import gmpy2
import pickle
from tqdm import tqdm, trange

# r = telnetlib.Telnet('52.194.203.194', 21700)
r = telnetlib.Telnet('127.0.0.1', 20974)
rline = lambda: r.read_until(b'\n')[:-1]
tohex = lambda x: codecs.encode(x, 'hex')
fromhex = lambda x: codecs.decode(x, 'hex')
xor = lambda a, b: bytes(ai ^ bi for ai, bi in zip(a, b))

def rawenc(s):
    r.write(b'1\n') # Add note
    r.write(b'3\n') # index
    r.write(b'1\n') # Type
    r.write(f'{len(s)}\n'.encode('ascii')) # size
    r.write(s)
    r.write(b'2\n') # Show note
    r.write(b'3\n') # index
    r.read_until(b'index:')
    r.read_until(b'index:')
    res = None
    try:
        l = rline()
        res = codecs.decode(l, 'hex')
    except:
        print(l)
        raise
    r.write(b'3\n') # Remove note
    r.write(b'3\n') # index
    r.read_until(b'index:')
    return res

enciv = rawenc(b'\0' * 17)[:16]

def enc(s):
    s = b'\0' * 16 + xor(enciv, s[:16]) + s[16:]
    return rawenc(s)[16:]

i = 1
arr = []
with open('o.local.pkl', 'rb') as f:
    arr = pickle.load(f)
for i in trange(len(arr), 300):
    plain = i.to_bytes(16, 'big')
    plain += b'\x10' * 16 + b'\x10'
    overflow = enc(plain)[:32][-4:]
    arr.append(tohex(overflow).decode('ascii'))
    with open('o.local.pkl', 'wb') as f:
        pickle.dump(arr, f)
# for i in trange(0, 300, desc='checking'):
    # plain = i.to_bytes(16, 'big')
    # plain += b'\x10' * 16 + b'\x10'
    # overflow = enc(plain)[:32][-4:]
    # assert(arr[i] == tohex(overflow).decode('ascii'))
print(arr)
# r.interact()
