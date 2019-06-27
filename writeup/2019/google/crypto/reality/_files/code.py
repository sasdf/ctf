import gmpy2
from telnetlib import Telnet


gmpy2.get_context().precision = 2048

xs = []
ys = []
r = Telnet('reality.ctfcompetition.com', 1337)
r.read_until(b'encrypted flag: ')
print('Encrypted flag: ', r.read_until(b'\n'))
r.read_until(b'coefficients')
for _ in range(3):
    r.read_until(b': ')
    c = r.read_until(b'\n').decode()
    x, y = c[:-1].split(', ')
    xs.append(gmpy2.mpfr(x))
    ys.append(gmpy2.mpfr(y))
r.close()

with open("data", 'w') as f:
    for x in xs:
        for i in range(5):
            f.write(str(int(x ** i * 10**450)) + '\n')
    for y in ys:
        f.write(str(int(y * 10**450)) + '\n')


"""sage
with open('data', 'r') as f:
    A = []
    for _ in range(3):
        A.append([Integer(f.readline()) for _ in range(5)])
    A = Matrix(A)
    y = vector([Integer(f.readline()) for _ in range(3)])
Ay = Matrix([r.list() + [v] + [1 if i == j else 0 for j in range(len(y))] for i, (r, v) in enumerate(zip(A, y))])
B = Ay.right_kernel_matrix()
print(-B.LLL()[0])
"""
