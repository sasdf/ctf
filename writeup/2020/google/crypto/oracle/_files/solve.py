import aegis
import base64
import secrets
import sys
import aes
import itertools
import re
from collections import defaultdict

from telnetlib import Telnet


def print_block(s, n=1):
    for i in range(0, len(s), 16*n):
        ss = [s[i+z*16:i+z*16+16].hex() for z in range(n)]
        print(f's_{i:04d}', *ss)
    print('')


def gen_diff(i, d, b=b'\0'*32*6, s=32):
    pt = b'\0' * i * s
    pt += bytes([d] * s)
    pt += b'\0' * 32*6
    pt = aes.xor_bytes(pt, b)
    return pt[:32*6]


def inv_diff(d1):
    d1 = aes.bytes2matrix(d1)
    aes.inv_mix_columns(d1)
    aes.inv_shift_rows(d1)
    d1 = aes.matrix2bytes(d1)
    return d1


def inv_state(d0, d1):
    d1 = aes.xor_bytes(d0, d1)
    d1 = aes.bytes2matrix(d1)
    aes.inv_mix_columns(d1)
    aes.inv_shift_rows(d1)
    aes.inv_sub_bytes(d1)
    d1 = aes.matrix2bytes(d1)
    return d1


mc_table = {}
for i in range(16):
    for c in range(1, 256):
        s = bytearray(16)
        s[i] = c
        s = aes.bytes2matrix(s)
        aes.shift_rows(s)
        aes.mix_columns(s)
        s = aes.matrix2bytes(s)
        for p in range(16):
            if s[p] != 0:
                assert (p, s[p]) not in mc_table
                mc_table[(i, p, s[p])] = c

sub_table = defaultdict(list)
for i in range(256):
    d = aes.sbox[i] ^ aes.sbox[i^1]
    sub_table[d].append(i)



remote = Telnet('oracle2.2020.ctfcompetition.com', 1337)

def solve_phase1():
    banner = remote.read_until(b'\n')
    iv = remote.read_until(b'\n')

    def enc(aad, pt):
        remote.write(base64.b64encode(pt).replace(b'\n', b'') + b'\n')
        remote.write(base64.b64encode(aad).replace(b'\n', b'') + b'\n')
        ct = base64.b64decode(remote.read_until(b'\n').strip())
        tag = base64.b64decode(remote.read_until(b'\n').strip())
        return ct

    def _recover_s(d1, d2):
        d1, d2 = inv_diff(d1), inv_diff(d2)
        res = []
        for y1, y2 in zip(d1, d2):
            for c in range(256):
                if (aes.sbox[c] ^ aes.sbox[c^1]) == y1 and (aes.sbox[c] ^ aes.sbox[c^2]) == y2:
                    res.append(c)
                    break
            else:
                raise ValueError('Not found')
        return bytes(res)

    def recover_s(i, base):
        ct1 = enc(b'', gen_diff(i, 1))
        ct2 = enc(b'', gen_diff(i, 2))
        d1 = aes.xor_bytes(ct1, base)
        d2 = aes.xor_bytes(ct2, base)
        off = (i + 2) * 32
        s0 = _recover_s(d1[off:off+16], d2[off:off+16])
        s4 = _recover_s(d1[off+16:off+32], d2[off+16:off+32])
        return s0, s4


    base = enc(b'', b'\0' * 32*6)
    print('0')
    s0, s4 = recover_s(0, base)
    print('1')
    s01, s41 = recover_s(1, base)
    s7, s3 = inv_state(s01, s0), inv_state(s41, s4)
    print('2')
    s02, s42 = recover_s(2, base)
    s71, s31 = inv_state(s02, s01), inv_state(s42, s41)
    s6, s2 = inv_state(s71, s7), inv_state(s31, s3)

    z = b'\0' * 16
    S = [s0, z, s2, s3, s4, z, s6, s7]
    m = aegis.Aegis128L.output_mask(S)
    m = aes.xor_bytes(m, base[32:])
    s1, s5 = S[1], S[5] = m[:16], m[16:]
    remote.write(base64.b64encode(b''.join(S)).replace(b'\n', b'') + b'\n')
    result = remote.read_until(b'\n').strip()
    assert result == b'OK'


