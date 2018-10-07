from binascii import b2a_hex
from struct import unpack


def u64(s):
    return unpack('<Q', s[:8])[0]


with open('./validator', 'rb') as f:
    binary = f.read()

va = 0x400000
rawkeys = binary[0x553c60-va:][:0x58*11]

xorIdx = binary[0x542138-va:][:11]
hexIdx = b2a_hex(xorIdx).decode('ascii')
print(f'Select keys')
print(f'[ 0:11] ^  {hexIdx}')

print('')
print(f'Keys:')
keys = []
for i in range(11):
    raw = rawkeys[i * 0x58: (i+1) * 0x58]
    ints = [u64(raw[i:i+8]) for i in range(0, 0x58, 8)]
    (offInp, xorInp, lenInp, _,
     xorTgt, lenTgt, _,
     offOut, xorOut, lenOut, _,
     ) = ints
    assert(lenInp == lenTgt)
    xorInp = binary[xorInp-va:][:lenInp]
    xorTgt = binary[xorTgt-va:][:lenTgt]
    target = bytes(i ^ t for i, t in zip(xorInp, xorTgt))
    endInp = offInp + lenInp
    xorOut = binary[xorOut-va:][:lenOut]
    endOut = offOut + lenOut
    hexTgt = b2a_hex(target).decode('ascii')
    hexOut = b2a_hex(xorOut).decode('ascii')
    print(f'Index {i}')
    print(f'[{offInp:2d}:{endInp:2d}] == {hexTgt}')
    print(f'[{offOut:2d}:{endOut:2d}] ^= {hexOut}')
    target = (b'\0' * offInp + target).ljust(69, b'\0')
    xorOut = (b'\0' * offOut + xorOut).ljust(69, b'\0')
    keys.append([offInp, endInp, target, offOut, endOut, xorOut])
    print('')


idx = [a ^ b for a, b in zip(keys[0][2], xorIdx)]
# idx = [0, 2, 1, 10, 6, 3, 8, 4, 7, 5, 9]
inp = [None] * 69
xor = [0] * 69
for i in idx:
    offInp, endInp, target, offOut, endOut, xorOut = keys[i]
    for i, (a, b) in enumerate(zip(inp[offInp:endInp], target[offInp:endInp])):
        if a is None:
            inp[offInp+i] = b
        else:
            assert(a == b)
    for i, (a, b) in enumerate(zip(inp[offOut:endOut], xorOut[offOut:endOut])):
        if a is None:
            continue
        else:
            inp[offOut+i] ^= b
    xor = [a ^ b for a, b in zip(xor, xorOut)]
print((bytes(inp)+b'}').decode('ascii'))
