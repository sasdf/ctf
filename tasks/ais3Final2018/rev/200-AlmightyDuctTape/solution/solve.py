#!/usr/bin/python3
from struct import pack, unpack


with open('../task/task', 'rb') as f:
    data = f.read()
target = unpack('<' + 'I' * 8, data[0x60a0:][:32])
sbox = unpack('<' + 'B' * 256, data[0x60c0:][:256])
sbox = {e: i for i, e in enumerate(sbox)}
keys = unpack('<' + 'I' * 8, data[0x6080:][:32])


def sub(v):
    v = pack('<I', v)
    v = bytes(sbox[c] for c in v)
    v = unpack('<I', v)[0]
    return v


def decryptTEA(v3, v4):
    v5 = keys[7] * 32
    for _ in range(32):
        v4 -= (v3 + v5) ^ ((v3 << 4) + keys[5]) ^ ((v3 >> 5) + keys[6])
        v4 &= 0xffffffff
        v3 -= (v4 + v5) ^ ((v4 << 4) + keys[3]) ^ ((v4 >> 5) + keys[4])
        v3 &= 0xffffffff
        v5 -= keys[7]
        v5 &= 0xffffffff
    return v3, v4


def decrypt(target):
    target = list(target[:])
    for i in range(64 * 8 - 2, 0, -2):
        i %= 8
        l, r = sub(target[i]), sub(target[i+1])
        l, r = decryptTEA(l, r)
        l ^= target[(i - 2) % 8]
        r ^= target[(i - 1) % 8]
        target[i], target[i+1] = l, r
    l, r = sub(target[0]), sub(target[1])
    l, r = decryptTEA(l, r)
    l ^= keys[1]
    r ^= keys[2]
    target[0], target[1] = l, r
    return target


def perturb(target):
    result = []
    for i, e in enumerate(target):
        e = (((e >> 5) | (e << 3)) ^ (keys[0] ^ i)) & 0xff
        result.append(e)
    return result


target = decrypt(target)
target = list(pack('<' + 'I' * 8, *target))
target = perturb(target)
print(bytes(target))
