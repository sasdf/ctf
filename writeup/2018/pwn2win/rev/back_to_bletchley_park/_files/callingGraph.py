import re
import os
import pickle
import contextlib


with contextlib.suppress(FileExistsError):
    os.mkdir('splits')

inp = open('./circuit.qasm')

inp.readline()  # Remove `include  "qelib1.inc";`

cnt = 0
dep = {}


def readline():
    line = inp.readline()
    if line == '':
        raise EOFError
    return line.strip()


with contextlib.suppress(EOFError):
    while True:
        line = readline()
        if line.startswith('gate '):
            name = line.split(' ')[1]
            assert(re.match(r'^sqgate_[0-9a-f]+$', name))
            assert(name not in dep)
            dep[name] = set()
            readline()
            line = readline()
            while line != '}':
                gate = line.split(' ')[0]
                dep[name].add(gate)
                line = readline()
            cnt += 1
            print(cnt)
        else:
            break

with open('dep2.pkl', 'wb') as f:
    pickle.dump(dep, f)
