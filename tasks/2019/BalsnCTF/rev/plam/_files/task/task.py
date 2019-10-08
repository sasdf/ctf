#!/usr/bin/python3

import sys
import re


flagSZ = 96

flag = input('flag > ').strip()
assert re.match(r'^Balsn\{[0-9a-f]{24}\}$', flag)
flag = bin(int(flag[6:-1], 16))[2:].rjust(flagSZ, '0')
assert len(flag) == flagSZ
flag = list(map(int, flag))

with open('task.txt') as f:
    task = f.read()

def sub(x):
    return chr(ord(x.group(1)) + flag[int(x.group(2))])

task = re.sub(r'(\w)\[([0-9]+)\]', sub, task)

with open('task.plam', 'w') as f:
    f.write(task)
