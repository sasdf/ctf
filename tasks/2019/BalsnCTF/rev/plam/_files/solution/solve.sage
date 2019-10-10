from collections import Counter


flagSZ = 96
F = GF(2)


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
    t += s
    p = (f, t)
    v = [[1 - e[-1] for e in g] for g in p]
    p = [[e[:-1] for e in g] for g in p]
    s = Matrix(F, s)
    equPairs.append((s, p, v))


def check(sel):
    ret = [e for s, equs in zip(sel, equPairs) for e in equs[2][s]]
    equs = [e for s, equs in zip(sel, equPairs) for e in equs[1][s]]
    ret = vector(F, ret)
    equs = Matrix(F, equs)
    try:
        sol = equs.solve_right(ret)
        sol = vector(F, sol.list() + [1])
        sel2 = [equs[0] * sol == vector(F, [1]*4) for equs in equPairs]
        sel2 = tuple(e + 0 for e in sel2)
        ret = sel2 == sel
        if ret:
            print(sol, sel2, sel)
        return ret
    except ValueError:
        return False
