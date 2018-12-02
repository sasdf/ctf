from N import N

files = [
    'sqgate_3858',
    'sqgate_3854',
    'sqgate_3864',
    'sqgate_3866',
    'sqgate_3867',
    'sqgate_3871',
    'sqgate_3876',
    'sqgate_3855',
    'sqgate_3870',
    'sqgate_3873',
    'sqgate_3874',
    'sqgate_3856',
    'sqgate_3861',
    'sqgate_3869',
    'sqgate_3875',
    'sqgate_3860',
    'sqgate_3857',
    'sqgate_3862',
    'sqgate_3865',
    'sqgate_3872',
    'sqgate_3863',
    'sqgate_3859',
    ]


def ccx(args):
    a, b, c = args
    mem[c] ^= (mem[a] & mem[b])


def cx(args):
    a, b = args
    mem[b] ^= mem[a]


def x(args):
    a, = args
    mem[a] ^= True


def swap(args):
    a, b = args
    mem[a], mem[b] = mem[b], mem[a]


funcs = {}
for f in files:
    with open('splits/' + f) as inp:
        data = inp.readlines()
        head, body = data[0], data[2:-1]
        _, _, args = head.strip().split(' ')
        args = args.split(',')
        mapping = {e: i for i, e in enumerate(args)}
        cmds = []
        for line in body:
            cmd, params = line.strip()[:-1].split(' ')
            params = params.split(',')
            params = [mapping[p] for p in params]
            cmds.append((cmd, params))
        funcs[f] = cmds


def run(func, args):
    if func not in funcs:
        return eval(func)(args)
    func = funcs[func]
    for cmd in func:
        gate, params = cmd
        params = [args[p] for p in params]
        run(gate, params)

"""
gate sqgate_3858 a[0:642],su[0:642],n[0:642],o[0:642],x[0:642],y[0:642],sc[0:643],ad,am
"""
mem = [False] * (642 + 642 + 642 + 642 + 642 + 642 + 643 + 2)

off = 642 + 642

for i in N:
    mem[off + i] = True

run('sqgate_3858', list(range(len(mem))))

mem = [e * 1 for e in mem]


def extract(nbits):
    global mem
    a, mem = mem[:nbits], mem[nbits:]
    a = ''.join(reversed(list(map(str, a))))
    return int(a, 2)


a = extract(642)
su = extract(642)
n = extract(642)
o = extract(642)
x = extract(642)
y = extract(642)
sc = extract(643)
aa = extract(1)
ab = extract(1)

print(f'a: {a}')
print(f'su: {su}')
print(f'n: {n}')
print(f'o: {o}')
print(f'x: {x}')
print(f'y: {y}')
print(f'sc: {sc}')
print(f'aa: {aa}')
print(f'ab: {ab}')

