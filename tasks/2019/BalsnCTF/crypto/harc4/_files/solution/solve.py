import random
from tqdm import trange
from Crypto.Cipher import ARC4
import os
import ast


def KSA(key):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    return S


def dfsSuffix(i, j, S, slot, val, suffix):
    """ Search for a suffix which won't destroy the state """
    off = 256 - len(suffix) + i
    if off == 256:
        return True
    k = suffix[i]
    for v in val:
        assert S[off] == -1
        p = (j + v + k) % 256
        if p not in slot:
            continue
        S[off] = v
        if dfsSuffix(i + 1, p, S, slot | {off}, val - {v}, suffix):
            return True
        S[off] = -1
    

def getFreeVal(target):
    """ Get values that can be pushed to suffix part """
    S = list(range(256))
    j = 0
    ret = []
    for i in range(256):
        if target[i] is not None and target[i] != -1:
            p = S.index(target[i])
        elif S[i] in target:
            p = target.index(S[i])
        elif target[i] is None:
            p = i
            ret.append(S[i])
        elif target[i] == -1:
            p = i
        else:
            raise NotImplementedError('WTF')
        j = p
        S[i], S[j] = S[j], S[i]
    return ret


def forgeKSA(target, suffix):
    # Search for a vaild suffix
    target = target[:]
    slot = set(s for s, v in enumerate(target) if v is None)
    val = set(getFreeVal(target))
    assert len(val) >= len(suffix)
    found = False
    # Iterate through possible initial values of j
    for s in slot:
        if dfsSuffix(0, s, target, slot | {255 - len(suffix)}, val, suffix):
            found = True
            break
    assert found

    # Generate key with greedy swap
    S = list(range(256))
    j = 0
    key = []
    for i in range(256 - len(suffix)):
        if target[i] is not None and target[i] != -1:
            p = S.index(target[i])
        elif target[i] == -1:
            # Start of suffix
            assert S[i] not in target
            p = s
        elif S[i] in target:
            p = target.index(S[i])
        elif target[i] is None:
            p = i
        else:
            raise NotImplementedError('WTF')
        key.append((p - j - S[i]) % 256)
        j = p
        S[i], S[j] = S[j], S[i]
    return bytes(key) + bytes(suffix)


def PRGA(S, n):
    i = 0
    j = 0
    ret = []
    for _ in range(n):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        ret.append(S[(S[i] + S[j]) % 256])
    return ret


def fillj(i, j, ti, il, S0, S, target):
    for iv in il:
        jv = (ti - iv) % 256
        if iv in S or jv in S or iv == jv:
            continue
        p = (iv + j) % 256
        if S[p] is not None:
            continue
        assert S[i] is -1
        assert S[p] is None
        assert S0[i] is -1
        assert S0[p] is None
        S0[i], S0[p], S[i], S[p] = iv, jv, jv, iv
        if fillidx(i, p, S0, S, target):
            return True
        S0[i], S0[p], S[i], S[p] = -1, None, -1, None
    return False


def fillidx(i, j, S0, S, target):
    if i == len(target):
        return True
    t = target[i]
    i += 1
    assert S[i] == S0[i] == -1
    slot = [s for s, v in enumerate(S) if v is None]
    il = [(p - j) % 256 for p in slot]
    if t in S:
        ti = S.index(t)
        return fillj(i, j, ti, il, S0, S, target)
    else:
        for ti in slot:
            assert S0[ti] is None
            assert S[ti] is None
            S0[ti], S[ti] = t, t
            if fillj(i, j, ti, il, S0, S, target):
                return True
            S0[ti], S[ti] = None, None
        return False


def forgePRGA(target, suffixSZ):
    """
    x i i i i i x x x x x x p s s s s s s
    """
    sz = len(target)
    S = [-1 if 1 <= i <= sz or i >= 255 - suffixSZ else None for i in range(256)]
    S0 = S[:]
    if fillidx(0, 0, S0, S, target):
        return S0
    else:
        raise FileNotFoundError('QAQ')


if __name__ == '__main__':
    from telnetlib import Telnet
    # r = Telnet('localhost', 5450)
    r = Telnet('3.226.122.181', 5450)

    r.read_until(b'> ')
    r.write(b'register\n')
    r.write(b'aa\n')
    r.write(b'\n')

    r.read_until(b'> ')
    r.write(b'_debug\n')
    db = ast.literal_eval(r.read_until(b'\n').decode())
    IV = bytes.fromhex(db['aa'])
    admin = bytes.fromhex(db['admin'])
    target = bytes(a ^ b for a, b in zip(IV, admin))

    S = forgePRGA(target, 32)
    key = forgeKSA(S, IV)
    assert len(key) <= 256
    assert key.endswith(IV)
    cipher = ARC4.new(key)
    result = cipher.encrypt(IV)
    assert result == admin
    
    key = key[:-len(IV)]

    r.write(b'login\n')
    r.write(b'admin\n')
    r.write(key.hex().encode())
    r.write(b'\n')
    r.interact()
