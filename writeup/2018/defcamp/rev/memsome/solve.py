import hashlib
import binascii
import codecs

with open('memsom', 'rb') as f:
    binary = f.read()

hshs = []
with open('list.txt') as f:
    for line in f:
        line = line.strip()
        if line.startswith('"'):
            hshs.append(line[1:-1].lower().encode('ascii'))
        else:
            off = int(line, 16)
            assert(binary[off+16] == 0)
            hshs.append(binascii.b2a_hex(binary[off:off+16]))


def hfunc(c):
    s = bytes([c])
    s = binascii.b2a_base64(s).replace(b'\n', b'')
    s = hashlib.md5(s).hexdigest().lower().encode('ascii')
    s = hashlib.md5(s).hexdigest().lower().encode('ascii')
    return s


mapping = {hfunc(c): chr(c) for c in range(128)}

ans = ''.join(mapping[h] for h in hshs)
print(codecs.decode(ans, 'rot13'))
