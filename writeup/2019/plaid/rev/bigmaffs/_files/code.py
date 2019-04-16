# coding: utf-8
import copy

one = {'size': 1, 'data': [1]}
zero = {'size': 1, 'data': [0]}
record = []
value = []
wanted = []

p = 87582797363973712706510077042909217030082081478550617

mapping = [
   0,    1,   -2,   -1,    4,    5,    2,    3,   -8,   -7,  -10,   -9,   -4,   -3,   -6,   -5,
  16,   17,   14,   15,   20,   21,   18,   19,    8,    9,    6,    7,   12,   13,   10,   11,
 -32,  -31,  -34,  -33,  -28,  -27,  -30,  -29,  -40,  -39,  -42,  -41,  -36,  -35,  -38,  -37,
 -16,  -15,  -18,  -17,  -12,  -11,  -14,  -13,  -24,  -23,  -26,  -25,  -20,  -19,  -22,  -21,
  64,   65,   62,   63,   68,   69,   66,   67,   56,   57,   54,   55,   60,   61,   58,   59,
  80,   81,   78,   79,   84,   85,   82,   83,   72,   73,   70,   71,   76,   77,   74,   75,
  32,   33,   30,   31,   36,   37,   34,   35,   24,   25,   22,   23,   28,   29,   26,   27,
  48,   49,   46,   47,   52,   53,   50,   51,   40,   41,   38,   39,   44,   45,   42,   43,
-128, -127, -130, -129, -124, -123, -126, -125, -136, -135, -138, -137, -132, -131, -134, -133,
-112, -111, -114, -113, -108, -107, -110, -109, -120, -119, -122, -121, -116, -115, -118, -117,
-160, -159, -162, -161, -156, -155, -158, -157, -168, -167, -170, -169, -164, -163, -166, -165,
-144, -143, -146, -145, -140, -139, -142, -141, -152, -151, -154, -153, -148, -147, -150, -149,
 -64,  -63,  -66,  -65,  -60,  -59,  -62,  -61,  -72,  -71,  -74,  -73,  -68,  -67,  -70,  -69,
 -48,  -47,  -50,  -49,  -44,  -43,  -46,  -45,  -56,  -55,  -58,  -57,  -52,  -51,  -54,  -53,
 -96,  -95,  -98,  -97,  -92,  -91,  -94,  -93, -104, -103, -106, -105, -100,  -99, -102, -101,
 -80,  -79,  -82,  -81,  -76,  -75,  -78,  -77,  -88,  -87,  -90,  -89,  -84,  -83,  -86,  -85,
]

M = [
0xA9, 0x65, 0x9A, 0x89, 0x3D, 0xEA, 0xF4, 0x44, 0x3A, 0x84, 0x77, 0x75, 0x13, 0x13, 0x66, 0x95, 0x7F, 0x51, 0x32, 0x95, 0x6B, 0x3E, 0x01
]
M = {'size': len(M), 'data': M}

flag = [
0x05, 0xBB, 0x01, 0x59, 0x6F, 0x06, 0x18, 0x61, 0x3D, 0xA0, 0x3A, 0xE4, 0x9C, 0xE4, 0xE1, 0xE6, 0x73, 0x93, 0x81, 0xF2, 0x10, 0x6B, 0x02
]


def toInt(a):
    res = 0
    for i in a['data'][::-1]:
        res = res * 256 + mapping[i]
    return res


def _fromInt(e, size):
    c = e >> (size * 8)
    ee = e - (c << (size * 8))
    if ee > 0:
        M = 0
        for i in range(size):
            M = M * 256 + 85
        if M < ee:
            c += 1
            ee -= 1 << (size * 8)
    else:
        M = 0
        for i in range(size):
            M = M * 256 -170
        if M > ee:
            c -= 1
            ee += 1 << (size * 8)
    if size == 0:
        return [c]
    else:
        return _fromInt(ee, size - 1) + [c]


