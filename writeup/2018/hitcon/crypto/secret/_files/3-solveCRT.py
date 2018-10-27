import libnum
from IPython import embed
import pickle

print('[*] Loading data')
with open('pair.pkl', 'rb') as f:
    data = pickle.load(f)
Cs, Ns = zip(*data)

print('[*] Solving CRT')
s = libnum.solve_crt(Cs, Ns)

print('[*] Solving Root')
k = libnum.nroot(s, 217)

print('[+] Flag (hex):')
print('[>] ' + hex(k))

print('[+] Flag:')
k = libnum.n2s(k)
print('[>] ' + k)
