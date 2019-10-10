from collections import Counter
from z3 import Bool, Solver, Xor, And, sat, If


flagSZ = 96


with open('../task/task.txt') as f:
    rawdata = f.read()


def group(x):
    ret = []
    while True:
        left = x.find('(')
        right = x.find(')')
        if 0 <= left < right:
            ret.extend(x[:left].strip().split(' '))
            r, x = group(x[left+1:])
            ret.append(r)
        else:
            assert right >= 0
            ret.extend(x[:right].strip().split(' '))
            ret = [e for e in ret if len(e) > 0]
            while len(ret) == 1:
                ret = ret[0]
            return ret, x[right+1:]


data = group(rawdata[1:])
pathes = data[0][0][1][1]
tree = data[0][0][2][4]

stack = []
top = None
for e in tree[3:-1]:
    stack.append(top)
    if e[0] in 'cd':
        if e == 'c':
            top = flagSZ + 1
        elif e == 'd':
            top = flagSZ
        else:
            top = int(e[2:-1])
    elif e[0] in 'hi':
        if e == 'h':
            top = flagSZ + 1
        elif e == 'i':
            top = flagSZ
        else:
            top = int(e[2:-1])
        top = [top, stack[-1], stack[-2]]
        stack = stack[:-2]
    else:
        print('WTF', e)
        exit(0)

assert stack == [None]
root = top


def extractPath(root, path):
    p = path[1:-2]
    p = [flagSZ + 1 - (e == 'e') for e in p]
    p = [p[i:i+2] for i in range(0, len(p), 2)]
    cur = root
    rows = []
    row = []
    for a, b in p:
        if a == cur[0]:
            rows.append(row)
            row = []
        if a == flagSZ:
            cur = cur[1]
        else:
            cur = cur[2]
        row.append(cur[0])
        if b == flagSZ:
            cur = cur[1]
        else:
            cur = cur[2]
    rows = [Counter(row) for row in rows]
    rows = [[row[i] & 1 for i in range(flagSZ+1)] for row in rows]
    return rows


pathes = [p for p in pathes if len(p) == 3]

equPairs = []
for s, t, f in pathes:
    s = extractPath(root, s)
    t = extractPath(root, t)
    f = extractPath(root, f)
    equPairs.append((s, f, t))


varset = [Bool('x%s' % i) for i in range(flagSZ)]
varset.append(True)


def buildexpr(table):
    ret = True
    for row in table:
        expr = False
        assert len(row) == len(varset)
        for e, v in zip(row, varset):
            if e:
                expr = Xor(expr, v)
        ret = And(ret, expr)
    return ret


solver = Solver()
for s, f, t in equPairs:
    s = buildexpr(s)
    f = buildexpr(f)
    t = buildexpr(t)
    solver.add(If(s, t, f))

# Add answer
# for i, v in enumerate(varset):
#     solver.add(v == ((i & 1) != 1))

print('Solving', flush=True)
if solver.check() == sat:
    print('OK')
    print(solver.model())
else:
    print('QAQ')