def fromInt(e):
    ret = _fromInt(e, (e.bit_length()+7) // 8)
    return [mapping.index(i) for i in ret]


def check(a):
    for n in a['data'][::-1]:
        if n:
            return (n & 0xAA) > (n & 0x55)
    return 0


def wtf(a, b):
    while not check(a):
        sub(a, b)
    add(a, b)


def add(a, b):
    v2 = 0
    mod_2 = [0, 1, 0, 1, 0, 1]
    unk_407E = [1, 1, 0, 0, -1, -1]
    for i in range(b['size']):
        v3 = 0
        if i == a['size']:
            a['data'].append(0)
            a['size'] += 1
        for j in range(8):
            idx = ((a['data'][i] >> j) & 1) + v2 + ((b['data'][i] >> j) & 1)
            v3 |= mod_2[idx + 2] << j
            v2 = unk_407E[idx + 2]
        a['data'][i] = v3
    i = b['size']
    while (v2):
        v3 = 0
        if i >= a['size']:
            a['data'].append(0)
            a['size'] += 1
        for k in range(8):
            idx = ((a['data'][i] >> k) & 1) + v2
            v3 |= mod_2[idx + 2] << k
            v2 = unk_407E[idx + 2]
        a['data'][i] = v3
        i += 1


def sub(a, b):
    v2 = 0
    mod_2 = [0, 1, 0, 1, 0, 1]
    unk_407E = [1, 1, 0, 0, -1, -1]
    for i in range(b['size']):
        v3 = 0
        if i == a['size']:
            a['data'].append(0)
            a['size'] += 1
        for j in range(8):
            idx = ((a['data'][i] >> j) & 1) + v2 - ((b['data'][i] >> j) & 1)
            v3 |= mod_2[idx + 2] << j
            v2 = unk_407E[idx + 2]
        a['data'][i] = v3
    i = b['size']
    while (v2):
        v3 = 0
        if i >= len(a['data']):
            a['data'].append(0)
            a['size'] += 1
        for k in range(8):
            idx = ((a['data'][i] >> k) & 1) + v2
            v3 |= mod_2[idx + 2] << k
            v2 = unk_407E[idx + 2]
        a['data'][i] = v3
        i += 1


def do_math(a1, a2):
    """
    a1 == 0: a2 + 1
    a2 == 0: F(a1 - 1, 1)
    F(a1 - 1, F(a1, a2 - 1))

    a1 == 1: F(1, a2 - 1) + 1
    """
    global record
    global value
    if sum(a1['data']) == 0:
        v2 = copy.deepcopy(zero)
        add(v2, a2)
        add(v2, one)
        return v2
    elif sum(a2['data']) == 0:
        v4 = copy.deepcopy(zero)
        add(v4, a1)
        sub(v4, one)
        return value[record.index((v4, one))]
    else:
        v5 = copy.deepcopy(zero)
        add(v5, a2)
        sub(v5, one)
        v6 = value[record.index((a1, v5))]
        v7 = copy.deepcopy(zero)
        add(v7, a1)
        sub(v7, one)
        return value[record.index((v7, v6))]


def do_math2(a1, a2):
    global record
    global value
    global wanted
    if sum(a1['data']) == 0:
        v2 = copy.deepcopy(zero)
        add(v2, a2)
        add(v2, one)
        return v2
    elif sum(a2['data']) == 0:
        v4 = copy.deepcopy(zero)
        add(v4, a1)
        sub(v4, one)
        if (v4, one) in record:
            return value[record.index((v4, one))]
        else:
            if (v4, one) not in wanted:
                wanted.append((v4, one))
            value.append(do_math2(v4, one))
            record.append((v4, one))
            wanted.remove((v4, one))
            return value[-1]
    else:
        v5 = copy.deepcopy(zero)
        add(v5, a2)
        sub(v5, one)
        if (a1, v5) in record:
            v6 = value[record.index((a1, v5))]
        else:
            if (a1, v5) not in wanted:
                wanted.append((a1, v5))
            value.append(do_math2(a1, v5))
            record.append((a1, v5))
            wanted.remove((a1, v5))
            v6 = value[-1]
        v7 = copy.deepcopy(zero)
        add(v7, a1)
        sub(v7, one)
        if (v7, v6) in record:
            return value[record.index((v7, v6))]
        else:
            if (v7, v6) not in wanted:
                wanted.append((v7, v6))
            value.append(do_math2(v7, v6))
            record.append((v7, v6))
            wanted.remove((v7, v6))
            return value[-1]


# try:
#     do_math2({'size': 1, 'data': [0x1e]}, {'size': 1, 'data': [0x1e]})
# except:
#     print(len(record))
#     print(len(wanted))

# while len(wanted) != 0:
#     for i in wanted[::-1]:
#         try:
#             value.append(do_math2(*i))
#             record.append(i)
#             wanted.remove(i)
#         except KeyboardInterrupt:
#             input("")
#         except:
#             pass
#     print(len(record))
#     print(len(wanted))

# print(do_math({'size': 1, 'data': [0x1e]}, {'size': 1, 'data': [0x1e]}))

"""
sage: pp = p
....: mods = [p]
....: while True:
....:     pp = euler_phi(pp)
....:     mods.append(pp)
....:     print(pp)
....:     if pp == 1:
....:         break

sage: e = 0
....: rmods = mods[::-1]
....: for phi, m in zip(rmods, rmods[1:]):
....:     assert pow(2, phi + e, m) == pow(2, phi * 2 + e, m)
....:     e = int(pow(2, phi + e, m))
....:     print(e)

In [272]: bytes(ai ^ bi for ai, bi in zip(fromInt(e-3), flag))
Out[272]: b'PCTF{u_r_a_H4CKERMANN}\x02'
"""
