import subprocess
from tqdm import tqdm, trange
import codecs
import random
from random import randrange as rg


def init():
    with open('/dev/urandom', 'rb') as f:
        flag = codecs.encode(f.read(1000), 'base64')
    flag = b'PCTF{' + flag[:random.randrange(20, 100)] + b'}\n'
    with open('./flag-cypress.txt', 'wb') as f:
        f.write(flag)
    flag_time = '2019%02d%02d%02d%02d.%02d' % (rg(1, 5), rg(1, 28), rg(0, 24), rg(0, 60), rg(0, 60))
    img_time = '2019%02d%02d%02d%02d.%02d' % (rg(1, 5), rg(1, 28), rg(0, 24), rg(0, 60), rg(0, 60))
    subprocess.check_call(['touch', '-mt', flag_time, './flag-cypress.txt'])
    subprocess.check_call(['touch', '-mt', img_time, './danny.jpg'])
    subprocess.check_call(['rm', '-rf', 'inpTmp.zip'])
    subprocess.check_call(['zip', 'inpTmp.zip', 'flag-cypress.txt', 'danny.jpg'])


def run(inp, pwd):
    with open('inpTmp', 'wb') as f:
        f.write(inp)
    subprocess.check_call(
        ['./splaid-cypress', '-e', 'inpTmp', '-o', 'outTmp', '-p', pwd],
        )
    with open('outTmp', 'rb') as f:
        ret = f.read()
    assert ret[:4] == b'SPLD'
    return ret[4:-4]


for qq in range(100, 500):
    init()
    with open('/dev/urandom', 'rb') as f:
        pwd = codecs.encode(f.read(1000), 'base64')
    pwd = pwd[:random.randrange(20, 100)]
    with open('./inpTmp.zip', 'rb') as f:
        inp = f.read()

    with open('bits/%d' % qq, 'w') as out:
        size = 0
        for i in trange(len(inp)):
            res = run(inp[:i + 1], pwd)
            byteOff = size // 8
            bitOff = size % 8
            res = res[byteOff:]
            res = ''.join(bin(c)[2:].rjust(8, '0') for c in res).rstrip('0')[:-1]
            res = res[bitOff:]
            size += len(res)
            out.write(hex(inp[i])[2:].rjust(2, '0') + ' ' + res + '\n')

