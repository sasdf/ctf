import sha256
import struct
from telnetlib import Telnet


remote = Telnet('sharky.2020.ctfcompetition.com', 1337)
remote.read_until(b'MSG Digest: ')
target = bytes.fromhex(remote.read_until(b'\n').strip().decode())

# Processing input blocks
input = b'Encoded with random keys'

sha2 = sha256.SHA256()
state = struct.unpack('>8L', target)

block = sha2.padding(input)
assert len(block) == 64
w = sha2.compute_w(block)

# Undo last 56 rounds with known round constants
state = [(x - y) & 0xffffffff for x, y in zip(state, sha2.h)]
for k in range(63, 7, -1):
    state = sha2.decompression_step(state, sha2.k[k], w[k])

# Recover secret round constants
rk = [0] * 8
for k in range(7, -1, -1):
    # Make the error propagate to first round
    state2 = state[:]
    for i in range(k, -1, -1):
        state2 = sha2.decompression_step(state2, 0, w[i])

    # Reveal the secret
    p = 7 - k
    key = (state2[p] - sha2.h[p]) & 0xffffffff
    rk[k] = key

    # Undo the last round with the secret we found
    state = sha2.decompression_step(state, key, w[k])

# Gimme flag
remote.write(','.join(map(hex, rk)).encode() + b'\n')
print(remote.read_all())