def solve_phase2():
    banner = remote.read_until(b'\n').strip()
    iv = base64.b64decode(remote.read_until(b'\n').strip())
    aad = base64.b64decode(remote.read_until(b'\n').strip())
    ct = base64.b64decode(remote.read_until(b'\n').strip())
    tag = base64.b64decode(remote.read_until(b'\n').strip())

    ct = ct + b'\0' * 32*6
    cnt = 0
    def oracle(ct):
        nonlocal cnt
        cnt += 1
        remote.write(base64.b64encode(ct).replace(b'\n', b'') + b'\n')
        res = remote.read_until(b'\n').strip().decode()
        m = re.match(r"'ascii' codec can't decode byte (0x[0-9a-f]+) in position ([0-9]+): ordinal not in range", res)
        val, idx = [int(e, 0) for e in m.groups()]
        return idx, val

    def leak(i, ct):
        m = gen_diff(i, 0x80, b=ct, s=1)
        idx, val = oracle(m)
        assert idx == i, (i, idx, val)
        return val ^ 0x80


    mod_pos = [0, 3, 2, 1, 1, 0, 3, 2, 2, 1, 0, 3, 3, 2, 1, 0]
    mod_grp = [[0, 5, 10, 15], [4, 9, 14, 3], [8, 13, 2, 7], [12, 1, 6, 11]]

    def poke(b, base=b''):
        queue = [[] for _ in range(4)]
        for g, q in zip(mod_grp, queue):
            for i in g:
                q.append(('0mod', (i,), 1, None, 0))
            q.append(('0mod', tuple(g), 2, None, 0))
        base = {i: e for i, e in enumerate(base)}
        diff = {}
        while sum(map(len, queue)):
            msg = bytearray(ct)
            retry = False
            for gi, q in enumerate(queue):
                if len(q) == 0:
                    continue
                q = queue[gi] = sorted(q)
                cmd, i, d, k, m = q[0]
                if cmd == '0mod':
                    for ii in i:
                        msg[b*16+ii] ^= d
                    if k is not None:
                        msg[(b + 2)*16+k] ^= m
                elif cmd == '2base':
                    if k in base:
                        retry = True
                        q.pop(0)
                        break
                    msg[(b + 2)*16+k] ^= 0x80
                elif cmd == '9any':
                    cur_basis = [z for z in range(gi*4, gi*4+4) if z in base] + [gi*4]
                    q[0] = ('0mod', i, d, cur_basis[0], 0x80)
                    retry = True
                    break
                else:
                    raise KeyError('WTF1')
            if retry:
                continue
            idx, val = oracle(msg)
            idx -= (b + 2) * 16
            assert idx >= 0
            if idx < 16:
                gi = idx // 4
                cmd, i, d, k, m = queue[gi].pop(0)
                if m is not None:
                    val = val ^ m
                # print(cmd)
                if cmd == '2base':
                    base[k] = val
                elif cmd == '0mod':
                    diff[(i, d)] = (idx, val)
                    queue[gi].append(('2base', None, None, idx, 0x80))
                else:
                    raise KeyError('WTF2')
            else:
                # print('gg')
                gi = 4
            for q in queue[:gi]:
                if len(q) == 0:
                    continue
                cmd, i, d, k, m = q.pop(0)
                if cmd == '0mod':
                    assert k is None
                    q.append(('9any', i, d, k, m))
                else:
                    raise KeyError('WTF3')
        diff1 = {k[0][0]: v for k, v in diff.items() if k[1] == 1}
        diff2 = {k[0]: v for k, v in diff.items() if k[1] == 2}
        return base, diff1, diff2
        

    def recover_s(b, base=b''):
        base, diff1, diff2 = poke(b, base)

        diff0 = []
        for i in range(16):
            idx, val = diff1[i]
            val = val ^ base[idx]
            diff0.append(mc_table[(i, idx, val)])

        rec = [None] * 16
        for idxs, (idx, val) in diff2.items():
            ca = [sub_table[diff0[i]] for i in idxs]
            val = val ^ base[idx]
            found = 0
            for s in itertools.product(*ca):
                d1 = [aes.sbox[z] ^ aes.sbox[z^2] for z in s]
                d1 = aes.mix_single_column(d1)
                if d1[idx%4] == val:
                    for i, z in zip(idxs, s):
                        rec[i] = z
        return base, bytes(rec)

    print('cnt', cnt)
    print('p0')
    p0 = bytes(leak(i+0*16, ct) for i in range(16))
    print('p1')
    p1 = bytes(leak(i+1*16, ct) for i in range(16))
    print('p2')
    p2 = bytes(leak(i+2*16, ct) for i in range(16))
    print('p3')
    p3 = bytes(leak(i+3*16, ct) for i in range(16))

    print('s0')
    b0, w0 = recover_s(0, p2)
    s0 = w0
    # assert s0 == ans[0]

    print('s1')
    b1, w01 = recover_s(1, p3)
    # assert w01 == ans1[0]
    s01 = aes.xor_bytes(w01, p1)
    s4 = inv_state(s01, w0)
    # assert s4 == ans[4]

    print('s2')
    b2, w02 = recover_s(2)
    # assert w02 == ans2[0]
    s02 = aes.xor_bytes(w02, p2)
    s41 = inv_state(s02, w01)
    s3 = inv_state(s41, s4)
    # assert s3 == ans[3]

    print('s3')
    b3, w03 = recover_s(3)
    # assert w03 == ans3[0]
    s03 = aes.xor_bytes(w03, p3)
    s42 = inv_state(s03, w02)
    s31 = inv_state(s42, s41)
    s2 = inv_state(s31, s3)
    # assert s2 == ans[2]

    z = b'\0' * 16
    S = [s0, z, s2, s3, s4]
    m = aegis.Aegis128.output_mask(S)
    m = aes.xor_bytes(m, p1)
    m = aes.xor_bytes(m, ct[1*16:2*16])
    s1 = S[1] = m
    # assert s1 == ans[1]
    print('cnt', cnt)


    DATA = b"""
Hear your fate, O dwellers in Sparta of the wide spaces;

Either your famed, great town must be sacked by Perseus' sons,
Or, if that be not, the whole land of Lacedaemon
Shall mourn the death of a king of the house of Heracles,
For not the strength of lions or of bulls shall hold him,
Strength against strength; for he has the power of Zeus,
And will not be checked until one of these two he has consumed
"""
    ad = aad + p0

    cipher = aegis.Aegis128(b'\0'*16)
    SS, ct = cipher.raw_encrypt(S, DATA)
    tag = cipher.finalize(SS, len(ad) * 8, len(DATA) * 8)

    remote.write(b'challenge\n')
    remote.write(base64.b64encode(ct).replace(b'\n', b'') + b'\n')
    remote.write(base64.b64encode(ad).replace(b'\n', b'') + b'\n')
    remote.write(base64.b64encode(tag).replace(b'\n', b'') + b'\n')

solve_phase1()
solve_phase2()
print(remote.read_all())
