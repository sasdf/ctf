import re
import os
import contextlib


with contextlib.suppress(FileExistsError):
    os.mkdir('splits')

inp = open('./circuit.qasm')

inp.readline()  # Remove `include  "qelib1.inc";`

cnt = 0
with contextlib.suppress(EOFError):
    while True:
        line = inp.readline()
        if line.startswith('gate '):
            name = line.split(' ')[1]
            assert(re.match(r'^sqgate_[0-9a-f]+$', name))
            with open('splits/%s' % (name), 'w') as f:
                f.write(line)
                while line != '}\n':
                    line = inp.readline()
                    f.write(line)
            cnt += 1
            print(cnt)
        else:
            break

with open('splits/main', 'w') as f:
    f.write(line + inp.read())
